---
name: multi-agent-coordination
description: Coordinate work between multiple AI agents in Agent Hive. Use this skill when multiple agents need to collaborate, managing dependencies between projects, preventing conflicts, using the coordination server, or understanding multi-agent workflows.
---

# Multi-Agent Coordination

Agent Hive enables coordination between multiple AI agents (Claude, Grok, Gemini, etc.) using shared memory and optional real-time coordination. This skill covers patterns for effective multi-agent collaboration.

## Coordination Layers

Agent Hive provides three coordination mechanisms:

### 1. Git-Based (Always Available)
- AGENCY.md files as shared memory
- Git commits track all state changes
- Pull/push for synchronization
- Works with any agent or environment

### 2. Cortex Orchestration (Automated)
- Runs every 4 hours via GitHub Actions
- Analyzes system state with LLM
- Identifies blocked tasks
- Updates project metadata

### 3. Real-Time Coordinator (Optional)
- FastAPI server for immediate coordination
- Prevents simultaneous claims
- TTL-based reservations
- Best for parallel agent sessions

## Ownership Protocol

### Claiming Ownership

Before working, an agent must claim the project:

```yaml
# In AGENCY.md frontmatter
owner: "claude-sonnet-4"  # Your agent identifier
```

### Ownership Rules

1. **Only claim unclaimed projects** - Check `owner: null`
2. **One owner at a time** - Never override another agent
3. **Release when done** - Set `owner: null` after work
4. **Respect claims** - If claimed, find another project

### Agent Identifiers

Use consistent naming for agent identification:

| Provider | Example Identifier |
|----------|-------------------|
| Anthropic Claude | `claude-sonnet-4`, `claude-opus-4` |
| OpenAI | `gpt-4-turbo`, `gpt-4o` |
| Google | `gemini-pro`, `gemini-ultra` |
| X.AI | `grok-beta`, `grok-2` |
| Custom | `my-agent-v1`, `research-bot` |

## Dependency Management

### Defining Dependencies

Use the `dependencies` field in AGENCY.md:

```yaml
dependencies:
  blocked_by: [auth-feature, database-setup]  # Must wait for these
  blocks: [frontend-integration]               # These wait for us
  parent: main-project                         # Hierarchical relationship
  related: [docs-project]                      # Informational link
```

### Dependency Flow

```
[auth-feature] ─────┐
                    ├──> [api-integration] ──> [frontend-integration]
[database-setup] ───┘
```

### Checking Dependencies

Before starting work, verify dependencies are met:

```bash
# Check dependency status
uv run python -m src.cortex --deps

# Or via Cortex Python API
from src.cortex import Cortex
cortex = Cortex()
blocking_info = cortex.is_blocked("my-project")
```

## Real-Time Coordinator

The optional coordination server prevents conflicts during parallel agent sessions.

### Starting the Server

```bash
# Start coordinator
uv run python -m src.coordinator

# Or with custom settings
COORDINATOR_HOST=0.0.0.0 COORDINATOR_PORT=8080 uv run python -m src.coordinator
```

### Using the Coordinator

#### Check Status
```bash
curl http://localhost:8080/health
```

#### Claim a Project
```bash
curl -X POST http://localhost:8080/claim \
  -H "Content-Type: application/json" \
  -d '{"project_id": "my-project", "agent_name": "claude-sonnet-4", "ttl_seconds": 3600}'
```

#### Release a Claim
```bash
curl -X DELETE http://localhost:8080/release/my-project
```

#### View All Reservations
```bash
curl http://localhost:8080/reservations
```

### Coordinator API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check and status |
| `/claim` | POST | Claim a project |
| `/release/{project_id}` | DELETE | Release by project ID |
| `/release/claim/{claim_id}` | DELETE | Release by claim ID |
| `/status/{project_id}` | GET | Check project status |
| `/reservations` | GET | List all active claims |
| `/extend/{project_id}` | POST | Extend claim TTL |

### TTL (Time-To-Live)

Claims automatically expire after TTL:
- Default: 3600 seconds (1 hour)
- Maximum: 86400 seconds (24 hours)
- Extend before expiration to continue working

## Multi-Agent Patterns

### 1. Sequential Handoff

Agents work one after another on the same project:

```
Agent A (Research) -> Agent B (Design) -> Agent C (Implementation)
```

**Protocol:**
1. Agent A completes work, adds notes, sets `owner: null`
2. Agent B sees unclaimed project, claims it
3. Agent B reads Agent A's notes, continues work
4. Repeat for Agent C

### 2. Parallel Independence

Multiple agents work on independent projects simultaneously:

```
Agent A -> [Project 1]
Agent B -> [Project 2]
Agent C -> [Project 3]
```

**Protocol:**
1. Each agent claims different project
2. No coordination needed during work
3. Use coordinator for claim management

### 3. Dependency Chain

Projects with sequential dependencies:

```
Agent A -> [Project 1] ──blocks──> Agent B -> [Project 2]
```

**Protocol:**
1. Agent B waits for Project 1 completion
2. Agent A sets `status: completed`
3. Cortex detects completion
4. Agent B sees Project 2 ready, claims it

### 4. Ensemble Collaboration

Multiple agents contribute to same project:

```
[Research Project]
├── Agent A: Sources 1-3
├── Agent B: Sources 4-6
└── Agent C: Synthesis
```

**Protocol:**
1. Create sub-tasks in AGENCY.md
2. Agents claim specific tasks via notes
3. Use atomic task markers
4. Final agent synthesizes contributions

## Conflict Resolution

### Optimistic Locking (Git)

If two agents modify the same file:
1. Git merge conflict occurs
2. Later agent must resolve
3. Review both changes
4. Commit resolved version

### Pessimistic Locking (Coordinator)

Coordinator prevents conflicts upfront:
1. First agent claims successfully
2. Second agent gets 409 Conflict
3. Second agent works on different project
4. First agent releases when done

### Conflict Prevention Tips

1. **Use coordinator for parallel sessions**
2. **Claim before reading** - Minimize race window
3. **Short sessions** - Reduce conflict probability
4. **Clear boundaries** - Define task ownership in notes
5. **Check before claiming** - Always verify `owner: null`

## Communication via Agent Notes

Agents communicate through the Agent Notes section:

```markdown
## Agent Notes
- **2025-01-15 16:00 - grok-beta**: Completed API integration.
  @claude-sonnet-4 - the auth module needs your review before merge.

- **2025-01-15 15:00 - claude-sonnet-4**: Starting auth implementation.
  Will coordinate with grok-beta on API integration.

- **2025-01-15 14:00 - gemini-pro**: Initial research complete.
  Key findings: [summary]. Recommending approach B for implementation.
```

### Note Conventions

- **@agent-name** - Direct mention for specific agent
- **BLOCKED** - Prefix for blocking issues
- **TODO** - Items for next agent
- **DECISION** - Record important choices

## Best Practices

1. **Always check ownership first** - Never override another agent
2. **Use coordinator for speed** - Faster than git-only coordination
3. **Keep notes detailed** - Other agents depend on your documentation
4. **Release promptly** - Don't hold claims unnecessarily
5. **Manage dependencies** - Keep `blocked_by`/`blocks` accurate
6. **Plan handoffs** - Document what's done and what's next
7. **Respect the protocol** - Coordination only works if everyone follows it
