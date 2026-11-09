#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from hrs.records import load_records, ValidationError
def main():
    p=argparse.ArgumentParser(description='Validate real measured JSONL records and trace hashes')
    p.add_argument('path'); a=p.parse_args()
    rows=load_records(a.path,ROOT)
    print(json.dumps({'validated_rows':len(rows),'stages':sorted({r['stage_id'] for r in rows}),
                      'noncomplete_attempts':sum(r['status']!='complete' for r in rows),
                      'notice':'Schema validation is not scientific validity or claim support.'},indent=2))
if __name__=='__main__':
    try: main()
    except (ValueError,OSError,KeyError) as e: print('BLOCKED: '+str(e),file=sys.stderr); sys.exit(2)

