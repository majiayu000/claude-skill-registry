---
name: Headless Runner
description: Run Claude Code in headless/programmatic mode for automation, CI/CD, and agent workflows. Use when user asks about headless mode, programmatic execution, scripting Claude, or automating Claude workflows.
---

# Headless Runner

Run Claude Code programmatically from scripts, CI/CD pipelines, and autonomous agent workflows. Headless mode automatically loads all project configuration (`.claude/` directory), giving you full access to skills, agents, hooks, and commands.

## Quick Start

**Most common usage:**
```bash
# Basic headless invocation (from project directory)
claude -p "Your prompt here"

# With JSON output for programmatic parsing
claude -p "Run eval baseline for v0.3.14" --output-format json

# Control tool access
claude -p "Analyze failures" --allowedTools "Bash,Read,Grep"

# Multi-turn conversation
claude -p "Start task" --output-format json > result.json
SESSION_ID=$(jq -r '.session_id' result.json)
claude --resume $SESSION_ID "Continue with next step"
```

**What gets loaded automatically:**
- ✅ `.claude/settings.json` and `.claude/settings.local.json`
- ✅ `.claude/agents/` (all project agents)
- ✅ `.claude/skills/` (all project skills)
- ✅ Hooks configured in settings
- ✅ Slash commands from `.claude/commands/`
- ✅ CLAUDE.md project instructions

## When to Use This Skill

Invoke this skill when user asks about:
- "How do I run Claude headless?"
- "Can I automate Claude workflows?"
- "How to use Claude in CI/CD?"
- "Programmatic Claude execution"
- "Script Claude commands"
- "Agent-to-agent communication"
- "Automated eval runs"
- "Scheduled Claude tasks"

## Core Commands

### Basic Invocation

```bash
# Text output (default)
claude -p "Prompt here"

# JSON output with metadata
claude -p "Prompt here" --output-format json
# Returns: {session_id, result, cost, duration, ...}

# Streaming JSON (for long-running tasks)
claude -p "Prompt here" --output-format stream-json
```

### Tool Permissions

```bash
# Allow specific tools
claude -p "Task" --allowedTools "Bash,Read,Write"

# Allow all tools (use with caution)
claude -p "Task" --allowedTools "*"

# Permission mode for edits
claude -p "Task" --permission-mode acceptEdits
```

### Multi-Turn Conversations

```bash
# Resume specific session
claude --resume SESSION_ID "Continue task"

# Continue most recent session
claude --continue "Next instruction"

# Extract session ID from JSON output
SESSION_ID=$(claude -p "Start" --output-format json | jq -r '.session_id')
claude --resume $SESSION_ID "Continue"
```

## Common Use Cases

### 1. CI/CD Integration

```bash
# .github/workflows/eval-baseline.yml
- name: Run eval baseline
  run: |
    claude -p "Use eval-orchestrator agent to run baseline for ${{ github.ref_name }}" \
      --output-format json \
      --allowedTools "Bash,Read,Write" \
      > eval_result.json

- name: Check for failures
  run: |
    FAILURES=$(jq -r '.failures' eval_result.json)
    if [ "$FAILURES" -gt 0 ]; then
      echo "::error::Eval baseline has $FAILURES failures"
      exit 1
    fi
```

### 2. Scheduled Analysis

```bash
#!/bin/bash
# cron_daily_check.sh - Run via cron daily

cd /path/to/project

# Check agent inbox
claude -p "Use agent-inbox skill to check for unread messages" \
  --output-format json > inbox.json

# If messages exist, notify
UNREAD=$(jq -r '.unreadCount' inbox.json)
if [ "$UNREAD" -gt 0 ]; then
  echo "Found $UNREAD unread agent messages"
  # Send notification, create issue, etc.
fi
```

### 3. Agent-to-Agent Workflows

```bash
#!/bin/bash
# autonomous_sprint_cycle.sh

# Agent A: Create design doc
claude -p "Use design-doc-creator to document feature X" \
  --output-format json > design.json

DESIGN_DOC=$(jq -r '.artifactPath' design.json)

# Agent B: Plan sprint from design
claude -p "Use sprint-planner to create plan from $DESIGN_DOC" \
  --output-format json > plan.json

PLAN_FILE=$(jq -r '.planPath' plan.json)

# Agent C: Execute sprint
claude -p "Use sprint-executor to execute $PLAN_FILE" \
  --output-format json > execution.json
```

### 4. Automated Testing

```bash
#!/bin/bash
# test_agent_quality.sh

# Run eval with specific model
claude -p "Use eval-orchestrator: run suite with gpt5-mini only" \
  --output-format json > results.json

# Parse results
SUCCESS_RATE=$(jq -r '.successRate' results.json)

# Assert quality threshold
if (( $(echo "$SUCCESS_RATE < 0.75" | bc -l) )); then
  echo "Agent quality below threshold: $SUCCESS_RATE"
  exit 1
fi
```

## Available Scripts

### `scripts/test_headless.sh`
Test headless mode works correctly with project configuration.

**Usage:**
```bash
.claude/skills/headless-runner/scripts/test_headless.sh
```

**What it tests:**
- ✓ `claude` command is available
- ✓ Project configuration loads (.claude/ directory)
- ✓ Skills are accessible
- ✓ Agents are accessible
- ✓ JSON output parses correctly
- ✓ Multi-turn sessions work

### `scripts/run_with_retry.sh <prompt> [max_retries]`
Run headless command with automatic retry on failure.

**Usage:**
```bash
.claude/skills/headless-runner/scripts/run_with_retry.sh "Run eval baseline" 3
```

**Features:**
- Retries on transient failures
- Exponential backoff
- JSON output preserved
- Exit codes: 0 (success), 1 (permanent failure), 2 (retries exhausted)

## Workflow Patterns

### Pattern 1: Single Command

**Use for:** Simple, one-off tasks

```bash
claude -p "Generate changelog from git log since v0.3.13"
```

### Pattern 2: Sequential Pipeline

**Use for:** Multi-step workflows where each step depends on previous

```bash
#!/bin/bash
set -euo pipefail

# Step 1
claude -p "Step 1" --output-format json > step1.json
ARTIFACT1=$(jq -r '.artifact' step1.json)

# Step 2 (uses Step 1 output)
claude -p "Step 2 using $ARTIFACT1" --output-format json > step2.json
ARTIFACT2=$(jq -r '.artifact' step2.json)

# Step 3
claude -p "Step 3 using $ARTIFACT2"
```

### Pattern 3: Conversation Session

**Use for:** Multi-turn tasks that need context

```bash
#!/bin/bash

# Start conversation
RESULT=$(claude -p "Analyze codebase for tech debt" --output-format json)
SESSION_ID=$(echo "$RESULT" | jq -r '.session_id')

# Continue conversation with context
claude --resume $SESSION_ID "Focus on files over 800 lines"
claude --resume $SESSION_ID "Generate refactoring plan"
claude --resume $SESSION_ID "Estimate effort for top 3 items"
```

### Pattern 4: Parallel Execution

**Use for:** Independent tasks that can run concurrently

```bash
#!/bin/bash

# Start multiple tasks in parallel
claude -p "Task A" --output-format json > taskA.json &
PID_A=$!

claude -p "Task B" --output-format json > taskB.json &
PID_B=$!

claude -p "Task C" --output-format json > taskC.json &
PID_C=$!

# Wait for all to complete
wait $PID_A $PID_B $PID_C

# Aggregate results
jq -s '{taskA: .[0], taskB: .[1], taskC: .[2]}' taskA.json taskB.json taskC.json
```

## Quick Tips

**Output formats:**
- `--output-format text` (default) - Human-readable
- `--output-format json` - For automation (includes session_id, status, cost)
- `--output-format stream-json` - For real-time progress

**Configuration:**
- Runs from project directory → auto-loads `.claude/` config
- No special flags needed for skills/agents/commands

**Error handling:**
- Always check exit codes: `if ! claude -p "..." ; then ...`
- Validate JSON: `echo "$RESULT" | jq -e '.status == "success"'`
- Use retry with backoff (see `run_with_retry.sh` script)

**Tool permissions:**
- Analysis: `--allowedTools "Read,Grep,Glob"`
- Testing: `--allowedTools "Bash,Read"`
- Development: `--allowedTools "Bash,Read,Write,Edit"`

For complete details, see [CLI Reference](resources/cli_reference.md) and [Troubleshooting](resources/troubleshooting.md).

## AILANG Agent Integration

**Build autonomous agents using headless Claude + AILANG messaging:**

For complete autonomous agent patterns (task claiming, handoffs, error handling), see:
- [`resources/agent_workflows.md`](resources/agent_workflows.md) - Autonomous agent patterns with messaging
- [agent-inbox skill](../agent-inbox/SKILL.md) - Inbox management and message format reference

**Quick example:**
```bash
# Agent checks inbox for tasks
MESSAGES=$(ailang agent inbox --unread-only my-agent)
MESSAGE_ID=$(echo "$MESSAGES" | grep "ID:" | head -1 | awk '{print $2}')

# Claim task
ailang agent ack $MESSAGE_ID

# Process with headless Claude
RESULT=$(claude -p "Process task from inbox" --output-format json)

# On success: keep ack, send result
if [ "$(echo "$RESULT" | jq -r '.status')" = "success" ]; then
  ailang agent send --to-user --from "my-agent" '{"status": "complete"}'
else
  # On failure: return to queue
  ailang agent unack $MESSAGE_ID
fi
```

## Resources

### Agent Workflows (NEW!)
See [`resources/agent_workflows.md`](resources/agent_workflows.md) for autonomous agent patterns with AILANG messaging system.

### CLI Reference
See [`resources/cli_reference.md`](resources/cli_reference.md) for complete CLI flag documentation.

### Examples
See [`resources/examples.md`](resources/examples.md) for comprehensive workflow examples.

### Troubleshooting
See [`resources/troubleshooting.md`](resources/troubleshooting.md) for common issues and solutions.

## Progressive Disclosure

This skill loads information progressively:

1. **Always loaded**: This SKILL.md file (YAML frontmatter + core workflows)
2. **Execute as needed**: Scripts in `scripts/` directory
3. **Load on demand**: `resources/` (detailed CLI reference, examples, troubleshooting)

## Notes

- **Requires**: Claude Code CLI installed and in PATH
- **Context window**: Be mindful of token limits for large prompts
- **Costs**: Track with `--output-format json` → `.cost` field
- **Concurrency**: Multiple headless sessions can run in parallel
- **State**: Each invocation is stateless unless using `--resume`
