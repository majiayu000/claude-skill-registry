---
name: longbridge-onchain
description: |
  On-chain data analysis framework — covers active addresses, whale behaviour, TVL (total value locked), DEX liquidity, and on-chain valuation metrics: MVRV (market cap / realised value), NVT (network value / transaction volume), SOPR. Longbridge provides spot crypto quotes (.HAS); raw on-chain data requires external sources (Glassnode / Dune Analytics). Triggers: "链上数据", "链上分析", "MVRV", "NVT", "活跃地址", "鲸鱼地址", "TVL", "SOPR", "链上指标", "链上估值", "鏈上數據", "鏈上分析", "活躍地址", "鯨魚地址", "鏈上指標", "鏈上估值", "on-chain data", "on-chain analysis", "MVRV ratio", "NVT ratio", "active addresses", "whale activity", "TVL", "SOPR", "on-chain valuation", "DeFi TVL", "crypto on-chain".
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

# longbridge-onchain

On-chain data analysis framework — MVRV, NVT, SOPR, whale behaviour, TVL, and DEX liquidity.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger on prompts asking for:

- On-chain valuation — *"MVRV 是多少"*, *"BTC MVRV ratio"*, *"NVT 指标"*
- Whale or address activity — *"鲸鱼地址动向"*, *"whale activity"*, *"active addresses"*
- DeFi / TVL — *"以太坊 TVL"*, *"DeFi TVL"*, *"链上流动性"*
- On-chain sentiment — *"SOPR"*, *"链上持仓盈亏"*, *"on-chain profit/loss"*

> **Data scope**: Longbridge CLI provides **spot crypto price and price history** only. On-chain raw data (address activity, TVL, whale transfers) is not available via the Longbridge CLI — the user must supply external data (Glassnode, Dune Analytics, Nansen, etc.) or paste it directly. This skill interprets and synthesises that data.

## Workflow

1. Fetch crypto spot quote and recent price history from Longbridge.
2. Ask the user to provide on-chain data, or guide them to a public source:
   - Glassnode: MVRV, NVT, SOPR, active addresses
   - Dune Analytics: DEX volume, TVL by protocol
   - Nansen: whale wallet labels and flows
   - DefiLlama: cross-chain TVL
3. Interpret the metrics using standard thresholds:
   - MVRV > 3.0 → historically overheated; < 1.0 → historically undervalued
   - NVT > 90th percentile → overvalued relative to transaction throughput
   - SOPR > 1 → holders selling at profit (potential distribution)
   - SOPR < 1 → holders selling at loss (potential capitulation)
4. Synthesise a verdict: Undervalued / Fair Value / Overheated / Distribution Zone.
5. Cross-reference with price trend from Longbridge kline data.

> If unsure of exact flag names, run `longbridge <subcommand> --help` before proceeding.

## CLI

```bash
# Crypto spot quote
longbridge quote BTCUSD.HAS --format json

# Recent daily price trend (ETH example); run --help for period/count flags
longbridge kline ETHUSD.HAS --format json   # run --help for available flags
```

Supported crypto symbols use the `.HAS` suffix (e.g. `BTCUSD.HAS`, `ETHUSD.HAS`, `SOLUSD.HAS`).

## Output structure

```
ON-CHAIN ANALYSIS — <TOKEN>  <Date>

PRICE CONTEXT (Longbridge)
Current: $xx,xxx   7d: +x.x%   30d: +x.x%
90d Range: $xx,xxx – $xx,xxx

ON-CHAIN METRICS (from <source>)
MVRV:   x.xx  → [Undervalued | Fair | Overheated]
NVT:    xxx   → [Low | Normal | High]
SOPR:   x.xxx → [Accumulation | Neutral | Distribution]
Active Addresses (7d avg): xxx,xxx

DEFI / TVL (if provided)
Total TVL: $xxB   7d change: +x.x%
Top Protocol: <Name>  $xxB

VERDICT
<2–3 sentence synthesis combining price trend and on-chain signals>
Signal: [Bullish | Neutral | Bearish | Cautious]

DATA SOURCES
Price: Longbridge Securities
On-chain: <Glassnode | Dune | User-supplied>
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|-----------|---------|---------|---------------|
| Crypto symbol not found | 请使用 .HAS 后缀格式，如 BTCUSD.HAS。 | 請使用 .HAS 後綴格式，如 BTCUSD.HAS。 | Use the .HAS suffix format, e.g. BTCUSD.HAS. |
| No on-chain data provided | 链上原始数据请从 Glassnode 或 Dune 获取后提供给我。 | 鏈上原始數據請從 Glassnode 或 Dune 取得後提供給我。 | Please provide on-chain data from Glassnode or Dune Analytics. |
| `command not found: longbridge` | 请安装 longbridge-terminal 或通过 MCP 连接。 | 請安裝 longbridge-terminal 或透過 MCP 連線。 | Install longbridge-terminal or connect via MCP. |
| `not logged in` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-quote` — crypto spot price and market data
- `longbridge-kline` — price history and intraday chart
- `longbridge-capital-flow` — on-platform capital flow signals
- `longbridge-valuation` — traditional equity valuation metrics

## File layout

```
skills/longbridge-onchain/
└── SKILL.md
```
