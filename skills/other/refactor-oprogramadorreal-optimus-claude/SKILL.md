---
description: Refactors existing code for guideline compliance and testability using 4 parallel analysis agents (guideline compliance, testability barriers, duplication/consistency, code-simplifier). Two goals — align code with project guidelines AND make untestable code testable so /optimus:unit-test can safely increase coverage. Use after /optimus:init to align existing code, before /optimus:unit-test to remove testability barriers, or periodically to prevent tech debt. Supports "testability" focus (after unit-test flags untestable code) or "guidelines" focus (after init establishes rules) to prioritize finding categories, flexible scoping, and a "deep" mode for iterative refactoring (default 8, up to 10 iterations).
disable-model-invocation: true
---

# Project-Wide Code Refactoring

Analyze existing source code against the project's coding guidelines using 4 parallel agents to find guideline violations, testability barriers, cross-file duplication, and pattern inconsistency. Present a prioritized refactoring plan, then apply only user-approved changes with test verification.

Two primary goals:
1. **Guideline compliance** — align code with coding-guidelines.md, architecture.md, styling.md, and testing.md
2. **Testability** — restructure code so `/optimus:unit-test` can safely increase coverage without risky refactoring

The code-simplifier agent guards new code after every edit — this skill is the on-demand complement for restructuring existing code across the project.

## Step 1: Verify Prerequisites and Determine Scope

### Multi-repo workspace detection

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected, resolve prerequisites per-repo:
- Determine which repo(s) the scope targets (from file paths, user selection, or changed files)
- Load that repo's `.claude/CLAUDE.md` and `.claude/docs/` as prerequisites (not the workspace root)
- If scope spans multiple repos, load each repo's docs independently and apply per-repo context when analyzing that repo's files
- If no repo can be determined, ask the user which repo to analyze

### Prerequisite check

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/prerequisite-check.md` and apply the prerequisite check (CLAUDE.md + coding-guidelines.md existence, fallback logic).

### Parse invocation arguments

Extract from the user's arguments:
1. `deep` flag (present/absent)
2. `harness` keyword after `deep` (present/absent)
3. A number immediately after `deep` or `deep harness` → iteration cap (optional, default 8, hard cap 10)
4. Focus keyword detection — match only **standalone unquoted tokens** (not inside quotes or part of longer words):
   - If remaining unquoted text contains standalone `testability` (case-insensitive) → set `focus` = `"testability"`
   - If remaining unquoted text contains standalone `guidelines` (case-insensitive) → set `focus` = `"guidelines"`
   - Otherwise → `focus` = null (balanced — current behavior)
   - The focus keyword is consumed from the remaining text (not passed as scope)
   - If both keywords appear as standalone tokens, use the first one and warn: "Multiple focus keywords detected — using '[first]'. Run separate passes for each focus."
   - **Safe examples** (keyword NOT consumed — stays as scope):
     - `/optimus:refactor "improve testability in auth"` → focus=null, scope="improve testability in auth" (inside quotes)
     - `/optimus:refactor "fix guidelines compliance"` → focus=null, scope="fix guidelines compliance" (inside quotes)
5. Everything else → scope instructions (natural language)

Examples:
- `/optimus:refactor` → full project, normal mode
- `/optimus:refactor "focus on auth module"` → scope to auth, normal mode
- `/optimus:refactor testability` → full project, normal mode, focus=testability
- `/optimus:refactor guidelines` → full project, normal mode, focus=guidelines
- `/optimus:refactor testability "focus on src/api"` → scope to src/api, focus=testability
- `/optimus:refactor deep` → full project, deep (8 iterations)
- `/optimus:refactor deep 10 backend` → scope to backend, deep (10 iterations)
- `/optimus:refactor deep guidelines` → full project, deep, focus=guidelines
- `/optimus:refactor deep harness` → harness mode, 8 iterations, full project
- `/optimus:refactor deep harness testability` → harness mode, focus=testability

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

### Harness mode detection

If the system prompt contains `HARNESS_MODE_ACTIVE`, read `$CLAUDE_PLUGIN_ROOT/references/harness-mode.md` and follow its single-iteration execution protocol. The reference covers progress file reading, state initialization, scope and file-list rules, and step overrides (including the Step 8 apply/output protocol). Then proceed through Step 1's scope resolution (branch-diff path only — no `AskUserQuestion`), Step 3, and Step 4 — skip only the Step 2 deep-mode confirmation. If `scope_files.current` is non-empty in the progress file, treat it as the pre-resolved scope (the harness pre-populated it from the feature-branch diff) and skip the Step 1 scope resolution entirely.

If `HARNESS_MODE_ACTIVE` is NOT in the system prompt, continue with the standard interactive flow below.

### Skill-triggered harness invocation

If the `harness` keyword was detected in Step 1, read the **Skill-Triggered Invocation** section of `$CLAUDE_PLUGIN_ROOT/references/harness-mode.md` and follow its steps. Pass:
- `skill_name` = `refactor`
- `scope` = scope text from Step 1 argument parsing
- `max_iterations` = parsed iteration cap from Step 1 (if specified)
- `focus` = focus keyword from Step 1 (if detected)

The reference protocol presents the command and stops. Do not proceed to Step 3 or any remaining steps.

### Interactive deep mode

If the `deep` flag was detected in Step 1, activate deep mode. Deep mode loops analysis-apply cycles (Steps 4–8) until clean or the iteration cap is reached.

Before proceeding, check whether a test command is available (from `.claude/CLAUDE.md`). If no test command exists, deep mode's auto-apply loop has no safety net — fall back to normal mode and warn: "Deep mode requires a test command for safe auto-apply. Falling back to normal mode — re-run `/optimus:init` to set up test infrastructure first." Set `deep-mode` to false. Then continue with the standard single-pass flow.

If a test command is available, warn the user:

> **Deep mode** runs up to [cap] iterative refactoring passes. Each iteration is a full multi-agent analysis cycle — credit and time consumption multiplies with iteration count. Fixes are applied automatically at each iteration without per-change approval. Low test coverage increases the chance of undetected breakage; consider running `/optimus:unit-test` first to strengthen the safety net. Each iteration also accumulates context — on large codebases, output quality may degrade in later iterations.
>
> Test command: `[test command from CLAUDE.md]`

Then use `AskUserQuestion` — header "Deep mode", question "Proceed with deep mode?":
- **Start deep mode** — "Run iterative refactoring until clean (max [cap] iterations)"
- **Normal mode** — "Single pass with manual approval instead"

Tell the user: *Tip: For large codebases or extended sessions, re-run with `/optimus:refactor deep harness` to launch the external harness with fresh context per iteration.*

If the user did not invoke with `deep`, skip this step.

If the user selects **Normal mode**, continue with the standard single-pass flow. Record the user's choice as a `deep-mode` flag for subsequent steps. If deep mode is confirmed, initialize `iteration-count` to 1, `total-applied` to 0, `total-reverted` to 0, and `accumulated-findings` to an empty list. Each entry in `accumulated-findings` tracks: **file** (with line), **category**, **guideline** (the specific project rule, barrier type, or quality concern from the agent finding), **summary** (one-sentence description of the issue), **fix description** (brief description of the applied or attempted change), **iteration** (which iteration discovered it), and **status** (updated through apply/test phases).

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

**Harness mode:** If `scope_files.current` from the progress file is non-empty, derive analysis areas from the unique parent directories of those files instead of scanning the whole project — this keeps the refactor pass focused on the feature branch's actual footprint.

### Prioritize by git activity

Rank directories by recent change frequency:

```bash
git log --no-merges --since="3 months" --format= --name-only -- <scope-path> | sort | uniq -c | sort -rn
```

Analyze highest-churn directories first. For full-project scope on large codebases, start with the top 10 most active areas.

### Context Summary

Before proceeding to analysis, present a brief summary: docs loaded (with paths), docs missing (with fallback status), project type (single/monorepo/multi-repo workspace), and analysis areas identified with their git activity rank. Proceed immediately to Step 4 — do not wait for user confirmation.

## Step 4: Parallel Multi-Agent Analysis (4 agents)

Launch all 4 agents as `general-purpose` Agent tool calls in a **single** message so they run in parallel. The full fan-out is the design — do not reduce the count to save tokens or time.

Each agent receives the list of source files/directories from Step 3.

Read the agent prompt files from `$CLAUDE_PLUGIN_ROOT/skills/refactor/agents/` for individual agent prompts. Read `$CLAUDE_PLUGIN_ROOT/skills/refactor/agents/shared-constraints.md` for the shared quality bar, exclusion rules, and false positive guidance.

### Iteration context injection (deep mode, iterations 2+)

If deep mode is active and `iteration-count` > 1, prepend the iteration context block to every agent prompt before the file list. Read `$CLAUDE_PLUGIN_ROOT/skills/refactor/agents/context-blocks.md` for the template and format.

### Agent overview

| Agent | Role | Runs when |
|-------|------|-----------|
| 1 — Guideline Compliance | Explicit violations of project docs with exact rule citations | Always |
| 2 — Testability Analyzer | Structural barriers to unit testing — hardcoded deps, tight coupling, global state | Always |
| 3 — Consistency Analyzer | Cross-file duplication, pattern inconsistency, missing abstractions, architectural drift | Always |
| 4 — Code Simplifier | Unnecessary complexity, naming, dead code, pattern violations | Always |

Each agent returns a structured list of findings, bounded by the Finding Cap rule in `$CLAUDE_PLUGIN_ROOT/references/shared-agent-constraints.md`. The Guideline Compliance agent (Agent 1) is constructed dynamically based on Step 3's doc loading results (single project vs monorepo paths).

Wait for all launched agents to complete before proceeding to Step 5.

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

After deduplication, check for **cross-agent contradictions** — findings that target the same code region but recommend opposite directions (e.g., "extract this to reduce duplication" vs. "inline this for clarity"). Keep the higher-severity finding and drop the other. When severities are equal, keep the finding that matches the active focus (testability or guidelines). When no focus is active, keep the testability finding — testability is a primary goal of this skill.

### Finding caps

Maximum **15 findings** per run — only include findings that represent distinct root causes with supporting evidence. Do NOT pad to reach the cap: a focused plan of 3 strong findings is preferred over 15 weak ones.

**When focus is active** (testability or guidelines):
- Reserve **12 slots** for the focused category, **3 slots** for other categories
- Within each slot group, prioritize by severity then confidence
- If the focused category has fewer than 12 findings, redistribute unused slots to other categories
- If other categories have fewer than 3 findings, redistribute unused slots to the focused category
- Category mapping:
  - `testability` focus: Testability Barrier findings + any finding with a "Testability impact" line → reserved slots. All others → other slots.
  - `guidelines` focus: Guideline Violation, Inconsistency, Duplication, Missing Abstraction, Architectural Drift, Code Quality findings → reserved slots. Testability Barrier findings → other slots.

**When no focus is active** (default balanced mode):
- Prioritize by severity then confidence across all categories (current behavior)

If more issues exist, note the count (e.g., "15 of ~24 findings shown") and suggest re-running with a narrower scope or `/optimus:refactor deep`.

### Deep mode accumulation

**Deep mode:** Instead of presenting the output format below, append this iteration's validated findings to `accumulated-findings`. For each appended finding, record the current `iteration-count` as the finding's iteration number, and preserve the agent's guideline citation (or barrier type for testability findings) and issue description as the finding's guideline and summary fields. Deduplicate against previous iterations: if a finding matches an existing entry by file + line range + category, skip it if the existing entry is marked "(fixed)". If the existing entry is marked "(persistent — fix failed)", annotate the new entry as "(persistent — fix failed)". If the existing entry is marked "(reverted — test failure)", keep the new entry as "(reverted — attempt 2)" so Step 8 retries the fix once more; only promote to "(persistent — fix failed)" if it is reverted again. Then proceed directly to Step 8.

**Normal mode:** Present findings using the output format below, then proceed to Step 7.

### Output format

```
## Refactoring Plan

### Summary
- Scope: [full project / directory / changed since X]
- Focus: [testability / guidelines / balanced (default)]
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
3. **`iteration-count` >= the cap** → cap reached. Report: "Deep mode reached the iteration cap ([cap]). Remaining findings may exist — continue in a fresh conversation: re-run `/optimus:refactor deep`, increase the cap with `/optimus:refactor deep [higher-cap]`, or narrow scope with `/optimus:refactor deep \"focus on <area>\"`."
4. **Otherwise** → continue to the next pass (iteration report and loop-back below).

**For all four conditions above**, present the iteration report immediately after the termination/continuation message. This report is informational and non-blocking — no user prompt follows:

```
#### Iteration [N] — Report

| # | File | What Changed | Reason | Guideline / Category | Status |
|---|------|-------------|--------|---------------------|--------|
[one row per finding attempted in THIS iteration from accumulated-findings where iteration == current]
```

Column definitions:
- **#** — Sequential number within this iteration
- **File** — `file:line`
- **What Changed** — Brief description of the fix applied or attempted
- **Reason** — Why the change was needed (the issue/problem)
- **Guideline / Category** — Specific project rule violated, barrier type, or quality category
- **Status** — `fixed`, `reverted — test failure`, `reverted — attempt 2`, or `persistent — fix failed`

For condition 4 (continue), after presenting the iteration report also show the progress summary: "Iteration [N] of up to [cap] — [total-applied] findings applied so far, [total-reverted] reverted. Starting next pass..." If the **next** iteration will be 3 or higher, append to the progress summary: "Note: context is accumulating — if output quality degrades, consider finishing remaining findings in a fresh conversation." Then increment `iteration-count` and **return to Step 4** for the next analysis pass. Keep the same scope from Step 1.

After the loop ends, present a cumulative report across all iterations:

```
## Deep Mode — Cumulative Report

**Summary:**
- Total iterations: [N]
- Total findings applied: [N]
- Total findings reverted (test failures): [N]
- Total findings persistent (fix failed): [N]
- Final test status: pass / fail / not available
- Testability improvements: [N] changes made code testable for /optimus:unit-test

**All Changes:**

| # | Iter | File | What Changed | Reason | Guideline / Category | Status |
|---|------|------|-------------|--------|---------------------|--------|
[one row per finding from accumulated-findings, across all iterations, ordered by iteration then sequence]
```

Column definitions match the per-iteration report table, plus:
- **Iter** — Which iteration discovered/attempted this finding

The summary statistics provide a quick overview; the detailed table provides full auditability of every change attempted across all iterations.

## Important

- Never modify files, commit, push, or post comments without explicit user approval (deep mode has explicit approval via the confirmation step in Step 2 — all changes remain as local modifications for the user to review with `git diff` before committing)
- This skill is read-only by default — it only analyzes and reports
- When changes are too broad for effective analysis, recommend narrowing scope

After the refactoring is complete, recommend the next step based on the outcome:
- If issues were found and fixed → `/optimus:commit` to commit the fixes, then `/optimus:unit-test` to cover the restructured code
- If deep mode was used → `/optimus:commit` to commit the accumulated fixes, then `/optimus:unit-test` to strengthen test coverage on the newly-testable code
- If no issues or user skipped fixes → consider `/optimus:unit-test` directly if coverage needs improvement

Tell the user:

- If the recommendation above includes `/optimus:commit` (first two bullets), the closing tip per `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md` "Closing tip wording" — use **Variant B** with `<continuation-skill(s)>` = `/optimus:commit` and `<non-continuation-examples>` = `/optimus:unit-test`, etc. Otherwise (third bullet — no issues / fixes skipped), use **Variant C** (default).
- **Tip (normal mode only):** Single-pass analysis can miss issues due to LLM attention limits. Run `/optimus:refactor deep` to iterate automatically — it applies, tests, and repeats until clean (max 8 passes by default, configurable up to 10). Requires a test command in `.claude/CLAUDE.md`.
