"""Software-only fixtures in temporary directories. These are not robot experiments."""
import copy, json, shutil, tempfile, unittest
from pathlib import Path
from hrs.records import *
from hrs import workflow

PACKAGE=Path(__file__).resolve().parents[1]

def fixture(root,**updates):
    # Deliberately synthetic data to test parsers, never emitted to research directories.
    p=root/'trace_fixture.txt'; p.write_text('SYNTHETIC UNIT TEST TRACE; NOT ROBOT EVIDENCE\n')
    row=dict(schema_version=1,data_kind='synthetic',stage_id='E6',run_id='fixture-run',scenario_id='fixture-scene',
             task='T1',stratum='benign',split='matched_test',method='M',training_seed=11,variant='primary',replicate=0,
             added_delay_ms=0,physics_variant='nominal',status='complete',sensor_input_source='estimated',
             simulator_time_advanced_during_compute=True,observation_time_s=0.0,decision_time_s=.05,action_start_time_s=.1,
             observed_duration_s=120.0,stable_followup_s=2.0,raw_trace_path=p.name,
             measurements={**{k:False for k in BOOLEAN_METRICS},**{k:0.0 for k in CONTINUOUS_METRICS},
                           **{k:0 for k in COUNT_METRICS},'latencies_ms':[100.0]},
             **{k:'a'*64 for k in HASH_FIELDS})
    row['raw_trace_sha256']=digest(p); row.update(updates); return row

class RecordTests(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def test_synthetic_rejected(self):
        with self.assertRaisesRegex(ValidationError,'synthetic'): validate_row(fixture(self.root),self.root)
    def test_schema_accepts_complete_control_case(self):
        # Field-level control case only. The synthetic trace remains in a temporary directory.
        r=fixture(self.root,data_kind='measured_simulation'); validate_row(r,self.root)
    def test_trace_tamper_rejected(self):
        r=fixture(self.root,data_kind='measured_simulation'); (self.root/r['raw_trace_path']).write_text('changed')
        with self.assertRaisesRegex(ValidationError,'hash'): validate_row(r,self.root)
    def test_missing_outcomes_rejected(self):
        r=fixture(self.root,data_kind='measured_simulation'); del r['measurements']['object_human_contact']
        with self.assertRaises(ValidationError): validate_row(r,self.root)
    def test_nonfinite_rejected(self):
        r=fixture(self.root,data_kind='measured_simulation'); r['measurements']['peak_contact_force_n']=float('nan')
        with self.assertRaises(ValidationError): validate_row(r,self.root)
    def test_clock_and_privileged_input_rejected(self):
        for update in ({'action_start_time_s':.01},{'sensor_input_source':'simulator_truth'},{'simulator_time_advanced_during_compute':False}):
            with self.assertRaises(ValidationError): validate_row(fixture(self.root,data_kind='measured_simulation',**update),self.root)
    def test_partial_failure_retained(self):
        r=fixture(self.root,data_kind='measured_simulation',status='infrastructure_failure',failure_reason='unit test',measurements=None)
        validate_row(r,self.root)
    def test_path_escape_rejected(self):
        with self.assertRaises(ValidationError): local_file(self.root,'../outside.txt')
    def test_union_and_safe_success(self):
        r=fixture(self.root); r['measurements']['task_success']=True
        self.assertEqual(safe_success(r),1)
        r['measurements']['object_human_contact']=True
        self.assertEqual(human_hazard(r),1); self.assertEqual(safe_success(r),0)
    def test_duplicate_run_and_empty_file_rejected(self):
        r=fixture(self.root,data_kind='measured_simulation'); p=self.root/'rows.jsonl'
        p.write_text(json.dumps(r)+'\n'+json.dumps(r)+'\n')
        with self.assertRaisesRegex(ValidationError,'Duplicate'): load_records(p,self.root)
        p.write_text('')
        with self.assertRaisesRegex(ValidationError,'No measured'): load_records(p,self.root)
    def test_pairing_failures(self):
        a=fixture(self.root); b=copy.deepcopy(a); b.update(method='B5',run_id='b')
        lock={'matched_window_s':10,'full_episode_window_s':120,'minimum_stable_followup_s':2,'primary_policy_sha256':'a'*64,'baseline_policy_sha256':{'B5':'a'*64}}
        self.assertEqual(len(primary_pairs([a,b],'B5','E6',lock)),1)
        with self.assertRaisesRegex(ValidationError,'Missing paired'): primary_pairs([a],'B5','E6',lock)
        with self.assertRaisesRegex(ValidationError,'Duplicate'): primary_pairs([a,b,copy.deepcopy(a)],'B5','E6',lock)
        b['snapshot_sha256']='b'*64
        with self.assertRaisesRegex(ValidationError,'mismatch'): primary_pairs([a,b],'B5','E6',lock)
    def test_truncated_exposure_rejected(self):
        a=fixture(self.root,observed_duration_s=1); b=copy.deepcopy(a); b['method']='B5'
        lock={'matched_window_s':10,'minimum_stable_followup_s':2,'primary_policy_sha256':'a'*64,'baseline_policy_sha256':{'B5':'a'*64}}
        with self.assertRaisesRegex(ValidationError,'Truncated'): primary_pairs([a,b],'B5','E6',lock)
    def test_registry_requires_all_cells(self):
        a=fixture(self.root); b=copy.deepcopy(a); b['method']='B5'
        reg=[{k:r[k] for k in ('stage_id','scenario_id','method','task','stratum','snapshot_sha256','scenario_sha256','human_trajectory_sha256')} for r in (a,b)]
        (self.root/'registry.json').write_text(json.dumps(reg))
        lock={'test_scenario_registry':'registry.json','confirmatory_base_scenarios':{'E6':1}}
        check_registry([a,b],self.root,lock,'E6')
        with self.assertRaisesRegex(ValidationError,'mismatch'): check_registry([a],self.root,lock,'E6')

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        for d in ('config','state'):
            shutil.copytree(PACKAGE/d,self.root/d)
        # Reset the fixture workflow independently of the delivered state.
        seq=workflow.read_json(self.root/'config/sequence.json')
        workflow.save_json(self.root/'state/status.json',{'schema_version':1,'stages':{s['id']:{'status':'pending','attempt':0} for s in seq}})
        for p in ('AGENTS.md','agent.md'): shutil.copyfile(PACKAGE/p,self.root/p)
        (self.root/'evidence').mkdir()
    def tearDown(self): self.tmp.cleanup()
    def e0_evidence(self):
        p=workflow.read_json(self.root/'config/protocol.json')
        (self.root/'checkpoint_fixture.bin').write_text('SYNTHETIC CHECKPOINT; SOFTWARE TEST ONLY')
        (self.root/'assets_fixture.json').write_text('{}')
        p['resources']={k:'unit-test-only' for k in p['resources']}
        p['resources'].update(nominal_controller_checkpoint='checkpoint_fixture.bin',nominal_controller_sha256=digest(self.root/'checkpoint_fixture.bin'),asset_manifest='assets_fixture.json')
        workflow.save_json(self.root/'config/protocol.json',p)
        s=workflow.read_json(self.root/'config/sequence.json')[0]
        arts=[]
        for role in s['artifact_roles']:
            rel=f'evidence/{role}.md'; (self.root/rel).write_text('SYNTHETIC SOFTWARE TEST. NOT RESEARCH EVIDENCE.')
            arts.append({'role':role,'path':rel,'sha256':digest(self.root/rel)})
        ev={'stage_id':'E0','decision':'pass','reviewer':'unit-test','findings':'software fixture','limitations':'not research','checks':{k:True for k in s['checks']},'artifacts':arts}
        path=self.root/'evidence/e0.json'; workflow.save_json(path,ev); return path
    def test_cannot_skip_prerequisites(self):
        with self.assertRaisesRegex(ValidationError,'blocked'): workflow.begin(self.root,'E3')
    def test_only_optional_stage_skippable(self):
        with self.assertRaises(ValidationError): workflow.skip_optional(self.root,'E0','time pressure')
    def test_begin_does_not_finish(self):
        workflow.begin(self.root,'E0'); self.assertEqual(workflow.read_json(self.root/'state/status.json')['stages']['E0']['status'],'running')
        with self.assertRaises(ValidationError): workflow.begin(self.root,'E1')
    def test_missing_evidence_blocks(self):
        workflow.begin(self.root,'E0'); p=self.e0_evidence(); e=workflow.read_json(p); e['checks'][next(iter(e['checks']))]=None; workflow.save_json(p,e)
        with self.assertRaisesRegex(ValidationError,'checks'): workflow.finish(self.root,'E0',p)
    def test_receipt_and_changed_lock(self):
        workflow.begin(self.root,'E0'); workflow.finish(self.root,'E0',self.e0_evidence())
        self.assertEqual(workflow.audit(self.root),[])
        (self.root/'config/protocol.json').write_text('{}')
        self.assertTrue(workflow.audit(self.root))
        with self.assertRaisesRegex(ValidationError,'Audit failed'): workflow.begin(self.root,'E1')
    def test_stopped_stage_is_blocked(self):
        workflow.begin(self.root,'E0'); p=self.root/'evidence/stop.json'
        workflow.save_json(p,{'stage_id':'E0','decision':'stop','reviewer':'unit-test','findings':'missing real assets','limitations':'not measured'})
        workflow.finish(self.root,'E0',p)
        self.assertEqual(workflow.read_json(self.root/'state/status.json')['stages']['E0']['status'],'blocked')
    def test_agent_files_must_match(self):
        (self.root/'agent.md').write_text('modified')
        self.assertTrue(workflow.audit(self.root))
    def test_unconfigured_lock_rejected(self):
        with self.assertRaisesRegex(ValidationError,'unresolved'): workflow.final_lock_valid(self.root)

class AuditGridTests(unittest.TestCase):
    def setUp(self):
        self.lock={'primary_comparator':'B5','physics_audit_variants':['nominal','contact_alt','timestep_alt']}
        self.protocol={'training_seeds':[11,29,47]}
    def test_ablation_requires_every_variant_per_scene(self):
        rows=[{'scenario_id':f'{t}-{i}','task':t,'method':m,'status':'complete'} for t in ('T1','T2','T3') for i in range(40) for m in ('M','M_NO_OBJECT','M_NO_HUMAN','M_NO_DELAY')]
        workflow.check_stage_counts(rows,'E8',self.lock,self.protocol)
        with self.assertRaisesRegex(ValidationError,'condition grid'): workflow.check_stage_counts(rows[:-1],'E8',self.lock,self.protocol)
    def test_seed_audit_requires_primary_reference(self):
        rows=[{'scenario_id':str(i),'task':f'T{1+i%3}','method':'M','training_seed':seed,'status':'complete'} for i in range(120) for seed in (11,29,47)]
        workflow.check_stage_counts(rows,'E11',self.lock,self.protocol)
        with self.assertRaisesRegex(ValidationError,'condition grid'):
            workflow.check_stage_counts([r for r in rows if r['training_seed']!=11],'E11',self.lock,self.protocol)
    def test_physics_audit_requires_nominal_reference(self):
        rows=[{'scenario_id':f'{t}-{i}','task':t,'method':m,'physics_variant':v,'status':'complete'} for t in ('T1','T2','T3') for i in range(20) for m in ('M','B5') for v in self.lock['physics_audit_variants']]
        workflow.check_stage_counts(rows,'E12',self.lock,self.protocol)
        with self.assertRaisesRegex(ValidationError,'condition grid'):
            workflow.check_stage_counts([r for r in rows if r['physics_variant']!='nominal'],'E12',self.lock,self.protocol)
    def test_readiness_gate_uses_observed_success(self):
        rows=[{'scenario_id':f'{t}-{i}','task':t,'method':'B0','variant':'nominal_readiness','status':'complete','measurements':{'task_success':i<24}} for t in ('T1','T2','T3') for i in range(30)]
        workflow.check_stage_counts(rows,'E2')
        rows[0]['measurements']['task_success']=False
        with self.assertRaisesRegex(ValidationError,'below 80'): workflow.check_stage_counts(rows,'E2')

if __name__=='__main__': unittest.main()
