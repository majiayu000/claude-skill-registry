---
name: sprint-1-executor
description: Execute Sprint 1 tasks for FASA optimization and trade analytics. This
  skill should be used when the user requests execution of any Sprint 1 task (Tasks
  1.1-1.4, 11-13, 2.1-2.4, 3.1-3.2), including ca
---

---
name: sprint-1-executor
description: Execute Sprint 1 tasks for FASA optimization and trade analytics. This skill should be used when the user requests execution of any Sprint 1 task (Tasks 1.1-1.4, 11-13, 2.1-2.4, 3.1-3.2), including cap space parsing, Sleeper integration, FASA target marts, FA acquisition history, roster depth analysis, enhanced FASA targets, notebooks, valuation models, trade analysis, automation workflows, or documentation. Each task is atomic, standalone, and designed for independent execution with built-in validation. Current focus: Phase 2 FASA Intelligence (Tasks 11-13, 1.4).
---

# Sprint 1 Executor

Execute Sprint 1 tasks for the Fantasy Football Analytics FASA optimization and trade intelligence sprint. This skill provides structured, atomic task execution with validation and progress tracking.

## When to Use This Skill

Use this skill proactively when:

- User requests execution of any Sprint 1 task (e.g., "Execute Task 1.1", "Start Sprint 1 Task 2.1")
- User asks to work on FASA optimization, cap space, Sleeper integration, or trade analysis
- User references sprint_1 documentation or task files
- User wants to continue sprint work after a break

## Sprint Overview

**Sprint Goal:** Deliver actionable FASA bidding strategy for Week 9 + trade analysis infrastructure
**Sprint End:** Wednesday 2025-10-29 11:59 PM EST
**Current Status:** 🟡 Phase 2 In Progress (Phase 1 ✅ Complete)

**Sprint Structure:**

- **Phase 1:** Foundation (FASA Critical Path) - ✅ COMPLETE
  - Tasks 1.1-1.3: Cap space, Sleeper, FASA marts
  - Bonus: IDP historical data (2020-2025)
- **Phase 2:** FASA Intelligence Enhancements - 🟡 IN PROGRESS
  - Tasks 11-13 (2.4-2.6): FA acquisition history, roster depth, enhanced FASA targets
  - Task 1.4: FASA strategy notebook
- **Phase 3:** Trade Intelligence - ⏸️ DEFERRED
  - Task 2.1: Historical backfill (🟡 partially complete: 2020-2025 done, 2012-2019 deferred)
  - Tasks 2.2-2.4: Valuation model, trade marts, analysis notebook (❌ blocked)
- **Phase 4:** Automation & Production - ⏸️ FUTURE
  - Tasks 3.1-3.2: GitHub Actions workflows, documentation

## Task Execution Workflow

When user requests task execution:

1. **Identify the task** - Determine which task (1.1 through 3.2) from user request

2. **Load task file** - Read the corresponding task file from `references/`:

   **Phase 1: Foundation (Complete ✅)**
   - Task 1.1: `references/01_task_cap_space_foundation.md`
   - Task 1.2: `references/02_task_sleeper_production_integration.md`
   - Task 1.3: `references/03_task_fasa_target_mart.md`

   **Phase 2: FASA Intelligence (Current Focus 🟡)**
   - Task 11 (2.4): `references/11_task_fa_acquisition_history.md`
   - Task 12 (2.5): `references/12_task_league_roster_depth.md`
   - Task 13 (2.6): `references/13_task_enhance_fasa_targets.md`
   - Task 1.4: `references/04_task_fasa_strategy_notebook.md`

   **Phase 3: Trade Intelligence (Deferred ⏸️)**
   - Task 2.1: `references/05_task_historical_backfill.md` (🟡 partial)
   - Task 2.2: `references/06_task_baseline_valuation_model.md` (❌ blocked)
   - Task 2.3: `references/07_task_trade_target_marts.md` (❌ blocked)
   - Task 2.4: `references/08_task_trade_analysis_notebook.md` (❌ blocked)

   **Phase 4: Automation (Future ⏸️)**
   - Task 3.1: `references/09_task_github_actions_workflows.md`
   - Task 3.2: `references/10_task_documentation_polish.md`

3. **Check dependencies** - Review the "Dependencies" section in the task file
   - Verify prerequisite tasks are complete
   - If blocked, inform user and suggest completing prerequisites first

4. **Implement the task** - Follow the task file's implementation steps:
   - Create/modify all files listed in "Files to Create/Modify" section
   - Use exact code templates and SQL from task file
   - Follow step-by-step implementation guide
   - For Tasks 1.3+ that reference `00_SPRINT_PLAN.md`: Load `references/00_SPRINT_PLAN.md` and extract the full SQL/code from the specified line ranges

5. **Validate the implementation** - Run all validation commands from task file:
   - Execute validation bash commands exactly as written
   - Verify all success criteria are met
   - Check code quality: `make lintcheck`, `make typecheck`, `make sqlcheck`
   - **IMPORTANT**: If running `make lintfix` or `make sqlfix`, re-run dbt tests afterward to confirm linters didn't break anything
   - Run dbt tests: `make dbt-test --select [models]`

6. **Report results** - Communicate clearly to user:
   - ✅ What was implemented
   - ✅ Validation results (pass/fail)
   - ⚠️ Any issues or warnings
   - ❌ Blockers (if any)
   - 📝 Next recommended task (if applicable)

7. **Commit changes** - Use the suggested commit message from task file:
   - Copy exact commit message from "Commit Message" section
   - Ensure conventional commit format (feat:/docs:/etc.)
   - Reference task number: "Resolves: Sprint 1 Task X.Y"

8. **Update progress tracking** - After successful commit:
   - Mark task complete in `references/README.md` (⬜ → ✅)
   - Update `references/00_SPRINT_PLAN.md` Progress Tracking section
   - Suggest next task if user wants to continue

## Task File Structure

Each task file contains these sections (use them in order):

1. **Objective** - What and why
2. **Context** - Current state, dependencies, why it matters
3. **Files to Create/Modify** - Complete code listings with templates
4. **Implementation Steps** - Step-by-step guide (follow exactly)
5. **Success Criteria** - Definition of done (validate against this)
6. **Validation Commands** - Exact bash commands to test
7. **Commit Message** - Suggested message (use exactly)
8. **Notes** - Gotchas, tips, future considerations

## Special Handling by Task Type

### Python Implementation Tasks (1.2, 2.1)

- Create modules in `src/ingest/` or `src/ff_analytics_utils/`
- Create production scripts in `scripts/ingest/`
- Follow existing patterns from similar files
- Include type hints and docstrings
- Run `make lint` and `make typecheck`

### dbt Model Tasks (1.1, 1.3, 2.2)

- Create models in `dbt/ff_data_transform/models/staging/` or `dbt/ff_data_transform/models/core/` or `dbt/ff_data_transform/models/marts/`
- Always create both `.sql` and `.yml` files
- Include comprehensive tests in `.yml`
- Set `EXTERNAL_ROOT` environment variable before dbt commands
- Run `make sqlcheck` for SQL linting
- If running `make sqlfix` for auto-formatting, **always re-run dbt tests** to confirm no functional changes
- Validate with `make dbt-run --select` and `make dbt-test --select`

### Notebook Tasks (1.4, 2.3)

- Create in `notebooks/` directory
- Use DuckDB for data loading
- Include visualizations (matplotlib/seaborn)
- Test execution: `uv run jupyter nbconvert --execute --to notebook --inplace`
- Ensure reproducibility (no hardcoded paths)

### GitHub Actions Tasks (3.1)

- Create in `.github/workflows/`
- Use Discord webhooks (not Slack)
- Test locally with `make` targets first
- Use environment variables from secrets
- Include `workflow_dispatch` for manual triggering

### Documentation Tasks (3.2)

- Create in `docs/analytics/` or `docs/dev/`
- Include examples and code snippets
- Link from main README
- Follow markdown formatting standards

## Environment Setup

Before executing tasks, ensure:

```bash
# Set environment variables
export SLEEPER_LEAGUE_ID="1230330435511275520"
export EXTERNAL_ROOT="$PWD/data/raw"

# Verify project dependencies
uv sync

# Verify dbt is working
make dbt-run --select dim_player
```

## Common Validation Patterns

### For Python Code

```bash
uv run python [script] --help
make lint
make typecheck
```

### For dbt Models

```bash
export EXTERNAL_ROOT="$PWD/data/raw"
make dbt-run --select [model_name]
make dbt-test --select [model_name]
dbt show --select [model_name] --limit 10
make sqlcheck

# If running linter auto-fix:
make sqlfix
# IMPORTANT: Re-run tests after linter changes
make dbt-test --select [model_name]
```

### For Data Outputs

```bash
ls -lh data/raw/[source]/[dataset]/dt=*/
uv run python -c "
import polars as pl
df = pl.read_parquet('data/raw/[source]/[dataset]/dt=*/*.parquet')
print(df.head())
print(f'Rows: {len(df)}')
"
```

## Progress Reference

Check current sprint progress in `references/README.md` Task Index table.

Full sprint plan and technical specifications in `references/00_SPRINT_PLAN.md`.

## Key Success Factors

1. **Follow task files exactly** - They contain complete, tested specifications
2. **Validate thoroughly** - Run all validation commands, check all success criteria
3. **Check dependencies** - Don't skip prerequisite tasks
4. **Commit atomically** - One task = one commit with provided commit message
5. **Update tracking** - Mark tasks complete in README and sprint plan
6. **Report clearly** - Tell user what worked, what didn't, what's next

## Handling Issues

If validation fails:

1. Review error messages carefully
2. Check common gotchas (see `references/README.md`)
3. Re-read task file for missed details
4. Verify prerequisites completed
5. Report specific error to user with context

If blocked by dependencies:

1. Identify which prerequisite task is missing
2. Inform user: "Task X.Y requires Task A.B to be complete first"
3. Offer to execute prerequisite task or wait

## Task Dependencies Quick Reference

**Phase 1: Foundation** (✅ COMPLETE)

- Task 1.1 (Cap Space) → Task 1.2 (Sleeper) → Task 1.3 (FASA Mart) ✅

**Phase 2: FASA Intelligence** (🟡 CURRENT FOCUS)

- Task 1.3 (FASA Mart) ✅
  - ⬇
  - Tasks 11, 12, 13 can run in parallel ⬜
    - Task 11 (FA Acquisition History)
    - Task 12 (League Roster Depth)
    - Task 13 (Enhance FASA Targets)
  - ⬇
  - Task 1.4 (FASA Strategy Notebook) 🟦

**Phase 3: Trade Intelligence** (⏸️ DEFERRED - blocked)

- Task 2.1 (Historical Backfill) 🟡 (2020-2025 complete, 2012-2019 deferred)
  - ⬇
  - Task 2.2 (Valuation Model) ❌ (blocked - needs full 2012-2024 backfill)
  - ⬇
  - Task 2.3 (Trade Marts) ❌ (blocked by 2.2)
  - ⬇
  - Task 2.4 (Trade Notebook) ❌ (blocked by 2.3)

**Phase 4: Automation** (⏸️ FUTURE)

- Task 3.1 (GitHub Actions) → Task 3.2 (Documentation) ⬜

See `references/README.md` dependency diagram for full details.

## Output Format

When reporting task completion:

```text
✅ Sprint 1 Task X.Y Complete: [Task Name]

**Implemented:**
- [List of files created/modified]

**Validation Results:**
- ✅ All tests passing (X/X)
- ✅ Code quality checks passed
- ✅ Success criteria met

**Committed:**
- Commit message: [exact message from task file]
- Branch: [current branch]

**Next Steps:**
- Task X.Z: [Next task name] [priority level]
- [or] Sprint 1 Phase X complete! Ready for Phase Y
```

If issues encountered:

```text
⚠️ Sprint 1 Task X.Y: Partial Completion / Issues

**Completed:**
- [What worked]

**Issues:**
- ❌ [Specific error/failure]
- ⚠️ [Warnings or concerns]

**Validation Status:**
- ✅ [Passed checks]
- ❌ [Failed checks]

**Recommended Action:**
- [Specific next steps to resolve]
```
