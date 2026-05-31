---
name: longbridge-regulatory-kb
description: |
  Financial regulatory knowledge base — A-shares (10% / 5% ST price limits, T+1 settlement, short-selling rules, new delisting rules), HK (T+0 short-selling, no price limits, odd-lot / grey market, profit test, insider dealing ordinance), US (PDT rule $25k threshold, Reg T margin, circuit breakers, SEC rules), crypto regulation, cross-border tax basics. Triggers: "监管规则", "涨跌停", "T+1", "融券", "退市", "做空规则", "PDT规则", "熔断", "保证金", "印花税", "監管規則", "漲跌停", "融券", "退市", "做空規則", "PDT規則", "熔斷", "保證金", "印花稅", "regulatory rules", "circuit breaker", "short selling rules", "PDT rule", "margin requirements", "stamp duty", "delisting rules", "trading rules", "settlement rules".
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

# longbridge-regulatory-kb

A structured regulatory knowledge base covering the rules, restrictions, and mechanisms investors face across A-shares, Hong Kong, US equity markets, and cryptocurrency — answers regulatory questions without needing live data lookups.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"A 股涨跌停规则是什么"*, *"what are A-share price limits"*, *"A 股漲跌停規則"*
- *"T+1 是什么意思"*, *"what is T+1 settlement"*
- *"港股可以 T+0 吗"*, *"can I sell HK stocks on the same day I buy"*
- *"PDT 规则是什么"*, *"explain the PDT rule"*
- *"美股熔断机制怎么触发"*, *"US circuit breaker trigger levels"*
- *"A 股退市新规"*, *"new A-share delisting rules"*
- *"港股碎股和暗盘怎么交易"*, *"odd-lot and grey market in HK"*

For live trading session status, supplement with `longbridge market-temp`. For symbol-specific rules, use `longbridge static <SYMBOL> --format json`.

## A-Share Rules (A股规则)

### Price limits (涨跌停)

| Board | Normal stocks | ST / *ST stocks |
|---|---|---|
| Shanghai / Shenzhen Main Board | ±10% | ±5% |
| STAR Market (科创板) | ±20% (first 5 days: ±30%) | N/A |
| ChiNext (创业板) | ±20% (first 5 days: ±30%) | N/A |
| Beijing Stock Exchange | ±30% | ±30% |

New listings: first day no limit; days 2–5 follow the limits above.

### Settlement (交收)

- **T+1**: Sell a stock on the day after purchase. Funds from sales available next day.
- **T+0**: Not permitted for equities (day trading is prohibited for ordinary investors).
- ETFs and convertible bonds: T+0 selling is allowed.

### Short selling (融券做空)

- Available only via margin accounts through approved brokers.
- Securities in the approved short-list only (maintained by exchanges).
- No naked short selling — must borrow first.
- Transfer fee: typically 0.05–0.10% daily.

### Circuit breakers (熔断)

- Triggered when CSI 300 falls ≥5% (15-min halt) or ≥7% (market close for the day).
- Note: implemented 2016-01-04, suspended 2016-01-08 due to market disruption.

### Delisting rules (退市新规, 2024)

- **Financial**: Net profit < 0 AND revenue < 100M RMB for 2 consecutive years → risk warning; 3 years → delisting.
- **Market cap**: < 300M RMB for 20 consecutive trading days → delisting warning.
- **Turnover**: < 2M RMB for 20 consecutive days → delisting warning.
- ST / *ST designation: 1 year of losses → ST; 2 consecutive → *ST; further violations → delisting review.

### Stamp duty (印花税)

- 0.1% on sell side only (halved from 0.1% on both sides effective Aug 2023).

## HK Stock Rules (港股规则)

### Price limits

- **No daily price limits** on the Hong Kong Stock Exchange.
- Extreme volatility may trigger Volatility Control Mechanism (VCM): 5-minute cooling-off if price moves ±10% in 5 minutes.

### Settlement (交收)

- **T+2**: Standard settlement. Sell on day T; proceeds settled T+2.
- **T+0 selling**: Allowed — you can sell shares purchased today if settled (e.g. shares transferred to your account already, which typically requires prior holding).

### Short selling (卖空)

- **Designated short-selling stocks only** — SEHK publishes the list.
- No naked short selling — must borrow.
- Short positions must be marked as "short" at order entry.

### Odd-lot trading (碎股)

- Board lot = standard trading unit (varies by stock: 100, 200, 500, 1000, 2000 shares, etc.).
- Odd lots (less than one board lot) trade in the odd-lot market at wider spreads.
- Retail investors often receive odd lots from rights issues or stock dividends.

### Grey market / dark pool (暗盘)

- Pre-IPO grey market: unofficial OTC trading in IPO shares before listing, typically evening before listing day.
- Provides price discovery but is not regulated by SEHK; settlement risk exists.

### Listing criteria / delisting (上市/退市)

- **Profit test**: Aggregate profit ≥ HK$50M over 3 years (main board). Alternative: market cap test or revenue test.
- **Delisting**: Prolonged trading suspension (typically > 18 months) triggers delisting review.

### Stamp duty (印花税)

- 0.1% on both buyer and seller (total 0.2% per round trip), effective from 2021.

### Insider dealing (内幕交易条例)

- Securities and Futures Ordinance (SFO) Cap. 571 governs insider dealing and market manipulation.
- Directors must disclose dealings within 3 business days.

## US Stock Rules (美股规则)

Key rules: PDT ($25k minimum, 4 day-trades in 5-day window), Reg T 50% initial margin, T+1 settlement (since May 2024), S&P 500 circuit breakers at -7%/-13%/-20%, Reg SHO short-locate requirement, LULD per-stock bands ±5%.

For full detail see [`references/us-rules.md`](references/us-rules.md).
For cryptocurrency regulation and cross-border tax basics see [`references/crypto-and-tax.md`](references/crypto-and-tax.md).

## CLI (supplementary)

For live trading session status:
```bash
longbridge market-temp --format json   # session open/closed, market sentiment
```

For symbol-specific board lot or margin tier:
```bash
longbridge static <SYMBOL> --format json   # verify available fields with --help
longbridge static --help
```

## Output

For each regulatory question:
1. Clear rule statement with the governing authority.
2. Numeric thresholds (%, days, amounts).
3. Consequences of violation / breach.
4. Practical tip for the user.
5. Caveat: rules evolve; link to official source when possible (CSRC / SFC / SEC / FINRA).

## Error handling

| Situation | 简体回复 | 繁體回覆 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 监管知识库无需 CLI。如需实时交易状态，请安装 longbridge-terminal。 | 監管知識庫無需 CLI。如需實時交易狀態，請安裝 longbridge-terminal。 | Regulatory KB needs no CLI. For live session status, install longbridge-terminal. |
| Rule not covered | 该规则暂未收录，建议查阅 CSRC/SFC/SEC 官网。 | 該規則暫未收錄，建議查閱 CSRC/SFC/SEC 官網。 | Rule not yet covered; consult CSRC / SFC / SEC official website. |
| User asks for specific account advice | 请咨询持牌财务顾问，本技能仅提供通用规则说明。 | 請諮詢持牌財務顧問，本技能僅提供通用規則說明。 | Consult a licensed financial adviser; this skill provides general rules only. |

## Related skills

- `longbridge-market-temp` — live trading session and sentiment
- `longbridge-flows` — short interest and insider trade data (US)
- `longbridge-derivatives` — options margin and exercise rules
- `longbridge-hedging` — hedging strategy design

## File layout

```
skills/longbridge-regulatory-kb/
└── SKILL.md
```
