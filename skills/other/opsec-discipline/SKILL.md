---
name: opsec-discipline
description: Use when about to take any outward or offensive action (request, payload, persistence, lateral movement, exfil, or feeding captured traffic to the model) — to decide detection footprint, cleanup, and secret redaction first
---

# OPSEC Discipline

## Overview

Decide the detection footprint and cleanup **before** acting, not after. Every offensive technique
in this repo pairs with the telemetry it generates and a detection signature — use that pairing to
choose the quieter path and to know what you'll need to clean up.

## Before acting, answer three questions

1. **Detection** — what telemetry does this generate? Which Sigma/EDR rule would catch it? (Each
   domain skill's OPSEC & Detection table has this.) Pick the lower-noise variant when one exists.
2. **Cleanup** — what does this touch (files, registry, services, accounts, tickets)? How is it
   reverted? Stage the cleanup before you create the artifact.
3. **Secret hygiene** — any captured traffic / output that reaches the model or the report must be
   redacted at the boundary:
   `python skills/coding-mastery/scripts/_lib/redact_headers.py < exchange.txt` (or `redact_text()`),
   so Authorization/Cookie/API-key/JWT values never land in context or the report.

## Red Flags — STOP, decide OPSEC first

- "I'll worry about cleanup after I'm in" (you won't; decide now)
- "Just paste the raw request/response" (redact secrets at the boundary first)
- "Loudest exploit is fine, it works" (pick the variant with the smaller footprint)
- "Persistence now, document later" (persistence on un-authorized hosts is out — see scope-discipline)
- "The token's only in a log" (a logged secret is a leaked secret — mask it)

## Rationalizations

| Excuse | Reality |
|--------|---------|
| "OPSEC slows me down" | Unplanned noise/loot is how engagements get burned and how data leaks. |
| "It's an internal tool log" | Logs get shipped, shared, and indexed. Redact. |
| "Cleanup is a reporting-phase task" | You can't clean what you didn't track. Track at action time. |

OPSEC is part of every action, not a phase. Detection-awareness also strengthens the defensive value
of the finding (you can tell the client exactly how to catch it).
