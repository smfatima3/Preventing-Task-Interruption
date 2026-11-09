"""Known-answer synthetic unit tests. No scientific results are generated."""
import unittest
try:
    from hrs.analysis import *
    HAVE_ANALYSIS=True
except ImportError:
    HAVE_ANALYSIS=False

@unittest.skipUnless(HAVE_ANALYSIS,'Install requirements-analysis.txt to test analysis')
class StatisticsTests(unittest.TestCase):
    def test_known_paired_difference_and_identity(self):
        result=paired_binary([0,1,0,0],[1,0,1,0],['T1']*4)
        self.assertAlmostEqual(result['difference'],-.25)
        self.assertEqual((result['introduced']-result['prevented'])/4,result['difference'])
        self.assertEqual(result['n_scenarios'],4)
    def test_bootstrap_reproducible(self):
        a=bootstrap_difference([-1,0,1,0],['T1','T1','T2','T2'])
        b=bootstrap_difference([-1,0,1,0],['T1','T1','T2','T2'])
        self.assertEqual(a,b)
    def test_zero_events_not_zero_risk(self):
        r=paired_binary([0]*20,[0]*20,['T1']*20)
        self.assertTrue(r['degenerate']); self.assertFalse(r['superiority_screen'])
        self.assertGreater(r['m_rate_ci95'][1],0); self.assertEqual(r['exact_mcnemar_two_sided_p'],1)
    def test_exact_binomial_bounds(self):
        lo,hi=exact_rate_interval(0,100)
        self.assertEqual(lo,0); self.assertAlmostEqual(hi,1-.025**(1/100))
        self.assertEqual(exact_rate_interval(100,100)[1],1)
    def test_mcnemar_known_case(self):
        r=paired_binary([0]*10,[1]*10,['T1']*10)
        self.assertAlmostEqual(r['exact_mcnemar_two_sided_p'],2/1024)
        self.assertTrue(r['degenerate'])
    def test_holm_known_values(self):
        self.assertEqual(holm_adjust([.01,.04,.03]),[.03,.06,.06])
    def test_calibration_denominators(self):
        r=calibration([0.,.2,.8,1.],[0,1,1,0],[False,False,True,False])
        self.assertEqual(r['n_approved'],1); self.assertEqual(r['n_hazardous'],2)
        self.assertEqual(r['p_hazard_given_approved'],1); self.assertEqual(r['p_approved_given_hazardous'],.5)
        self.assertEqual(sum(x['n'] for x in r['reliability']),4)
    def test_cluster_size_not_row_count(self):
        rows=[]
        for sid in range(6):
            for delay in (0,100,300,600):
                for method in ('M','B5'):
                    rows.append({'scenario_id':str(sid),'task':'T1','method':method,'delay':delay,'metric':(sid%2 if method=='M' else 1)})
        r=clustered_repeated_difference(rows,'M','B5',lambda x:x['metric'],['delay'])
        self.assertEqual(r['n_scenarios'],6); self.assertEqual(r['conditions_per_scenario'],4)
        self.assertEqual(r['difference'],-.5)
        with self.assertRaises(ValidationError): clustered_repeated_difference(rows[:-1],'M','B5',lambda x:x['metric'],['delay'])
    def test_invalid_probabilities_rejected(self):
        with self.assertRaises(ValueError): calibration([1.2],[1],[True])
        with self.assertRaises(ValueError): holm_adjust([float('nan')])

if __name__=='__main__': unittest.main()
