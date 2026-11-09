#!/usr/bin/env python3
import argparse,csv,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from hrs.records import digest,ValidationError
from hrs import workflow

def main():
    p=argparse.ArgumentParser(description='Plot measured primary summaries; no expected-result plots')
    p.add_argument('--stage',required=True,choices=['E6','E7']); a=p.parse_args()
    workflow.require_clean(ROOT)
    dest=ROOT/f'results/computed/{a.stage}'
    provenance=json.loads((dest/'paired_primary.json').read_text())
    if provenance['input_sha256']!=digest(ROOT/f'results/raw/{a.stage}/records.jsonl'): raise ValidationError('Summary is stale')
    if provenance['final_lock_sha256']!=digest(ROOT/'config/final_lock.json'): raise ValidationError('Lock changed')
    if workflow.read_json(ROOT/'state/status.json')['stages'][a.stage]['status']=='passed':
        raise ValidationError('Stage is sealed; generate plots before finishing the stage')
    rows=list(csv.DictReader((dest/'method_summary.csv').open()))
    if not rows: raise ValidationError('No measured summaries')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    means=[float(r['human_hazard_rate'])*100 for r in rows]
    lows=[m-float(r['human_hazard_ci95_low'])*100 for m,r in zip(means,rows)]
    highs=[float(r['human_hazard_ci95_high'])*100-m for m,r in zip(means,rows)]
    fig,ax=plt.subplots(figsize=(7,4.5),layout='constrained')
    ax.errorbar(range(len(rows)),means,yerr=[lows,highs],fmt='o',capsize=4,color='#255d82')
    ax.set_xticks(range(len(rows)),[r['method'] for r in rows]); ax.set_ylabel('Human-contact scenarios (%)')
    ax.set_title(f'{a.stage}: measured human-contact outcomes')
    ax.grid(axis='y',alpha=.25); ax.set_ylim(bottom=0)
    fig.text(.5,.01,'95% exact per-method event-rate intervals; use paired analysis for comparisons.',ha='center',fontsize=8)
    fig.savefig(dest/'human_hazard_rates.pdf',bbox_inches='tight'); fig.savefig(dest/'human_hazard_rates.png',dpi=200,bbox_inches='tight'); plt.close(fig)
    print(f'Wrote measured plot to {dest}')
if __name__=='__main__':
    try: main()
    except (OSError,ValueError,KeyError) as e: print('BLOCKED: '+str(e),file=sys.stderr); sys.exit(2)

