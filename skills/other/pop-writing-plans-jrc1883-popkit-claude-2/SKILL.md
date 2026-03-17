---
name: writing-plans
description: "Creates comprehensive implementation plans with exact file paths, complete code examples, and verification steps for engineers with zero codebase context. Assumes skilled developers who need domain-specific guidance, following DRY, YAGNI, and TDD principles. Use after brainstorming/design is complete when handing off to another developer or planning complex multi-step work. Do NOT use for simple tasks, quick fixes, or when you're implementing yourself and already understand the codebase - just start coding instead."
inputs:
  - from: pop-brainstorming
    field: design_document
    required: false
  - from: any
    field: topic
    required: false
outputs:
  - field: plan_document
    type: file_path
  - field: github_issue
    type: issue_number
  - field: task_count
    type: number
next_skills:
  - pop-executing-plans
  - pop-subagent-driven
workflow:
  file: examples/workflow-definition.yml
  description: Complete workflow definition with all decision points
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Workflow

See [examples/workflow-definition.yml](examples/workflow-definition.yml) for complete workflow with all decision points.

**Key steps:**

1. Check upstream context (from brainstorming or GitHub issue)
2. Gather requirements
3. Choose detail level (comprehensive/standard/outline)
4. Write plan with code-architect agent
5. Validate structure
6. Create/link GitHub issue
7. Offer execution choice (subagent/parallel/later)

## Plan Structure

### Document Header

See [examples/plan-template.md](examples/plan-template.md) for complete template.

Every plan must include:

- **Goal**: One sentence describing what this builds
- **Architecture**: 2-3 sentences about approach
- **Tech Stack**: Key technologies/libraries

### Task Breakdown

**Bite-sized tasks** (2-5 minutes each):

- Write failing test
- Run to verify failure
- Implement minimal code
- Run to verify pass
- Commit

Each task specifies:

- **Files**: Exact paths to create/modify/test
- **Steps**: Numbered with complete code examples
- **Commands**: Exact commands with expected output

**Template**: See [examples/plan-template.md](examples/plan-template.md) for full task structure.

## Context Integration

### Check Upstream Context

Before creating plan, check for context from previous skills (brainstorming, GitHub issues).

**Implementation**: See [examples/context-handling.md](examples/context-handling.md)

Key points:

- Load skill_context to check for design documents
- Reuse decisions already made
- Don't re-ask questions answered in brainstorming

### Save Context Output

Save plan context for downstream skills (executing-plans, subagent-driven).

**Implementation**: See [examples/context-handling.md](examples/context-handling.md)

Includes:

- Plan file path
- Task count
- GitHub issue number
- Link to workflow

## GitHub Integration

After plan created, integrate with GitHub for tracking:

**Search for existing issue:**

```bash
gh issue list --search "<topic>" --state open --json number,title --limit 5
```

**Offer choices** via AskUserQuestion:

- Create new issue with plan summary and task checklist
- Link to existing issue number
- Skip GitHub tracking

**Issue creation**: See [examples/context-handling.md](examples/context-handling.md) for template.

## Execution Handoff

After saving plan, use AskUserQuestion to offer execution choice:

**Options:**

1. **Subagent-Driven**: Execute in this session with fresh subagent per task
2. **Parallel Session**: Open new session with executing-plans skill
3. **Later**: Save for manual execution

**NEVER** present as plain text like "1. Subagent, 2. Parallel... type 1 or 2". Always use AskUserQuestion tool.

**If Subagent-Driven chosen:**

- Use subagent-driven-development skill
- Stay in this session
- Fresh subagent per task + code review
- Context automatically passed

**If Parallel Session chosen:**

- Guide user to open new session in worktree
- New session uses executing-plans skill
- Context available via `.popkit/context/current-workflow.json`

## Quality Guidelines

**Always include:**

- Exact file paths (not "add to utils folder")
- Complete code examples (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax

**Principles:**

- DRY (Don't Repeat Yourself)
- YAGNI (You Aren't Gonna Need It)
- TDD (Test-Driven Development)
- Frequent commits (after each passing test)

## Related Skills

- **pop-brainstorming**: Upstream - provides design document input
- **pop-executing-plans**: Downstream - executes plan task-by-task
- **pop-subagent-driven**: Downstream - executes with fresh subagent per task
- **pop-code-architect**: Called internally - writes the actual plan

## Examples

See [examples/](examples/) directory for:

- Complete workflow definition
- Plan document template
- Task structure template
- Context handling code
- GitHub integration examples

---

**Version**: 1.0.0
**Category**: Development Workflow
**Tier**: Core
