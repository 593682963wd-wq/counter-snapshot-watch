import unittest,tempfile,json
from pathlib import Path
from core import run

class Tests(unittest.TestCase):
 def test_delta(self):self.assertEqual(run(json.loads(Path('example.json').read_text()))['events'][0]['delta'],3)
 def test_empty(self):self.assertEqual(run({})['events'],[])
 def test_bad_order(self):
  with self.assertRaises(ValueError):run({'snapshots':[{'time':1,'counts':{}},{'time':1,'counts':{}}]})
 def test_reset(self):self.assertTrue(run({'snapshots':[{'time':0,'counts':{'x':8}},{'time':60,'counts':{'x':2}}]})['events'][0]['reset'])
 def test_anomaly(self):
  snapshots=[{'time':i*60,'counts':{'x':i if i<8 else 100}} for i in range(9)]
  self.assertTrue(run({'snapshots':snapshots})['events'][-1]['anomaly'])

if __name__=="__main__":unittest.main()
