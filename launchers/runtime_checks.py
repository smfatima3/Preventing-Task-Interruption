"""E0 upstream setup checks. No HRS stages or scientific trials are skipped."""
from concurrent.futures import ThreadPoolExecutor
import datetime
import json
from pathlib import Path
import modal

OUT = Path(__file__).resolve().parents[1] / 'verification' / 'modal'
app = modal.App.lookup('hrs-resource-validation', create_if_missing=True)

HTB = '''set -eu
git clone https://github.com/SNU-PI/HumanoidToolBench.git /opt/htb
cd /opt/htb
git checkout 3fec9bd36933a1648ff7f95468c983f3452243a0
uv run --no-project scripts/setup_evaluation.py
'''
SIMPLE = '''set -eu
nvidia-smi --query-gpu=name,driver_version --format=csv
cd /workspace/simple
pwd
ls -l .venv/bin/python
.venv/bin/python -c 'import simple, mujoco; print("SIMPLE", simple.__version__, "MuJoCo", mujoco.__version__)'
.venv/bin/python -c 'from isaacsim import SimulationApp; app = SimulationApp({"headless": True}); print("HRS_ISAAC_INIT_OK"); app.close()'
'''

def run(name):
    record = {'name':name, 'purpose':'E0 upstream runtime validation only', 'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    sb=None
    try:
        if name=='simple':
            image=modal.Image.from_registry('ghcr.io/physical-superintelligence-lab/simple@sha256:38a674039f413ca171d5f8f841c2b9a9d67771fdaf7bcc73c4777fdfcb7a561f')
            command=SIMPLE
        else:
            image=modal.Image.debian_slim(python_version='3.10').apt_install('git','zstd','libegl1','libopengl0','libgl1','libglib2.0-0').pip_install('uv')
            command=HTB
        sb=modal.Sandbox.create('bash','-lc',command,app=app,image=image,gpu='RTX-PRO-6000',cpu=8,memory=32768,timeout=1800,env={'ACCEPT_EULA':'Y','OMNI_KIT_ACCEPT_EULA':'YES','PRIVACY_CONSENT':'N','PYTHONUNBUFFERED':'1'})
        record['sandbox_id']=sb.object_id
        (OUT/f'{name}_runtime_pending.json').write_text(json.dumps(record,indent=2))
        print(json.dumps(record),flush=True)
        def stream(reader,path):
            with path.open('w',encoding='utf-8') as f:
                for line in reader:
                    f.write(line); f.flush()
        with ThreadPoolExecutor(max_workers=2) as pool:
            a=pool.submit(stream,sb.stdout,OUT/f'{name}_runtime.stdout.log')
            b=pool.submit(stream,sb.stderr,OUT/f'{name}_runtime.stderr.log')
            a.result();b.result()
        sb.wait()
        record['returncode']=sb.returncode
    except Exception as exc:
        record['error']=f'{type(exc).__name__}: {exc}'
    finally:
        if sb is not None:
            sb.terminate()
        record['finished_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        (OUT/f'{name}_runtime.json').write_text(json.dumps(record,indent=2))
    print(json.dumps(record),flush=True)

if __name__=='__main__':
    with modal.enable_output():
        with ThreadPoolExecutor(max_workers=2) as pool:
            list(pool.map(run,['simple','htb']))
