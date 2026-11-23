"""司汰（SITAI）算子骨架单测：名帖完整、桩位齐整、只增不覆盖。"""
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

    def test_prune_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.prune(None)

    def test_report_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.report()


if __name__ == "__main__":
    unittest.main()
