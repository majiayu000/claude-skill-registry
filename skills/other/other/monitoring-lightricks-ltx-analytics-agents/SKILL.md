---
name: monitoring
description: Monitors key metrics and sends alerts for revenue, usage, enterprise accounts, backend costs, and API runtime. Routes requests to specialized monitoring sub-agents.
tags: [monitoring, alerts, metrics]
---

# Monitoring Agent

## When to use

- "Monitor revenue metrics"
- "Set up usage alerts"
- "Track enterprise account health"
- "Monitor backend costs"
- "Alert on API runtime issues"
- "Create monitoring dashboard"
- "Set up anomaly detection"

## What it does

Routes monitoring requests to specialized sub-agents based on the monitoring type:

| Monitoring Type | Sub-Agent | File |
|----------------|-----------|------|
| Revenue tracking | **Revenue Monitor** | `agents/monitoring/revenue/SKILL.md` |
| Feature/user usage | **Usage Monitor** | `agents/monitoring/usage/SKILL.md` |
| Enterprise accounts | **Enterprise Monitor** | `agents/monitoring/enterprise/SKILL.md` |
| Backend/GPU costs | **BE Cost Monitor** | `agents/monitoring/be-cost/SKILL.md` |
| API runtime & performance | **API Runtime Monitor** | `agents/monitoring/api-runtime/SKILL.md` |

## How to route

1. **Identify monitoring type** from user request
2. **Read the appropriate sub-agent SKILL.md**
3. **Follow that sub-agent's workflow**

## Examples

| User says... | Route to... |
|-------------|-------------|
| "Alert me when revenue drops" | Revenue Monitor |
| "Track feature adoption rates" | Usage Monitor |
| "Monitor McCann account usage" | Enterprise Monitor |
| "Alert on GPU cost spikes" | BE Cost Monitor |
| "Track API latency issues" | API Runtime Monitor |

## Reference files

All monitoring agents use:

| File | Read when |
|------|-----------|
| `shared/bq-schema.md` | Before writing SQL |
| `shared/metric-standards.md` | Before defining metrics |
| `shared/event-registry.yaml` | Before referencing events |

## Rules

- DO identify the monitoring type before routing
- DO read the sub-agent's SKILL.md completely before executing
- DO NOT mix multiple monitoring types in one workflow — route separately
- DO validate threshold values with the user before setting alerts
