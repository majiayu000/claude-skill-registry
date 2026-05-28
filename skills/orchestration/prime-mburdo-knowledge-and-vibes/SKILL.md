---
name: prime
description: New agent startup checklist for Agent Mail and Beads. Use when starting a new agent session, when the user says "prime" or "startup", or when beginning work on a multi-agent project.
---

# Prime — Session Startup

Complete startup checklist for new agent sessions. Direct execution (no subagents).

> **Design rationale:** This skill executes directly rather than spawning subagents because each step is a simple command sequence (~200 tokens each), not substantial analytical work. Per Lita research: "Simple agents achieve 97% of complex system performance with 15x less code." Subagent overhead would exceed actual work.

## When This Applies

| Signal | Action |
|--------|--------|
| New session starting | Run full checklist |
| User says "/prime" | Run full checklist |
| User says "startup" or "initialize" | Run full checklist |
| Multi-agent coordination needed | Run full checklist |

---

## Tool Reference

### Agent Mail (MCP)
| Tool | Purpose |
|------|---------|
| `macro_start_session(human_key, program, model)` | **PREFERRED:** All-in-one startup |
| `ensure_project(human_key)` | Initialize project in Agent Mail |
| `register_agent(project_key, program, model)` | Register and get agent name |
| `set_contact_policy(agent_name, policy)` | Set to "open" for coordination |
| `fetch_inbox(agent_name, limit)` | Check for messages |
| `send_message(to, subject, body_md)` | Send greeting/announcements |

### Bash Commands
| Command | Purpose |
|---------|---------|
| `cm context "task description" --json` | Get patterns + anti-patterns before work |
| `cass search "query" --robot --days 7` | Search session history |
| `bd ready --json` | List available tasks |
| `bv --robot-triage` | Get task recommendations |
| `git status` | Check repo state |
| `git log --oneline -5` | Recent commits |

---

## Execution Flow

Execute these steps directly. No subagents needed.

### Step 1: Register Identity

**PREFERRED — Use macro for simplicity:**

```python
result = macro_start_session(
    human_key="PROJECT_PATH",  # Absolute path to project
    program="claude-code",
    model="opus-4.5",
    inbox_limit=10
)
agent_name = result["agent"]["name"]  # e.g., "BlueLake"
```

**ALTERNATIVE — Manual steps:**

```python
# 1. Ensure project exists
ensure_project(human_key="PROJECT_PATH")

# 2. Register agent (name is auto-assigned)
result = register_agent(
    project_key="PROJECT_PATH",
    program="claude-code",
    model="opus-4.5",
    task_description="Agent initializing..."
)
agent_name = result["name"]  # SAVE THIS

# 3. Set contact policy for coordination
set_contact_policy(
    project_key="PROJECT_PATH",
    agent_name=agent_name,
    policy="open"
)
```

**Update terminal title:**
```bash
echo -ne "\033]0;[{agent_name}] | PROJECT_NAME\007"
```

---

### Step 2: Orient

**Read project documentation:**
```
Read("AGENTS.md")     # Agent workflow instructions
Read("CLAUDE.md")     # Project overview
```

**Check recent session history:**
```bash
cass search "PROJECT_NAME" --workspace "PROJECT_PATH" --robot --days 7 --limit 5
```

**Get learned patterns:**
```bash
cm context "starting work on PROJECT_NAME" --json
```

**Check git state:**
```bash
git status
git log --oneline -5
git branch
```

**Discover active agents:**
```python
ReadMcpResourceTool(
    server="mcp-agent-mail",
    uri="resource://agents/PROJECT_PATH"
)
```

---

### Step 3: Coordinate

**Check inbox:**
```python
messages = fetch_inbox(
    project_key="PROJECT_PATH",
    agent_name=agent_name,
    include_bodies=True,
    limit=20
)
```

**Categorize messages:**
- **Urgent** — Requires response before starting work
- **Informational** — [CLAIMED], [CLOSED] announcements
- **Acknowledgement required** — ack_required=True

**Note file reservations** from other agents (these are off-limits).

**Send greeting (if other agents active):**
```python
send_message(
    project_key="PROJECT_PATH",
    sender_name=agent_name,
    to=[active_agents],
    subject="Agent Online",
    body_md="I'm online. Focusing on: [task]. What needs attention?",
    importance="normal"
)
```

---

### Step 4: Discover Work

**Get recommendations:**
```bash
bv --robot-triage      # Priority analysis
bv --robot-next        # Single best task
```

**Get ready tasks:**
```bash
bd ready --json
```

**Check already claimed:**
```bash
bd list --status in_progress --json
```

**Filter by file availability:**
- Check each ready task's required files
- Exclude tasks where files are reserved by others
- Recommend highest-priority available task

---

### Step 5: Output Summary

Present to user:

```markdown
## Agent Initialized

**Name:** {agent_name}
**Project:** PROJECT_NAME
**Branch:** {git_branch}

### Context
- Recent sessions: {summary from CASS}
- Active agents: {list or "none"}
- Inbox: {count} messages ({urgent} urgent)
- Blocked files: {list or "none"}

### Learned Patterns
{relevant patterns from cm}

### Recommended Task
**ID:** {task_id}
**Title:** {task_title}
**Priority:** {priority}
**Files:** {file_scope}

Ready to claim? Use `/advance` to claim and begin work.
```

---

## Mandatory Gates

After priming, these gates apply to all work:

| Gate | Requirement | Evidence |
|------|-------------|----------|
| **TDD-first** | Write tests before implementation | 45.97% higher success rate |
| **ubs --staged** | Security scan before every commit | ~40% of LLM code has vulnerabilities |
| **Max 3 iterations** | Stop after 3 repair attempts | Security degrades with more |
| **Escalate on failure** | Create spike, notify operator | Don't waste time debugging |

---

## Quick Reference

```bash
# Register (preferred)
macro_start_session(human_key=PROJECT_PATH, program="claude-code", model="opus-4.5")

# Orient
cass search "PROJECT" --robot --days 7
cm context "task" --json
git status

# Coordinate
fetch_inbox(agent_name=YOUR_NAME, limit=20)
send_message(to=[...], subject="Agent Online", ...)

# Discover
bv --robot-triage
bd ready --json
```

---

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Skip registration | Can't coordinate | Always register first |
| Ignore inbox | Miss urgent messages | Check before claiming |
| Ignore reservations | File conflicts | Respect all reservations |
| Skip cm context | Miss learned patterns | Always check patterns |
| Claim without checking | Duplicate work | Verify availability first |

---

## See Also

- `/advance` — Claim and work on tasks
- `/recall` — Get context from past sessions
- `beads-cli/` — bd command reference
- `beads-viewer/` — bv command reference
