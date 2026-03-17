---
name: executing-plans
description: "Controlled batch execution of implementation plans with review checkpoints between phases. Loads plan, critically reviews for issues, executes tasks in batches, then pauses for architect feedback before continuing. Use when you have a complete implementation plan from brainstorming/writing-plans and want structured execution with quality gates. Do NOT use for ad-hoc implementation, exploratory coding, or when you don't have a formal plan - just implement directly with code review at the end."
inputs:
  - from: pop-writing-plans
    field: plan_path
    required: true
  - from: any
    field: batch_size
    required: false
outputs:
  - field: tasks_completed
    type: number
  - field: verification_status
    type: string
  - field: github_issue
    type: issue_number
next_skills:
  - pop-finishing-a-development-branch
  - pop-session-capture
workflow:
  file: examples/workflow-definition.yml
  description: Complete workflow with review checkpoints and feedback loops
---

# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## Workflow

See [examples/workflow-definition.yml](examples/workflow-definition.yml) for complete workflow.

**Key phases:**

1. Load and critically review plan
2. Execute batch (default: 3 tasks)
3. Report results and get feedback
4. Continue, revise, or pause based on feedback
5. Complete with finishing-a-development-branch
6. Present next action options (Issue #118)

## Execution Process

See [examples/batch-execution-guide.md](examples/batch-execution-guide.md) for detailed process.

**Key points:**

- **Default batch size**: 3 tasks
- **Checkpoint after each batch**: Report and wait for feedback
- **TodoWrite integration**: Track progress through tasks
- **Verification**: Run all verification steps as specified in plan
- **Stop when blocked**: Ask for help, don't guess

## PDF Plan Support

Plans can be provided as Markdown or PDF format.

See [examples/pdf-plan-support.md](examples/pdf-plan-support.md) for PDF processing details.

**Supported formats:**

- Markdown implementation plans
- PDF implementation plans
- PDF PRDs (for context)

## Quality Gates

**Stop and ask for help when:**

- Plan has concerns or gaps before starting
- Hit blocker mid-batch (missing dependency, failing test, unclear instruction)
- Verification fails repeatedly
- Don't understand an instruction

**Don't force through blockers** - ask for clarification.

## Batch Feedback

After each batch, use AskUserQuestion with options:

- **Continue**: Proceed to next batch
- **Revise**: Apply feedback to current batch
- **Pause**: Stop and save progress

See [examples/batch-execution-guide.md](examples/batch-execution-guide.md) for templates.

## Next Action Loop (Issue #118)

**CRITICAL**: After completion, ALWAYS present next actions:

- Work on another issue
- Run tests/checks
- Session capture and exit

**NEVER end without presenting next step options.**

See [examples/batch-execution-guide.md](examples/batch-execution-guide.md#step-6-next-action-loop-critical---issue-118) for implementation.

## Integration

**Upstream skills:**

- **pop-writing-plans**: Provides implementation plan
- **pop-brainstorming**: Provides design context

**Downstream skills:**

- **pop-finishing-a-development-branch**: Called after all tasks complete
- **pop-session-capture**: Called when pausing execution

**Internal agents:**

- **code-explorer**: Loads and parses plans
- **code-architect**: Reviews plans and implements tasks
- **test-writer-fixer**: Runs verification steps

## Related Skills

- **pop-writing-plans**: Create the implementation plan
- **pop-finishing-a-development-branch**: Complete development after tasks done
- **pop-session-capture**: Save progress when pausing
- **pop-subagent-driven**: Alternative execution with fresh subagent per task

## Remember

- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess

---

**Version**: 1.0.0
**Category**: Development Workflow
**Tier**: Core
