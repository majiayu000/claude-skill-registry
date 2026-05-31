---
name: longbridge-index-quote
description: |
  Major index real-time quotes via Longbridge Securities — Shanghai Composite, CSI 300, ChiNext, Hang Seng, NASDAQ, S&P 500, Dow Jones and more; supports price, change, volume, historical trend. Triggers: "上证指数", "沪深300", "创业板指", "恒生指数", "纳斯达克", "标普500", "道琼斯", "指数行情", "指数点位", "上證指數", "滬深300", "創業板指", "恒生指數", "納斯達克", "標普500", "道瓊斯", "指數行情", "Shanghai Composite", "CSI 300", "Hang Seng Index", "NASDAQ", "S&P 500", "Dow Jones", "index quote", "market index".
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

# longbridge-index-quote

Real-time and historical quotes for major global stock indices.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger on prompts asking about:

- Index level / change / volume — *"上证今天涨了多少"*, *"恒生指数现在多少点"*, *"S&P 500 today"*
- Historical index trend — *"沪深300近一个月走势"*, *"Dow Jones 6-month chart"*
- Multiple index comparison — *"美股三大指数今天表现"*, *"US indices today"*

For index constituent stocks defer to `longbridge-constituent`. For individual stock quotes defer to `longbridge-quote`.

## Index symbol reference

| Index | Symbol | 简体名称 | 繁體名稱 |
|-------|--------|---------|---------|
| Shanghai Composite | 000001.SH | 上证指数 | 上證指數 |
| CSI 300 | 000300.SH | 沪深300 | 滬深300 |
| ChiNext | 399006.SZ | 创业板指 | 創業板指 |
| CSI 500 | 000905.SH | 中证500 | 中證500 |
| Hang Seng Index | HSI.HK | 恒生指数 | 恒生指數 |
| Hang Seng Tech | HSTECH.HK | 恒生科技 | 恒生科技 |
| NASDAQ Composite | .IXIC.US | 纳斯达克综合 | 納斯達克綜合 |
| S&P 500 | .SPX.US | 标普500 | 標普500 |
| Dow Jones | .DJI.US | 道琼斯 | 道瓊斯 |
| Russell 2000 | .RUT.US | 罗素2000 | 羅素2000 |
| VIX | .VIX.US | 恐慌指数 | 恐慌指數 |
| Nikkei 225 | NI225.JP | 日经225 | 日經225 |

> If unsure of exact flag names, run `longbridge <subcommand> --help` before proceeding.

## Workflow

1. Map the user's plain-language index name to the correct symbol using the table above.
2. If multiple indices are mentioned, query all of them.
3. Fetch real-time quote.
4. If historical trend is requested, fetch daily OHLCV.
5. Present results as a clean table; add brief market context if notable moves are present.

## CLI

```bash
# Real-time index quote
longbridge quote <INDEX_SYMBOL> --format json

# Historical daily OHLCV
longbridge kline <INDEX_SYMBOL> --period day --count 60 --format json

# Intraday minute chart (today)
longbridge kline <INDEX_SYMBOL> --period minute --format json
```

## Output

For a single index:

```
上证指数 (000001.SH)
现价：3,312.45    涨跌：+0.82%    成交额：3,240亿
今日高：3,318.02  今日低：3,288.11  昨收：3,285.57
```

For multiple indices: a comparison table sorted by today's change.

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|-----------|---------|---------|---------------|
| Index symbol not found | 未找到该指数，请参考指数代码表（如 HSI.HK）。 | 找不到該指數，請參考指數代碼表（如 HSI.HK）。 | Index not found — check the symbol table (e.g. HSI.HK). |
| Market closed | 市场已收盘，显示最新收盘数据。 | 市場已收盤，顯示最新收盤數據。 | Market closed — showing latest close data. |
| `command not found: longbridge` | 请安装 longbridge-terminal 或通过 MCP 连接。 | 請安裝 longbridge-terminal 或透過 MCP 連線。 | Install longbridge-terminal or connect via MCP. |
| `not logged in` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-constituent` — index constituent stocks and rankings
- `longbridge-quote` — individual stock quotes
- `longbridge-market-temp` — market temperature and session times
- `longbridge-kline` — candlestick / OHLCV detail

## File layout

```
skills/longbridge-index-quote/
└── SKILL.md
```
