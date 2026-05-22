---
name: "incident-response"
description: "Calm, systematic crisis handling — from detection through post-mortem to prevention"
applyTo: "**/*incident*,**/*outage*,**/*alert*,**/*emergency*"
---

# Incident Response Skill

> In a crisis, follow the process. Panic is the enemy of resolution.

## Severity Levels

| Level | Definition | Response Time | Escalation |
| ----- | ---------- | ------------- | ---------- |
| P1 | Service down, all users affected | Immediate (drop everything) | Notify leadership within 15 min |
| P2 | Major feature broken, no workaround | < 1 hour | Notify team lead |
| P3 | Feature degraded, workaround exists | < 4 hours | Normal channels |
| P4 | Minor issue, cosmetic or low-impact | < 24 hours | Next sprint |

**When unsure**: Triage UP (P2 → P1), not down. Downgrade after investigation.

## Response Phases

### 1. Detect — Know something is wrong

| Detection Source | Reliability | Action |
| ---------------- | ----------- | ------ |
| Automated monitoring/alerts | High | Trust the data, verify scope |
| User reports (1-2) | Medium | Reproduce, check if isolated |
| User reports (many) | High | Treat as confirmed |
| Internal discovery | Medium | Check if it's already in production |

### 2. Triage — Assess impact and urgency

Answer these **in order** (each takes < 1 minute):

1. **Who is affected?** All users / subset / internal only
2. **How many?** Percentage or count
3. **What can't they do?** Core function or edge case
4. **Is there a workaround?** If yes, communicate it immediately
5. **What changed recently?** Last deploy, config change, dependency update
6. **Severity level?** Assign P1-P4 based on answers above

### 3. Resolve — Fix it (safely)

| Situation | Best Action | Why |
| --------- | ----------- | --- |
| Recent deploy caused it | **Rollback first** | Fastest path to recovery |
| Config change caused it | **Revert config** | No code deploy needed |
| Root cause is clear, fix is small | **Hotfix** | If rollback isn't possible |
| Root cause unclear | **Enable debug logging** + check recent changes | Don't guess-and-deploy |
| Third-party dependency is down | **Activate fallback** or communicate ETA | You can't fix their service |

**Golden rule**: Restore service first, then investigate. Don't debug in production while users wait.

### 4. Review — Learn from it (post-mortem)

Do this within 48 hours while memory is fresh.

## Post-Mortem Template

```markdown
# Incident: [Brief Title]
**Date**: YYYY-MM-DD
**Severity**: P1/P2/P3/P4
**Duration**: X hours Y minutes
**Impact**: [Who was affected, what they couldn't do]

## Summary
One paragraph: what happened, impact, resolution.

## Timeline
| Time (UTC) | Event |
| ---------- | ----- |
| HH:MM | First alert / user report |
| HH:MM | Triage: determined P-level |
| HH:MM | Root cause identified |
| HH:MM | Fix deployed / service restored |
| HH:MM | Confirmed resolved |

## Root Cause
[5 Whys analysis — see root-cause-analysis skill]

## What Went Well
- [Detection was fast because...]
- [Rollback was clean because...]

## What Went Wrong
- [Alert was noisy / missed because...]
- [Took X minutes to find the right person because...]

## Action Items
| Action | Owner | Due Date | Status |
| ------ | ----- | -------- | ------ |
| Add monitoring for X | @name | YYYY-MM-DD | Open |
| Write runbook for Y | @name | YYYY-MM-DD | Open |
```

## Communication Templates

### To Users (Status Page / Email)
> **[Service] is experiencing [issues/downtime].** We are investigating and will update every [30 min / 1 hour]. Current workaround: [describe if applicable].

### To Leadership
> **Incident P[X]**: [Service] [is down / degraded] since [time]. Impact: [N users / $X revenue]. ETA for resolution: [time / investigating]. Next update: [time].

### Resolution Announcement
> **Resolved**: [Service] has been restored as of [time]. Root cause: [one sentence]. Full post-mortem to follow within 48 hours.

## On-Call Handoff Checklist

- [ ] Active incidents (status + next steps)
- [ ] Recent deploys (last 24h, any risky changes)
- [ ] Known issues (monitoring gaps, flaky tests)
- [ ] Pending alerts (expected noise vs real signal)
- [ ] Escalation contacts (who to call at 3am)

## Synapses

See [synapses.json](synapses.json) for connections.
