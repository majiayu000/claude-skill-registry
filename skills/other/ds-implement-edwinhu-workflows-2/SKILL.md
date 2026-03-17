---
name: ds-implement
description: "REQUIRED Phase 3 of /ds workflow. Enforces output-first verification at each step."
---

## Overview

Apply output-first verification at every step of analysis implementation. This is Phase 3 of the `/ds` workflow.

## Contents

- [The Iron Law of DS Implementation](#the-iron-law-of-ds-implementation) - EVERY step MUST produce visible output
- [Delegation](#delegation) - Main chat orchestrates, subagents analyze
- [What Output-First Means](#what-output-first-means)
- [Red Flags](#red-flags---stop-immediately)
- [Implementation Process](#implementation-process)
- [Verification Patterns](#verification-patterns) - See `references/verification-patterns.md`
- [Common Failures](#common-failures-to-avoid)
- [Gate: Exit Implementation](#gate-exit-implementation)

# Implementation (Output-First Verification)

Implement analysis with mandatory visible output at every step.
**NO TDD** - instead, every code step MUST produce and verify output.

<EXTREMELY-IMPORTANT>
## The Iron Law of DS Implementation

**EVERY CODE STEP MUST PRODUCE VISIBLE OUTPUT. This is not negotiable.**

Before moving to the next step, you MUST:
1. Run the code
2. See the output (print, display, plot)
3. Verify output is correct/reasonable
4. Document in LEARNINGS.md
5. Only THEN proceed to next step

This applies even when YOU think:
- "I know this works"
- "It's just a simple transformation"
- "I'll check results at the end"
- "The code is straightforward"

**If you're about to write code without outputting results, STOP.**
</EXTREMELY-IMPORTANT>

## Delegation

<EXTREMELY-IMPORTANT>
**YOU MUST NOT WRITE ANALYSIS CODE IN MAIN CHAT. This is not negotiable.**

You orchestrate. Subagents analyze. For every task in PLAN.md, use the delegation skill:

```
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/ds-delegate/SKILL.md")
```

This is MANDATORY. ds-delegate contains the Task agent templates, output-first protocol details, methodology review patterns, and rationalization prevention. Do not attempt to summarize or shortcut it.

**If you're about to write analysis code directly, STOP and read ds-delegate.**

If you wrote analysis code in main chat, DELETE it immediately and dispatch a Task agent instead. Code written in main chat is contaminated by orchestrator context and must not be kept.
</EXTREMELY-IMPORTANT>

## What Output-First Means

| DO | DON'T |
|-------|----------|
| Print shape after each transform | Chain operations silently |
| Display sample rows | Trust transformations work |
| Show summary stats | Wait until end to check |
| Verify row counts | Assume merges worked |
| Check for unexpected nulls | Skip intermediate checks |
| Plot distributions | Move on without looking |

**The Mantra:** If not visible, it cannot be trusted.

## Red Flags - STOP Immediately

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "I'll check at the end" | STOP - you're letting errors compound silently | Check after every step |
| "This transform is simple" | STOP - simple code can still be wrong | Output and verify |
| "I know merge worked" | STOP - you've assumed this before and been wrong | Check row counts |
| "Data looks fine" | STOP - you're confusing "looks" with verification | Print stats, show samples |
| "I'll batch the outputs" | STOP - you're about to lose your ability to isolate issues | Output per operation |
| "Just a quick plot in main chat" | STOP - you're about to violate delegation | Spawn a Task agent |


## Implementation Strategy Choice

After prerequisites pass and PLAN.md verified, check for parallelization potential:

**Skip this choice when:**
- PLAN.md has fewer than 4 tasks
- All tasks are dependent (every task is `after N` with no independent groups)
- Tasks form a pipeline (clean → merge → aggregate → model)
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is not available

**Otherwise, ask the user:**

```python
AskUserQuestion(questions=[{
  "question": "How should we implement the analysis tasks in PLAN.md?",
  "header": "Strategy",
  "options": [
    {"label": "Sequential (Default)", "description": "One task at a time with output-first verification. Safest, most DS work is sequential."},
    {"label": "Agent team (parallel)", "description": "Spawn analyst per independent task group. Only for truly independent analysis branches (descriptive stats by subgroup, model comparisons). Requires reconciliation."}
  ],
  "multiSelect": false
}])
```

**If Sequential:** Proceed to [Implementation Process](#implementation-process) below (current behavior).

**If Agent team:** Skip to [Agent Team Implementation (Parallel)](#agent-team-implementation-parallel).


## Implementation Process

### Step 1: Read Plan and Delegation Skill

```
Read(".claude/PLAN.md")
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/ds-delegate/SKILL.md")
```

Follow the task order defined in the plan. Use ds-delegate's templates for every task.

### Step 2: Execute Each Task via Delegation

For each task in PLAN.md:
1. Dispatch analyst subagent (per ds-delegate pattern)
2. Verify outputs are present and reasonable
3. Dispatch methodology reviewer (for statistical tasks)
4. Log findings to LEARNINGS.md

### Step 3: Log to LEARNINGS.md

Document every significant step:

```markdown
## Task N: [Description] - COMPLETE

**Input:** [Describe input state]

**Operation:** [What was done]

**Output:**
- Shape: [final shape]
- Key findings: [observations]

**Verification:** [How you confirmed it worked]

**Next:** [What comes next]
```

## Verification Patterns

See [references/verification-patterns.md](references/verification-patterns.md) for detailed code patterns for:
- Data loading, filtering, merging
- Aggregation and model training
- Quick reference table by operation type

## Common Failures to Avoid

| Failure | Why It Happens | Prevention |
|---------|----------------|------------|
| Silent data loss | Merge drops rows | Print row counts before/after |
| Hidden nulls | Join introduces nulls | Check null counts after joins |
| Wrong aggregation | Groupby logic error | Display sample groups |
| Type coercion | Pandas silent conversion | Verify dtypes after load |
| Off-by-one | Date filtering edge cases | Print min/max dates |

## If Output Looks Wrong

1. **STOP** - do not proceed
2. **Investigate** - print more details
3. **Document** - log the issue in LEARNINGS.md
4. **Ask** - if unclear, ask user for guidance
5. **Fix** - only proceed after output verified

**Never hide failures.** Bad output documented is better than silent failure.

## No Pause Between Tasks

<EXTREMELY-IMPORTANT>
**After completing task N, IMMEDIATELY start task N+1. You MUST NOT pause.**

| Thought | Reality |
|---------|---------|
| "Task done, should check in with user" | You're wasting context. User wants ALL tasks done. Keep going. |
| "User might want to see intermediate results" | You're assuming wrong. User will see results at the END. Continue. |
| "Natural pause point" | You're making excuses. Only pause when ALL tasks complete or you're blocked. |
| "Should summarize this step" | You're procrastinating. Summarize AFTER all tasks. Keep moving. |

**Your pausing between tasks is procrastination disguised as courtesy.**
</EXTREMELY-IMPORTANT>


### 1. Prerequisites Check

Before spawning any teammates:

1. **Verify PLAN.md** exists with task list and `Deps` column annotations
2. **Group tasks by independence:**
   - Tasks with `Deps: —` (no dependencies) can run in parallel
   - Tasks with `Deps: after N` form dependency chains — keep these sequential within one teammate
   - Group dependent chains into a single teammate assignment
3. **Verify data scope separation:**
   - Each independent task/group should analyze different datasets OR different subsets
   - If two independent tasks modify the same output files, merge them into one group (prevents conflicts)
   - Example: Analysis by year (2020, 2021, 2022) = independent. Pipeline (clean → merge → model) = sequential.
4. **Confirm at least 2 independent groups exist** — otherwise fall back to sequential

Example grouping from a PLAN.md:
```
Task 0: Data cleaning (Deps: —)        → Run sequentially FIRST (foundation task)
Task 1: Descriptive stats by region (Deps: after 0) → Teammate A
Task 2: Descriptive stats by year (Deps: after 0)   → Teammate B (parallel with A)
Task 3: Logit model (Deps: after 0)    → Teammate C (parallel with A, B)
Task 4: Probit model (Deps: after 0)   → Teammate D (parallel with A, B, C)
Task 5: Comparison table (Deps: after 3, 4) → Run sequentially AFTER (needs all results)
```

**Foundation tasks** (like data cleaning or ETL) that everything depends on must complete BEFORE spawning parallel teammates. Run these sequentially first using normal ds-delegate loops.

**Reconciliation tasks** (like comparison tables) that need all parallel results must run AFTER teammates complete.

### 2. Create Shared Task List and Enter Delegate Mode

1. **Run foundation tasks first** (any task that all others depend on) using sequential ds-delegate
2. After foundation tasks complete, create one `TaskCreate` per independent task/group:
   - Subject: `Analyze: [Task Name(s)]`
   - Description: task details, data scope, expected outputs
3. Press **Shift+Tab** to enter delegate mode — the lead coordinates, does NOT analyze
4. Spawn one teammate per task/group

### 3. Spawn Prompt Template

Each teammate receives this self-contained prompt. **Teammates start with a blank conversation and do NOT auto-load skills.** The prompt must contain everything they need.

**Before spawning, substitute these variables:**
- `TASK_NAME` → task name(s) from PLAN.md
- `TASK_DETAILS` → full task text pasted from PLAN.md (not a file reference)
- `SPEC_CONTEXT` → relevant section of SPEC.md pasted inline (objective, methodology requirements)
- `DATA_SCOPE` → specific datasets/subsets this teammate may use (prevents conflicts)
- `OUTPUT_FILES` → specific output files this teammate will create (prevents overwrites)
- `PREVIOUS_WORK` → relevant entries from LEARNINGS.md (foundation task results)
- `PLUGIN_ROOT` → resolved value of `${CLAUDE_PLUGIN_ROOT}`

```
You are implementing one analysis task as part of a data science team. You have EXCLUSIVE
ownership of the data scope and output files listed below. Do not modify outputs outside your scope.

## Your Assignment

Task: {TASK_NAME}

### Task Details (from PLAN.md)
{TASK_DETAILS}

### Analysis Objective (from SPEC.md)
{SPEC_CONTEXT}

### Previous Work (from LEARNINGS.md)
{PREVIOUS_WORK}

## Data Scope (EXCLUSIVE — do not use data outside this scope)

{DATA_SCOPE}

If you discover you need data NOT in your scope, STOP and message the lead:
"Need access to [dataset/subset] which is outside my scope. Reason: [why]."

## Output Files (EXCLUSIVE — do not modify files outside this list)

{OUTPUT_FILES}

If you need to create an output file NOT in this list, STOP and message the lead.

## Iron Law of Output-First Verification (Non-Negotiable)

**EVERY CODE STEP MUST PRODUCE VISIBLE OUTPUT. This is not negotiable.**

Before moving to the next step, you MUST:
1. Run the code
2. See the output (print, display, plot)
3. Verify output is correct/reasonable
4. Document what you observed
5. Only THEN proceed to next step

**If you're about to write code without outputting results, STOP.**

### What Output-First Means

| DO | DON'T |
|-------|----------|
| Print shape after each transform | Chain operations silently |
| Display sample rows | Trust transformations work |
| Show summary stats | Wait until end to check |
| Verify row counts | Assume merges worked |
| Check for unexpected nulls | Skip intermediate checks |
| Plot distributions | Move on without looking |

### Rationalization Prevention

| Thought | Reality |
|---------|---------|
| "I'll check at the end" | STOP — you're letting errors compound silently. Check after every step. |
| "This transform is simple" | STOP — simple code can still be wrong. Output and verify. |
| "I know merge worked" | STOP — you've assumed this before and been wrong. Check row counts. |
| "Data looks fine" | STOP — you're confusing "looks" with verification. Print stats, show samples. |
| "I'll batch the outputs" | STOP — you're about to lose your ability to isolate issues. Output per operation. |

## Step 1: Load Analysis Protocol

```
Read("{PLUGIN_ROOT}/lib/skills/ds-delegate/SKILL.md")
```

This contains the detailed output-first protocol and verification patterns.

## Step 2: Implement with Output-First Protocol

For EVERY operation (load, filter, merge, transform, model):

1. **BEFORE:** Print state (shape, head, dtypes)
2. **EXECUTE:** Run operation
3. **AFTER:** Print state (shape, nulls, sample)
4. **VERIFY:** Check output is reasonable
5. **DOCUMENT:** Note what you observed

Example:
```python
print(f"Before merge: df1={df1.shape}, df2={df2.shape}")
df = df1.merge(df2, on='key', how='left')
print(f"After merge: df={df.shape}")
print(f"Nulls introduced: {df.isnull().sum().sum()}")
print(df.head())
```

### Required Outputs by Operation

| Operation | Required Output |
|-----------|-----------------|
| Load data | shape, dtypes, head() |
| Filter | shape before/after, % removed |
| Merge/Join | shape, null check, sample |
| Groupby | result shape, sample groups |
| Model fit | metrics, convergence check |

## Step 3: Save Outputs to Your Scope

Save all analysis outputs (plots, tables, model objects) to the files in OUTPUT FILES.

Use clear naming:
- Plots: `{OUTPUT_FILES[0]}/plot_distribution.png`
- Tables: `{OUTPUT_FILES[0]}/table_summary.csv`
- Models: `{OUTPUT_FILES[0]}/model_logit.pkl`

## Step 4: Message the Lead

After completing your analysis, send a message to the lead with:

```
Finished: {TASK_NAME}

Outputs created:
- [list each file with brief description]

Data quality observations:
- [any nulls, outliers, or data issues found]
- [or "No issues" if clean]

Methodology notes:
- [any assumptions made about statistical approach]
- [or "Standard approach per spec" if straightforward]

Key findings:
- [1-3 bullet points of main results]
```

The lead uses these messages to check for methodology inconsistencies between teammates.
Do NOT message other teammates directly — the lead coordinates all cross-task communication.

## Step 5: Self-Verification Checklist

Before marking your task complete, verify ALL of the following:

- [ ] Every operation produced visible output
- [ ] All outputs saved to files in OUTPUT FILES
- [ ] Only data in DATA SCOPE was used
- [ ] No silent data loss (row counts checked before/after merges)
- [ ] No unexpected nulls introduced
- [ ] Methodology matches SPEC.md requirements (re-read spec context above)
- [ ] Key findings documented in message to lead

Only mark your task complete after all boxes pass.

## If You Encounter Issues

- **Need data outside scope:** Message lead, do NOT access it
- **Output looks wrong:** STOP, investigate, document in message to lead
- **Blocked by missing data:** Message lead: "Blocked — need [data/result] from foundation task"
- **Unclear methodology:** Message lead with specific question. Do NOT guess.
- **Code error:** Debug with output-first approach (print state at each step)
```

### 4. Lead Monitoring

While teammates analyze:

- **Watch the shared task list** for completion status and messages
- **If a teammate reports a methodology question:** Relay the answer to ALL affected teammates (e.g., "Use robust standard errors for all regressions")
- **If a teammate reports data quality issues:** Decide whether to halt parallel work and fix foundation task
- **If a teammate requests out-of-scope data:** Decide whether to expand scope or note as limitation
- **If a teammate has been working significantly longer than others:** Message them for status
- **Do NOT implement any analysis yourself** — your job is coordination and reconciliation

### 5. Reconciliation Protocol (3 Passes)

After ALL teammates mark their tasks complete, the lead performs three passes:

<EXTREMELY-IMPORTANT>
**Pass 1 — Collect & Conflicts:**

1. Read all output files created by teammates
2. Check for file conflicts:
   - Did teammates overwrite each other's outputs? (should not happen if scope separation worked)
   - Are output file names clear and non-overlapping?
3. Verify all expected outputs exist (cross-check against each teammate's completion message)
4. If outputs are missing or conflict, identify which teammate and request fix

**Pass 2 — Output Verification:**

1. For each teammate's outputs, verify:
   - Data shapes are reasonable (no unexpected empty DataFrames)
   - Summary statistics make sense (no all-zeros, no suspicious outliers)
   - Plots render correctly (no blank images)
   - Model convergence achieved (if applicable)
2. Cross-check outputs against SPEC.md requirements:
   - Did we get all the analyses requested?
   - Are output formats what spec required (tables vs plots)?
3. If outputs look wrong:
   - Identify specific issue (e.g., "Model failed to converge", "Plot shows no data")
   - Dispatch fix subagent using ds-delegate targeting the specific issue
   - Re-verify after fix

**Pass 3 — Methodology Consistency:**

1. Read each teammate's completion message (methodology notes section)
2. Check for methodology conflicts:
   - Did teammates make different assumptions about the same thing? (e.g., one used robust SE, another didn't)
   - Did teammates use different variable definitions? (e.g., one logged income, another didn't)
   - Did teammates handle nulls differently? (one dropped, another imputed)
3. Read SPEC.md methodology requirements — verify all teammates followed spec
4. If methodology conflicts found:
   - Document the conflict
   - Decide on canonical approach (from spec or user input)
   - Dispatch fix subagent to harmonize methodology
   - Re-run affected analyses

**If ANY pass fails → fix before proceeding. Do NOT skip reconciliation passes.**
</EXTREMELY-IMPORTANT>

### 6. When to Use Agent Teams

<EXTREMELY-IMPORTANT>
**DS work is MOSTLY sequential. Only use parallel mode for rare cases with true independence.**

**Use agent teams when:**
- 4+ tasks in PLAN.md with at least 2 independent groups
- Independent tasks analyze different datasets OR different subsets of same data
- Tasks create different output files (no overlap)
- Tasks are self-contained (each has own data scope and outputs)
- Examples:
  - ✅ Descriptive stats by subgroup (region A, region B, region C)
  - ✅ Model comparisons (logit, probit, random forest on same cleaned data)
  - ✅ Robustness checks (main spec, alternative spec 1, alternative spec 2)
  - ✅ Multiple visualizations (time series plot, scatter plot, correlation heatmap)

**Do NOT use agent teams when:**
- Tasks form a pipeline (clean → merge → transform → model) — this is SEQUENTIAL
- Each task depends on seeing the previous output to decide next step — this is EXPLORATORY
- Multiple tasks modify the same datasets or output files
- Fewer than 4 tasks (overhead exceeds benefit)
- Tasks require shared state that's built incrementally
- Exploratory analysis where you don't know what's needed until you see data
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is not available

**The default is sequential.** Parallel is the exception, not the rule.
</EXTREMELY-IMPORTANT>

### 7. After Reconciliation

After all three reconciliation passes complete successfully:

1. **Log consolidated results to LEARNINGS.md:**

```markdown
## Parallel Analysis Complete

**Tasks executed in parallel:**
- Task N: [Name] - Teammate A
- Task M: [Name] - Teammate B
- Task P: [Name] - Teammate C

**Outputs created:**
- [List all output files across teammates]

**Methodology:**
- [Document canonical approach used across analyses]

**Key findings:**
- [Consolidated findings from all teammates]

**Reconciliation:**
- Pass 1 (Collect): [Any conflicts? How resolved?]
- Pass 2 (Outputs): [Any issues? How fixed?]
- Pass 3 (Methodology): [Any conflicts? How harmonized?]
```

2. **Proceed to next phase** (either next sequential task or ds-review if all tasks complete)

## Gate: Exit Implementation

<EXTREMELY-IMPORTANT>
**You MUST NOT proceed to review without verifying ALL tasks are complete. This is not negotiable.**

Before invoking ds-review, execute this gate:

1. **IDENTIFY**: Read `.claude/PLAN.md` — list every task by number and name
2. **RUN**: Read `.claude/LEARNINGS.md` — find entries for each task
3. **READ**: For each task, confirm LEARNINGS.md contains:
   - A "Task N: [Name] - COMPLETE" entry
   - Verified output (shape, stats, or sample)
   - No unresolved issues flagged
4. **VERIFY**: Count tasks in PLAN.md vs completed entries in LEARNINGS.md. They MUST match.
5. **CLAIM**: Only if all tasks accounted for, proceed to review

**If ANY task is missing from LEARNINGS.md, implement it before proceeding.**

**Claiming all tasks are done without checking LEARNINGS.md against PLAN.md is LYING.**
</EXTREMELY-IMPORTANT>

## Phase Complete

After passing the exit gate, IMMEDIATELY invoke:
```
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/ds-review/SKILL.md")
```
