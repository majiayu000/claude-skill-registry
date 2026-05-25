---
name: incident-response
description: >
  When something breaks in production: triage the severity, gather evidence,
  identify root cause, deploy a fix or mitigation, and write a post-mortem.
  Provides a calm, structured process for high-stress moments.
---

<!--
  TÜRKÇE AÇIKLAMA
  ───────────────
  Bu skill, production'da bir şey patladığında sakin ve yapılandırılmış bir kriz yönetimi
  sağlar. Şiddeti sınıflandır → kanıtları topla → kök nedeni bul → düzelt → post-mortem yaz.
  Panikle atılan komutlar sorunu büyütür; bu skill önce düşün, sonra hareket et prensibini uygular.

  NE ZAMAN: Production çöktüğünde, error spike'ta, güvenlik ihlali şüphesinde,
            deployment sonrası beklenmedik regresyonda.
  ÇIKTI:    .agent/incidents/INC-<tarih>-<slug>.md — timeline + root cause + action items.
-->

# Incident Response Skill

## When to Trigger

- Production is down or severely degraded
- Error rate spikes significantly above baseline
- A customer reports a critical bug in production
- A security breach or data leak is suspected
- A deployment caused an unexpected regression

## Step-by-Step Process

### 1. Declare and Classify the Incident

**First: breathe. Then classify.**

| Severity | Definition | Response Time |
|----------|-----------|---------------|
| P1 — Critical | Full outage, data loss, security breach | Immediate |
| P2 — High | Major feature broken, significant users affected | < 30 min |
| P3 — Medium | Partial degradation, workaround exists | < 2 hours |
| P4 — Low | Minor bug, cosmetic issue | Next sprint |

Open `.agent/incidents/INC-<YYYY-MM-DD>-<slug>.md` and write:

```markdown
# Incident: <short title>
**Date:** <YYYY-MM-DD HH:MM UTC>
**Severity:** P<N>
**Status:** Investigating
**Incident Commander:** <name>
```

### 2. Triage — Gather Evidence Fast

Don't guess. Collect data first.

Checklist:
- [ ] What is the user-visible symptom?
- [ ] When did it start? (check monitoring, not just "someone reported it")
- [ ] What changed recently? (last deploy, config change, dependency update)
- [ ] What does the error log say? (get exact error messages + stack traces)
- [ ] Is it affecting all users or a subset?
- [ ] Is there an automated alert, or was this user-reported?

Commands to run immediately:

```bash
# Recent deploys
git log --oneline -20

# Check running process / container health
# (adjust for your stack)
docker ps
systemctl status <service>

# Tail live logs
docker logs -f <container> --tail 100
journalctl -u <service> -n 100 -f
```

Add findings to the incident file under `## Evidence`.

### 3. Contain the Blast Radius

Before fixing, limit the damage:

- **If a bad deploy caused it:** roll back immediately
  ```bash
  git revert HEAD
  # or redeploy previous known-good version
  ```
- **If a specific feature is failing:** toggle it off via feature flag
- **If data is being corrupted:** take the affected service offline temporarily
- **If a secret was exposed:** rotate it immediately, then investigate

Document every action taken in the incident file with timestamps.

### 4. Root Cause Analysis

Once contained, find the *real* cause — not just the symptom.

Use the **5 Whys** technique:
```
Why did users see a 500 error?
→ Because the database query timed out.
Why did the query time out?
→ Because a new index was missing after the migration.
Why was the index missing?
→ Because the migration script didn't include CREATE INDEX.
Why didn't the migration script include it?
→ Because we don't have a convention for checking query plans before deploy.
→ Root cause: Missing pre-deploy query plan review process.
```

The root cause is almost never the immediate technical failure — it's the process gap that allowed it.

### 5. Fix and Deploy

Write the fix:
- Smallest possible change that resolves the issue
- Add a test that would have caught this
- Double-check the fix in staging before production

Deploy:
- Monitor metrics during deploy
- Keep someone watching logs for 15 minutes post-deploy
- Confirm symptom is resolved with a real user test

### 6. Write the Post-Mortem

Within 24h of resolution, write a post-mortem in `.agent/incidents/INC-<date>-<slug>.md`:

```markdown
# Post-Mortem: <title>

## Summary
<2-3 sentences: what happened, how long, how many users affected>

## Timeline
| Time (UTC) | Event |
|------------|-------|
| HH:MM | Issue first occurred (inferred from logs) |
| HH:MM | First alert / user report |
| HH:MM | Incident declared |
| HH:MM | Mitigation applied |
| HH:MM | Root cause identified |
| HH:MM | Fix deployed |
| HH:MM | Incident resolved |

## Root Cause
<The actual root cause — not just the symptom>

## What Went Well
- <something that helped — good monitoring, fast rollback, etc.>

## What Went Poorly
- <something that made it worse — slow detection, unclear runbook, etc.>

## Action Items

| Action | Owner | Due Date |
|--------|-------|----------|
| Add missing index to migration convention | <name> | <date> |
| Add test for query performance | <name> | <date> |
| Set up alert for DB query p99 latency | <name> | <date> |
```

### 7. Update the Knowledge Base

After the post-mortem, use the `knowledge-base-update` skill to create a `gotcha` entry for the root cause so future agents and developers know about it.

## Rules

- **Contain first, diagnose second.** Stopping the bleeding is more important than understanding the wound.
- **No blame in post-mortems.** Focus on process gaps, not people.
- **Every incident generates at least one action item.** If nothing changes, it will happen again.
- **Never declare an incident resolved until a real user confirms the fix.** Metrics can lie; users don't.
- **All P1/P2 incidents require a post-mortem.** No exceptions.
