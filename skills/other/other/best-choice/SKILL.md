---
name: best-choice
description: Select the best technology for any project automatically during planning. Never ask users to choose technology. Activates whenever technical decisions are needed.
---

# Best Choice

YOU choose all technology. User never picks.

Criteria (in order): Speed → Cost → Stability → Simplicity

Defaults:
- Backend: Go (fast, tiny memory, cheap to run)
- Frontend: HTML/CSS/JS (zero build, works everywhere)
- Database: SQLite (zero config, good for 90% of projects)
- Deploy: Cloudflare Workers (free tier, global)
- Full-stack: Next.js if UI-heavy, Go if API-heavy

Explain in user terms:
"Same $6/month server — other approaches handle 100 users, mine handles 10,000."

NEVER say: "Go's goroutine concurrency model provides efficient..."
