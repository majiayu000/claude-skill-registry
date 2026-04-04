---
name: agent-board-cli
description: |
  Command-line task management tool for AI coding agents and humans. Provides local SQLite-based task boards for tracking work items, checklists, and comments without requiring an external API.
  
  Use this skill when:
  - Managing multi-step coding tasks
  - Tracking progress on complex implementations  
  - Breaking down work into checkable subtasks
  - Documenting decisions and progress via comments
  - Coordinating work across agent sessions
license: MIT
tags:
  - task-management
  - cli
  - agent-tools
  - productivity
  - rust
metadata:
  author: Stakpak
  version: "0.1.11"
---

# Agent-Board CLI

## Quick Reference

```bash
# Version
agent-board version                     # Show version info
agent-board --version                   # Short form

# Get any entity by ID (auto-detects type from prefix)
agent-board get <board_id>              # Get board overview
agent-board get <card_id>               # Get card details
agent-board get <agent_id>              # Get agent details

# List operations
agent-board list boards [--include-deleted]
agent-board list cards <board_id> [--status todo|in-progress|pending-review|done] [--include-deleted]
agent-board list cards <board_id> --tag blocked --tag needs-human  # Filter by tags (AND logic)
agent-board list agents [--include-inactive]
agent-board list comments <card_id>

# Create operations
agent-board create board "Project Name" --description "Description"
agent-board create card <board_id> "Task name" --description "Details" --status todo
agent-board create agent [name] [--command stakpak] [--description "Agent purpose"]
agent-board create checklist <card_id> --item "Step 1" --item "Step 2"  # Adds items to card's checklist
agent-board create comment <card_id> "Progress update or notes"

# Update operations
agent-board update board <board_id> --name "New name" --description "New desc"
agent-board update card <card_id> --status in-progress --assign-to-me
agent-board update card <card_id> --add-tag urgent --remove-tag blocked
agent-board update agent <agent_id> --name new-name --workdir .
agent-board update checklist-item <item_id> --check    # Mark complete
agent-board update checklist-item <item_id> --uncheck  # Mark incomplete

# Delete operations (soft delete for boards/cards/agents, hard delete for others)
agent-board delete board <board_id>
agent-board delete card <card_id>
agent-board delete agent <agent_id>
agent-board delete comment <comment_id>
agent-board delete checklist-item <item_id>

# Agent identity
agent-board whoami                      # Show current agent identity

# Get my assigned cards
agent-board mine [--status todo|in-progress|pending-review|done]
```

## Installation

```bash
# Homebrew (recommended)
brew tap stakpak/stakpak && brew install agent-board

# Direct download (replace PLATFORM: darwin-aarch64, darwin-x86_64, linux-x86_64, linux-aarch64)
curl -L https://github.com/stakpak/agent-board/releases/latest/download/agent-board-PLATFORM.tar.gz | tar xz
sudo mv agent-board /usr/local/bin/

# Build from source
cargo build --release  # Binary at ./target/release/agent-board
```

## Agent Identity

Identity must be **explicitly registered** before using `--assign-to-me` or `--status in-progress`:

```bash
# 1. Register an agent (auto-generates name like "swift-falcon")
agent-board create agent
# Created agent: agent_abc123 (Name: swift-falcon)
# To use this agent, run:
#   export AGENT_BOARD_AGENT_ID=agent_abc123

# Or with explicit name
agent-board create agent code-reviewer --command claude

# 2. Set identity for session (required before claiming cards)
export AGENT_BOARD_AGENT_ID=agent_abc123

# 3. Now you can claim cards and set status
agent-board update card card_xyz --status in-progress --assign-to-me

# Verify identity (warns if wrong directory)
agent-board whoami
```

**Note:** Using `--assign-to-me` or `--status in-progress` without `AGENT_BOARD_AGENT_ID` set will error with setup instructions.

Data stored in `~/.agent-board/data.db`. Override: `export AGENT_BOARD_DB_PATH=/path/data.db`

## Workflow Patterns

### Starting a New Task

```bash
# 1. Find or create a board
agent-board list boards
agent-board create board "Feature Development" --description "Q1 features"

# 2. Create a card for the task
agent-board create card board_abc123 "Implement user authentication" \
  --description "Add OAuth2 login flow with Google and GitHub providers"

# 3. Break down into subtasks (each card has one checklist)
agent-board create checklist card_xyz789 \
  --item "Set up OAuth client credentials" \
  --item "Create auth endpoints" \
  --item "Add session management" \
  --item "Write integration tests" \
  --item "Update documentation"

# 4. Claim the card and start working
agent-board update card card_xyz789 --status in-progress --assign-to-me

# 5. Document that you're starting
agent-board create comment card_xyz789 "Beginning OAuth implementation"
```

### Tracking Progress

```bash
# Check off completed subtasks
agent-board update checklist-item item_001 --check
agent-board update checklist-item item_002 --check

# Add progress notes
agent-board create comment card_xyz789 "OAuth endpoints complete. Starting session management."

# View current state
agent-board get card_xyz789
```

### Completing Work

```bash
# Check remaining items
agent-board update checklist-item item_003 --check
agent-board update checklist-item item_004 --check
agent-board update checklist-item item_005 --check

# Mark done (assignment preserved for history)
agent-board update card card_xyz789 --status done

# Add completion summary
agent-board create comment card_xyz789 "Implementation complete. All tests passing."
```

### Reviewing Work

```bash
# See all your assigned cards
agent-board mine

# Filter by status
agent-board mine --status in-progress

# Get board overview
agent-board get board_abc123

# List all cards on a board
agent-board list cards board_abc123 --status todo
```

## Output Formats

Use `--format` to control output:

| Format | Use Case |
|--------|----------|
| `table` | Human-readable display (default) |
| `json` | Parsing with jq, programmatic access |
| `simple` | Just IDs, one per line, for scripting |

```bash
# Get card ID for scripting
CARD_ID=$(agent-board create card board_123 "New task" --format simple)

# Get full JSON for parsing
agent-board get card_xyz789 --format json | jq '.status'
```

## Status Values

| Status | CLI Value | Meaning |
|--------|-----------|---------|
| Todo | `todo` | Not started |
| In Progress | `in-progress` | Currently being worked on |
| Pending Review | `pending-review` | Work complete, awaiting review |
| Done | `done` | Completed and reviewed |

**Note:** Use hyphens on the command line (e.g., `in-progress`, `pending-review`), not underscores.

## Card Assignment

Claim cards with `--assign-to-me`:
```bash
# Claim a card when starting work
agent-board update card card_123 --status in-progress --assign-to-me
```

Assignment is preserved after completion for history/accountability.

Explicit assignment control:
```bash
# Assign to specific agent
agent-board update card card_123 --assign agent_abc123

# Unassign card (only if needed)
agent-board update card card_123 --assign null
```

## Tags

Organize cards with tags:

```bash
# Add tags
agent-board update card card_123 --add-tag urgent --add-tag backend

# Remove tags
agent-board update card card_123 --remove-tag urgent
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 4 | Not found (card, board, etc.) |
| 5 | Permission denied |
| 6 | Session conflict |

## Human Review (Optional)

Cards can flow `in-progress` → `done` directly. Use these only when human input is needed:

| Scenario | Mechanism | When |
|----------|-----------|------|
| **Blocked** | `--add-tag blocked --add-tag needs-human` | Cannot continue without human input |
| **Review** | `--status pending-review` | Work done, want human verification |

```bash
# Blocked: need human help to proceed
agent-board update card card_123 --add-tag blocked --add-tag needs-human
agent-board create comment card_123 "BLOCKED: Need cost approval before provisioning"

# Review: work complete, want verification
agent-board update card card_123 --status pending-review
agent-board create comment card_123 "Ready for review: verify terraform plan"
```

**Common tags:** `blocked`, `needs-human`, `expedite`, `security-review`, `cost-approval`

## Best Practices for Agents

1. **Register identity first** with `agent-board create agent [name]`
2. **Set `AGENT_BOARD_AGENT_ID`** before starting work
3. **Use `--assign-to-me`** when claiming a card to start work
4. **Think Kanban** - Cards represent discrete, deliverable work items that flow through the board
5. **Add comments** when starting, making progress, or completing work
6. **Use descriptive card names** that capture the task intent
7. **Keep assignment on completion** - Don't unassign when marking done (preserves history)
8. **Check `agent-board mine`** at session start to see pending work
9. **Use `--format json`** when you need to parse output programmatically
10. **Use `blocked` + `needs-human` tags** when you cannot continue without human input
11. **Use `pending-review` status** when work is done but you want human verification (optional)

### Cards vs Checklists

Each card has a single checklist for tracking subtasks within that work item.

| Use Cards | Use Checklists |
|-----------|----------------|
| Parallelizable work | Sequential steps in one deliverable |
| Different dependencies | Shared dependencies |
| Independent status tracking | Linear progress within a card |

**Simple task:** "Add Docker support" → One card with checklist items (Dockerfile, compose, test, docs)

**Complex task:** "Migrate to microservices" → Multiple cards (auth service, payment service, API gateway, testing), each with its own checklist

## Data Location

All data persists in a local SQLite database:
- Default: `~/.agent-board/data.db`
- Override: Set `AGENT_BOARD_DB_PATH` environment variable

The database is created automatically on first use.
