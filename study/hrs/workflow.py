"""Sequential evidence gates with hash-checked receipts. Not a security boundary."""
import datetime as dt
import json
import math
from pathlib import Path
from .records import ValidationError, digest, valid_hash, local_file, load_records, check_registry, primary_pairs

def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def read_json(path):
    return json.loads(Path(path).read_text(),parse_constant=lambda x: (_ for _ in ()).throw(ValidationError(f'Nonfinite JSON: {x}')))
def save_json(path,obj):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp'); tmp.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n'); tmp.replace(path)
def setup(root):
    root=Path(root).resolve()
    return root,read_json(root/'config/sequence.json'),read_json(root/'state/status.json')
def journal(root,event,**kwargs):
    with (root/'state/journal.jsonl').open('a') as f: f.write(json.dumps({'time':now(),'event':event,**kwargs})+'\n')
def fingerprints(root,paths): return {p:digest(local_file(root,p)) for p in paths}
def source_files(root):
    return sorted(str(p.relative_to(root)) for d in ('hrs','scripts','adapters') for p in (root/d).rglob('*.py'))

def audit(root):
    root,seq,state=setup(root); issues=[]
    if (root/'AGENTS.md').read_bytes()!=(root/'agent.md').read_bytes(): issues.append('AGENTS.md and agent.md differ')
    previous_pass=True
    for s in seq:
        entry=state['stages'][s['id']]
        if entry['status'] in ('passed','skipped'):
            if not previous_pass: issues.append(f'{s["id"]} completed out of order')
            try:
                receipt_file=local_file(root,entry['receipt'])
                if digest(receipt_file)!=entry['receipt_sha256']: raise ValidationError('Receipt changed')
                r=read_json(receipt_file)
                for p,h in r['fingerprints'].items():
                    if digest(local_file(root,p))!=h: raise ValidationError(f'Changed locked artifact: {p}')
                if 'source_inventory' in r and r['source_inventory']!=source_files(root):
                    raise ValidationError('Research code inventory changed after E5')
                if r.get('record_path'):
                    load_records(local_file(root,r['record_path']),root,stage_id=s['id'])
            except (OSError,ValueError,KeyError) as e: issues.append(f'{s["id"]}: {e}')
        else:
            previous_pass=False
    return issues

def require_clean(root):
    errors=audit(root)
    if errors: raise ValidationError('Audit failed: '+'; '.join(errors))

def eligible(root,stage_id):
    root,seq,state=setup(root)
    candidates=[s for s in seq if s['id']==stage_id]
    if not candidates: raise ValidationError('Unknown stage')
    s=candidates[0]
    for dependency in s['depends_on']:
        if state['stages'][dependency]['status'] not in ('passed','skipped'):
            raise ValidationError(f'{stage_id} blocked: {dependency} has not passed')
    return root,s,state

def begin(root,stage_id):
    require_clean(root); root,s,state=eligible(root,stage_id); entry=state['stages'][stage_id]
    if entry['status'] not in ('pending','blocked'):
        raise ValidationError(f'Cannot begin {stage_id} in state {entry["status"]}')
    entry.update(status='running',attempt=entry['attempt']+1,started=now())
    save_json(root/'state/status.json',state); journal(root,'begin',stage_id=stage_id,attempt=entry['attempt'])

def final_lock_valid(root):
    lock=read_json(root/'config/final_lock.json')
    missing=[k for k,v in lock.items() if v is None]
    if missing: raise ValidationError(f'Final lock has unresolved choices: {missing}')
    if lock['status']!='FROZEN': raise ValidationError('Final lock status must be FROZEN')
    methods=lock['included_methods']; b=lock['primary_comparator']
    if len(methods)!=len(set(methods)): raise ValidationError('Duplicate method in lock')
    if not {'B0','B1','B4','B5','M'}<=set(methods) or not {'B2','B3'} & set(methods):
        raise ValidationError('Insufficient baseline set for the declared method contribution')
    if b not in methods or b in ('M','B0'): raise ValidationError('B* must be an included non-nominal baseline')
    missing_methods=set(read_json(root/'config/protocol.json')['planned_methods'])-set(methods)
    if set(lock['unavailable_methods'])!=missing_methods or any(not v for v in lock['unavailable_methods'].values()):
        raise ValidationError('Every unavailable method needs a reason')
    for h in [lock['primary_policy_sha256'],lock['primitive_library_sha256']]+[lock['baseline_policy_sha256'].get(m) for m in methods if m!='M']:
        if not valid_hash(h): raise ValidationError('Missing/invalid frozen policy or primitive hash')
    for key in ('matched_window_s','full_episode_window_s','minimum_stable_followup_s','decision_deadline_ms'):
        if not isinstance(lock[key],(int,float)) or lock[key]<=0: raise ValidationError(f'Invalid {key}')
    if not 0<lock['noninferiority_margin']<1: raise ValidationError('Invalid noninferiority margin')
    if not isinstance(lock['contact_tolerance_n'],(int,float)) or lock['contact_tolerance_n']<0: raise ValidationError('Invalid contact tolerance')
    if type(lock['bootstrap_resamples']) is not int or lock['bootstrap_resamples']<10000: raise ValidationError('At least 10,000 bootstrap resamples required')
    registry=read_json(local_file(root,lock['test_scenario_registry']))
    if not isinstance(registry,list) or not registry: raise ValidationError('Empty test registry')
    for stage in ('E6','E7'):
        if type(lock['confirmatory_base_scenarios'][stage]) is not int or lock['confirmatory_base_scenarios'][stage]<1:
            raise ValidationError('Invalid fixed test N')
    expected_methods=set(methods)
    for stage in ('E6','E7'):
        cells=[r for r in registry if r.get('stage_id')==stage]
        if {r['task'] for r in cells}!={'T1','T2','T3'}: raise ValidationError('Both confirmatory studies require all three tasks')
        ids={r['scenario_id'] for r in cells}
        if len(ids)!=lock['confirmatory_base_scenarios'][stage]: raise ValidationError(f'{stage} planned N does not match registry')
        if len({(r['scenario_id'],r['method']) for r in cells})!=len(cells): raise ValidationError('Duplicate planned registry cells')
        for sid in ids:
            rr=[r for r in cells if r['scenario_id']==sid]
            if {r['method'] for r in rr}!=expected_methods: raise ValidationError('Every scenario needs all registered methods')
            if len({tuple(r[k] for k in ('task','stratum','scenario_sha256','snapshot_sha256','human_trajectory_sha256')) for r in rr})!=1:
                raise ValidationError('Planned matched metadata disagree')
    if {r['scenario_id'] for r in registry if r['stage_id']=='E6'} & {r['scenario_id'] for r in registry if r['stage_id']=='E7'}:
        raise ValidationError('Confirmatory scenario splits overlap')
    return lock

def check_stage_counts(rows,stage_id,lock=None,protocol=None):
    bytask={t:{r['scenario_id'] for r in rows if r['task']==t} for t in ('T1','T2','T3')}
    minimum={'E1':12,'E2':30,'E3':20,'E5':30,'E8':40,'E9':20,'E10':60,'E12':20}.get(stage_id)
    if minimum and any(len(v)<minimum for v in bytask.values()): raise ValidationError(f'{stage_id} requires at least {minimum} independent base scenarios per task')
    if stage_id=='E4':
        for t in bytask:
            for split,n in [('train',100),('calibration',40)]:
                if len({r['scenario_id'] for r in rows if r['task']==t and r['split']==split})<n:
                    raise ValidationError(f'E4 requires {n} {split} base states for {t}')
    if stage_id=='E11' and len({r['scenario_id'] for r in rows})<120: raise ValidationError('E11 requires 120 audit states')
    if stage_id=='E9' and {r['added_delay_ms'] for r in rows}!={0,100,300,600}: raise ValidationError('E9 requires all four added-delay settings')
    if stage_id=='E2':
        for task in ('T1','T2','T3'):
            nominal=[r for r in rows if r['task']==task and r['method']=='B0' and r['variant']=='nominal_readiness']
            if len(nominal)<30 or len({r['scenario_id'] for r in nominal})!=len(nominal):
                raise ValidationError('E2 needs >=30 independent nominal_readiness B0 episodes per task')
            if any(r['status']!='complete' for r in nominal): raise ValidationError('E2 nominal outcomes unresolved')
            if sum(r['measurements']['task_success'] for r in nominal)/len(nominal)<.8:
                raise ValidationError('E2 nominal success is below 80% for a task')
    if stage_id in ('E8','E9','E10','E11','E12'):
        if lock is None or protocol is None: raise ValidationError('Audit stages require frozen condition definitions')
        b=lock['primary_comparator']; ids={r['scenario_id'] for r in rows}
        if stage_id=='E8':
            fields=('method',); expected={(m,) for m in ('M','M_NO_OBJECT','M_NO_HUMAN','M_NO_DELAY')}
        elif stage_id=='E9':
            fields=('method','added_delay_ms'); expected={(m,d) for m in ('M',b,'M_NO_DELAY') for d in (0,100,300,600)}
        elif stage_id=='E10':
            fields=('method',); expected={(m,) for m in ('M',b)}
            if not {'layout','payload_grasp','human_motion','combined'}<={r.get('shift_type') for r in rows}:
                raise ValidationError('E10 needs all four declared shift types')
        elif stage_id=='E11':
            fields=('method','training_seed'); expected={('M',seed) for seed in protocol['training_seeds']}
        else:
            fields=('method','physics_variant'); expected={(m,p) for m in ('M',b) for p in lock['physics_audit_variants']}
        for sid in ids:
            rr=[r for r in rows if r['scenario_id']==sid]
            if stage_id=='E11': rr=[r for r in rr if r['method']=='M']
            grid=[tuple(r[k] for k in fields) for r in rr]
            if len(set(grid))!=len(grid) or set(grid)!=expected:
                raise ValidationError(f'{stage_id} incomplete/duplicate condition grid for scenario {sid}')
            if any(r['status']!='complete' for r in rr): raise ValidationError(f'{stage_id} has unresolved audit outcomes')

def finish(root,stage_id,evidence_path):
    require_clean(root); root,s,state=eligible(root,stage_id)
    if state['stages'][stage_id]['status']!='running': raise ValidationError('Begin the stage before finishing')
    ep=Path(evidence_path).resolve()
    if not ep.is_relative_to(root): raise ValidationError('Evidence must be inside package')
    e=read_json(ep)
    if e.get('stage_id')!=stage_id: raise ValidationError('Evidence stage mismatch')
    for k in ('reviewer','findings','limitations'):
        if not isinstance(e.get(k),str) or not e[k].strip(): raise ValidationError(f'Evidence needs {k}')
    if e.get('decision')=='stop':
        state['stages'][stage_id]['status']='blocked'; save_json(root/'state/status.json',state)
        journal(root,'blocked',stage_id=stage_id,evidence=str(ep.relative_to(root)),reason=e['findings']); return
    if e.get('decision')!='pass': raise ValidationError('Decision must be pass or stop')
    if set(e.get('checks',{}))!=set(s['checks']) or any(v is not True for v in e['checks'].values()):
        raise ValidationError('All stage checks must be explicitly supported and true')
    artifacts=e.get('artifacts',[]); roles={a.get('role') for a in artifacts}
    required=set(s['artifact_roles']) | ({'records'} if s['requires_records'] else set())
    if not required<=roles: raise ValidationError(f'Missing evidence roles {required-roles}')
    if len(roles)!=len(artifacts): raise ValidationError('Duplicate evidence roles')
    paths=[str(ep.relative_to(root))]
    for a in artifacts:
        p=local_file(root,a['path'])
        if not p.stat().st_size or not valid_hash(a.get('sha256')) or digest(p)!=a['sha256']:
            raise ValidationError(f'Empty artifact or incorrect hash: {a.get("path")}')
        paths.append(a['path'])
    record_path=None
    if s['requires_records']:
        record_path=next(a['path'] for a in artifacts if a['role']=='records')
        rows=load_records(local_file(root,record_path),root,stage_id=stage_id)
        if type(e.get('record_count_expected')) is not int or len(rows)!=e['record_count_expected']:
            raise ValidationError('Declared record count differs from manifest')
        lock_for_counts=final_lock_valid(root) if int(stage_id[1:])>=8 else None
        check_stage_counts(rows,stage_id,lock_for_counts,read_json(root/'config/protocol.json'))
        # Check scenario reuse against all completed scientific splits.
        seen={}
        for old in state['stages'].values():
            if old['status']=='passed':
                receipt=read_json(local_file(root,old['receipt']))
                if receipt.get('record_path'):
                    for r in load_records(local_file(root,receipt['record_path']),root): seen[r['scenario_id']]=r['split']
        current={}
        for r in rows:
            if r['scenario_id'] in seen: raise ValidationError('Scenario reused across experiment stages; use a separately declared audit reference, not a new independent sample')
            prior=current.setdefault(r['scenario_id'],r['split'])
            if prior!=r['split']: raise ValidationError('Scenario crosses train/calibration splits')
        if stage_id in ('E6','E7'):
            lock=final_lock_valid(root); check_registry(rows,root,lock,stage_id)
            primary_pairs(rows,lock['primary_comparator'],stage_id,lock)
            for r in rows:
                expected=lock['primary_policy_sha256'] if r['method']=='M' else lock['baseline_policy_sha256'][r['method']]
                if r['policy_sha256']!=expected or r['config_sha256']!=digest(root/'config/final_lock.json'):
                    raise ValidationError('Policy/config hash differs from frozen confirmatory configuration')
    if stage_id=='E0':
        p=read_json(root/'config/protocol.json')
        if any(v is None or v=='' for v in p['resources'].values()): raise ValidationError('E0 simulator/controller/adapter resources unresolved')
        if not valid_hash(p['resources']['nominal_controller_sha256']): raise ValidationError('Invalid controller checkpoint hash')
        checkpoint=local_file(root,p['resources']['nominal_controller_checkpoint'])
        if digest(checkpoint)!=p['resources']['nominal_controller_sha256']: raise ValidationError('Controller checkpoint hash mismatch')
        local_file(root,p['resources']['asset_manifest'])
        paths += [p['resources']['nominal_controller_checkpoint'],p['resources']['asset_manifest']]
        paths+=['config/protocol.json','config/sequence.json','AGENTS.md','agent.md']
    lock=None
    if stage_id=='E5':
        lock=final_lock_valid(root)
        paths+=['config/final_lock.json',lock['test_scenario_registry']]+source_files(root)
    receipt={'stage_id':stage_id,'completed':now(),'fingerprints':fingerprints(root,paths),'record_path':record_path,'reviewer':e['reviewer'],'findings':e['findings'],'claim_status':'Not inferred by workflow; see scientific analysis'}
    if lock is not None: receipt['source_inventory']=source_files(root)
    receipt_rel=f'state/receipts/{stage_id}_attempt_{state["stages"][stage_id]["attempt"]}.json'
    rp=root/receipt_rel
    if rp.exists(): raise ValidationError('Receipt already exists; refusing overwrite')
    save_json(rp,receipt)
    state['stages'][stage_id].update(status='passed',receipt=receipt_rel,receipt_sha256=digest(rp))
    save_json(root/'state/status.json',state); journal(root,'passed',stage_id=stage_id,receipt=receipt_rel)

def skip_optional(root,stage_id,reason):
    require_clean(root); root,s,state=eligible(root,stage_id)
    if not s['optional'] or not reason.strip(): raise ValidationError('Only E13 may be skipped, with a reason')
    if state['stages'][stage_id]['status'] not in ('pending','running'): raise ValidationError('Stage already resolved')
    rel=f'state/receipts/{stage_id}_skipped.json'; p=root/rel
    if p.exists(): raise ValidationError('Skip receipt already exists')
    save_json(p,{'stage_id':stage_id,'completed':now(),'reason':reason,'fingerprints':{}})
    state['stages'][stage_id].update(status='skipped',receipt=rel,receipt_sha256=digest(p))
    save_json(root/'state/status.json',state); journal(root,'skipped',stage_id=stage_id,reason=reason)

