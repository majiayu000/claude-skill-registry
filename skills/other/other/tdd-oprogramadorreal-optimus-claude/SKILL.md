---
description: Guides test-driven development — decompose a feature or bug fix into behaviors, then cycle through Red (failing test) → Green (minimal implementation) → Refactor for each one. Requires /optimus:init and working test infrastructure. Use when starting a new feature or bug fix with test-first discipline.
disable-model-invocation: true
---

# Test-Driven Development

Guide the user through Red-Green-Refactor cycles to implement a feature or fix a bug test-first. Each cycle: write a failing test (Red), write the minimum code to pass it (Green), clean up while tests stay green (Refactor). One behavior per cycle.

This skill is for **new features** and **bug fixes** — not refactoring. For restructuring existing code without changing behavior, use `/optimus:refactor` instead (existing tests verify behavior is preserved).

### The Iron Law

**No production code without a failing test first.** If implementation code is written before its test, delete it entirely and begin the cycle fresh. Do not preserve it as reference, do not adapt it — write the implementation from scratch once the failing test exists. This is the non-negotiable foundation of every step that follows.

## Step 1: Pre-flight

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected, process each repo independently: run Steps 1–9 inside the repo the user is targeting. If ambiguous, ask which repo.

### Verify prerequisites

Check that `.claude/CLAUDE.md` exists. If it doesn't, stop and recommend running `/optimus:init` first — coding guidelines and project context are essential for the Refactor step.

Load these documents (they affect quality at every step):

| Document | Role | Effect on skill |
|----------|------|-----------------|
| `.claude/CLAUDE.md` | Project overview | Tech stack, test runner command |
| `coding-guidelines.md` | Code quality reference | Applied during Refactor step |
| `testing.md` | Testing conventions | Test file location, naming, framework, mocking patterns |

**Monorepo path note:** Read the "Monorepo Scoping Rule" section of `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md` for doc layout and scoping rules. When running TDD inside a subproject, load that subproject's `testing.md`, not another subproject's.

### Verify test infrastructure

Locate the test runner command from `testing.md`, `CLAUDE.md`, or project manifests (`package.json` scripts, `Makefile`, `Cargo.toml`, etc.). Run it once to confirm it works.

- **Tests pass** — proceed to Step 2 (Suitability Analysis)
- **Tests fail** — stop and report. Existing failures must be resolved before TDD can begin (a failing suite makes Red/Green indistinguishable)
- **No test runner found** — stop and recommend running `/optimus:init` first to set up test infrastructure (framework, runner, coverage tooling, `testing.md`)

## Step 2: Suitability Analysis

Before starting TDD cycles, analyze whether the user's task is a good fit for test-driven development.

### Gather the task

**Context detection** (runs before the task-gathering prompts below — first match wins):

1. **Explicit reference** — if the user's input references a file path ending in `.md` inside `docs/design/` or `docs/jira/`, read that file and use its Goal section as the task description. Proceed to distillation below if the goal is longer than 2-3 sentences.

2. **Design doc auto-discovery** — if no explicit reference but `docs/design/` exists with `.md` files, check the most recent one (by filename date prefix). If its date is within the last 7 days, mention it: "Found design doc `<path>` — use it as the basis for TDD?" via `AskUserQuestion` — header "Design doc", options "Use it" / "Ignore — describe a different task". If its date is older than 7 days, add a note: "(This design doc is [N] days old — you may want to re-run `/optimus:brainstorm` for a fresh design.)" Design docs contain full approach details from `/optimus:brainstorm` — use Goal, Components, and Interfaces sections as the task description.

3. **JIRA context auto-discovery** — if no design doc found (or user ignored it) but `docs/jira/` exists with `.md` files, read each file's YAML frontmatter and select the one with the most recent `date` field. If its date is within the last 7 days, mention it: "Found JIRA context `<path>` — use it as the basis for TDD?" via `AskUserQuestion` — header "JIRA context", options "Use it" / "Ignore — describe a different task". If its date is older than 7 days, add a note: "(This context is [N] days old — you may want to re-run `/optimus:jira` for fresh data.)" JIRA context provides Goal and Acceptance Criteria as the task description.

4. **No context found** — proceed with normal task gathering below.

Design docs take priority over JIRA files because they are more detailed (they incorporate JIRA context if brainstorm consumed it). Detected context feeds into the existing task-gathering cascade below — it does NOT bypass Step 3 decomposition. TDD still independently decomposes the goal into behaviors.

If context detection above resolved a task description (user accepted a design doc or JIRA context), use it — skip the inline/prompt gathering below. Otherwise, if the user provided a task description inline (e.g., `/optimus:tdd "Add auth endpoint"`), use it. Otherwise, use `AskUserQuestion` — header "TDD scope", question "What feature or bug fix do you want to implement with TDD?":
- **New feature** — "Implement a new capability (e.g., 'Add user authentication endpoint')"
- **Bug fix** — "Fix a bug by reproducing it with a test first (e.g., 'Login fails when email has uppercase')"

If the task description is longer than ~2-3 sentences (e.g., a pasted spec, JIRA ticket, or acceptance criteria list), distill it into a **single-sentence goal** and confirm with `AskUserQuestion` — header "Distilled goal", question "I've distilled your spec to: '[single-sentence summary]'. Is this accurate?":
- **Looks good** — "Proceed with this goal"
- **Adjust** — "Let me refine the focus"

### Analyze suitability

Examine the task description against the codebase and classify it:

**Suitable for TDD** — proceed silently to Step 3:
- New features with testable behavior (API endpoints, business logic, data transformations, utilities)
- Bug fixes where the bug can be reproduced with a test
- Adding capabilities to existing modules
- Large features (frontend + backend, multi-component) — these are suitable but need careful decomposition in Step 3

**Not suitable for TDD** — stop and redirect:
- **Refactoring** (restructuring code without changing behavior) → recommend `/optimus:refactor`
- **Documentation-only changes** (README, comments, CLAUDE.md) → no testable code
- **Pure styling/cosmetic changes** (CSS colors, spacing, fonts with no logic) → no testable logic
- **Configuration changes** (environment variables, CI/CD, linter config) → no testable behavior
- **Deleting code/features** without replacement → tests should be removed, not added
- **Generated code** (protobuf, OpenAPI, ORM migrations) → generated output, not hand-written behavior

If **not suitable**, report to the user:

```
## Task Analysis

**Task:** [user's description]
**Suitability for TDD:** Not recommended

**Reason:** [specific explanation — e.g., "This is a refactoring task — it changes code structure
without adding new behavior. TDD is for building new behavior test-first."]

**Recommended approach:** [specific skill or approach — e.g., "/optimus:refactor restructures code
while using existing tests as a safety net."]
```

If **ambiguous** (the task has both testable and non-testable aspects, or it's unclear whether behavior changes), use `AskUserQuestion` — header "TDD fit", question "[specific concern about the task]. Proceed with TDD or use a different approach?":
- **Proceed with TDD** — "Focus on the testable parts and continue"
- **Use [recommended alternative]** — "[brief explanation of why the alternative fits better]"

## Step 3: Scope and Decompose

### Create feature branch

Always create a new branch from the current branch for TDD work. This keeps the user's original branch clean — all changes happen on the new branch.

1. Record the current branch name (this becomes the PR/MR target later): `git rev-parse --abbrev-ref HEAD`
2. Derive a branch name from the task description. Read `$CLAUDE_PLUGIN_ROOT/skills/commit/references/branch-naming.md` for the naming convention. The `<type>` is `feat` for new features or `fix` for bug fixes (from the task classification in Step 2). The `<description>` is the slugified task description.
3. Create and switch to the branch: `git checkout -b <branch-name>`
4. Report the branch name to the user:

```
## Branch

Created branch `<branch-name>` from `<original-branch>`.
All TDD work will be committed to this branch.
```

### Worktree isolation (optional)

Read `$CLAUDE_PLUGIN_ROOT/skills/tdd/references/tdd-worktree-orchestration.md` and follow the **Setup** section, using `<branch-name>` and `<original-branch>` from above.

### Decompose into behaviors

Break the user's description into small, individually testable behaviors. Each behavior should be:
- **Observable** — has a clear expected output or side effect; phrase as "When [input/action], then [outcome]" so success criteria are unambiguous (e.g., "handle errors" becomes "When the API returns 404, then return null and log a warning")
- **Independent** — it can be tested and implemented without the other behaviors being done yet
- **Small** — one test, one assertion focus (a test may have supporting assertions, but tests one thing)

Decomposition strategies by task type:
- **API endpoints** — one behavior per response scenario (success case, each error code, each validation rule)
- **Business logic** — one behavior per business rule or edge case
- **Bug fixes** — first behavior is always "reproduce the bug" (a test that demonstrates the current broken behavior)
- **Data transformations** — one behavior per transformation step or boundary (empty input, boundary values, malformed data)

If the decomposition produces more than 10 behaviors, split into milestones. Present the first milestone (~5-8 behaviors that deliver a coherent slice of functionality) as the current scope, and list remaining behaviors as "Future milestones" with brief descriptions. After completing the last behavior of the current milestone, use `AskUserQuestion` — header "Milestone complete", question "Milestone [N] is done ([N] behaviors). Continue to the next milestone?":
- **Next milestone** — "Load the next milestone's behaviors for approval"
- **Stop here** — "Done for now — show summary"

If the user chooses to continue, present the next milestone's behaviors for approval (return to the "Behaviors" confirmation above), then resume Step 4. This prevents overwhelming behavior lists and gives natural stopping points.

Present the decomposition as a numbered list:

```
## Behaviors to Implement

1. [Behavior description] — [what the test will verify]
2. [Behavior description] — [what the test will verify]
3. [Behavior description] — [what the test will verify]
...
```

Use `AskUserQuestion` — header "Behaviors", question "Does this decomposition look right? Adjust, reorder, or approve to start cycling.":
- **Start cycling** — "Looks good — begin Red-Green-Refactor with behavior #1"
- **Adjust** — "I want to modify the list before starting"

For **bug fixes**: the first behavior is always "reproduce the bug" — a test that demonstrates the current broken behavior.

## Step 4: Red — Write a Failing Test

For the current behavior, write a minimal test that:
- Follows the project's testing conventions from `testing.md` (framework, file location, naming, mocking patterns)
- Tests exactly one behavior — clear expected input and output
- Uses descriptive test names that read as behavior specifications (e.g., `"returns 401 when token is expired"`, not `"test auth"`)
- Avoids common testing anti-patterns — read `$CLAUDE_PLUGIN_ROOT/skills/tdd/references/testing-anti-patterns.md` before writing mocks; prefer real code over mocks, never assert on mock behavior, mock only external services or non-deterministic dependencies

Place the test file according to the project's convention (from `testing.md`). If adding to an existing test file, append; if the convention calls for a new file, create one.

### Run the test suite

**Verification protocol** — every test run in this skill (Steps 4, 5, 6) must follow the gate function in `$CLAUDE_PLUGIN_ROOT/skills/init/references/verification-protocol.md`: identify the command, run it fresh, read complete output, verify the claim matches the evidence, only then report. Never claim "should pass" or "probably works" — state the actual result with evidence (e.g., "14 passed, 1 failed"). This protocol applies to every "Run the test suite" instruction below.

Run the project's test command. The new test **must fail**. Verify:

- **Test fails for the right reason** — the assertion fails because the behavior isn't implemented yet (not because of a syntax error, import error, or infrastructure problem)
- **All other tests still pass** — the new test didn't break existing tests

If the test **passes unexpectedly**, the behavior may already be implemented. Use `AskUserQuestion` — header "Test passed", question "The test passed without new code. The behavior may already exist. How to proceed?":
- **Skip this behavior** — "Move to the next behavior in the list"
- **Strengthen the test** — "Add edge cases or stricter assertions to find the real gap"
- **Investigate** — "Check if the behavior is truly complete or accidentally passing"

If the test **fails for the wrong reason** (import error, missing dependency, syntax error), fix the test — not the source code. The test itself must be valid; only the assertion should fail.

Report to the user:

```
## 🔴 Red — [Behavior description]

Test: [test file path]:[test name]
Status: FAILS ✓ (expected)
Reason: [why it fails — e.g., "function returns undefined, expected 'authenticated'"]
Other tests: all passing ✓
```

## Step 5: Green — Minimal Implementation

Write the **minimum code** to make the failing test pass. Resist the urge to implement more than what the test demands:
- No handling of edge cases that aren't tested yet (those are future behaviors)
- No premature abstractions or "while I'm here" improvements
- If a hardcoded return value passes the test, that's valid — later tests will force generalization

### Run the test suite

Run the project's test command. **All tests must pass** — including the new one.

- **All pass** — proceed to lint/type-check below
- **New test still fails** — fix the implementation (not the test). The test defines the expected behavior; the code must meet it
  - **Circuit breaker** — if the test still fails after 3 implementation attempts, stop. Use `AskUserQuestion` — header "Implementation stuck", question "The test has failed after 3 fix attempts. This usually signals a design problem, not a code problem. How to proceed?":
    - **Rethink the approach** — "Step back and reconsider the behavior's design or decomposition"
    - **Simplify the behavior** — "Break this behavior into smaller, simpler sub-behaviors"
    - **Skip for now** — "Revert implementation changes from this cycle (`git checkout -- <implementation files>`), mark the test as skipped per the project's convention (e.g., `skip`/`xit`/`@pytest.mark.skip`), move to the next behavior"
- **Other tests broke** — the implementation introduced a regression. Fix it before proceeding — all tests must stay green

### Bug-fix regression gate

**When:** the current behavior is a bug reproduction (the first behavior in a bug-fix decomposition). **Skip** for regular feature behaviors.

This gate proves two things: (1) the test genuinely catches the bug, and (2) the fix genuinely resolves it. Without this, you may have a test that passes regardless of the fix — providing false confidence.

1. **Commit the test** separately: `git add <test-file> && git commit -m "test: reproduce <bug-description>"`
2. **Revert only the fix**: `git stash push <implementation-files>`
3. **Run the test** — it **must fail**. This proves the test catches the bug.
4. **Restore the fix**: `git stash pop`
5. **Run the test again** — it **must pass**. This proves the fix resolves the bug.

Report:

```
## 🔒 Regression Gate — [Bug description]

Test: [test file path]:[test name]
Without fix: FAILS ✓ (test catches the bug)
With fix: PASSES ✓ (fix resolves the bug)
Verdict: REGRESSION GATE PASSED
```

If the test **passes with the fix reverted** (step 3), the test is not actually catching the bug. Restore the fix (`git stash pop`), then rewrite the test to target the actual failure condition.

### Lint / type-check (if available)

If a lint or type-check command is configured in `CLAUDE.md` or the project manifest (e.g., `tsc --noEmit`, `cargo check`, `go vet`, `dotnet build`), run it. Type errors in implementation code can hide behind passing tests. If it fails, fix the implementation before proceeding to Step 6.

Report to the user:

```
## 🟢 Green — [Behavior description]

Test: [test file path]:[test name]
Status: PASSES ✓
Implementation: [file path]:[function/method]
All tests: passing ✓
Type-check: passing ✓ [or omit this line if no type-check command is available]
```

## Step 6: Refactor — Clean Up While Green

With all tests passing, review the code just written (both test and implementation) against `coding-guidelines.md`. Apply each principle as a lens — does the new code satisfy the guidelines? If not, refactor.

**Refactoring scope:** Review code written in this TDD session **and** existing code that the new implementation directly interacts with (files it imports, calls, or inherits from). Look for:
- Duplication between new code and existing code in those files — extract a shared abstraction
- An existing method or class that should be adjusted to cleanly accommodate both the old and new usage
- Naming inconsistencies between the new code and the existing code it touches

Stay bounded: only consider files the new code already references — don't search the broader codebase for extraction opportunities and don't restructure code that the current behavior doesn't interact with. Eliminate duplication created by getting the test to work, but don't refactor further than necessary for this session.

Also review the test:
- Is the test name a clear behavior specification?
- Are assertions focused and readable?
- Does it follow `testing.md` conventions?

Make improvements only if they genuinely simplify or clarify. **Do not add features, handle untested edge cases, or "prepare for" the next behavior.**

### Run the test suite

Run the project's test command after every refactoring change. **All tests must remain green.** If any test fails, undo the last refactoring change — the refactoring was incorrect.

If a lint or type-check command was run in Step 5, run it here too — refactoring can introduce lint or type errors that tests don't catch. If it fails, fix the issue before proceeding.

Report to the user:

```
## 🔄 Refactor — [Behavior description]

Changes: [brief description of what was cleaned up, or "No changes needed — code is clean"]
All tests: passing ✓
```

## Step 7: Commit and Loop

After completing one Red-Green-Refactor cycle, automatically commit the work on the feature branch:

1. Stage changes: prefer `git add <specific files>` for the test and implementation files touched in this cycle. Use `git add -A` only if many files were changed (e.g., renames, moves). Never stage files that look like secrets (`.env`, credentials, keys) — warn the user if any appear in `git status`
2. Generate a conventional commit message. Read `$CLAUDE_PLUGIN_ROOT/skills/commit-message/references/conventional-commit-format.md` for the format. The message should cover the behavior just completed
3. Commit: `git commit -m "<message>"`
4. Report the commit:

```
Committed: <short-hash> <commit message>
```

Then, if behaviors remain, use `AskUserQuestion` — header "Next step", question "Cycle complete for behavior #[N]. What next?":
- **Next behavior** — "Continue to behavior #[N+1]: [description]"
- **Stop here** — "Done for now — show summary"

If behaviors remain and the user chooses to continue, return to Step 4 (Red) for the next one.

If no behaviors remain, or the user chooses "Stop here", proceed to Step 8 (Quality Gate).

## Step 8: Quality Gate (parallel agents)

Read these files for the quality gate:
- `$CLAUDE_PLUGIN_ROOT/skills/tdd/agents/shared-constraints.md` — shared constraints for both agents
- `$CLAUDE_PLUGIN_ROOT/skills/tdd/agents/code-simplifier.md` — code-simplifier prompt
- `$CLAUDE_PLUGIN_ROOT/skills/tdd/agents/test-guardian.md` — test-guardian prompt
- `$CLAUDE_PLUGIN_ROOT/skills/tdd/references/quality-gate.md` — execution procedure

Follow the **Execution** section in `quality-gate.md`. Use `<original-branch>` from Step 3 to scope the changed files. When complete, proceed to Step 9.

## Step 9: Summary, Push, and PR/MR

After all behaviors are implemented (or the user stops early):

### Commit remaining work

If there are uncommitted changes (e.g., the user stopped mid-cycle before the auto-commit):
1. Stage the remaining files (prefer `git add <specific files>`; use `git add -A` only if many files changed) and commit: `git commit -m "<conventional message covering remaining work>"`

### Present summary

```
## TDD Summary

### Behaviors Implemented
| # | Behavior | Test | Status |
|---|----------|------|--------|
| 1 | [description] | [test file]:[test name] | ✓ Complete |
| 2 | [description] | [test file]:[test name] | ✓ Complete |
| 3 | [description] | — | ⏸ Not started |

### Stats
- Cycles completed: [N] of [total]
- Tests written: [N]
- Tests passing: all ✓
- Files created: [list new files]
- Files modified: [list modified files]
- Quality gate: code-simplifier ([N] findings), test-guardian ([N] findings)

### Coverage
[Detect coverage command from: testing.md coverage section, test runner built-in flag
(e.g., vitest --coverage, pytest --cov=., go test -cover, dotnet test --collect:"XPlat Code Coverage"),
or package.json coverage script. Run it before the first cycle and after the last cycle to measure delta.
If no coverage command is found, omit this section entirely.]
- Before: [X]%
- After: [Y]%
- Delta: +[Z]%
```

### Push and create PR/MR

If there are commits on the branch:

1. **Push** the feature branch: `git push -u origin <branch-name>`

2. **Detect the hosting platform** — read `$CLAUDE_PLUGIN_ROOT/skills/pr/references/platform-detection.md` and use the **origin URL check** and **CI file fallback** from the **Platform Detection Algorithm**. Skip multi-remote disambiguation — if ambiguous or unknown, skip PR/MR creation, report the push and suggest running `/optimus:pr` to create one

3. **Create a PR/MR** using the Conventional PR format:

   Read `$CLAUDE_PLUGIN_ROOT/skills/pr/references/pr-template.md` for the Conventional PR format. Generate the PR title and body following this template.

   Write the body to a secure temp file: `TMPFILE=$(mktemp "${TMPDIR:-/tmp}/pr-body-XXXXXX.md")`. Clean up after the creation attempt: `rm -f "$TMPFILE"`.

   **GitHub** (requires `gh` CLI):
   - Verify `gh` is available: `gh --version`. If not, skip and tell the user to run `/optimus:pr` to create the PR (it can install the CLI)
   - `gh pr create --title "<conventional title>" --body-file "$TMPFILE" --base <original-branch>`

   **GitLab** (requires `glab` CLI):
   - Verify `glab` is available: `glab --version`. If not, skip and tell the user to run `/optimus:pr` to create the MR (it can install the CLI)
   - `glab mr create --title "<conventional title>" --description "$(cat "$TMPFILE")" --target-branch <original-branch>`

   Follow the Conventional PR template, incorporating TDD-specific data: include how many behaviors were implemented via TDD in the **Summary**, use `git diff --stat <original-branch>..HEAD` for **Changes**, and list each behavior as a verification item in the **Test plan** with coverage delta if available (e.g., "Coverage: [X]% → [Y]% (+[Z]%)").

4. **Report** to the user:

```
### Git Activity
- Branch: `<branch-name>` (from `<original-branch>`)
- Commits: [N]
- Pushed: ✓
- PR/MR: [URL] (or "Run `/optimus:pr` to create — CLI not available")
```

If behaviors remain unfinished, note them and suggest re-running `/optimus:tdd` to continue.

### Worktree cleanup

If a worktree was used (Step 3), read `$CLAUDE_PLUGIN_ROOT/skills/tdd/references/tdd-worktree-orchestration.md` and follow the **Cleanup** section.

Recommend running `/optimus:code-review` to review the PR/MR before merging.

Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
