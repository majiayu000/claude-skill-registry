---
name: skill-cli
description: CLI for Skill Recordings Support Agent platform. Use when investigating support issues, debugging workflows, inspecting Front/Inngest data, or managing app integrations.
allowed-tools: Bash(skill:*)
---

# Skill Recordings Support Agent CLI

CLI tool for the Skill Recordings support platform. Named `skill` after Skill Recordings (the company), not Claude skills.

## Quick start

```bash
skill front search "refund" --inbox inb_4bj7r  # Search conversations
skill front search --status unassigned          # Filter-only search
skill front conversation <id> -m                # Conversation with history
skill front assign cnv_xxx tea_xxx              # Assign to teammate
skill front reply cnv_xxx --body "On it"        # Draft reply (never auto-sends)
skill front api GET /me                         # Raw API escape hatch
skill inngest events --after 1h                 # Recent workflow events
skill inngest failures --after 2h               # Aggregate failure analysis
```

## Inngest Commands

### List events
```bash
skill inngest events                      # List recent events (default 20)
skill inngest events --after 2h           # Events from last 2 hours
skill inngest events --after 1d           # Events from last day
skill inngest events --name "support/inbound.received"  # Filter by name
skill inngest events --limit 50           # Limit results
skill inngest events --json               # JSON output
skill inngest events --dev                # Use dev server (localhost:8288)
```

### Get event details
```bash
skill inngest event <id>                  # Event details + triggered runs
skill inngest event <id> --json           # JSON output
```

### Get run details
```bash
skill inngest run <id>                    # Run status, output, timing
skill inngest run <id> --json             # JSON output
```

### Investigation Commands (Agent-Optimized)

These commands output JSON by default, optimized for agent consumption with aggregate stats and anomaly detection.

```bash
skill inngest inspect <event-id>          # Deep dive: event + runs + results
skill inngest failures --after 2h         # Aggregate failure analysis
skill inngest stats --after 1d            # Stats with anomaly detection
skill inngest trace <run-id>              # Full workflow trace
skill inngest search "email@example"      # Search event data for patterns
skill inngest search "refund" --field result  # Search specific field
```

#### Inspect (Deep Dive)
```bash
skill inngest inspect 01KFxxx
# Returns: event details, all triggered runs with results/errors, durations
```

#### Failures (Aggregate Analysis)
```bash
skill inngest failures --after 2h --limit 20
# Returns: total failures, grouped by error message, failure details
```

#### Stats (Pattern Detection)
```bash
skill inngest stats --after 1d
# Returns: event counts by type, workflow outcomes, skip reasons, anomalies
# Anomalies detected: high failure rate, more skipped than completed, etc.
```

#### Trace (Workflow Debug)
```bash
skill inngest trace 01KFxxx
# Returns: run details, input, result, error, duration
```

#### Search (Pattern Matching)
```bash
skill inngest search "purchase_id" --after 1h
skill inngest search "error" --field result --limit 100
# Returns: matching events with data
```

### Cancel run
```bash
skill inngest cancel <id>                 # Cancel running function
```

### Send signal
```bash
skill inngest signal <name>               # Resume waiting function
skill inngest signal approval:draft_123   # Example: approval signal
skill inngest signal <name> --data '{"approved":true}'  # With payload
```

## Front Commands

### Search conversations
```bash
skill front search "payment failed"                              # Text search (subject + body)
skill front search "refund" --inbox inb_4bj7r --status unassigned  # With filters
skill front search "is:unreplied" --inbox inb_4bj7r --after 1706745600
skill front search --status unassigned --inbox inb_4bj7r         # Filters only, no text
skill front search "from:dale@a.com tag:tag_14nmdp" --limit 50  # Inline Front syntax
skill front search                                                # Shows full query syntax help
```

**Filters (CLI flags):** `--inbox`, `--tag`, `--assignee`, `--status`, `--from`, `--after`, `--before`, `--limit`, `--json`

**Inline Front syntax (in the query arg):** `inbox:inb_xxx`, `tag:tag_xxx`, `from:email`, `to:email`, `cc:email`, `recipient:email`, `assignee:tea_xxx`, `participant:tea_xxx`, `author:tea_xxx`, `mention:tea_xxx`, `commenter:tea_xxx`, `is:<status>`, `before:<ts>`, `after:<ts>`, `during:<ts>`, `custom_field:"Key=Value"`

**Status values:** open, archived, assigned, unassigned, unreplied, snoozed, trashed, waiting

**Logic:** Multiple filters = AND. Multiple from/to/cc/bcc = OR. Max 15 filters.

### Get message
```bash
skill front message <id>                  # Full message details (body, author, recipients)
skill front message msg_xxx --json        # JSON output
```

### Get conversation
```bash
skill front conversation <id>             # Conversation details
skill front conversation cnv_xxx -m       # Include message history
skill front conversation <id> --json      # JSON output
```

### Inbox & conversations
```bash
skill front inbox                         # List all inboxes
skill front inbox inb_xxx                 # List conversations in inbox
skill front inbox inb_xxx --status unassigned  # Filter by status
skill front inbox "AI Hero"               # Lookup by name
skill front inbox inb_xxx --tag "500 Error" --limit 100 --json
```

### Assign / unassign conversations
```bash
skill front assign cnv_xxx tea_xxx        # Assign to teammate
skill front assign cnv_xxx --unassign     # Remove assignee
skill front assign cnv_xxx tea_xxx --json # JSON output
```

### Tag / untag conversations
```bash
skill front tag cnv_xxx "bug report"      # Add tag by name (case-insensitive)
skill front tag cnv_xxx tag_xxx           # Add tag by ID
skill front untag cnv_xxx "bug report"    # Remove tag by name
skill front untag cnv_xxx tag_xxx --json  # JSON output
```

### Reply (draft only — HITL)
```bash
skill front reply cnv_xxx --body "Thanks for reporting this"
skill front reply cnv_xxx --body "We're looking into it" --author tea_xxx
skill front reply cnv_xxx --body "..." --json
# NEVER auto-sends. Creates a draft. Review and send from Front.
```

### Tag management
```bash
skill front tags list                     # All tags with conversation counts
skill front tags list --unused            # Tags with 0 conversations
skill front tags delete tag_xxx           # Delete a tag
skill front tags rename tag_xxx "New Name"
skill front tags cleanup                  # Interactive: dedup, fix variants, remove obsolete
```

### Teammates
```bash
skill front teammates                     # List all teammates
skill front teammates --json
skill front teammate tea_xxx              # Get teammate details
skill front teammate tea_xxx --json
```

### Archive & bulk operations
```bash
skill front archive cnv_xxx               # Archive single conversation
skill front bulk-archive --inbox inb_xxx --dry-run  # Preview bulk archive
skill front bulk-archive --inbox inb_xxx --tag "spam" --execute
```

### Report & triage
```bash
skill front report --inbox inb_xxx        # Inbox forensics report
skill front triage --inbox inb_xxx        # AI-powered triage
skill front triage --inbox inb_xxx --auto-archive  # Auto-archive noise
```

### Raw API passthrough
```bash
skill front api GET /me                   # Escape hatch for any endpoint
skill front api GET /conversations/cnv_xxx
skill front api PATCH /conversations/cnv_xxx --data '{"status":"archived"}'
skill front api POST /conversations/cnv_xxx/tags --data '{"tag_ids":["tag_xxx"]}'
# Always outputs JSON. Supports GET, POST, PATCH, PUT, DELETE.
```

### Pull conversations (eval datasets)
```bash
skill front pull-conversations --inbox inb_xxx --output data.json
```

## Linear Commands

### ⚠️ Personal API Key Required for Write Operations

**All write operations (create, update, assign, close, comment, etc.) require a personal LINEAR_API_KEY.**

```bash
# Set up your personal API key
skill config init
skill config set LINEAR_API_KEY=lin_api_xxx

# Without a personal key, write commands will fail with:
# "Write operations require a personal API key for LINEAR_API_KEY."
```

### Read Operations (no personal key needed)
```bash
skill linear issues                           # List issues
skill linear issues --team ENG                # Filter by team
skill linear issues --state "In Progress"     # Filter by state
skill linear issues --assignee me             # My issues
skill linear issue ENG-123                    # Get issue details
skill linear search "bug"                     # Search issues
skill linear teams                            # List teams
skill linear users                            # List users
skill linear states ENG                       # Workflow states for team
skill linear labels ENG                       # Labels for team
skill linear projects                         # List projects
skill linear my                               # My assigned issues
```

### Write Operations (require personal API key)
```bash
skill linear create "Fix the bug" --team ENG                    # Create issue
skill linear create "Task" --team ENG --priority 1 --state "Todo"
skill linear update ENG-123 --priority 0 --estimate 3           # Update issue
skill linear assign ENG-123 --to user@example.com               # Assign
skill linear assign ENG-123 --unassign                          # Unassign
skill linear state ENG-123 --state "In Review"                  # Change state
skill linear close ENG-123                                      # Close issue
skill linear close ENG-123 --reason "Fixed in PR #42"           # Close with reason
skill linear comment ENG-123 --body "Working on this"           # Add comment
skill linear label ENG-123 --add "bug"                          # Add label
skill linear label ENG-123 --remove "feature"                   # Remove label
skill linear link ENG-123 --blocks ENG-456                      # Link issues
skill linear link ENG-123 --blocked-by ENG-456
skill linear link ENG-123 --related ENG-456
```

### JSON Output with HATEOAS
```bash
skill linear issue ENG-123 --json
# Response includes:
# - _meta.personal_key_hint: Warning about write operations
# - _actions[].requires_personal_key: true for write actions
# - _links: Related resources
```

## Other Commands

### Initialize integration
```bash
skill init                                # Interactive mode
skill init my-app                         # Quick mode with name
skill init --json                         # JSON output
```

### Setup wizard
```bash
skill wizard                              # Interactive property setup
skill wizard --json                       # JSON output
```

### Health check
```bash
skill health                              # Check default integration
skill health total-typescript             # Check by slug
skill health https://example.com -s secret  # Check by URL
skill health -l                           # List all registered apps
skill health --json                       # JSON output
```

### Run evals
```bash
skill eval routing dataset.json           # Run routing eval
skill eval routing dataset.json --json    # JSON output
skill eval routing dataset.json --min-precision 0.95
skill eval routing dataset.json --min-recall 0.98
skill eval routing dataset.json --max-fp-rate 0.02
skill eval routing dataset.json --max-fn-rate 0.01
```

## Response Analysis Commands

### List recent responses
```bash
skill responses list                          # List recent responses (default 20)
skill responses list --app total-typescript   # Filter by app
skill responses list --limit 50               # More results
skill responses list --rating bad             # Only bad-rated responses
skill responses list --rating unrated         # Only unrated responses
skill responses list --since 2024-01-01       # Since date
skill responses list --json                   # JSON output
```

### Get response details
```bash
skill responses get <actionId>                # Response details
skill responses get <actionId> --context      # Include conversation history
skill responses get <actionId> --json         # JSON output
```

### Export for analysis
```bash
skill responses export                        # Export all with context
skill responses export --app total-typescript # Filter by app
skill responses export --rating bad           # Only bad responses
skill responses export -o bad-responses.json  # Output to file
```

## Common Workflows

### Triage an inbox
```bash
# 1. Search for unassigned conversations
skill front search --inbox inb_4bj7r --status unassigned --json

# 2. Get details on a specific conversation
skill front conversation cnv_xxx -m

# 3. Assign, tag, and reply
skill front assign cnv_xxx tea_xxx
skill front tag cnv_xxx "needs-investigation"
skill front reply cnv_xxx --body "Looking into this now"

# 4. Or bulk triage with AI
skill front triage --inbox inb_4bj7r
```

### Find conversations from a specific sender
```bash
skill front search "from:user@example.com" --inbox inb_4bj7r
skill front search "from:user@example.com is:unreplied"
```

### Debug empty message body
```bash
# 1. Find recent inbound events
skill inngest events --after 1h --name "support/inbound.received"

# 2. Get event details
skill inngest event 01KFxxx

# 3. Check if message has body via Front API
skill front message msg_xxx

# 4. Compare webhook data vs API data
```

### Investigate failed workflow
```bash
# 1. Find failures
skill inngest failures --after 2h

# 2. Get run details
skill inngest run 01KFxxx

# 3. Check event that triggered it
skill inngest event <event_id>
```

### Pipe search results to other commands
```bash
# Get all unassigned conversation IDs
skill front search --inbox inb_4bj7r --status unassigned --json | jq '.data.conversations[].id'

# Archive all snoozed conversations (careful!)
skill front search "is:snoozed" --inbox inb_4bj7r --json | jq -r '.data.conversations[].id' | xargs -I{} skill front archive {}
```

## Environment Variables

Required in `.env.local`:
```bash
FRONT_API_TOKEN=           # For Front API commands
INNGEST_SIGNING_KEY=       # For Inngest API commands
```

## JSON Output

All commands support `--json` for machine-readable output:
```bash
skill inngest events --json | jq '.[0].data'
skill front message msg_xxx --json | jq '.body'
```
