---
name: binance-futures-trading
description: 使用币安 USDT-M 永续合约 MCP 工具进行交易操作, 包括账户查询、杠杆设置、开仓平仓、止损止盈等.当需要执行币安合约交易相关操作时触发此技能.
---

# 币安 USDT 合约交易技能

## 概述

本技能提供币安 USDT-M 永续合约的完整交易功能, 通过 MCP 工具实现:

- 账户余额查询
- 持仓信息查询
- 杠杆/保证金模式设置
- 开仓/平仓操作
- 止损止盈设置
- 订单管理 (查询/撤销)

---

## 环境配置

### 必需的环境变量

```bash
# API 密钥 (必需)
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret

# 模拟交易模式 (默认 true, 不执行真实订单)
TRADING_SIMULATION=true

# 使用测试网 (可选, 默认 false)
BINANCE_USE_TESTNET=false
```

### 安全提醒

- **禁止**在代码中硬编码 API 密钥
- 建议先使用测试网验证策略
- 默认启用模拟模式, 防止误操作

---

## 可用工具

### 查询类 (只读)

| 工具名称 | 功能 | 参数 |
|----------|------|------|
| `binance_get_balance` | 查询账户余额 | `asset` (可选) |
| `binance_get_positions` | 查询持仓信息 | `symbol` (可选) |
| `binance_get_open_orders` | 查询普通挂单 (限价单等) | `symbol` (可选) |
| `binance_get_open_algo_orders` | 查询条件单 (止盈止损) | `symbol` (可选) |

> **注意**: 止盈止损订单使用 Algo Order API, 需要用 `binance_get_open_algo_orders` 查询, 不会出现在 `binance_get_open_orders` 中.

### 设置类

| 工具名称 | 功能 | 参数 |
|----------|------|------|
| `binance_change_leverage` | 设置杠杆倍数 | `symbol`, `leverage` (1-125) |
| `binance_change_margin_type` | 设置保证金模式 | `symbol`, `margin_type` (ISOLATED/CROSSED) |

### 交易类

| 工具名称 | 功能 | 关键参数 |
|----------|------|----------|
| `binance_place_order` | 下单 | `symbol`, `side`, `type`, `quantity` |
| `binance_close_position` | 平仓 | `symbol`, `quantity` (可选) |
| `binance_set_stop_loss_take_profit` | 设置止损止盈 | `symbol`, `stopLossPrice`, `takeProfitPrice` |
| `binance_cancel_order` | 撤销普通订单 | `symbol`, `orderId` |
| `binance_cancel_all_orders` | 撤销所有普通订单 | `symbol` |
| `binance_cancel_algo_order` | 撤销单个条件单 | `symbol`, `algoId` |
| `binance_cancel_all_algo_orders` | 撤销所有条件单 | `symbol` |

---

## 使用示例

### 1. 查询账户状态

```python
# 查询 USDT 余额
binance_get_balance(asset="USDT")

# 查询所有持仓
binance_get_positions()

# 查询指定交易对持仓
binance_get_positions(symbol="BTCUSDT")
```

### 2. 设置杠杆和保证金模式

```python
# 设置 BTCUSDT 杠杆为 10 倍
binance_change_leverage(symbol="BTCUSDT", leverage=10)

# 切换为逐仓模式 (有持仓时无法切换)
binance_change_margin_type(symbol="BTCUSDT", margin_type="ISOLATED")
```

### 3. 开仓

```python
# 市价做多 0.01 BTC
binance_place_order(
    symbol="BTCUSDT",
    side="BUY",
    type="MARKET",
    quantity=0.01,
    confirm_real_order=True  # 实盘必须
)

# 限价做空
binance_place_order(
    symbol="BTCUSDT",
    side="SELL",
    type="LIMIT",
    quantity=0.01,
    price=100000,
    timeInForce="GTC",
    confirm_real_order=True
)
```

### 4. 平仓

```python
# 全部平仓
binance_close_position(
    symbol="BTCUSDT",
    confirm_real_order=True
)

# 部分平仓
binance_close_position(
    symbol="BTCUSDT",
    quantity=0.005,
    confirm_real_order=True
)
```

### 5. 设置止损止盈

```python
# 同时设置止损和止盈
binance_set_stop_loss_take_profit(
    symbol="BTCUSDT",
    stopLossPrice=95000,
    takeProfitPrice=110000,
    confirm_real_order=True
)

# 只设置止损
binance_set_stop_loss_take_profit(
    symbol="BTCUSDT",
    stopLossPrice=95000,
    confirm_real_order=True
)
```

### 6. 订单管理

```python
# 查询普通挂单 (限价单等)
binance_get_open_orders(symbol="BTCUSDT")

# 查询条件单 (止盈止损订单)
binance_get_open_algo_orders(symbol="BTCUSDT")

# 撤销指定订单
binance_cancel_order(symbol="BTCUSDT", orderId=123456789)

# 撤销所有普通挂单
binance_cancel_all_orders(symbol="BTCUSDT")

# 撤销单个条件单 (止盈止损)
binance_cancel_algo_order(symbol="BTCUSDT", algoId=123456789)

# 撤销所有条件单 (止盈止损)
binance_cancel_all_algo_orders(symbol="BTCUSDT")
```

> **重要**:
> - 止盈止损订单使用 Algo Order API (2025-12-09 迁移后)
> - 查询条件单: `binance_get_open_algo_orders`
> - 撤销条件单: `binance_cancel_algo_order` 或 `binance_cancel_all_algo_orders`
> - 普通的 `binance_cancel_all_orders` **无法撤销条件单**

---

## 订单类型说明

| 类型 | 说明 | 必需参数 |
|------|------|----------|
| `MARKET` | 市价单, 立即成交 | `quantity` |
| `LIMIT` | 限价单 | `quantity`, `price`, `timeInForce` |
| `STOP_MARKET` | 止损市价单 | `stopPrice` |
| `TAKE_PROFIT_MARKET` | 止盈市价单 | `stopPrice` |
| `STOP` | 止损限价单 | `price`, `stopPrice` |
| `TAKE_PROFIT` | 止盈限价单 | `price`, `stopPrice` |

---

## 交易方向

**账户使用对冲模式 (Hedge Mode)**, 所有交易操作必须指定 `positionSide` 参数:

- **开多**: `side=BUY` + `positionSide=LONG`
- **平多**: `side=SELL` + `positionSide=LONG`
- **开空**: `side=SELL` + `positionSide=SHORT`
- **平空**: `side=BUY` + `positionSide=SHORT`

> 注意: 不要使用 `positionSide=BOTH`, 会报错 `-4061`

---

## 模拟交易模式

默认情况下, 所有交易类工具运行在**模拟模式**:

1. 不会执行真实订单
2. 返回模拟订单信息
3. 用于验证参数和策略逻辑

### 启用实盘交易

1. 设置环境变量: `TRADING_SIMULATION=false`
2. 调用时传入: `confirm_real_order=True`

```python
# 两个条件都满足才会执行真实订单
binance_place_order(
    symbol="BTCUSDT",
    side="BUY",
    type="MARKET",
    quantity=0.01,
    confirm_real_order=True  # 必须显式确认
)
```

---

## 风险提示

1. **资金安全**: 合约交易有爆仓风险, 请谨慎操作
2. **杠杆风险**: 高杠杆放大盈亏, 建议使用低杠杆
3. **止损保护**: 开仓后应立即设置止损
4. **测试优先**: 新策略先在测试网验证
5. **单笔风险**: 建议单笔亏损不超过账户 1-2%

---

## 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| -1000 | 未知错误 | 检查网络, 重试 |
| -1021 | 时间戳超出范围 | 检查系统时间同步 |
| -1022 | 签名无效 | 检查 API Secret |
| -2010 | 余额不足 | 检查可用余额 |
| -2019 | 保证金不足 | 降低仓位或增加保证金 |
| -4003 | 数量小于最小值 | 检查交易对最小交易量 |
| -4014 | 价格不符合精度 | 调整价格精度 |

---

## 技术实现

本 MCP 工具使用 [binance-futures-connector-python](https://github.com/binance/binance-futures-connector-python) 官方 SDK, 无需手动处理签名等底层细节.

### API 端点说明

**普通订单 API**:
- `GET /fapi/v1/openOrders` - 查询普通挂单
- `DELETE /fapi/v1/order` - 撤销单个普通订单
- `DELETE /fapi/v1/allOpenOrders` - 撤销所有普通订单

**条件单 Algo Order API** (2025-12-09 迁移后):
- `POST /fapi/v1/algoOrder` - 创建条件单 (止盈止损)
- `GET /fapi/v1/openAlgoOrders` - 查询条件单
- `DELETE /fapi/v1/algoOrder` - 撤销单个条件单
- **注意**: 币安没有提供批量撤销条件单的 API, `binance_cancel_all_algo_orders` 工具通过先查询再逐个撤销实现

### 开发注意事项

修改本 MCP 服务前, 应使用 Context7 查询最新 API 文档:

```
# 查询币安合约 API 文档
resolve-library-id: "binance futures connector python"
get-library-docs: context7CompatibleLibraryID="/binance/binance-futures-connector-python", topic="具体功能"
```

---

## 参考资料

- [币安 USDT-M 合约 API 文档](https://developers.binance.com/docs/zh-CN/derivatives/usds-margined-futures/general-info)
- [binance-futures-connector-python](https://github.com/binance/binance-futures-connector-python)
- Context7 Library ID: `/binance/binance-futures-connector-python`

