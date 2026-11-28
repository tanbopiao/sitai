"""司汰（SITAI）· MEM-04 遗忘修剪：修剪失效记忆与冗余。

命名即种子：司汰＝《宋史·选举志》汰冗员，义理出《道德经》「为学日益，为道日损」。
逻辑本体：记忆库要常汰常新——失效的剪掉、冗余的淘去、每一剪都入册可回放。

三算子：
- 汰（tai.Tai）  汰冗官：剔除 valid=False 的失效记忆。
- 金（jin.Jin）  存金官：等价去重，沙里淘金，只留一件。
- 册（ce.Ce）    修剪台账官：只增不覆盖的修剪流水，可回放。

三算子合枢于 Sitai 门面（prune / report / replay）。
原单文件骨架 API（describe / prune / report）收编保留，行为不变。
"""

from .legacy import Sitai as _LegacySitai
from .tai import Tai
from .jin import Jin
from .ce import Ce

__all__ = ["Sitai", "Tai", "Jin", "Ce"]


class Sitai(_LegacySitai):
    """司汰门面：原 v1 API 之上长出汰/金/册三算子。"""

    def __init__(self, config=None):
        super().__init__(config)
        self._tai = Tai()
        self._jin = Jin()
        self._ce = Ce()

    def prune(self, memories, ledger_id=None):
        """汰沙存金：先汰冗、再淘金，全程入册。

        原 v1 行为不变（返回存活列表）；入册为增量行为，不改返回值。
        """
        after_tai = self._tai.cull(memories)
        kept = self._jin.pan(after_tai)
        pruned = len(memories) - len(kept)
        entry = self._ce.record("prune", {
            "ledger_id": ledger_id,
            "in": len(memories),
            "kept": len(kept),
            "pruned": pruned,
            "invalid_removed": len(memories) - len(after_tai),
            "duplicates_removed": len(after_tai) - len(kept),
        })
        # legacy 计数与事件同步留痕（原字段语义不变）
        self.pruned_count += pruned
        self.kept_count += len(kept)
        self.events.append({"event": "prune", "pruned": pruned})
        return kept

    def prune_detailed(self, memories, ledger_id=None):
        """修剪并返回台账视图：{kept, pruned, ledger_id, entry}。"""
        kept = self.prune(memories, ledger_id=ledger_id)
        entry = self._ce.replay("prune")[-1]
        return {
            "kept": kept,
            "pruned": len(memories) - len(kept),
            "ledger_id": ledger_id,
            "entry": entry,
        }

    def replay(self, action=None):
        """册：回放修剪流水（只增不覆盖）。"""
        return self._ce.replay(action)

    def ledger_summary(self):
        """册：修剪对账摘要。"""
        return self._ce.summary()
