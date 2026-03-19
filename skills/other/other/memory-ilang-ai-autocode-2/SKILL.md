---
name: memory
description: Persistent project memory across sessions. Load on start, save on stop, merge across sessions.
---

# Memory

Persistent memory stored at `.autocode/memory.md`.

## Format

```markdown
## Project
[name] | [stack] | [key files]

## Decisions
[DECISION] description — YYYY-MM-DD

## State
[DONE] what's completed
[WORKS] what's working
[BROKEN] what's broken

## Next
- [ ] immediate task

## User
[PREFERS] brief updates over detailed explanations
[PREFERS] you decide, don't ask
[BUILDS] mostly web apps for ecommerce
[MISTAKE] forgot input validation on signup — 2026-03-17
```

## Rules
1. Max 200 lines — compress aggressively
2. Merge, don't overwrite — old decisions stay
3. Deduplicate — keep most recent
4. Date everything
5. No secrets — no API keys, passwords, tokens
6. No code — only descriptions
7. ## User section captures learn-preference, learn-pattern, learn-mistake data
