---
name: parallel-review
description: Orchestrate multiple review skills in parallel against a codebase. Spawns specialized subagents, waits for all to complete, and synthesizes findings into a unified report. Supports pre-merge, deep audit, project health, and post-incident modes.
user-invocable: true
argument-hint: "<mode> <target> — modes: pre-merge | deep-audit | health | post-incident | test | design"
---

Read `../_house-style/house-style.md` before starting.

## What this skill does

You are a review coordinator. You do not review code yourself. You spawn parallel subagents — each running a specialized review skill — wait for all to finish, then synthesize their findings into a single, prioritized, deduplicated report.

## Modes

Parse the first argument to determine the mode. If no mode is given, infer from context or ask.

### `pre-merge` — Before merging a PR or branch

Spawn **three** parallel subagents:

1. **Paranoid reviewer** — Run `/paranoid-review` on the target. Hunt for production killers, race conditions, silent failures, missing error handling.
2. **Dependency auditor** — Run `/dep-audit` on the target. Check for CVEs, abandoned deps, unnecessary deps, license risk.
3. **Ship gate** — Run `/ship` on the target. Pre-flight checklist: debug artifacts, secrets, test coverage, PR hygiene, rollback readiness.

### `deep-audit` — Comprehensive quality review

Spawn **three** parallel subagents:

1. **Section reviewer** — Run `/section-review` on the target. First-principles decomposition, scoring, scalability, security, testability.
2. **Tech debt assessor** — Run `/tech-debt` on the target. Quantified inventory: weekly cost, incident risk, blast radius, fix effort.
3. **API reviewer** — Run `/api-review` on the target. Consumer-first audit of contracts, error shapes, auth, pagination, idempotency. *Skip this subagent if the target has no API surface — state that you skipped it and why.*

### `health` — Monthly project health check

Spawn **three** parallel subagents:

1. **Dependency auditor** — Run `/dep-audit` on the target.
2. **Tech debt assessor** — Run `/tech-debt` on the target.
3. **Onboarding auditor** — Run `/onboarding-audit` on the target. Zero-knowledge new-developer experience.

### `post-incident` — After an outage or incident

Spawn **three** parallel subagents:

1. **Postmortem investigator** — Run `/postmortem` on the target. Reconstruct timeline from git, find process failures, five whys.
2. **Retrospective analyst** — Run `/retro` on the target. Git-data-backed analysis of what actually happened.
3. **Paranoid reviewer** — Run `/paranoid-review` on the target. Find related bugs that haven't fired yet.

### `test` — Full test suite assessment and remediation

Spawn **three** parallel subagents:

1. **Test auditor** — Run `/test-audit` on the target. Measure real confidence vs. false confidence. Classify every test as valuable, decoration, or harmful. Identify critical untested paths.
2. **Test writer** — Run `/test-write` on the target. Read the code, identify the highest-risk untested behaviors, and write tests that would catch real bugs. Focus on error paths, edge cases, and security paths.
3. **Test fixer** — Run `/test-fix` on the target. Run the existing test suite, diagnose every failure and flaky test, determine if the test is wrong or the code is wrong, and fix the right one.

### `design` — Full UX, UI, and accessibility audit

Spawn **three** parallel subagents:

1. **UX designer** — Run `/ux-designer` on the target. Walk every core flow as a new user. Find friction, dead ends, confusion, broken mental models. Score time-to-value, flow clarity, information architecture, state coverage, recovery.
2. **UI designer** — Run `/ui-designer` on the target. Evaluate visual hierarchy, typography, color, spacing, component consistency, responsiveness. Find design system violations, weak affordances, missing states.
3. **Accessibility auditor** — Run `/a11y-audit` on the target. Audit against WCAG 2.2 AA. Keyboard navigation, screen reader compatibility, color contrast, semantic HTML, form accessibility. Every violation references the specific WCAG criterion.

## Execution rules

1. **Spawn all subagents in a single message.** Do not run them sequentially. The entire point is parallelism.
2. **Each subagent gets the full target path/branch/PR as context.** Pass the user's target argument to each one.
3. **Each subagent must read `../_house-style/house-style.md`** — this is already in each skill's instructions, but verify the subagent follows house style in its output.
4. **Wait for all subagents to complete before synthesizing.** Do not start the synthesis until every subagent has returned.
5. **Do not soften or editorialize subagent findings.** Your job is to deduplicate, prioritize, and structure — not to add diplomacy.

## Synthesis rules

After all subagents return:

### 1. Deduplicate

Multiple reviewers will find the same issue. Merge duplicates into a single finding, crediting which reviewers flagged it. If reviewers disagree on severity, take the higher severity and note the disagreement.

### 2. Prioritize

Rank all findings by severity:

1. **Disasters waiting to happen** — structurally guaranteed failures that haven't fired yet
2. **Critical** — will break in production or is actively broken
3. **High** — breaks under load, edge cases, or adversarial input
4. **Medium** — tech debt, missing tests, compounding quality issues
5. **Low** — style, minor improvements

### 3. Resolve conflicts

If reviewers contradict each other (one says ship, another says block), surface the contradiction explicitly. Do not silently pick a side. Present both arguments and state which has stronger evidence.

## Output format

### Mode and target

State the mode, target, and which subagents were spawned.

### Unified findings

All findings from all reviewers, deduplicated and priority-ordered. Each finding includes:

- **Severity** (Disaster / Critical / High / Medium / Low)
- **Source** (which reviewer(s) flagged it)
- **File:line** and evidence
- **The fix** — specific, not "add error handling"

### Reviewer verdicts

| Reviewer | Verdict | Key concern |
|---|---|---|
| (name) | (their verdict) | (one-line summary) |

### Conflicts

Where reviewers disagreed. Both sides. Which has stronger evidence.

### Combined verdict

One of:

- **Ship it** — no critical/high findings across all reviewers
- **Fix then ship** — list the blockers, in priority order
- **Rethink** — fundamental problems identified by multiple reviewers
- **Investigate** — (post-incident mode) action items before any code changes

### Top 5 action items

Dependency-ordered. File:line, what to do, why, which reviewer identified it.

### What was checked

Which skills ran, what each covered.

### What was NOT checked

Gaps across all reviewers. If all three reviewers say they didn't check X, that's a blind spot worth highlighting.
