#!/usr/bin/env python3
import datetime, json, sys, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from hrs import workflow
from hrs.records import digest,ValidationError
def main():
    workflow.require_clean(ROOT)
    state=workflow.read_json(ROOT/'state/status.json')['stages']
    pending=[k for k,v in state.items() if v['status'] not in ('passed','skipped')]
    label='INCOMPLETE' if pending else 'AUDITED'
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    folder=ROOT/'releases'; folder.mkdir(exist_ok=True)
    files=[p for p in ROOT.rglob('*') if p.is_file() and not {'__pycache__','releases','.venv','.git'}&set(p.relative_to(ROOT).parts) and p.suffix!='.pyc']
    manifest={'release_status':label,'incomplete_stages':pending,'notice':'Software verification is separate from measured robotics evidence. Audit does not itself prove a hypothesis.',
              'files':{str(p.relative_to(ROOT)):digest(p) for p in sorted(files)}}
    out=folder/f'HRS_results_{label}_{stamp}.zip'
    with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files): z.write(p,str(p.relative_to(ROOT)))
        z.writestr('RELEASE_MANIFEST.json',json.dumps(manifest,indent=2))
    print(out)
if __name__=='__main__':
    try: main()
    except (ValueError,OSError) as e: print('BLOCKED: '+str(e),file=sys.stderr); sys.exit(2)
