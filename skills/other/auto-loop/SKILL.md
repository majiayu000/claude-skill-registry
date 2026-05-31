---
name: auto-loop
description: TDD-based autonomous development loop with checkpoint recovery and observability changelog
user-invocable: true
---

# Auto-Loop

Execute a TDD-based autonomous development loop with full observability.

---

## Usage

```bash
# Start new task
/auto-loop "Implement user login"

# With acceptance criteria
/auto-loop "Implement authentication

Acceptance Criteria:
- [ ] Login form (email + password)
- [ ] JWT token generation
- [ ] Error handling
"

# Resume interrupted session
/auto-loop --resume

# Force restart (clear old state)
/auto-loop --force "New task"

# Check status
/auto-loop --status

# With iteration limit
/auto-loop "Task" --max-iterations 15
```

---

## How It Works

```
┌───────────────────────────────────────────────────────────────┐
│                      TDD Iteration                            │
├───────────┬───────────────────────────────────────────────────┤
│  RED      │ Write failing test for next AC                    │
│           │ → Auto-logged: file_created, test_fail            │
├───────────┼───────────────────────────────────────────────────┤
│  GREEN    │ Write implementation to make test pass            │
│           │ → Auto-logged: file_created/modified, test_pass   │
├───────────┼───────────────────────────────────────────────────┤
│  REFACTOR │ Improve code quality (no behavior change)         │
│           │ → Use code-reviewer agent for suggestions         │
├───────────┼───────────────────────────────────────────────────┤
│  VALIDATE │ Run full test suite + linter                      │
│           │ → Auto-logged: test_pass/fail                     │
├───────────┼───────────────────────────────────────────────────┤
│  COMMIT   │ Commit changes with descriptive message           │
│           │ → Auto-logged: commit                             │
├───────────┼───────────────────────────────────────────────────┤
│  DECIDE   │ Check AC completion → continue or complete        │
└───────────┴───────────────────────────────────────────────────┘
```

---

## Execution

When user runs `/auto-loop "<request>"`:

### 1. State Detection (Conflict Prevention)

```bash
STATE_DIR=".auto-loop"
CHECKPOINT="$STATE_DIR/checkpoint.json"

# Check for existing in-progress session
if [ -f "$CHECKPOINT" ]; then
    status=$(jq -r '.status // "unknown"' "$CHECKPOINT" 2>/dev/null || echo "unknown")
    iteration=$(jq -r '.current_iteration // 0' "$CHECKPOINT" 2>/dev/null || echo "0")

    if [ "$status" == "in_progress" ]; then
        echo "⚠️  Found interrupted session at iteration #$iteration"
        echo "Options:"
        echo "  /auto-loop --resume        → Continue"
        echo "  /auto-loop --force \"...\"  → Start fresh"
        exit 1
    fi
fi
```

**Behavior Matrix:**

| Existing State | Command | Action |
|----------------|---------|--------|
| None | `/auto-loop "task"` | Start new |
| `completed` | `/auto-loop "task"` | Archive & start new |
| `in_progress` | `/auto-loop "task"` | **Block** - prompt user |
| `in_progress` | `/auto-loop --resume` | Continue |
| `in_progress` | `/auto-loop --force "task"` | Archive & start new |

### 2. Initialize

```bash
# Archive old changelog if > 100 lines
CHANGELOG_DIR=".director-mode"
CHANGELOG="$CHANGELOG_DIR/changelog.jsonl"

if [ -f "$CHANGELOG" ] && [ $(wc -l < "$CHANGELOG") -gt 100 ]; then
    mv "$CHANGELOG" "$CHANGELOG_DIR/changelog.$(date +%Y%m%d_%H%M%S).jsonl"
fi

# Create state directories
mkdir -p "$STATE_DIR" "$CHANGELOG_DIR"

# Initialize checkpoint
cat > "$CHECKPOINT" << EOF
{
  "request": "$ARGUMENTS",
  "current_iteration": 0,
  "max_iterations": 20,
  "status": "in_progress",
  "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "acceptance_criteria": [],
  "last_test_result": null,
  "files_changed": []
}
EOF
```

### 3. Parse Acceptance Criteria

```
Input:
  "Implement authentication

  Acceptance Criteria:
  - [ ] Login form
  - [ ] JWT token
  "

Parsed:
{
  "acceptance_criteria": [
    { "id": 1, "description": "Login form", "done": false },
    { "id": 2, "description": "JWT token", "done": false }
  ]
}
```

### 4. DECIDE - Completion Check

```
┌─────────────────────────────────────────────────────────────┐
│  DECIDE - Iteration #3                                      │
├─────────────────────────────────────────────────────────────┤
│  [x] 1. Login form            ← test passing               │
│  [x] 2. JWT token             ← test passing               │
│  [ ] 3. Error handling        ← NO TEST YET                │
├─────────────────────────────────────────────────────────────┤
│  Decision: 2/3 complete → CONTINUE                          │
└─────────────────────────────────────────────────────────────┘
```

**Complete when:**
- All AC marked `done: true`
- All tests passing

**Stop when:**
- `max_iterations` reached
- `.auto-loop/stop` file exists

---

## Flags

| Flag | Description |
|------|-------------|
| `--resume` | Continue interrupted session |
| `--force` | Clear old state, start fresh |
| `--status` | Show current session status |
| `--max-iterations N` | Set iteration limit (default: 20) |

---

## Observability

All events are automatically logged via PostToolUse hooks:

| Event | Trigger | Hook |
|-------|---------|------|
| `file_created` | Write tool | `log-file-change.sh` |
| `file_modified` | Edit tool | `log-file-change.sh` |
| `test_pass/fail` | Bash (test) | `log-bash-event.sh` |
| `commit` | Bash (git commit) | `log-bash-event.sh` |

Query with `/changelog`:

```bash
/changelog              # Recent events
/changelog --summary    # Statistics
/changelog --type test  # Filter by type
```

---

## Stop / Resume

```bash
# Interrupt (stop after current iteration)
touch .auto-loop/stop

# Check status
/auto-loop --status

# Resume
/auto-loop --resume

# Force restart
/auto-loop --force "New task"
```

---

## Related

- [/changelog](../changelog/SKILL.md) - View development events
- [code-reviewer](../../agents/code-reviewer.md) - Code quality review
- [debugger](../../agents/debugger.md) - Error analysis
- [test-runner](../test-runner/SKILL.md) - Test automation
