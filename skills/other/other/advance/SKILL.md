---
name: advance
description: Claim and work on beads safely with proper coordination. Use when starting work, finishing work, or finding the next task. Covers the full bead lifecycle: discover → verify → claim → work → close.
---

# Advance — Bead Lifecycle

Complete bead lifecycle: discover → verify → claim → work → close. Direct execution.

> **Design rationale:** This skill executes directly rather than spawning subagents because each step is a simple command sequence (~200 tokens each), not substantial analytical work. Per Lita research: "Simple agents achieve 97% of complex system performance with 15x less code." Subagent overhead would exceed actual work.

## When This Applies

| Signal | Action |
|--------|--------|
| User says "next task" or "what's next" | Run discovery → claim |
| User says "/advance" | Run full protocol |
| Just finished a task | Close out, then discover |
| Starting work on a specific bead | Verify → claim |
| User says "claim" or "start" | Verify → claim |
| User says "done" or "close" | Run close protocol |

---

## Tool Reference

### Agent Mail (MCP)
| Tool | Purpose |
|------|---------|
| `fetch_inbox(agent_name)` | Check for messages before claiming |
| `file_reservation_paths(paths, exclusive)` | Reserve files before editing |
| `release_file_reservations(agent_name)` | Release files after closing |
| `send_message(to, subject, body_md, thread_id)` | Announce [CLAIMED]/[CLOSED] |

### Bash Commands
| Command | Purpose |
|---------|---------|
| `bd list --status in_progress --json` | Check for current work |
| `bd ready --json` | List available tasks |
| `bd update <id> --status in_progress --assignee NAME` | Claim task |
| `bd close <id> --reason "..."` | Close completed bead |
| `bd dep tree <id>` | View dependencies |
| `bd blocked` | View blocked tasks |
| `bv --robot-triage` | Get recommendations |
| `bv --robot-next` | Get single best task |
| `bv --robot-plan` | Get execution order |
| `cm context "task description" --json` | Get patterns before starting |
| `pytest` | Run tests before closing |
| `ubs --staged` | Security scan (MANDATORY) |

---

## Execution Flow

Execute these steps directly. No subagents needed.

### Step 1: Close Out Previous Work

Check for in-progress work:
```bash
bd list --status in_progress --assignee YOUR_NAME --json
```

**If work exists:**

1. **Run verification gates:**
   ```bash
   pytest  # or your test command
   ubs --staged  # MANDATORY - never skip
   ```

2. **Commit changes:**
   ```bash
   git add -A
   git commit -m "Implement {feature}

   Closes {bead-id}"
   ```
   Always include `.beads/issues.jsonl` in commits.

3. **Close sub-beads FIRST, then parent:**
   ```bash
   bd close {id}.1 --reason "Completed: {summary}"
   bd close {id}.2 --reason "Completed: {summary}"
   bd close {id} --reason "Completed: {summary}"
   ```

4. **Release file reservations:**
   ```python
   release_file_reservations(
       project_key=PROJECT_PATH,
       agent_name=YOUR_NAME
   )
   ```

5. **Announce closure:**
   ```python
   send_message(
       project_key=PROJECT_PATH,
       sender_name=YOUR_NAME,
       to=[ALL_AGENTS],
       subject="[CLOSED] {id} - {title}",
       body_md="Completed **{id}**.\n\nTests: passing\nSecurity: clean\nReservations: released",
       thread_id="{id}"
   )
   ```

---

### Step 2: Discover Available Work

**Get recommendations:**
```bash
bv --robot-triage       # Priority recommendations
bv --robot-next         # Single best task
bv --robot-plan         # Execution order
```

**Get ready tasks:**
```bash
bd ready --json
```

**Check already claimed:**
```bash
bd list --status in_progress --json
```

**Discover active agents:**
```python
ReadMcpResourceTool(
    server="mcp-agent-mail",
    uri="resource://agents/{PROJECT_PATH}"
)
```

**Check inbox:**
```python
fetch_inbox(
    project_key=PROJECT_PATH,
    agent_name=YOUR_NAME,
    include_bodies=True,
    limit=10
)
```

Address urgent messages before claiming new work.

---

### Step 3: Verify Target Task

All must pass before claiming:

- [ ] Task status is `ready`
- [ ] No other agent has claimed it (check recent `[CLAIMED]` messages)
- [ ] Required files not reserved by others
- [ ] Dependencies satisfied (`bd dep tree {id}`)
- [ ] No blocking inbox messages

**Check task status:**
```bash
bd show {task_id} --json
```

**Check file availability:**
```python
# Test if files are available
file_reservation_paths(
    project_key=PROJECT_PATH,
    agent_name=YOUR_NAME,
    paths=["src/module/**"],
    ttl_seconds=60,      # Short test
    exclusive=False      # Just checking
)
```

**Check for claim conflicts:**
```python
search_messages(
    project_key=PROJECT_PATH,
    query="[CLAIMED] {task_id}"
)
```

**If ANY check fails → pick different task or coordinate first.**

If uncertain, ask:
```python
send_message(
    project_key=PROJECT_PATH,
    sender_name=YOUR_NAME,
    to=[OTHER_AGENTS],
    subject="Claiming task: {task-id}?",
    body_md="Planning to pick up **{task-id}**. Files: `src/...`. Conflicts?",
    importance="normal"
)
```

---

### Step 4: Claim

**Claim parent AND all sub-beads:**
```bash
bd update {id} --status in_progress --assignee YOUR_NAME
bd update {id}.1 --status in_progress --assignee YOUR_NAME
bd update {id}.2 --status in_progress --assignee YOUR_NAME
```

**CRITICAL:** Always claim parent AND all sub-beads together. If you only claim parent, other agents may grab sub-beads.

**Reserve files:**
```python
file_reservation_paths(
    project_key=PROJECT_PATH,
    agent_name=YOUR_NAME,
    paths=["src/module/**", "tests/**"],
    ttl_seconds=3600,    # 1 hour
    exclusive=True,
    reason="{bead-id}: {description}"
)
```

**Announce (MANDATORY):**
```python
send_message(
    project_key=PROJECT_PATH,
    sender_name=YOUR_NAME,
    to=[ALL_AGENTS],
    subject="[CLAIMED] {id} - {title}",
    body_md="""Starting work on **{id}**: {title}

**Files reserved:**
- src/module/**
- tests/**

**Sub-beads claimed:**
- {id}.1: {sub_title_1}
- {id}.2: {sub_title_2}
""",
    importance="normal",
    thread_id="{id}"
)
```

---

### Step 5: Get Context Before Working

After claiming, get patterns and anti-patterns:
```bash
cm context "{task-title}" --json
```

This returns:
- **Relevant rules** from past sessions
- **Anti-patterns** to avoid
- **Historical context** about similar work

---

### Step 6: Work (TDD-First)

Based on research (45.97% higher pass@1 rate with TDD):

1. **Check if tests exist in bead description**
2. If not, **write tests FIRST** (do not implement without tests)
3. Implement to pass tests
4. Run `ubs --staged` before any commit

**Max 3 repair iterations per bead.**

After 3 attempts:
1. **STOP** implementation immediately
2. **Create spike bead** to investigate
3. **Notify operator:**
   ```python
   send_message(
       project_key=PROJECT_PATH,
       sender_name=YOUR_NAME,
       to=["operator"],
       subject="[BLOCKED] {id} - Needs investigation",
       body_md="Bead {id} failed after 3 repair attempts.\n\nLast error: ...\nSpike created: {spike-id}",
       importance="high",
       thread_id="{id}"
   )
   ```

**Why the cap?** Security degrades with repeated self-correction. Models flip-flop on correct answers. Failing fast is safer than debugging loops.

---

### Step 7: Output Summary

Present to user:

```markdown
## Task Claimed

**Bead:** {id} - {title}
**Priority:** {priority}
**Files:** {file_list}

### Context from Memory
{relevant patterns from cm}

### TDD Checklist
- [ ] Write/review tests first
- [ ] Implement to pass tests
- [ ] Run `ubs --staged` before commit
- [ ] Max 3 repair iterations

Ready to begin implementation.
```

---

## Mandatory Gates

These gates apply to ALL bead work:

| Gate | Requirement | Evidence |
|------|-------------|----------|
| **TDD-first** | Write tests before implementation | 45.97% higher success rate |
| **ubs --staged** | Security scan before every commit | ~40% of LLM code has vulnerabilities |
| **Max 3 iterations** | Stop after 3 repair attempts | Security degrades with more |
| **Escalate on failure** | Create spike, notify operator | Don't waste time debugging |

---

## Dependency Management

### Types

| Type | Meaning | Example |
|------|---------|---------|
| `blocks` | A must complete before B can start | Schema blocks implementation |
| `discovered-from` | Found B while working on A | Bug found during feature work |

### Commands

```bash
# Add dependency (B is blocked by A)
bd dep add {child-id} {blocker-id} --type blocks

# View dependencies
bd dep tree {id}

# View blocked tasks
bd blocked

# Full graph analysis
bv --robot-triage
```

### Common Patterns

**Schema → Implementation → Tests:**
```bash
bd dep add impl-id schema-id --type blocks
bd dep add test-id impl-id --type blocks
```

**Discovered Issues:**
```bash
# While working on feature-123, found bug
bd create "Found: edge case in validation" -t bug
bd dep add {new-bug-id} feature-123 --type discovered-from
```

---

## Multi-Agent Coordination

When multiple agents are active:

### File Reservations

**Check for conflicts:**
```python
# If reservation fails, another agent has those files
# Options:
# 1. Pick different task
# 2. Coordinate via message
# 3. Wait for TTL expiry
```

**Extend if needed:**
```python
renew_file_reservations(
    project_key=PROJECT_PATH,
    agent_name=YOUR_NAME,
    extend_seconds=1800
)
```

### Inbox Protocol

- **Before claiming:** Check for recent `[CLAIMED]` messages
- **While working:** Check inbox every ~30 minutes
- **Look for:** API changes, coordination requests, blockers

### Thread IDs

Use bead ID as thread ID for all related messages:
```
Bead:           bd-123
Thread ID:      bd-123
Subject:        [CLAIMED] bd-123 - Title
Reservation:    reason="bd-123"
Commit:         Closes bd-123
```

### Conflict Resolution

| Conflict | Resolution |
|----------|------------|
| Both claimed same task | First [CLAIMED] wins, other picks new task |
| Both editing same file | Reservation holder wins, other waits |
| Dependency disagreement | Discuss in thread, escalate if stuck |

---

## Quick Reference

```bash
# Recommended next
bv --robot-triage
bv --robot-next          # Single best task

# Ready tasks
bd ready --json

# Claimed tasks
bd list --status in_progress --json

# Claim (always include sub-beads + assignee)
bd update {id} --status in_progress --assignee YOUR_NAME

# Close (sub-beads first)
bd close {id}.1 --reason "..."
bd close {id} --reason "..."

# Dependencies
bd dep add {child} {blocker} --type blocks
bd dep tree {id}
bd blocked
```

---

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Claim only parent | Sub-beads appear "ready" to others | Claim all sub-beads |
| Skip assignee | Can't track who's working | Always `--assignee` |
| Skip [CLAIMED] | Duplicate work | Always announce |
| Skip [CLOSED] | Stale state | Always announce |
| Close parent first | Sub-beads orphaned | Close sub-beads first |
| Hoard tasks | Blocks others | One task at a time |
| Skip file reservations | Merge conflicts | Reserve before editing |
| Implement before tests | 45.97% lower success rate | TDD-first always |
| Skip `ubs --staged` | ~40% of LLM code has vulnerabilities | Mandatory gate |
| Unlimited repair loops | Security degrades, models flip-flop | Max 3 iterations |
| Continue after 3 failures | Wastes time, introduces bugs | Stop, spike, escalate |
| Skip inbox checks | Miss coordination messages | Check before claiming |

---

## See Also

- `/prime` — Session startup
- `/calibrate` — Phase boundary checks
- `/release` — Pre-ship checklist
- `beads-cli/` — bd command reference
- `beads-viewer/` — bv command reference
