---
name: start-refactor-task
description: 'Start or complete a specific refactoring task from a task file (for sub-agents)'
argument-hint: <task-file-path> [--task <task-id>] [--complete <task-id>]
user-invocable: true
model: sonnet
---

# Start Refactor Task

You are implementing a specific refactoring task from a plugin refactoring plan.

<task_input>
$ARGUMENTS
</task_input>

---

## Parse Arguments

- `task_file_path`: Path to the task file (required)
- `--task <id>`: Task ID to start (optional, defaults to first ready task)
- `--complete <id>`: Task ID to mark complete (optional)

---

## If `--complete <task-id>` Provided

1. READ the task file
2. EDIT the task status from `🔄 IN PROGRESS` to `✅ COMPLETE`
3. Output: `Task {ID}: {Name} marked as COMPLETE`
4. EXIT

---

## Starting a Task

### 1. Load Context

READ the task file. It contains everything you need:

- Task details (status, dependencies, priority, complexity)
- Target file being refactored
- Issue type (SKILL_SPLIT, AGENT_OPTIMIZE, DOC_IMPROVE, ORPHAN_RESOLVE, STRUCTURE_FIX)
- Acceptance criteria (your definition of done)
- Required inputs (design spec sections, source files to read)
- Expected outputs (files to create/modify)
- Verification steps (how to prove completion)

The task file header links to the design spec. READ it for refactoring context.

### 2. Select Task

If `--task <id>` specified: Use that task.

Otherwise, find the first task where:

- Status is `❌ NOT STARTED`
- All dependencies are `✅ COMPLETE` or "None"

If no ready task: Output "No ready tasks" and EXIT.

### 3. Update Status

EDIT the task file: Change `❌ NOT STARTED` to `🔄 IN PROGRESS`

### 4. Track Progress

Use the Task API to track acceptance criteria:

```
TaskCreate(
    subject="AC1: {criterion}",
    description="{detailed criterion description}",
    activeForm="Implementing {criterion}"
)
TaskCreate(
    subject="Verification: Run all verification steps",
    description="{verification steps}",
    activeForm="Running verification"
)
```

### 5. Implement

Work through each acceptance criterion based on the issue type:

#### For SKILL_SPLIT Tasks

1. READ the current skill file completely
2. READ the design spec section for this split
3. IDENTIFY content domains as specified in design
4. CREATE new skill directories and SKILL.md files
5. DISTRIBUTE content according to design spec
6. UPDATE cross-references between skills
7. CREATE shared references if specified
8. VERIFY all links resolve

#### For AGENT_OPTIMIZE Tasks

1. READ the current agent file
2. READ the design spec section for optimization
3. LOAD reference skills: claude-skills-overview-2026, prompt-optimization-claude-45
4. REWRITE description with trigger keywords
5. IMPROVE instruction clarity
6. REVIEW tool restrictions
7. VALIDATE frontmatter format

#### For DOC_IMPROVE Tasks

1. READ the current file
2. READ the design spec section for improvements
3. IDENTIFY specific quality issues
4. REWRITE with improved clarity, triggers, examples
5. ENSURE proper markdown formatting
6. VALIDATE frontmatter if applicable

#### For ORPHAN_RESOLVE Tasks

1. READ the orphaned file
2. READ the design spec classification
3. IF integrating: ADD link from appropriate SKILL.md
4. IF removing: DELETE the file (after confirming no references)
5. IF merging: COMBINE content with target file

#### For STRUCTURE_FIX Tasks

1. READ all affected files
2. IDENTIFY broken links or structural issues
3. FIX links to point to correct locations
4. VERIFY all cross-references resolve

Mark todos as you complete them.

### 6. Verify

Run each verification step from the task. All must pass.

Common verification steps:

- `Read the created/modified files to confirm content`
- `Verify all internal links resolve`
- `Check frontmatter validates against schema`
- `Confirm file structure matches design spec`

### 7. Complete

When all verification passes:

```
/plugin-creator:start-refactor-task {task_file_path} --complete {task_id}
```

---

## Working Environment

### Collaborative Agents

Other agents may be working nearby on related tasks. If you notice edits to files you didn't make:

- **This is intentional** - the user or other agents made those changes
- **Include these changes in your considerations**
- If the changes block your work, STOP and report to the orchestrator with your reasoning

### Reference Skills

Load these skills for guidance on proper formats:

| Skill                         | Use For                   |
| ----------------------------- | ------------------------- |
| claude-skills-overview-2026   | Skill SKILL.md format     |
| claude-plugins-reference-2026 | Plugin structure          |
|                               | Command format            |
| claude-hooks-reference-2026   | Hooks format              |
| prompt-optimization-claude-45 | Agent prompt optimization |

### Research and Knowledge

**Be bold with research. Be skeptical of built-in knowledge.**

Your training data may be outdated. The codebase and reference skills are the source of truth.

Before implementing:

1. READ existing skills/agents that are well-formatted
2. CHECK reference skills for format requirements
3. USE context7, Ref MCPs for documentation questions
4. VERIFY patterns match what's actually in the codebase

```
# Good: Verify format before writing
READ ./plugins/example-plugin/skills/example/SKILL.md  # Check actual format
Skill(skill="claude-skills-overview-2026")  # Load format reference
```

### Quality Standards

- Follow existing patterns in the plugin
- Preserve content fidelity during splits (no information loss)
- Maintain or improve frontmatter quality
- Ensure all cross-references resolve
- Keep line counts under thresholds (skills <500 lines)

---

## Error Handling

**Blocked by dependency**: Report which tasks must complete first.

**Verification failure**: After 3 fix attempts, STOP and report the failure details.

**Design conflict**: If the design spec conflicts with codebase reality, STOP and report.

**Content loss**: If splitting would lose content, STOP and request design clarification.
