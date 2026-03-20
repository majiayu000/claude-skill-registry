---
description: Refactors existing code for guideline compliance and testability using up to 4 parallel analysis agents (guideline compliance, testability barriers, duplication/consistency, optional code-simplifier). Two goals — align code with project guidelines AND make untestable code testable so /optimus:unit-test can safely increase coverage. Use after /optimus:init to align existing code, before /optimus:unit-test to remove testability barriers, or periodically to prevent tech debt. Supports flexible scoping and a "deep" mode for iterative refactoring (default 5, up to 10 iterations).
disable-model-invocation: true
---

# Project-Wide Code Refactoring

Analyze existing source code against the project's coding guidelines using up to 4 parallel agents to find guideline violations, testability barriers, cross-file duplication, and pattern inconsistency. Present a prioritized refactoring plan, then apply only user-approved changes with test verification.

Two primary goals:
1. **Guideline compliance** — align code with coding-guidelines.md, architecture.md, styling.md, and testing.md
2. **Testability** — restructure code so `/optimus:unit-test` can safely increase coverage without risky refactoring

The code-simplifier agent guards new code after every edit — this skill is the on-demand complement for restructuring existing code across the project.

**Progress visibility** — When starting each step, show a brief one-line progress indicator (e.g., "**[Step 2/8]** Activating deep mode..."). Keep it short — the indicator orients the user, not narrate internals.

## Step 1: Verify Prerequisites and Determine Scope

### Multi-repo workspace detection

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected, resolve prerequisites per-repo:
- Determine which repo(s) the scope targets (from file paths, user selection, or changed files)
- Load that repo's `.claude/CLAUDE.md` and `.claude/docs/` as prerequisites (not the workspace root)
- If scope spans multiple repos, load each repo's docs independently and apply per-repo context when analyzing that repo's files
- If no repo can be determined, ask the user which repo to analyze

### Prerequisite check

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/prerequisite-check.md` and apply the prerequisite check (CLAUDE.md + coding-guidelines.md existence, fallback logic).

### Agent prerequisites

Check that this file exists:
- `.claude/agents/code-simplifier.md`

**If missing**, warn the user and recommend running `/optimus:init` to install it. Agent 4 (Code Simplifier) will be skipped in Step 4; the analysis still covers guidelines, testability, and duplication via Agents 1–3.

### Parse invocation arguments

Extract from the user's arguments:
1. `deep` flag (present/absent)
2. A number immediately after `deep` → iteration cap (optional, default 5, hard cap 10)
3. Everything else → scope/focus instructions (natural language)

Examples:
- `/optimus:refactor` → full project, normal mode
- `/optimus:refactor backend only` → scope to backend, normal mode
- `/optimus:refactor "focus on auth module"` → scope to auth, normal mode
- `/optimus:refactor deep` → full project, deep (5 iterations)
- `/optimus:refactor deep 8` → full project, deep (8 iterations)
- `/optimus:refactor deep "focus on src/api"` → scope to src/api, deep (5 iterations)
- `/optimus:refactor deep 10 backend` → scope to backend, deep (10 iterations)

If the iteration cap exceeds 10, clamp it to 10 and warn: "Iteration cap clamped to 10 (maximum)."
If the iteration cap is less than 1, clamp it to 1 and warn: "Iteration cap clamped to 1 (minimum)."

### Scope resolution

- **If scope provided in arguments** → use it directly. Map the user's description to directory paths by scanning the project structure. No `AskUserQuestion` needed.
- **If no scope provided** → use `AskUserQuestion` — header "Scope", question "What scope would you like to refactor?":
  - **Full project** — "All source directories — best for first run or periodic review"
  - **Directory** — "Specific path(s) — best for targeted cleanup"
  - **Changed since** — "Files modified since a commit, tag, or date — incremental review"

Default to **full project** if the user just says "refactor" without specifying.

For **changed since**: use `git diff --name-only <ref>...HEAD` for commit SHAs, branch names, and tags. For relative dates, use `git log --no-merges --since="2 weeks ago" --format= --name-only` instead (`--since` is a `git log` flag, not `git diff`). Filter to source files only (apply the exclusion rules from Step 3).

For monorepos with **full project** scope: ask which subprojects to include (default: all). For **directory** scope: auto-detect which subproject the path belongs to.

## Step 2: Deep Mode Activation

If the `deep` flag was detected in Step 1, activate deep mode. Deep mode loops analysis-apply cycles (Steps 4–8) until zero findings remain or the iteration cap is reached.

Before proceeding, check whether a test command is available (from `.claude/CLAUDE.md`). If no test command exists, deep mode's auto-apply loop has no safety net — fall back to normal mode and warn: "Deep mode requires a test command for safe auto-apply. Falling back to normal mode — re-run `/optimus:init` to set up test infrastructure first." Set `deep-mode` to false. Then continue with the standard single-pass flow.

If a test command is available, warn the user:

> **Deep mode** runs up to [cap] iterative refactoring passes. Each iteration is a full multi-agent analysis cycle — credit and time consumption multiplies with iteration count. Fixes are applied automatically at each iteration without per-change approval. Low test coverage increases the chance of undetected breakage; consider running `/optimus:unit-test` first to strengthen the safety net.
>
> Test command: `[test command from CLAUDE.md]`

Then use `AskUserQuestion` — header "Deep mode", question "Proceed with deep mode?":
- **Start deep mode** — "Run iterative refactoring until clean (max [cap] iterations)"
- **Normal mode** — "Single pass with manual approval instead"

If the user did not invoke with `deep`, skip this step.

If the user selects **Normal mode**, continue with the standard single-pass flow. Record the user's choice as a `deep-mode` flag for subsequent steps. If deep mode is confirmed, initialize `iteration-count` to 1, `total-applied` to 0, `total-reverted` to 0, and `accumulated-findings` to an empty list.

## Step 3: Load Project Context and Map Analysis Areas

### Load constraint docs

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md` for the full document loading procedure (single project and monorepo layouts, scoping rules).

These files define the rules. Every suggestion must be justified by what these docs establish — never impose external preferences.

### Exclude git submodules

Apply the "Submodule Exclusion" rule from `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md` — exclude submodule directories from the analysis.

### Map analysis areas

Within the chosen scope (Step 1), identify source directories. Skip non-source:
- **Dot-directories**: `.git`, `.github`, `.vscode`, `.idea`, `.claude`, `.husky`
- **Dependencies**: `node_modules`, `vendor`, `.venv`, `venv`, `env`
- **Build output**: `dist`, `build`, `out`, `target`, `bin`, `obj`, `coverage`
- **Framework/cache**: `.next`, `.nuxt`, `__pycache__`, `.cache`, `.tox`, `.turbo`
Also skip non-source **file types**: `*.min.js`, `*.min.css`, lock files (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, etc.), `*.d.ts` (unless hand-written), binary and data files.

Also skip **generated source files** that should never be manually edited: `*.g.dart`, `*.freezed.dart`, `*.mocks.dart` (Dart/Flutter build_runner output), `*.Designer.cs` (Visual Studio generated), and any file inside a directory named `Migrations/` (database migration files — EF Core, Django, Alembic, etc.).

**Single project:** Group files by top-level source directory.
**Monorepo:** Organize by subproject, then by source directory within each.

### Prioritize by git activity

Rank directories by recent change frequency:

```bash
git log --no-merges --since="3 months" --format= --name-only -- <scope-path> | sort | uniq -c | sort -rn
```

Analyze highest-churn directories first. For full-project scope on large codebases, start with the top 10 most active areas.

### Context Summary

Before proceeding to analysis, present a brief summary: docs loaded (with paths), docs missing (with fallback status), project type (single/monorepo/multi-repo workspace), agents available (with skip status for missing ones), and analysis areas identified with their git activity rank. Proceed immediately to Step 4 — do not wait for user confirmation.

## Step 4: Parallel Multi-Agent Analysis (up to 4 agents)

3 core analysis agents + 1 project-level agent, all launched in parallel for maximum coverage.

Launch up to 4 `general-purpose` Agent tool calls simultaneously. Agents 1–3 always run; Agent 4 only runs if `.claude/agents/code-simplifier.md` exists (checked in Step 1).

Each agent receives the list of source files/directories from Step 3.

Read `$CLAUDE_PLUGIN_ROOT/skills/refactor/references/agent-prompts.md` for the full prompt templates, quality bar, exclusion rules, and false positive guidance for all 4 agents.

### Iteration context injection (deep mode, iterations 2+)

If deep mode is active and `iteration-count` > 1, prepend the iteration context block to every agent prompt before the file list. Read the **Iteration Context Block** section in `$CLAUDE_PLUGIN_ROOT/skills/refactor/references/agent-prompts.md` for the template and format.

### Agent overview

| Agent | Role | Runs when |
|-------|------|-----------|
| 1 — Guideline Compliance | Explicit violations of project docs with exact rule citations | Always |
| 2 — Testability Analyzer | Structural barriers to unit testing — hardcoded deps, tight coupling, global state | Always |
| 3 — Duplication & Consistency | Cross-file duplication, pattern inconsistency, missing abstractions, architectural drift | Always |
| 4 — Code Simplifier | Unnecessary complexity, naming, dead code, pattern violations | `.claude/agents/code-simplifier.md` exists |

Each agent: max 8 findings, structured list format. The Guideline Compliance agent (Agent 1) is constructed dynamically based on Step 3's doc loading results (single project vs monorepo paths).

### Execution

Launch all available agents simultaneously (parallel, not sequential). Wait for all launched agents to complete before proceeding to Step 5.

**Agent availability summary**: Agents 1–3 always run (no project dependencies). Agent 4 depends on the installed code-simplifier agent. If it is missing, note in the summary and recommend `/optimus:init` for full 4-agent analysis.

## Step 5: Validate Findings

Independently verify each finding to filter false positives. Apply the verification protocol from `$CLAUDE_PLUGIN_ROOT/skills/init/references/verification-protocol.md` — treat agent-reported findings as claims that require independent evidence, not as ground truth.

For each finding from Step 4:
1. **Context check** — read ±30 lines around the flagged location to verify the issue exists in context
2. **Intent check** — look for comments, test assertions, or established patterns that explain the code's behavior (what looks like a violation may be intentional)
3. **Cross-agent consensus** — for guideline/duplication findings, check if Agents 1 and 3 flagged the same location (consensus = higher confidence)
4. **Runtime assumption check** — if an agent flagged a function or module, verify whether the code assumes something about inputs, dependencies, or environment that is not validated or documented. Unvalidated assumptions that could cause runtime failures strengthen the finding's confidence.

### Change-intent awareness

For each unique file that has findings, check recent git history for deliberate changes:

```bash
git log --no-merges --format="%h %s" -5 -- <file>
```

If a recent commit message clearly indicates deliberate code introduction (e.g., "add dependency injection", "extract service layer") **and** a finding suggests removing or reverting that code → reduce the finding's confidence by one level (High → Medium, Medium → Low → drop).

For uninformative commit messages (fewer than 15 characters, or generic like "fix", "update", "changes"), run `git show <sha> -- <file>` to examine the actual diff for intent patterns: added abstractions, validation logic, or architectural changes. Apply the same confidence reduction if the diff shows deliberate structural code that a finding wants to undo.

Skip gracefully if `git log` fails or returns no results (e.g., shallow clone, newly created file, or file outside the repository).

### Confidence assignment

Assign confidence:
- **High** — clear issue with strong evidence → keep
- **Medium** — plausible issue, some evidence → keep with note
- **Low** — uncertain, likely false positive → drop

Only findings with High or Medium confidence proceed to Step 6.

## Step 6: Present Refactoring Plan

Merge validated findings from Steps 4–5. Deduplicate: if two agents flagged the same file and line range for the same category, keep the more detailed version. For findings flagged by both Agents 1 and 3, merge into one finding and note "confirmed by independent review".

### Contradiction resolution

After deduplication, check for **cross-agent contradictions** — findings that target the same code region but recommend opposite directions (e.g., "extract this to reduce duplication" vs. "inline this for clarity"). Keep the higher-severity finding and drop the other. When severities are equal, keep the testability finding — testability is a primary goal of this skill.

### Finding caps

Maximum **8 findings** per run, prioritized by severity then confidence. If more issues exist, note the count (e.g., "8 of ~18 findings shown") and suggest re-running with a narrower scope — e.g., `/optimus:refactor "focus on src/auth"` or `/optimus:refactor deep` for exhaustive refactoring.

### Deep mode accumulation

**Deep mode:** Instead of presenting the output format below, append this iteration's validated findings to `accumulated-findings`. Deduplicate against previous iterations: if a finding matches an existing entry by file + line range + category, skip it if the existing entry is marked "(fixed)". If the existing entry is marked "(persistent — fix failed)", annotate the new entry as "(persistent — fix failed)". If the existing entry is marked "(reverted — test failure)", keep the new entry as "(reverted — attempt 2)" so Step 8 retries the fix once more; only promote to "(persistent — fix failed)" if it is reverted again. Then proceed directly to Step 8.

**Normal mode:** Present findings using the output format below, then proceed to Step 7.

### Output format

```
## Refactoring Plan

### Summary
- Scope: [full project / directory / changed since X]
- Areas analyzed: [N]
- Total findings: [N] shown (of ~[M] detected) — Critical: [N], Warning: [N], Suggestion: [N]
- Cross-cutting findings: [N]
- Testability improvements: [N] findings will make code testable for /optimus:unit-test
- Top recommendation: [one-sentence summary of highest-impact finding]

### Cross-Cutting Findings

**[N]. [Finding title]** (Critical/Warning/Suggestion)
- **Files:** `file1:line`, `file2:line`, ...
- **Category:** [Guideline Violation | Testability Barrier | Duplication | Inconsistency | Missing Abstraction | Architectural Drift]
- **Guideline:** [which project guideline this addresses]
- **Pattern:** [brief description of the cross-file issue]
- **Suggested:** [brief description of the fix approach]
- **Testability impact:** [what becomes testable after this refactoring — omit if not applicable]

### Findings by Area

#### [Area/Module Name] — [path]

**[N]. [Finding title]** (Critical/Warning/Suggestion)
- **File:** `file:line`
- **Category:** [Guideline Violation | Testability Barrier | Code Quality | Duplication | Inconsistency | Missing Abstraction | Architectural Drift]
- **Guideline:** [which project guideline this addresses]
- **Current:**
  ```
  [code sketch — max 5 lines]
  ```
- **Suggested:**
  ```
  [code sketch — max 5 lines]
  ```
- **Testability impact:** [what becomes testable after this refactoring — omit if not applicable]

### Areas with No Findings
- [Area name] — code follows project guidelines
```

Prioritize by severity:
- **Critical** — Testability barrier blocking unit testing, cross-cutting pattern, significant duplication, or SRP violation affecting readability/safety
- **Warning** — Guideline violation or consistency improvement in limited scope
- **Suggestion** — Minor clarity or hygiene item

Include "Areas with No Findings" to confirm coverage — the user should know those areas were reviewed, not skipped.

**No findings at all:**

**Deep mode:** this is the convergence signal — report "Deep mode complete — no findings on iteration [N]", then skip to the cumulative summary and recommendation in Step 8 (bypass the apply phase).

**Normal mode:** Report as a positive result ("code follows project guidelines and is well-structured for testing"). Suggest tightening guidelines or broadening scope if the user expected issues. Skip Steps 7–8 and proceed directly to the recommendation in the Important section below.

## Step 7: Ask User How to Proceed

**Deep mode:** Skip this step — auto-select "Apply all" and proceed directly to Step 8.

**Normal mode:**

Use `AskUserQuestion` — header "Action", question "How would you like to proceed with the refactoring findings?":
- **Apply all** — "Apply every recommendation"
- **Selective** — "Choose specific finding numbers to apply"
- **Skip** — "No changes — keep the report as reference"

If the user selects **Selective**, ask which finding numbers to apply (e.g., "1, 3, 5"). Remember the user's choice and approved finding numbers for Step 8.

## Step 8: Apply Approved Changes and Verify

For each approved finding (skipping any annotated "(persistent — fix failed)" — these have already failed in a prior iteration):
1. Apply the refactoring using Edit or MultiEdit
2. Verify the change matches the suggestion from Step 6

After applying all approved changes, run the project's test command (from `.claude/CLAUDE.md`) if available. Follow the verification protocol from `$CLAUDE_PLUGIN_ROOT/skills/init/references/verification-protocol.md` — run tests fresh, read complete output, report actual results with evidence:
- If tests pass → report success. If `deep-mode` is true, annotate each applied finding as "(fixed)" in `accumulated-findings` and add the count of applied fixes to `total-applied`.
- If tests fail → revert all changes, then re-apply one at a time with a test run after each. Keep changes that pass, skip those that fail. If `deep-mode` is true: annotate kept changes as "(fixed)" in `accumulated-findings` (add to `total-applied`); for failed changes, if already annotated "(reverted — attempt 2)" promote to "(persistent — fix failed)", otherwise annotate as "(reverted — test failure)" (add to `total-reverted`).

If no test command is available, warn the user that changes were applied without automated verification and carry higher risk.

### Final summary

**Deep mode (non-final iteration):** Skip this subsection — the iteration progress summary in the deep mode loop below replaces it.

**Deep mode (final iteration) and Normal mode:**

- Scope analyzed (from Step 1)
- Changes applied (with file references)
- Changes skipped (with reasons if selective)
- Test results (pass/fail/not available)
- Any changes reverted due to test failures
- Remaining findings not shown in this run (if cap was hit)
- Testability improvements: [N] changes will make code testable — run `/optimus:unit-test` to cover the restructured code

### Deep mode loop

**Normal mode:** Skip this subsection — proceed to the recommendation below.

**Deep mode:** If arriving here from convergence (zero findings in Step 6), skip the termination checks below and go directly to the cumulative summary.

After applying changes and running tests, check termination conditions (the iteration's counts were already added to `total-applied` and `total-reverted` in the apply phase above):

1. **All changes in this iteration were reverted due to test failures** → stop to prevent a loop of failed attempts. Report: "Deep mode stopped — all findings in iteration [N] caused test failures."
2. **No changes were applied** (all findings lacked actionable code edits) → stop. Report: "Deep mode stopped — remaining findings require manual review."
3. **`iteration-count` >= the cap** → cap reached. Report: "Deep mode reached the iteration cap ([cap]). Remaining findings may exist — re-run `/optimus:refactor deep [higher-cap]` with a larger iteration cap, or narrow scope with `/optimus:refactor deep \"focus on <area>\"`."
4. **Otherwise** → present an iteration progress summary: "Iteration [N] of up to [cap] — [total-applied] findings applied so far, [total-reverted] reverted. Starting next pass..." Increment `iteration-count` and **return to Step 4** for the next analysis pass. Keep the same scope from Step 1.

After the loop ends, present a cumulative summary across all iterations:

- Total iterations: [N]
- Total findings applied: [N]
- Total findings reverted (test failures): [N]
- Test status: pass / fail / not available
- Testability improvements: [N] changes made code testable for /optimus:unit-test

Mark each finding's status: "(fixed)", "(reverted — test failure)", or "(persistent — fix failed)".

## Important

- Never modify files, commit, push, or post comments without explicit user approval (deep mode has explicit approval via the confirmation step in Step 2 — all changes remain as local modifications for the user to review with `git diff` before committing)
- This skill is read-only by default — it only analyzes and reports
- When changes are too broad for effective analysis, recommend narrowing scope

After the refactoring is complete, recommend the next step based on the outcome:
- If issues were found and fixed → `/optimus:commit` to commit the fixes, then `/optimus:unit-test` to cover the restructured code
- If deep mode was used → `/optimus:commit` to commit the accumulated fixes, then `/optimus:unit-test` to strengthen test coverage on the newly-testable code
- If no issues or user skipped fixes → consider `/optimus:unit-test` directly if coverage needs improvement

Tell the user:

- **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
- **Tip (normal mode only):** Single-pass analysis can miss issues due to LLM attention limits. Run `/optimus:refactor deep` to iterate automatically — it applies, tests, and repeats until clean (max 5 passes by default, configurable up to 10). Requires a test command in `.claude/CLAUDE.md`.
