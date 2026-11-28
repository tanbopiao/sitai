"""金（JIN）· 存金官：沙里淘金，冗余去重。

命名即种子：汰沙存金——存金官只认「等价」：内容完全等价的记忆无论来几遍，
只留一件；留的是第一件，后面的皆是沙。
"""

import json


class Jin:
    """存金官：等价去重，只留一件。"""

    CODE = "JIN"

    def __init__(self):
        self.events = []

    @staticmethod
    def _key(item):
        return json.dumps(item, sort_keys=True, ensure_ascii=False)

    def pan(self, memories):
        """淘金：等价项只留第一件，返回存活项。"""
        seen = set()
        kept = []
        for m in memories:
            key = self._key(m)
            if key in seen:
                continue
            seen.add(key)
            kept.append(m)
        self.events.append({"event": "pan", "in": len(memories), "kept": len(kept)})
        return kept

    def describe(self):
        return {"code": self.CODE, "cn": "存金官", "duty": "等价去重，只留一件"}
