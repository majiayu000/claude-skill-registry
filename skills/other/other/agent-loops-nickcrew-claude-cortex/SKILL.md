---
name: agent-loops
description: Complete operational workflow for implementer agents (Codex, Gemini, etc.) making code changes and writing tests. Drives all work through atomic commits — each loop operates on the smallest complete, reviewable change. Defines the Code Change Loop, Test Writing Loop, Lint Gate, and Issue Filing process with circuit breakers, severity levels, and escalation rules. Requires `committer` for all commits. Includes bundled provider-aware review scripts that keep same-model shell-outs as the last resort, plus a fresh-context Codex fallback for code review and test audit. Use this skill when starting any implementation task.
keywords:
  - agent workflow
  - code review loop
  - test writing loop
  - lint gate
  - linter
  - code quality
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

**You do not review your own work.** All reviews are performed by an independent
reviewer. Prefer Claude via the bundled scripts. If Claude is unavailable, use a
different model before asking your own model family to review. Same-model shell-outs
are the last resort. You never grade your own homework.

**Bundled references:**
- `references/testing-standards.md` — Test quality standards (how to write tests)
- `references/audit-workflow.md` — Test gap discovery (how to find what's missing)
- `references/perspective-catalog.md` — Review perspective selection (used by primary and fallback code review)
- `references/review-prompt.md` — Code review prompt template for fallback reviewers
- `references/audit-prompt.md` — Test audit prompt template for fallback reviewers

**Bundled scripts:**
- `$SKILL_DIR/scripts/specialist-review.sh` — Provider-aware Claude/Gemini/Codex CLI path for code review
- `$SKILL_DIR/scripts/test-review-request.sh` — Provider-aware Claude/Gemini/Codex CLI path for test audit

### Locate Scripts

The bundled scripts live inside the installed skill directory, not the project tree.
Before invoking any script, resolve `SKILL_DIR` so paths work regardless of install scope:

```bash
SKILL_DIR="$(ls -d ~/.codex/skills/agent-loops 2>/dev/null || ls -d .codex/skills/agent-loops 2>/dev/null)"
```

All script invocations below use `"$SKILL_DIR/scripts/..."`. Run the snippet above once
at the start of your session and reuse the variable.

---

## Architecture: Who Does What

| Role | Agent | How |
|------|-------|-----|
| **Implementer** | Codex or Gemini | Writes code changes and test code |
| **Code Reviewer** | Claude preferred; non-self scripted fallback next; same-model provider last; fresh-context Codex final fallback | `specialist-review` keeps same-model shell-outs last; fallback reviewer uses bundled prompts and produces a review artifact |
| **Test Auditor** | Claude preferred; non-self scripted fallback next; same-model provider last; fresh-context Codex final fallback | `test-review-request` keeps same-model shell-outs last; fallback auditor uses bundled prompts and produces an audit artifact |
| **Remediator** | Codex or Gemini | Fixes findings from the independent review/audit artifact |

**Critical rule:** Codex and Gemini NEVER self-review unless every independent
provider path has already failed. Every review step must be performed by an
independent reviewer using this selection order:
1. Bundled script with automatic Claude-first, self-last provider selection
2. A fresh-context Codex reviewer that did not implement the change

If neither path is available, stop and escalate to the user.

## Reviewer Selection Order

When a review or audit is required, use this exact fallback chain:

1. **Bundled script first.** Let the bundled script try Claude, then another model
   family, and keep the current model family last. The script validates the artifact
   contract before accepting the generated artifact.
2. **Fresh-context Codex next.** Spawn a reviewer agent with fresh context. That
   agent must:
   - not have authored or edited the implementation under review
   - receive only the task spec, relevant diff/module/tests, and the bundled references
   - act only as reviewer/auditor, not as implementer
   - write its result to a markdown artifact under `.agents/reviews/`
3. **Escalate** if no independent reviewer is available.

Treat fallback artifacts exactly like script-generated `REVIEW_FILE` or
`REPORT_FILE` outputs in the loops below. Call out fallback usage in the handoff so
humans know whether the review came from Claude, Gemini, Codex, or fresh-context Codex.

---

## Skill Invocation Reference

### Pre-Review: Impact Analysis with Codanna (Optional)

Before requesting code review, you can use codanna to understand the blast radius
of your changes. This provides grounded structural data that helps scope the review
and catch issues the diff alone won't reveal.

```bash
# What calls the functions you changed?
codanna mcp find_callers process_request --watch

# What's the full impact if this symbol changes?
codanna mcp analyze_impact DatabaseConnection --watch --json

# Feed impact data into review context
IMPACT=$(codanna mcp analyze_impact "$CHANGED_SYMBOL" --watch --json 2>/dev/null)
```

This is optional — agent-loops works without codanna. But when available, impact data
makes reviews more precise and catches downstream breakage the diff doesn't show.

### `specialist-review` — Request Code Review

**When:** After completing implementation, after each remediation cycle.
**What you get back:** Findings with severity levels (P0-P3) and a verdict (BLOCKED / PASS WITH ISSUES / CLEAN).

#### IMPORTANT: Do Not Review the Code Yourself

Your ONLY job is to invoke an independent reviewer and read the output artifact. Do
NOT analyze the diff as the reviewer. Do NOT write review comments yourself. Do NOT
adopt perspectives yourself. Route the review to Claude first, then fallback if needed.

Claude is still the preferred reviewer because it can load domain-specific skills such as
`owasp-top-10`, `secure-coding-practices`, and `python-testing-patterns`. The bundled
script now tries Claude first, then a different model family, and keeps same-model
shell-outs for last resort. Codex and Gemini are both available as explicit providers.
If the automated providers are unavailable or fail, continue with a fresh-context Codex
reviewer instead of reviewing the code yourself.

#### Automated Path: Provider-Aware Script

```bash
# Review only the files you changed (RECOMMENDED)
"$SKILL_DIR/scripts/specialist-review.sh" --git -- src/parser/ src/auth.rs

# Review changes since a specific ref, scoped to a directory
"$SKILL_DIR/scripts/specialist-review.sh" --git origin/main -- claude_ctx_py/

# Review all changes vs last commit (use sparingly in monorepos)
"$SKILL_DIR/scripts/specialist-review.sh" --git

# Pipe in a pre-filtered diff
git diff HEAD~3..HEAD -- src/ | "$SKILL_DIR/scripts/specialist-review.sh" -

# Review a diff file
"$SKILL_DIR/scripts/specialist-review.sh" /path/to/changes.diff

# Custom output directory
"$SKILL_DIR/scripts/specialist-review.sh" --git --output ./my-reviews -- src/

# Force Gemini CLI for this run
"$SKILL_DIR/scripts/specialist-review.sh" --provider gemini --git -- src/parser/

# Force Codex CLI for this run
"$SKILL_DIR/scripts/specialist-review.sh" --provider codex --git -- src/parser/
```

Read the output file path printed to stdout:
```bash
REVIEW_FILE=$("$SKILL_DIR/scripts/specialist-review.sh" --git -- src/parser/)
cat "$REVIEW_FILE"
```

**Always scope to the files you touched.** In a monorepo, an unscoped `--git` sends
the entire repo diff to the reviewer, wasting tokens and risking timeouts.

Provider selection:

- Default is `auto`, which tries Claude first, keeps the current agent's own model
  family last, and uses the remaining provider in between.
- Override per run with `--provider auto|claude|gemini|codex`.
- Override by environment with `AGENT_LOOPS_LLM_PROVIDER` or `SPECIALIST_REVIEW_PROVIDER`.
- Set `AGENT_LOOPS_SELF_PROVIDER=claude|gemini|codex` when the current agent is not
  auto-detected. Codex sessions auto-detect themselves already.
- The script validates the review artifact shape before accepting it; invalid provider output is rejected and the next fallback is tried.
- If both CLIs are unavailable or fail, use the fresh-context Codex fallback below.

#### Manual Fallback: Fresh-Context Codex

If the bundled script cannot get a usable artifact from any scripted provider:

1. Generate the same scoped diff you would have sent to the script.
2. Provide the reviewer:
   - `references/review-prompt.md`
   - `references/perspective-catalog.md`
   - the scoped diff
   - the prior review artifact, if this is a remediation cycle
3. Require the reviewer to emit markdown that follows the `Review Output Format`
   documented later in this skill.
4. Save that output under `.agents/reviews/review-<timestamp>-fallback.md` and treat
   the saved path as `REVIEW_FILE`.

#### Anti-Patterns

- **Performing the review yourself** — Use an independent reviewer, never the implementer.
- **Summarizing the diff before invoking the script** — Unnecessary. The script reads the diff directly.
- **Ignoring the output artifact** — The review is written to a file. Read it.
- **Using a same-context Codex agent as reviewer** — If Codex is the fallback reviewer, it must have fresh context and no implementation authorship.
- **Stopping at the first Claude failure** — Let the script try the non-self provider before the same-model last resort and fresh-context Codex.

### `test-review-request` — Request Test Audit

**When:** Initial audit (before writing tests) and re-audit (after writing/fixing tests).
**What you get back:** A gap report covering both missing coverage AND test quality issues (mirror tests, flaky assertions, etc.), with P0/P1/P2 severity.

#### IMPORTANT: Do Not Audit the Tests Yourself

Your ONLY job is to invoke an independent auditor and read the output artifact. Do
NOT map behaviors yourself. Do NOT classify test coverage yourself. Do NOT produce
the gap report yourself. Route the audit to Claude first, then fallback if needed.

Claude is still the preferred auditor because it can apply the testing standards and audit
workflow with project-aware skill support. The bundled script now tries Claude first,
then a different model family, and keeps same-model shell-outs for last resort. Codex
and Gemini are both available as explicit providers. If the automated providers are
unavailable or fail, continue with a fresh-context Codex auditor instead of skipping
the audit.

#### Automated Path: Provider-Aware Script

```bash
# Full audit of a module (default — reads ALL source files)
"$SKILL_DIR/scripts/test-review-request.sh" /path/to/module

# Audit only changed files in a module (RECOMMENDED for large modules)
"$SKILL_DIR/scripts/test-review-request.sh" /path/to/module --git

# Audit changed files since a specific ref
"$SKILL_DIR/scripts/test-review-request.sh" /path/to/module --git origin/main

# Audit changed files with additional path filters
"$SKILL_DIR/scripts/test-review-request.sh" /path/to/module --git -- src/parser/ src/auth.py

# Full audit with specific test directory
"$SKILL_DIR/scripts/test-review-request.sh" /path/to/module --tests /path/to/tests

# Quick review of specific test files only
"$SKILL_DIR/scripts/test-review-request.sh" --quick /path/to/test_file.py

# Custom output directory
"$SKILL_DIR/scripts/test-review-request.sh" /path/to/module --output ./my-reports

# Force Gemini CLI for this run
"$SKILL_DIR/scripts/test-review-request.sh" --provider gemini /path/to/module

# Force Codex CLI for this run
"$SKILL_DIR/scripts/test-review-request.sh" --provider codex /path/to/module
```

Read the output file path printed to stdout:
```bash
REPORT_FILE=$("$SKILL_DIR/scripts/test-review-request.sh" src/parser)
cat "$REPORT_FILE"
```

Provider selection:

- Default is `auto`, which tries Claude first, keeps the current agent's own model
  family last, and uses the remaining provider in between.
- Override per run with `--provider auto|claude|gemini|codex`.
- Override by environment with `AGENT_LOOPS_LLM_PROVIDER` or `TEST_REVIEW_PROVIDER`.
- Set `AGENT_LOOPS_SELF_PROVIDER=claude|gemini|codex` when the current agent is not
  auto-detected. Codex sessions auto-detect themselves already.
- The script validates the audit artifact shape before accepting it; invalid provider output is rejected and the next fallback is tried.
- If both CLIs are unavailable or fail, use the fresh-context Codex fallback below.

#### Manual Fallback: Fresh-Context Codex

If the bundled script cannot get a usable artifact from any scripted provider:

1. Gather the same source, tests, and bundled references the script would have used.
2. Provide the auditor:
   - `references/audit-prompt.md`
   - `references/testing-standards.md`
   - `references/audit-workflow.md`
   - the scoped module and test content
3. Require the auditor to emit markdown that follows the same gap-report contract
   used by this skill's audit loop.
4. Save that output under `.agents/reviews/test-audit-<timestamp>-fallback.md` and
   treat the saved path as `REPORT_FILE`.

Act on findings:
- **P0 (Security/Correctness Critical)**: Fix before merge.
- **P1 (Reliability/Edge Cases)**: Fix in current sprint.
- **P2 (Completeness/Confidence)**: Backlog.

#### Anti-Patterns

- **Performing the audit yourself** — Use an independent auditor, never the implementer.
- **Pre-reading source before invoking the script** — Unnecessary. The script passes the module path to the provider flow.
- **Ignoring the output artifact** — The gap report is written to a file. Read it.
- **Using a same-context Codex agent as auditor** — If Codex is the fallback auditor, it must have fresh context and no authorship of the tested change.
- **Proceeding without any audit artifact** — Let the script try the non-self provider before the same-model last resort and fresh-context Codex.

---

## Atomic Commits: The Unit of Work

Every loop operates on **atomic commits**, not features. An atomic commit is the
smallest change that is complete, correct, and reviewable in isolation.

### What Makes a Commit Atomic

An atomic commit:
- **Does one thing.** One bug fix, one new behavior, one refactor — not all three.
- **Is self-consistent.** The codebase compiles, tests pass, and lint is clean at this commit. You could revert it without breaking other commits.
- **Is reviewable in isolation.** A reviewer can understand the intent and evaluate correctness without seeing what comes next.
- **Groups related files.** If adding a function requires updating a test and a type — that's one commit, not three.

An atomic commit is NOT:
- An entire feature with multiple independent components.
- A single file (if the logical change spans several files).
- "Everything I did today."

### How This Drives the Loops

For a multi-component feature, decompose into a sequence of atomic commits.
Each commit gets its own pass through the relevant loop:

```
Feature: "Add rate limiting to API"

  Commit 1: rate limiter data model       → Code Change Loop → commit
  Commit 2: rate limiter business logic    → Code Change Loop → commit
  Commit 3: integrate into request handler → Code Change Loop → commit
  Commit 4: tests for rate limiter         → Test Writing Loop → commit
  Commit 5: lint fixes                     → Lint Gate → commit
```

The question at every step is: **"What is my next atomic commit?"** — not
"How do I implement this feature?"

### Commit Rules

1. **Use `committer`, not `git commit`.** Unless you have explicit user approval
   to commit another way, always use the `committer` tool. It prevents common
   mistakes (staging `.`, empty messages, committing directories).
   ```bash
   committer "fix(parser): reject CONNECT requests with missing port" src/parser.rs tests/test_parser.rs
   ```
2. **Commit at the end of every loop.** Each loop exit (code change, test writing,
   lint gate) produces a commit. Do not batch multiple loop exits into one commit.
3. **Run existing tests before committing.** After implementation, after lint fixes,
   after any code change — verify the existing test suite passes. A commit that
   breaks existing tests is not atomic.
4. **Commit messages follow Conventional Commits.** `<type>(scope): <summary>`.
   The summary should describe *what changed*, not *what you were asked to do*.

### When to Split

If you find yourself in any of these situations, you need to split:
- Your diff touches more than one module for unrelated reasons.
- You're fixing a bug AND adding a feature in the same change.
- The review would need to evaluate two independent design decisions.
- You can describe your change only with "and" — "adds X **and** changes Y."

---

## Overview

There are three primary loops. They run sequentially — code loop, then test loop, then lint gate.

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
├─────────────────────────────────────────────────────────────────┤
│                        LINT GATE                                │
│  Discover Linter → Auto-fix → Check → Remediate → Re-check    │
│  Exit: zero errors, no new warnings                             │
│  Output: lint-clean code                                        │
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
ENTRY: Next atomic commit from your decomposition plan.
       (One logical change — see "Atomic Commits" above.)

┌──────────────────┐
│  IMPLEMENT       │ ← You (Codex/Gemini): write ONE atomic commit's worth of change
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ specialist-review│ ← Run: "$SKILL_DIR/scripts/specialist-review.sh" --git -- <files>
└──────┬───────────┘   Claude script first; fallback reviewer uses the same scoped diff
       │
       ├── Findings? ──► Yes ──► Any P0 or P1? ──► Yes ──┐
       │                                                   │
       │                        No ──► File P2/P3 issues   │
       │                               Run tests ──► Pass? │
       │                               Commit (committer)  │
       │                               Exit loop           │
       │                                                   │
       │   No findings ──► Run tests ──► Pass?             │
       │                   Commit (committer)               │
       │                   Exit loop                        │
       │                                                   │
       ▼                                                   ▼
                                          ┌──────────────────┐
                                          │  REMEDIATE       │ ← You: fix ONLY P0/P1
                                          └──────┬───────────┘   findings cited by the review artifact
                                                 │
                                                 ▼
                                          ┌──────────────────┐
                                          │ specialist-review│ ← Run with --prior-review and only remediated files:
                                          └──────┬───────────┘   "$SKILL_DIR/scripts/specialist-review.sh" --git \
                                                 │                 --prior-review "$REVIEW_FILE" -- <remediated-files>
                                                 └── Loop back to findings check
```

### Circuit Breaker

**Maximum iterations: 3 `specialist-review` cycles.**

If P0/P1 findings remain after 3 cycles:
1. Stop. Do not attempt a 4th remediation.
2. Produce a summary of unresolved findings with context on why they persist.
3. Escalate to human reviewer with the summary and the latest review artifact.

This prevents infinite loops when you keep introducing new issues while fixing old ones, or when a finding requires a design-level change you can't make in remediation scope.

### Code Review Checklist (Reviewer Criteria)

Any reviewer evaluates against these criteria. Use them to anticipate and prevent
issues before review, and to interpret findings during remediation.

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

### Review Output Format (What the Reviewer Returns)

All review paths must produce this format. Parse it to determine your next action.

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

When fixing findings from the review artifact:
- Fix ONLY the cited findings. Do not refactor adjacent code.
- Do not introduce new functionality while remediating.
- If a fix requires changing the approach significantly, note this in the remediation and let the next reviewer evaluate the full new approach on the next review cycle.
- Each remediated finding should be annotated: `Fixed P0-001: [what was changed]`
- **Scope remediation reviews to only the files you touched.** Pass `--prior-review "$REVIEW_FILE"` when using Claude, or provide the prior artifact when using a fallback reviewer, so the next review can verify fixes and check for regressions without re-reviewing already-approved code:
  ```bash
  # Initial review — full scope
  REVIEW_FILE=$("$SKILL_DIR/scripts/specialist-review.sh" --git -- src/parser/ src/auth.rs)

  # Remediation review — only the files you fixed, with prior review for continuity
  REVIEW_FILE=$("$SKILL_DIR/scripts/specialist-review.sh" --git --prior-review "$REVIEW_FILE" -- src/auth.rs)
  ```
- If you disagree with a finding, see "Disagreeing with Review Findings" below — do not silently skip it.

---

## Loop 2: Test Writing Loop

This loop runs after the code change loop exits cleanly. It ensures the new (and existing) code has adequate test coverage.

The audit does double duty: it finds missing coverage AND flags bad tests (mirror tests, flaky assertions, etc.). A bad test doesn't close a gap, so a single audit pass catches both problems. No separate quality review step needed.

### Roles

| Role | Agent | Skill |
|------|-------|-------|
| **Auditor** | Claude preferred; non-self scripted fallback next; same-model provider last; fresh-context Codex final fallback | `test-review-request` keeps same-model shell-outs last; fallback auditor uses bundled references and writes an artifact |
| **Test Writer** | Codex or Gemini | Writes tests per `references/testing-standards.md` standards |

### Pragmatic Enforcement Policy

Use a hybrid gate to avoid unnecessary friction while preserving confidence:

- **Non-trivial code changes (default):** The test-writing loop is required. Do not close the loop without audit evidence from `test-review-request` or a fallback audit artifact, and a re-audit state with no unresolved P0/P1 gaps.
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
│  AUDIT               │ ← Run: "$SKILL_DIR/scripts/test-review-request.sh" <module>
└──────┬───────────────┘   Claude script first; fallback auditor uses the same scoped materials
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
└──────┬───────────────┘   1. Compile / pass lint (test files — full lint in Loop 3)
       │                   2. All pass (no test is born failing)
       │                   3. Actually exercise the code (not no-ops)
       ▼
┌──────────────────────┐
│  RE-AUDIT            │ ← Run: "$SKILL_DIR/scripts/test-review-request.sh" <module>
└──────┬───────────────┘   Same module path — script re-reads source + tests
       │                   Reviewer checks: gaps closed? new tests good?
       │
       ├── All P0/P1 resolved? ──► Yes ──► File P2/P3 issues
       │                                   Run full test suite
       │                                   Commit (committer)
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

If Claude was unavailable for one or more audit cycles, include that fact in the
summary so humans know the audit path used.

---

## Loop 3: Lint Gate

After the test writing loop exits cleanly, run the project linter against ALL files touched across both loops. Lint fixes are code changes — they may produce deferred findings or break tests — so the lint gate runs before issue filing.

### Linter Discovery

Discover the project's linter using this cascade. Stop at the first match:

1. **Project docs** — Check `CLAUDE.md`, `README.md`, and `CONTRIBUTING.md` for lint commands or conventions.
2. **Task runner targets** — Look for standard targets: `make lint`, `npm run lint`, `cargo clippy`, `./gradlew lint`, `bundle exec rubocop`, etc.
3. **Config file inference** — Match config files to linters:
   - `.eslintrc*` / `eslint.config.*` → `npx eslint`
   - `pyproject.toml [tool.ruff]` → `ruff check`
   - `pyproject.toml [tool.black]` → `black --check`
   - `.prettierrc*` → `npx prettier --check`
   - `Cargo.toml` → `cargo clippy`
   - `.rubocop.yml` → `bundle exec rubocop`
   - `.golangci.yml` → `golangci-lint run`
   - `biome.json` → `npx biome check`
4. **Fallback** — If no linter is discoverable, escalate to the user. **Never guess.**

### The Loop

```
ENTRY: Test writing loop has exited cleanly.

┌──────────────────────┐
│  DISCOVER LINTER     │ ← You: use the 4-step cascade above
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  AUTO-FIX            │ ← You: run linter's auto-fix command (see table below)
└──────┬───────────────┘   Eliminates 80%+ of issues without iteration cost
       │
       ▼
┌──────────────────────┐
│  LINT CHECK          │ ← You: run lint check command
└──────┬───────────────┘
       │
       ├── Clean? ──► Yes ──► Run full test suite ──► Pass?
       │                      Commit (committer)
       │                      Exit loop ✅
       │
       └── No ──► Errors or new warnings remain
                  │
                  ▼
           ┌──────────────────┐
           │  REMEDIATE       │ ← You: manually fix remaining lint issues
           └──────┬───────────┘
                  │
                  ▼
           ┌──────────────────┐
           │  VERIFY TESTS    │ ← You: re-run tests to confirm lint fixes
           └──────┬───────────┘   didn't break anything
                  │
                  └── Back to LINT CHECK
```

### What "Clean" Means

- **Zero errors** from the project linter.
- **No new warnings** introduced by your changes.
- Pre-existing warnings in unmodified files are noted but not blocking.

### Auto-fix Reference

| Linter | Check Command | Auto-fix Command |
|--------|--------------|-----------------|
| ESLint | `npx eslint .` | `npx eslint . --fix` |
| Ruff | `ruff check .` | `ruff check . --fix` |
| Black | `black --check .` | `black .` |
| Prettier | `npx prettier --check .` | `npx prettier --write .` |
| Clippy | `cargo clippy` | `cargo clippy --fix --allow-dirty` |
| RuboCop | `bundle exec rubocop` | `bundle exec rubocop -A` |
| golangci-lint | `golangci-lint run` | `golangci-lint run --fix` |
| Biome | `npx biome check .` | `npx biome check . --fix` |
| rustfmt | `cargo fmt --check` | `cargo fmt` |
| gofmt | `gofmt -l .` | `gofmt -w .` |

### Auto-fix Rules

1. **Always auto-fix before manual remediation.** Auto-fix eliminates the mechanical majority.
2. **Re-run tests after auto-fix.** If auto-fix breaks tests, revert the auto-fix and remediate manually.
3. **Revert if auto-fix breaks tests.** A passing test suite takes priority over lint cleanliness.

### Circuit Breaker

**Maximum iterations: 2 lint-check cycles** (initial check + 1 re-check after remediation).

Lint is mechanical, not semantic. If you can't get clean in 2 cycles, the issue is either a misconfigured rule or a design problem:
1. Stop. Do not attempt a 3rd remediation.
2. Summarize unresolved lint errors with context on why they persist.
3. Escalate to human reviewer with the summary.

### Severity Model

Lint findings use a **binary pass/fail** model — no P0/P1/P2 triage. Lint rules are team policy: the agent complies, it doesn't judge. If a rule seems wrong, escalate to the user rather than disabling or ignoring it.

---

## Loop 4: Issue Filing

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
- Decomposing the task into atomic commits (one logical change each)
- Writing implementation code — one atomic commit at a time
- Writing test code
- Running the full test suite before every commit
- Using `committer` for all commits (not `git commit`) unless explicitly approved otherwise
- Committing at the end of every loop exit (code change, test writing, lint gate)
- Running `"$SKILL_DIR/scripts/specialist-review.sh" --git -- <your-files>` after implementation; on remediation cycles, scope to remediated files and pass `--prior-review "$REVIEW_FILE"`
- Running `"$SKILL_DIR/scripts/test-review-request.sh" <module>` for initial audit and each re-audit
- Preserving fallback review/audit artifacts in `.agents/reviews/` when Claude is unavailable
- Falling back to another model family before the same-model last resort when Claude is unavailable
- Fixing ONLY the findings the independent review/audit artifact identifies (no scope creep during remediation)
- Discovering and running the project linter after both loops exit
- Running auto-fix first, then manually fixing remaining lint issues
- Verifying tests still pass after lint fixes
- Escalating if lint cannot be resolved in 2 cycles
- Filing P2/P3 issues when loop exits
- Escalating when circuit breaker triggers

**You are NOT responsible for:**
- Reviewing your own code (an independent reviewer does this)
- Judging your own test coverage or quality (an independent auditor does this)
- Deciding whether a finding is valid (if you disagree, note it in the remediation and let the next review re-evaluate — do not silently skip findings)

### Disagreeing with Review Findings

If the reviewer flags something you believe is incorrect:
1. Do NOT silently ignore the finding.
2. In your remediation response, explicitly state: `Disputed P1-003: [your reasoning]`
3. Run the next review pass with the dispute noted in your commit/changes or fallback review materials.
4. The next review pass will either accept your reasoning or reaffirm the finding with additional context.
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
2. DECOMPOSE into atomic commits
   └── Each commit = one logical change, reviewable in isolation
       │
       ▼
3. FOR EACH atomic commit:
   │
   ├── CODE CHANGE LOOP
   │   ├── You: implement ONE commit's worth of change
   │   ├── specialist-review → Claude reviews diff, else non-self provider, else same-model last resort, else fresh-context Codex (max 3 cycles)
   │   ├── You: remediate P0/P1 → re-review with prior artifact
   │   ├── File issues for P2/P3
   │   ├── Run tests → Pass?
   │   └── committer "type(scope): summary" <files>
   │       │
   │   ├── TEST WRITING LOOP
   │   │   ├── test-review-request → Claude audits, else non-self provider, else same-model last resort, else fresh-context Codex
   │   │   ├── Human: scope approval (P0/P1 auto-approved)
   │   │   ├── You: write tests (testing-standards.md)
   │   │   ├── You: verify tests pass locally
   │   │   ├── test-review-request → re-audit using the same reviewer chain (max 3 cycles)
   │   │   ├── You: remediate P0/P1 gaps and bad tests
   │   │   ├── File issues for P2/P3
   │   │   ├── Run full test suite → Pass?
   │   │   └── committer "test(scope): summary" <files>
   │   │       │
   │   └── LINT GATE
   │       ├── You: discover project linter
   │       ├── You: run auto-fix if available
   │       ├── You: run lint check (max 2 cycles)
   │       ├── You: remediate remaining issues
   │       ├── Run full test suite → Pass?
   │       └── committer "style(scope): summary" <files>
   │
   └── Next atomic commit (back to step 3)
       │
       ▼
4. ISSUE FILING
   └── P2/P3 findings → tracked issues
       │
       ▼
5. PR READY FOR HUMAN REVIEW
```
