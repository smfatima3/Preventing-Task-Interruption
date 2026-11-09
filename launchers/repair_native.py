import json
from pathlib import Path
import modal
import simple_diagnostics as diagnostics

diagnostics.IMAGE=modal.Image.from_id('im-01M6ZHBRD6ZWG9RTVRJM3M6CYD')
original=diagnostics.COMMANDS['simple_native'][1]
repair='''set -eu
cd /workspace/simple
.venv/bin/python - <<'PY'
from pathlib import Path
import hashlib, urllib.request
for p in Path('src/simple/robots/policy').glob('*.pt'):
    if p.stat().st_size>1024: continue
    lines=p.read_text().splitlines()
    expected=next(x.split('sha256:')[1] for x in lines if x.startswith('oid '))
    url='https://media.githubusercontent.com/media/physical-superintelligence-lab/SIMPLE/b75c6786f87b4a7f43b52b0ac5b83a1d9ea62e11/'+str(p)
    data=urllib.request.urlopen(url,timeout=120).read()
    actual=hashlib.sha256(data).hexdigest()
    if actual!=expected: raise RuntimeError('Checkpoint hash mismatch: '+str(p))
    p.write_bytes(data)
    print('VERIFIED_CHECKPOINT',str(p),len(data),actual,flush=True)
PY
'''
diagnostics.COMMANDS['simple_native_repaired']=('RTX-PRO-6000',repair+original)
# Retain the successfully repaired runtime even if the next integration check fails.
source=Path(diagnostics.__file__).read_text()
source=source.replace("if name=='simple_native':", "if name.startswith('simple_native'):")
namespace={**diagnostics.__dict__,'__name__':'repair_driver'}
exec(compile(source,diagnostics.__file__,'exec'),namespace)
namespace['IMAGE']=diagnostics.IMAGE
namespace['COMMANDS']=diagnostics.COMMANDS
namespace['run']('simple_native_repaired')
