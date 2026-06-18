---
name: win-loss-analysis
version: '1.0'
last_updated: 2026-06-17
author: genesys-growth
description: Analyze sales-call transcripts to extract why deals are won and lost across six dimensions — product, messaging, GTM/sales, pricing, competition, and customer context. Produces aggregated patterns with verbatim buyer quotes, frequencies, and recommendations. Writes to marketing/win-loss/win-loss.md as the evidence base under positioning, messaging, and ICP. Triggers - "win loss analysis", "why are we losing deals", "why do we win", "analyze sales calls", "churn analysis", "deal review"
goal: Turn raw sales-call transcripts into a pattern-level account of why deals close — and why they don't — in the buyer's own words.
outcome: marketing/win-loss/win-loss.md with win/loss patterns by dimension, verbatim quotes, frequencies, and marketing-handoff recommendations.
primitive: research
ontology_type: win-loss-analysis
review_gate: 1
inputs:
  required: []
  recommended:
    - icp-research
outputs:
  - type: win-loss-analysis
    feeds_into:
      - positioning
      - product-messaging
      - icp-research
owned_by_agent: researcher
mcps_used:
  - granola
triggers:
  slash_commands:
    - /win-loss-analysis
status: draft
---

# win-loss-analysis — Day 4 research skill

The Example 1 Day 4 skill. Reads your won + lost sales-call transcripts and writes a pattern-level analysis to `marketing/win-loss/win-loss.md`. This is the evidence base under positioning, messaging, and ICP — every claim in those docs should trace back to something a real buyer said here.

---

## When to use

- Day 4 of Example 1: before `/icp-research` + `/positioning`, so the strategy reads from real buyer language
- You have a fresh batch of 5+ won/lost call transcripts
- A quarter closes and you want to refresh why deals moved
- Churn spikes and you need the pattern, not the anecdote

## When NOT to use

- For a single account's interview prep (use `/customer-interviews` — not in V2 quickstart)
- For behavioural simulation of a buyer (use `/icp-behavioural` — not in V2 quickstart)
- When you have fewer than ~5 transcripts — patterns need volume; below that you get anecdotes, not signal

## Two rules apply before any analysis

- **Redact PII first** — [`.claude/rules/pii-redaction.md`](../../rules/pii-redaction.md). Mask end-customer names, emails, and account numbers before processing; keep roles, company, and deal context.
- **Bind every claim to evidence** — [`.claude/rules/evidence-bound-outputs.md`](../../rules/evidence-bound-outputs.md). Every pattern cites a verbatim quote + speaker, or it lowers its confidence. No invented quotes.

## How it works

1. Inputs: sales-call transcripts (Gong, Fireflies, Otter, Granola, Zoom/Avoma VTT, or pasted text), each tagged with the deal outcome (won / lost / churned). Optional: `marketing/icp/ICP.md` to frame patterns by segment.
2. Normalize each transcript to speaker-attributed turns with timestamps where present.
3. Pick a mode:
   - **Single** — deep analysis of one transcript
   - **Batch** (default) — aggregate 5–20 transcripts into patterns with frequency counts
   - **Comparison** — won vs lost (or retained vs churned) side by side
4. Extract patterns across six dimensions: **product**, **messaging**, **GTM / sales process**, **pricing**, **competition**, **customer context**.
5. Score confidence by frequency: a pattern needs 2+ occurrences across different deals; High = 3+ deals, Medium = 2, Low = single mention. Aim for ≥5 wins and ≥5 losses before trusting a pattern.
6. Writes to `marketing/win-loss/win-loss.md` (overwrites prior canonical; git history preserves prior versions).

## Invoke

```
/win-loss-analysis
```

Then paste or point to the transcripts and tag each outcome. Or:

```
/win-loss-analysis — here are 8 won + 6 lost transcripts: [paste / paths]
```

## Example output

See [`marketing/win-loss/win-loss.md`](../../../pulse-analytics-example/win-loss/win-loss.md) for the PulseAnalytics example seed. Notice: patterns are grouped by dimension; each carries a frequency + a verbatim quote with speaker; the closing section routes findings to positioning / messaging / ICP.

## Dependencies

- **Reads from:** sales-call transcripts (required); `marketing/icp/ICP.md` (optional, for segment framing)
- **Reads via Granola MCP (optional):** meeting transcripts, if wired
- **Writes to:** `marketing/win-loss/win-loss.md` (canonical; positioning, messaging, and ICP read from here)

## Customization

Split the analysis by segment when your ICP has more than one (enterprise vs mid-market lose for different reasons). Add a competitor column to the competition dimension once you're losing to a named rival repeatedly — that feeds `/competitor-research`.

## Where this fits in the Example 1 chain

```
Day 1-3: /competitor-research × N → per-competitor files
Day 3:   /competitor-aggregate → competitor canonical
Day 4:   /win-loss-analysis (THIS SKILL) → win-loss canonical
Day 5:   /icp-research reads win-loss + competitors → canonical ICP
Week 2:  /positioning + /product-messaging read win-loss quotes for real buyer language
```

## Refresh cadence

Monthly if deal volume is high; quarterly otherwise. Refresh sooner on a churn spike or a new competitor showing up repeatedly in lost deals.
