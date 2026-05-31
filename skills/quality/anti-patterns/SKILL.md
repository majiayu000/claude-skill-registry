---
name: anti-patterns
description: Catalogue of known SDLC anti-patterns that great_cto agents must actively reject when reviewing architecture, plans, code, or post-mortems. Used by architect (pre-impl), pm (planning), senior-dev (impl), l3-support (post-incident).
when_to_use: |
  Apply when:
  - architect is writing ARCH/ADR and might be tempted by a known bad pattern
  - pm is decomposing tasks and the breakdown smells like a known failure mode
  - senior-dev is implementing and considers a "quick fix" that is anti-pattern
  - l3-support is doing root-cause and finds an anti-pattern as the cause
  - any agent reviewing third-party code that exhibits anti-patterns
effort: low
allowed-tools: Read, Grep, Glob
paths:
  - "docs/**"
  - "src/**"
  - "lib/**"
---

# SDLC anti-patterns to reject

Reference catalogue. Cite the anti-pattern by name when blocking a
proposal — gives the user a clear vocabulary to discuss the issue.

## Architecture anti-patterns

### A-1. God service
**Smell:** One service does auth, billing, search, file storage, and email.
**Why bad:** Single deploy unit, single point of failure, every team
touches it, change velocity drops over time.
**Fix:** Split by business capability (DDD bounded context).

### A-2. Distributed monolith
**Smell:** 12 microservices but they share a database and deploy together.
**Why bad:** All cost of distributed (latency, eventual consistency, ops
overhead) with none of the benefits (independent deploy, isolation).
**Fix:** Either truly separate (own DB, own deploy pipeline) or merge.

### A-3. Synchronous chains
**Smell:** Request → Service A → Service B → Service C → Service D.
**Why bad:** Compound failure probability, p99 latency adds up.
**Fix:** Async with events, or co-locate hot path.

### A-4. Premature optimization
**Smell:** Custom Redis Lua scripts, hand-tuned binary protocols, before
the first paying user.
**Why bad:** Complexity cost paid up front, never recouped.
**Fix:** Start simple. Optimize when you have load data.

### A-5. Resume-driven development
**Smell:** "Let's use Kubernetes / GraphQL / event sourcing / DDD" with
no current pain it solves.
**Why bad:** Optimizes for engineer's resume, not user's outcome.
**Fix:** Ask "what's the simplest thing that could work?"

## Plan / process anti-patterns

### P-1. Big-bang rewrite
**Smell:** "Let's rewrite this in <new framework>."
**Why bad:** 80% of rewrites fail. The old system has years of bug fixes
baked in.
**Fix:** Strangler-fig. New behaviour in new code, old code coexists,
delete when traffic moves.

### P-2. Hero culture
**Smell:** "Senior X always fixes the 3am incidents."
**Why bad:** Bus factor 1. X burns out. Knowledge doesn't transfer.
**Fix:** Runbooks, post-mortems, rotating on-call, pair-debugging.

### P-3. No reversibility plan
**Smell:** Plan ships a one-way door (data migration, public API change,
breaking-contract release).
**Why bad:** If wrong, recovery is days or weeks.
**Fix:** Mandate dry-run + rollback path before approval.

### P-4. Plan without timeboxes
**Smell:** Tasks named "implement feature X" with no end criteria.
**Why bad:** Open scope, time inflates to fit.
**Fix:** Each task ≤ 4 hours, with explicit "done = X" criteria.

## Code-level anti-patterns

### C-1. God class / God function
**Smell:** A class > 500 lines or function > 100 lines doing 5 unrelated things.
**Why bad:** Tests become integration tests. Diff readability collapses.
**Fix:** Single responsibility. Extract collaborators.

### C-2. Stringly typed
**Smell:** Status passed as strings ("open", "closed", "blocked") with no enum.
**Why bad:** Typos compile. New status forgotten in switch.
**Fix:** Enum / discriminated union / branded type.

### C-3. Catch-and-continue
**Smell:**
```js
try { doThing(); } catch (e) { console.log(e); }
```
**Why bad:** Hides bugs. Silent corruption.
**Fix:** Catch only what you can handle; re-throw the rest; log with context.

### C-4. Hardcoded secrets
**Smell:** API keys, passwords, DB URLs in source.
**Why bad:** Leaks in git history forever; rotation requires force-push (impossible).
**Fix:** Env vars or secret manager. Pre-commit hook to grep for `sk-`, `ghp_`, etc.

## Incident / ops anti-patterns

### O-1. No SLO
**Smell:** "Production seems slow today" but no SLO target.
**Why bad:** Can't tell breach from normal.
**Fix:** Set p99 latency, error rate, availability SLOs. Track burn.

### O-2. Alert spam
**Smell:** Every error pages. Engineers stop reading alerts.
**Why bad:** Real incidents get missed in noise.
**Fix:** Page only on user-visible failure. Other signals to dashboard, not pager.

### O-3. Post-mortem blame
**Smell:** "Engineer X deployed without testing."
**Why bad:** Suppresses future post-mortems. Blame doesn't fix the system.
**Fix:** Blameless post-mortems. Focus on missing guardrails, not the human.

### O-4. Snowflake servers
**Smell:** "Don't reboot SRV-PROD-3, it has special config that's not in IaC."
**Why bad:** Disaster recovery impossible.
**Fix:** Everything in IaC. Servers are cattle, not pets.

## How to use this catalogue

When you find one of these in a proposal/review:

1. Cite the code (A-3, P-1, etc.) so the user has a vocabulary
2. Quote the specific smell from the proposal
3. Propose the specific fix
4. If the user disagrees, capture as ADR with the alternatives section
   filled in

## When NOT to apply

- Hobby projects, learning exercises — anti-patterns are about scale
- Throwaway code with explicit `// TODO delete in 2 weeks`
- Time-boxed POCs where the goal is "does the API actually work"
