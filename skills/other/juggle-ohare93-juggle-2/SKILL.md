---
name: juggle
description: Task management via CLI for agent loops. Balls are tasks with acceptance criteria; sessions group related balls. Use when working on a project with a .juggle/ directory, when user mentions juggle/balls/sessions, when planning tasks before agent loops, or when updating task state and logging progress during execution.
---

# Juggle

Juggle runs autonomous AI agent loops with good UX for the developer. This skill teaches you (the agent) how to use CLI commands to manage tasks - updating state, logging progress, and checking acceptance criteria as you work.

## CLI-First Approach

**Always prefer `juggle` CLI commands over direct file access.** While ball and session data is stored in `.juggle/balls.jsonl` and `.juggle/sessions/*/` files, you should interact with this data through CLI commands rather than reading files directly.

**Use CLI commands:**
- `juggle list --format json` - Get all balls in structured format
- `juggle show <ball-id> --json` - Get specific ball details
- `juggle sessions show <session-id>` - Get session with linked balls
- `juggle export --format json` - Export all active balls

**Only read files directly as a last resort** when the CLI doesn't provide the specific data or format you need. The CLI provides proper validation, error handling, and will remain stable across version changes.

## Core Concepts

### Balls = Tasks

A ball is a unit of work with:

- **Intent**: What you're trying to accomplish
- **Acceptance Criteria**: Verifiable conditions that define "done"
- **State**: pending → in_progress → complete (or blocked)
- **Tags**: Links to sessions and categories
- **Model Size** (optional): Preferred model size (`small`, `medium`, `large`) for cost optimization

### Sessions = Groupings

A session groups related balls and provides:

- **Context**: Background info, constraints, architecture notes (read by agents)
- **Progress**: Append-only log of what happened (memory across loop iterations)

Sessions give agents memory between iterations - context is the "brief" and progress is the "journal".

## Writing Good Acceptance Criteria

Acceptance criteria define when a ball is DONE. Write them so an agent (or human) can verify completion objectively.

**Good acceptance criteria are:**

- Verifiable: Can be checked with a command or inspection
- Specific: No ambiguity about what "done" means
- Include verification: Tests pass, builds succeed, etc.

**Examples:**

```bash
# Good - specific and verifiable
juggle plan "Add login endpoint" \
  -c "POST /api/login accepts email+password JSON body" \
  -c "Returns 200 with JWT token on valid credentials" \
  -c "Returns 401 with error message on invalid credentials" \
  -c "Unit tests cover success and failure cases" \
  -c "go test ./... passes"

# Bad - vague and unverifiable
juggle plan "Add login endpoint" \
  -c "Login should work" \
  -c "Good error handling" \
  -c "Tests"
```

**Always include a verification criterion** like:

- `go test ./... passes`
- `npm run test passes`
- `cargo build succeeds`
- `linter reports no errors`

## Planning Tasks (Before Loops)

### 1. Create a Session

```bash
# Create session with description
juggle sessions create auth-feature -m "User authentication system"

# Create with initial context (agent-friendly)
juggle sessions create auth-feature -m "User authentication" \
  --context "Use JWT tokens. Follow existing patterns in api/handlers/."
```

### 2. Add Session Context

Context provides background that agents need. Include constraints, architecture decisions, and relevant file locations.

```bash
# Set context directly (agent-friendly)
juggle sessions context auth-feature --set "Background: Building auth for the API.
Constraints: Must use existing User model in models/user.go.
Patterns: Follow handler patterns in api/handlers/.
Tests: All new code needs unit tests."

# Or edit interactively
juggle sessions context auth-feature --edit
```

### 3. Create Balls with Acceptance Criteria

Link balls to sessions with the `--session` flag. Use `-c` for each acceptance criterion.

```bash
# Create ball in session with criteria
juggle plan "Add login endpoint" --session auth-feature \
  -c "POST /api/login accepts {email, password}" \
  -c "Returns JWT token on success" \
  -c "Returns 401 on invalid credentials" \
  -c "go test ./... passes"

# Create standalone ball (no session)
juggle plan "Fix header styling" \
  -c "Header text is centered" \
  -c "npm run build succeeds"
```

## Updating State (During Loops)

During execution, agents update ball state and log progress.

### Update Ball State

```bash
# Mark ball as in progress
juggle update myapp-5 --state in_progress

# Mark ball as complete
juggle update myapp-5 --state complete

# Mark ball as blocked with reason
juggle update myapp-5 --state blocked --reason "Waiting for API spec"

# Use --json flag for structured output (agent-friendly)
juggle update myapp-5 --state complete --json
```

### Log Progress

Progress entries are timestamped and persist across loop iterations. Use them for:

- Recording what was accomplished
- Noting decisions made
- Flagging issues for next iteration

```bash
# Append progress entry
juggle progress append auth-feature "Implemented login endpoint with tests"

# Multiple entries
juggle progress append auth-feature "Added JWT validation middleware"
juggle progress append auth-feature "Discovered: need to handle token refresh"
```

### View Current State

```bash
# Show ball details
juggle show myapp-5

# Show session with linked balls
juggle sessions show auth-feature

# List all balls
juggle list
```

## Ball States

| State         | Meaning                                  |
| ------------- | ---------------------------------------- |
| `pending`     | Planned, not yet started                 |
| `in_progress` | Currently being worked on                |
| `blocked`     | Stuck (reason in `blocked_reason` field) |
| `complete`    | Done and archived                        |

### Model Size

Model size indicates the preferred LLM model for cost optimization:

| Size     | Model  | Use For                                             |
| -------- | ------ | --------------------------------------------------- |
| `small`  | haiku  | Simple fixes, docs, straightforward implementations |
| `medium` | sonnet | Standard features, moderate complexity              |
| `large`  | opus   | Complex refactoring, architectural changes          |

When running the agent with a specific model (`--model`), balls matching that model size are prioritized. This allows running cheaper models for simple tasks.

```bash
# Run with sonnet model (good for medium complexity)
juggle agent run my-feature --model sonnet

# Set model size when creating or updating a ball
juggle update myapp-5 --model-size small
```

### In-Progress Ball Handling

When the agent receives balls, **in_progress balls appear first** because they represent unfinished work from previous iterations.

**How to handle in_progress balls:**

1. **Check if already done** - Sometimes work was completed in a previous iteration but the agent loop was interrupted before updating state
2. **If done:** Verify acceptance criteria are met, update state to `complete`, then continue to next ball
3. **If not done:** Continue the implementation

This ensures work is never lost between agent loop iterations.

## Ball Dependencies

Balls can depend on other balls to express ordering requirements. Dependencies ensure prerequisite work is completed first.

### Specifying Dependencies

When creating a ball:

```bash
# Create a ball that depends on another ball
juggle plan "Add user profile page" --depends-on my-app-5

# Create with multiple dependencies
juggle plan "Integrate auth with profile" --depends-on auth-ball-1 --depends-on profile-ball-2
```

When updating an existing ball:

```bash
# Add a dependency
juggle update my-app-10 --add-dep my-app-5

# Remove a dependency
juggle update my-app-10 --remove-dep my-app-5

# Replace all dependencies
juggle update my-app-10 --set-deps my-app-5,my-app-6
```

### ID Resolution

Dependency IDs support:

- Full ball ID: `my-project-abc12345`
- Short ID: `abc12345`
- Prefix match: `abc` (if unique)

### Circular Dependency Detection

Juggle automatically detects and rejects circular dependencies:

```bash
# This will fail if ball-A depends on ball-B and ball-B depends on ball-A
juggle update ball-A --add-dep ball-B
# Error: dependency error: circular dependency detected: ball-A → ball-B → ball-A
```

### Agent Priority Ordering

When the agent receives balls, dependencies are considered for ordering:

1. **In-progress balls first** (unfinished work from previous iterations)
2. **Balls with satisfied dependencies** (all dependencies complete)
3. **Balls with pending dependencies** (blocked until dependencies complete)

If a ball has dependencies that are not yet complete, the agent should complete the dependencies first.

## Headless/Non-Interactive Mode

For automated agents and scripts, juggle commands support non-interactive modes:

### Creating Balls (Non-Interactive)

```bash
# Use --non-interactive to skip all prompts and use defaults
juggle plan "Task intent" --non-interactive

# Specify all options via flags for full control
juggle plan "Task intent" \
  --priority high \
  --session my-feature \
  -c "AC 1" -c "AC 2" \
  --non-interactive
```

In non-interactive mode:

- Intent is required (via args or `--intent`)
- Priority defaults to `medium`
- State defaults to `pending`
- Tags, session, and ACs default to empty

### Session Commands (Non-Interactive)

```bash
# Delete session without confirmation
juggle sessions delete my-session --yes

# Or short form
juggle sessions delete my-session -y
```

### Config Commands (Non-Interactive)

```bash
# Clear acceptance criteria without confirmation
juggle config ac clear --yes
```

### Agent Run (Non-Interactive)

When running without a terminal (stdin not a TTY), the session selector is skipped:

```bash
# Specify session explicitly
juggle agent run my-session

# Or target all balls without a session
juggle agent run all

# Target a specific ball
juggle agent run --ball ball-id
```

The agent run command will error gracefully if no session is provided and stdin is not a terminal.

## Command Reference

### Planning Commands

| Command                                        | Description                 |
| ---------------------------------------------- | --------------------------- |
| `juggle sessions create <id> -m "desc"`        | Create session              |
| `juggle sessions create <id> --context "text"` | Create with initial context |
| `juggle sessions context <id> --set "text"`    | Set session context         |
| `juggle sessions context <id> --edit`          | Edit context in $EDITOR     |
| `juggle plan "intent" -c "criterion"`          | Create ball with criteria   |
| `juggle plan "intent" --session <id>`          | Create ball in session      |
| `juggle plan "intent" --depends-on <ball-id>`  | Create ball with dependency |
| `juggle plan "intent" --non-interactive`       | Create ball without prompts |

### State Update Commands

| Command                                             | Description                   |
| --------------------------------------------------- | ----------------------------- |
| `juggle update <id> --state <state>`                | Update ball state             |
| `juggle update <id> --state blocked --reason "why"` | Block with reason             |
| `juggle update <id> --add-dep <ball-id>`            | Add dependency                |
| `juggle update <id> --remove-dep <ball-id>`         | Remove dependency             |
| `juggle update <id> --set-deps <ids>`               | Replace all dependencies      |
| `juggle progress append <session> "text"`           | Log progress entry            |
| `juggle show <id> [--json]`                         | View ball details             |
| `juggle sessions show <id>`                         | View session with balls       |
| `juggle sessions delete <id> --yes`                 | Delete session without prompt |
| `juggle delete <id> --force`                        | Delete ball without prompt    |

## File Locations

Data is stored in these locations, but **prefer CLI commands over direct file access**:

- Balls: `.juggle/balls.jsonl` (use `juggle list --format json` instead)
- Sessions: `.juggle/sessions/<id>/session.json` (use `juggle sessions show <id>` instead)
- Progress: `.juggle/sessions/<id>/progress.txt` (use `juggle sessions show <id>` instead)

Direct file access should only be used as a last resort when the CLI doesn't provide the needed functionality.
