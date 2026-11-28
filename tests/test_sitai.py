"""司汰（SITAI）v0.1 单测：三算子＋门面＋legacy 兼容＋边界。"""
import unittest

from sitai import Ce, Jin, Sitai, Tai


class TestTai(unittest.TestCase):
    def test_cull_invalid(self):
        kept = Tai().cull([{"m": 1}, {"m": 2, "valid": False}, {"m": 3}])
        self.assertEqual(kept, [{"m": 1}, {"m": 3}])

    def test_cull_keeps_non_dict(self):
        kept = Tai().cull(["文本", 42, {"valid": False}, None])
        self.assertEqual(kept, ["文本", 42, None])

    def test_cull_all_invalid(self):
        self.assertEqual(Tai().cull([{"valid": False}, {"valid": False}]), [])

    def test_cull_records_event(self):
        tai = Tai()
        tai.cull([{"valid": False}, {"m": 1}])
        self.assertEqual(tai.events[0]["removed"], 1)


class TestJin(unittest.TestCase):
    def test_pan_dedup(self):
        kept = Jin().pan([{"m": 1}, {"m": 1}, {"m": 2}])
        self.assertEqual(kept, [{"m": 1}, {"m": 2}])

    def test_pan_keeps_first_occurrence(self):
        kept = Jin().pan([{"m": 1, "v": "首"}, {"m": 1, "v": "首"}])
        self.assertEqual(kept, [{"m": 1, "v": "首"}])

    def test_pan_key_order_insensitive(self):
        kept = Jin().pan([{"a": 1, "b": 2}, {"b": 2, "a": 1}])
        self.assertEqual(len(kept), 1)

    def test_pan_mixed_types(self):
        kept = Jin().pan(["x", "x", 3, 3, None, None])
        self.assertEqual(kept, ["x", 3, None])


class TestCe(unittest.TestCase):
    def test_record_seq_incremental(self):
        ce = Ce()
        e1 = ce.record("prune", {"in": 3})
        e2 = ce.record("prune", {"in": 2})
        self.assertEqual((e1["seq"], e2["seq"]), (1, 2))

    def test_replay_filter(self):
        ce = Ce()
        ce.record("prune", {"in": 3})
        ce.record("audit", {"note": "x"})
        self.assertEqual(len(ce.replay()), 2)
        self.assertEqual(len(ce.replay("prune")), 1)

    def test_replay_is_copy(self):
        ce = Ce()
        ce.record("prune", {"in": 1})
        out = ce.replay()
        out.clear()
        self.assertEqual(len(ce.replay()), 1)

    def test_summary(self):
        ce = Ce()
        ce.record("prune", {})
        ce.record("prune", {})
        self.assertEqual(ce.summary(), {"prune": 2})


class TestTamperEvidence(unittest.TestCase):
    """篡改现形：台账只增不覆盖，任何对副本的篡改都必须现形。"""

    def test_ledger_resists_external_tamper(self):
        ce = Ce()
        e1 = ce.record("prune", {"in": 3, "kept": 2})
        e1["detail"]["in"] = 999          # 试图篡改已入册的记录
        e1["action"] = "fake"
        self.assertEqual(ce.replay()[0]["detail"]["in"], 3)   # 正本无损，篡改现形
        self.assertEqual(ce.replay()[0]["action"], "prune")

    def test_replay_copy_tamper_visible(self):
        ce = Ce()
        ce.record("prune", {"in": 1})
        out = ce.replay()
        out[0]["action"] = "篡改"
        self.assertEqual(ce.replay()[0]["action"], "prune")

    def test_seq_cannot_be_rewritten(self):
        ce = Ce()
        ce.record("prune", {})
        ce.record("prune", {})
        seqs = [e["seq"] for e in ce.replay()]
        self.assertEqual(seqs, [1, 2])    # 序号连续，抽掉或改写即现形


class TestFacade(unittest.TestCase):
    def setUp(self):
        self.op = Sitai()

    def test_prune_returns_kept_list(self):
        kept = self.op.prune([{"m": 1}, {"m": 1}, {"m": 2, "valid": False}, {"m": 3}])
        self.assertEqual(kept, [{"m": 1}, {"m": 3}])

    def test_prune_detailed_view(self):
        r = self.op.prune_detailed([{"m": 1}, {"m": 1}, {"m": 2, "valid": False}], ledger_id="L-01")
        self.assertEqual(r["pruned"], 2)
        self.assertEqual(r["ledger_id"], "L-01")
        self.assertEqual(r["entry"]["detail"]["duplicates_removed"], 1)
        self.assertEqual(r["entry"]["detail"]["invalid_removed"], 1)

    def test_replay_full_chain(self):
        self.op.prune([{"m": 1}])
        self.op.prune([{"m": 2, "valid": False}])
        entries = self.op.replay("prune")
        self.assertEqual(len(entries), 2)
        self.assertEqual(self.op.ledger_summary(), {"prune": 2})

    def test_legacy_describe_unchanged(self):
        """回归：骨架 v1 名帖字段与取值不变（回归用例）。"""
        d = self.op.describe()
        self.assertEqual(d["repo"], "sitai")
        self.assertEqual(d["code"], "SITAI")
        self.assertEqual(d["mingwen"], "汰沙存金，损而不匮")
        self.assertTrue(d["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))

    def test_legacy_report_unchanged(self):
        """回归：骨架 v1 prune/report 计数行为不变（回归用例）。"""
        self.op.prune([{"m": 1}, {"m": 1}, {"m": 2, "valid": False}, {"m": 3}])
        self.assertEqual(self.op.report(), {"pruned": 2, "kept": 2})

    def test_empty_input(self):
        self.assertEqual(self.op.prune([]), [])
        self.assertEqual(self.op.report(), {"pruned": 0, "kept": 0})


if __name__ == "__main__":
    unittest.main()
