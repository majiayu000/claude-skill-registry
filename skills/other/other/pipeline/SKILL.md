---
name: pipeline
description: |
  Orchestration pattern for sequential, dependent tasks. When work must flow
  through stages where each stage depends on the previous (design → implement →
  test → review), structure as a pipeline with explicit handoffs. Each stage
  completes before the next begins.
allowed-tools: |
  bash: ls, cat, grep
  file: read, write
  mcp: task
---

# Pipeline

<purpose>
Some tasks are inherently sequential - you can't test what isn't built, can't
build what isn't designed, can't review what isn't complete. This elixir
enforces pipeline discipline: define stages, ensure clean handoffs, and never
skip ahead.
</purpose>

## When To Activate

Trigger when:

- Task has natural phases that must happen in order
- Output of one stage is input to the next
- Skipping stages would cause problems
- User describes multi-phase work ("first X, then Y, then Z")
- Work involves: plan → implement → verify pattern

Do NOT trigger for:

- Independent tasks (use fan-out instead)
- Single-stage work
- Exploratory work with no clear sequence

## The Pattern

```
[Input] → [Stage 1] → [Handoff] → [Stage 2] → [Handoff] → [Stage 3] → [Output]
              │                        │                        │
              └── Checkpoint ──────────┴── Checkpoint ──────────┘
```

## Instructions

### Step 1: Define the Pipeline

Map out all stages:

```
Pipeline: [Task Name]

Stages:
1. [Stage Name] - [What happens] - [Output artifact]
2. [Stage Name] - [What happens] - [Output artifact]
3. [Stage Name] - [What happens] - [Output artifact]

Dependencies:
- Stage 2 requires: [Stage 1 output]
- Stage 3 requires: [Stage 2 output]
```

### Step 2: Define Checkpoints

Each stage needs exit criteria:

```
Stage 1 checkpoint:
- [ ] [Exit criterion 1]
- [ ] [Exit criterion 2]
- [ ] Artifact produced: [what]

Stage 2 checkpoint:
- [ ] [Exit criterion 1]
- [ ] Receives: [Stage 1 artifact]
- [ ] Artifact produced: [what]
```

### Step 3: Execute Stage by Stage

For each stage:

```
═══════════════════════════════════════
STAGE [N]: [Name]
═══════════════════════════════════════

Input: [What this stage receives]

[Execute stage work]

Checkpoint:
- [✓/✗] Criterion 1
- [✓/✗] Criterion 2

Output: [What this stage produces]

[If all criteria pass] → Proceed to Stage N+1
[If any criterion fails] → Stop and resolve
```

### Step 4: Handoff Protocol

Between stages, explicit handoff:

```
──────────────────────────────────────
HANDOFF: Stage [N] → Stage [N+1]
──────────────────────────────────────

Passing:
- [Artifact 1]: [description]
- [Artifact 2]: [description]

Context for next stage:
- [Key decision made]
- [Constraint to maintain]
- [Risk to watch for]
──────────────────────────────────────
```

### Step 5: Pipeline Completion

When all stages complete:

```
═══════════════════════════════════════
PIPELINE COMPLETE: [Task Name]
═══════════════════════════════════════

Stages completed: [N/N]

Final output:
[Description of what was produced]

Artifacts:
- [Final deliverable 1]
- [Final deliverable 2]

Summary:
- Stage 1: [Brief outcome]
- Stage 2: [Brief outcome]
- Stage 3: [Brief outcome]
```

## Common Pipeline Templates

<templates>
**Feature Development**
```
1. Design    → Spec document
2. Implement → Working code
3. Test      → Passing tests
4. Review    → Approved PR
```

**Bug Fix**
```
1. Reproduce → Consistent repro steps
2. Diagnose  → Root cause identified
3. Fix       → Code change
4. Verify    → Bug no longer occurs
```

**Refactoring**
```
1. Assess    → Impact analysis
2. Prepare   → Tests in place
3. Refactor  → Code changed
4. Validate  → Tests still pass
```

**Documentation**
```
1. Outline   → Structure defined
2. Draft     → Content written
3. Review    → Feedback incorporated
4. Publish   → Live documentation
```
</templates>

## Handling Stage Failures

<failure-handling>
When a stage fails:

1. **Stop the pipeline** - Don't proceed with bad input
2. **Diagnose the failure** - What went wrong?
3. **Options:**
   - Fix and retry current stage
   - Roll back to previous stage
   - Abort pipeline with partial results

```
STAGE FAILURE: [Stage Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Failed criterion: [What didn't pass]
Reason: [Why it failed]

Options:
A) Retry after fixing [specific issue]
B) Roll back to [previous stage]
C) Abort - partial output available

Recommendation: [A/B/C] because [reason]
```
</failure-handling>

## NEVER

- Skip stages, even when "obvious" they'll pass
- Proceed without explicit checkpoint verification
- Let failures cascade to later stages
- Lose context between stages (use handoff protocol)
- Run stages in parallel (use fan-out for that)

## ALWAYS

- Define all stages before starting
- Verify checkpoint criteria explicitly
- Document handoffs with context
- Stop on stage failure
- Report pipeline status at completion

## Examples

### Example 1: Feature Implementation

User: "Add password reset functionality"

```
Pipeline: Password Reset Feature

Stages:
1. Design    → Security spec, API contract
2. Implement → Endpoint, email service, token handling
3. Test      → Unit tests, integration tests
4. Review    → Security review, code review

═══════════════════════════════════════
STAGE 1: Design
═══════════════════════════════════════

[Produces security spec covering token expiry,
rate limiting, email verification]

Checkpoint:
- [✓] Security requirements defined
- [✓] API contract specified
- [✓] Edge cases documented

Output: Design spec

──────────────────────────────────────
HANDOFF: Design → Implement
──────────────────────────────────────

Passing: Design spec
Context: Tokens expire in 1 hour, max 3 attempts/hour

═══════════════════════════════════════
STAGE 2: Implement
═══════════════════════════════════════

[Implements based on spec]

...continues through all stages...
```

### Example 2: Debugging Pipeline

User: "Users are seeing 500 errors on checkout"

```
Pipeline: Checkout 500 Error Fix

Stages:
1. Reproduce → Consistent repro steps
2. Diagnose  → Root cause found
3. Fix       → Code change
4. Verify    → Error resolved

═══════════════════════════════════════
STAGE 1: Reproduce
═══════════════════════════════════════

Attempting to reproduce...

Checkpoint:
- [✓] Error reproduced locally
- [✓] Consistent reproduction steps documented

Output: Repro steps - 500 occurs when cart has
item with null price field

──────────────────────────────────────
HANDOFF: Reproduce → Diagnose
──────────────────────────────────────

Passing: Repro steps
Context: Only occurs with specific data condition

...continues...
```

<failed-attempts>
What DOESN'T work:
- Skipping reproduce stage: "I think I know what's wrong" → fixes wrong thing
- Soft checkpoints: "Probably good enough" → issues cascade
- No handoff context: Next stage misses critical constraints
- Parallelizing dependent stages: Race conditions, inconsistent results
</failed-attempts>

## Why This Elixir Exists

Sequential work needs sequential discipline. The temptation is to skip ahead -
"I'll just start coding and figure out the design as I go." This leads to
rework, bugs, and frustration.

Pipelines force the discipline: complete each stage before moving on. It feels
slower but is faster in total time because you don't backtrack.

The checkpoint isn't bureaucracy - it's the moment where you catch problems
before they become expensive.
