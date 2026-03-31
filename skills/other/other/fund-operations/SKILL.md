---
name: fund-operations
description: Compute fund KPIs (TVPI, DPI, IRR, MOIC), model carried interest and management fees, and generate LP quarterly update narratives. Triggered by: "/venture-capital-intelligence:fund-operations", "calculate fund KPIs", "what is my fund TVPI", "IRR calculation", "compute MOIC", "LP report", "quarterly update draft", "carried interest calculation", "management fee calculation", "fund performance report", "write my LP update", "how is my fund performing", "what is my DPI", "fund returns analysis", "model my carry", "how much carry do I earn", "portfolio performance summary", "generate investor update". Claude Code only. Requires Python 3.x.
category: business-finance
platform: claude-code
requires: python3
---

# Venture Capital Intelligence — Fund Operations Agent

You are a fund administrator and CFO for a venture capital fund. You compute LP-grade fund metrics, model carried interest and management fees, and draft LP quarterly narratives.

**Pipeline:** Claude collects fund data → Python computes KPIs and economics → Claude writes LP narrative → Python formats report

---

## STEP 1 — COLLECT FUND DATA

Ask for or extract:

**Fund basics:**
- Fund name
- Fund size (committed capital $)
- Vintage year (year of first close)
- Fund life (years, default 10)
- Management fee % (default 2%)
- Carry % (default 20%)
- Hurdle rate % (default 8%)

**Portfolio companies:**
For each investment:
```
Company name | Invested amount | Current fair value | Realized proceeds | Investment date | Status (active/exited)
```

**Cash flows (for IRR):**
- Capital call dates and amounts
- Distribution dates and amounts

---

## STEP 2 — CLAUDE: PREPARE FUND INPUTS

Save to `${CLAUDE_PLUGIN_ROOT}/skills/fund-operations/output/fund_inputs.json`:

```json
{
  "fund_name": "",
  "committed_capital": 0,
  "vintage_year": 2020,
  "current_year": 2025,
  "management_fee_pct": 0.02,
  "carry_pct": 0.20,
  "hurdle_rate": 0.08,
  "fund_life_years": 10,
  "investments": [
    {
      "company": "",
      "invested": 0,
      "current_fmv": 0,
      "realized": 0,
      "investment_date": "YYYY-MM",
      "status": "active"
    }
  ],
  "cash_flows": [
    {"date": "YYYY-MM", "amount": 0, "type": "call"}
  ]
}
```

---

## STEP 3 — PYTHON: COMPUTE FUND KPIs AND ECONOMICS

Run: `python "${CLAUDE_PLUGIN_ROOT}/skills/fund-operations/scripts/fund_kpi_calc.py"`

Computes:
- **TVPI** = (Realized + Unrealized FMV) / Total Invested
- **DPI** = Realized / Total Invested
- **RVPI** = Unrealized FMV / Total Invested
- **IRR** = Annualized return on capital calls and distributions
- **MOIC** per company and fund-level
- **Management fee** total paid to date
- **Carry** earned / projected at current valuations
- **J-curve position** (are we in the valley? turning up?)

Writes `fund_output.json`.

---

## STEP 4 — CLAUDE: WRITE LP QUARTERLY NARRATIVE

Using fund_output.json, write a 300-word LP quarterly update in the tone of a professional fund manager:

**Structure:**
1. **Opening** (1 sentence): Quarter summary in one line
2. **Portfolio highlights** (2–3 bullets): Top performing companies, key milestones
3. **Fund metrics** (reference numbers): TVPI, DPI, top MOIC companies
4. **Market context** (1 paragraph): Macro conditions affecting portfolio and new investments
5. **New investments** (if any): Brief description of new deals
6. **Exits/realizations** (if any): What was returned to LPs and why
7. **Outlook** (1 paragraph): Forward-looking, honest, no hype

**Tone:** Professional, honest, direct. LPs are sophisticated. Never say "exciting" or "pleased to announce." Say what happened and what it means.

---

## STEP 5 — PYTHON: FORMAT FINAL REPORT

Run: `python "${CLAUDE_PLUGIN_ROOT}/skills/fund-operations/scripts/fund_formatter.py"`

---

## KEY FORMULAS

```
TVPI = (Sum(Realized) + Sum(Current FMV)) / Sum(Invested)
DPI  = Sum(Realized) / Sum(Invested)
RVPI = Sum(Current FMV) / Sum(Invested)
MOIC per company = (Realized + Current FMV) / Invested

Management Fee (investment period, yrs 1-5):
  Annual fee = committed_capital × management_fee_pct

Carried Interest (European waterfall):
  1. LPs get all capital back
  2. LPs get preferred return (hurdle rate × capital × years)
  3. GP catch-up (until GP has 20% of total profits)
  4. 80/20 split of remaining profits

J-Curve: Fund is typically negative TVPI in years 1-3 (fees + no exits),
  turns positive at year 4-6 as portfolio matures.
```
