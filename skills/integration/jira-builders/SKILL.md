---
name: jira-builders
description: |
  Guide for using jira-tool CLI correctly to create and manage Jira tickets with rich formatting.
  Use when working with Jira tickets, epics, or exports. Triggers on "create Jira ticket",
  "search Jira", "get Jira ticket", "export Jira data", "list epics", or any Jira API operations.
  Prevents common mistakes like trying to import jira_tool Python module or using curl unnecessarily.
  Works with jira-tool CLI command and environment variables (JIRA_BASE_URL, JIRA_USERNAME, JIRA_API_TOKEN).
---

# Jira Ticket Management

Use `jira-tool` CLI for all Jira operations.

## Core Commands

```bash
# Get ticket
jira-tool get WPCW-370

# Search
jira-tool search 'project=WPCW AND status="To Do"'

# List epics
jira-tool epics --project WPCW

# Create epic
jira-tool create --project WPCW --type Epic --summary "Title"

# Create story under epic
jira-tool create --project WPCW --type Story --summary "Title" --parent WPCW-370

# Create subtask
jira-tool create --project WPCW --type Sub-task --summary "Title" --parent WPCW-371

# Export for analysis
jira-tool export --project WPCW --all --format jsonl -o data.jsonl
```

## Rich Descriptions

Use heredoc for multi-line descriptions:

```bash
jira-tool create --project WPCW --type Epic \
  --summary "User Authentication" \
  --description "$(cat <<'EOF'
Implement OAuth2 authentication with session management.

**Problem Statement:**
Users cannot securely log in.

**Acceptance Criteria:**
- User can log in with email/password
- Session persists across refresh
- Logout invalidates sessions
EOF
)"
```

## Batch Operations

Shell scripts with jira-tool:

```bash
#!/bin/bash
EPIC=$(jira-tool create --project WPCW --type Epic \
  --summary "Parent Epic" --format json | jq -r '.key')

for task in "Task 1" "Task 2" "Task 3"; do
  jira-tool create --project WPCW --type Story \
    --summary "$task" --parent "$EPIC"
done
```

## Data Processing

Export and process with shell tools:

```bash
# Export tickets
jira-tool export --project WPCW --all --format jsonl -o tickets.jsonl

# Process with jq
jq -r 'select(.fields.status.name == "To Do") | .key' tickets.jsonl
```

## When to Use What

- **Single operation:** `jira-tool` directly
- **Batch operations:** Shell scripts with `jira-tool` in loops
- **Complex workflows:** Invoke `jira-ticket-manager` agent
- **Data analysis:** Export + process with jq/awk

## Requirements

- `jira-tool` CLI installed (check with `jira-tool --version`)
- Environment: `JIRA_BASE_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`

## Critical Anti-Patterns to Avoid

**DO NOT:**
1. Import jira_tool Python module - it's internal/private
   ```python
   # WRONG - This will fail
   from jira_tool import JiraClient
   ```

2. Use curl for Jira API unless jira-tool doesn't support the operation
   ```bash
   # WRONG - Fragile, error-prone
   curl -u "$JIRA_USERNAME:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/search"
   ```

3. Create multiple scripts for same purpose (violates DRY principle)
   ```bash
   # WRONG - Multiple scripts for slight variations
   pull_tickets_basic.py, pull_tickets_filtered.py, pull_tickets_csv.py
   ```

**DO:**
1. Use jira-tool CLI for all operations
   ```bash
   # RIGHT - Use the CLI
   jira-tool search 'project=WPCW'
   ```

2. Use subprocess if you need programmatic access
   ```python
   # RIGHT - Call CLI from Python
   import subprocess
   result = subprocess.run(['jira-tool', 'get', 'PROJ-123'],
                          capture_output=True, text=True)
   ```

3. Use command-line flags for variations
   ```bash
   # RIGHT - One script with options
   jira-tool export --format csv --filter status=Open -o file.csv
   ```

## Supporting References

- **Quick Reference:** `~/.claude/skills/jira-builders/references/QUICK_REFERENCE.md` - Common CLI patterns and examples
- **Tool Selection:** `~/.claude/skills/jira-builders/references/TOOL_SELECTION.md` - When to use CLI vs agent vs curl
