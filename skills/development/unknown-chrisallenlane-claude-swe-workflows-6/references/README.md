# /lead-review — Autonomous Comprehensive Review

## Overview

The `/lead-review` skill drives a codebase through every review dimension — orientation, architecture, security, performance, accessibility, tests, release-readiness — without operator involvement between startup and termination. The operator states **scope, ticket creation (yes/no), severity floor (if tickets), and constraints** at startup; the skill then runs each enabled sub-skill in sequence, auto-approving or auto-declining ticket proposals uniformly per the startup choice. Termination is structural — once all enabled sub-skills have run, the consolidated report is produced.

This skill is the successor to `/review-deep`. The v10 move into the `/lead-*` namespace makes the autonomy-axis identity explicit; the redesign trades interactive participation for autonomous execution and adds the ticket-creation toggle so the run can serve both "produce a comprehensive backlog" and "produce a comprehensive audit report" use cases.

This skill is a member of the **orchestrator family** and implements the autonomy discipline documented in [`references/autonomy.md`](../../../references/autonomy.md). The shared discipline governs the five levers (altitude rule, pre-loaded options, pre-rebutted recommendation, commander's intent, risk budgets), the cascade rule, the no-unilateral-breaking-changes guardrail, and the shared handoff template.

**Key benefits:**
- Unattended comprehensive review — kick it off and walk away
- Two modes from one workflow: backlog generation OR audit report
- Operator intent is sovereign — CRITICAL findings in tickets-OFF mode are surfaced, not silently overridden
- Auto-detects sub-skills that do not apply (no web content → skip `/review-a11y`; no tests → skip `/review-test`)
- Cross-cutting observations highlight findings that recur across sub-skills
- `LEAD_REVIEW_STATE.md` as persistent state across sessions

## When to Use

**Use `/lead-review` for:**
- Pre-release comprehensive audit where you want all dimensions covered
- Periodic codebase health checks
- Inheriting an unfamiliar codebase (tickets OFF first, then OFF→ON after orientation)
- Producing a consolidated backlog of review-driven work for follow-up implementation
- Any time you'd otherwise run `/review-health` → `/review-arch` → `/review-security` → … by hand

**Don't use `/lead-review` for:**
- Targeted single-dimension review — use the individual `/review-*` skill directly
- Bug hunting — use `/bug-hunt` or `/lead-bug-hunt`
- Change-oriented cleanup — use `/lead-refactor`

**Rule of thumb:** if the goal is "audit the codebase across every dimension before shipping (or before deciding what to fix)," `/lead-review` is the right entry point. If the goal is targeted (one dimension, one area), invoke the relevant `/review-*` skill directly.

## The Two Modes

The same pipeline serves two operator intents:

| Mode                         | Field 2 | Behavior                                                                                                                            |
|------------------------------|---------|-------------------------------------------------------------------------------------------------------------------------------------|
| **Backlog generation**       | tickets ON  | Auto-approve sub-skill ticket proposals at/above severity floor. Tracker writes. Output: comprehensive ticket backlog + report.        |
| **Audit report**             | tickets OFF | Auto-decline all sub-skill ticket proposals uniformly. No tracker writes. Output: consolidated audit report only.                      |

The operator chooses at startup. No mid-run switching. CRITICAL findings in tickets-OFF mode are surfaced prominently in the report, not silently overridden into tickets — the autonomy contract honors commander's intent strictly.

## Relationship to `/review-deep` (predecessor)

| Dimension                | `/review-deep` (v9)                                            | `/lead-review` (v10)                                              |
|--------------------------|----------------------------------------------------------------|-------------------------------------------------------------------|
| Mode                     | Interactive throughout — operator participates in each phase   | Autonomous from startup to termination                            |
| Commander's intent       | Minimal — just skip-list confirmation                          | Four-field schema (scope, tickets, floor, constraints)            |
| Sub-skill ticket prompts | Operator answers each                                          | Auto-approved or auto-declined uniformly per startup choice       |
| /tidy-docs inclusion     | Yes (Phase 7)                                                  | No — out of axis (mutates docs even in audit-only mode)            |
| State doc                | None                                                           | `LEAD_REVIEW_STATE.md`                                            |
| Andon cord               | Operator could abort                                           | Formal andon protocol per orchestrator-family discipline           |

If you want the interactive walkthrough that `/review-deep` provided, invoke individual `/review-*` skills directly — that's the same experience without the orchestration glue.

## Relationship to Other `/lead-*` Skills

| Skill              | Outcome contract                                                  | Composition                                                                        |
|--------------------|-------------------------------------------------------------------|------------------------------------------------------------------------------------|
| `/lead-project`    | Open-ended commander's intent → OODA loop                         | May invoke `/lead-review` as a comprehensive validation pass                       |
| `/lead-bug-hunt`   | Iterate `/bug-hunt` → fix until bugs converge                     | Sibling — different outcome contract                                                |
| `/lead-refactor`   | Tactical + architectural + tactical refactor                      | Shares `/review-arch` with `/lead-review`; pick one based on goal                  |
| `/implement-project`  | Implement a multi-batch ticket project                            | Natural pair: `/lead-review` (backlog) → `/implement-project` (execution)             |

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /lead-review Workflow                                           │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  0. STARTUP                                  │
 │  ────────────────────────────────────────    │
 │  0a. Branch and working-tree check           │
 │  0b. Resume existing run or start fresh      │
 │  0c. Elicit commander's intent (4 fields)    │
 │      - Scope                                 │
 │      - Tickets ON/OFF                        │
 │      - Severity floor (if ON)                │
 │      - Constraints                           │
 │  0d. Auto-detect skip-list, confirm          │
 │  0e. Seed LEAD_REVIEW_STATE.md               │
 └──────────────────────────────────────────────┘
                      │
                      ▼
 ┌──────────────────────────────────────────────┐
 │  PHASES 1–7 (sequential, once-through)       │
 │  ────────────────────────────────────────    │
 │  1. /review-health (orientation)             │
 │  2. /review-arch (architecture)              │
 │  3. /review-security (security)              │
 │  4. /review-perf (performance)               │
 │  5. /review-a11y — if web content            │
 │  6. /review-test (test suite)                │
 │  7. /review-release (release readiness)      │
 │                                              │
 │  Each phase:                                 │
 │  - Invoke sub-skill with scope+constraints   │
 │  - Auto-approve OR auto-decline ticket       │
 │    proposals per startup choice              │
 │  - Record findings, durations, ticket IDs    │
 │  - Update state doc                          │
 │  - Cascade up any sub-skill cord pulls       │
 └──────────────────────────────────────────────┘
                      │
                      ▼
 ┌──────────────────────────────────────────────┐
 │  8. TERMINATION                              │
 │  ────────────────────────────────────────    │
 │  Consolidated completion report              │
 │  - Top things to scrutinize                  │
 │  - Cross-cutting observations                │
 │  - Per-phase summary                         │
 │  - Tickets created (if ON) or                │
 │    findings list (if OFF)                    │
 │  - Constraint adherence                      │
 │  - Run metadata                              │
 └──────────────────────────────────────────────┘
```

## Commander's Intent

Elicited interactively at startup, frozen for the duration of the run.

### Scope

Same shape as the individual `/review-*` skills' scope.

Examples:
- "Entire codebase, excluding `vendor/` and `gen/`."
- "Just `pkg/auth` and `pkg/session`."
- "All production code, with extra attention to `pkg/payments`."

### Ticket creation

The mode-defining choice. Binary.

- **Yes (backlog generation)** — every sub-skill that proposes tickets has those tickets auto-approved at/above the severity floor. Below-floor proposals are declined; findings recorded in the report. Tracker writes occur.
- **No (audit report)** — every sub-skill's ticket proposals are auto-declined uniformly. No tracker writes. All findings surface in the consolidated report.

### Severity floor

Only consulted when ticket creation is Yes.

| Floor              | Effect                                                                                                          |
|--------------------|-----------------------------------------------------------------------------------------------------------------|
| CRITICAL only      | Smallest backlog. Ships with HIGH+MEDIUM+LOW deferred to the report.                                            |
| HIGH+              | **Default.** Reasonable backlog covering real-impact findings.                                                  |
| MEDIUM+            | Larger backlog including moderate-severity work.                                                                 |
| All severities     | Largest backlog. May produce hundreds of tickets in mature codebases.                                            |

### Constraints

Hard limits beyond the always-on guardrails (no breaking changes, no main/master writes). Passed through to all sub-skills.

Examples:
- "Do not propose changes to the public API of package `auth`."
- "Do not audit `pkg/legacy`."
- "Must remain Go 1.22 compatible."

## The Andon Cord

The only planned escalation path. See `references/autonomy.md` § "Shared handoff template" for the canonical structure.

### Triggers

- **Contested finding.** The skill believes a sub-skill's finding is wrong on substance.
- **Breaking-change required.** A recommended fix would require a breaking change.
- **Sub-skill cord cascaded up.** A review sub-skill pulled its own cord.
- **Resume-time HEAD divergence.** Recorded branch SHA does not match current HEAD.

### Skill-specific handoff extensions

- **Title** — `## Andon Cord — /lead-review — Phase N (<sub-skill>)`
- **Current state** additionally includes current phase, phases complete, phases remaining, findings-ledger summary, and state-doc pointer.

After pulling the cord: stop. Wait for operator input.

## State Management

`LEAD_REVIEW_STATE.md` lives at the repo root, is gitignored, and survives across invocations. See SKILL.md § "State Management" for the full structure. Key sections:

- Pinned commander's intent
- Enabled phases / skip-list (with reasons)
- Cycle log (per phase: findings counts, ticket IDs, duration, notes)
- Findings ledger (created / declined / surfaced / contested / breaking-change-required)
- Andon cord history (full handoff text for each pull)

Update at every phase transition.

## Hard Caps

- No iteration cap — once-through pipeline has structural termination.
- 3 consecutive andon-cord triggers from the same sub-skill — if the same sub-skill produces contested findings repeatedly, pull the cord rather than triaging individually.

No file-touch or dependency-change budgets, per the autonomy discipline.

## Available Sub-Skills

The bounded review repertoire:

| Skill              | Native contract                                                | In /lead-review                                                 |
|--------------------|----------------------------------------------------------------|-----------------------------------------------------------------|
| `/review-health`   | Advisory — strategic orientation                               | Phase 1. Tickets auto-approved/declined per startup choice.     |
| `/review-arch`     | Advisory — noun analysis, target blueprint, ticket proposals   | Phase 2.                                                        |
| `/review-security` | Advisory — blue/red parallel-isolated audit, ticket proposals  | Phase 3.                                                        |
| `/review-perf`     | Advisory — compute/web performance                             | Phase 4.                                                        |
| `/review-a11y`     | Advisory — WCAG audit (skipped if no web content)              | Phase 5 (conditional).                                          |
| `/review-test`     | Advisory — five-phase test survey, ticket proposals            | Phase 6.                                                        |
| `/review-release`  | Pre-release scanner — runs tests/build, surfaces findings      | Phase 7.                                                        |

Skills explicitly **not** in the repertoire (out-of-axis):
- `/tidy-docs` — mechanical mutations, not advisory. Run separately if doc cleanup is wanted.
- `/scope-*`, `/test-mutation`, `/tidy-git`, `/bug-*`, `/refactor`, `/implement-*` — adjacent concerns.

If your goal mixes review with implementation, refactoring, or doc tidying, use `/lead-project` instead, or chain `/lead-review` with `/implement-project` / `/lead-refactor`.

## Examples

### Example 1: Pre-release audit with backlog generation

```
User: /lead-review

Starting commander's intent elicitation.

Scope — what does this review cover?
> Entire production codebase. Exclude vendor/, gen/, and the
  integration test fixtures under test/fixtures/.

Ticket creation — yes or no?
> Yes. We have time to fix things; want a backlog.

Severity floor — lowest severity that creates tickets?
> Critical+High. Defer Medium and Low to the report.

Constraints — hard limits?
> Don't propose breaking changes to pkg/api's exported types.
  Don't audit pkg/legacy (slated for removal).
  Must remain Go 1.22 compatible.

Read back:
[four-field intent]

Confirm?
> Yes

Auto-detecting skip-list...
- Web content detected (HTML in pkg/web/templates) — /review-a11y will run
- Tests detected — /review-test will run
- Dockerfile + release pipeline — /review-release will run
All 7 phases enabled. Confirm?
> Yes

Creating branch: lead-review/2026-05-12
Seeding LEAD_REVIEW_STATE.md

[Phase 1 — /review-health]
12 findings (1 Critical, 4 High, 5 Medium, 2 Low)
2 tickets proposed at/above floor, auto-approved → #501, #502
3 findings below floor (Medium/Low) deferred

[Phase 2 — /review-arch]
8 findings (3 High, 4 Medium, 1 Low)
3 tickets proposed at/above floor, auto-approved → #503, #504, #505

[Phase 3 — /review-security]
6 findings (2 Critical, 2 High, 1 Medium, 1 Low)
4 tickets proposed at/above floor, auto-approved → #506-#509

[Phase 4 — /review-perf]
4 findings (1 High, 3 Medium)
1 ticket proposed → #510

[Phase 5 — /review-a11y]
9 findings (2 High, 5 Medium, 2 Low)
2 tickets proposed → #511, #512

[Phase 6 — /review-test]
14 findings across 5 phases (coverage + quality)
6 tickets proposed → #513-#518

[Phase 7 — /review-release]
5 findings (2 High, 3 Medium)
2 tickets proposed → #519, #520

Producing consolidated report ...

## Lead-Review Complete

### Run mode
- Tickets: ON
- Severity floor: Critical+High
- Scope: production code, excluding vendor/, gen/, test/fixtures/, pkg/legacy

### Outcome
58 findings across 7 phases. 20 tickets created (#501-#520) covering
Critical+High severity findings. 38 findings below floor deferred to
the report. No contested findings, no breaking-change recommendations.

### Top things to scrutinize
1. [#506] Critical: OAuth state parameter not validated on /api/auth/callback
   — see /review-security finding, SHA <short> in state doc
2. [#510] High: O(N²) algorithm in pkg/inventory hot path
   — see /review-perf finding
3. [Cross-cutting] pkg/order flagged by /review-arch (boundary issue),
   /review-security (privilege concentration), and /review-test (coverage gap)
4. ...

### Cross-cutting observations
- pkg/order appears in 3 phases' findings — boundary clarification would
  reduce both architectural and security surface
- 7 of 14 /review-test findings involve mocked database tests — pattern
  worth addressing systematically

### Tickets created
[List of 20 tickets with IDs and one-line descriptions]

### Findings below floor (declined for ticket creation)
[List of 38 findings grouped by severity]

### Recommendation
Feed #501-#520 to /implement-project when ready to address the backlog.
```

### Example 2: Audit-only mode (no tracker writes)

```
User: /lead-review

[startup; ticket creation = No, severity floor = N/A]

[All 7 phases run, sub-skills' ticket proposals auto-declined uniformly]

## Lead-Review Complete

### Run mode
- Tickets: OFF
- Scope: entire codebase

### Outcome
58 findings across 7 phases. No tracker writes (tickets OFF).
2 Critical-severity findings — flagged in "Top things to scrutinize"
below. Operator decides next steps.

### Top things to scrutinize
1. [CRITICAL | /review-security] OAuth state parameter not validated
   on /api/auth/callback — exploitable CSRF on auth flow
2. [CRITICAL | /review-security] SSRF in /api/import via webhook URL
   — internal-network reachable
3. ...

### Findings surfaced for operator review
[All 58 findings grouped by severity, then by sub-skill]

### Recommendation
2 CRITICAL findings warrant immediate attention. Operator may:
- Re-run /lead-review with tickets ON and severity floor CRITICAL only,
  to cut just the two Critical-severity tickets
- Run individual /implement against the surfaced findings directly
- Triage findings manually and act outside the orchestrator family
```

## Tips

**Use tickets OFF for unfamiliar codebases.** A first-pass audit produces a lot of findings; you don't need them all in your tracker. Run with tickets OFF, read the report, then re-run with tickets ON scoped to the areas worth addressing.

**Severity floor calibrates effort.** Critical+High is the productive default. Lower the floor for follow-up runs once the higher severities are clean. "All severities" produces overwhelming backlogs in mature codebases.

**Cross-cutting observations are the unique value.** A finding that recurs across `/review-arch`, `/review-security`, and `/review-test` is a project-level signal worth acting on. `/lead-review`'s consolidated report highlights these explicitly.

**Resume is cheap.** Interrupting the skill is safe — the state doc captures completed phases. Re-invoke and choose "Resume" to continue from the next enabled phase.

**Andon cords are not failures.** A contested finding or a breaking-change-required recommendation is the skill doing its job — surfacing decisions that need operator judgment.

**Pair with `/implement-project` for the full review-and-fix arc.** `/lead-review` (tickets ON) generates the backlog; `/implement-project` works through it. Two skills, one comprehensive sweep.

**Pair with `/tidy-docs` separately if you want doc cleanup.** `/tidy-docs` is mechanical and out-of-axis for `/lead-review`.

## Integration with Other Skills

**Individual `/review-*` skills:** the workhorses. Each keeps its native contract; `/lead-review` adds orchestration (scope passthrough, auto-approve/decline, consolidated reporting).

**`/implement-project`:** natural pair. `/lead-review` (tickets ON) → backlog → `/implement-project` → work through backlog.

**`/lead-refactor`:** shares `/review-arch` with `/lead-review`. Pick one based on goal.

**`/lead-project`:** may invoke `/lead-review` as a comprehensive validation pass, or invoke individual `/review-*` skills earlier when specific concerns arise.

**`/tidy-docs`:** explicitly out-of-axis. Run separately.

## Agent Coordination

**Sequential execution.** One phase at a time. One sub-skill invocation per phase. No parallel phases.

**Context discipline.** The skill is a thin coordinator. All review work is delegated to sub-skills. Summary-level state lives in the skill's context; `LEAD_REVIEW_STATE.md` holds durable memory.

**Sub-skill invocation.** Invoke via the Skill tool. Sub-skill interactive prompts are answered using engineering judgment anchored to commander's intent. Specifically, ticket-creation prompts are auto-approved (tickets ON) or auto-declined (tickets OFF) uniformly.

## Abort Conditions

**Do NOT abort for:**
- A sub-skill finding nothing (proceed to next phase).
- High finding counts (the floor handles triage).
- A sub-skill being skipped per auto-detection (record and proceed).

**Pull the andon cord for:**
- Triggers listed under "The Andon Cord" above.

**Abort the entire workflow for:**
- Operator interrupts.
- Critical system error (repository corrupted, git state unrecoverable).
- Operator declines to confirm commander's intent at startup.
