---
name: orchestrate
description: Guide a project from idea to implementation using the appropriate workflow depth
argument-hint: <project idea or goal>
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Task
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
  - TaskList
---

# /orchestrate - Workflow Orchestration

Guide a project through the appropriate development workflow based on complexity.

## Purpose

Orchestrate the full development lifecycle by:
- Assessing project complexity
- Selecting appropriate workflow depth
- Coordinating agents through the workflow
- Consulting user at key decision points
- Ensuring artifacts flow between phases

**CRITICAL**: The orchestrator NEVER edits files or runs bash directly. All implementation work is delegated to subagents via the Task tool.

## Context Discipline

**CRITICAL for orchestration quality**: Lean context = clear signal.

### What to Read (High-Level Only)
- `docs/objectives/ROADMAP.md` - milestone/phase overview
- `docs/development/BACKLOG.md` - task table only (not full details)
- `docs/architecture/PRD.md` - requirements summary
- Agent results - summary output from Task tool

### What to NEVER Read Directly
- Source code files
- Full file contents
- Detailed implementations
- Test files
- Logs

### Why This Matters
Cluttered context causes:
- Missed decision points
- Wrong workflow depth selection
- Failure to catch blockers
- Lost orchestration thread

**Rule**: If you need details, spawn an agent to analyze and summarize.

### Context Budget
- Keep orchestrator turns focused on: assess → delegate → checkpoint → proceed
- Each phase transition: brief status, next action
- Avoid: debugging, code review, detailed analysis (delegate these)

## Inputs

- `$ARGUMENTS`: Project idea, goal, or feature description
- `${PROJECT_NAME}`: Current project context
- Existing docs in `docs/` (if resuming)

## Outputs

Artifacts produced by each phase:
- PRD at `docs/architecture/PRD.md` (/spec)
- Architecture at `docs/architecture/ARCHITECTURE.md` (/design)
- ROADMAP/BACKLOG at `docs/objectives/` and `docs/development/` (/plan)
- Code and tests in source files (/implement)

## Workflow Depths

### Full Workflow
**Use when**: New product, complex system, multiple components, unclear requirements

```
/spec → /design → /plan → /implement → /validate → /deploy → /document
```

Phases:
1. **Specification**: Elicit requirements, define acceptance criteria
2. **Design**: Architecture, components, ADRs
3. **Planning**: Milestones, epics, tasks
4. **Implementation**: Code and tests
5. **Validation**: Testing, verification
6. **Deployment**: Build, deploy, release
7. **Documentation**: User docs, guides

### Medium Workflow
**Use when**: New feature, moderate complexity, clear scope

```
/spec → /plan → /implement → /validate
```

Phases:
1. **Specification**: Quick PRD with acceptance criteria
2. **Planning**: Task breakdown
3. **Implementation**: Code and tests
4. **Validation**: Testing

### Light Workflow
**Use when**: Simple change, bug fix, clear task

```
/plan → /implement
```

Phases:
1. **Planning**: Quick task definition
2. **Implementation**: Code and tests

## Complexity Assessment

Assess complexity to select workflow depth:

| Factor | Score |
|--------|-------|
| New system/product | +3 |
| Multiple components | +2 |
| Integration needed | +2 |
| New API | +1 |
| UI changes | +1 |
| Simple fix | -2 |
| Documentation only | -3 |

**Scoring**:
- Score >= 4: **Full** workflow
- Score 1-3: **Medium** workflow
- Score <= 0: **Light** workflow

## Orchestration Process

### 1. Assess Request
Read `$ARGUMENTS` and assess:
- What is being requested?
- Is this new or modification?
- How many components involved?
- Are requirements clear?

### 2. Select Workflow Depth
Based on complexity assessment, propose a workflow:

```
I've assessed this as a [complexity] project.

Recommended workflow: [Full/Medium/Light]
- Phase 1: [description]
- Phase 2: [description]
...

Proceed with this workflow?
```

Use `AskUserQuestion` to confirm with user.

### 3. Execute Phases
For each phase in the selected workflow:

**Option A - Agent Delegation (Recommended)**:
Use `Task` tool to spawn the appropriate agent:
```
Task(subagent_type="business-analyst", prompt="Create PRD for: ...")
Task(subagent_type="architect", prompt="Design architecture for: ...")
Task(subagent_type="project-manager", prompt="Create implementation plan for: ...")
Task(subagent_type="developer", prompt="Implement task T-001: ...")
```

**IMPORTANT**: Always use Option A. The orchestrator coordinates; subagents execute.

### 4. Checkpoint Between Phases
After each major phase:
- Verify artifacts were produced
- Check for blockers or issues
- Consult user if decisions needed
- Proceed to next phase

### 5. Handle Blockers
If a phase is blocked:
1. Document the blocker
2. Ask user for guidance
3. Either resolve or skip to next feasible phase

## Agent Invocation Pattern

When spawning agents via Task tool:

```python
# Spawn Business Analyst for /spec
Task(
    subagent_type="business-analyst",
    description="Generate PRD",
    prompt=f"""
    Create a Product Requirements Document for:
    {$ARGUMENTS}

    Project context: {$PROJECT_NAME}
    Output to: docs/architecture/PRD.md

    Follow the /spec skill workflow.
    """
)
```

Agents have skills injected via their `skills:` frontmatter, so they will follow the skill instructions.

## Decision Points

Consult user at these points:
1. **Workflow selection**: Confirm depth is appropriate
2. **Scope changes**: If requirements significantly different than expected
3. **Trade-offs**: When design decisions have significant impact
4. **Blockers**: When unable to proceed
5. **Phase completion**: Before major transitions (design → implement)

## Example Session

```
User: /orchestrate Build a CLI tool for managing todo items

Orchestrator:
I've assessed this request:
- New tool (not modification): +3
- Single component (CLI): 0
- No integration: 0
- Simple scope: -1

Total: 2 → Medium workflow

Recommended workflow:
1. /spec - Define requirements and CLI interface
2. /plan - Break into implementable tasks
3. /implement - Build the CLI
4. /validate - Test functionality

Proceed with Medium workflow?

User: Yes

Orchestrator: [Spawns business-analyst agent for /spec]
...
Orchestrator: PRD complete. Proceeding to /plan.
[Spawns project-manager agent for /plan]
...
```

## Parallel Execution

When tasks are independent, spawn multiple agents in a single message:
- Multiple implementation tasks → parallel developer agents
- Multiple validation tasks → parallel validator agents
- Independent research → parallel explore agents

Example:
```
Task(subagent_type="developer", prompt="Implement T-001...")
Task(subagent_type="developer", prompt="Implement T-002...")
Task(subagent_type="developer", prompt="Implement T-003...")
```

All three run concurrently, results collected together.

## Validation Checklist
- [ ] Workflow depth matches complexity
- [ ] User confirmed workflow selection
- [ ] Each phase produced expected artifacts
- [ ] Artifacts flow correctly between phases
- [ ] Decision points consulted user appropriately
- [ ] Context stayed lean (no code/detail clutter)
- [ ] Blockers documented if any
