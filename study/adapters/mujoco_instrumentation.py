"""Physics instrumentation for SIMPLE's native MuJoCo state.

This is shared infrastructure, not a complete experiment adapter or E1 evidence.
All non-physics state must have explicit hooks before a causal replay is valid.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import random
import threading
import time
from typing import Callable, Mapping, Protocol
import uuid

import mujoco
import numpy as np


class StateHook(Protocol):
    def capture(self): ...
    def restore(self, state): ...


@dataclass
class Snapshot:
    model_sha256: str
    physics: np.ndarray
    auxiliary: dict
    numpy_rng: tuple
    python_rng: tuple


class NativeSnapshotter:
    """Capture integration state plus declared controller/task/sensor/RNG hooks.

    External DDS/SONIC processes cannot be replayed by this class unless their
    state is exported by a supplied hook. Do not claim a full-state replay from
    qpos/qvel alone. Model mutations require a different snapshotter instance.
    """
    REQUIRED_HOOKS = {'controller', 'task', 'human_motion', 'sensor', 'scheduler'}

    def __init__(self, model, data, *, model_sha256: str, hooks: Mapping[str, StateHook]):
        if len(model_sha256) != 64 or any(c not in '0123456789abcdef' for c in model_sha256):
            raise ValueError('A verified model/asset manifest SHA-256 is required')
        missing = self.REQUIRED_HOOKS - hooks.keys()
        if missing:
            raise ValueError(f'Uncaptured simulator components: {sorted(missing)}')
        self.model, self.data = model, data
        self.model_sha256, self.hooks = model_sha256, dict(hooks)
        self.spec = mujoco.mjtState.mjSTATE_INTEGRATION

    def capture(self):
        state = np.empty(mujoco.mj_stateSize(self.model, self.spec), dtype=np.float64)
        mujoco.mj_getState(self.model, self.data, state, self.spec)
        if not np.isfinite(state).all():
            raise ValueError('Cannot save nonfinite simulator state')
        return Snapshot(self.model_sha256, state,
                        {name: copy.deepcopy(hook.capture()) for name, hook in self.hooks.items()},
                        copy.deepcopy(np.random.get_state()), copy.deepcopy(random.getstate()))

    def restore(self, snapshot: Snapshot):
        if snapshot.model_sha256 != self.model_sha256 or set(snapshot.auxiliary) != set(self.hooks):
            raise ValueError('Snapshot model or component inventory differs')
        expected = mujoco.mj_stateSize(self.model, self.spec)
        if snapshot.physics.shape != (expected,) or not np.isfinite(snapshot.physics).all():
            raise ValueError('Invalid integration state')
        for name, hook in self.hooks.items():
            hook.restore(copy.deepcopy(snapshot.auxiliary[name]))
        mujoco.mj_setState(self.model, self.data, snapshot.physics.copy(), self.spec)
        # Forward rebuilds derived fields; restore integration state afterward
        # because mj_forward may change warm-start state used by the solver.
        mujoco.mj_forward(self.model, self.data)
        mujoco.mj_setState(self.model, self.data, snapshot.physics.copy(), self.spec)
        np.random.set_state(copy.deepcopy(snapshot.numpy_rng))
        random.setstate(copy.deepcopy(snapshot.python_rng))


def contact_samples(model, data):
    """Capture actual solver force, identities and per-step impulse increments.

    A step impulse is not an event impulse; callers must aggregate continuous
    contact intervals by declared body pair and preserve all samples.
    """
    rows = []
    dt = float(model.opt.timestep)
    for index in range(data.ncon):
        contact = data.contact[index]
        wrench = np.zeros(6)
        mujoco.mj_contactForce(model, data, index, wrench)
        if not np.isfinite(wrench).all():
            raise ValueError('Nonfinite contact wrench')
        geom_ids = [int(contact.geom1), int(contact.geom2)]
        body_ids = [int(model.geom_bodyid[g]) for g in geom_ids]
        norm = float(np.linalg.norm(wrench[:3]))
        rows.append({
            'simulation_time_s': float(data.time), 'physics_timestep_s': dt,
            'geom_ids': geom_ids,
            'geom_names': [mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, g) for g in geom_ids],
            'body_ids': body_ids,
            'body_names': [mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, b) for b in body_ids],
            'position_m': contact.pos.copy().tolist(), 'contact_frame': contact.frame.copy().tolist(),
            'distance_m': float(contact.dist), 'wrench_contact_frame': wrench.tolist(),
            'force_norm_n': norm, 'impulse_increment_ns': norm * dt,
        })
    return rows


class AttemptJournal:
    """Exclusive per-attempt trace and immutable completion/failure metadata."""
    def __init__(self, directory: Path, metadata: dict):
        self.run_id = uuid.uuid4().hex
        self.directory = Path(directory) / self.run_id
        self.directory.mkdir(parents=True, exist_ok=False)
        self.trace_path = self.directory / 'trace.jsonl'
        self.trace = self.trace_path.open('x', encoding='utf-8')
        self.metadata = {**metadata, 'run_id': self.run_id}
        (self.directory / 'attempt.json').write_text(json.dumps(self.metadata, indent=2, allow_nan=False), encoding='utf-8')
        self.closed = False

    def append(self, row: dict):
        if self.closed:
            raise RuntimeError('Attempt already finalized')
        self.trace.write(json.dumps(row, allow_nan=False) + '\n')
        self.trace.flush()

    def finish(self, status: str, *, failure_reason=None):
        if self.closed:
            raise RuntimeError('Refusing to overwrite an attempted run')
        if status not in {'complete', 'timeout', 'controller_failure', 'infrastructure_failure'}:
            raise ValueError('Unrecognized attempt status')
        if status != 'complete' and not failure_reason:
            raise ValueError('Failed attempts require a reason')
        self.trace.close()
        self.closed = True
        digest = hashlib.sha256(self.trace_path.read_bytes()).hexdigest()
        result = {**self.metadata, 'status': status, 'raw_trace_sha256': digest,
                  'failure_reason': failure_reason}
        with (self.directory / 'completion.json').open('x', encoding='utf-8') as stream:
            json.dump(result, stream, indent=2, allow_nan=False)
        return result


def decide_while_advancing(*, observation: dict, policy: Callable, step_holding: Callable,
                           simulation_time: Callable, added_delay_ms: float,
                           deadline_ms: float):
    """Run a policy on a detached observation while holding advances physics.

    The simulation follows at least elapsed wall time, including injected delay.
    The policy must be a bounded local call. A timed-out response is discarded;
    its daemon thread cannot access physics or replace the active controller.
    """
    if added_delay_ms < 0 or deadline_ms <= 0:
        raise ValueError('Invalid delay/deadline')
    done = threading.Event()
    outcome = {}
    frozen_observation = copy.deepcopy(observation)
    wall_start, sim_start = time.perf_counter(), simulation_time()

    def compute():
        try:
            outcome['action'] = policy(frozen_observation)
        except Exception as exc:
            outcome['error'] = f'{type(exc).__name__}: {exc}'
        finally:
            outcome['compute_s'] = time.perf_counter() - wall_start
            done.set()

    threading.Thread(target=compute, daemon=True).start()
    while True:
        elapsed = time.perf_counter() - wall_start
        timed_out = elapsed * 1000 >= deadline_ms
        ready = done.is_set() and elapsed >= outcome['compute_s'] + added_delay_ms / 1000
        while simulation_time() - sim_start < elapsed:
            before = simulation_time()
            step_holding()
            if simulation_time() <= before:
                raise RuntimeError('Holding step did not advance physics')
        if ready or timed_out:
            break
        done.wait(min(.001, max(0., deadline_ms / 1000 - elapsed))) if not done.is_set() else time.sleep(.001)
    return {
        'action': None if timed_out else outcome.get('action'),
        'error': 'decision deadline exceeded' if timed_out else outcome.get('error'),
        'deadline_miss': timed_out, 'observation_time_s': sim_start,
        'decision_time_s': sim_start + outcome.get('compute_s', elapsed),
        'action_start_time_s': simulation_time(), 'latency_ms': elapsed * 1000,
        'added_delay_ms': added_delay_ms,
    }
