---
name: longbridge-consensus
description: |
  Analyst consensus snapshot for listed companies via Longbridge — current revenue / EPS / target-price consensus estimates and analyst rating distribution. For revision direction, beat/miss tracking, and PEAD signals use longbridge-earnings-revision. Triggers: "一致预期", "分析师预期", "EPS预测", "目标价", "分析师评级分布", "买入评级", "卖出评级", "一致預期", "分析師預期", "EPS預測", "目標價", "分析師評級分佈", "買入評級", "賣出評級", "analyst consensus", "EPS forecast", "target price", "analyst rating distribution", "buy sell hold", "price target consensus", "TSLA.US consensus", "700.HK analyst estimates".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: analysis
---

# longbridge-consensus

Prompt-only analysis skill. Orchestrates Longbridge CLI commands to surface analyst consensus estimates, estimate revision trends, beat/miss history, and post-earnings announcement drift (PEAD) signals.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"TSLA 分析师预期"*, *"TSLA analyst consensus"*, *"TSLA 分析師預期"*
- *"NVDA 下季度 EPS 预期"*, *"NVDA next-quarter EPS forecast"*
- *"苹果最近预期修正了吗"*, *"has AAPL had estimate revisions recently"*
- *"700.HK 目标价共识"*, *"700.HK price target consensus"*
- *"TSLA 上季超预期了吗"*, *"did TSLA beat last quarter"*, *"TSLA 上季超預期嗎"*
- *"NVDA PEAD 信号"*, *"NVDA post-earnings drift"*

For full fundamentals (revenue/margins/ROE) use `longbridge-fundamental`. For valuation use `longbridge-valuation`.

## CLI

Run `longbridge --help` to see all available subcommands, then `longbridge <subcommand> --help` before calling. Types of data needed (call concurrently):

- Coverage count, buy/hold/sell distribution, consensus target price
- Revenue / EPS estimates (high / low / mean / median)
- Forward EPS by period
- Institution rating distribution + median target price
- Rating and target price change history (for revision trend — run `--help` for available history flags)

```bash
longbridge <subcommand> TSLA.US --format json   # run --help for available flags and subcommand names
```

## Workflow

1. **Resolve symbol** to `<CODE>.<MARKET>` format.
2. **Determine scope** from the user prompt:

   | Prompt intent | Data to fetch |
   |---|---|
   | Consensus snapshot | Coverage count + buy/hold/sell + EPS estimates + forward EPS |
   | Rating distribution / target price | Institution rating distribution + median target |
   | Revision trend | Rating and target price change history |
   | Beat / miss analysis | EPS actuals vs consensus mean |
   | PEAD signal | EPS actuals + consensus + price context |

3. **In-LLM analysis**:

   | Quantity | Method |
   |---|---|
   | **Estimate revision direction** | Compare current mean EPS vs prior period from rating history; rising / flat / falling |
   | **Beat / miss** | Actual EPS vs consensus mean; beat threshold > +2% |
   | **PEAD signal** | Consecutive beats + upward revisions → positive momentum; consecutive misses + downward revisions → negative momentum. **Note**: PEAD is a statistical tendency, not a guarantee. |
   | **Surprise %** | `(Actual − Estimate) / |Estimate| × 100%` |

4. Output structured report; cite **Longbridge Securities**; end with disclaimer.

## Output template

```
{Symbol} ({code}) Analyst Consensus — Source: Longbridge Securities
As of: {date}

[Coverage & ratings]
- Analysts covering: N  |  Buy: X / Hold: Y / Sell: Z
- Median target price: {price} ({currency})  |  Upside from last: ±X%

[EPS consensus]
- Current-quarter estimate: mean {X}, range [{low} – {high}]
- Next-quarter estimate:    mean {X}, range [{low} – {high}]
- FY estimate:              mean {X}, range [{low} – {high}]

[Revenue consensus]
- Current-quarter estimate: mean {X}  YoY ±Y%
- FY estimate:              mean {X}  YoY ±Y%

[Estimate revision trend]
- Direction (past 30/90 days): {rising / flat / falling}
- Key revisions: {summary from rating/target price change history}

[Beat / miss history (last 4 quarters)]
| Quarter | Actual EPS | Estimate | Surprise % |
|---------|-----------|----------|-----------|
| {Q}     | {A}       | {E}      | {±X%}     |
...

[PEAD signal]
- Pattern: {N consecutive beats / misses / mixed}
- Revision bias: {upward / neutral / downward}
- PEAD inference: {positive momentum / neutral / negative momentum}
⚠️ PEAD is a statistical tendency, not a forecast.

⚠️ 以上数据仅供参考，不构成投资建议。/ 以上數據僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

(Omit sections where data is unavailable; state so explicitly.)

## Error handling

| Situation | 简体中文回复 | 繁體中文 / English |
|---|---|---|
| `command not found: longbridge` | 回退到 MCP；如 MCP 也不可用，请用户安装 longbridge-terminal。 | 回退到 MCP；如也不可用，請安裝 longbridge-terminal。/ Fall back to MCP; if also unavailable, tell user to install longbridge-terminal. |
| stderr `not logged in` | 请运行 `longbridge auth login` 登录。 | 請執行 `longbridge auth login`。/ Run `longbridge auth login`. |
| Consensus data has < 3 analysts | 覆盖分析师不足 3 位，一致预期仅供参考。 | 覆蓋分析師不足 3 位，僅供參考。/ Fewer than 3 analysts — consensus is indicative only. |
| Analyst estimates data returns empty | "{symbol} 暂无分析师预期数据。" | "{symbol} 暫無分析師預期。" / "{symbol} has no analyst estimates." |
| No actuals for beat/miss | 跳过超预期/低于预期分析，注明无历史实际值。 | 跳過超預期分析，注明無歷史數據。/ Skip beat/miss analysis; note no historical actuals available. |
| Other stderr | 直接显示原始错误，不静默重试。 | 顯示原始錯誤。/ Surface verbatim — do not retry silently. |

## MCP fallback

If `longbridge` CLI is not installed (`command not found`), use MCP tools:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Full fundamentals (revenue / ROE / margins) → `longbridge-fundamental`
- Valuation (PE / PB / industry) → `longbridge-valuation`
- Three-statement financials → `longbridge-financial-report`
- News & market reaction → `longbridge-news`
- Post-earnings deep-dive → `longbridge-earnings`

## File layout

```
longbridge-consensus/
└── SKILL.md   # prompt-only, no scripts/
```
