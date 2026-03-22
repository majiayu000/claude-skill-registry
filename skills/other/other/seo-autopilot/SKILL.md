---
name: seo-autopilot
description: Run local SEO autopilot for boll-koll.se or hyresbyte.se and return PR link plus summary.
allowed-tools:
  - exec
metadata:
  triggers:
    - "seo"
    - "seo boll-koll.se"
    - "seo hyresbyte.se"
  allowed_sites:
    - boll-koll.se
    - hyresbyte.se
  command:
    - scripts/run.sh
license: MIT
---

# seo-autopilot

## Usage (WhatsApp / chat)
- seo
- seo boll-koll.se
- seo hyresbyte.se

Default site: boll-koll.se

## Safety
Only allow: boll-koll.se, hyresbyte.se  
Never run arbitrary commands. Only run:
- scripts/run.sh <site>

## Behavior
1. Parse site from the message, default to boll-koll.se.
2. Refuse if site is not in allowlist.
3. Run: scripts/run.sh <site>
4. Extract PR url from stdout (line starting with "PR:").
5. If SEO_REPORT.md exists in the repo, include the top 3 findings in the reply.
