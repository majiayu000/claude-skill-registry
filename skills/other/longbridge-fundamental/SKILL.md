---
name: longbridge-fundamental
description: |
  Company fundamentals via Longbridge — latest financial report KPIs (revenue / net income / EPS / ROE / margins / cash flow), YoY trends, dividend history, forward EPS consensus, analyst ratings, corporate actions. Three depth tiers (snapshot / standard / full). Triggers: "基本面", "业绩", "财报", "财务健康", "盈利能力", "营收", "净利润", "ROE", "毛利率", "分红历史", "EPS 预期", "研报评级", "業績", "財報", "財務健康", "毛利率", "分紅歷史", "fundamentals", "financials", "earnings report", "EPS forecast", "analyst rating", "ROE", "gross margin", "free cash flow", "dividend history", "company report".
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

# longbridge-fundamental

Prompt-only analysis skill. Orchestrates Longbridge CLI commands to deliver a five-dimension fundamentals snapshot: profitability, financial health, growth, shareholder return, market expectation.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Three depth tiers

LLM picks based on prompt verbosity:

| Tier | Trigger phrases | Data needed |
|---|---|---|
| **snapshot** | *"X 怎么样"*, *"how is X"*, brief curiosity | Latest financial report KPIs + analyst estimates + consensus |
| **standard** (default) | *"X 基本面 / 业绩 / 财报"*, *"X fundamentals"* | Snapshot + full income/balance/cash-flow statements + dividend history |
| **full** | *"X 全面分析"*, *"detailed fundamentals"* | Standard + company profile + operating data + corporate actions + institution ratings (distribution, history, per-institution detail, industry rank) |

Tiers are additive — don't pull all 8+ tools when the user asks a casual question.

## When to use

- *"贵州茅台 基本面"*, *"NVDA fundamentals"* → standard
- *"NVDA 业绩好不好"*, *"how is NVDA's earnings"* → standard, but **never reduce to good/bad** — give numbers
- *"AAPL 毛利率"*, *"AAPL gross margin"* → snapshot/standard
- *"X 下季度 EPS 预期"* → snapshot is sufficient
- *"X 财务健康吗"*, *"is X financially healthy"* → standard

For valuation lens (PE, PB) → `longbridge-valuation`. For comparison → `longbridge-peer-comparison`.

## CLI

Run `longbridge --help` to see all available subcommands, then `longbridge <subcommand> --help` before calling. Types of data needed by tier:

**Snapshot tier** (run concurrently):
- Latest financial report KPIs (revenue / EPS / ROE)
- Analyst EPS estimates (high / low / mean / median)
- Coverage count, rating distribution, consensus target price

**Standard tier** — add:
- Full line-item financial statements (income statement, balance sheet, cash flow)
- Dividend history
- Forward EPS by period

**Full tier** — add:
- Company profile
- Operating metrics
- Corporate actions
- Institution rating distribution + target price
- Rating and target price change history
- Per-institution rating detail
- Industry-wide analyst coverage rank

```bash
longbridge <subcommand> NVDA.US --format json   # run --help for available flags and subcommand names
```

## Workflow

1. Resolve symbol; multi-symbol → route to `longbridge-peer-comparison`.
2. Pick a tier based on prompt; call CLI commands concurrently (see CLI section above).
3. If `longbridge` is not installed, fall back to MCP (see MCP fallback section).
4. Translate fields using the dictionary below; output the **5-section structure** with disclosure dates.
5. Cite **Longbridge Securities**; end with not-investment-advice disclaimer.

## Output template (5 sections, mandatory)

```
{Symbol} ({code}) fundamentals — Source: Longbridge Securities (period end: {fp_end / rpt_date})

[1. Profitability]
- Revenue (latest quarter): X (currency), YoY +Y%
- Net income: X, YoY +Y%
- Gross / net margin: X% / Y%
- ROE: X%

[2. Financial health]
- Debt-to-equity: X%
- Operating cash flow (TTM): X
- Free cash flow: X
- Current / quick ratio (if available)

[3. Growth]
- Revenue YoY (last 4 quarters): +X% / +Y% / +Z% / +W% — trend description
- Net income YoY (last 4 quarters): same

[4. Shareholder return]
- Last dividend date / amount
- Dividend yield: X% (if computable)
- Recent buybacks / issuance (full tier only)

[5. Market expectations (analysts)]
- Consensus next-quarter EPS: X
- Coverage: N analysts; X buy / Y hold / Z sell
- Median target price: X

⚠️ 以上数据仅供参考，不构成投资建议。/ 以上數據僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

(Translate to the user's language; if a section's data is missing, state so explicitly — do not invent.)

## Field dictionary

The full IS / BS / CF / ratio field-name dictionary (中 / 繁 / EN), plus per-industry reading guidance, lives in [references/field-dictionary.md](references/field-dictionary.md). Load it on demand when the prompt actually requires field translation or industry context.

## Output constraints

- **Must** cover all 5 sections (state missing data, do not silently skip).
- **Must** include the disclosure date (`fp_end` / `rpt_date`).
- **Must** end with the not-investment-advice disclaimer.
- **Do not** say "good earnings / bad earnings" as a binary. Anchor language in numbers (e.g. *"revenue grew 20% YoY, above the industry mean of 12%"*).
- **Do not** forecast next quarter's earnings — the analyst consensus already covers that.

## Industry-specific reading

Heuristics differ by sector. Anchor on **vs industry mean** or **vs own history**, not absolute thresholds. Concrete sector notes (banks / tech / cyclicals / asset-heavy) live in [references/field-dictionary.md](references/field-dictionary.md#industry-context).

## Error handling

| Situation | Reply |
|---|---|
| `command not found: longbridge` | Fall back to MCP; if MCP also unavailable, tell user to install longbridge-terminal. |
| Financial report data returns empty | "{symbol} has no reported earnings (newly listed?)." |
| Analyst consensus has < 3 analysts | Caveat: "small coverage — consensus is indicative only" |
| Dividend history data returns empty | "{symbol} pays no dividends or has no dividend record." |
| stderr `not logged in` | Tell user to run `longbridge auth login`. |

## MCP fallback

If `longbridge` CLI is not installed (`command not found`), use MCP tools instead:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Valuation lens (PE / PB / industry) → `longbridge-valuation`
- 2–5 symbol comparison → `longbridge-peer-comparison`
- News / market reaction → `longbridge-news`
- Live price → `longbridge-quote`

## File layout

```
longbridge-fundamental/
├── SKILL.md
└── references/
    └── field-dictionary.md   # IS/BS/CF/ratio field names + per-industry caveats
```

Prompt-only — no `scripts/`.
