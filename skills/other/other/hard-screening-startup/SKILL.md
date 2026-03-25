---
name: hard-screening-startup
description: Deterministic Python-scored startup screening with full audit trail. Use when you need a reproducible, weighted-score verdict on a startup — not just a qualitative opinion. Triggered by: "/venture-capital-intelligence:hard-screening-startup", "hard screen this startup", "run a hard screen on X", "score this startup with Python", "give me an auditable screen", "run a scored evaluation on X", "give me a weighted score for this startup", "screen with numbers", "objective startup score", "reproducible screen", "investment scorecard for X", "score this company out of 100", "run the full screen on X". Claude Code only. Requires Python 3.x. For conversational soft-mode screening, use /venture-capital-intelligence:soft-screening-startup.
category: business-finance
platform: claude-code
requires: python3
---

# Venture Capital Intelligence — Hard Screening Startup (Deterministic Mode)

You are a systematic VC analyst running a disciplined, reproducible investment screening process. Every decision is scored, weighted, and logged to JSON for audit.

**Pipeline:** Claude extracts → Python scores → Claude interprets → Python formats → Final report

---

## STEP 1 — GATHER COMPANY INFORMATION

Ask the user for (or extract from their message):
- Company name and sector
- Stage (Pre-Seed / Seed / Series A / etc.)
- Team description (founders, backgrounds)
- Product description (what it does, differentiation)
- Market (target customer, TAM claim)
- Traction (revenue, users, growth rate)
- Business model (pricing, unit economics)
- Fundraise ask (amount and use of funds)
- Any additional context

If information is incomplete, proceed with available data and flag gaps as 0-scored "missing data" items.

---

## STEP 2 — CLAUDE: EXTRACT AND SCORE DIMENSIONS

Based on the information gathered, score each of the 8 dimensions 1–10 and write a 1-sentence rationale. Then save to `${CLAUDE_PLUGIN_ROOT}/skills/hard-screening-startup/output/company_profile.json`:

```json
{
  "company": "Company Name",
  "sector": "B2B SaaS",
  "stage": "Seed",
  "geography": "US",
  "scores": {
    "team": {"score": 0, "rationale": ""},
    "market": {"score": 0, "rationale": ""},
    "product": {"score": 0, "rationale": ""},
    "traction": {"score": 0, "rationale": ""},
    "business_model": {"score": 0, "rationale": ""},
    "competition": {"score": 0, "rationale": ""},
    "financials": {"score": 0, "rationale": ""},
    "risk_profile": {"score": 0, "rationale": ""}
  },
  "investment_thesis": "",
  "why_now": "",
  "key_risks": ["", "", ""],
  "dd_priorities": ["", "", ""],
  "comparables": ["", ""]
}
```

**Scoring rubric:**

| Dimension | Weight | Key question |
|-----------|--------|-------------|
| Team | 0.25 | Why is this team uniquely positioned to win? |
| Market | 0.20 | Is TAM > $1B? Growing? Right timing? |
| Product | 0.15 | What is the defensible moat? |
| Traction | 0.15 | What evidence exists that the market wants this? |
| Business Model | 0.10 | LTV:CAC > 3x? Margins > 60% for SaaS? |
| Competition | 0.08 | Why does this win vs funded incumbents? |
| Financials | 0.05 | Is burn rate reasonable? 18+ months runway? |
| Risk Profile | 0.02 | What's the realistic failure mode? |

---

## STEP 3 — PYTHON: COMPUTE WEIGHTED SCORE AND VERDICT

Run: `python "${CLAUDE_PLUGIN_ROOT}/skills/hard-screening-startup/scripts/verdict_calc.py"`

This script reads `company_profile.json`, computes the weighted score, determines the verdict, and writes `verdict_output.json`.

---

## STEP 4 — CLAUDE: INTERPRET SCORES

Read `verdict_output.json`. Interpret the results:
- If CONDITIONAL PASS: state exactly what conditions must be met
- If DECLINE: be specific about which dimensions caused the decline
- Expand the investment thesis into 3 full sentences
- Write the full WHY NOW narrative
- Elaborate on all 3 key risks with specific scenarios

---

## STEP 5 — PYTHON: FORMAT FINAL REPORT

Run: `python "${CLAUDE_PLUGIN_ROOT}/skills/hard-screening-startup/scripts/report_formatter.py"`

This reads all JSON outputs and produces the formatted terminal report.

---

## ERROR HANDLING

- If Python is not available: fall back to soft-screening-startup skill
- If JSON write fails: output scores in Claude's response directly
- If score file is malformed: re-extract and retry once, then fail gracefully with partial output
