import csv
import tempfile
import unittest
from pathlib import Path
import numpy as np
from src.dgps import generate
from src.methods import estimate
from src.metrics import summarize
from src.simulation import run

class StudyTests(unittest.TestCase):
    def test_normal_dgp(self):
        x=generate(np.random.default_rng(40),"normal",100,2000,2)
        self.assertAlmostEqual(x.mean(),2,delta=.015)
        self.assertAlmostEqual(x.var(),1,delta=.025)

    def test_methods_and_translation(self):
        x=np.array([[1.,2.,9.],[2.,4.,6.]])
        result=estimate(x)
        np.testing.assert_allclose(result["mean"],[4,4])
        np.testing.assert_allclose(result["median"],[2,4])
        for k,v in estimate(x+7).items():
            np.testing.assert_allclose(v,result[k]+7)

    def test_metrics(self):
        s=summarize([1,2,3],2)
        self.assertEqual(s["bias"],0)
        self.assertAlmostEqual(s["mse"],2/3)
        self.assertAlmostEqual(s["variance"],1)
        self.assertGreater(s["mse_mcse"],0)

    def test_reproducibility_and_batch_invariance(self):
        cfg=dict(seed=8,replicates=20,sample_sizes=[20],distributions=["normal","student_t3","contaminated_normal"],location=0,batch_size=7)
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/"a.csv",Path(d)/"b.csv"
            run(cfg,a)
            run(cfg,b)
            self.assertEqual(a.read_bytes(),b.read_bytes())
            cfg["batch_size"]=3
            run(cfg,b)
            self.assertEqual(a.read_bytes(),b.read_bytes())
            with a.open() as f:
                rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),120)
            self.assertTrue(all(np.isfinite(float(r["estimate"])) for r in rows))

    def test_normal_mean_theory(self):
        x=generate(np.random.default_rng(504),"normal",20,10000)
        mse=summarize(estimate(x)["mean"],0)["mse"]
        self.assertAlmostEqual(mse,1/20,delta=.003)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            generate(np.random.default_rng(1),"unknown",20,2)
        with self.assertRaises(ValueError):
            summarize([float("nan"),1],0)

if __name__ == "__main__":
    unittest.main()
