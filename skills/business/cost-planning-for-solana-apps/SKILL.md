---
name: cost-planning-for-solana-apps
description: Estimate and control costs for Solana apps: RPC, indexing, storage, bots, and on-chain fees. Use for budgeting and scaling.
---

# Cost Planning for Solana Apps

Role framing: You are a cost engineer. Your goal is to forecast and manage spend while maintaining reliability.

## Initial Assessment
- User and transaction volume forecasts? Peak vs average?
- Components: RPC providers, indexers, storage, bots, CDNs?
- On-chain fee sensitivity? Priority fee usage?
- Growth plans or campaigns that cause spikes?

## Core Principles
- Measure before optimizing; instrument request counts and tx fees.
- Separate fixed vs variable costs; design caps for bursty traffic.
- Choose the right tier per workload (read-heavy vs write-heavy).

## Workflow
1) Baseline
   - Measure current request/tx volume; classify by method.
2) Forecast
   - Model scenarios (steady, spike, campaign) with request multipliers.
3) Map providers and pricing
   - RPC per 1M, indexer tiers, storage (DB/kv), alerting tools.
4) Optimization levers
   - Caching, batching, webhooks over polling, hedged reads vs redundant writes, priority fee tuning.
5) Budgets and alerts
   - Set monthly budget, per-component limits; alerts when 75/90% used.
6) Review
   - Weekly spend review; adjust configs and rate limits.

## Templates / Playbooks
- Cost sheet columns: component | unit cost | baseline usage | forecast usage | monthly est | owner | levers.
- Priority fee tuning guide: start low, monitor confirmation time vs cost.

## Common Failure Modes + Debugging
- Underestimating spikes from campaigns -> blown RPC budget; pre-purchase burst capacity or throttle.
- Polling loops runaway; switch to webhooks.
- Priority fees set too high by default; adjust dynamically.
- Duplicate requests from retries; add idempotency and caching.

## Quality Bar / Validation
- Cost model built with at least two scenarios; assumptions documented.
- Alerts configured; dashboards show usage vs budget.
- Optimization actions identified and scheduled.

## Output Format
Provide cost model table, key assumptions, levers to pull, and alert setup plan.

## Examples
- Simple: Small dApp uses free tier read RPC + single paid write endpoint; cache balances; monthly budget  with alerts.
- Complex: High-volume bot infra; multiple paid RPCs, Kafka + DB storage, webhook ingest; cost model includes spike during launch; dynamic priority fee controller to keep confirmations under 2s within budget.