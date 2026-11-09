"""Retained, bounded infrastructure attempts after the RTX/Isaac crash."""
import concurrent.futures
import datetime
import json
from pathlib import Path
import modal

OUT=Path(__file__).resolve().parents[1]/'verification'/'modal'
APP=modal.App.lookup('hrs-resource-validation',create_if_missing=True)
IMAGE=modal.Image.from_registry('ghcr.io/physical-superintelligence-lab/simple@sha256:38a674039f413ca171d5f8f841c2b9a9d67771fdaf7bcc73c4777fdfcb7a561f').add_local_dir(str(Path(__file__).resolve().parents[1]/'study'),'/hrs',ignore=['__pycache__','releases'])

COMMANDS={
 'isaac_l40s': ('L40S', '''set -eu
cd /workspace/simple
nvidia-smi --query-gpu=name,driver_version --format=csv
.venv/bin/python -c 'import torch; from isaacsim import SimulationApp; app=SimulationApp({"headless":True,"multi_gpu":False}); print("HRS_ISAAC_INIT_OK",flush=True); app.close()'
'''),
 'simple_native': ('RTX-PRO-6000', '''set -eu
cd /workspace/simple
git rev-parse HEAD || true
find src/simple/robots/policy -name '*.pt' -printf '%p %s bytes\\n'
PYTHONPATH=/hrs .venv/bin/python -m unittest discover -s /hrs/tests -p test_instrumentation.py -v
MUJOCO_GL=egl .venv/bin/python - <<'PY'
import json
import gymnasium as gym
import simple.envs
env=gym.make('simple/G1WholebodyBendPickMP-v0', target='primitive:cube', sim_mode='mujoco', headless=True)
obs,info=env.reset(seed=11)
print('HRS_NATIVE_ENV_RESET_OK',json.dumps({'nq':env.unwrapped.mujoco.mjModel.nq,'nv':env.unwrapped.mujoco.mjModel.nv,'time':float(env.unwrapped.mujoco.mjData.time),'obs_keys':list(obs)}),flush=True)
env.close()
PY
''')}

def run(name):
    gpu,command=COMMANDS[name]
    record={'name':name,'gpu_requested':gpu,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'E0 runtime diagnostics / software tests only'}
    sb=None
    try:
        sb=modal.Sandbox.create('sleep','1200',app=APP,image=IMAGE,gpu=gpu,cpu=8,memory=32768,timeout=1250,env={'ACCEPT_EULA':'Y','OMNI_KIT_ACCEPT_EULA':'YES','PRIVACY_CONSENT':'N','PYTHONUNBUFFERED':'1','NVIDIA_DRIVER_CAPABILITIES':'all'})
        record['sandbox_id']=sb.object_id
        (OUT/f'{name}_pending.json').write_text(json.dumps(record,indent=2))
        print(json.dumps(record),flush=True)
        process=sb.exec('bash','-lc',command,timeout=900)
        def stream(reader,path):
            with path.open('w',encoding='utf-8') as handle:
                for line in reader:
                    handle.write(line);handle.flush()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            a=pool.submit(stream,process.stdout,OUT/f'{name}.stdout.log')
            b=pool.submit(stream,process.stderr,OUT/f'{name}.stderr.log')
            a.result();b.result()
        record['returncode']=process.wait()
        if name=='simple_native':
            try:
                record['snapshot_image_id']=sb.snapshot_filesystem(timeout=55).object_id
            except Exception as exc:
                record['snapshot_error']=f'{type(exc).__name__}: {exc}'
    except Exception as exc:
        record['error']=f'{type(exc).__name__}: {exc}'
    finally:
        if sb is not None: sb.terminate()
        record['finished_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        (OUT/f'{name}.json').write_text(json.dumps(record,indent=2))
    print(json.dumps(record),flush=True)

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run,COMMANDS))
