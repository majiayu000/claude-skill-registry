---
name: longbridge-sector-screener
description: |
  Sector screening and ranking — filter and rank A-share / HK / US industry sectors by valuation (PE/PB), capital inflow, price performance (1d/5d/20d), and turnover rate. Outputs a sector leaderboard. Triggers: "板块筛选", "行业筛选", "强势板块", "弱势板块", "板块排行", "行业排名", "资金流入板块", "涨幅最大板块", "板塊篩選", "行業篩選", "強勢板塊", "弱勢板塊", "板塊排行", "行業排名", "sector screener", "sector filter", "sector ranking", "top sectors", "hot sectors", "capital inflow sectors", "sector scan", "industry ranking", "sector performance", "best sectors today".
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

# longbridge-sector-screener

Sector screening and ranking — filter and rank industry sectors across A-share / HK / US markets by valuation (PE/PB), capital inflow, price performance (1d/5d/20d), and turnover rate. Outputs a ranked sector leaderboard.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user asks about:

- Top or bottom performing sectors — *"今天哪个行业涨得最多"*, *"最强势板块"*, *"best performing sectors today"*
- Sector capital flow ranking — *"哪些板块在吸资金"*, *"sectors with net capital inflow"*
- Sector valuation screening — *"哪些行业PE最低"*, *"low-PE sectors"*
- Broad sector overview — *"美股各行业今天表现"*, *"A股行业板块排名"*

For individual stock anomalies, prefer `longbridge-anomaly`. For a single stock's capital flow, prefer `longbridge-capital-flow`. For index constituents, prefer `longbridge-constituent`.

## Workflow

1. Identify the target market (A-share / HK / US) from the prompt.
2. Select representative sector ETFs or indices for that market:
   - **A-share**: major CSI sector indices (e.g. CSI Banks, CSI Tech, CSI Consumer)
   - **HK**: Hang Seng sector sub-indices or sector ETFs
   - **US**: SPDR sector ETFs (XLK, XLF, XLE, XLV, XLI, XLY, XLP, XLU, XLRE, XLB, XLC)
3. Run `longbridge quote` on each sector proxy to get 1d / 5d / 20d performance and turnover rate.
4. Run `longbridge capital` on each sector proxy for net capital inflow.
5. Run `longbridge calc-index` for PE and PB of each sector proxy.
6. Sort and rank by the user's requested criterion; present as a leaderboard table.

## CLI

```bash
# Sector proxy quote (price change, turnover rate)
longbridge quote <SECTOR_SYMBOL> --format json

# Sector capital flow
longbridge capital <SECTOR_SYMBOL> --format json

# Sector valuation
longbridge calc-index <SECTOR_SYMBOL> --index pe_ttm,pb --format json

# Constituent list of a sector index (if drilling into members)
longbridge constituent <INDEX> --format json
```

> Run `longbridge quote --help`, `longbridge capital --help`, and `longbridge calc-index --help` to verify flags.

## Output

A ranked leaderboard table:

| Rank | Sector | 简体 | 繁體 | English |
|---|---|---|---|---|
| 1d change | 今日涨跌幅 | 今日漲跌幅 | 1d change |
| 5d change | 近5日涨跌幅 | 近5日漲跌幅 | 5d change |
| Net capital inflow | 净流入 | 淨流入 | Net inflow |
| PE | 市盈率 | 市盈率 | PE |
| PB | 市净率 | 市淨率 | PB |
| Turnover rate | 换手率 | 換手率 | Turnover rate |

Note: Sector coverage depends on available representative ETFs/indices in Longbridge. Full market-wide sector screening (like Wind or 同花顺) is not supported — the LLM must manually iterate over a curated set of sector proxies.

## Error handling

| Situation | 简体回复 | 繁體回覆 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 请先安装 longbridge-terminal | 請先安裝 longbridge-terminal | Install longbridge-terminal first |
| `not logged in` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| Sector proxy not found | 提示该板块代理标的无数据 | 提示該板塊代理標的無數據 | Sector proxy symbol not found |
| Other stderr | 原样展示，不重试 | 原樣展示，不重試 | Surface verbatim, do not retry |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

| User asks | Route to |
|---|---|
| Individual stock anomalies | `longbridge-anomaly` |
| Single stock capital flow | `longbridge-capital-flow` |
| Index constituents | `longbridge-constituent` |
| Market temperature / overall sentiment | `longbridge-market-temp` |
| Multi-stock comparison | `longbridge-peer-comparison` |

## File layout

```
longbridge-sector-screener/
└── SKILL.md
```

Prompt-only — no `scripts/`. Sector proxies are selected in-context based on market and user request. Discover current CLI flags via `longbridge <subcommand> --help`.
