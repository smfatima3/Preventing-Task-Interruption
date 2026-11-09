"""Bounded E0 infrastructure probes; never scientific outcome records."""
import concurrent.futures
import datetime
import json
from pathlib import Path
import modal

OUT = Path(__file__).resolve().parents[1] / 'verification' / 'modal'
OUT.mkdir(exist_ok=True)
app = modal.App.lookup('hrs-resource-validation', create_if_missing=True)
image = modal.Image.debian_slim(python_version='3.10').pip_install('mujoco==3.3.6')
probe = '''import json, platform, subprocess
import mujoco
print(json.dumps({'python': platform.python_version(), 'mujoco': mujoco.__version__}))
subprocess.run(['nvidia-smi', '--query-gpu=name,uuid,memory.total,driver_version', '--format=csv'], check=True)
'''

def run(gpu):
    record = {'gpu_requested': gpu, 'purpose': 'E0 infrastructure only', 'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    sb = None
    try:
        sb = modal.Sandbox.create('python', '-c', probe, app=app, image=image, gpu=gpu, timeout=120, cpu=2, memory=4096)
        record['sandbox_id'] = sb.object_id
        print(json.dumps({'gpu': gpu, 'sandbox_id': sb.object_id}), flush=True)
        record['stdout'] = sb.stdout.read()
        record['stderr'] = sb.stderr.read()
        sb.wait()
        record['returncode'] = sb.returncode
    except Exception as exc:
        record['error'] = f'{type(exc).__name__}: {exc}'
    finally:
        if sb is not None:
            sb.terminate()
        record['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        (OUT / (gpu.replace('!', '') + '.json')).write_text(json.dumps(record, indent=2), encoding='utf-8')
    return record

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(run, ['H100!', 'RTX-PRO-6000']):
            print(json.dumps(result), flush=True)
