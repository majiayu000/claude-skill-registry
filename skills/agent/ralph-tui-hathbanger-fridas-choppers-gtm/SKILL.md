---
name: ralph-tui
description: AI agent loop orchestrator for autonomous task execution - coding, content, any multi-step work
---

# Ralph TUI - Autonomous Task Execution

Break down complex work into tasks, then let AI execute them autonomously.

**Why this matters:** Instead of manually prompting for each step, define the work upfront as a PRD, then let ralph-tui orchestrate execution. It selects tasks, builds prompts with context, executes your AI agent, and advances automatically.

## Usage

```
/ralph-tui                    # Show available commands
/ralph-tui run                # Run autonomous loop on current prd.json
/ralph-tui create             # Create a new PRD with AI assistance
/ralph-tui status             # Check execution status
```

## On Skill Invoke

### If no args or "help":
Show the ralph-tui command reference:

```
Ralph TUI - AI Agent Loop Orchestrator

Commands:
  jfl ralph run --prd ./tasks/file.json    Run autonomous task loop
  jfl ralph create-prd --chat              Create PRD with AI
  jfl ralph setup                          Initialize in project
  jfl ralph status                         Show session status
  jfl ralph resume                         Resume paused session

Quick Start:
  1. Create PRD: jfl ralph create-prd --chat
  2. Run loop:   jfl ralph run --prd ./tasks/my-feature.json

Keyboard (in TUI):
  s = start, p = pause, q = quit
  j/k = navigate, Enter = details
```

### If "run" or "start":

1. Check for prd.json files:
```bash
ls ./tasks/*.json 2>/dev/null || ls ./prd.json 2>/dev/null
```

2. If found, ask which to run:
```
Found PRD files:
1. tasks/admin-dashboard-prd.json (15 stories)
2. tasks/auth-migration.json (8 stories)

Which PRD to execute? (or 'new' to create one)
```

3. Launch ralph-tui:
```bash
jfl ralph run --prd <selected-file>
```

### If "create" or "new":

1. Ask about the work:
```
What do you want to build or accomplish?
(Describe the feature, fix, or task - I'll break it into stories)
```

2. Launch the chat-based PRD creator:
```bash
jfl ralph create-prd --chat --output ./tasks/
```

3. After PRD is created, offer to run it:
```
PRD created: ./tasks/my-feature.json

Want to start autonomous execution?
  jfl ralph run --prd ./tasks/my-feature.json
```

### If "status":

Check ralph-tui status:
```bash
jfl ralph status
```

Show current session info, completed tasks, remaining work.

---

## PRD Format

Ralph TUI uses JSON PRDs with this structure:

```json
{
  "name": "Feature Name",
  "description": "What we're building",
  "quality_gates": ["bun run typecheck", "bun run lint"],
  "stories": [
    {
      "id": "US-001",
      "title": "Story title",
      "priority": 1,
      "status": "pending",
      "description": "What to implement",
      "acceptance_criteria": ["Criterion 1", "Criterion 2"],
      "files": ["path/to/file.ts"],
      "dependencies": ["US-000"],
      "context": "Additional context for the agent"
    }
  ]
}
```

### Story Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique ID (US-001 format) |
| `title` | Yes | Short description |
| `priority` | Yes | 1 = highest, higher = lower priority |
| `status` | Yes | pending, in_progress, completed, blocked |
| `description` | Yes | What to implement |
| `acceptance_criteria` | Yes | List of requirements |
| `files` | No | Files likely to be modified |
| `dependencies` | No | Story IDs that must complete first |
| `context` | No | Extra info for the agent |

---

## Creating Good PRDs

### 1. Keep Stories Small
Each story should be completable in one agent session (typically <30 min of AI work).

Bad: "Implement user authentication"
Good: "Add login form component", "Create auth API route", "Add session middleware"

### 2. Clear Acceptance Criteria
Make criteria specific and testable.

Bad: "Should work well"
Good: "Returns 401 for invalid credentials", "Sets httpOnly cookie on success"

### 3. Order Dependencies
Put foundational work first. Use `dependencies` field when order matters.

### 4. Include Context
Add relevant info the agent needs but won't find in the codebase.

```json
{
  "context": "We're using Drizzle ORM. The users table already has an isAdmin column."
}
```

---

## Execution Model

1. **Task Selection**: Ralph picks the highest-priority pending task with no blocked dependencies
2. **Prompt Building**: Combines task details with your project context (CLAUDE.md, etc.)
3. **Agent Execution**: Runs your AI agent (Claude Code, OpenCode, etc.)
4. **Completion Detection**: Watches for `<promise>COMPLETE</promise>` token
5. **Quality Gates**: Runs checks (typecheck, lint) before advancing
6. **Loop**: Moves to next task automatically

---

## Integration with JFL

Ralph TUI is bundled with JFL CLI:

```bash
# Install JFL (includes ralph-tui)
npm install -g jfl

# Use ralph via jfl
jfl ralph run --prd ./tasks/feature.json

# Or directly
ralph-tui run --prd ./tasks/feature.json
```

PRDs are typically stored in `./tasks/` directory within your GTM workspace.

---

## Best Practices

1. **Start with /spec**: Use `/spec` skill to refine your PRD through adversarial review before execution
2. **Run quality gates**: Always include typecheck/lint in quality_gates
3. **Review between tasks**: Use `p` to pause and review changes before continuing
4. **Keep context files updated**: Ralph reads CLAUDE.md for project context

---

## Docs

Full documentation: https://ralph-tui.com/docs

Installed docs: `knowledge/RALPH_TUI_DOCS.txt`
