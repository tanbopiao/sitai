"""汰簪（SITAI）算子单测：名帖完整、行为达标、只增不覆盖。"""
import unittest

from sitai import Sitai


class TestSitai(unittest.TestCase):
    def setUp(self):
        self.op = Sitai()

    def test_describe(self):
        d = self.op.describe()
        self.assertEqual(d["repo"], "sitai")
        self.assertEqual(d["code"], "SITAI")
        self.assertTrue(d["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))
        self.assertTrue(d["mingwen"])

    def test_prune(self):
        kept = self.op.prune([{"m": 1}, {"m": 1}, {"m": 2, "valid": False}, {"m": 3}])
        self.assertEqual(kept, [{"m": 1}, {"m": 3}])
        self.assertEqual(self.op.report(), {"pruned": 2, "kept": 2})


if __name__ == "__main__":
    unittest.main()
