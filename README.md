# sitai · 司汰

**MEM-04 遗忘修剪：修剪失效记忆与冗余。**

> 命名即种子：司汰＝《宋史·选举志》汰冗员，义理出《道德经》「为学日益，为道日损」。名字所对应的逻辑与架构，是从种子长出来的。

## 命名映射（道统 → 架构）

| 道 | 义 | 算子 |
|----|----|------|
| 汰 | 汰冗员——剪除失效记忆（valid=False） | `Tai` 汰冗官 |
| 金 | 汰沙存金——等价去重，只留一件 | `Jin` 存金官 |
| 册 | 修剪必有册——只增不覆盖的修剪流水，可回放 | `Ce` 修剪台账官 |

逻辑本体：**记忆库要常汰常新——失效的剪掉、冗余的淘去、每一剪都入册可回放。**
不是提醒修剪者别漏记，而是结构上每一剪自动入册，只增不覆盖。

## 安装

零第三方依赖，仅 Python 3.10+ 标准库。

```bash
git clone https://github.com/tanbopiao/sitai.git
cd sitai
python -m unittest discover -s tests -v   # 自测
python examples/demo_prune.py             # 端到端演示
```

## 用法

```python
from sitai import Sitai

gate = Sitai()

memories = [
    {"id": 1, "text": "用户偏好深色主题"},
    {"id": 1, "text": "用户偏好深色主题"},          # 冗余
    {"id": 2, "text": "旧版接口已下线", "valid": False},  # 失效
    {"id": 3, "text": "周三例会改到周四"},
]

kept = gate.prune(memories, ledger_id="MEM-04-001")
print(gate.report())          # {'pruned': 2, 'kept': 2}
print(gate.replay("prune"))   # 台账回放：每次汰了什么、留了什么
```

原单文件骨架 API（`describe()` / `prune()` / `report()`）收编保留，行为不变。

## 自测

```bash
python -m unittest discover -s tests -v
```

## 许可

MIT
