---
name: review-deep
description: Comprehensive pre-release review pipeline. Runs /review-health, /review-arch, /review-security, /review-perf, /review-a11y, /review-test, /review-doc, and /review-release in sequence. Thin orchestrator — each sub-skill keeps its normal interactive behavior. Auto-detects phases that do not apply and asks the user to confirm skipping them. Ends with a consolidated report.
model: opus
---

# Review-Deep — Comprehensive Pre-Release Review

Convenience wrapper that runs every `/review-*` skill in a coordinated sequence. Typically used before a release, or any time you want a comprehensive audit across every review dimension the plugin provides.

## Philosophy

**Thin orchestrator, not a new process.** This skill composes eight existing `/review-*` skills. It adds sequencing, skip detection, branch safety, and a consolidated final report — nothing else. Each sub-skill retains its normal behavior.

**Interactive throughout.** The user participates in every sub-skill's decision points. This is not fire-and-forget. If you want an autonomous sweep, use the individual skills directly with their autonomous modes (where supported).

**Detect-and-confirm skips.** Some phases do not apply to every project (no web content → no a11y; no tests → no test review). The orchestrator detects these conditions, proposes a skip list, and asks the user to confirm before starting.

## Workflow Overview

```
┌──────────────────────────────────────────────────────┐
│                 REVIEW-DEEP WORKFLOW                 │
├──────────────────────────────────────────────────────┤
│  0. Branch safety check                              │
│  1. Skip detection + user confirmation               │
│  2. Execute enabled phases, in order:                │
│     1. /review-health                                │
│     2. /review-arch                                  │
│     3. /review-security                              │
│     4. /review-perf                                  │
│     5. /review-a11y                                  │
│     6. /review-test                                  │
│     7. /review-doc                                   │
│     8. /review-release                               │
│  3. Consolidated final report                        │
└──────────────────────────────────────────────────────┘
```

## Workflow Details

### 0. Branch Safety Check

Before starting, verify the current git branch.

**If on `main` or `master`:**
- Ask the user: "You're on `<branch>`. This workflow may produce many commits across multiple phases. Create a new branch, or proceed on `<branch>`?"
- If the user wants a new branch: create `review-deep/<date>` (e.g., `review-deep/2026-04-22`) and check it out.
- If the user explicitly confirms proceeding on main/master: continue.

**If on any other branch:** Proceed without asking.

### 1. Skip Detection + User Confirmation

Only the following phases are candidates for auto-skipping. All other phases always run.

| Phase              | Skip condition                                                                                   | Heuristic                                                                                                                                                                                                         |
|--------------------|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/review-security` | No meaningful executable source code (e.g., a Claude plugin of only markdown, a docs-only repo)  | Scan for source files with runtime-relevant extensions (`.go`, `.rs`, `.py`, `.rb`, `.js`, `.ts`, `.tsx`, `.jsx`, `.java`, `.c`, `.cpp`, `.sh`, `.php`, etc.). If count is zero or trivially small, propose skip. |
| `/review-perf`     | No meaningful executable source code                                                             | Same heuristic as security.                                                                                                                                                                                       |
| `/review-a11y`     | No web content                                                                                   | Scan for `.html`, `.htm`, `.jsx`, `.tsx`, `.vue`, `.svelte`, `.css`, `.scss`, `.less`, `.ejs`, `.hbs`, `.pug`, `.njk`. If none, propose skip.                                                                     |
| `/review-test`     | No tests available                                                                               | Scan for common test markers: `tests/`, `test/`, `spec/`, `__tests__/`, files matching `*_test.go`, `test_*.py`, `*_test.py`, `*.test.ts`, `*.spec.ts`, `*_spec.rb`. If none, propose skip.                       |

**Exclude from scans:** `vendor/`, `node_modules/`, `dist/`, `build/`, `.git/`, and similar generated/vendored directories.

**Present the proposal to the user:**

```
## Review-Deep — Phase Plan

Proposed to skip:
- /review-a11y   — no web content detected
- /review-test   — no tests detected

Will run:
- /review-health
- /review-arch
- /review-security
- /review-perf
- /review-doc
- /review-release

Confirm, or override (e.g., "also skip /review-perf", "force-run /review-test")?
```

Accept the user's confirmation or overrides. The user may force-run any skipped phase, or force-skip any phase (including ones not in the skip-candidate table). Record the final enabled phase list.

If no phases end up as skip candidates, still present the full plan so the user knows what is about to happen and can override before starting.

### 2. Execute Enabled Phases

For each enabled phase, in the fixed order listed above:

1. Announce the phase:
   ```
   ## Phase N of M: /review-<name>
   ```
2. Invoke the sub-skill. **Do not override its interactive behavior.** The user interacts with the sub-skill directly — answering its scope questions, its boldness prompts, its selection menus, and so on. The orchestrator does not suppress, fast-path, or reinterpret any sub-skill prompt.
3. When the sub-skill completes, capture its completion summary (each sub-skill already produces one). Store it for the final report.
4. Briefly acknowledge completion and transition:
   ```
   ## Phase N complete. Moving on to /review-<next>.
   ```

**Branch safety delegation.** The orchestrator has already performed the branch safety check in step 0. If a sub-skill would otherwise ask the same question, inform it: "Branch safety has been handled by /review-deep." (This applies primarily to `/refactor-deep`-style checks; most `/review-*` skills do not check the branch.)

**Mid-phase user abort.** If the user aborts a sub-skill mid-flight, treat that phase as incomplete. Ask whether to continue to the next phase or end the workflow. Do not retry the aborted sub-skill automatically.

**Sub-skill failure.** If a sub-skill fails (error, unrecoverable state), record the failure and ask whether to continue to the next phase. Do not abort the whole workflow on a single phase failure.

### 3. Consolidated Final Report

Present a single report that aggregates the results of every enabled phase. The goal is synthesis across phases, not re-printing each sub-skill's summary verbatim.

```
## Review-Deep Complete

### Phases
| Phase            | Status        | Key Outcome                                     |
|------------------|---------------|-------------------------------------------------|
| /review-health   | Complete      | Classified as OSS library; 2 Major findings    |
| /review-arch     | Complete      | 3 blueprint items implemented, 2 deferred       |
| /review-security | Complete      | 1 high-severity finding; 4 advisory             |
| /review-perf     | Complete      | No critical bottlenecks; 2 caching suggestions  |
| /review-a11y     | Skipped       | No web content                                  |
| /review-test     | Complete      | +14 tests, -3 brittle tests; coverage 72 → 81%  |
| /review-doc      | Complete      | 7 docs updated                                  |
| /review-release  | Complete      | Release verdict: GO, after 2 advisory items     |

### Changes Made
[Summarize commits made during the workflow, using `git log`
 from the branch-start point. Group by phase where possible.]

### Cross-Cutting Observations
[Synthesize across phases. Examples:
 - Multiple phases flagged inconsistent error handling → project-level concern
 - Arch review renamed modules; doc review updated doc references to match
 - Security and perf both pointed at the same hot-path function
 If no cross-cutting themes emerged, say so concisely.]

### Outstanding Recommendations
[Items that phases surfaced but did not implement, grouped by phase.
 The user can address these later or in a follow-up run.]

### Release Readiness
[If /review-release ran, carry forward its final verdict (GO / NO-GO / GO with conditions)
 and the specific conditions, if any. Otherwise, omit this section.]
```

## Abort Conditions

**Do NOT abort the workflow for:**
- A single phase finding nothing to report
- A single sub-skill failing (record and move on after user confirmation)
- User aborting a single sub-skill (ask about continuing)
- A skipped phase turning out to be warranted (report it, move on)

**Abort the workflow for:**
- Andon cord triggers: unrecoverable git state, critical system error
- User explicitly ends the workflow

## Andon Cord Protocol

**Before pulling the andon cord:**
1. Attempt autonomous resolution first (e.g., ask the sub-skill to recover, re-invoke with narrower scope)
2. Only escalate if autonomous resolution has failed or is clearly futile

**When pulled:**
1. Stop all work immediately
2. Present current phase, what was attempted, what went wrong, any recovery tried, and a recommended path forward
3. Wait for user guidance

## Integration with Other Skills

**This skill is a composition of:**
- `/review-health` — first-pass strategic orientation on the repo
- `/review-arch` — architectural analysis and restructuring
- `/review-security` — white-box security audit
- `/review-perf` — performance review (compute and/or web)
- `/review-a11y` — WCAG accessibility audit
- `/review-test` — coverage, fuzz, and quality test review
- `/review-doc` — documentation audit and updates
- `/review-release` — pre-release readiness check

**When to use `/review-deep` vs. individual skills:**
- Use `/review-deep` before a release, or for a comprehensive periodic audit.
- Use an individual `/review-*` skill for targeted single-dimension review, or when a previous `/review-deep` surfaced a specific area to re-examine.

**Relationship to `/refactor-deep`:**
- `/refactor-deep` composes refactoring skills: `/refactor`, `/review-arch`, `/refactor`, `/review-doc`. It is change-oriented.
- `/review-deep` composes review skills and is evaluation-oriented. It shares `/review-arch` and `/review-doc` with `/refactor-deep`; running both back-to-back in the same session is usually redundant. Prefer `/review-deep` when release readiness is the goal.
