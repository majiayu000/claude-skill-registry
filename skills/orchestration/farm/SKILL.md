---
name: farm
description: 'Spawn Agent Farm for parallel issue execution. Mayor orchestrates crew via tmux + MCP Agent Mail. Replaces /crank for multi-agent work. Triggers: "farm", "spawn agents", "parallel work", "multi-agent".'
---

# Farm Skill

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Spawn an Agent Farm to execute multiple issues in parallel with witness monitoring.

## Architecture

```
Mayor (this session)
    |
    +-> ao farm start --agents N
    |       |
    |       +-> Pre-flight validation
    |       +-> Spawn agents in tmux (serial, 30s stagger)
    |       +-> Spawn witness in separate tmux session
    |
    +-> ao inbox (poll for updates)
    |
    +-> Witness sends "FARM COMPLETE" message
    |
    +-> /post-mortem (extract learnings)
```

## Execution Steps

Given `/farm [--agents N] [epic-id]`:

### Step 1: Pre-Flight Validation

**Run pre-flight checks before spawning any agents:**

```bash
ao farm validate 2>/dev/null
```

If not available, perform manual checks:

1. **Verify beads exist:**
```bash
ls .beads/issues.jsonl 2>/dev/null || echo "ERROR: No beads found. Run /plan first."
```

2. **Check ready issues:**
```bash
bd ready 2>/dev/null | wc -l
```
If 0 ready issues, STOP: "No ready issues. Check dependencies or run /plan."

3. **Detect circular dependencies:**
```bash
bd validate --check-cycles 2>/dev/null
```
If cycle detected, STOP with error listing the cycle.

4. **Verify disk space:**
```bash
df -h . | awk 'NR==2 {print $4}'
```
If < 5GB, warn user.

### Step 2: Determine Agent Count

**Default:** `N = min(5, ready_issues)`

**If --agents specified:** Use that value, but cap at ready_issues count.

```bash
READY_COUNT=$(bd ready 2>/dev/null | wc -l | tr -d ' ')
AGENTS=${N:-5}
AGENTS=$((AGENTS < READY_COUNT ? AGENTS : READY_COUNT))
```

If AGENTS = 0, STOP: "No work available for agents."

### Step 3: Spawn Agent Farm

**Start the farm with serial agent spawn (30s stagger):**

```bash
ao farm start --agents $AGENTS --epic <epic-id> 2>&1
```

This command:
1. Creates tmux session `ao-farm-<project>`
2. Spawns agents one at a time with 30s delay
3. Spawns witness in separate session `ao-farm-witness-<project>`
4. Writes `.farm.meta` with PIDs and state
5. Returns immediately with status message

**Expected output:**
```
Farm started: 5 agents, 1 witness
Session: ao-farm-nami
Witness: ao-farm-witness-nami
Check progress: ao inbox
Stop: ao farm stop
```

### Step 4: Monitor Progress (Loop)

**Tell the user farm is running, then monitor:**

```
Farm running. Check /inbox periodically for progress updates.

- Witness summarizes every 5 minutes
- Agents send completion messages per issue
- "FARM COMPLETE" signals all work done

Commands:
  ao inbox              - Check messages
  ao farm status        - Show agent states
  ao farm stop          - Graceful shutdown
```

**Optional: Periodically check inbox:**
```bash
ao inbox --since 5m 2>/dev/null
```

### Step 5: Handle Completion

When witness sends "FARM COMPLETE" message:

1. Verify all issues closed:
```bash
bd list --status open 2>/dev/null | wc -l
```

2. Clean up farm resources:
```bash
ao farm stop 2>/dev/null
```

3. Suggest next step:
```
Farm complete. X issues closed in Y minutes.
Run /post-mortem to extract learnings.
```

## Error Handling

### Circuit Breaker

If >50% agents fail within 60 seconds:
```bash
ao farm stop --reason "circuit-breaker"
```

Tell user: "Circuit breaker triggered. >50% agents failed. Check logs."

### Witness Death

If witness process dies (detected via PID check):
```bash
if ! kill -0 $(cat .witness.pid 2>/dev/null) 2>/dev/null; then
    echo "ERROR: Witness died. Stopping farm."
    ao farm stop --reason "witness-died"
fi
```

### Orphaned Issues

If issues stuck in_progress after farm stop:
```bash
ao farm resume
```

## Key Rules

- **Pre-flight first** - Never spawn without validation
- **Serial spawn** - 30s stagger prevents rate limits
- **Cap agents** - Never more agents than ready issues
- **Monitor witness** - Check PID health every 30s
- **Graceful stop** - Clean up all child processes
- **Resume capability** - Recover from disconnects

## Without ao CLI

If `ao farm` commands not available:

1. **Manual tmux spawn:**
```bash
# Create session
tmux new-session -d -s ao-farm

# For each agent
tmux send-keys -t ao-farm "claude --prompt 'Run /implement on next ready issue'" Enter
sleep 30  # Wait before next agent
```

2. **Manual witness:**
```bash
tmux new-session -d -s ao-farm-witness
tmux send-keys -t ao-farm-witness "claude --prompt 'Monitor tmux session ao-farm, summarize every 5m'" Enter
```

3. **Manual inbox (beads messages):**
```bash
bd list --type message --to mayor 2>/dev/null
```

## Agent Farm Behavior

Each spawned agent:
1. Runs `/implement` loop until no ready issues
2. Claims issues atomically via `bd claim`
3. Sends completion message via Agent Mail
4. Exits when no more work

Witness:
1. Polls agent tmux panes every 60s
2. Summarizes to mayor every 5m
3. Escalates blockers immediately
4. Sends "FARM COMPLETE" when all agents idle and no ready issues

## Exit Conditions

Farm exits when:
- All issues closed (success)
- Circuit breaker triggers (>50% fail)
- Witness dies unexpectedly (error)
- User runs `ao farm stop` (manual)
- Mayor disconnects (orphaned - use resume)
