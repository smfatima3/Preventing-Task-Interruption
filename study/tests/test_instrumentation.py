"""Software tests on a tiny MuJoCo model, never HRS humanoid evidence."""
import hashlib
import random
import tempfile
import time
import unittest
from pathlib import Path
import numpy as np
import mujoco
from adapters.mujoco_instrumentation import NativeSnapshotter, contact_samples, AttemptJournal, decide_while_advancing

XML = '<mujoco><option timestep="0.002"/><worldbody><geom name="floor" type="plane" size="2 2 .1"/><body name="ball" pos="0 0 .2"><freejoint/><geom name="ball_geom" type="sphere" size=".1" mass="1"/></body></worldbody></mujoco>'

class Hook:
    def __init__(self): self.state = {'count': 0}
    def capture(self): return self.state
    def restore(self, state): self.state = state

class InstrumentationTests(unittest.TestCase):
    def setUp(self):
        self.model = mujoco.MjModel.from_xml_string(XML)
        self.data = mujoco.MjData(self.model)
        self.hooks = {name: Hook() for name in NativeSnapshotter.REQUIRED_HOOKS}
        self.snap = NativeSnapshotter(self.model, self.data, model_sha256=hashlib.sha256(XML.encode()).hexdigest(), hooks=self.hooks)

    def test_replay_restores_physics_rng_and_mutable_hooks(self):
        for _ in range(100): mujoco.mj_step(self.model, self.data)
        snapshot = self.snap.capture()
        def rollout():
            random_values = (random.random(), np.random.random())
            for _ in range(120): mujoco.mj_step(self.model, self.data)
            return self.data.qpos.copy(), self.data.qvel.copy(), random_values
        first = rollout()
        self.hooks['controller'].state['count'] = 100
        self.snap.restore(snapshot)
        second = rollout()
        np.testing.assert_array_equal(first[0], second[0])
        np.testing.assert_array_equal(first[1], second[1])
        self.assertEqual(first[2], second[2])
        self.assertEqual(self.hooks['controller'].state['count'], 0)

    def test_incomplete_component_state_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Uncaptured'):
            NativeSnapshotter(self.model, self.data, model_sha256='a'*64, hooks={})

    def test_contact_force_units_and_identities(self):
        for _ in range(1500): mujoco.mj_step(self.model, self.data)
        rows = contact_samples(self.model, self.data)
        self.assertTrue(rows)
        self.assertAlmostEqual(sum(r['force_norm_n'] for r in rows), 9.81, delta=.05)
        self.assertEqual(set(rows[0]['geom_names']), {'floor','ball_geom'})
        self.assertAlmostEqual(rows[0]['impulse_increment_ns'], rows[0]['force_norm_n']*.002)

    def test_decision_delay_advances_physics_and_isolates_observation(self):
        obs = {'x': [1]}
        def policy(detached):
            detached['x'][0]=9
            time.sleep(.01)
            return [0.]
        result = decide_while_advancing(observation=obs, policy=policy,
            step_holding=lambda: mujoco.mj_step(self.model,self.data),
            simulation_time=lambda: float(self.data.time), added_delay_ms=10, deadline_ms=500)
        self.assertEqual(obs['x'],[1])
        self.assertFalse(result['deadline_miss'])
        self.assertGreaterEqual(self.data.time,.02)
        self.assertLessEqual(result['decision_time_s'],result['action_start_time_s'])

    def test_late_response_is_discarded(self):
        result = decide_while_advancing(observation={}, policy=lambda _: time.sleep(.1),
            step_holding=lambda: mujoco.mj_step(self.model,self.data),
            simulation_time=lambda: float(self.data.time), added_delay_ms=0, deadline_ms=10)
        self.assertTrue(result['deadline_miss'])
        self.assertIsNone(result['action'])
        self.assertGreaterEqual(self.data.time,.01)

    def test_failed_attempt_is_retained_and_cannot_be_rewritten(self):
        with tempfile.TemporaryDirectory() as td:
            journal = AttemptJournal(Path(td), {'data_kind':'synthetic_software_test'})
            journal.append({'event':'fixture'})
            result = journal.finish('controller_failure',failure_reason='software test')
            self.assertTrue((journal.directory/'completion.json').is_file())
            self.assertEqual(result['raw_trace_sha256'],hashlib.sha256(journal.trace_path.read_bytes()).hexdigest())
            with self.assertRaises(RuntimeError): journal.finish('complete')

if __name__=='__main__': unittest.main()
