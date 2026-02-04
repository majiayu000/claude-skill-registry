---
name: naming
description: 命名规范 / Naming conventions。在创建类、函数、变量，或重命名、检查命名时使用。核心原则：简洁优先，上下文消歧义，类型提示已提供足够信息。Use when naming classes/functions/variables, renaming code, or reviewing names. Prioritizes brevity over self-documentation.
---

# Naming conventions for fund-portfolio-bot

本 Skill 定义项目的命名规范，核心哲学是 **上下文消歧义**（Context-Aware Minimal Naming）。

## When to use

在以下场景使用本 Skill（触发词：命名、取名、重命名、名字太长、naming、rename）：

- 创建新的类、函数、变量时
- 重命名现有代码时
- 代码评审时检查命名是否简洁
- 设计新模块时确定命名风格
- 用户提到"名字太长"、"命名太啰嗦"、"简化命名"时

## 核心哲学

```
┌────────────────────────────────────────────────────────────┐
│         名字只需在其出现的上下文中唯一消歧义                 │
│                                                            │
│   模块路径 + 类型提示 + 简短名字 = 完整语义                 │
└────────────────────────────────────────────────────────────┘
```

**背景**：本项目是 AI 驱动开发的独立项目，代码由开发者自己维护。类型提示、IDE 导航、AI 辅助已经提供了足够的上下文，名��不需要过度自解释。

---

## 五条规则

### 规则 1：领域名词保持完整

这些是领域建模的"根"，不能简化：

```
Trade / Fund / Nav / Dca / Action / Restriction / Policy / Config / Batch
Repo / Service / Client
```

### 规则 2：上下文不重复

模块路径已有的信息，类名不再重复。

```python
# BAD - 模块名已经是 fund_restriction
from src.core.models.fund_restriction import FundRestrictionFact

# GOOD
from src.core.models.fund_restriction import Restriction
from src.core.models.fund_restriction import Fact
```

```python
# BAD - 模块名已经是 dca_backfill
class DcaDayCheck: ...
class FundDcaFacts: ...

# GOOD
class DayCheck: ...
class Facts: ...  # 或 DcaFacts（保留一级前缀）
```

### 规则 3：后缀按需使用

后缀仅在需要区分时使用：

| 后缀 | 含义 | 何时使用 |
|------|------|----------|
| `Result` | 函数返回的聚合结果 | 需要区分动词和名词时 |
| `Facts` | 规则层只读快照 | AI 分析场景 |
| `Draft` | 待确认的建议方案 | 不入库的中间结构 |
| `Check` | 检查/验证结果 | 规则层输出 |
| `Flag` | 标记/警告 | 异常标识 |

**简化示例**：

```python
# BAD
class BackfillDaysResult: ...

# GOOD
class BackfillResult: ...
```

### 规则 4：参数名极简

类型提示已说明类型，变量名只需说明角色。

```python
# BAD
def foo(trade_repo: TradeRepo, fund_code: str, trade_date: date): ...

# GOOD
def foo(repo: TradeRepo, code: str, day: date): ...
```

**常用简化映射**：

| 冗余写法 | 简化写法 | 说明 |
|----------|----------|------|
| `fund_code` | `code` | 基金上下文已知 |
| `trade_date` | `day` / `on` | 类型已知是 date |
| `trade_repo` | `repo` | 类型已知是 TradeRepo |
| `dca_plan_key` | `dca_key` / `key` | 上下文已知 |
| `confirmation_status` | `state` | 简单词优先 |
| `delayed_reason` | `delay_reason` | 去掉 ed |

### 规则 5：函数名动词优先

```
动词（必需） + 对象（仅当上下文不明确时）
```

```python
# BAD - 过度描述
def build_dca_facts_for_batch(): ...
def get_dca_day_checks(): ...
def update_dca_plan_key_bulk(): ...

# GOOD - 动词 + 最小限定
def build_facts(): ...      # batch_id 是参数，不需要在函数名里
def day_checks(): ...       # 或 checks()
def tag_dca(): ...          # 或 set_keys()
```

---

## 具体示例

### 模块级重命名示例

**dca_backfill 模块**（典型冗余案例）：

```python
# 现有
class DcaDayCheck: ...
class BackfillDaysResult: ...
class FundDcaFacts: ...
class SkippedTrade: ...
def build_dca_facts_for_batch(): ...
def get_dca_day_checks(): ...

# 建议
class DayCheck: ...         # 模块已知是 dca
class BackfillResult: ...   # 简化
class Facts: ...            # 或 DcaFacts
class Skipped: ...          # 上下文已知是 trade
def build_facts(): ...      # batch_id 是参数
def checks(): ...           # 或 day_checks()
```

### 字段命名示例

```python
# 现有
@dataclass
class Trade:
    confirmation_status: str
    delayed_reason: str | None
    delayed_since: date | None
    dca_plan_key: str | None
    import_batch_id: int | None

# 建议
@dataclass
class Trade:
    state: str              # 或 confirm_state
    delay_reason: str | None
    delay_since: date | None
    dca_key: str | None
    batch_id: int | None    # import 上下文已知
```

---

## 边界情况

### 何时保留完整名字

1. **跨模块导出**：如果类会被多个模块 import，保留前缀避免歧义
   ```python
   # 在 __init__.py 导出时保留完整名
   from .dca_backfill import DcaFacts  # 不是 Facts
   ```

2. **领域核心模型**：Trade, Fund, Nav 等不简化

3. **容易混淆的场景**：如果简化后有歧义，保留

### 渐进式应用

- 新代码遵循新规范
- 重构时顺便改旧代码
- 不要求一次性重命名所有代码

---

## 与其他 Skill 的关系

- **code-style**：定义类型注解、docstring 等通用规范
- **naming**（本 Skill）：专注命名简洁性
- **architecture**：定义分层和依赖方向

命名规范是 code-style 的子集，但更专注、更激进。
