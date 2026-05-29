---
name: skill-cli
description: CLI for Skill Recordings Support Agent platform. Use when investigating support issues, debugging workflows, inspecting Front/Inngest data, or managing app integrations.
allowed-tools: Bash(skill:*)
---

# Skill Recordings Support Agent CLI

CLI tool for the Skill Recordings support platform. Named `skill` after Skill Recordings (the company), not Claude skills.

## Quick start

```bash
skill inngest events --after 1h     # Recent events
skill inngest event <id>            # Event details + runs
skill front message <id>            # Full message with body
skill front conversation <id> -m    # Conversation with history
skill skills list                   # Available skills
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

### Get message
```bash
skill front message <id>                  # Full message details
skill front message msg_xxx --json        # JSON output

# Output includes:
# - ID, type, subject, created timestamp
# - Author email
# - Recipients (from, to, cc, bcc)
# - Body (HTML length, text length, preview)
# - Attachments
```

### Get conversation
```bash
skill front conversation <id>             # Conversation details
skill front conversation cnv_xxx -m       # Include message history
skill front conversation <id> --json      # JSON output

# Output includes:
# - ID, subject, status, created timestamp
# - Recipient, assignee
# - Tags
# - Message history (with -m flag)
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
# 1. Find function.finished events
skill inngest events --after 2h | grep function.finished

# 2. Get run details
skill inngest run 01KFxxx

# 3. Check event that triggered it
skill inngest event <event_id>
```

### Check conversation context
```bash
# Get full conversation with message history
skill front conversation cnv_xxx -m

# Or just the conversation metadata
skill front conversation cnv_xxx
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
