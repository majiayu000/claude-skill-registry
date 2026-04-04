---
name: incident-mode
description: Triage a production incident with safe, minimal changes and rollback guidance.
---

## Intent
Use for production incidents or outages.

## Steps
1. Identify scope, impact, and current environment.
2. Gather logs/metrics safely (Prometheus/Grafana, app logs).
3. Propose minimal fix or mitigation; avoid risky refactors.
4. Provide rollback plan and post-incident follow-ups.

## Safety
- No destructive commands without explicit approval.
- Preserve evidence for postmortem.
