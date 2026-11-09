#!/usr/bin/env python3
import argparse, csv, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from hrs import workflow
from hrs.records import load_records, check_registry, primary_pairs, ValidationError, digest
from hrs.analysis import summarize, primary_analysis

def main():
    p=argparse.ArgumentParser(description='Analyze frozen measured E6/E7 outcomes; refuses empty/synthetic/incomplete data')
    p.add_argument('--stage',required=True,choices=['E6','E7'])
    p.add_argument('--reproduce-to',help='New directory under verification/reproductions; never overwrites sealed results')
    a=p.parse_args()
    workflow.require_clean(ROOT)
    state=workflow.read_json(ROOT/'state/status.json')['stages']
    if state['E5']['status']!='passed': raise ValidationError('E5 must pass before confirmatory analysis')
    if state[a.stage]['status'] not in ('running','passed'): raise ValidationError('Stage not started')
    lock=workflow.final_lock_valid(ROOT); path=ROOT/f'results/raw/{a.stage}/records.jsonl'
    rows=load_records(path,ROOT,stage_id=a.stage); check_registry(rows,ROOT,lock,a.stage)
    for r in rows:
        expected=lock['primary_policy_sha256'] if r['method']=='M' else lock['baseline_policy_sha256'][r['method']]
        if r['policy_sha256']!=expected or r['config_sha256']!=digest(ROOT/'config/final_lock.json'):
            raise ValidationError('Policy/config differs from final lock')
    for method in lock['included_methods']:
        if method!='M': primary_pairs(rows,method,a.stage,lock)
    pairs=primary_pairs(rows,lock['primary_comparator'],a.stage,lock)
    summary=summarize(rows); result=primary_analysis(pairs,lock,a.stage)
    result['input_sha256']=digest(path); result['final_lock_sha256']=digest(ROOT/'config/final_lock.json')
    result['hierarchy_status']='E6 is the first confirmatory endpoint; scientific audit remains required'
    if a.stage=='E7':
        prior_path=ROOT/'results/computed/E6/paired_primary.json'
        if not prior_path.exists(): raise ValidationError('E6 analysis is required before E7 hierarchy interpretation')
        prior=json.loads(prior_path.read_text())
        if prior['input_sha256']!=digest(ROOT/'results/raw/E6/records.jsonl') or prior['final_lock_sha256']!=result['final_lock_sha256']:
            raise ValidationError('Stale E6 analysis')
        previous=bool(prior['human_hazard']['superiority_screen'])
        result['hierarchy_status']='Prior E6 statistical screen passed' if previous else 'E6 screen not passed; E7 claim tests remain descriptive'
        result['utility_claim_statistical_screen']=bool(previous and result['human_hazard']['superiority_screen'] and result['task_success']['noninferiority_screen'])
    dest=ROOT/f'results/computed/{a.stage}'
    if a.reproduce_to:
        dest=Path(a.reproduce_to).resolve()
        if not dest.is_relative_to(ROOT/'verification/reproductions') or dest.exists():
            raise ValidationError('Reproduction destination must be a new directory under verification/reproductions')
    # Do not overwrite sealed analysis. A genuine correction needs a documented new protocol/version.
    if state[a.stage]['status']=='passed' and not a.reproduce_to: raise ValidationError('Stage is sealed; use --reproduce-to with a new verification/reproductions directory')
    dest.mkdir(parents=True,exist_ok=True)
    with (dest/'method_summary.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0])); w.writeheader(); w.writerows(summary)
    workflow.save_json(dest/'paired_primary.json',result)
    h=result['human_hazard']; u=result['task_success']
    report=f'''# Measured {a.stage} analysis

Comparator: {lock['primary_comparator']}. Independent paired scenarios: {len(pairs)}.

Human-hazard difference M minus comparator: {100*h['difference']:.3f} percentage points; 95% paired interval [{100*h['ci95'][0]:.3f}, {100*h['ci95'][1]:.3f}]. Counts: M {h['n_m']}/{len(pairs)}, comparator {h['n_comparator']}/{len(pairs)}. Exact paired two-sided p: {h['exact_mcnemar_two_sided_p']:.6g}.

Task-success difference: {100*u['difference']:.3f} percentage points; 95% paired interval [{100*u['ci95'][0]:.3f}, {100*u['ci95'][1]:.3f}]. This is a full-episode utility endpoint only for E7.

Hierarchy: {result['hierarchy_status']}.

These are measured statistical estimates, not an automatic conclusion of safety. Review degeneracy flags, exact event-rate intervals, harm components, physics validity, baseline fidelity and missing-data handling before writing a claim. No certification or injury conclusion follows.
'''
    (dest/'interpretation.md').write_text(report)
    print(f'Wrote measured outputs to {dest}')

if __name__=='__main__':
    try: main()
    except (ValueError,OSError,KeyError) as e: print('BLOCKED: '+str(e),file=sys.stderr); sys.exit(2)

