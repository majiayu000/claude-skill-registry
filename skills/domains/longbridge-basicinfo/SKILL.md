---
name: longbridge-basicinfo
description: |
  Static basic information for all Longbridge-tradable securities — stocks, ETFs, options, warrants: company name, listing date, exchange, industry classification, total shares, circulating shares, market cap, IPO price, website, address. Futures / bonds / funds have limited coverage. Triggers: "基础信息", "股票信息", "上市日期", "总股本", "流通股", "IPO价格", "标的信息", "品种信息", "基礎信息", "股票資料", "上市日期", "總股本", "流通股", "IPO價格", "基本資料", "basic info", "stock info", "listing date", "shares outstanding", "IPO price", "symbol info", "static data", "security info", "exchange listing", "total shares".
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

# longbridge-basicinfo

Static basic information for Longbridge-tradable securities across all categories — stocks, ETFs, options, warrants. Returns name, listing date, exchange, industry, share structure, market cap, IPO price, website, and address.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user asks about:

- Company name / exchange / listing date — *"茅台是什么时候上市的"*, *"AAPL 在哪个交易所"*
- Share structure (total shares, circulating shares, free float) — *"NVDA 总股本多少"*
- IPO price / founding info — *"700.HK 上市价格是多少"*
- Official website or company address — *"Apple 官网"*, *"腾讯公司地址"*
- Industry classification — *"特斯拉属于什么行业"*

For live price / volume, defer to `longbridge-quote`. For executives / board / major shareholders, defer to `longbridge-corporate`.

## Workflow

1. Normalise the symbol to `<CODE>.<MARKET>` format (see symbol table below).
2. Run `longbridge static` to get share structure and listing metadata.
3. Run `longbridge company` to get company profile (name, website, address, founding date, employees).
4. Optionally run `longbridge calc-index` for market-cap derived from real-time data.
5. Merge results by `symbol` and present as a structured summary.

## Symbol format

| Pattern | Market | Example |
|---|---|---|
| Uppercase ticker | `.US` | `AAPL.US`, `NVDA.US` |
| 4-digit numeric | `.HK` | `700.HK`, `9988.HK` |
| 6-digit starts `60` | `.SH` | `600519.SH` |
| 6-digit starts `00`/`30` | `.SZ` | `300750.SZ` |
| Singapore | `.SG` | `D05.SG` |

## CLI

```bash
# Static share structure and listing info
longbridge static <SYMBOL> --format json

# Company profile (name, address, website, employees)
longbridge company <SYMBOL> --format json

# Market cap and valuation indices
longbridge calc-index <SYMBOL> --index total_market_value --format json
```

> If unsure of exact flag names, run `longbridge static --help`, `longbridge company --help`, or `longbridge calc-index --help` first — the CLI self-documents all arguments.

## Output

Merge the three JSON responses by `symbol` and present key fields:

| Field | 简体 | 繁體 | English |
|---|---|---|---|
| Company name | 公司名称 | 公司名稱 | Company name |
| Exchange | 交易所 | 交易所 | Exchange |
| Listing date | 上市日期 | 上市日期 | Listing date |
| Industry | 行业 | 行業 | Industry |
| Total shares | 总股本 | 總股本 | Total shares |
| Circulating shares | 流通股 | 流通股 | Circulating shares |
| IPO price | IPO价格 | IPO價格 | IPO price |
| Market cap | 总市值 | 總市值 | Market cap |
| Website | 官网 | 官網 | Website |
| Address | 地址 | 地址 | Address |

## Error handling

| Situation | 简体回复 | 繁體回覆 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 请先安装 longbridge-terminal | 請先安裝 longbridge-terminal | Please install longbridge-terminal first |
| `not logged in` / `unauthorized` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Please run `longbridge auth login` |
| `invalid symbol` / `param_error` | 请确认标的代码格式 `CODE.MARKET` | 請確認標的代碼格式 | Please verify symbol format `CODE.MARKET` |
| Other stderr | 原样展示错误信息，不重试 | 原樣展示錯誤，不重試 | Surface verbatim, do not retry |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

| User asks | Route to |
|---|---|
| Live price / volume | `longbridge-quote` |
| Executives / board / major shareholders | `longbridge-corporate` |
| Share structure + top-10 shareholders | `longbridge-ownership` |
| Fundamentals / financials | `longbridge-fundamental` |
| Candlestick / price history | `longbridge-kline` |

## File layout

```
longbridge-basicinfo/
└── SKILL.md
```

Prompt-only — no `scripts/`. Discover current CLI flags via `longbridge <subcommand> --help`.
