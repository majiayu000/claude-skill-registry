---
name: coinank-data-analysis
description: 使用 Coinank MCP 工具进行加密货币衍生品市场分析
---

# Coinank 数据分析

Coinank MCP 提供加密货币衍生品市场的专业数据接口.

## 数据类型

| 类别 | 工具 | 用途 |
|------|------|------|
| 价格数据 | `get_last_price`, `get_klines` | 实时价格、K线 |
| 持仓数据 | `get_open_interest_kline`, `get_open_interest_rank` | 持仓量变化 |
| 资金数据 | `get_realtime_fund_flow`, `get_funding_rate_kline` | 资金流向、费率 |
| 买卖力量 | `get_cvd_kline`, `get_aggregated_cvd` | CVD 累积成交量差 |
| 情绪指标 | `get_long_short_ratio`, `get_rsi_map` | 多空比、RSI |
| 大单监控 | `get_large_market_orders`, `get_large_limit_orders` | 大额订单 |
| 排行榜 | `get_price_rank`, `get_volume_rank` | 涨跌幅、交易量排名 |

## 核心概念

- **CVD**: 买卖力量差, 正值=买方强, 负值=卖方强
- **资金流向**: 净流入/流出, 正值=流入, 负值=流出
- **持仓量**: 增加=新仓开立, 减少=平仓
- **资金费率**: 正=多头付费, 负=空头付费
- **多空比**: >1 多头人数多, <1 空头人数多

## 使用场景

1. **选币**: RSI 筛选超买超卖 + 资金流向确认
2. **分析**: 价格 + 持仓 + CVD + 资金流 综合判断
3. **监控**: 大单追踪主力动向
4. **排行**: 发现热门币种

## 代码参考

具体工具参数和实现细节, 查看源码:

```
mcps/coinank.py
```
