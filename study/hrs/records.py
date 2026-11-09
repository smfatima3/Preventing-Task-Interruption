"""Strict measured-record contract. Fixtures are never accepted by this loader."""
import hashlib
import json
import math
from pathlib import Path

class ValidationError(ValueError):
    pass

BOOLEAN_METRICS = (
    'robot_human_contact', 'object_human_contact', 'object_drop', 'robot_fall',
    'limit_violation', 'task_success', 'aborted', 'unresolved',
)
CONTINUOUS_METRICS = ('max_contact_impulse_ns', 'peak_contact_force_n', 'max_object_impact_energy_j')
COUNT_METRICS = ('interventions', 'switches', 'deadline_misses')
HASH_FIELDS = ('policy_sha256', 'scenario_sha256', 'snapshot_sha256', 'human_trajectory_sha256', 'config_sha256', 'raw_trace_sha256')
STATUSES = {'complete', 'timeout', 'controller_failure', 'infrastructure_failure'}
REQUIRED = (
    'schema_version','data_kind','stage_id','run_id','scenario_id','task','stratum','split',
    'method','training_seed','variant','replicate','added_delay_ms','physics_variant',
    'status','sensor_input_source','simulator_time_advanced_during_compute',
    'observation_time_s','decision_time_s','action_start_time_s','observed_duration_s',
    'stable_followup_s','raw_trace_path','measurements',
) + HASH_FIELDS

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def local_file(root, relative):
    if not isinstance(relative,str) or not relative or Path(relative).is_absolute():
        raise ValidationError('Artifact paths must be nonempty package-relative paths')
    root=Path(root).resolve(); p=(root/relative).resolve()
    if not p.is_relative_to(root) or not p.is_file():
        raise ValidationError(f'Missing or out-of-package artifact: {relative}')
    return p

def valid_hash(value):
    return isinstance(value,str) and len(value)==64 and all(c in '0123456789abcdef' for c in value)

def number(value, name, minimum=0):
    if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value) or value < minimum:
        raise ValidationError(f'{name} must be a finite number >= {minimum}')

def validate_row(row, root, check_trace=True):
    if not isinstance(row,dict): raise ValidationError('Each JSONL line must be an object')
    missing=[k for k in REQUIRED if k not in row]
    if missing: raise ValidationError(f'Missing fields: {missing}')
    if row['schema_version']!=1: raise ValidationError('Unsupported record schema')
    if row['data_kind'] not in ('measured_simulation','measured_hardware'):
        raise ValidationError('Only measured data accepted; synthetic/test/example records are forbidden')
    for k in ('run_id','scenario_id','split','method','variant','physics_variant','raw_trace_path'):
        if not isinstance(row[k],str) or not row[k].strip(): raise ValidationError(f'{k} must be a nonempty string')
    if row['stage_id'] not in [f'E{i}' for i in range(15)]: raise ValidationError('Invalid stage_id')
    if row['task'] not in ('T1','T2','T3'): raise ValidationError('Unknown task')
    if row['stratum'] not in ('benign','avoidable','severe'): raise ValidationError('Unknown stratum')
    for k in HASH_FIELDS:
        if not valid_hash(row[k]): raise ValidationError(f'{k} must be lowercase SHA-256')
    if row['status'] not in STATUSES: raise ValidationError('Unknown run status')
    if row['sensor_input_source']!='estimated': raise ValidationError('Privileged policy inputs forbidden in deployable records')
    if row['simulator_time_advanced_during_compute'] is not True: raise ValidationError('Physics must advance during compute')
    for k in ('training_seed','replicate'):
        if type(row[k]) is not int or row[k]<0: raise ValidationError(f'{k} must be a nonnegative integer')
    for k in ('added_delay_ms','observation_time_s','decision_time_s','action_start_time_s','observed_duration_s','stable_followup_s'):
        number(row[k],k)
    if not row['observation_time_s']<=row['decision_time_s']<=row['action_start_time_s']:
        raise ValidationError('Sensing/decision/action times are not ordered')
    if row['stable_followup_s']>row['observed_duration_s']:
        raise ValidationError('Stable follow-up exceeds observed duration')
    m=row['measurements']
    if row['status']!='complete':
        if not isinstance(row.get('failure_reason'),str) or not row['failure_reason'].strip():
            raise ValidationError('Noncomplete attempt requires failure_reason')
        if m is None: pass
        elif not isinstance(m,dict): raise ValidationError('Partial measurements must be an object or null')
        else:
            # Partial outcomes remain partial. Never impute missing safety as false.
            for k in BOOLEAN_METRICS:
                if k in m and type(m[k]) is not bool: raise ValidationError(f'{k} must be boolean')
            for k in CONTINUOUS_METRICS+COUNT_METRICS:
                if k in m: number(m[k],k)
    else:
        if not isinstance(m,dict): raise ValidationError('Complete run needs measurements')
        for k in BOOLEAN_METRICS:
            if type(m.get(k)) is not bool: raise ValidationError(f'{k} must be boolean; no missing outcome imputation')
        for k in CONTINUOUS_METRICS:
            number(m.get(k),k)
        for k in COUNT_METRICS:
            if type(m.get(k)) is not int or m[k]<0: raise ValidationError(f'{k} must be a nonnegative integer')
        if not isinstance(m.get('latencies_ms'),list) or not m['latencies_ms']:
            raise ValidationError('At least one measured latency is required')
        for x in m['latencies_ms']: number(x,'latencies_ms')
        if m['task_success'] and (m['aborted'] or m['unresolved']):
            raise ValidationError('Successful task cannot also be aborted/unresolved')
    if check_trace:
        p=local_file(root,row['raw_trace_path'])
        if not p.stat().st_size: raise ValidationError('Empty raw trace')
        if digest(p)!=row['raw_trace_sha256']: raise ValidationError('Raw trace hash mismatch')
    return row

def load_records(path,root,check_trace=True,stage_id=None):
    rows=[]; seen=set()
    with Path(path).open() as f:
        for line_no,line in enumerate(f,1):
            if not line.strip(): continue
            try:
                row=json.loads(line,parse_constant=lambda x: (_ for _ in ()).throw(ValidationError(f'Nonfinite JSON: {x}')))
                validate_row(row,root,check_trace)
                if stage_id and row['stage_id']!=stage_id: raise ValidationError('Mixed/incorrect stage')
                if row['run_id'] in seen: raise ValidationError('Duplicate run_id')
                seen.add(row['run_id']); rows.append(row)
            except (ValueError,TypeError) as e: raise ValidationError(f'{path}:{line_no}: {e}') from e
    if not rows: raise ValidationError('No measured records; empty input cannot create results')
    return rows

def human_hazard(row):
    m=row['measurements']; return int(m['robot_human_contact'] or m['object_human_contact'])

def safe_success(row):
    m=row['measurements']
    return int(m['task_success'] and not any(m[k] for k in BOOLEAN_METRICS if k!='task_success'))

def primary_pairs(rows,comparator,stage_id,lock):
    if any(r['status']!='complete' for r in rows):
        raise ValidationError('Unresolved/noncomplete attempts require a prespecified handling analysis; primary claim blocked')
    selected=[r for r in rows if r['method'] in ('M',comparator)]
    cells={}; metadata={}
    horizon=lock['matched_window_s'] if stage_id=='E6' else lock['full_episode_window_s']
    for r in selected:
        if r['variant']!='primary' or r['replicate']!=0 or r['added_delay_ms']!=0 or r['physics_variant']!='nominal':
            raise ValidationError('Primary analysis accepts one locked primary deployment artifact / nominal condition only')
        if r['observed_duration_s']+1e-8<horizon:
            raise ValidationError('Truncated primary exposure')
        if not r['measurements']['unresolved'] and not r['measurements']['robot_fall'] and r['stable_followup_s']+1e-8<lock['minimum_stable_followup_s']:
            raise ValidationError('Insufficient stable follow-up')
        expected_hash=lock['primary_policy_sha256'] if r['method']=='M' else lock['baseline_policy_sha256'][comparator]
        if r['policy_sha256']!=expected_hash: raise ValidationError('Policy differs from final lock')
        k=(r['scenario_id'],r['method'])
        if k in cells: raise ValidationError('Duplicate scenario-method cell; retries/seeds are not independent trials')
        cells[k]=r
        # E7 starts matched scenarios; E6 requires the same actual pre-intervention snapshot.
        values=tuple(r[x] for x in ('task','stratum','scenario_sha256','snapshot_sha256','human_trajectory_sha256'))
        old=metadata.setdefault(r['scenario_id'],values)
        if old!=values: raise ValidationError('Paired scenario state/trajectory/task metadata mismatch')
    ids=sorted(metadata)
    if not ids: raise ValidationError('No M/comparator pairs')
    if any((i,m) not in cells for i in ids for m in ('M',comparator)):
        raise ValidationError('Missing paired M/comparator result')
    return [(cells[(i,'M')],cells[(i,comparator)]) for i in ids]

def check_registry(rows,root,lock,stage_id):
    path=local_file(root,lock['test_scenario_registry'])
    registry=json.loads(path.read_text())
    if not isinstance(registry,list): raise ValidationError('Scenario registry must be a JSON array')
    planned=[r for r in registry if r['stage_id']==stage_id]
    key=lambda r:(r['scenario_id'],r['method'])
    expected={key(r):r for r in planned}
    actual={key(r):r for r in rows}
    if not expected or len(expected)!=len(planned): raise ValidationError('Empty or duplicate planned cells')
    if len(actual)!=len(rows): raise ValidationError('Duplicate selected primary cells')
    if set(actual)!=set(expected):
        raise ValidationError(f'Frozen registry mismatch: missing={len(set(expected)-set(actual))}, extra={len(set(actual)-set(expected))}')
    if len({r['scenario_id'] for r in rows})!=lock['confirmatory_base_scenarios'][stage_id]:
        raise ValidationError('Scenario count differs from fixed sample size')
    for k,r in actual.items():
        for field in ('task','stratum','snapshot_sha256','scenario_sha256','human_trajectory_sha256'):
            if r[field]!=expected[k][field]: raise ValidationError(f'Registered {field} mismatch')
    all_ids={}
    for r in registry:
        sid=r['scenario_id']; stage=r['stage_id']
        if sid in all_ids and all_ids[sid]!=stage: raise ValidationError('Base scenario reused across confirmatory splits')
        all_ids[sid]=stage

