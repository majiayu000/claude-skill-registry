---
name: operational-modes
description: Defines operational modes for agent work - planning (read-only analysis), editing (full write access), and interactive (guided development). Helps agents self-regulate tool usage based on current phase.
version: 1.0.0
model: sonnet
invoked_by: agent
user_invocable: true
tools: [Read, Glob, Grep]
best_practices:
  - Start in planning mode for unfamiliar tasks
  - Explicitly transition between modes
  - Respect mode constraints on tool usage
  - Use interactive mode for user-guided development
  - Document mode transitions in task logs
error_handling: graceful
streaming: supported
---

<identity>
Operational Mode Controller - Self-regulation framework for agent tool usage based on task phase.
</identity>

<capabilities>
- Defining clear operational boundaries for each mode
- Self-regulating tool usage based on current mode
- Transitioning between modes appropriately
- Preventing premature code changes during analysis
- Enabling focused, phase-appropriate work
</capabilities>

<instructions>

## Overview

Operational modes help agents self-regulate their behavior based on the current phase of work. This prevents premature code changes during analysis, ensures focused work, and creates clear phase transitions.

## Available Modes

### Mode 1: Planning Mode

**Purpose**: Analysis and planning without making changes.

**Characteristics**:

- Read-only operations
- Focus on understanding the codebase
- Create plans and strategies
- Identify affected components

**Allowed Tools**:

- `Read` - Read files
- `Glob` - Find files
- `Grep` - Search content
- `Bash` - Read-only commands (ls, cat, git status, git log)

**Excluded Tools**:

- `Write` - No file creation
- `Edit` - No file modification
- `Bash` - No commands that modify state
- `NotebookEdit` - No notebook changes

**When to Use**:

- Starting work on unfamiliar tasks
- Analyzing complex bugs
- Planning architectural changes
- Understanding dependencies before refactoring

**Example Prompt**:

```
You are operating in PLANNING MODE.

Your task is to analyze the codebase but NOT write any code.
Focus on:
- Understanding the current implementation
- Identifying affected components
- Creating a comprehensive plan
- Documenting your findings

Do NOT:
- Create new files
- Modify existing files
- Run commands that change state
```

### Mode 2: Editing Mode

**Purpose**: Full implementation capability.

**Characteristics**:

- Full write access
- Implementation focus
- Test-driven when appropriate
- Follows established patterns

**Allowed Tools**:

- All read tools
- `Write` - Create files
- `Edit` - Modify files
- `Bash` - All safe commands (build, test, lint)
- `NotebookEdit` - Modify notebooks

**Excluded Tools**:

- Destructive bash commands (rm -rf, git reset --hard, etc.)

**When to Use**:

- After planning is complete
- When implementation path is clear
- For well-defined tasks
- During test-driven development

**Example Prompt**:

```
You are operating in EDITING MODE.

You have full capability to:
- Create new files
- Modify existing files
- Run build/test commands

Guidelines:
- Follow TDD: write test first, then implement
- Follow project conventions
- Run tests after changes
- Keep changes focused on the task
```

### Mode 3: Interactive Mode

**Purpose**: User-guided development with frequent checkpoints.

**Characteristics**:

- Pause for user approval before major changes
- Explain options before proceeding
- Smaller, incremental changes
- More user involvement

**Allowed Tools**:

- All tools available
- Frequent use of AskUserQuestion

**Behavior**:

- Explain what you're about to do before doing it
- Present options when multiple approaches exist
- Ask for confirmation before significant changes
- Provide clear progress updates

**When to Use**:

- Learning user preferences
- High-risk changes
- Unclear requirements
- When user wants to stay involved

**Example Prompt**:

```
You are operating in INTERACTIVE MODE.

Before any significant action:
1. Explain what you plan to do
2. Present alternatives if they exist
3. Wait for user confirmation
4. Make the change
5. Report the result

Always keep the user informed and in control.
```

### Mode 4: One-Shot Mode

**Purpose**: Single-task execution without follow-up.

**Characteristics**:

- Optimized for quick, focused tasks
- Minimal interaction
- Complete task fully before stopping
- No iterative refinement expected

**Allowed Tools**:

- All tools as appropriate

**Behavior**:

- Understand the complete task upfront
- Execute fully
- Provide comprehensive summary at end

**When to Use**:

- Simple, well-defined tasks
- Automation scripts
- Batch operations
- When user won't be monitoring

**Example Prompt**:

```
You are operating in ONE-SHOT MODE.

Complete the following task fully in a single execution:
- Analyze requirements
- Implement solution
- Validate/test
- Summarize changes

Do not expect follow-up interaction.
```

## Mode Transitions

### Planning -> Editing

Transition when:

- Plan is complete
- User has approved approach
- All unknowns are resolved

```markdown
## Mode Transition: Planning -> Editing

**Planning Summary**:

- Analyzed: [files/components]
- Plan: [brief description]
- Affected: [components list]

**Ready to implement**: [yes/no]
**Blockers**: [none / list blockers]

Transitioning to EDITING MODE.
```

### Editing -> Planning

Transition when:

- Unexpected complexity discovered
- Scope expansion needed
- Architectural questions arise

```markdown
## Mode Transition: Editing -> Planning

**Reason**: Discovered unexpected dependency
**Need to analyze**: [what needs investigation]

Returning to PLANNING MODE for analysis.
```

### Any -> Interactive

Transition when:

- User requests involvement
- High-risk decision point
- Multiple valid approaches

```markdown
## Mode Transition: -> Interactive

**Reason**: Multiple valid approaches identified
**Options**:

1. Approach A - [pros/cons]
2. Approach B - [pros/cons]

Entering INTERACTIVE MODE for user decision.
```

## Integration with Task System

When using tasks, note the current mode:

```javascript
TaskCreate({
  subject: 'Implement user validation',
  description: '...',
  metadata: { mode: 'editing' },
});

TaskUpdate({
  taskId: '1',
  metadata: { mode: 'planning', reason: 'Need architectural review' },
});
```

## Self-Assessment Checklist

Before changing modes, verify:

**Entering Planning Mode**:

- [ ] Task requires analysis
- [ ] Don't have enough information to proceed
- [ ] Complex decision points ahead

**Entering Editing Mode**:

- [ ] Plan is complete
- [ ] Approach is decided
- [ ] User has approved (if required)

**Entering Interactive Mode**:

- [ ] User involvement needed
- [ ] Multiple options to present
- [ ] High-risk or unclear situation

</instructions>

<examples>
<usage_example>
**Scenario**: User asks "Refactor the authentication system"

**Agent Response**:

```
This is a significant task. I'll start in PLANNING MODE.

## Planning Mode Analysis

### Current Understanding
Reading authentication-related files...
- auth.ts - Main authentication logic
- session.ts - Session management
- middleware/auth.ts - Auth middleware

### Observations
- Current: Custom JWT implementation
- Dependencies: 12 files import from auth.ts
- Tests: 24 tests in auth.test.ts

### Plan
1. Identify all auth touchpoints
2. Design new interface (minimal breaking changes)
3. Implement with backwards compatibility
4. Migrate consumers gradually

### Questions
Before proceeding to EDITING MODE:
1. Should I preserve the current API or is breaking change OK?
2. Target deadline/timeline?

Awaiting your input before transitioning modes.
```

</usage_example>
</examples>

<integration>
**Related Skills**:
- `thinking-tools` - Use within each mode for quality checks
- `writing-plans` - Use in planning mode
- `tdd` - Use in editing mode
- `summarize-changes` - Use when completing editing mode
</integration>

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern discovered -> `.claude/context/memory/learnings.md`
- Issue encountered -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
