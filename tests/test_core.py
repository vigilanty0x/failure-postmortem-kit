import unittest
from failure_postmortem_kit import build,probe
S={"incident":"i","impact":"x","timeline":["t"],"evidence":["e"],"causes":["c"],"actions":[{"owner":"o","due":"d","action":"a"}]}
class T(unittest.TestCase):
 def test_build(self):self.assertTrue(build(S)["ok"])
 def test_evidence_required(self):self.assertFalse(build({**S,"evidence":[]})["ok"])
 def test_owner_required(self):self.assertFalse(build({**S,"actions":[{"action":"a"}]})["ok"])
 def test_probe(self):self.assertTrue(probe()["ok"])
if __name__=="__main__":unittest.main()
