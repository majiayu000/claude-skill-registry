---
name: work-loop
description: Queue-driven work orchestrator. Processes requests from do-work/requests/ using isolated sub-agents. Use to start or resume the work loop.
user-invocable: true
context: fork
argument-hint: "[--once|--watch]"
---

# Work Loop

Queue-driven development workflow that processes requests using isolated sub-agents.

## Core Principle

**The Orchestrator never performs task work.**

Every request spawns a fresh sub-agent. Sub-agents die after completion. This ensures:
- Context isolation between tasks
- Clean state for each request
- Crash resilience
- Predictable execution

## Directory Structure

```
do-work/
├── requests/     # Pending work (input queue)
├── in-progress/  # Currently executing (max 1)
├── archive/      # Completed successfully
└── errors/       # Failed with error summary
```

If directories don't exist, create them on first run.

## Workflow

### 1. Initialize

Check for and create required directories:

```bash
mkdir -p do-work/{requests,in-progress,archive,errors}
```

### 2. Check Queue

```bash
ls -1 do-work/requests/*.md 2>/dev/null | head -1
```

If empty and `--watch` not set, exit cleanly.
If empty and `--watch` set, poll every 5 seconds.

### 3. Process Request

For each request file:

#### 3a. Claim Request

Move from `requests/` to `in-progress/`:

```bash
mv do-work/requests/FILENAME.md do-work/in-progress/
```

Only ONE file should be in `in-progress/` at a time.

#### 3b. Parse Request

Read the request file and extract:
- **Intent** - What outcome is desired
- **Context** - Relevant constraints
- **Tasks** - Steps to complete
- **Done When** - Completion criteria

#### 3c. Spawn Sub-Agent

Create a fresh execution context with:
- Request content only
- Current repo state
- No previous task context

The sub-agent operates in three phases:

**Planning Phase:**
- Analyze the request
- Identify files to modify
- Determine approach
- Validate against "Done When" criteria

**Execution Phase:**
- Implement the tasks
- Make necessary changes
- Run relevant tests

**Validation Phase:**
- Verify "Done When" criteria met
- Run tests if applicable
- Check for regressions

#### 3d. Handle Outcome

**Success:**
```bash
mv do-work/in-progress/FILENAME.md do-work/archive/
```

**Failure:**
Append error summary to file, then:
```bash
mv do-work/in-progress/FILENAME.md do-work/errors/
```

Error summary format:
```markdown
---
## Execution Failed

**Timestamp:** 2026-01-28T14:30:22Z
**Reason:** Tests failed after implementing feature
**Details:**
- test_user_auth.py::test_login FAILED
- Expected redirect, got 500 error

**Attempted:**
- Added login route
- Created auth middleware
- Tests revealed database connection issue
```

### 4. Continue or Exit

After processing:
- If more requests in queue → process next
- If queue empty and `--once` → exit
- If queue empty and `--watch` → poll for new requests

## Commands

| Command | Behavior |
|---------|----------|
| `/work-loop` | Process all requests, then exit |
| `/work-loop --once` | Process ONE request, then exit |
| `/work-loop --watch` | Continuous mode, poll for new requests |

## Sub-Agent Rules

Sub-agents MUST:
- Work only on the assigned request
- Stop when "Done When" criteria are met
- Not access other requests
- Not persist state between requests
- Report clear success/failure

Sub-agents MUST NOT:
- Process multiple requests
- Access the orchestrator's context
- Modify the queue directly
- Retry on failure (orchestrator decides)

## Recovery

### Crash Recovery

If work-loop crashes mid-execution:
- Check `in-progress/` on restart
- File there = incomplete request
- Move back to `requests/` or `errors/` based on state

### Stuck Request

If a request is in `in-progress/` for too long:
1. Check if sub-agent is still running
2. If not, move to `errors/` with timeout note
3. If yes, wait or kill based on user preference

### Manual Intervention

User can always:
- Move files between directories manually
- Edit request files to clarify
- Delete requests that are no longer needed
- Re-queue errors by moving to `requests/`

## Integration with Thunderdome

The work-loop integrates with Thunderdome:

- `/thunderdome status` shows queue depth
- `/thunderdome debrief` verifies queue is empty
- Gamification scores apply to completed requests

Typical session:
```
/thunderdome          # Check status
/capture-request      # Capture work items
/work-loop            # Process the queue
/thunderdome debrief  # Verify and close
```

## Configuration

Optional `.thunderdome/config.json` settings:

```json
{
  "workLoop": {
    "maxExecutionTime": 600,
    "pollInterval": 5,
    "autoRetry": false,
    "notifyOnComplete": true
  }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `maxExecutionTime` | 600 | Seconds before timeout |
| `pollInterval` | 5 | Seconds between polls in watch mode |
| `autoRetry` | false | Auto-retry failed requests |
| `notifyOnComplete` | true | Notify when queue empties |

## Example Session

```
$ claude

> /capture-request Add user authentication to the app

Captured 1 request:
1. do-work/requests/20260128-143022-user-auth.md
   Intent: Add user authentication

Run `/work-loop` to begin processing.

> /work-loop

Processing: 20260128-143022-user-auth.md
Intent: Add user authentication

[Sub-agent spawned]
- Planning: Identified auth approach
- Executing: Adding login page...
- Executing: Adding auth middleware...
- Validating: Running tests...

Completed: user-auth
Moved to: do-work/archive/

Queue empty. Work loop complete.

> /thunderdome debrief

Tests: 47 passed
Changes: 5 files modified
Status: ALL CLEAR - Safe to close
```

## Guarantees

1. **Context Isolation** - Each request runs with fresh context
2. **Atomic Execution** - Requests complete or fail, no partial states left hanging
3. **Crash Resilience** - Recovery possible from any interruption
4. **Audit Trail** - All requests preserved in archive/errors
5. **Single Execution** - Only one request processes at a time
