"""司汰端到端演示：汰冗→淘金→入册→回放。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sitai import Sitai

gate = Sitai()

memories = [
    {"id": 1, "text": "用户偏好深色主题"},
    {"id": 1, "text": "用户偏好深色主题"},          # 冗余：等价重复
    {"id": 2, "text": "旧版接口已下线", "valid": False},  # 失效
    {"id": 3, "text": "周三例会改到周四"},
]

kept = gate.prune(memories, ledger_id="MEM-04-001")
print("修剪后存活：", kept)
print("对账：", gate.report())
print("台账回放：")
for e in gate.replay("prune"):
    print(" ", e["seq"], e["detail"])
