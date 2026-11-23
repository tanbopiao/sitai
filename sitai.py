"""司汰（SITAI）· MEM-04 遗忘修剪：修剪失效记忆与冗余。典出《宋史·选举志》汰冗员，义理出《道德经》「为学日益，为道日损」

道统出处：元极恒一·术语缩影表 T056 ｜ 第六批
体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002

工程映射：MEM-04 遗忘修剪：修剪失效记忆与冗余。典出《宋史·选举志》汰冗员，义理出《道德经》「为学日益，为道日损」。

边界：本件为算子 v1——骨架桩已按命名映射补齐实现；遵循元法第四条「只增不覆盖」，
方法只增不改名不删，行为变更走新版本；凭据不入档，宣称与事实分离。
"""

class Sitai:
    """司汰（SITAI）算子 v1。"""

    ANCHOR = "Ω₀⊂⊙∞⊂Ω｜DID-BR-000002"
    CODE = "SITAI"

    def __init__(self, config=None):
        self.config = dict(config or {})
        self.events = []  # 只增不覆盖：会话内事件留痕
        self.pruned_count = 0
        self.kept_count = 0

    def describe(self):
        """构件名帖：名、代号、职责、铭文、体系锚。"""
        return {
            "repo": "sitai",
            "cn": "司汰",
            "code": self.CODE,
            "duty": "MEM-04 遗忘修剪：修剪失效记忆与冗余。典出《宋史·选举志》汰冗员，义理出《道德经》「为学日益，为道日损」",
            "mingwen": "汰沙存金，损而不匮",
            "anchor": self.ANCHOR,
        }

    def prune(self, memories):
        """汰沙存金：剪失效与冗余，留有效唯一。"""
        import json
        seen = set()
        kept = []
        for m in memories:
            if isinstance(m, dict) and m.get("valid") is False:
                continue
            key = json.dumps(m, sort_keys=True, ensure_ascii=False)
            if key in seen:
                continue
            seen.add(key)
            kept.append(m)
        self.pruned_count += len(memories) - len(kept)
        self.kept_count += len(kept)
        self.events.append({"event": "prune", "pruned": len(memories) - len(kept)})
        return kept

    def report(self):
        """修剪台账。"""
        return {"pruned": self.pruned_count, "kept": self.kept_count}
