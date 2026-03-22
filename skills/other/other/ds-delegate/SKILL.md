---
name: ds-delegate
description: "Subagent delegation for data analysis. Dispatches fresh Task agents with output-first verification."
user-invocable: false
disable-model-invocation: true
hooks:
  PostToolUse:
    - matcher: "Agent"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-post-subagent-guard.py"
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-read-after-subagent-guard.py"
    - matcher: "Grep"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-read-after-subagent-guard.py"
    - matcher: "Glob"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-read-after-subagent-guard.py"
---


## Contents

- [The Iron Law of Delegation](#the-iron-law-of-delegation)
- [Core Principle](#core-principle)
- [The Process](#the-process)
- [Drive-Aligned Framing](#drive-aligned-framing)
- [Rationalization Prevention](#rationalization-prevention)

<EXTREMELY-IMPORTANT>
## The Iron Law of Delegation

**YOU MUST route EVERY ANALYSIS STEP THROUGH A TASK AGENT. This is not negotiable.**

You MUST NOT:
- Write analysis code directly
- Run "quick" data checks
- Edit notebooks or scripts
- Make "just this one plot"

**If you're about to write analysis code in main chat, STOP. Spawn a Task agent instead.**
</EXTREMELY-IMPORTANT>

## Core Principle

**Fresh subagent per task + output-first verification = reliable analysis**

- Analyst subagent does the work
- Must produce visible output at each step
- Methodology reviewer checks approach
- Loop until output verified

## When to Use

Called by `ds-implement` for each task in PLAN.md. Don't invoke directly.

## The Process

```
For each task:
    1. Dispatch analyst subagent
       - If questions → answer, re-dispatch
       - Implements with output-first protocol
    2. Verify outputs are present and reasonable
    3. Dispatch methodology reviewer (if complex)
    4. Mark task complete, log to LEARNINGS.md
```

## Task Type Detection

Each task in PLAN.md should have a `type` field. Detect and route accordingly:

| Task Type | Agent | Constraints | Example Tasks |
|-----------|-------|-------------|---------------|
| `engineering` | `workflows:ds-engineer` | ds-engineering-constraints.md index + atomic E1-E5 files | ETL, merge, clean, transform, pipeline, schema, join |
| `analysis` | `workflows:ds-analyst` | ds-analysis-constraints.md index + atomic A1-A7 files | regression, test, model, visualize, estimate, summarize |

**Detection heuristic (when type field is missing):**

| Task contains these keywords | Type |
|------------------------------|------|
| merge, join, clean, ETL, transform, pipeline, ingest, schema, deduplicate, normalize | engineering |
| regression, estimate, test, model, plot, chart, visualize, summarize, correlate, panel | analysis |
| ambiguous | Default to `analysis` (safer — analysis constraints are stricter) |

## Step 1: Dispatch Analyst/Engineer

**Pattern:** Use structured delegation template from `references/delegation-template.md`

Every delegation MUST include:
1. TASK - What to analyze
2. EXPECTED OUTCOME - Success criteria
3. REQUIRED SKILLS - Statistical/ML methods needed
4. REQUIRED TOOLS - Data access and analysis tools
5. MUST DO - Output-first verification
6. MUST NOT DO - Methodology violations
7. CONTEXT - Data sources and previous work
8. VERIFICATION - Output requirements

Use this Task invocation (fill in brackets). **Route based on task type detected above:**

*All paths below are relative to this skill's base directory.*

**For `analysis` tasks:**
```
Task(subagent_type="workflows:ds-analyst", prompt="""
# TASK

Analyze: [TASK NAME]

## EXPECTED OUTCOME

You will have successfully completed this task when:
- [ ] [Specific analysis output 1]
- [ ] [Specific analysis output 2]
- [ ] Output-first verification at each step
- [ ] Results documented with evidence

## REQUIRED SKILLS

This task requires:
- [Statistical method]: [Why needed]
- [Programming language]: Data manipulation
- Output-first verification (mandatory)
- SQL reference: Read `../ds-delegate/references/sql-patterns.md` for dialect-specific patterns
- Data quality checks: Read `../ds-implement/references/ds-checks.md` for DQ1-DQ6 verification patterns (mandatory)
- Analysis constraints: Read `${CLAUDE_SKILL_DIR}/../../references/ds-analysis-constraints.md` for the constraint index, then load:
  Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-robustness-checks.md`
  Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-standard-error-spec.md`
  Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-visualization-integrity.md`
- Analysis conventions: Read `${CLAUDE_SKILL_DIR}/../../references/ds-common-conventions.md` for the convention index, then load:
  Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-statistical-validity.md`
  Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-p-hacking-prevention.md`
  Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-sample-selection.md`
  Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-deviation-rules-analysis.md`

## REQUIRED TOOLS

You will need:
- Read: Load datasets and existing code
- Write: Create analysis scripts/notebooks
- Bash: Run analysis and verify outputs

**Tools denied:** None (full analysis access)

## MUST DO

- [ ] Print state BEFORE each operation (shape, head)
- [ ] Print state AFTER each operation (nulls, sample)
- [ ] Verify outputs are reasonable at each step
- [ ] Document methodology decisions

## MUST NOT DO

- ❌ Skip verification outputs
- ❌ Proceed with questionable data without flagging
- ❌ Guess on methodology (ask if unclear)
- ❌ Claim completion without visible outputs

## CONTEXT

### Task Description
[PASTE FULL TASK TEXT FROM PLAN.md]

### Analysis Context
- Analysis objective: [from SPEC.md]
- Data sources: [list with paths]
- Previous steps: [summary from LEARNINGS.md]

## Output-First Protocol (MANDATORY)
For EVERY operation:
1. Print state BEFORE (shape, head)
2. Execute operation
3. Print state AFTER (shape, nulls, sample)
4. Verify output is reasonable

Example:
```python
print(f"Before: {df.shape}")
df = df.merge(other, on='key')
print(f"After: {df.shape}")
print(f"Nulls introduced: {df.isnull().sum().sum()}")
df.head()
```

## Required Outputs by Operation
| Operation | Required Output |
|-----------|-----------------|
| Load data | shape, dtypes, head() |
| Filter | shape before/after, % removed |
| Merge/Join | shape, null check, sample |
| Groupby | result shape, sample groups |
| Model fit | metrics, convergence |

## If Unclear
Ask questions BEFORE implementing. Don't guess on methodology.

## Output
Report: what you did, key outputs observed, any data quality issues found.
""")
```

**For `engineering` tasks:**
```
Task(subagent_type="workflows:ds-engineer", prompt="""
# TASK

Engineer: [TASK NAME]

## EXPECTED OUTCOME

You will have successfully completed this task when:
- [ ] [Specific engineering output 1]
- [ ] [Specific engineering output 2]
- [ ] Output-first verification at each step
- [ ] Results documented with evidence

## REQUIRED SKILLS

This task requires:
- [Engineering method]: [Why needed]
- [Programming language]: Data manipulation
- Output-first verification (mandatory)
- SQL reference: Read `../ds-delegate/references/sql-patterns.md` for dialect-specific patterns
- Data quality checks: Read `../ds-implement/references/ds-checks.md` for DQ1-DQ6 verification patterns (mandatory)
- Engineering constraints: Read `${CLAUDE_SKILL_DIR}/../../references/ds-engineering-constraints.md` for the constraint index, then load:
  Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-determinism.md`
  Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-schema-contracts.md`
  Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-join-audits.md`
  Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-idempotency.md`
  Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-error-handling.md`

## REQUIRED TOOLS

You will need:
- Read: Load datasets and existing code
- Write: Create ETL scripts/pipelines
- Bash: Run transformations and verify outputs

**Tools denied:** None (full engineering access)

## MUST DO

- [ ] Print state BEFORE each operation (shape, head)
- [ ] Print state AFTER each operation (nulls, sample)
- [ ] Verify schema contracts at each step
- [ ] Validate determinism (same input → same output)
- [ ] Check join key uniqueness before merging
- [ ] Document pipeline decisions

## MUST NOT DO

- ❌ Skip verification outputs
- ❌ Proceed with non-deterministic transforms without flagging
- ❌ Introduce silent data loss (row drops without logging)
- ❌ Claim completion without visible outputs

## CONTEXT

### Task Description
[PASTE FULL TASK TEXT FROM PLAN.md]

### Engineering Context
- Pipeline objective: [from SPEC.md]
- Data sources: [list with paths]
- Previous steps: [summary from LEARNINGS.md]

## Output-First Protocol (MANDATORY)
For EVERY operation:
1. Print state BEFORE (shape, head)
2. Execute operation
3. Print state AFTER (shape, nulls, sample)
4. Verify output is reasonable

Example:
```python
print(f"Before: {df.shape}")
df = df.merge(other, on='key')
print(f"After: {df.shape}")
print(f"Nulls introduced: {df.isnull().sum().sum()}")
df.head()
```

## Required Outputs by Operation
| Operation | Required Output |
|-----------|-----------------|
| Load data | shape, dtypes, head() |
| Filter | shape before/after, % removed |
| Merge/Join | shape, null check, key uniqueness |
| Transform | before/after sample, determinism check |
| Pipeline step | input shape → output shape, schema validation |

## If Unclear
Ask questions BEFORE implementing. Don't guess on architecture.

## Output
Report: what you did, key outputs observed, any data quality or schema issues found.
""")
```

**If agent asks questions:** Answer clearly, especially about methodology choices (analysis) or architecture decisions (engineering).

**If agent completes task:** Verify outputs, then proceed or review.

## Step 2: Verify Outputs (Post-Subagent Boundary)

<EXTREMELY-IMPORTANT>
**After analyst returns, you are at the post-subagent boundary. Constraints C5 from ds-common-constraints.md apply.**

**ALLOWED (Verification):**
- [ ] Read the analyst's returned report/summary
- [ ] Check LEARNINGS.md for output documentation
- [ ] Confirm output files exist (`ls -la`)
- [ ] Compare task counts (expected vs actual)

**FORBIDDEN (Investigation):**
- ❌ Read project source code, notebooks, or data files
- ❌ Run analysis code to "confirm" results
- ❌ Query databases or inspect intermediate files
- ❌ Grep/Glob project files

**If the analyst's report shows problems, re-dispatch a Task agent. Do NOT investigate yourself.**
</EXTREMELY-IMPORTANT>

Upon verification failure, re-dispatch analyst with specific fix instructions.

## Step 3: Dispatch Methodology Reviewer (Complex Tasks)

For statistical analysis, modeling, or methodology-sensitive tasks, dispatch a methodology reviewer. **Tailor the review checklist to the task type:**

```
Task(subagent_type="general-purpose",
  allowed_tools=["Read", "Glob", "Grep", "Bash(read-only)"],
  prompt="""
Review methodology for: [TASK NAME]
Task type: [engineering | analysis]

## What Was Done
[SUMMARY FROM ANALYST/ENGINEER OUTPUT]

## Original Requirements
[FROM SPEC.md - especially any replication requirements]

**Tool Restrictions:** The methodology reviewer is READ-ONLY. It reads code, verifies outputs, and returns a verdict. It MUST NOT use Write or Edit.

## CRITICAL: Do Not Trust the Report

The agent may have:
- Reported success without actually running the code
- Cherry-picked output that looks correct
- Glossed over data quality issues
- Made methodology choices without justification

**DO:**
- Read the actual code or notebook cells
- Verify outputs exist and match claims
- Check for silent failures (empty DataFrames, all nulls)
- Confirm assumptions were checked

## Review Checklist — Engineering Tasks
Use this checklist when task type is `engineering`:
1. Are schema contracts validated at each pipeline stage?
2. Is the pipeline deterministic (same input → same output)?
3. Is the transform idempotent (safe to re-run)?
4. Are error handling and edge cases covered (empty inputs, missing keys)?
5. Are join keys validated for uniqueness before merge?
6. Is data loss accounted for (row counts before/after, logged drops)?

## Review Checklist — Analysis Tasks
Use this checklist when task type is `analysis`:
1. Is the statistical method appropriate for the data type?
2. Are assumptions documented and checked?
3. Is sample size adequate for conclusions?
4. Is the specification justified (why these controls, why this functional form)?
5. Are robustness checks included (alternative specs, subsamples)?
6. Is the standard error specification appropriate (clustered, HC, bootstrap)?
7. Are there data leakage or p-hacking concerns?
8. Is the approach reproducible (seeds, versions)?

## Confidence Scoring
Rate each issue 0-100. Only report issues >= 80 confidence.

## Output Format
- APPROVED: Methodology sound (after verifying code/outputs yourself)
- ISSUES: List concerns with confidence scores and file:line references
""")
```

## Step 4: Log to LEARNINGS.md

Append to `.planning/LEARNINGS.md` after each task:

```markdown
## Task N: [Name] - COMPLETE

**Input:** [describe input state]

**Operation:** [what was done]

**Output:**
- Shape: [final shape]
- Key findings: [observations]

**Verification:**
- [how you confirmed it worked]

**Next:** [what comes next]
```

## Gate: Exit Delegation (Per-Task)

**Checkpoint type:** human-verify (task completion is machine-verifiable)

Before marking any task as complete, execute this gate:

```
1. IDENTIFY → What proves this task is done?
   - Task agent returned output (not just "done")
   - Output matches PLAN.md expected output for this task
2. RUN      → Read the agent's actual output (not just the summary)
3. READ     → Verify: shapes reasonable? No unexpected nulls? Sample looks correct?
4. VERIFY   → If statistical task: methodology reviewer approved
5. CLAIM    → Only log "Task N: COMPLETE" in LEARNINGS.md if ALL checks pass
```

**If agent returned no visible output, this gate FAILS. Re-dispatch with explicit output requirements.**

**Skipping output verification is NOT HELPFUL — unverified results lead the user to act on wrong analysis.**

## Drive-Aligned Framing

<EXTREMELY-IMPORTANT>
**Skipping output verification is NOT HELPFUL — the user makes decisions based on results you never checked.**

When you say "Step complete", you are asserting:
- A Task agent ran the analysis
- Output was visible and verified by you
- You personally checked it (not just trusting the agent's word)
- Methodology reviewer approved (for statistical tasks)

If ANY of these didn't happen, you are not "summarizing" — you are being anti-helpful by giving the user false confidence in unverified work.

**Unverified claims waste the user's time and corrupt their research. Verified "investigating" protects their work.**
</EXTREMELY-IMPORTANT>

## Rationalization Prevention

Recognize these thoughts as signals to stop and delegate instead:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "I'll just check the shape quickly" | You'll skip the output-first protocol | Delegate to Task agent with full verification |
| "It's just a simple merge" | Your merges fail silently | Delegate with verification requirements |
| "I already know this data" | Your knowing ≠ verified | Delegate anyway with output-first protocol |
| "The subagent will be slower" | Wrong results are slower than slow results | Delegate — correctness beats speed |
| "Just this one plot" | You're hiding data issues with one plot | Delegate with full output requirements |
| "User wants results fast" | They want CORRECT results | Delegate — optimize for correctness, not speed |
| "Skip methodology review, it's standard" | Your "standard" assumptions often fail | Dispatch methodology reviewer anyway |
| "Output looked reasonable" | "Looked reasonable" ≠ verified | Check the actual numbers against expectations |

### Drive-Aligned Framing

| Shortcut | Consequence |
|----------|-------------|
| Delegating without context | You spawned a task agent without SPEC/PLAN context. It guesses wrong — your delegation created confusion. |
| Skipping verification of agent output | You trusted the agent's claim of completion. The output is wrong — your trust was negligence. |

### Delete & Restart

**If you wrote analysis code in the main chat instead of delegating to a task agent, DELETE it immediately and dispatch a Task agent.**

Code written in main chat is contaminated by orchestrator context, skips the output-first protocol, and bypasses methodology review. It cannot be salvaged — it must be replaced.

## Red Flags

**If you catch yourself thinking these, STOP immediately:**

- "I can skip output verification this time"
- "I'll chain operations together, it's fine"
- "Unexpected nulls are probably okay"
- "Methodology review takes too long, skip it"
- "The merge probably worked"
- "Output-first protocol is overkill here"
- "I'll just summarize PLAN.md for the analyst" (STOP—provide full text)

**When analyst produces no visible output:**
- You must re-dispatch with explicit output requirements
- Treat this as a hard failure, not something to work around

**When analyst fails a task:**
- You must dispatch a fix subagent with specific instructions
- Don't fix it yourself in main chat—you'll pollute context and hide the real issue

## Example Flow

```
Me: Implementing Task 1: Load and clean transaction data

[Dispatch analyst with full task text]

Analyst:
- Loaded transactions.csv: (50000, 12)
- Found 5% nulls in amount column
- "Should I drop or impute nulls?"

Me: "Impute with median, flag imputed rows"

[Re-dispatch with answer]

Analyst:
- Imputed 2,500 rows with median ($45.50)
- Added is_imputed flag column
- Final shape: (50000, 13)
- Sample output: [shows head with flag]

[Verify: shapes match, flag exists, no unexpected changes]

[Log to LEARNINGS.md]

[Mark Task 1 complete, move to Task 2]
```

## Model Tier Hints

When dispatching subagents, match model capability to task complexity. This is **advisory** -- Claude Code doesn't yet support model routing -- but documents intent for cost-aware delegation.

| Task Complexity | Model Tier | Signals | Example |
|----------------|------------|---------|---------|
| **Mechanical** | Cheapest capable | Data loading, simple filtering, descriptive stats, file format conversion | "Load CSV and compute summary statistics" |
| **Integration** | Standard | Merges/joins across sources, aggregations, visualization, data reshaping | "Merge transaction and customer tables, create pivot summary" |
| **Architecture/Review** | Most capable | Feature engineering strategy, model selection, statistical assumption validation, methodology review | "Select appropriate model family and validate distributional assumptions" |

**Complexity signals:**
- Reads/writes 1 file with clear spec -> mechanical
- Joins/reshapes across sources or produces visualizations -> integration
- Requires statistical judgment or methodology design -> architecture

**When in doubt, use the standard tier.** Over-allocating is wasteful; under-allocating produces poor results.

## Integration

This skill is invoked by `ds-implement` during the output-first implementation phase.
After all tasks complete, `ds-implement` proceeds to `ds-review`.
