---
name: faion-make-tasks
description: "Create tasks from SDD documents (spec + design + implementation plan). Uses faion-task-creator-agent agent for deep research."
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, Task, TodoWrite, AskUserQuestion
---

# SDD Make Tasks Skill

**Communication with user: User's language. Task content: English.**

## Purpose

Create implementation tasks from SDD documents using the `faion-task-creator-agent` agent.

## Input

- `project`: Project name
- `feature`: Feature name
- OR `description`: Free-form task description (legacy mode)

## Modes

### SDD Mode (Primary)
When project/feature specified:
1. Load spec, design, implementation-plan
2. Verify documents approved
3. Create tasks per implementation-plan
4. Review with faion-tasks-reviewer-agent

### Free Mode (Legacy)
When description provided:
1. Clarify requirements with user
2. Research codebase
3. Plan task structure
4. Create tasks

## SDD Mode Workflow

```
1. Load SDD documents
   ↓
2. Verify: spec approved? design approved?
   ↓
3. Check/create implementation-plan
   ↓
4. For each task in plan:
   ↓
   Call faion-task-creator-agent agent
   ↓
5. Run faion-tasks-reviewer-agent (4-pass)
   ↓
6. Report results
```

## Document Verification

Check these files exist and are approved:
```
aidocs/sdd/{project}/features/{status}/{feature}/spec.md
aidocs/sdd/{project}/features/{status}/{feature}/design.md
aidocs/sdd/{project}/features/{status}/{feature}/implementation-plan.md
```

If implementation-plan missing:
→ Call faion-writing-implementation-plan skill first

## Task Creation

For each task in implementation-plan:

```python
Task(
    subagent_type="faion-task-creator-agent",
    description=f"Create {task_name}",
    prompt=f"""
PROJECT: {project}
FEATURE: {feature}
TASK_INFO: {task_from_plan}
SDD_PATH: aidocs/sdd/{project}/features/{status}/{feature}/

Create comprehensive task file with:
- Clear objective
- Acceptance criteria (AC-XX.X)
- Technical approach
- Files to modify
- Dependencies
- Estimated complexity

Research codebase deeply before writing.
"""
)
```

## Task Review

After all tasks created:

```python
Task(
    subagent_type="faion-tasks-reviewer-agent",
    prompt=f"""
Multi-pass review for {project}/{feature}:

Pass 1: Completeness - all plan items covered?
Pass 2: Consistency - no contradictions?
Pass 3: Coverage - all requirements addressed?
Pass 4: Executability - can be implemented as written?
"""
)
```

## Output Format

```markdown
## Tasks Created: {project}/{feature}

### Summary
- **Tasks created:** {count}
- **Review status:** ✅ Passed | ⚠️ Issues found

### Tasks
| Task | Description | Complexity |
|------|-------------|------------|
| TASK_001 | {desc} | Medium |
| TASK_002 | {desc} | Low |
| TASK_003 | {desc} | High |

### Review Notes
{from faion-tasks-reviewer-agent}

### Next Steps
- Run `/sdd` → Execute tasks
- Or `/sdd` → Do all tasks
```

## Agents Used

| Agent | Model | Purpose |
|-------|-------|---------|
| faion-task-creator-agent | opus | Deep research + task creation |
| faion-tasks-reviewer-agent | opus | Multi-pass quality review |
