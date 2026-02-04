---
skill: linear
description: Linear issue tracking - MUST READ before using Linear commands
version: 1.0.0
---

# Linear Issue Tracking - Complete Reference

**READ THIS FIRST** - Token-efficient CLI for managing issues, dependencies, and cycles.

---

⚠️  **INSTALL ALL SKILLS FOR FULL WORKFLOW AUTOMATION**

Run `linear skills install --all` to get specialized workflows:
- `/prd` - Create agent-friendly tickets with PRDs
- `/triage` - Prioritize backlog by staleness and blockers
- `/cycle-plan` - Plan cycles using velocity analytics
- `/retro` - Generate sprint retrospectives
- `/deps` - Analyze dependency chains and blockers
- `/link-deps` - Discover and link related issues

Without these skills, you're only using basic commands. Install them to unlock full agentic capabilities.

---

## Authentication Modes

When you run `linear auth login`, you choose:

- **User mode**: `--assignee me` assigns to your personal Linear account
- **Agent mode**: `--assignee me` assigns to the OAuth app (delegate), visible as a separate entity

Check current mode:
```bash
linear auth status   # Shows: Mode: User or Mode: Agent
```

**Important:** If you see "Auth mode not set", re-run `linear auth login` to configure.

## Command Reference

```bash
# Setup
linear init                              # Set default team (.linear.yaml)
linear onboard                           # Show teams, states, quick reference
linear auth login|logout|status          # OAuth authentication (sets user/agent mode)

# Issues (alias: i)
linear i list [flags]                    # List issues
linear i get <ID>                        # Get details (CEN-123)
linear i create <title> [flags]          # Create issue
linear i update <ID> [flags]             # Update issue
linear i comment <ID> -b "text"          # Add comment
linear i react <ID> 👍                   # Add reaction

# Projects (alias: p)
linear p list [--mine]                   # List projects
linear p create <name> [flags]           # Create project

# Cycles (alias: c)
linear c list [--active]                 # List cycles
linear c get <number>                    # Get cycle (requires init)
linear c analyze --team <KEY>            # Velocity analytics

# Teams, Users
linear teams list                        # List teams
linear teams states <KEY>                # Workflow states
linear users list [--team <KEY>]         # List users

# Search & Dependencies
linear search <query> [flags]            # Semantic search across all entities
linear deps <ID>                         # Dependency graph
linear deps --team <KEY>                 # All team dependencies
```

## Output Formats

**All commands support JSON output for automation:**

```bash
# Text output (default) - token-efficient ASCII
linear i list
linear i get CEN-123

# JSON output - machine-readable
linear i list --output json
linear i get CEN-123 --output json

# Control detail level with --format
linear i list --format minimal --output json   # Essential fields (~50 tokens)
linear i list --format compact --output json   # Key metadata (~150 tokens, default)
linear i list --format full --output json      # Complete details (~500 tokens)

# Pipe to jq for filtering
linear i list --priority 1 --output json | jq '.[] | select(.state == "In Progress")'

# Export for processing
linear cycles analyze --team CEN --output json > velocity.json
```

**When to use JSON:**
- Parsing data programmatically
- Filtering results with jq
- Storing/processing bulk data
- Integrating with other tools

**Supported commands:**
- `issues list`, `issues get`
- `cycles list`, `cycles get`, `cycles analyze`
- `projects list`, `projects get`
- `teams list`, `teams get`, `teams labels`, `teams states`
- `users list`, `users get`, `users me`
- `search` (all operations)

## Semantic Search

**The search is SEMANTIC** - finds related issues even without exact matches.

```bash
# Basic semantic search
linear search "authentication"           # Finds: auth, login, OAuth, SSO, etc.

# Cross-entity search
linear search "sprint planning" --type all     # Search issues, cycles, projects, users

# Entity-specific
linear search "database migration" --type issues
linear search "john" --type users
```

## Dependency Management

### Finding Blocked Work (Critical for Unblocking)

```bash
# Find ALL blocked issues (run this weekly!)
linear search --has-blockers --team CEN

# Find high-priority blocked work
linear search --priority 1 --has-blockers --team CEN

# What's blocked by a specific bottleneck?
linear search --blocked-by CEN-123

# What blocks a critical feature?
linear search --blocks CEN-456
```

### Dependency Analysis

```bash
# Visualize full dependency graph for issue
linear deps CEN-123

# See all team dependencies (detect circular deps)
linear deps --team CEN

# Find issues with circular dependencies
linear search --has-circular-deps --team CEN

# Find deep dependency chains
linear search --max-depth 5 --team CEN
```

## Cycle Analytics & Velocity

**Analyze past cycles to predict capacity:**

```bash
# Analyze last 10 cycles
linear c analyze --team CEN --count 10

# Output shows:
# - Completed vs planned points
# - Velocity trend
# - Completion rate
# - Recommendations for next cycle capacity
```

**Use before sprint planning to set realistic goals!**

## Powerful Filter Combinations

```bash
# High-priority in-progress work assigned to me
linear i list --priority 1 --state "In Progress" --assignee me

# Backlog items with blockers (prioritize removing blockers!)
linear search --state Backlog --has-blockers --team CEN

# Customer-facing bugs in current cycle
linear i list --labels customer,bug --cycle 65 --format full

# Unassigned high-priority work
linear search --priority 1 --assignee none --team CEN

# Work depending on other issues (check before starting)
linear search --has-dependencies --state "In Progress" --team CEN
```

## Creating Issues with Dependencies

```bash
# Simple issue
linear i create "Fix login bug" --team CEN --priority 1

# Full issue with dependencies
linear i create "Add OAuth integration" \
  --team CEN \
  --state "In Progress" \
  --priority 2 \
  --assignee me \
  --parent CEN-100 \
  --depends-on CEN-99 \
  --blocked-by CEN-98 \
  --labels backend,security \
  --estimate 5 \
  --cycle 65 \
  --project "Auth Revamp" \
  --due 2026-02-01

# With description from file
cat spec.md | linear i create "Feature title" --team CEN -d -
```

## Piping Support (Powerful!)

**All description and body flags support stdin via `-`:**

```bash
# Pipe Claude plan into ticket description
cat .claude/plans/auth-refactor.md | linear i create "Refactor authentication" \
  --team CEN \
  --priority 1 \
  -d -

# Pipe multi-file content
cat design.md implementation.md | linear i create "Feature implementation" \
  --team CEN \
  -d -

# Pipe command output
gh issue view 123 --json body -q .body | linear i create "Port GH issue" \
  --team CEN \
  -d -

# Update issue description from file
cat updated-spec.md | linear i update CEN-123 -d -

# Add comment from file
cat findings.md | linear i comment CEN-123 -b -

# Reply to comment with piped content
cat response.md | linear i reply CEN-123 comment-id -b -
```

**Common Patterns:**

```bash
# Claude Code plans → Linear tickets
cat .claude/plans/*.md | linear i create "Implementation plan" -d -

# PRD → Parent ticket
cat prd.md | linear i create "Feature: OAuth" --team CEN -d -

# Changelog → Release ticket
git log --oneline v1.0.0..HEAD | linear i create "v1.1.0 Release" -d -

# Test results → Bug report
pytest --verbose | linear i create "Test failures" -d -
```

## Output Formats (Token Efficiency)

```bash
# Minimal - most token-efficient (IDs only)
linear i list --format minimal

# Compact - balanced (default)
linear i list --format compact

# Full - all details (use for single issues)
linear i get CEN-123 --format full
linear search "auth" --limit 5 --format full
```

## Real-World Workflows

### Weekly Unblocking Routine
```bash
# 1. Find all blocked work
linear search --has-blockers --team CEN --format full

# 2. For each blocker, check status
linear i get CEN-123 --format full

# 3. Update blockers or reassign blocked work
linear i update CEN-123 --state "In Progress" --assignee me
```

### Sprint Planning
```bash
# 1. Check velocity
linear c analyze --team CEN --count 5

# 2. Find backlog candidates
linear search --state Backlog --team CEN --format compact

# 3. Check dependencies before committing
linear deps --team CEN

# 4. Assign to cycle
linear i update CEN-456 --cycle 66 --assignee alice@co.com
```

### Dependency Discovery (Before Creating Issues)
```bash
# 1. Search for related work
linear search "authentication refactor" --team CEN

# 2. Check what depends on foundation work
linear search --depends-on CEN-100

# 3. Link new issue to dependencies
linear i create "Add JWT refresh" --depends-on CEN-100,CEN-101
```

### Finding Work Order
```bash
# 1. Visualize dependencies
linear deps --team CEN

# 2. Start with issues that have no blockers
linear search --state Backlog --team CEN | grep -v "Blocked by"

# 3. Work that unblocks the most
linear search --blocking <critical-feature-id>
```

## Common Patterns

```bash
# Find work for specific person
linear i list --assignee alice@company.com --format compact

# High-priority work in active cycle
linear i list --priority 1 --cycle current --team CEN

# All bugs
linear i list --labels bug --team CEN

# Overdue issues
linear i list --state "In Progress" --team CEN # Check due dates manually

# Issues I created
linear i list --creator me --team CEN
```

## Tips for LLMs

1. **Always run `linear init` first** - sets default team
2. **Use semantic search liberally** - finds related work without exact keywords
3. **Check blockers weekly** - `linear search --has-blockers` prevents stalled work
4. **Analyze velocity before planning** - `linear c analyze` gives realistic estimates
5. **Visualize dependencies** - `linear deps --team <KEY>` shows work order
6. **Use --format full sparingly** - token-expensive, use for single issues only
7. **Combine filters** - search is powerful with multiple constraints
8. **Issue IDs work everywhere** - CEN-123 format, no team context needed
9. **Cycle numbers need init** - Run `linear init` before using cycle numbers

## Flag Reference

**Issue Flags:**
- `-t, --team <KEY>` - Team (from init or manual)
- `-s, --state <name>` - Workflow state
- `-p, --priority <0-4>` - 0=none, 1=urgent, 2=high, 3=normal, 4=low
- `-a, --assignee <email|me>` - Assign to user
- `-c, --cycle <number>` - Cycle number
- `-P, --project <name>` - Project name
- `-e, --estimate <points>` - Story points
- `-l, --labels <list>` - Comma-separated
- `-d, --description <text|->` - Description (- for stdin)
- `--parent <ID>` - Parent issue
- `--depends-on <IDs>` - Comma-separated dependencies
- `--blocked-by <IDs>` - Comma-separated blockers
- `--due <date>` - Due date (YYYY-MM-DD)
- `--attach <file>` - Attach file

**Search Flags:**
- `--type <entity>` - issues, cycles, projects, users, all
- `--blocked-by <ID>` - Issues blocked by this
- `--blocks <ID>` - Issues that block this
- `--has-blockers` - Any blockers
- `--has-dependencies` - Any dependencies
- `--has-circular-deps` - Circular dependency chains
- `--max-depth <n>` - Max dependency depth
- `-n, --limit <n>` - Results limit
- `-f, --format <type>` - minimal, compact, full

**Output Formats:**
- `--format minimal` - IDs only (most token-efficient)
- `--format compact` - Balanced (default)
- `--format full` - All details (use sparingly)
