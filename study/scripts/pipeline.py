#!/usr/bin/env python3
import argparse, importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from hrs import workflow
from hrs.records import ValidationError, digest

def main():
    p=argparse.ArgumentParser(description='HRS sequential evidence workflow; no physics is simulated by this command')
    sub=p.add_subparsers(dest='command',required=True)
    for name in ('status','audit','doctor'): sub.add_parser(name)
    b=sub.add_parser('begin'); b.add_argument('stage')
    f=sub.add_parser('finish'); f.add_argument('stage'); f.add_argument('--evidence',required=True)
    s=sub.add_parser('skip'); s.add_argument('stage'); s.add_argument('--reason',required=True)
    h=sub.add_parser('hash'); h.add_argument('paths',nargs='+')
    a=p.parse_args()
    if a.command=='status':
        _,seq,state=workflow.setup(ROOT)
        for st in seq: print(f"{st['id']:3} {state['stages'][st['id']]['status']:8} {st['title']}")
        print('Stage completion does not imply hypothesis support.')
    elif a.command=='audit':
        issues=workflow.audit(ROOT)
        print(json.dumps({'audit_integrity':'PASS' if not issues else 'FAIL','issues':issues,'scientific_completion':all(x['status'] in ('passed','skipped') for x in workflow.read_json(ROOT/'state/status.json')['stages'].values())},indent=2))
        return 1 if issues else 0
    elif a.command=='doctor':
        print(json.dumps({'python':sys.version.split()[0],
            'analysis_dependencies':{m:bool(importlib.util.find_spec(m)) for m in ('numpy','scipy','matplotlib')},
            'resources':workflow.read_json(ROOT/'config/protocol.json')['resources'],
            'notice':'No simulator, trained policies or measured scientific results bundled.'},indent=2))
    elif a.command=='begin': workflow.begin(ROOT,a.stage); print(f'{a.stage} running; produce actual evidence before finish.')
    elif a.command=='finish': workflow.finish(ROOT,a.stage,Path(a.evidence)); print(f'{a.stage}: {workflow.read_json(ROOT/"state/status.json")["stages"][a.stage]["status"]}')
    elif a.command=='skip': workflow.skip_optional(ROOT,a.stage,a.reason); print(f'{a.stage} explicitly skipped.')
    elif a.command=='hash':
        for path in a.paths: print(digest(path)+'  '+str(path))
    return 0

if __name__=='__main__':
    try: sys.exit(main())
    except (ValidationError,OSError,KeyError,ValueError) as e: print('BLOCKED: '+str(e),file=sys.stderr); sys.exit(2)

