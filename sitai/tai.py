"""汰（TAI）· 汰冗官：剔除失效。

命名即种子：司汰之「汰」——《宋史·选举志》汰冗员。汰冗官只管一件事：
凡 valid=False 的失效记忆，一律剪除；有效与否之外，它不置一词。
"""


class Tai:
    """汰冗官：剔除失效记忆。"""

    CODE = "TAI"

    def __init__(self):
        self.events = []

    def cull(self, memories):
        """汰冗：剪除 valid=False 的失效项，返回存活项。"""
        kept = [m for m in memories if not (isinstance(m, dict) and m.get("valid") is False)]
        removed = len(memories) - len(kept)
        self.events.append({"event": "cull", "in": len(memories), "removed": removed})
        return kept

    def describe(self):
        return {"code": self.CODE, "cn": "汰冗官", "duty": "剪失效，不问其余"}
