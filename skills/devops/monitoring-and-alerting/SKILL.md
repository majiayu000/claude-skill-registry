---
name: monitoring-and-alerting
description: Monitoring plan for Solana apps: RPC health, tx success, program errors, and liquidity signals. Use to set up dashboards and alerts.
---

# Monitoring and Alerting

Role framing: You are an observability lead. Your goal is to ensure early detection of issues across RPC, programs, and markets.

## Initial Assessment
- What components exist? (frontend, backend, programs, bots, LPs)
- SLOs for latency/success? On-call structure?
- Tools available (Grafana, Datadog, Helius webhooks, Sentry)?

## Core Principles
- Measure what users feel: tx success, latency, wallet connect, pool health.
- Separate signal from noise: actionable alerts only.
- Include on-chain + off-chain metrics.

## Workflow
1) Metrics selection
   - RPC: latency, error rates, slot lag.
   - Tx pipeline: submit latency, confirmation time, failure codes.
   - Program: error counts by code, compute units used.
   - Market: price, liquidity depth, volume, holder concentration.
2) Instrumentation
   - Add logs with error codes; emit metrics from services/bots.
   - Subscribe to webhooks for program logs/events.
3) Dashboards
   - Build views for user journeys (connect, sign, swap/mint) and infra (RPC health).
4) Alerts
   - Set thresholds and runbooks (e.g., tx fail rate >3% over 5m -> switch RPC).
   - Pager paths with severity levels.
5) Testing
   - Fire drill alerts; validate runbooks; ensure contacts current.

## Templates / Playbooks
- Alert table: metric | threshold | duration | action | owner.
- Standard runbook entries for RPC failover, blockhash errors, LP imbalance.

## Common Failure Modes + Debugging
- Alert fatigue: too many low-priority alerts; prune.
- Missing program error visibility; add msg! with codes and parse logs.
- Slot lag misread due to provider differences; monitor per provider.
- No runbook -> slow response; write and link.

## Quality Bar / Validation
- Dashboards live with top metrics; alerts tested.
- Each alert has runbook and owner.
- On-call rotation known; contact methods tested.

## Output Format
Provide monitoring plan: metrics list, dashboards needed, alert thresholds with runbooks, and ownership map.

## Examples
- Simple: Dashboard for tx success + RPC latency; alert to Slack on error spike; runbook to switch RPC.
- Complex: Full stack including program log parsing, pool depth alerts, holder concentration tracking; PagerDuty rotation with quarterly drills.