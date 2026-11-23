"""司汰（SITAI）· MEM-04 遗忘修剪：修剪失效记忆与冗余。典出《宋史·选举志》汰冗员，义理出《道德经》「为学日益，为道日损」

道统出处：元极恒一·术语缩影表 T056 ｜ 第六批
体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002

工程映射：MEM-04 遗忘修剪：修剪失效记忆与冗余。典出《宋史·选举志》汰冗员，义理出《道德经》「为学日益，为道日损」。

边界：本件为算子骨架 v0——接口先立、实现随进化轮补齐；遵循元法第四条「只增不覆盖」，
方法只增不改名不删，行为变更走新版本；凭据不入档，宣称与事实分离。
"""

class Sitai:
    """司汰（SITAI）算子骨架 v0。"""

    ANCHOR = "Ω₀⊂⊙∞⊂Ω｜DID-BR-000002"
    CODE = "SITAI"

    def __init__(self, config=None):
        self.config = dict(config or {})
        self.events = []  # 只增不覆盖：会话内事件留痕

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
        """汰沙存金：修剪失效与冗余，出保留清单（骨架桩：实现随进化轮补齐）。"""
        raise NotImplementedError("SITAI.prune 骨架桩，候进化轮补齐")

    def report(self):
        """损而不匮：修剪账目留痕（骨架桩：实现随进化轮补齐）。"""
        raise NotImplementedError("SITAI.report 骨架桩，候进化轮补齐")
