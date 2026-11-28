"""册（CE）· 修剪台账官：只增不覆盖，可回放。

命名即种子：修剪必有册——台账官把每一次修剪记成流水：汰了什么、留了什么，
一条不落、一条不改；台账只增不覆盖，随时回放。
"""

import copy
import time


class Ce:
    """修剪台账官：只增不覆盖的修剪流水。"""

    CODE = "CE"

    def __init__(self):
        self._entries = []

    def record(self, action, detail):
        """记一笔：动作＋摘要，附时间与序号，只增不覆盖。"""
        entry = {
            "seq": len(self._entries) + 1,
            "action": action,
            "detail": detail,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S+08:00", time.localtime()),
        }
        self._entries.append(copy.deepcopy(entry))
        return entry

    def replay(self, action=None):
        """回放：按动作过滤的流水副本（外部改不动正本）。"""
        if action is None:
            return copy.deepcopy(self._entries)
        return copy.deepcopy([e for e in self._entries if e["action"] == action])

    def summary(self):
        """对账：各动作笔数。"""
        out = {}
        for e in self._entries:
            out[e["action"]] = out.get(e["action"], 0) + 1
        return out

    def describe(self):
        return {"code": self.CODE, "cn": "修剪台账官", "duty": "只增不覆盖，可回放"}
