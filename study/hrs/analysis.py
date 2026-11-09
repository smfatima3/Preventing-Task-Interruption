"""Paired scenario statistics. Scientific interpretation still requires review."""
import math
import numpy as np
from scipy.stats import beta, binomtest
from .records import ValidationError, human_hazard, safe_success

def exact_rate_interval(k,n,alpha=0.05):
    if not 0<=k<=n or n<1: raise ValueError('Invalid binomial counts')
    return [0.0 if k==0 else float(beta.ppf(alpha/2,k,n-k+1)),
            1.0 if k==n else float(beta.ppf(1-alpha/2,k+1,n-k))]

def bootstrap_difference(differences,tasks,resamples=10000,seed=20261104):
    d=np.asarray(differences,dtype=float); t=np.asarray(tasks)
    if d.ndim!=1 or len(d)<2 or len(t)!=len(d) or not np.isfinite(d).all():
        raise ValueError('At least two finite paired scenario differences with matching strata required')
    if resamples<10000: raise ValueError('Use at least 10,000 resamples')
    rng=np.random.default_rng(seed); boot=np.empty(resamples)
    groups=[d[t==x] for x in sorted(set(tasks))]
    for start in range(0,resamples,250):
        n=min(250,resamples-start); totals=np.zeros(n)
        for g in groups: totals+=g[rng.integers(0,len(g),size=(n,len(g)))].sum(axis=1)
        boot[start:start+n]=totals/len(d)
    ci=np.quantile(boot,[0.025,0.975]).tolist()
    return {'n_scenarios':len(d),'difference':float(d.mean()),'ci95':ci,
            'bootstrap_resamples':resamples,'analysis_seed':seed,
            'degenerate':bool(np.all(d==d[0])),
            'strata_with_one_scenario':[str(x) for x in sorted(set(tasks)) if np.sum(t==x)<2]}

def paired_binary(a,b,tasks,resamples=10000,seed=20261104):
    a=np.asarray(a); b=np.asarray(b)
    if len(a)!=len(b) or not set(a.tolist()+b.tolist())<={0,1}: raise ValueError('Paired binary vectors required')
    result=bootstrap_difference(a-b,tasks,resamples,seed)
    introduced=int(np.sum((a==1)&(b==0))); prevented=int(np.sum((a==0)&(b==1)))
    discord= introduced+prevented
    result.update(n_m=int(a.sum()),n_comparator=int(b.sum()),introduced=introduced,prevented=prevented,
                  m_rate_ci95=exact_rate_interval(int(a.sum()),len(a)),
                  comparator_rate_ci95=exact_rate_interval(int(b.sum()),len(b)),
                  exact_mcnemar_two_sided_p=1.0 if discord==0 else float(binomtest(introduced,discord,0.5).pvalue),
                  relative_risk=None if int(b.sum())==0 else float(a.mean()/b.mean()))
    result['superiority_screen']=bool(result['ci95'][1]<0 and result['exact_mcnemar_two_sided_p']<0.05 and not result['degenerate'] and not result['strata_with_one_scenario'])
    return result

def summarize(rows):
    if any(r['status']!='complete' for r in rows): raise ValidationError('Incomplete rows cannot be silently dropped')
    result=[]
    for method in sorted({r['method'] for r in rows}):
        rr=[r for r in rows if r['method']==method]
        if len({r['scenario_id'] for r in rr})!=len(rr): raise ValidationError('Descriptive primary table requires one row per base scenario/method')
        n=len(rr); k=sum(human_hazard(r) for r in rr)
        lat=[x for r in rr for x in r['measurements']['latencies_ms']]
        item={'method':method,'n_scenarios':n,'human_hazards':k,'human_hazard_rate':k/n,
              'human_hazard_ci95_low':exact_rate_interval(k,n)[0],'human_hazard_ci95_high':exact_rate_interval(k,n)[1],
              'safe_successes':sum(safe_success(r) for r in rr),
              'latency_p50_ms':float(np.quantile(lat,.5)),'latency_p95_ms':float(np.quantile(lat,.95)),
              'latency_p99_ms':float(np.quantile(lat,.99)),'n_latency_observations':len(lat)}
        for key in ('robot_human_contact','object_human_contact','object_drop','robot_fall','limit_violation','task_success','aborted','unresolved'):
            item[key+'_count']=sum(r['measurements'][key] for r in rr)
        for key in ('max_contact_impulse_ns','peak_contact_force_n','max_object_impact_energy_j'):
            values=[r['measurements'][key] for r in rr]
            item[key+'_mean']=float(np.mean(values)); item[key+'_p95']=float(np.quantile(values,.95)); item[key+'_max']=max(values)
        item['deadline_misses']=sum(r['measurements']['deadline_misses'] for r in rr)
        result.append(item)
    return result

def primary_analysis(pairs,lock,stage_id):
    tasks=[a['task'] for a,b in pairs]
    kwargs={'resamples':lock['bootstrap_resamples'],'seed':lock['analysis_seed']}
    hazard=paired_binary([human_hazard(a) for a,b in pairs],[human_hazard(b) for a,b in pairs],tasks,**kwargs)
    success=paired_binary([int(a['measurements']['task_success']) for a,b in pairs],
                          [int(b['measurements']['task_success']) for a,b in pairs],tasks,**kwargs)
    success['noninferiority_screen']=bool(success['ci95'][0]>-lock['noninferiority_margin'] and not success['degenerate'] and not success['strata_with_one_scenario'])
    return {'stage_id':stage_id,'primary_comparator':lock['primary_comparator'],
            'human_hazard':hazard,'task_success':success,'noninferiority_margin':lock['noninferiority_margin'],
            'status':'Measured analysis; screens are not a final scientific claim',
            'limitations':['Bootstrap degeneracy requires additional inference; zero events do not prove zero risk.',
                           'Task-stratified intervals target the empirical benchmark mixture.',
                           'E6 task success is descriptive; the utility claim requires E7 and the declared hierarchy.',
                           'Physics validity, baseline fidelity, harm transfer and missing-data handling require separate audit.']}

def clustered_repeated_difference(rows,method_a,method_b,metric,condition_keys,resamples=10000,seed=20261104):
    """Average matched-condition differences within each scenario, then bootstrap scenarios.

    Conditions must form an identical planned grid for every scene. Unequal/missing
    grids are refused to avoid accidental weighting changes. metric is a callable.
    """
    cells={}; tasks={}; byscenario={}
    for r in rows:
        if r['method'] not in (method_a,method_b): continue
        condition=tuple(r[k] for k in condition_keys)
        key=(r['scenario_id'],condition,r['method'])
        if key in cells: raise ValidationError('Duplicate repeated-condition cell')
        cells[key]=float(metric(r)); tasks.setdefault(r['scenario_id'],r['task'])
        if tasks[r['scenario_id']]!=r['task']: raise ValidationError('Scenario changes task')
        byscenario.setdefault(r['scenario_id'],set()).add(condition)
    if not byscenario: raise ValidationError('No comparable repeated observations')
    grids=list(byscenario.values())
    if any(g!=grids[0] for g in grids): raise ValidationError('Unequal repeated-condition grids need an explicitly weighted estimator')
    d=[]; ts=[]
    for sid in sorted(byscenario):
        vals=[]
        for cond in sorted(byscenario[sid]):
            ka=(sid,cond,method_a); kb=(sid,cond,method_b)
            if ka not in cells or kb not in cells: raise ValidationError('Missing repeated-condition pair')
            vals.append(cells[ka]-cells[kb])
        d.append(float(np.mean(vals))); ts.append(tasks[sid])
    out=bootstrap_difference(d,ts,resamples,seed)
    out['conditions_per_scenario']=len(grids[0]); out['estimand']='Equal condition average within scenario, then empirical scenario average'
    return out

def holm_adjust(pvalues):
    p=list(pvalues)
    if any(not isinstance(v,(float,int)) or not math.isfinite(v) or not 0<=v<=1 for v in p): raise ValueError('Invalid p-value')
    order=sorted(range(len(p)),key=lambda i:p[i]); out=[0.0]*len(p); last=0.0
    for rank,i in enumerate(order):
        last=max(last,(len(p)-rank)*p[i]); out[i]=min(1.0,last)
    return out

def calibration(predictions,outcomes,approved,bins=10):
    p=np.asarray(predictions,dtype=float); y=np.asarray(outcomes); a=np.asarray(approved)
    if len(p)==0 or len(p)!=len(y) or len(p)!=len(a) or not np.isfinite(p).all() or np.any((p<0)|(p>1)):
        raise ValueError('Invalid calibration arrays')
    if not set(y.tolist())<={0,1} or not set(a.tolist())<={True,False}: raise ValueError('Outcomes and approvals must be binary')
    a=a.astype(bool); y=y.astype(int)
    unsafe=int(np.sum(a & (y==1))); na=int(a.sum()); nh=int(y.sum()); reliability=[]
    for i in range(bins):
        mask=(p>=i/bins)&((p<(i+1)/bins) if i<bins-1 else (p<=1))
        reliability.append({'low':i/bins,'high':(i+1)/bins,'n':int(mask.sum()),
                            'mean_prediction':float(p[mask].mean()) if mask.any() else None,
                            'observed_rate':float(y[mask].mean()) if mask.any() else None})
    return {'n':len(p),'brier_score':float(np.mean((p-y)**2)),
            'unsafe_approvals':unsafe,'n_approved':na,'n_hazardous':nh,
            'p_hazard_given_approved':unsafe/na if na else None,
            'p_approved_given_hazardous':unsafe/nh if nh else None,'reliability':reliability}

