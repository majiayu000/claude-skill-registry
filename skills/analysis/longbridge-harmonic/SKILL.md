---
name: longbridge-harmonic
description: |
  谐波形态信号引擎——基于斐波那契几何识别 XABCD 五点结构，支持 Gartley、Bat（蝙蝠）、Butterfly（蝴蝶）、Crab（螃蟹），在潜在反转区（PRZ）生成交易信号。Triggers: "谐波形态", "谐波", "Gartley", "蝙蝠形态", "蝴蝶形态", "螃蟹形态", "XABCD", "潜在反转区", "PRZ", "斐波那契形态", "諧波形態", "諧波", "蝙蝠形態", "蝴蝶形態", "螃蟹形態", "harmonic pattern", "Gartley pattern", "Bat pattern", "Butterfly pattern", "Crab pattern", "PRZ", "potential reversal zone", "fibonacci harmonic".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: read
---

# longbridge-harmonic

谐波形态信号引擎：基于斐波那契几何关系识别 XABCD 五点结构，支持 Gartley、Bat（蝙蝠）、Butterfly（蝴蝶）、Crab（螃蟹）四种经典形态，在潜在反转区（PRZ）生成多/空方向交易信号。

> **Response language**: match the user's input language —
> Simplified Chinese / Traditional Chinese / English.

## When to use

- 用户询问谐波形态：*"AAPL 有没有 Gartley 形态"*、*"700.HK 蝙蝠形态分析"*、*"TSLA PRZ 在哪里"*
- 检测 XABCD 结构是否满足特定谐波形态的斐波那契比率
- 判断潜在反转区（PRZ）位置，辅助入场决策
- 用户提到"蝴蝶形态"、"螃蟹形态"、"XABCD"等关键词

## Workflow

1. 提取标的代码，标准化为 `<CODE>.<MARKET>` 格式。
2. 获取日线 OHLCV 数据（200 根 K 线）：
   ```bash
   longbridge kline <SYMBOL> --period day --format json   # run --help for available flags
   ```
3. **Zigzag 识别摆动点**（threshold 默认 5%），取最近 5 个有效摆动点作为 X-A-B-C-D 候选。
4. **计算各段斐波那契比率**：
   - `AB/XA`：AB 相对于 XA 的回撤比
   - `BC/AB`：BC 相对于 AB 的回撤比
   - `CD/BC`：CD 相对于 BC 的延伸比
   - `AD/XA`：AD 相对于 XA 的整体比（PRZ 核心）
5. **与四种标准谐波容差（±5%）比较**：

   | 形态 | AB/XA | BC/AB | CD/BC | AD/XA |
   |---|---|---|---|---|
   | Gartley | 0.618 | 0.382–0.886 | 1.272–1.618 | 0.786 |
   | Bat | 0.382–0.500 | 0.382–0.886 | 1.618–2.618 | 0.886 |
   | Butterfly | 0.786 | 0.382–0.886 | 1.618–2.618 | 1.272–1.618 |
   | Crab | 0.382–0.618 | 0.382–0.886 | 2.618–3.618 | 1.618 |

6. 匹配成功则计算 PRZ 区间（D 点目标范围），判断看多（看涨 XABCD）或看空（看跌 XABCD）方向。
7. 输出形态名称、PRZ 范围、方向、止损位。

> 若不确定 CLI 参数，先运行 `longbridge kline --help` 查看最新参数。

## CLI

```bash
# 日线数据（主要数据源）
longbridge kline AAPL.US --period day --format json   # run --help for available flags

# 4 小时线（辅助确认短周期形态，可选）
longbridge kline TSLA.US --period 60m --format json
```

## Output

以自然语言呈现，包含：

- **识别到的形态**：如 "Bullish Gartley（看涨 Gartley）"、"Bearish Bat（看跌蝙蝠）"
- **XABCD 各点价格和日期**
- **PRZ 区间**：[PRZ 低点, PRZ 高点]（D 点潜在落点范围）
- **交易方向**：看多（Bullish）/ 看空（Bearish）
- **止损位**：突破 X 点则形态失效
- **斐波那契比率符合度**（各比率实际值 vs 标准值）
- **数据来源**：Longbridge Securities / 数据来源：长桥证券 / 數據來源：長橋證券

## Error handling

| 情形 | LLM 回复 |
|---|---|
| `command not found: longbridge` | 尝试 MCP fallback；否则告知用户安装 longbridge-terminal |
| stderr 含 `not logged in` | 告知用户运行 `longbridge auth login` |
| Zigzag 摆动点不足（少于 5 个） | 建议切换更长周期（如周线），运行 `longbridge kline --help` 查看可用参数 |
| 无法匹配任何谐波形态 | 告知"当前未检测到满足标准谐波比率的 XABCD 结构" |
| 其他 stderr | 原样透传，不静默重试 |

## MCP fallback

若 CLI 不可用且已配置 MCP：

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

| 用户询问 | 路由至 |
|---|---|
| 实时股价/行情 | `longbridge-quote` |
| K线图/历史价格 | `longbridge-kline` |
| 缠论分型/买卖点 | `longbridge-chanlun` |
| 艾略特波浪 | `longbridge-elliott` |
| 聪明钱/SMC | `longbridge-smc` |
| 资金流向 | `longbridge-capital-flow` |

## File layout

```
longbridge-harmonic/
└── SKILL.md
```
