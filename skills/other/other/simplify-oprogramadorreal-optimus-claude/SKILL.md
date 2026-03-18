---
description: Analyzes the codebase against project coding guidelines as on-demand code simplification — run after /optimus:init, when code quality drifts, or for periodic cleanup. Surfaces issues that span multiple files (duplication across modules, pattern inconsistency, architectural drift) and presents a simplification plan for approval before changes are applied. Supports a "deep" parameter for iterative cleanup until zero findings remain.
disable-model-invocation: true
---

# Project-Wide Code Simplification

Analyze source code against the project's coding guidelines to find issues that span multiple files: duplication across modules, inconsistent patterns between areas, architectural drift, and dead code. Present a prioritized simplification plan, then apply only user-approved changes with test verification.

The code-simplifier agent guards new code after every edit — this skill is the on-demand complement for reviewing existing code across the project.

## Step 1: Verify Prerequisites and Determine Scope

### Multi-repo workspace detection

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected, resolve prerequisites per-repo:
- Determine which repo(s) the scope targets (from file paths, user selection, or changed files)
- Load that repo's `.claude/CLAUDE.md` and `.claude/docs/` as prerequisites (not the workspace root)
- If scope spans multiple repos, load each repo's docs independently and apply per-repo context when analyzing that repo's files
- If no repo can be determined, ask the user which repo to analyze

### Prerequisite check

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/prerequisite-check.md` and apply the prerequisite check (CLAUDE.md + coding-guidelines.md existence, fallback logic).

Use `AskUserQuestion` to let the user choose a scope — header "Scope", question "What scope would you like to analyze?":
- **Full project** — "All source directories — best for first run or periodic review"
- **Directory** — "Specific path(s) — best for targeted cleanup"
- **Changed since** — "Files modified since a commit, tag, or date — incremental review"

Default to **full project** if the user just says "simplify" without specifying.

For **changed since**: use `git diff --name-only <ref>...HEAD` for commit SHAs, branch names, and tags. For relative dates, use `git log --since="2 weeks ago" --format= --name-only` instead (`--since` is a `git log` flag, not `git diff`). Filter to source files only (apply the exclusion rules from Step 3).

For monorepos with **full project** scope: ask which subprojects to include (default: all). For **directory** scope: auto-detect which subproject the path belongs to.

## Step 2: Deep Mode Activation

If the user invoked with `deep` (e.g., `/optimus:simplify deep` or `/optimus:simplify deep "focus on src/"`), activate deep mode. Deep mode loops analysis-apply cycles (Steps 4–7) until zero findings remain or **5 iterations** are reached.

Before proceeding, check whether a test command is available (from `.claude/CLAUDE.md`). If no test command exists, deep mode's auto-apply loop has no safety net — fall back to normal mode and warn: "Deep mode requires a test command for safe auto-apply. Falling back to normal mode — run `/optimus:unit-test` first to enable deep mode." Then continue with the standard single-pass flow.

If a test command is available, warn the user:

> **Deep mode** runs up to 5 iterative simplification passes. Each iteration is a full analysis-apply cycle — credit and time consumption multiplies with iteration count. Low test coverage increases the chance of undetected breakage; consider running `/optimus:unit-test` first to strengthen the safety net.

Then use `AskUserQuestion` — header "Deep mode", question "Proceed with deep mode?":
- **Start deep mode** — "Run iterative cleanup until clean (max 5 iterations)"
- **Normal mode** — "Single pass with manual approval instead"

If the user did not invoke with `deep`, skip this step.

If the user selects **Normal mode**, continue with the standard single-pass flow. Record the user's choice as a `deep-mode` flag for subsequent steps. If deep mode is confirmed, initialize `iteration-count` to 1, `total-applied` to 0, and `total-reverted` to 0.

## Step 3: Load Project Context and Map Analysis Areas

### Load constraint docs

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md` for the full document loading procedure (single project and monorepo layouts, scoping rules).

These files define the rules. Every suggestion must be justified by what these docs establish — never impose external preferences.

### Map analysis areas

Within the chosen scope (Step 1), identify source directories. Skip non-source:
- **Dot-directories**: `.git`, `.github`, `.vscode`, `.idea`, `.claude`, `.husky`
- **Dependencies**: `node_modules`, `vendor`, `.venv`, `venv`, `env`
- **Build output**: `dist`, `build`, `out`, `target`, `bin`, `obj`, `coverage`
- **Framework/cache**: `.next`, `.nuxt`, `__pycache__`, `.cache`, `.tox`, `.turbo`
- **Git submodules**: Any directory containing a `.git` *file* (not directory) — these belong to external repositories

Also skip non-source **file types**: `*.min.js`, `*.min.css`, lock files (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, etc.), `*.d.ts` (unless hand-written), binary and data files.

Also skip **generated source files** that should never be manually edited: `*.g.dart`, `*.freezed.dart`, `*.mocks.dart` (Dart/Flutter build_runner output), `*.Designer.cs` (Visual Studio generated), and any file inside a directory named `Migrations/` (database migration files — EF Core, Django, Alembic, etc.).

**Single project:** Group files by top-level source directory.
**Monorepo:** Organize by subproject, then by source directory within each.

### Prioritize by git activity

Rank directories by recent change frequency:

```bash
git log --since="3 months" --format= --name-only -- <scope-path> | sort | uniq -c | sort -rn
```

Analyze highest-churn directories first. For full-project scope on large codebases, start with the top 10 most active areas.

### Context Summary

Before proceeding to analysis, present a brief summary: docs loaded (with paths), docs missing (with fallback status), project type (single/monorepo/multi-repo workspace), and analysis areas identified with their git activity rank. Let the user confirm before heavy analysis begins.

## Step 4: Analyze Source Code

For each area, evaluate source files against the constraints loaded in Step 3.

### Cross-cutting analysis (highest priority)

These findings span multiple files — the unique value of project-wide review that single-file analysis cannot provide:

- **Duplication across modules** — Repeated logic in different files/directories that could be consolidated (when consolidation improves clarity or reduces maintenance burden)
- **Pattern inconsistency** — Code in one area that deviates from patterns established elsewhere in the same codebase (e.g., error handling done three different ways, inconsistent service layer patterns)
- **Architectural drift** — Code that has evolved away from the boundaries defined in `architecture.md` (e.g., direct DB access in a controller when the project uses a repository pattern)
- **Missing shared abstraction** — Multiple files working around the absence of a common utility or type that would clarify intent across the codebase
- **Testability barriers** — Code with testable logic that cannot be unit-tested due to hardcoded dependencies or tight coupling, when the coding guidelines justify extraction

### Per-file analysis

These supplement cross-cutting findings with localized improvements. Apply each principle from the project's coding guidelines (loaded in Step 3) as an analysis lens — for each principle the guidelines establish, check whether the code follows it.

### Finding quality bar

Only surface findings that meet ALL of these criteria:
- Justified by a specific guideline from the project's docs (Step 3)
- Respects architectural boundaries, test conventions, and styling conventions
- The fix is concrete and demonstrable (not vague "consider refactoring")
- The improvement is meaningful enough that a reviewer would approve the change

When in doubt, don't flag it. Prefer well-justified, low-risk changes over speculative restructuring. Never change what the code does — only how it expresses it.

**Monorepo:** Apply each subproject's own constraint docs to its code. The shared `coding-guidelines.md` applies everywhere, but `testing.md`, `styling.md`, and `architecture.md` are subproject-scoped — don't apply backend testing conventions to frontend code or vice versa.

### Finding caps

Surface at most **12 findings per run** and **5 per area**, prioritized by impact. If more issues exist, note the count (e.g., "12 of ~25 findings shown") and suggest re-running with a narrower scope — e.g., `/optimus:simplify` "focus on src/auth" or "review only the api module".

## Step 5: Present Simplification Plan

Present findings as a structured report:

```
## Simplification Plan

### Summary
- Scope: [full project / directory / changed since X]
- Areas analyzed: [N]
- Total findings: [N] shown (of ~[M] detected) — High: [N], Medium: [N], Low: [N]
- Cross-cutting findings: [N]
- Top recommendation: [one-sentence summary of highest-impact finding]

### Cross-Cutting Findings

**[N]. [Finding title]** (High/Medium/Low)
- **Files:** `file1:line`, `file2:line`, ...
- **Guideline:** [which project guideline this addresses]
- **Pattern:** [brief description of the cross-file issue]
- **Suggested:** [brief description of the fix approach]

### Findings by Area

#### [Area/Module Name] — [path]

**[N]. [Finding title]** (High/Medium/Low)
- **File:** `file:line`
- **Guideline:** [which project guideline this addresses]
- **Current:**
  ```
  [code sketch — max 5 lines]
  ```
- **Suggested:**
  ```
  [code sketch — max 5 lines]
  ```

### Areas with No Findings
- [Area name] — code follows project guidelines
```

Prioritize by impact:
- **High** — Cross-cutting pattern, significant duplication, or SRP violation affecting readability/safety
- **Medium** — Clarity/consistency improvement in limited scope
- **Low** — Minor style or hygiene item

Include "Areas with No Findings" to confirm coverage — the user should know those areas were reviewed, not skipped.

**No findings at all:**

**Deep mode:** this is the convergence signal — report "Deep mode complete — no findings on iteration [N]", then skip to the cumulative summary and recommendation in Step 7 (bypass the apply phase).

**Normal mode:** Report as a positive result ("code follows project guidelines"). Suggest tightening guidelines or broadening scope if the user expected issues.

## Step 6: Ask User How to Proceed

**Deep mode:** Skip this step — auto-select "Apply all" and proceed directly to Step 7.

**Normal mode:**

Use `AskUserQuestion` — header "Action", question "How would you like to proceed with the simplification findings?":
- **Apply all** — "Apply every recommendation"
- **Selective** — "Choose specific finding numbers to apply"
- **Skip** — "No changes — keep the report as reference"

If the user selects **Selective**, ask which finding numbers to apply (e.g., "1, 3, 5"). Remember the user's choice and approved finding numbers for Step 7.

## Step 7: Apply Approved Changes and Report

For each approved finding:
1. Apply the simplification using Edit or MultiEdit
2. Verify the change matches the suggestion from Step 5

After applying all approved changes, run the project's test command (from `.claude/CLAUDE.md`) if available. Follow the verification protocol from `$CLAUDE_PLUGIN_ROOT/skills/init/references/verification-protocol.md` — run tests fresh, read complete output, report actual results with evidence:
- If tests pass → report success
- If tests fail → revert all changes, then re-apply one at a time with a test run after each. Keep changes that pass, skip those that fail, and record each failure as "reverted due to test failure"

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

### Deep mode loop

**Normal mode:** Skip this subsection — proceed to the recommendation below.

**Deep mode:** If arriving here from convergence (zero findings in Step 5), skip the termination checks below and go directly to the cumulative summary.

After applying changes and running tests, add this iteration's applied and reverted counts to the `total-applied` and `total-reverted` running totals, then check termination conditions:

1. **`iteration-count` equals 5** → cap reached. Report: "Deep mode reached the iteration cap (5). Remaining findings may exist — re-run `/optimus:simplify deep` in a fresh conversation to continue."
2. **All changes in this iteration were reverted due to test failures** → stop to prevent a loop of failed attempts. Report: "Deep mode stopped — all findings in iteration [N] caused test failures."
3. **Otherwise** → present an iteration progress summary: "Iteration [N] of up to 5 — [total-applied] findings applied so far, [total-reverted] reverted. Starting next pass..." Increment `iteration-count` and **return to Step 4** for the next analysis pass. Keep the same scope from Step 1.

After the loop ends, present a cumulative summary across all iterations:

- Total iterations: [N]
- Total findings applied: [N]
- Total findings reverted (test failures): [N]
- Test status: pass / fail / not available

**Deep mode recommendation:** Recommend running `/optimus:commit` to commit the accumulated changes, then `/optimus:unit-test` to strengthen test coverage — deep simplification benefits from a strong safety net. Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.

**Normal mode recommendation:** Recommend running `/optimus:commit` to commit the changes. Tell the user:

- **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
- **Tip:** Single-pass analysis can miss issues due to LLM attention limits. Run `/optimus:simplify deep` to iterate automatically — it applies, tests, and repeats until clean (max 5 passes). Requires a test command in `.claude/CLAUDE.md`.
