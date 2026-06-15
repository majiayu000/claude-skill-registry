---
name: unikit-verify
description: >-
  Verify completed implementation against the feature plan from .unikit/plans/.
  Checks that all tasks were fully implemented, nothing was forgotten, code compiles,
  tests pass, and {{engine_name}}-specific conventions are followed (per ENGINE_RULES.md).
  Use after "/unikit-implement" completes, or when user says "verify", "check work",
  "did we miss anything". Also trigger when reviewing a feature branch before merge
  or PR creation.
argument-hint: "[--strict] [NNN-feature-name]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(wc *)
  - Agent
  - AskUserQuestion
  - Skill
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "1.2"
  category: quality
---

# Verify — Post-Implementation Quality Check

Verify that the implementation matches the plan, nothing was missed, and the code is ready for merge.

This skill runs after `/unikit-implement` or manually at any time.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

<!-- unikit:agents codex -->
## Subagent Delegation — BLOCKING PRE-REQUISITE

When the workflow reaches a step that requires a subagent (`Agent`), the assistant MUST automatically spawn the
subagent if agent execution is supported by the current environment and not prohibited by higher-priority
instructions.

Only if agent execution is unavailable or blocked, the assistant MUST ask the user before proceeding with any
alternative.
<!-- unikit:end -->

---

## Delegation agents

This skill uses named delegation aliases for `Agent(...)` calls. Each alias expands to an `Agent(subagent_type: "general-purpose", ...)` invocation with the matching skill loaded.

- **`develop-agent`** — used ONLY for fixes that span many independent files OR require extensive codebase exploration. Default fixes are applied inline by this skill using rules loaded in Step 0.2 Bootstrap. Expands to:

  ```
  Agent(
    subagent_type: "general-purpose",
    prompt: "/unikit-devcontext <fix details>",
    description: "Apply fix",
    skills: ["unikit-devcontext"]
  )
  ```

  Fallback: if the `Agent` tool is unavailable, invoke `/unikit-devcontext` inline.

- **`rules-agent`** — capture a new project rule spotted during verification. Expands to:

  ```
  Agent(
    subagent_type: "general-purpose",
    prompt: "/unikit-rules Add rule: <rule text>",
    description: "Record project rule",
    skills: ["unikit-rules"]
  )
  ```

  Fallback: if the `Agent` tool is unavailable, invoke `/unikit-rules` inline, one rule at a time.

---

## Step 0: Load Context

### 0.0 Load Ownership and Gate Contract

- Read `{{skills_dir}}/{{self_name}}/references/CONTEXT-GATES-AND-OWNERSHIP.md` first.
- Treat it as the canonical source for:
  - command-to-artifact ownership,
  - read-only behavior for `unikit-commit`/`unikit-review`/`unikit-verify`,
  - normal vs strict context-gate thresholds.
- If this contract conflicts with older examples in this file, follow the contract.

### 0.1 Find Feature Plan

Search logic — same as `/unikit-implement` (unified plan detection):

1. If `$ARGUMENTS` specifies a folder name (e.g. `2026-03-10_core-loop` or legacy `NNN-feature-name`) → use it
2. Otherwise → auto-detect:
   a. **Fast plan check** — if `.unikit/PLAN.md` exists, use it (flat fast-mode plan)
   b. **Git branch match** — if on `feature/*` branch, find folder ending with `_<feature-name>` (new format) or `*-<feature-name>` (legacy)
   c. **Latest by date** (fallback) — sort all folders lexicographically descending, pick first (YYYY-MM-DD gives chronological order; legacy `DDD-*` sorts before `2xxx-*`)
3. If no plan found (no `.unikit/PLAN.md` and `.unikit/plans/` is empty or doesn't exist):

```
No plan found. What should I verify?

Options:
1. Verify branch diff — compare current branch against master
2. Verify last N commits — check recent commits for completeness
3. Cancel
```

Based on choice:
- Branch diff → gather `CHANGED_FILES` via `git diff --name-only $BASE_BRANCH...HEAD`. Skip Step 1 (Task Completion Audit — no plan exists). Execute Step 2 (Code Quality) and Step 3 (Consistency Checks) on collected files. In the report (Step 4), use header: `### Standalone verification (no plan)` instead of `### Feature: ...`
- Last N commits → ask user for the number of commits via AskUserQuestion. Gather files via `git diff --name-only HEAD~N..HEAD`. Skip Step 1. Execute Steps 2-3 on collected files. Same standalone report header.
- Cancel → **STOP**

**If both `.unikit/PLAN.md` and a matching folder plan exist**, ask the user which one to verify.

Check if `--strict` is in `$ARGUMENTS`. If yes — enable strict mode (see Strict Mode section).

### 0.2 Read Plan & Context

**If using `.unikit/PLAN.md`** (fast-mode plan):
- Read **`.unikit/PLAN.md`** — single file containing checklist, overview, settings, and optionally technical context inline
- Read **`.unikit/DESCRIPTION.md`** — project specification, tech stack
- Read **`.unikit/ARCHITECTURE.md`** — project structure, dependency rules, modules, namespace conventions
- Read **`.unikit/ROADMAP.md`** (if present) — strategic milestones for alignment checks

**If using a folder plan** (`.unikit/plans/<folder>/`):
- Read **`TASKS.md`** — feature overview (`## Overview`), task checklist with phases and statuses
- Read **`PLAN-BRIEF.md`** — technical context: constraints, interfaces, key patterns, files, DI bindings (if exists in plan folder)
- If `TASKS.md` has a `## Based on` section pointing to a research → read that research's `RESEARCH_BRIEF.md` instead
- Read **`.unikit/DESCRIPTION.md`** — project specification, tech stack
- Read **`.unikit/ARCHITECTURE.md`** — project structure, dependency rules, modules, namespace conventions
- Read **`.unikit/ROADMAP.md`** (if present) — strategic milestones for alignment checks

Bootstrap loads coding rules and principles ONCE upfront so Step 4.3 fixes can be applied inline without re-loading on each delegation.

**Read in parallel (rules + principles, for inline fix execution in Step 4.3):**
1. `.unikit/system/dev-principles.md` — engine development principles
2. `.unikit/RULES.md` — project overrides (highest priority)
3. `.unikit/memory/RULES_INDEX.md` — index of core/stack rules
4. For EACH row in the Core table where Required By = `all` or contains `unikit-verify` — read that file from `.unikit/memory/core/` using the Read tool.

Stack rules are loaded on-demand if Step 4.3 fixes reveal framework-specific issues.

**Read `.unikit/skill-context/unikit-verify/SKILL.md`** — MANDATORY if the file exists.

This file contains project-specific rules accumulated by `/unikit-evolve` from patches,
codebase conventions, and tech-stack analysis. These rules are tailored to the current project.

**How to apply skill-context rules:**
- Treat them as **project-level overrides** for this skill's general instructions
- When a skill-context rule conflicts with a general rule written in this SKILL.md,
  **the skill-context rule wins** (more specific context takes priority)
- When there is no conflict, apply both: general rules from SKILL.md + project rules from skill-context
- Do NOT ignore skill-context rules even if they seem to contradict this skill's defaults —
  they exist because the project's experience proved the default insufficient

Understand:
- Which tasks are completed (`- [x]`) and which are not (`- [ ]`)
- Dependencies between phases
- Which files and classes are expected

### 0.3 Load Engine Rules

Read `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md` to load engine-specific verification checks.

This file contains:
- **Companion file checks** — engine-specific file pairing rules
- **Module boundary checks** — engine-specific boundary enforcement mechanism
- **Structural checks** — engine-specific code conventions and validation rules
- **Read-only paths** — engine-specific directories that must not be modified
- **Strict mode items** — engine-specific checks that always fail on violation

All engine-specific checks in Steps 2 and 3 reference this file. If `ENGINE_RULES.md` is missing, skip engine-specific checks and note: `Engine rules: ENGINE_RULES.md not found, engine-specific checks skipped`.

### 0.4 Detect Base Branch

Determine the project's base branch (may be `main` or `master`):

```bash
# Detect base branch
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
# Fallback: check which branch exists
if [ -z "$BASE_BRANCH" ]; then
  BASE_BRANCH=$(git rev-parse --verify origin/master >/dev/null 2>&1 && echo master || echo main)
fi
```

Save as `$BASE_BRANCH` — use it in all subsequent git commands instead of hardcoded `main` or `master`.

### 0.5 Gather Changed Files

```bash
# Files changed within the feature
git diff --name-only $BASE_BRANCH...HEAD
# Or if on $BASE_BRANCH — check recent commits
git diff --name-only HEAD~20..HEAD
```

Save as `CHANGED_FILES` — this list will be used in all subsequent steps.

---

## Step 1: Task Completion Audit

**Use `Agent` tool with `subagent_type: Explore, model: sonnet` to verify task completion in parallel.** This keeps the main context clean and allows simultaneous verification of multiple phases.

Launch one Explore task per phase from the plan's task list. For each phase, provide:
- Task descriptions from the roadmap
- `CHANGED_FILES` list for context
- Instructions: find implementing code using Glob/Grep, read key files, confirm completeness (not a stub), report status per task with file paths

**Fallback:** If Agent tool is unavailable, investigate directly using Glob and Grep.

### 1.1 Build Checklist

After tasks return, synthesize findings into a checklist:

```
✅ Task 1.1: Create ICustomer interface — COMPLETED
   - ICustomer.cs created in Assets/Modules/Characters/Scripts/Customers/
   - All methods from plan are present
   - Namespace is correct

⚠️ Task 2.3: Add customer factory — PARTIAL
   - CustomerFactory.cs created
   - MISSING: CreateFromConfig() method mentioned in plan
   - MISSING: registration in Zenject installer

❌ Task 3.1: Create CustomerView — NOT FOUND
   - File not found in expected directory
   - No mention of CustomerView in changed files
```

Statuses:
- `✅ COMPLETED` — all requirements confirmed in code
- `⚠️ PARTIAL` — partially implemented, something missing
- `❌ NOT FOUND` — implementation not found
- `⏭️ SKIPPED` — task was intentionally skipped by the user

---

## Step 2: Code Quality Verification

### 2.1 {{engine_name}} Compile Check

Use {{engine_mcp_tool}} to check that the project compiles after implementation:
- Refresh/recompile the project through {{engine_mcp_tool}}
- Check the {{engine_name}} console for compilation errors
- If errors found — display them with `file:line` references
- If {{engine_mcp_tool}} is unavailable — skip and note: `Compilation check: {{engine_mcp_tool}} unavailable, skipped`

### 2.2 {{engine_name}} Test Check

Use {{engine_mcp_tool}} to run tests for affected modules:
- Determine which test assemblies cover the modified modules (check CLAUDE.md for the list of test assemblies)
- If changed files include modules with test assemblies — run those assemblies specifically
- Otherwise run all EditMode tests as a baseline check
- Wait for results and display them — highlight any failures
- If {{engine_mcp_tool}} is unavailable — skip and note: `Test run: {{engine_mcp_tool}} unavailable, skipped`

### 2.3 Engine-Specific Checks

Apply all checks defined in `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md`:

- **Companion file checks** — verify file pairing rules for this engine (if applicable)
- **Module boundary checks** — verify dependency boundaries using the engine's boundary mechanism (if applicable)
- **Structural checks** — verify engine-specific code conventions
- **Read-only path enforcement** — flag any modifications to engine-defined read-only directories

If `ENGINE_RULES.md` is not loaded (Step 0.3), skip this section and note: `Engine-specific checks: skipped (no ENGINE_RULES.md)`


---

## Step 3: Consistency Checks

### 3.1 Plan vs Code Drift

Check discrepancies between plan and code:

- **Naming**: do class/interface/method names match the plan?
- **File locations**: are files where the plan expected them?
- **Contracts**: do interfaces contain the methods described in the plan?

### 3.2 Leftover Artifacts

Search for artifacts that should have been cleaned up:

```
Grep in CHANGED_FILES: TODO|FIXME|HACK|XXX|TEMP|PLACEHOLDER
```

Also check:
- `Debug.Log` without conditional context (not in #if DEBUG)
- Commented-out code blocks

Each finding — record it, but note it may be intentional.

### 3.3 DESCRIPTION.md Sync

Check whether `.unikit/DESCRIPTION.md` reflects the current state:

- New dependencies/libraries → should be in the document
- Architecture changes → should be reflected
- New modules → should be documented

### 3.4 ARCHITECTURE.md Sync

Check `.unikit/ARCHITECTURE.md`:

- New modules or directories → should be in the project tree
- New module boundaries → should be reflected in dependency rules
- Changes to folder structure → should be updated

### 3.5 Context Gates (Architecture / Rules / Roadmap)

Apply the canonical contract from `{{skills_dir}}/{{self_name}}/references/CONTEXT-GATES-AND-OWNERSHIP.md`.

Evaluate and report each gate explicitly:

- **Architecture gate**
  - Pass: implementation follows module/layer boundaries, dependency rules, and anti-patterns from `.unikit/ARCHITECTURE.md`
  - Warn: architecture document appears stale or mapping is ambiguous
  - Fail: clear boundary/dependency violation (e.g. `Assets/Modules/` → `Assets/Game/`)

- **Rules gate**
  - Pass: implementation follows explicit project rules
  - Warn: relevance/verification is ambiguous
  - Fail: clear violation of explicit rule text

- **Roadmap gate** (only if `.unikit/ROADMAP.md` exists)
  - Pass: `feat`/`fix`/`perf` work has milestone linkage in the plan's `## Roadmap Linkage` section
  - Warn: `.unikit/ROADMAP.md` missing, ambiguous milestone mapping, or no milestone linkage for `feat`/`fix`/`perf` scope
  - Note: missing milestone linkage for `feat`/`fix`/`perf` remains a warning even in strict mode — it is never a blocker

Normal mode behavior:
- Architecture/rules clear violations fail verification.
- Ambiguous or stale context artifacts are warnings.
- Missing milestone linkage is a warning.

Strict mode behavior:
- Architecture and rules clear violations fail verification.
- Stale context artifacts are warnings.
- Missing milestone linkage is a warning (not a failure).

Logging/reporting format:
- Non-blocking findings: `WARN [gate-name] ...`
- Blocking findings: `ERROR [gate-name] ...`

### 3.6 Context Drift (Optional Remediation)

`/unikit-verify` is **read-only** for context artifacts. Do not edit or regenerate `.unikit/*` files here.

If you detect that a context artifact is stale, missing, or ambiguous, report it as a drift finding and provide the owner-command remediation:

- `DESCRIPTION.md` drift → suggest `/unikit` (or note that `/unikit-implement` should have updated it)
- `ARCHITECTURE.md` drift → suggest `/unikit-architecture`
- `RULES.md` drift → suggest `/unikit-rules` to add missing conventions
- `ROADMAP.md` drift → suggest `/unikit-roadmap check` (or `/unikit-roadmap <update request>`)

Ask the user a single optional question **only if** drift was detected and fixing it now would materially improve correctness:

```
Context drift detected. Update now?

Options:
1. Yes — show update commands (recommended)
2. No — continue without updating
```

Based on choice:
- Yes → show update commands for user to invoke
- No → continue verification without updating

### 3.7 Documentation Sync

Check whether the implementation introduced user-facing changes that should be reflected in project documentation (`README.md`, `docs/`).

**a) Check plan's Docs policy:**

Read the `## Settings` section from `TASKS.md` (or `.unikit/PLAN.md`):
- If `Docs: yes` — verify that documentation was actually updated during implementation (check `CHANGED_FILES` for `README.md`, `docs/*.md`, or `.unikit/docs-config.json`). If no doc files were modified: `WARN [docs] Docs policy was 'yes' but no documentation files were changed — run /unikit-docs`
- If `Docs: no` or missing — check whether the implementation introduced new public APIs, new modules, changed configuration, or modified user-facing behavior. If yes: `WARN [docs] Implementation changed public API/behavior but Docs policy was no/unset — consider /unikit-docs`

**b) Check existing docs for staleness:**

If `README.md` and/or `docs/` exist:
- Scan for references to classes, interfaces, or files that were renamed or deleted during this implementation
- Check if docs mention modules or systems that were substantially restructured
- If stale references found: `WARN [docs] docs/<file>.md references <old-name> which was renamed/deleted in this implementation`

**c) Report:**

Include documentation findings in the verification report under a `### Documentation` section:
- `✅ Documentation up to date` — docs policy satisfied or no doc-impacting changes
- `⚠️ Documentation may need update` — with specific findings and suggestion to run `/unikit-docs`

---

## Step 4: Verification Report

### 4.1 Display Results

```
## Verification Report

### Feature: {NNN-feature-name}
### Branch: {current branch}

### Task Completion: 7/8 (87%)
| # | Task | Status | Notes |
|---|------|--------|-------|
| 1.1 | Create ICustomer | ✅ Completed | |
| 1.2 | Create CustomerArgs | ✅ Completed | |
| 2.1 | Add CustomerFactory | ⚠️ Partial | Missing CreateFromConfig() |
| 2.2 | Register in DI | ✅ Completed | |
| 3.1 | Create CustomerView | ❌ Not found | File missing |

### Code Quality
- Compilation: ✅ / ⏭️ {{engine_mcp_tool}} unavailable
- Tests: ✅ 12 passed, 0 failed / ⏭️ {{engine_mcp_tool}} unavailable
- Engine checks: ✅ All passed (per ENGINE_RULES.md)
- Anti-patterns: ⚠️ 2 warnings

### Issues Found
1. **Task 2.1 partial** — CustomerFactory created but missing CreateFromConfig() method
2. **Task 3.1 not implemented** — CustomerView.cs not found
3. **Anti-pattern** — async void in CustomerSpawner.cs:42
4. **TODO found** — Assets/Game/Scripts/.../CustomerSystem.cs:87

### Documentation
- Documentation: ✅ up to date / ⚠️ may need update (run /unikit-docs)

### No Issues
- Engine-specific checks passed (per ENGINE_RULES.md)
- Namespace convention followed
- DESCRIPTION.md up to date
```

### 4.2 Determine Overall Status

- **All clean** — all tasks verified, no issues
- **Minor issues** — can be fixed quickly
- **Significant gaps** — tasks not implemented, needs more work

### 4.3 Action on Issues

If issues were found:

```
Verification found issues. What to do?

Options:
1. Fix now (recommended) — fix all issues right here
2. Fix critical only — skip warnings
3. Accept as is — move on
```

Based on choice:
- Fix now → apply fixes inline using `Read/Edit/Write/Bash` with the rules and principles loaded in Step 0.2. Use `develop-agent` ONLY when fixes span many independent files OR require extensive codebase exploration. Do NOT invoke `/unikit-devcontext` via `Skill(...)` — Bootstrap already covers everything.
- Fix critical only → same inline approach, but only incomplete tasks — skip warnings
- Accept as is → mark accepted issues in the report, proceed to Step 5

**Fallback:** If `Agent` tool is unavailable, do NOT invoke `/unikit-devcontext` inline. Implement fixes directly with the rules from Step 0.2 Bootstrap.

For each fix iteration (Fix now / Fix critical only). Fixes are written by this skill directly; rules are already in context from Step 0.2 Bootstrap.
- For each incomplete/partial task — implement the missing parts
- For TODO/debug artifacts — clean up
- For anti-patterns — fix
- Update `TASKS.md` after fixes
- After fixes — re-run checks on affected items

---

## Step 5: Suggest Follow-Up

After verification completes, suggest next steps based on results:

- If unresolved issues remain (accepted or deferred), suggest `/unikit-fix` first
- If all green, suggest review/commit flow

If recurring convention violations were found during verification (e.g. the same naming pattern was wrong in multiple places, or a DI convention was consistently missed), formulate up to 3 candidate rules and delegate to `rules-agent` (1 agent per rule, up to 3 agents), passing each rule text as the agent's prompt — e.g. `Add rule: Factory methods use CreateDefault() naming`. Do NOT wait for agents to finish — proceed to the next step immediately.

**Fallback** (if the `Agent` tool is unavailable in the current environment): you MUST invoke `/unikit-rules` yourself, one candidate at a time. Do NOT print the list of pending invocations to the user as a recommendation — that is a known failure mode where LLMs render the list instead of executing it. For every candidate rule, in order:

1. Invoke the `/unikit-rules` skill directly using whatever skill-invocation mechanism is available, passing the rule text as the argument. The slash-command invocation must be a real call, not printed text.
2. Wait for the invocation to return control before starting the next iteration.
3. Move to the next candidate. Do not stop after the first one. Do not ask the user to confirm between iterations. Do not wrap `/unikit-rules ...` lines in triple backticks.

Only after every candidate has been processed, proceed to the next step.

```
Verification complete. What's next?

Options:
1. Fix issues — run /unikit-fix with verification findings
2. Code review — run /unikit-review on changed files
3. Commit — run /unikit-commit
4. Skip — I'll handle it myself
```

Based on choice:
- Fix issues → run `/unikit-fix` with issue summary
- Code review → run `/unikit-review` on changed files
- Commit → run `/unikit-commit`
- Skip → **STOP**

### Context Cleanup

Suggest the user to free up context space if needed: `/clear` (full reset) or `/compact` (compress history).

---

## Strict Mode

When called with `--strict`:

```
/unikit-verify --strict
```

Normal mode already checks all items below but tolerates partial results and warnings. Strict mode **raises the bar** on these specific points:

| Check | Normal mode | Strict mode |
|-------|-------------|-------------|
| Task completion | `⚠️ PARTIAL` and `⏭️ SKIPPED` allowed | All tasks must be `✅ COMPLETED` — partial and skipped are failures |
| Compilation ({{engine_mcp_tool}}) | Reported if available | **Required** to pass if {{engine_mcp_tool}} is available |
| Tests ({{engine_mcp_tool}}) | Reported if available | **Required** to pass if test assemblies exist for affected modules |
| TODO/FIXME/HACK | Warning | **Failure** — no leftover markers allowed in changed files |
| Anti-patterns | Warning | **Failure** — async void, missing CancellationToken, etc. |

Items that behave **the same** in both modes (always checked, always fail on violation):
- Engine-specific checks (per ENGINE_RULES.md strict mode items)
- Namespace correctness
- Context gates (Architecture, Rules — see thresholds in `{{skills_dir}}/{{self_name}}/references/CONTEXT-GATES-AND-OWNERSHIP.md`)

Strict mode is recommended before merging to the base branch or creating a PR.

---

## Important Rules

1. **Read-only by default** — verification only reads and analyzes; fixes only with explicit user consent
2. **Respond in the configured language** — use `language.ui` from `.unikit/config.yaml` (default: English)
3. **Precise references** — always provide file:line for each finding
4. **No false positives** — if unsure, mark as "⚠️ Verify manually"
5. **Do not modify .unikit/ files** — only report drift and suggest updates
6. **Do not touch engine read-only paths** — see ENGINE_RULES.md for the list of read-only directories; ignore them during checks
7. **Agent-based delegation** — use `Agent(subagent_type: Explore, model: sonnet, ...)` for read-only investigation. Fixes are applied INLINE by this skill using rules loaded in Step 0.2 Bootstrap. Use `develop-agent` for fixes ONLY when they span many independent files or require extensive codebase exploration. Never invoke `/unikit-devcontext` via `Skill(...)`. If Agent tool is unavailable, fall back to inline work for both exploration (Glob/Grep/Read) and fixes (direct Read/Edit/Write/Bash with loaded rules).

---

## Usage

### After implement (recommended)
```
/unikit-verify
```

### Strict mode before merge
```
/unikit-verify --strict
```

### Specific feature
```
/unikit-verify 2026-03-08_customers-system
```

### Strict + specific feature
```
/unikit-verify --strict 2026-03-08_customers-system
```
