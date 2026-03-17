---
name: agent-loops
description: Complete operational workflow for implementer agents (Codex, Gemini, etc.) making code changes and writing tests. Defines the Code Change Loop, Test Writing Loop, and Issue Filing process with circuit breakers, severity levels, and escalation rules. Includes bundled scripts for specialist-review (code review) and test-review-request (test audit) that delegate to Claude CLI. Use this skill when starting any implementation task.
keywords:
  - agent workflow
  - code review loop
  - test writing loop
  - implementer
  - remediation
  - circuit breaker
triggers:
  - starting implementation work
  - code change task
  - writing tests after implementation
  - remediation cycle
  - filing issues from review findings
---

# Agent Workflow Loops

This skill defines the operational loops that implementer agents follow when making
code changes and writing tests. Each loop has explicit entry criteria, exit criteria,
and escalation rules. If you are an agent, follow these loops exactly.

**You do not review your own work.** All reviews are performed by Claude via dedicated
skills. You never grade your own homework.

**Bundled references:**
- `references/testing-standards.md` — Test quality standards (how to write tests)
- `references/audit-workflow.md` — Test gap discovery (how to find what's missing)
- `references/perspective-catalog.md` — Review perspective selection (used by specialist-review)
- `references/review-prompt.md` — Claude review prompt template
- `references/audit-prompt.md` — Claude test audit prompt template

**Bundled scripts:**
- `scripts/specialist-review.sh` — Shell out to Claude CLI for code review
- `scripts/test-review-request.sh` — Shell out to Claude CLI for test audit

---

## Architecture: Who Does What

| Role | Agent | How |
|------|-------|-----|
| **Implementer** | Codex or Gemini | Writes code changes and test code |
| **Code Reviewer** | Claude | Invoked via `specialist-review` skill |
| **Test Auditor** | Claude | Invoked via `test-review-request` skill — finds gaps AND flags bad tests |
| **Remediator** | Codex or Gemini | Fixes findings from Claude's reviews |

**Critical rule:** Codex and Gemini NEVER self-review. Every review step means invoking a skill to send work to Claude. If you cannot invoke the review skill, STOP and escalate to the user — do not substitute your own review.
If shelling out to Claude fails (script error, CLI unavailable, permissions/network failure, timeout), escalate to the user immediately.

---

## Skill Invocation Reference

### `specialist-review` — Request Code Review from Claude

**When:** After completing implementation, after each remediation cycle.
**What you get back:** Findings with severity levels (P0-P3) and a verdict (BLOCKED / PASS WITH ISSUES / CLEAN).

#### IMPORTANT: Do Not Review the Code Yourself

Your ONLY job is to run the script and read the output file. Do NOT analyze the diff.
Do NOT write review comments. Do NOT adopt perspectives. Shell out and read the result.

The review requires Claude's skills ecosystem (JIT loading of domain-specific skills
like `owasp-top-10`, `secure-coding-practices`, `python-testing-patterns`, etc.).
Non-Claude agents do not have access to these skills.

#### How to Invoke

```bash
# Review only the files you changed (RECOMMENDED)
scripts/specialist-review.sh --git -- src/parser/ src/auth.rs

# Review changes since a specific ref, scoped to a directory
scripts/specialist-review.sh --git origin/main -- claude_ctx_py/

# Review all changes vs last commit (use sparingly in monorepos)
scripts/specialist-review.sh --git

# Pipe in a pre-filtered diff
git diff HEAD~3..HEAD -- src/ | scripts/specialist-review.sh -

# Review a diff file
scripts/specialist-review.sh /path/to/changes.diff

# Custom output directory
scripts/specialist-review.sh --git --output ./my-reviews -- src/
```

Read the output file path printed to stdout:
```bash
REVIEW_FILE=$(scripts/specialist-review.sh --git -- src/parser/)
cat "$REVIEW_FILE"
```

**Always scope to the files you touched.** In a monorepo, an unscoped `--git` sends
the entire repo diff to Claude, wasting tokens and risking timeouts.

#### Anti-Patterns

- **Performing the review yourself** — You do not have the skills ecosystem. Shell out.
- **Summarizing the diff before shelling out** — Unnecessary. The script reads the diff directly.
- **Ignoring the output file** — The review is written to a file. Read it.
- **Using sub-agents for the review** — The script invokes a single Claude CLI process.
- **Proceeding after a failed shell-out** — Escalate to the user instead of continuing without Claude review.

### `test-review-request` — Request Test Audit from Claude

**When:** Initial audit (before writing tests) and re-audit (after writing/fixing tests).
**What you get back:** A gap report covering both missing coverage AND test quality issues (mirror tests, flaky assertions, etc.), with P0/P1/P2 severity.

#### IMPORTANT: Do Not Audit the Tests Yourself

Your ONLY job is to run the script and read the output file. Do NOT read source code
to map behaviors. Do NOT classify test coverage. Do NOT produce a gap report.
Shell out and read the result.

The audit requires Claude's skills ecosystem — specifically the `test-review` skill
which pipelines testing standards into a structured audit workflow. Non-Claude agents
do not have access to these skills or the project-specific testing standards.

#### How to Invoke

```bash
# Full audit of a module (default)
scripts/test-review-request.sh /path/to/module

# Full audit with specific test directory
scripts/test-review-request.sh /path/to/module --tests /path/to/tests

# Quick review of specific test files only
scripts/test-review-request.sh --quick /path/to/test_file.py

# Custom output directory
scripts/test-review-request.sh /path/to/module --output ./my-reports
```

Read the output file path printed to stdout:
```bash
REPORT_FILE=$(scripts/test-review-request.sh src/parser)
cat "$REPORT_FILE"
```

Act on findings:
- **P0 (Security/Correctness Critical)**: Fix before merge.
- **P1 (Reliability/Edge Cases)**: Fix in current sprint.
- **P2 (Completeness/Confidence)**: Backlog.

#### Anti-Patterns

- **Performing the audit yourself** — You do not have the testing standards or audit workflow.
- **Pre-reading source before shelling out** — Unnecessary. The script passes the module path to Claude.
- **Ignoring the output file** — The gap report is written to a file. Read it.
- **Using sub-agents for the audit** — The script invokes a single Claude CLI process.
- **Proceeding after a failed shell-out** — Escalate to the user instead of continuing without Claude audit.

---

## Overview

There are two primary loops. They run sequentially — the code loop completes before the test loop begins.

```
┌─────────────────────────────────────────────────────────────────┐
│                        CODE CHANGE LOOP                         │
│  Implement → specialist-review → Remediate → specialist-review  │
│  Exit: all P0/P1 findings resolved                              │
│  Output: clean code + issues filed for P2+                      │
├─────────────────────────────────────────────────────────────────┤
│                        TEST WRITING LOOP                        │
│  Audit → Write Tests → Verify → Re-audit → Remediate → ...    │
│  Exit: all P0/P1 gaps covered, no bad tests                    │
│  Output: tests passing + issues filed for P2+                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Loop 1: Code Change Loop

### Severity Levels

| Severity | Meaning | Loop Behavior |
|----------|---------|---------------|
| P0 | Security flaw, incorrect behavior, data loss, crashes | MUST fix before exit |
| P1 | Error handling gaps, resource leaks, missing validation, concurrency issues | MUST fix before exit |
| P2 | Code quality, naming, documentation, minor edge cases | File issue, do not block |
| P3 | Style preferences, optional improvements, future optimization | File issue, do not block |

### The Loop

```
ENTRY: Task spec or ticket describing the required change.

┌──────────────────┐
│  IMPLEMENT       │ ← You (Codex/Gemini): write the code change per spec
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ specialist-review│ ← Run: scripts/specialist-review.sh --git -- <files>
└──────┬───────────┘   Script diffs your changed files, sends to Claude
       │
       ├── Findings? ──► Yes ──► Any P0 or P1? ──► Yes ──┐
       │                                                   │
       │                        No ──► File P2/P3 issues   │
       │                               Exit loop           │
       │                                                   │
       │   No findings ──► Exit loop                       │
       │                                                   │
       ▼                                                   ▼
                                          ┌──────────────────┐
                                          │  REMEDIATE       │ ← You: fix ONLY P0/P1
                                          └──────┬───────────┘   findings cited by Claude
                                                 │
                                                 ▼
                                          ┌──────────────────┐
                                          │ specialist-review│ ← Run script again (same paths)
                                          └──────┬───────────┘   Script diffs remediated files,
                                                 │               Claude re-evaluates
                                                 └── Loop back to findings check
```

### Circuit Breaker

**Maximum iterations: 3 `specialist-review` cycles.**

If P0/P1 findings remain after 3 cycles:
1. Stop. Do not attempt a 4th remediation.
2. Produce a summary of unresolved findings with context on why they persist.
3. Escalate to human reviewer with the summary and Claude's last review output.

This prevents infinite loops when you keep introducing new issues while fixing old ones, or when a finding requires a design-level change you can't make in remediation scope.

### Code Review Checklist (Claude's Criteria)

Claude evaluates against these criteria via `specialist-review`. You need to understand these so you can anticipate and prevent issues before review, and correctly interpret findings during remediation.

**Correctness:**
- [ ] Does the code do what the spec says? Not more, not less.
- [ ] Are all error cases handled? No unwrap() on fallible operations in non-test code (Rust). No unhandled promise rejections (TS).
- [ ] Are numeric operations safe from overflow/underflow?
- [ ] Are string operations safe with unicode input?
- [ ] Does the code handle empty/zero/None inputs?

**Security (when applicable):**
- [ ] Is untrusted input validated before use?
- [ ] Are auth checks present on protected paths?
- [ ] Is sensitive data (keys, tokens) excluded from logs and error messages?
- [ ] Are timing-safe comparisons used for secrets?

**Patterns and conventions:**
- [ ] Does the code follow existing patterns in the codebase? (highest precedence)
- [ ] Are new types/functions placed in the right modules?
- [ ] Do public APIs have doc comments?
- [ ] Are error types specific and actionable?

**Resource management:**
- [ ] Are connections, file handles, and locks properly released?
- [ ] Are timeouts set on all I/O operations?
- [ ] Do caches/pools have bounded capacity?
- [ ] Is cleanup handled on error paths, not just success paths?

**Concurrency (when applicable):**
- [ ] Is shared state accessed through appropriate synchronization?
- [ ] Are lock scopes minimized?
- [ ] Could this deadlock? (nested locks, await while holding lock)

### Review Output Format (What Claude Returns)

Claude's `specialist-review` response will follow this format. Parse it to determine your next action.

```markdown
## Code Review: [change description]

**Files reviewed:** [list]
**Iteration:** N of 3

### Findings

#### P0-001: [title]
**File:** `src/tunnel.rs:45-52`
**Issue:** [what's wrong]
**Impact:** [what happens if not fixed]
**Suggested fix:** [specific guidance, not just "fix this"]

#### P1-001: [title]
**File:** `src/auth.rs:23`
**Issue:** [what's wrong]
**Impact:** [what happens if not fixed]
**Suggested fix:** [specific guidance]

#### P2-001: [title]
**File:** `src/config.rs:100`
**Issue:** [what's wrong]
**Recommendation:** [what to improve]

### Summary
- P0: N findings (MUST fix)
- P1: N findings (MUST fix)
- P2: N findings (file issues)
- P3: N findings (file issues)
- **Verdict:** BLOCKED / PASS WITH ISSUES / CLEAN
```

### Remediation Rules

When fixing findings from Claude's review:
- Fix ONLY the cited findings. Do not refactor adjacent code.
- Do not introduce new functionality while remediating.
- If a fix requires changing the approach significantly, note this in the remediation and let Claude evaluate the full new approach on the next `specialist-review` cycle.
- Each remediated finding should be annotated: `Fixed P0-001: [what was changed]`
- If you disagree with a finding, see "Disagreeing with Claude's Findings" below — do not silently skip it.

---

## Loop 2: Test Writing Loop

This loop runs after the code change loop exits cleanly. It ensures the new (and existing) code has adequate test coverage.

The audit does double duty: it finds missing coverage AND flags bad tests (mirror tests, flaky assertions, etc.). A bad test doesn't close a gap, so a single audit pass catches both problems. No separate quality review step needed.

### Roles

| Role | Agent | Skill |
|------|-------|-------|
| **Auditor** | Claude | `test-review-request` — finds gaps and flags bad tests per `references/audit-workflow.md` |
| **Test Writer** | Codex or Gemini | Writes tests per `references/testing-standards.md` standards |

### Pragmatic Enforcement Policy

Use a hybrid gate to avoid unnecessary friction while preserving confidence:

- **Non-trivial code changes (default):** The test-writing loop is required. Do not close the loop without audit evidence from `test-review-request` and a re-audit state with no unresolved P0/P1 gaps.
- **Trivial changes (explicit exception):** Docs-only, comments-only, formatting-only, or rename-only edits may skip the audit loop.
- **Mandatory note for skips:** Every skip must include `audit skipped: trivial` with a one-line reason in the loop summary.
- **Uncertainty rule:** If it is not clearly trivial, run the audit.

**Practical close criteria for implementer loops:**
1. Tests added or updated for the change (when behavior changed).
2. Local verification commands run and reported.
3. Audit evidence present, or explicit trivial skip note present.

### The Loop

```
ENTRY: Code change loop has exited cleanly.

┌──────────────────────┐
│  AUDIT               │ ← Run: scripts/test-review-request.sh <module>
└──────┬───────────────┘   Script sends module + tests to Claude, returns gap report
       │
       ▼
┌──────────────────────┐
│  SCOPE APPROVAL      │ ← Human reviews gap report
└──────┬───────────────┘   P0/P1 auto-approved. P2+ at human discretion.
       │                   Approved gaps become your work list.
       ▼
┌──────────────────────┐
│  WRITE TESTS         │ ← You (Codex/Gemini): write tests for P0 first,
└──────┬───────────────┘   then P1. Follow testing-standards.md.
       │
       ▼
┌──────────────────────┐
│  VERIFY              │ ← You: run the tests locally. They must:
└──────┬───────────────┘   1. Compile / pass lint
       │                   2. All pass (no test is born failing)
       │                   3. Actually exercise the code (not no-ops)
       ▼
┌──────────────────────┐
│  RE-AUDIT            │ ← Run: scripts/test-review-request.sh <module>
└──────┬───────────────┘   Same module path — script re-reads source + tests
       │                   Claude checks: gaps closed? new tests good?
       │
       ├── All P0/P1 resolved? ──► Yes ──► File P2/P3 issues
       │                                   Exit loop ✅
       │
       └── No ──► Any P0/P1 remaining?
                  │
                  ▼
           ┌──────────────────┐
           │  REMEDIATE       │ ← You: fix/rewrite the flagged tests
           └──────┬───────────┘   or write tests for remaining gaps
                  │
                  └── Back to VERIFY
```

### What the Audit Catches

The audit report covers both gap analysis and quality in a single pass:

**Coverage gaps (missing tests):**
- Behaviors in the public contract with no corresponding test
- Error paths with no failure test
- Edge cases (empty input, boundary values, unicode) not exercised

**Test quality issues (bad tests):**
- Mirror tests — expected values computed from implementation, not hardcoded
- Trivial assertions — `assert(true)`, assertions that can never fail
- Happy-path-only — tested behavior has no edge case or failure test
- Over-mocking — mocks at internal boundaries, not just external (network, fs, time)
- Flaky patterns — timing-dependent assertions, hardcoded ports, shared state

A bad test shows up as an unclosed gap. A mirror test for behavior X means X is still "Missing" in the gap report, not "Covered". This is why one audit pass is sufficient.

### Audit Severity

| Severity | Meaning | Example |
|----------|---------|---------|
| P0 | Critical gap or false confidence | Missing auth test, mirror test on security path, assertion that passes with implementation deleted |
| P1 | Meaningful gap or fragile test | No error path test, happy-path-only, hardcoded port, timing-dependent assertion |
| P2 | Coverage improvement or test hygiene | Missing edge case, poor naming, verbose setup that should be a helper |

### Circuit Breaker

**Maximum iterations: 3 audit cycles** (initial audit + 2 re-audits).

If P0/P1 gaps remain after 3 cycles, escalate to human with a summary of what's proving difficult to test and why. This usually indicates the code needs refactoring to be testable — that's a design problem, not a test problem.

---

## Loop 3: Issue Filing

After both loops exit, file issues for everything that was deferred.

### Backlog-First Policy

When filing deferred findings in this repository:

- If a `backlog/` folder exists at repo root **and** Backlog tooling is available (Backlog MCP tools and/or Backlog CLI), use Backlog to create tracked issues/tasks.
- Include enough context for another agent to execute without re-auditing:
  - source review/audit artifact
  - affected files/modules
  - severity and user impact
  - suggested fix direction
  - acceptance criteria
- If Backlog is not available, create a markdown handoff under `.agents/fixes/`.
  - Prefer naming by replacing `review` with `fix` from the source artifact name (`s/review/fix/`).
  - If no review artifact name exists, use a descriptive `*-fix.md` filename.
- Implementers may also choose to fix deferred findings immediately instead of filing, when appropriate.

### Issue Template

```markdown
## [P2/P3] [Module]: [Brief description]

**Source:** [Code Review / Test Audit] iteration N
**Severity:** P2 | P3
**Module:** [file path]

### Description
[What's missing or what could be improved]

### Context
[Why this was deferred — not blocking but worth addressing]

### Suggested approach
[Brief guidance on how to address]

### Acceptance criteria
[How to verify this is done]
```

### Filing Rules

- One issue per finding. Do not batch unrelated findings.
- P2 issues get the label `quality` or `test-gap` as appropriate.
- P3 issues get the label `improvement`.
- Issues from test audits reference the specific behavior from the gap report.
- Issues include enough context that a different agent (or human) can pick them up without re-auditing.

---

## Operational Notes

### Agent Responsibilities Summary

**You (Codex / Gemini) are responsible for:**
- Reading and understanding the task spec
- Writing implementation code
- Writing test code
- Running tests locally and verifying they pass
- Running `scripts/specialist-review.sh --git -- <your-files>` after implementation and each code remediation
- Running `scripts/test-review-request.sh <module>` for initial audit and each re-audit
- Fixing ONLY the findings Claude identifies (no scope creep during remediation)
- Filing P2/P3 issues when loop exits
- Escalating when circuit breaker triggers

**You are NOT responsible for:**
- Reviewing your own code (Claude does this)
- Judging your own test coverage or quality (Claude does this via audit)
- Deciding whether a finding is valid (if you disagree, note it in the remediation and let Claude re-evaluate — do not silently skip findings)

### Disagreeing with Claude's Findings

If Claude flags something you believe is incorrect:
1. Do NOT silently ignore the finding.
2. In your remediation response, explicitly state: `Disputed P1-003: [your reasoning]`
3. Run the script again with the dispute noted in your commit/changes.
4. Claude will either accept your reasoning or reaffirm the finding with additional context.
5. If still disputed after 2 cycles, escalate to human — do not loop forever on a disagreement.

### What "Escalate to Human" Means

When the circuit breaker triggers:
1. Stop all loops.
2. Produce a structured summary:
   - What was attempted
   - What findings remain unresolved
   - Why they persist (agent's best assessment)
   - Recommended human action
3. Do not attempt creative workarounds to avoid escalation.

### Metrics (Track If Tooling Supports)

Per loop run:
- Number of iterations before exit
- Findings by severity per iteration
- Number of findings that regressed (fixed then reappeared)
- Time per iteration
- Circuit breaker activations

These metrics help tune the loop — if you're consistently hitting 3 iterations, either the review checklist is too strict or the implementer instructions need work.

---

## Quick Reference: The Full Pipeline

```
1. TASK SPEC arrives
       │
       ▼
2. CODE CHANGE LOOP
   ├── You: implement
   ├── scripts/specialist-review.sh --git -- <files> → Claude reviews diff (max 3 cycles)
   ├── You: remediate P0/P1
   ├── File issues for P2/P3
   └── Exit with clean code
       │
       ▼
3. TEST WRITING LOOP
   ├── scripts/test-review-request.sh <module> → Claude audits (gaps + quality)
   ├── Human: scope approval (P0/P1 auto-approved)
   ├── You: write tests (testing-standards.md)
   ├── You: verify tests pass locally
   ├── scripts/test-review-request.sh <module> → Claude re-audits (max 3 cycles)
   ├── You: remediate P0/P1 gaps and bad tests
   ├── File issues for P2/P3
   └── Exit with tested code
       │
       ▼
4. ISSUE FILING
   └── P2/P3 findings → tracked issues
       │
       ▼
5. PR READY FOR HUMAN REVIEW
```
