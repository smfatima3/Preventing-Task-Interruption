"""End-to-end software tests in disposable packages with clearly synthetic traces.

The measured_simulation label is exercised only to test the production schema's
positive path. No fixture is an actual simulation and no fixture is released as
research data. Header labels cannot substitute for raw-data provenance review.
"""
import copy, json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
from hrs import workflow
from hrs.records import digest
from test_integrity import fixture

PACKAGE=Path(__file__).resolve().parents[1]

class CliTests(unittest.TestCase):
    def test_unexecuted_package_refuses_analysis(self):
        p=subprocess.run([sys.executable,str(PACKAGE/'scripts/analyze.py'),'--stage','E6'],capture_output=True,text=True)
        self.assertEqual(p.returncode,2); self.assertIn('E5 must pass',p.stderr)
        self.assertFalse((PACKAGE/'results/computed/E6/method_summary.csv').exists())
    def test_unconfigured_adapter_refuses_fabrication(self):
        from hrs.adapter import UnconfiguredAdapter
        with self.assertRaisesRegex(NotImplementedError,'No research trials'):
            UnconfiguredAdapter().execute_registered_stage(PACKAGE,'E1',{}, {})
    def test_primary_analysis_and_plot_positive_path_in_temporary_fixture(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for d in ('hrs','scripts','config'):
                shutil.copytree(PACKAGE/d,root/d,ignore=shutil.ignore_patterns('__pycache__'))
            for name in ('AGENTS.md','agent.md'): shutil.copyfile(PACKAGE/name,root/name)
            (root/'state/receipts').mkdir(parents=True)
            # Small fixture workflow isolates CLI wiring; it does not pretend to pass E0-E4.
            workflow.save_json(root/'config/sequence.json',[{'id':'E5'},{'id':'E6'},{'id':'E7'}])
            workflow.save_json(root/'state/receipts/e5_fixture.json',{'fingerprints':{}})
            workflow.save_json(root/'state/status.json',{'stages':{
                'E5':{'status':'passed','receipt':'state/receipts/e5_fixture.json','receipt_sha256':digest(root/'state/receipts/e5_fixture.json')},
                'E6':{'status':'running'},'E7':{'status':'running'}}})
            lock=workflow.read_json(root/'config/final_lock.json')
            methods=['B0','B1','B2','B4','B5','M']
            for k,v in lock.items():
                if v is None: lock[k]='software fixture only'
            lock.update(status='FROZEN',primary_comparator='B5',included_methods=methods,unavailable_methods={'B3':'unit fixture excludes B3'},
                primary_policy_sha256='a'*64,baseline_policy_sha256={m:'a'*64 for m in methods if m!='M'},primitive_library_sha256='a'*64,
                contact_tolerance_n=.01,decision_deadline_ms=1000,confirmatory_base_scenarios={'E6':6,'E7':6},test_scenario_registry='config/registry_fixture.json')
            registry=[]; allrows={}
            for stage in ('E6','E7'):
                rows=[]
                for i in range(6):
                    for method in methods:
                        r=fixture(root,data_kind='measured_simulation',stage_id=stage,scenario_id=f'{stage}-fixture-{i}',run_id=f'{stage}-{i}-{method}',method=method,task=f'T{1+i//2}')
                        r['measurements']['robot_human_contact']=(i==0 if method=='M' else i in (0,2,4))
                        r['measurements']['task_success']=(i!=5 if method=='M' else i!=4)
                        rows.append(r)
                        registry.append({k:r[k] for k in ('stage_id','scenario_id','method','task','stratum','snapshot_sha256','scenario_sha256','human_trajectory_sha256')})
                allrows[stage]=rows
            workflow.save_json(root/'config/registry_fixture.json',registry)
            workflow.save_json(root/'config/final_lock.json',lock)
            for stage,rows in allrows.items():
                p=root/f'results/raw/{stage}/records.jsonl'; p.parent.mkdir(parents=True)
                for r in rows:r['config_sha256']=digest(root/'config/final_lock.json')
                p.write_text(''.join(json.dumps(r)+'\n' for r in rows))
            for stage in ('E6','E7'):
                proc=subprocess.run([sys.executable,str(root/'scripts/analyze.py'),'--stage',stage],cwd=root,capture_output=True,text=True)
                self.assertEqual(proc.returncode,0,proc.stderr)
                result=workflow.read_json(root/f'results/computed/{stage}/paired_primary.json')
                self.assertAlmostEqual(result['human_hazard']['difference'],-1/3)
                self.assertEqual(result['human_hazard']['n_scenarios'],6)
            plot=subprocess.run([sys.executable,str(root/'scripts/plot_results.py'),'--stage','E6'],cwd=root,capture_output=True,text=True)
            self.assertEqual(plot.returncode,0,plot.stderr)
            self.assertGreater((root/'results/computed/E6/human_hazard_rates.png').stat().st_size,1000)
            dest=root/'verification/reproductions/e6_fixture'
            proc=subprocess.run([sys.executable,str(root/'scripts/analyze.py'),'--stage','E6','--reproduce-to',str(dest)],cwd=root,capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
            for filename in ('method_summary.csv','paired_primary.json','interpretation.md'):
                self.assertEqual(digest(dest/filename),digest(root/f'results/computed/E6/{filename}'))

if __name__=='__main__': unittest.main()
