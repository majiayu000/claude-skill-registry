---
name: aws-cost-estimate
description: Generate AWS cost estimates from architecture documents. Use when the user needs to estimate monthly/annual costs for an AWS architecture.
argument-hint: "[doc-path] [--lang en|ja] [--currency usd|jpy]"
user-invocable: true
---

# AWS Cost Estimate Skill

Generate accurate AWS cost estimates from architecture documents or descriptions.

## Arguments

- `doc-path`: Path to architecture document (markdown, text) or inline description
- `--lang`: Output language. `ja` (default) or `en`
- `--currency`: `usd` (default) or `jpy`. When `jpy`, ask the user for the exchange rate to use

## Workflow

### 1. Parse the architecture

Read the provided document. Extract:

- AWS services used and their configuration
- Data flow patterns (for data transfer estimates)
- Scale assumptions (users, queries/day, data volume)

If anything critical is ambiguous, ask using AskUserQuestion. Keep clarification minimal — only ask what materially affects the estimate.

### 2. Verify pricing — AWS CLI first, web search fallback

**CRITICAL: Always verify current prices. Never rely on training data.**

1. Silently check if AWS CLI is available and authenticated (see `references/aws-pricing-api.md`)
2. **If available** → use AWS Price List API for exact regional pricing. Read `references/aws-pricing-api.md` for service codes, example queries, and JSON parsing
3. **If unavailable** → fall back to web search: `"AWS [service] pricing [region] [current year]"`. Use WebFetch on official pricing pages if results are insufficient

For required permissions, see `references/permissions.md`.

### 3. Calculate and output the report

Output a clean cost report. No greetings, no sign-offs — just the report.

**Structure:**

```
## Assumptions
- Region, scale, availability config
- Exchange rate (if currency is JPY)
- Services using existing infrastructure (noted as $0 with explanation)

## Monthly Cost Breakdown

**[Service name] ([config])**
- Cost: $XX.XX/month
- Calculation: [unit price] × [usage]
- Source: [pricing page URL]

(repeat for each service)

## Monthly Total: $XXX〜$XXX

## Scaling Options
(How cost changes at different tiers, e.g., 1→2→4 OCU)

## Initial Costs
- AWS service fees: none for listed services
- Development effort: [key build tasks]

## Caveats
- Unverified regional prices, assumptions, limitations
```

Use the user's `--lang` for all section headers and descriptions.

### 4. Offer AWS Pricing Calculator link (optional)

After outputting the report, ask the user:

> "AWS Pricing Calculatorの共有リンクを作成しますか？（Playwrightブラウザ操作が必要です）"
> (or in English: "Would you like me to generate a shareable AWS Pricing Calculator link? (Requires Playwright browser automation)")

If yes, read `references/calculator-automation.md` for the full Playwright workflow, known limitations, and service-specific tips.

## Rules

1. **Always verify prices** — use AWS Price List API (preferred) or web search. Never use memorized prices
2. **Show the math** — unit price × usage for each line item
3. **Cite sources** — pricing page URL for every service
4. **No greetings or sign-offs** — output is a raw report, not a message
5. **Be honest about uncertainty** — flag when using US prices with regional estimates
6. **Flag cost drivers** — clearly call out which service dominates the total
7. **Don't editorialize costs** — present numbers neutrally, don't say "small" or "large"
8. **Include existing infra** — if user says a service is already running, show it at $0 with a note

## Common pitfalls to verify

- **OpenSearch Serverless**: min OCU varies (1 without redundancy, 4 with). Actual billing supports 0.5 OCU increments
- **S3 endpoints**: Gateway Endpoint = FREE, Interface Endpoint = PAID
- **Bedrock**: separate charges for embedding (Titan) vs generation (Claude) — very different price points
- **Transit Gateway**: hourly per-attachment + per-GB data processing
- **VPC Endpoints**: per-AZ pricing — confirm how many AZs
- **EC2 Tokyo**: typically higher than US East — verify exact regional rate
