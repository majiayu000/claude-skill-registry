---
name: architecture
description: 分层架构规范 / Architecture and layering rules (v0.3.1)。在设计新组件、修改导入、检查分层时使用。核心约束：cli → flows → data，core 向内不向外。Use when designing components, changing imports, or reviewing layering decisions. Enforces cli/flows/core/data separation.
---

# Architecture and layering for fund-portfolio-bot (v0.3.1)

本 Skill 关注分层职责与依赖方向。详细说明参见 `docs/architecture.md`。

## When to use

在以下场景使用本 Skill（触发词：分层、导入、架构、依赖、architecture、layering、import）：

- 设计新模块或新功能时
- 修改 import 语句或依赖时
- 代码评审时检查分层是否正确
- 用户提到"我应该把这个放在哪一层"、"这个导入对吗"、"循环依赖"时

## 层次结构概览（v0.3.1 简化版 + 依赖注入）

项目采用自外向内依赖的 3 层架构 + 依赖注入：

- `cli/`：命令行入口，参数解析 + 调用 Flow 函数
- `flows/`：业务流程函数（纯函数 + `@dependency` 装饰器）
- `core/`：核心逻辑 + 依赖注入
  - `models/`：领域数据类（Trade, Fund, DcaPlan 等）
  - `rules/`：纯业务规则函数（settlement, rebalance 等）
  - `dependency.py`：依赖注入装饰器（@dependency, @register）
  - `container.py`：依赖工厂函数集合
  - `config.py`, `log.py`：配置和日志
- `data/`：数据访问层
  - `db/`：数据库 Repo（TradeRepo, NavRepo 等）
  - `client/`：外部客户端（Eastmoney, Discord 等）

## 依赖规则（必须遵守）

依赖方向：**只能向内依赖**：

```
cli → flows → data
        ↓       ↓
      core ← ← ←
        ↑
    container（创建 data 层实例）
```

- `core/`
  - 只能依赖 `core/` 内部模块
  - **例外**：`container.py` 可以导入 `data/`（用于创建实例）
  - **不得**导入 `cli/`、`flows/`

- `flows/`
  - 可以依赖 `core/`（models + rules + dependency）
  - **通过 @dependency 装饰器注入** `data/` 层实例（不直接导入）
  - **不得**导入 `cli/`

- `data/`
  - 可以依赖 `core/`（models + rules）
  - **不得**导入 `cli/`、`flows/`

- `cli/`
  - 可以依赖 `flows/`（调用函数）
  - **不需要**直接导入 `data/`（由装饰器处理）
  - 只做参数解析和流程调用

## 关键约束

1. **无 Protocol 抽象层**：
   - v0.3.1 删除了 `protocols.py`
   - 直接使用具体类：`TradeRepo`、`NavRepo` 等
   - 类的方法签名即为"接口约定"

2. **依赖注入机制**（v0.3.1 新增）：
   - `core/dependency.py`：提供 `@dependency` 和 `@register` 装饰器
   - `core/container.py`：集中管理所有依赖工厂函数
   - Flow 函数使用 `@dependency` 自动注入参数
   - CLI 无需手动实例化 Repo，直接调用 Flow 函数

3. **避免循环导入**：
   - 如需 TYPE_CHECKING，使用 `from typing import TYPE_CHECKING`
   - 类型注解使用字符串形式：`"TradeRepo"`

## 设计或修改代码时的步骤

1. **识别所在层级**
   - 判断文件属于 `cli` / `flows` / `core` / `data` 中的哪一层
   - 确保其职责与该层定位一致：
     - 命令行入口 + 流程函数 → `cli`
     - 业务流程编排 → `flows`
     - 数据模型 + 纯规则 → `core`
     - 数据库访问 + 外部客户端 → `data`

2. **检查依赖方向**
   - 确保 import 语句符合依赖规则
   - `core` 不能 import `flows` 或 `data`
   - `flows` 不能 import `cli`

3. **命名约定**
   - Repo 类：`TradeRepo`、`NavRepo`（不带 Sqlite 前缀）
   - Service 类：`CalendarService`、`EastmoneyNavService`
   - Flow 函数：小写蛇形（`create_trade()`、`confirm_trades()`、`make_daily_report()`）
   - Flow 文件：`trade.py`、`dca.py`、`market.py`、`report.py`
   - Result 类：`ConfirmResult`、`ReportResult`、`FetchNavsResult`

4. **类型注解**
   - 使用具体类型：`TradeRepo`、`FundRepo`
   - 避免循环导入时使用 TYPE_CHECKING
   - 字符串类型注解：`def __init__(self, repo: "TradeRepo")`

## 违反规则示例（禁止）

```python
# ❌ core/ 中导入 data/（除了 container.py）
from src.data.db.trade_repo import TradeRepo  # 禁止（models/rules 中）

# ❌ flows/ 中导入 cli/
from src.cli.confirm import main  # 禁止

# ❌ flows/ 中直接导入 data/（应使用装饰器注入）
from src.data.db.trade_repo import TradeRepo  # 禁止（应通过 @dependency）

# ❌ data/ 中导入 flows/
from src.flows.trade import confirm_trades  # 禁止
```

## 正确示例

```python
# ✅ container.py 注册依赖工厂
from src.core.dependency import register
from src.data.db.trade_repo import TradeRepo
from src.data.db.calendar import CalendarService

@register("trade_repo")
def get_trade_repo() -> TradeRepo:
    conn = get_db_connection()
    calendar = get_calendar_service()
    return TradeRepo(conn, calendar)

# ✅ flows/ 使用 @dependency 装饰器
from src.core.dependency import dependency
from src.core.models.trade import Trade
from src.data.db.trade_repo import TradeRepo  # 仅用于类型注解
from src.data.client.local_nav import LocalNavService

@dependency
def confirm_trades(
    *,
    today: date,
    trade_repo: TradeRepo | None = None,  # 自动注入
    nav_service: LocalNavService | None = None,  # 自动注入
) -> ConfirmResult:
    # 直接使用，无需检查 None
    to_confirm = trade_repo.list_pending(today)
    ...

# ✅ cli/ 直接调用 Flow 函数
from src.flows.trade import confirm_trades

def main():
    args = parse_args()
    result = confirm_trades(today=args.day)  # 依赖自动注入
    print(f"确认 {result.confirmed_count} 笔交易")
```

## 依赖注入使用指南

### 注册依赖（在 `src/core/container.py`）

```python
from src.core.dependency import register

@register("trade_repo")  # 注册名 = Flow 函数参数名
def get_trade_repo() -> TradeRepo:
    """注册名：trade_repo"""
    conn = get_db_connection()
    calendar = get_calendar_service()
    return TradeRepo(conn, calendar)
```

### 使用依赖（在 `src/flows/*.py`）

```python
from src.core.dependency import dependency

@dependency
def confirm_trades(
    *,
    today: date,
    trade_repo: TradeRepo | None = None,  # 参数名必须与注册名一致
) -> ConfirmResult:
    # trade_repo 已自动注入，直接使用
    ...
```

### 测试时覆盖依赖

```python
# 测试时手动传入 Mock 对象
mock_repo = MockTradeRepo()
result = confirm_trades(today=date.today(), trade_repo=mock_repo)
```

## 重构历史

- **v0.1-v0.3**：4 层架构（jobs → wiring → usecases(Protocol) → adapters）
- **v0.3.1 阶段 1**：3 层架构（cli → flows → data，删除 Protocol 和 wiring）
- **v0.3.1 阶段 2**：引入依赖注入（Flow 类改函数 + @dependency 装饰器）
