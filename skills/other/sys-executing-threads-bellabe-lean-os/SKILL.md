---
name: sys-executing-threads
description: Writes agent outputs to numbered thread stage files. Called by agents after domain work completes. Maps agent type to stages, updates frontmatter status, and records completion metadata. Stage 1 (1-input.md) is never written by this skill.
triggers: write thread, complete stage, update thread, record output
allowed-tools: Read, Write, Glob
license: Complete terms in LICENSE.txt
---

# Thread Executor

Write agent outputs to thread stage files using the numbered convention.

## Responsibility

Accept agent outputs and write them to the correct numbered stage files in a thread directory. Update frontmatter to track completion.

## Thread File Convention

```
threads/{domain}/{thread-name}/
├── 1-input.md          # Goal context (written by sys-activating-goals, NEVER by this skill)
├── 2-hypothesis.md     # Approach, assumptions, expected outcomes
├── 3-implication.md    # If hypothesis true, what follows
├── 4-decision.md       # Chosen course of action
├── 5-actions.md        # Execution steps and status
└── 6-learning.md       # Outcomes, insights, improvements
```

## Agent-to-Stage Mapping

| Type | Stages Written | Agents |
|------|---------------|--------|
| planning | 2, 3, 4 | mkt-strategist, sls-strategist |
| execution | 5, 6 | mkt-campaign-manager, sls-outbound-manager, cst-advocacy-manager |
| spec | 2, 3, 4, 5 | prd-engineer, prd-growth-engineer |
| full-cycle | 2, 3, 4, 5, 6 | ops-manager |
| lifecycle | 2, 4, 5, 6 | cst-success-manager, cst-expansion-manager, cst-retention-manager |
| content | 2, 5 | mkt-content-manager, sls-enablement-manager |
| inbound | 2, 3, 5 | mkt-inbound-manager |
| partnership | 2, 4, 5, 6 | sls-partner-manager |

## Input

The calling agent provides:

```yaml
thread_path: threads/{domain}/{thread-name}
agent_name: {agent that produced the output}
agent_type: planning | execution | spec | full-cycle | lifecycle | content | inbound | partnership
outputs:
  hypothesis: |    # Stage 2 content (if in agent's stages)
    ...
  implication: |   # Stage 3 content
    ...
  decision: |      # Stage 4 content
    ...
  actions: |       # Stage 5 content
    ...
  learning: |      # Stage 6 content
    ...
```

## Process

### Step 1: Validate Thread

```
1. Confirm thread_path exists
2. Confirm 1-input.md exists (thread was properly activated)
3. Read 1-input.md frontmatter for thread_id and goal_id
```

### Step 2: Determine Stages

```
1. Look up agent_type in mapping table
2. Get list of stage numbers to write
3. Confirm agent provided content for each stage
```

### Step 3: Write Stage Files

For each stage in the agent's mapping:

```
1. Create stage file with frontmatter:
   - status: completed
   - completed_by: {agent_name}
   - completed_at: {YYYY-MM-DD}
2. Write agent output as file body
3. Save file
```

### Step 4: Verify

```
1. Confirm all mapped stages have status: completed
2. Return summary of stages written
```

## Frontmatter

Stage files are created by this skill (not pre-existing). Each file gets:

```yaml
---
status: completed
completed_by: mkt-strategist
completed_at: 2026-02-01
---
```

For `4-decision.md` specifically:
```yaml
---
status: completed
decided_by: mkt-strategist
decided_at: 2026-02-01
---
```

For `5-actions.md` specifically:
```yaml
---
status: completed
started_at: 2026-02-01
completed_at: 2026-02-01
---
```

## Stage Content Guidelines

### 2-hypothesis.md

Agent fills:
- Approach section with strategy/methodology
- Expected Outcome with measurable targets
- Key Assumptions table
- Risks table

### 3-implication.md

Agent fills:
- If Hypothesis Succeeds with quantified impact
- If Hypothesis Fails with fallback plan
- Decision Criteria table with thresholds

### 4-decision.md

Agent fills:
- Chosen Action with explicit commitment
- Rationale linking back to hypothesis
- Trade-offs table
- Approval gate (if impact >= 0.8)

### 5-actions.md

Agent fills:
- Execution Plan table with steps, owners, due dates
- Progress Log (updated during execution)
- Blockers (if any)

### 6-learning.md

Agent fills:
- Outcome (expected vs actual)
- What Worked list
- What Didn't Work list
- Key Insights
- Process Improvements
- Recommendations

## Output

```yaml
execution_summary:
  thread_path: threads/{domain}/{thread-name}
  agent: {agent_name}
  type: {agent_type}
  stages_written: [2, 3, 4]  # example for planning type
  completed_at: 2026-02-01
  status: all_stages_written | partial
```

## Integration

### Upstream

- All thread-routable agents: Produce outputs then call this skill
- `sys-activating-goals`: Creates thread with 1-input.md (prerequisite)

### Downstream

- `sys-tracking-goals`: Reads completed stages to assess progress
- `6-learning.md`: Feeds back into goal tracking and loop detection

## Constraints

**This skill NEVER:**
- Writes to `1-input.md` (owned by sys-activating-goals)
- Creates thread directories (owned by sys-activating-goals)
- Executes domain work (agents do)
- Skips stages in the agent's mapping

**This skill ALWAYS:**
- Validates thread exists before writing
- Updates frontmatter status on every stage file
- Records which agent completed each stage
- Returns execution summary
