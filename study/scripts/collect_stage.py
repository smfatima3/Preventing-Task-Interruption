#!/usr/bin/env python3
import argparse, importlib, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from hrs import workflow
from hrs.records import load_records, ValidationError
def main():
    p=argparse.ArgumentParser(description='Execute a real user-supplied simulator adapter')
    p.add_argument('stage'); a=p.parse_args()
    workflow.require_clean(ROOT); _,stage,state=workflow.eligible(ROOT,a.stage)
    if not stage['requires_records']: raise ValidationError('This stage is documentary; use its evidence template')
    if state['stages'][a.stage]['status']!='running': raise ValidationError('Begin this stage first')
    protocol=workflow.read_json(ROOT/'config/protocol.json'); spec=protocol['resources']['adapter_module']
    if not spec or ':' not in spec: raise ValidationError('Configure adapter_module as module:Class; no simulator is bundled')
    module,cls=spec.split(':',1); adapter=getattr(importlib.import_module(module),cls)()
    output=Path(adapter.execute_registered_stage(ROOT,a.stage,protocol,workflow.read_json(ROOT/'config/final_lock.json'))).resolve()
    if not output.is_relative_to(ROOT/'results/raw'): raise ValidationError('Measured output must be under results/raw')
    rows=load_records(output,ROOT,stage_id=a.stage)
    print(f'Validated {len(rows)} measured records at {output}. Stage still requires evidence review.')
if __name__=='__main__':
    try: main()
    except (ValueError,OSError,ImportError,NotImplementedError,AttributeError) as e: print('BLOCKED: '+str(e),file=sys.stderr); sys.exit(2)

