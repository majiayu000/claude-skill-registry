---
name: retro
description: Brutally honest engineering retrospective. Analyzes git history for what actually happened — not what people think happened. Gives blunt, specific, data-backed feedback per contributor. No vibes, only data.
user-invocable: true
argument-hint: "[time range, e.g. 'last week', 'last 2 weeks', 'march']"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- Git is the source of truth. Not memory. Not standups. Not Slack.
- More commits does not mean more output. More LOC does not mean more value.
- "Great job everyone" is not feedback. It's the absence of feedback.
- Specific praise builds trust. Vague praise builds nothing.

## Domain-specific examples

**Contributor feedback — wrong way:**

"Alice had a productive week with lots of commits. She's doing great work on the payment system. Keep it up!"

**Contributor feedback — right way:**

"**Alice** — 12 commits, +1.8k LOC, 8% test ratio, 3 PRs. All PRs under 200 LOC — disciplined. Shipped the Stripe webhook handler (`app/services/webhooks/stripe.rb`) with retry logic and idempotency keys — this is the kind of infrastructure that prevents 2am pages. **Growth opportunity:** test ratio at 8% on payment code is a liability. The webhook handler has no test for the duplicate-event path, which is the most common Stripe failure mode. Add integration tests for duplicate and out-of-order events before the next payment feature goes in."

**Team observation — wrong way:**

"Overall a productive week. We should try to write more tests and do code reviews faster."

**Team observation — right way:**

"14 PRs merged, 3 sat open for over 48 hours (PRs #89, #92, #94 — all waiting on Bob's review). Review bottleneck is measurable: those 3 PRs represent 4 days of blocked work. Either distribute review load (Alice reviewed 0 PRs this week) or set a 24-hour SLA. Test ratio dropped from 34% to 28% week-over-week. The decline is entirely in `app/services/` — 6 new service files, 0 test files. This is debt accumulating in the most critical layer."

## Data collection

From git history for the requested range:

**Per-contributor:** commits, LOC +/-, files touched, test LOC %, PR count/size, fix/revert ratio, active days, peak hours (from timestamps).

**Team-level:** total commits/LOC/PRs, hotspot files, biggest ship, revert ratio, test ratio.

**Patterns:** coding sessions (commit clusters), late-night commits (burnout signal), long branch gaps (blockers), stale PRs (review bottleneck), multi-person hotspot files (coordination risk).

## Output format

### Period summary
One paragraph: what shipped, in numbers. Not what was planned.

### Biggest wins
Top 3. Specific: what, who, why it matters. From git.

### Biggest problems
Top 3. Blunt. Evidence from git.

### Per-contributor breakdown
For each:
- **Stats:** commits, LOC, test ratio, PRs, active days, peak hours
- **What they shipped:** specific, from git
- **What went well:** specific praise with evidence
- **Growth opportunity:** specific, actionable, engineering-practice-level

### Hotspots
Most-modified files. Who touched them, how often, test coverage.

### Risks
Trends: test coverage direction, PR size growth, bus factor changes, dep update freshness.

### Three things to change
Specific, owned: what, who, by when, how you verify.

### Devil's advocate
For your harshest per-person feedback: could external factors explain it? Blockers you don't see in git?

### What I didn't check
Context I can't get from git: meetings, planning, blocked-on-others time.
