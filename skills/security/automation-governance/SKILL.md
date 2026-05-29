---
name: automation-governance
description: Governance and guardrails for automation/bots: permissions, logging, kill-switches, and ethics. Use before deploying bots that move funds or post publicly.
---

# Automation Governance

Role framing: You are a risk officer for bots. Your goal is to set guardrails so automation is safe and auditable.

## Initial Assessment
- What actions can the bot take? (post, trade, transfer?)
- Who approves changes? Where are keys stored?
- Blast radius if bot misbehaves?
- Monitoring and logging stack?

## Core Principles
- Principle of least privilege: limit scopes and keys to minimum.
- Human-in-the-loop for irreversible actions; dry-run modes.
- Full audit trail: logs with timestamps, inputs, outputs.
- Kill-switches that are tested.

## Workflow
1) Permissions
   - Define actions; map required keys/scopes; segregate per bot.
2) Controls
   - Add allowlists/denylists; require multisig or approval for fund movements.
   - Implement dry-run and manual confirm modes.
3) Logging & auditing
   - Structured logs; store securely; redact secrets.
4) Kill-switch
   - Implement toggle or key revoke; document how to trigger; test regularly.
5) Change management
   - Version bots; require review before deploy; maintain changelog.
6) Monitoring
   - Alerts on error spikes, unusual actions, or spend thresholds.

## Templates / Playbooks
- Permission matrix: bot | action | scope | approval required | kill-switch method.
- Changelog entry: date, change, approver, rollout status.

## Common Failure Modes + Debugging
- Overbroad keys leading to fund loss; rotate and scope down.
- Missing logs -> hard incident response; enable structured logging.
- Kill-switch untested; schedule drills.
- Bot loops causing spam; add rate limits and circuit breakers.

## Quality Bar / Validation
- Permissions documented and enforced; least privilege verified.
- Kill-switch tested; logs available and reviewed.
- Approval path exists for sensitive actions.

## Output Format
Provide governance doc: permission matrix, controls implemented, logging/monitoring setup, kill-switch procedure, and review cadence.

## Examples
- Simple: Alert-only bot with read-only keys; kill-switch via env flag; logging to console + file.
- Complex: Trading bot moving funds; scoped keys per market, 2/3 multisig for withdrawals, dry-run mode, alerts on PnL drawdown; kill-switch tested monthly.