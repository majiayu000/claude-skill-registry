---
name: start-task
description: Start work on a task. Use when user says "začni práci na task-XX", "chci pracovat na task-XX", "start task XX", or runs /start-task.
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion, WebSearch, WebFetch, Task
---

# Start Task

Validate dependencies, perform thorough research & analysis, present implementation proposal with supporting arguments, and get user approval before starting work.

## Usage

```
/start-task 02                # Task 02 - stays on main (default)
/start-task 02 --branch       # Task 02 - creates feature branch
/start-task task-02           # Explicit task-02
```

## Current State

Current branch:
!git branch --show-current

Uncommitted changes:
!git status --porcelain

Is worktree:
!test -f "$(git rev-parse --show-toplevel)/.git" && echo "YES - WORKTREE" || echo "NO - main repo"

## Process

### Step 1: Parse Task Identifier

The script accepts multiple formats:
- `02` or `2` - just task number (uses current or default phase)
- `task-02` - explicit task ID
- `--branch` flag - create feature branch instead of staying on main

### Step 2: Validate Dependencies

Before starting, check:
1. Task file exists in `specification/phase-XX-*/tasks/`
2. Task is not already in_progress or completed
3. All dependencies are completed (status: ✅)

If blocked, show which tasks need to be completed first.

### Step 3: Detect Mode & Handle Branch

**Mode detection:**
```bash
IS_WORKTREE=false
if [[ -f "$(git rev-parse --show-toplevel)/.git" ]]; then
  IS_WORKTREE=true
fi
```

**Branch handling by mode:**

| Mode | Action |
|------|--------|
| MAIN (default) | Stay on main, no branch created |
| `--branch` flag | Create `phase-XX/task-YY-desc` branch from main |
| WORKTREE | Branch already exists, just update status |

### Step 4: Update Task Status

Update the task file:
- Changes `| Status | ⚪ pending |` to `| Status | 🔵 in_progress |`

### Step 5: Research & Analysis (CRITICAL)

**This step is MANDATORY before any implementation begins.**

Perform thorough research based on task scope:

1. **Codebase Analysis**
   - Use `Glob` and `Grep` to explore existing patterns in the codebase
   - Check how similar features are implemented
   - Identify relevant existing code, interfaces, base classes

2. **Web Research**
   - Use `WebSearch` to find:
     - Official documentation for libraries/frameworks mentioned in scope
     - Best practices for the specific technology/pattern
     - Common pitfalls and how to avoid them
     - Current recommended approaches (2025/2026)
   - Use `WebFetch` to read specific documentation pages

3. **Related Specs Review**
   - Read all files listed in "Related Specs" section of the task
   - Understand architectural constraints and requirements

### Step 6: Present Implementation Proposal

Create a structured proposal with:

```markdown
## Implementation Proposal for [Task Name]

### Approach
[Describe the chosen approach in 2-3 sentences]

### Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Decision 1] | [Choice] | [Why - with source reference] |
| [Decision 2] | [Choice] | [Why - with source reference] |

### Implementation Steps
1. [Step 1 - specific and actionable]
2. [Step 2 - specific and actionable]
...

### Supporting Evidence
- 📚 [Documentation link or codebase reference]
- ✅ Best practice: [description with source]
- ⚠️ Avoided pitfall: [what we're avoiding and why]

### Alternatives Considered
| Alternative | Why not chosen |
|-------------|----------------|
| [Alt 1] | [Reason] |

### Questions/Clarifications (if any)
- [Question needing user input]
```

### Step 7: Get User Approval

**STOP and ask for user confirmation before implementing:**

Use `AskUserQuestion` with options:
- "Proceed with this approach" (recommended)
- "Modify the approach"
- "Need more research on specific area"
- Other (for custom input)

**Do NOT start implementation without explicit user approval.**

### Step 8: Show Task Scope

After approval, display the task's scope section and begin implementation.

## Arguments

- `$ARGUMENTS` - Task identifier + optional flags
  - `02` - task number
  - `--branch` - create feature branch (otherwise stays on main)

## Output

On success (MAIN mode):
```
Started task task-02: Shared Kernel
Mode: MAIN (commits go directly to main)
Task file: specification/phase-01-foundation/tasks/task-02-shared-kernel.md

Task scope:
- [ ] Implement Entity base class
...
```

On success (BRANCH mode):
```
Started task task-02: Shared Kernel
Mode: FEATURE_BRANCH
Branch: phase-01/task-02-shared-kernel
Task file: specification/phase-01-foundation/tasks/task-02-shared-kernel.md

Task scope:
- [ ] Implement Entity base class
...
```

On error (blocked):
```
Error: Task task-03 is blocked by: task-02
Complete the blocking tasks first or use /task-status to see the full picture.
```

## Safety Rules

1. NEVER start a task with incomplete dependencies
2. ALWAYS show uncommitted changes warning if present
3. NEVER force-checkout if there are uncommitted changes
4. ALWAYS preserve existing branch if it exists

## Integration

After starting a task:
- Use `/commit` to commit changes with proper `[XX-YY] type:` format
- Use `/finish-task` when done (behavior depends on mode)
- Use `/task-status` to check progress
