---
name: phx:challenge
description: Challenge mode reviews - rigorous questioning before approving changes. Use when you want thorough scrutiny of Ecto changes, LiveView events, or PR readiness.
effort: high
argument-hint: ecto | liveview | pr
---

# Challenge Mode Reviews

Rigorous, critical review patterns inspired by Boris Cherny's "Grill me" approach. Push beyond first solutions to ensure quality.

## Iron Laws - Never Violate These

1. **No approval without verification** - Don't approve until all concerns addressed
2. **Assume bugs exist** - Look for edge cases, race conditions, missing handlers
3. **Question everything** - Even "obvious" code can hide issues
4. **Demand proof** - Ask for tests, show state transitions, verify behavior

## Adversarial Lenses (Apply to ALL Modes)

Before diving into mode-specific checks, apply these three lenses:

1. **"What Would Break This?"** — Describe realistic scenarios where this code fails catastrophically. Not edge cases — production failure modes under load, during deploys, with unexpected data.
2. **"Assumption Stress Test"** — List every assumption this code relies on. Which are most fragile? (e.g., "assumes user always has an email", "assumes this query returns < 1000 rows")
3. **"Contradictions Finder"** — Find contradictions between tests and implementation, docs and behavior, or between different parts of the changeset.

## Challenge Modes

### Ecto Challenge (`/phx:challenge ecto`)

Grill the developer on database changes:

**Migration Safety**

- Will this migration lock the table in production?
- What happens to existing records without the new field?
- Is the migration reversible?
- Are there any unsafe operations (column removal, type change)?

**Query Performance**

- Have you introduced any N+1 queries?
- Are there missing indexes for new WHERE clauses?
- Will this query scale with data growth?

**Schema Integrity**

- Are all constraints enforced at database level?
- What happens during rolling deployment (old code, new schema)?
- Are foreign key cascades correct?

**Backward Compatibility**

- Will old code work during deployment?
- Are there any breaking changes to the context API?

### LiveView Challenge (`/phx:challenge liveview`)

Prove the LiveView handles all cases:

**Event Coverage**

- List every `handle_event` clause and expected socket state
- What happens if socket assigns are missing when event fires?
- Are there race conditions between user events and server pushes?

**PubSub Handling**

- List every `handle_info` clause and when it's triggered
- Do all PubSub subscriptions have corresponding handlers?
- What happens if a message arrives before mount completes?

**State Transitions**

- Show the event → handler → state transition table
- Are all error states handled gracefully?
- What's the recovery path from each error state?

**Memory & Performance**

- Are large lists using streams?
- Is transient data using temporary_assigns?
- What's the memory footprint per connected user?

### PR Challenge (`/phx:challenge pr`)

Senior engineer review checklist:

**Must Pass**

- [ ] No direct Repo calls in controllers/LiveViews
- [ ] All Ecto queries use explicit preloads
- [ ] Changesets validate all user input
- [ ] No atoms created from params
- [ ] Error cases handled (not just happy path)
- [ ] Tests cover new functionality

**Performance**

- [ ] No queries in Enum.map loops
- [ ] LiveView streams for lists > 100 items
- [ ] Indexes exist for WHERE clause columns

**OTP**

- [ ] GenServers have supervision
- [ ] Timeouts set for GenServer.call
- [ ] No unbounded process spawning

**Security**

- [ ] No SQL injection via raw queries
- [ ] No path traversal in file handling
- [ ] Authorization checks present

## Prior Findings Deduplication (MANDATORY)

**CRITICAL**: This step prevents the "3 challenges to clear" problem
where identical issues are re-discovered across consecutive runs.
Session data confirms this happens without explicit dedup enforcement.

Before running a challenge, **ALWAYS** check for prior review output:

1. **Search** for existing reviews in `.claude/plans/*/reviews/` and `.claude/reviews/`
2. If prior findings exist, **read ALL of them** before analyzing code
3. Build a PRIOR_FINDINGS list with file:line references
4. During analysis, check each potential finding against PRIOR_FINDINGS:
   - If the exact code location was flagged AND is now fixed → **SKIP entirely**
   - If flagged AND still present → Mark **PERSISTENT** (one line, not full re-analysis)
   - If NOT in prior findings → Mark **NEW** (full analysis)
   - If was fixed but reintroduced → Mark **REGRESSION**
5. **Only NEW findings get full analysis** — PERSISTENT gets one-line mention

When presenting results, show NEW findings first, then PERSISTENT
(one-line each), then REGRESSION. Never re-analyze code that was
already flagged — just check if the fix was applied.

## Usage

Run `/phx:challenge [mode]` to initiate a rigorous review. The reviewer will not approve until all concerns are addressed with evidence.

Example workflow:

1. Run `/phx:challenge ecto` after migration changes
2. Answer each question with code references or test results
3. Address all concerns before proceeding to PR
