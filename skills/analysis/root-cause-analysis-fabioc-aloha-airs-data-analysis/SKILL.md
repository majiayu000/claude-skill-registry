---
name: "root-cause-analysis"
description: "Find the true source, not symptoms — systematic debugging from observation to permanent fix"
applyTo: "**/*debug*,**/*error*,**/*bug*,**/*issue*,**/*problem*"
---

# Root Cause Analysis Skill

> If you fixed it but it came back, you fixed a symptom.

## Core Principle

Every symptom has a cause. Every cause has a deeper cause. Keep digging until you reach something you can *prevent*, not just fix.

## 5 Whys — Extended Example

| # | Question | Answer |
| - | -------- | ------ |
| 1 | Why did the page crash? | JavaScript threw a TypeError on null |
| 2 | Why was the value null? | The API returned an empty response |
| 3 | Why did the API return empty? | The database query timed out |
| 4 | Why did the query time out? | Missing index on a 10M-row table |
| 5 | Why was the index missing? | No performance review in the PR process |

**Root cause**: Process gap (no performance review), not the missing index.
**Fix the system**: Add performance checklist to PR template, not just add the index.

### 5 Whys Traps

| Trap | Example | How to Avoid |
| ---- | ------- | ------------ |
| Stopping at human error | "Dev forgot to add the index" | Ask *why was it possible to forget?* |
| Single chain only | Only follow one branch | Branch at each Why if multiple causes |
| Speculation without evidence | "Probably because of..." | Each answer must have evidence |
| Going too deep | Why #12: "Because physics" | Stop when you reach an actionable system change |

## Cause Categories

| Category | Common Patterns | Investigation Tools |
| -------- | --------------- | ------------------- |
| Code | Null reference, off-by-one, race condition, type mismatch | Debugger, unit tests, static analysis |
| Data | Corrupt input, unexpected format, encoding issues | Query logs, data validation, sample inspection |
| Infrastructure | Disk full, memory exhaustion, network partition | Metrics dashboards, health endpoints, `top`/`df` |
| Dependencies | Breaking change, version mismatch, transitive conflict | Lockfile diff, changelog review, `npm ls` |
| Configuration | Wrong env var, feature flag state, missing secret | Config diff, environment comparison |
| Process | Missing review, unclear ownership, no runbook | Post-mortem patterns, team interviews |

## Investigation Techniques

### Binary Search Debugging

When you don't know where the bug is, halve the search space:

1. Identify the last known good state (commit, deploy, timestamp)
2. `git bisect` between good and bad
3. Each step: does the bug exist? Yes → go earlier. No → go later.
4. Result: the exact commit that introduced the bug.

### Timeline Reconstruction

| Time | Event | Source |
| ---- | ----- | ------ |
| T-24h | Deploy v2.3.1 | CI/CD logs |
| T-12h | Config change: cache TTL 60→30s | Config audit log |
| T-2h | First user report | Support tickets |
| T-0 | Alert fired | Monitoring |

**Key question**: What changed between "working" and "broken"?

### Correlation vs Causation

| Evidence Type | Confidence | Example |
| ------------- | ---------- | ------- |
| Reproduces on demand | High | "Every time I submit this form..." |
| Correlates with a deploy | Medium | "Started after we deployed" |
| Timing coincidence | Low | "Started Monday" (traffic patterns?) |
| "It's never done this before" | Very Low | Memory is unreliable — check logs |

## Fix + Prevent Pattern

| Phase | Purpose | Example | Deadline |
| ----- | ------- | ------- | -------- |
| **Immediate** | Stop the bleeding | Rollback, disable feature, redirect traffic | Now |
| **Permanent** | Fix root cause | Add missing index, fix validation, patch dependency | This sprint |
| **Prevention** | Stop recurrence | Add CI check, monitoring alert, runbook, PR checklist | Next sprint |

**Test the fix**: The permanent fix should make the immediate fix unnecessary. If you remove the band-aid and the symptom returns, you haven't found root cause.

## Common Symptom → Root Cause Patterns

| Symptom | Obvious Cause | Deeper Root Cause |
| ------- | ------------- | ----------------- |
| Memory leak | Unclosed resource | No resource cleanup pattern in codebase |
| N+1 queries | Missing join | ORM hides query count, no query logging |
| Intermittent test failure | Timing-dependent | Shared mutable state between tests |
| "Works on my machine" | Different environment | No environment parity tooling (Docker, etc.) |
| Data corruption | Missing validation | Validation in UI only, not at API boundary |
| Slow deploys | Large artifact | No build caching, monorepo without selective builds |

## Post-Mortem Integration

The RCA section of a post-mortem should include:

1. **The 5 Whys chain** (with evidence for each level)
2. **Contributing factors** (things that made it worse, not the direct cause)
3. **What we were lucky about** (things that could have made it much worse)
4. **Action items** with owners and dates for permanent fix + prevention

## Synapses

See [synapses.json](synapses.json) for connections.
