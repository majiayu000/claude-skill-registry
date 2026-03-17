---
name: ralph-wiggum
version: 1.0.0
description: "Ralph Wiggum iterative development loop methodology for persistent AI agent work. Implements continuous iteration loops where AI works on tasks until completion, using Archon for state management and context handoffs. Integrates with The Long Run Harness, Spec Kit, and PRP frameworks. Triggers: ralph, wiggum, iteration loop, persistent agent, continuous development."
---

# Ralph Wiggum - Iterative AI Development Loops

> **"Ralph is a Bash loop"** - A simple `while true` that repeatedly feeds an AI agent a prompt, allowing it to iteratively improve its work until completion.

## 🚀 Quick Start

| Command | Description |
|---------|-------------|
| `/ralph-start` | Launch the setup wizard |
| `/ralph-iterate` | Run one iteration manually |
| `/ralph-status` | Check loop status & progress |
| `/ralph-cancel` | Cancel active Ralph loop |
| `/ralph-integrate` | Integrate Ralph with other frameworks |

---

## What is Ralph Wiggum?

Ralph Wiggum is a development methodology based on continuous AI agent loops. Named after Ralph Wiggum from The Simpsons, it embodies the philosophy of **persistent iteration despite setbacks**.

### Core Concept

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RALPH WIGGUM LOOP                                │
│                                                                     │
│    ┌──────────┐                                                     │
│    │  PROMPT  │ ◄────────────────────────────────────┐              │
│    └────┬─────┘                                      │              │
│         │                                            │              │
│         ▼                                            │              │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐     │              │
│    │  AGENT   │───►│  WORK    │───►│ CHECK    │─────┤              │
│    │  START   │    │  ON TASK │    │ COMPLETE │     │              │
│    └──────────┘    └──────────┘    └────┬─────┘     │              │
│                                         │           │              │
│                              ┌──────────┴───────┐   │              │
│                              │                  │   │              │
│                              ▼                  ▼   │              │
│                         [COMPLETE]          [ITERATE]              │
│                              │                                     │
│                              ▼                                     │
│                    ┌──────────────┐                                │
│                    │   UPDATE     │                                │
│                    │   ARCHON     │                                │
│                    │   COMPLETE   │                                │
│                    └──────────────┘                                │
│                                                                     │
│    State: Archon Tasks & Documents (context preserved)             │
└─────────────────────────────────────────────────────────────────────┘
```

### Self-Referential Feedback Loop

- The **prompt never changes** between iterations
- Previous work **persists in files** and git history
- Each iteration sees **modified files** from previous work
- Agent autonomously **improves by reading its own past work**
- **Archon tracks state** for handoffs and context management

---

## Philosophy

### 1. Iteration > Perfection

Don't aim for perfect on first try. Let the loop refine the work.

### 2. Failures Are Data

"Deterministically bad" means failures are predictable and informative. Use them to tune prompts.

### 3. Operator Skill Matters

Success depends on writing good prompts, not just having a good model.

### 4. Persistence Wins

Keep trying until success. The loop handles retry logic automatically.

---

## Execution Modes

### Mode 1: Background Workflow

Use the existing background workflow system for autonomous iteration:

```bash
# Start Ralph in background (recommended for long-running tasks)
& /ralph-loop "Build a REST API for todos" --max-iterations 50
```

### Mode 2: Manual Iteration

Control each iteration explicitly:

```bash
# Run one iteration
/ralph-iterate

# Check status
/ralph-status

# Continue if needed
/ralph-iterate
```

### Mode 3: Hybrid (Recommended)

Start with supervision, then background:

```bash
# First few iterations - supervised
/ralph-iterate  # Watch output
/ralph-iterate  # Verify direction

# Once confident, go to background
& /ralph-continue --remaining
```

---

## Loop Termination

Ralph loops terminate when ANY of these conditions are met:

### 1. Completion Promise (Primary)

Agent outputs the completion marker in response:

```markdown
<promise>COMPLETE</promise>
```

### 2. Archon Task Status (Recommended)

Task status changes to "done" in Archon:

```python
manage_task("update", task_id="...", status="done")
```

### 3. Max Iterations (Safety Net)

Always set a reasonable limit:

```bash
/ralph-loop "..." --max-iterations 50
```

### 4. Manual Cancellation

```bash
/ralph-cancel
```

---

## Archon Integration

Ralph uses Archon MCP for state management and context handoffs:

### State Tracking

```python
# Create Ralph loop state document
manage_document("create",
    project_id=PROJECT_ID,
    title="Ralph Loop State",
    document_type="note",
    content={
        "loop_id": "ralph-001",
        "status": "running",
        "current_iteration": 5,
        "max_iterations": 50,
        "task_id": "task-uuid",
        "completion_promise": "COMPLETE",
        "started_at": "2026-01-22T15:00:00Z",
        "last_iteration": "2026-01-22T15:30:00Z",
        "iterations": [
            {"n": 1, "summary": "Initial setup", "files_changed": 5},
            {"n": 2, "summary": "Basic implementation", "files_changed": 8},
            # ...
        ]
    }
)
```

### Context Handoff

Each iteration updates Archon with:
- Progress summary
- Files changed
- Test results
- Blockers encountered
- Next steps

This enables:
- Session recovery after interruption
- Progress monitoring from outside the loop
- Context transfer between AI agents

---

## Prompt Best Practices

### 1. Clear Completion Criteria

❌ **Bad:**
```
Build a todo API and make it good.
```

✅ **Good:**
```markdown
Build a REST API for todos.

When complete:
- All CRUD endpoints working
- Input validation in place  
- Tests passing (coverage > 80%)
- README with API docs
- Output: <promise>COMPLETE</promise>
```

### 2. Incremental Goals

❌ **Bad:**
```
Create a complete e-commerce platform.
```

✅ **Good:**
```markdown
Phase 1: User authentication (JWT, tests)
Phase 2: Product catalog (list/search, tests)
Phase 3: Shopping cart (add/remove, tests)

Output <promise>COMPLETE</promise> when all phases done.
```

### 3. Self-Correction Instructions

❌ **Bad:**
```
Write code for feature X.
```

✅ **Good:**
```markdown
Implement feature X following TDD:
1. Write failing tests
2. Implement feature
3. Run tests
4. If any fail, debug and fix
5. Refactor if needed
6. Repeat until all green
7. Output: <promise>COMPLETE</promise>
```

### 4. Escape Hatches

Always include guidance for stuck states:

```markdown
After 15 iterations, if not complete:
- Document what's blocking progress
- List what was attempted
- Suggest alternative approaches
- Update Archon task with blocker details
- Output: <promise>BLOCKED</promise>
```

---

## When to Use Ralph

### ✅ Good For

| Use Case | Why |
|----------|-----|
| Well-defined tasks with clear success criteria | Loop knows when to stop |
| Tasks requiring iteration and refinement | E.g., getting tests to pass |
| Greenfield projects where you can walk away | Autonomous operation |
| Tasks with automatic verification | Tests, linters, type checkers |
| TDD/BDD development | Clear red→green→refactor cycle |

### ❌ Not Good For

| Use Case | Why |
|----------|-----|
| Tasks requiring human judgment | Can't verify completion |
| Design decisions | Needs human creativity |
| One-shot operations | Overkill |
| Unclear success criteria | Infinite loops |
| Production debugging | Use targeted debugging instead |

---

## Framework Integration

Ralph integrates with all existing frameworks as an optional enhancement.

### With The Long Run Harness

```bash
# Use Ralph for harness coding sessions
/harness-ralph "Continue implementing features"

# Ralph wraps harness-coder with iteration loop
```

### With Spec Kit

```bash
# Use Ralph for spec implementation
/speckit-ralph "Implement the authentication spec"

# Ralph iterates until spec requirements met
```

### With PRP Framework

```bash
# Use Ralph for plan implementation
/prp-ralph PRPs/plans/feature.plan.md

# Ralph iterates until all tasks in plan complete
```

---

## Real-World Results

From the original Ralph technique:

| Metric | Result |
|--------|--------|
| Repositories generated overnight | 6 (Y Combinator hackathon) |
| Contract value completed | $50,000 |
| API costs for that contract | $297 |
| Programming language created | "cursed" (3 months) |

---

## Commands Reference

### /ralph-start

Launch the full setup wizard.

**Collects:**
- Project and task selection
- Prompt/task description
- Completion criteria
- Max iterations
- Execution mode
- Framework integration

### /ralph-iterate

Run a single iteration manually.

**Options:**
```bash
/ralph-iterate                    # Run next iteration
/ralph-iterate --verbose          # Detailed output
/ralph-iterate --dry-run          # Show what would happen
```

### /ralph-status

Check loop status and progress.

**Shows:**
- Current iteration / max
- Task completion percentage
- Files changed
- Test status
- Time elapsed
- Estimated remaining

### /ralph-cancel

Cancel the active Ralph loop.

**Options:**
```bash
/ralph-cancel                     # Cancel and save state
/ralph-cancel --force             # Cancel without saving
/ralph-cancel --cleanup           # Cancel and revert changes
```

### /ralph-integrate

Configure Ralph integration with other frameworks.

**Options:**
```bash
/ralph-integrate harness          # Integrate with Long Run Harness
/ralph-integrate speckit          # Integrate with Spec Kit
/ralph-integrate prp              # Integrate with PRP Framework
/ralph-integrate all              # Enable all integrations
```

---

## Configuration

### Loop State File

Location: `.ralph/loop-state.json`

```json
{
  "loop_id": "ralph-20260122-150000",
  "archon_project_id": "proj-uuid",
  "archon_task_id": "task-uuid",
  "archon_doc_id": "doc-uuid",
  "prompt_file": ".ralph/prompts/current.md",
  "status": "running",
  "current_iteration": 5,
  "max_iterations": 50,
  "completion_promise": "COMPLETE",
  "started_at": "2026-01-22T15:00:00Z",
  "mode": "background",
  "integration": {
    "harness": true,
    "speckit": false,
    "prp": true
  }
}
```

### Environment Variables

```bash
RALPH_MAX_ITERATIONS=50           # Default max iterations
RALPH_DEFAULT_MODE=hybrid         # background|manual|hybrid
RALPH_ARCHON_PROJECT=             # Default Archon project ID
RALPH_COMPLETION_PROMISE=COMPLETE # Default completion marker
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Loop never completes | Check completion criteria; add `--max-iterations` |
| Agent stuck in loop | Add escape hatch instructions in prompt |
| Context lost between iterations | Verify Archon connection and state document |
| Tests keep failing | Review test output; may need prompt refinement |
| Token limits reached | Break task into smaller phases |

### Recovery Commands

```bash
# Check state
cat .ralph/loop-state.json

# View Archon state
find_tasks(task_id="<TASK_ID>")
find_documents(project_id="<PROJECT_ID>", query="Ralph Loop State")

# Resume from checkpoint
/ralph-resume

# Reset and restart
/ralph-cancel --cleanup
/ralph-start
```

---

## Learn More

- [Original Ralph Technique](https://ghuntley.com/ralph/)
- [Ralph Orchestrator](https://github.com/mikeyobrien/ralph-orchestrator)
- [Autonomous Agent Harness Skill](../autonomous-agent-harness/SKILL.md)
- [PRP Framework Skill](../prp-framework/SKILL.md)
