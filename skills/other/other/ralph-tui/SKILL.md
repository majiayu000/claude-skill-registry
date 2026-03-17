---
name: ralph-tui
description: Run ralph-tui task loops for automated PRD execution. Covers headless mode, PRD preparation, agent selection (opencode/claude), session management, and troubleshooting. Use when asked to "run ralph-tui", "execute PRD tasks", or "start a ralph session".
---

# Ralph-TUI Agent Execution Guide

> A practical guide for AI agents running ralph-tui task loops

## Quick Start

```bash
cd /path/to/project

# Run ralph-tui (both agents work reliably)
ralph-tui run --prd ./prd.json --agent opencode --headless --iterations 20
# or
ralph-tui run --prd ./prd.json --agent claude --headless --iterations 20

# Monitor progress
ralph-tui status --json | jq '{status, progress: .session.progress}'
```

## Agent Selection

**Both agents work reliably** when sessions are properly managed.

| Agent | Speed | Notes |
|-------|-------|-------|
| `opencode` | ~5-10s/task | Lightweight, fast |
| `claude` | ~20-30s/task | More verbose output, thorough |

```bash
# OpenCode
ralph-tui run --prd ./prd.json --agent opencode --headless

# Claude  
ralph-tui run --prd ./prd.json --agent claude --headless
```

---

## Prerequisites

1. **ralph-tui installed**: `which ralph-tui`
2. **Agent CLI installed**: `opencode` or `claude`
3. **PRD file**: JSON format with user stories

---

## Preparing a PRD

### Option 1: Create PRD Interactively

```bash
ralph-tui create-prd
# or with AI chat assistance:
ralph-tui create-prd --chat
```

### Option 2: Convert Markdown to JSON

```bash
ralph-tui convert --to json ./prd.md --output ./prd.json
```

### Option 3: Manual JSON Structure

Create a `prd.json` file:

```json
{
  "name": "Project Name",
  "description": "What this PRD accomplishes",
  "branchName": "main",
  "userStories": [
    {
      "id": "US-001",
      "title": "Short task title",
      "description": "Detailed description of what to implement",
      "acceptanceCriteria": [
        "Specific verifiable criterion 1",
        "Specific verifiable criterion 2",
        "Build succeeds with no new warnings"
      ],
      "priority": 1,
      "passes": false,
      "labels": [],
      "dependsOn": []
    },
    {
      "id": "US-002",
      "title": "Second task",
      "description": "Description",
      "acceptanceCriteria": ["Criteria"],
      "priority": 2,
      "passes": false,
      "labels": [],
      "dependsOn": ["US-001"]
    }
  ]
}
```

### Key PRD Fields

| Field | Purpose |
|-------|---------|
| `id` | Unique identifier (US-001, US-002, etc.) |
| `title` | Short task name shown in TUI |
| `description` | Full task description for the agent |
| `acceptanceCriteria` | Array of verifiable requirements |
| `priority` | Execution order (1 = highest) |
| `passes` | `false` = pending, `true` = completed |
| `dependsOn` | Array of task IDs that must complete first |

---

## The `.ralph-tui/` Directory

**Important**: This directory contains valuable session history. Never delete it carelessly.

| File/Dir | Purpose | Persists? |
|----------|---------|-----------|
| `config.toml` | Project configuration | ✅ Yes |
| `progress.md` | Human-readable progress log | ✅ Yes |
| `iterations/` | Per-iteration agent logs | ✅ Yes |
| `session.json` | Active session state | ❌ Removed on completion |
| `ralph.lock` | Prevents concurrent runs | ❌ Removed on completion |

---

## Running Ralph-TUI

### Standard Execution

```bash
cd /path/to/project

# Ensure config exists
mkdir -p .ralph-tui
cat > .ralph-tui/config.toml << 'EOF'
agent = "opencode"
tracker = "json"
EOF

# Run
ralph-tui run --prd ./prd.json --headless --iterations 20 > /tmp/ralph.log 2>&1 &
echo "PID: $!"
```

### Check Status

```bash
ralph-tui status --json | jq '{status, progress: .session.progress}'
```

### Resume Interrupted Session

```bash
ralph-tui resume --headless
```

---

## Session Management

### Starting Fresh (Preserving History)

**Never use `rm -rf .ralph-tui/`** - this destroys valuable iteration logs and progress history.

Instead, archive the old session:

```bash
# Archive old session before starting fresh
if [ -d .ralph-tui ]; then
  ARCHIVE_NAME=".ralph-tui-archive-$(date +%Y%m%d-%H%M%S)"
  mv .ralph-tui "$ARCHIVE_NAME"
  echo "Archived to $ARCHIVE_NAME"
fi

# Create fresh config
mkdir -p .ralph-tui
cat > .ralph-tui/config.toml << 'EOF'
agent = "opencode"
tracker = "json"
EOF

# Start new session
ralph-tui run --prd ./prd.json --headless --iterations 20
```

### Clearing Only Session State (Keep Config & History)

If you just need to reset session state but keep config and logs:

```bash
# Remove only session state, keep config and history
rm -f .ralph-tui/ralph.lock .ralph-tui/session.json

# Resume or start fresh
ralph-tui run --prd ./prd.json --headless
```

### Stuck Session Recovery

```bash
# 1. Check what's blocking
ralph-tui status --json

# 2. Remove lock if stale
rm -f .ralph-tui/ralph.lock

# 3. Reset session to paused (preserves progress tracking)
if [ -f .ralph-tui/session.json ]; then
  cat .ralph-tui/session.json | jq '.status = "paused"' > /tmp/s.json
  mv /tmp/s.json .ralph-tui/session.json
fi

# 4. Resume
ralph-tui resume --headless
```

---

## Troubleshooting

### Problem: "Invalid session file"

**Solution**: Remove only the session file, not the entire directory:

```bash
rm -f .ralph-tui/session.json
ralph-tui run --prd ./prd.json --headless
```

### Problem: Session Stuck / Agent at 0% CPU

**Diagnosis**:
```bash
# Check agent process
ps aux | grep -E "claude|opencode" | grep -v grep

# Check ralph-tui status
ralph-tui status --json
```

**Solution**:
```bash
# Kill stuck processes
pkill -f "ralph-tui run"

# Remove lock, reset session
rm -f .ralph-tui/ralph.lock
cat .ralph-tui/session.json | jq '.status = "paused"' > /tmp/s.json && mv /tmp/s.json .ralph-tui/session.json

# Resume
ralph-tui resume --headless
```

### Problem: Setup Wizard Blocks Headless Mode

**Cause**: No config.toml exists.

**Solution**: Create config before running:
```bash
mkdir -p .ralph-tui
cat > .ralph-tui/config.toml << 'EOF'
agent = "opencode"
tracker = "json"
EOF
```

### Problem: Config Validation Warnings

**Note**: Warnings like "Invalid input: expected string, received object" are often non-fatal. Check if tasks are completing:

```bash
tail /tmp/ralph.log | grep "COMPLETED"
```

---

## Running Multiple PRDs Sequentially

```bash
#!/bin/bash
# run-all-prds.sh

PROJECT_DIR=~/dev/my-project
PRDS=(
  "./prd.json"
  "./tasks/prd-phase2.json"
  "./tasks/prd-phase3.json"
)

for prd in "${PRDS[@]}"; do
  echo "=== Running $prd ==="
  cd "$PROJECT_DIR"
  
  # Archive previous session if exists
  if [ -f .ralph-tui/session.json ]; then
    ARCHIVE=".ralph-tui-$(basename $prd .json)-$(date +%H%M%S)"
    cp -r .ralph-tui "$ARCHIVE"
    rm -f .ralph-tui/session.json .ralph-tui/ralph.lock
  fi
  
  # Run this PRD
  ralph-tui run --prd "$prd" --headless --iterations 20 > "/tmp/ralph-$(basename $prd .json).log" 2>&1
  
  echo "Completed: $prd"
done

echo "All PRDs completed!"
```

---

## Verifying Completion

```bash
# Check all tasks passed
cat prd.json | jq '[.userStories[] | .passes] | all'
# Should return: true

# Count passed vs pending
cat prd.json | jq '[.userStories[] | .passes] | group_by(.) | map({passes: .[0], count: length})'

# List any incomplete tasks
cat prd.json | jq '.userStories[] | select(.passes == false) | {id, title}'
```

---

## Best Practices

1. **Create config.toml** before running headless
2. **Archive, don't delete** `.ralph-tui/` - history is valuable
3. **Set reasonable `--iterations`** - 20 is good default
4. **Log to file** - `> /tmp/ralph.log 2>&1`
5. **Monitor with status** - `ralph-tui status --json`
6. **Include "Build succeeds"** in acceptance criteria

---

## Command Reference

| Command | Purpose |
|---------|---------|
| `ralph-tui run --prd <file>` | Start new session |
| `ralph-tui resume` | Resume interrupted session |
| `ralph-tui status --json` | Check session status |
| `ralph-tui logs` | View iteration logs |
| `ralph-tui plugins agents` | List available agents |
| `ralph-tui create-prd` | Create PRD interactively |
| `ralph-tui convert --to json` | Convert MD to JSON |

### Common Flags

| Flag | Purpose |
|------|---------|
| `--headless` | Run without TUI |
| `--agent <name>` | Agent: `opencode` or `claude` |
| `--iterations <n>` | Max iterations (0 = unlimited) |
| `--prd <path>` | PRD file path |

---

## Example Session

```bash
# 1. Prepare project
cd ~/dev/my-project

# 2. Ensure config exists
mkdir -p .ralph-tui
echo 'agent = "opencode"' > .ralph-tui/config.toml
echo 'tracker = "json"' >> .ralph-tui/config.toml

# 3. Archive any existing session
if [ -f .ralph-tui/session.json ]; then
  mv .ralph-tui/session.json ".ralph-tui/session-$(date +%H%M%S).json.bak"
fi

# 4. Start ralph-tui
ralph-tui run --prd ./prd.json --headless --iterations 20 > /tmp/ralph.log 2>&1 &
echo "Started with PID: $!"

# 5. Monitor progress
watch -n 5 'ralph-tui status --json | jq "{status, progress: .session.progress}"'

# 6. Verify completion
cat prd.json | jq '[.userStories[] | .passes] | all'
```

---

*Last updated: 2026-01-15*
*Tested with: ralph-tui v0.1.5, opencode v1.1.6, claude v2.1.7*
*Both agents verified working*
