---
name: execution-tracking
description: Execution status management and reporting for implementation plugin. Use when initializing execution tracking, updating task status, generating progress reports, calculating completion metrics, tracking layer execution, monitoring feature implementation progress, or when user mentions execution status, progress tracking, or implementation monitoring.
allowed-tools: Bash, Read, Write, Edit, Glob
---

# Execution Tracking

Status file management and progress reporting for the implementation plugin.

## Overview

This skill provides comprehensive execution tracking capabilities including status file initialization, task completion tracking, progress calculation, report generation, and metrics aggregation. Manages execution state in `.claude/execution/` directory with JSON-based status files.

## When to Use This Skill

Use this skill when:
- Initializing execution tracking for a feature implementation
- Updating task completion status during execution
- Generating progress reports showing current state
- Calculating completion metrics and percentages
- Tracking layer-by-layer execution progress
- Monitoring overall feature implementation status
- Identifying next actions and pending tasks
- Logging execution errors and warnings

## Core Capabilities

### 1. Initialize Execution Tracking

**Script:** `scripts/update-status.sh init <spec-id>`

Creates new execution status file from layered tasks specification.

**What it does:**
- Reads `specs/<spec>/layered-tasks.md` to extract task structure
- Creates `.claude/execution/<spec>.json` status file
- Initializes all layers with "pending" status
- Sets up task tracking for each layer
- Calculates total task count

**Example:**
```bash
bash scripts/update-status.sh init F001
# Creates: .claude/execution/F001.json
```

### 2. Update Task Status

**Script:** `scripts/update-status.sh update <spec> <layer> <task-index> <status>`

Updates individual task completion status.

**Supported statuses:**
- `complete` - Task successfully completed
- `failed` - Task execution failed
- `skipped` - Task skipped (dependency issue)
- `in_progress` - Task currently executing

**What it does:**
- Updates task status and timestamp
- Records execution duration (if complete)
- Recalculates layer metrics
- Recalculates overall progress
- Updates `last_updated` timestamp

**Example:**
```bash
bash scripts/update-status.sh update F001 L1 2 complete
# Marks third task in L1 as complete
```

### 3. Mark Layer Complete

**Script:** `scripts/update-status.sh complete-layer <spec> <layer>`

Marks entire layer as complete and advances to next layer.

**What it does:**
- Verifies all layer tasks are complete
- Sets layer status to "complete"
- Records layer completion timestamp
- Advances `current_layer` to next layer
- Recalculates overall metrics

**Example:**
```bash
bash scripts/update-status.sh complete-layer F001 L0
# Marks L0 complete, advances to L1
```

### 4. Log Execution Error

**Script:** `scripts/update-status.sh error <spec> <layer> <task-index> <error-message>`

Logs execution errors for troubleshooting.

**What it does:**
- Adds error to errors array
- Records layer, task, and timestamp
- Categorizes error severity
- Updates task status to "failed"
- Generates error report

**Example:**
```bash
bash scripts/update-status.sh error F001 L1 3 "API endpoint creation failed: invalid path syntax"
```

### 5. Generate Progress Report

**Script:** `scripts/update-status.sh report <spec>`

Creates comprehensive progress report from status file.

**Report includes:**
- Overall progress percentage
- Layer-by-layer status breakdown
- Current executing task
- Next pending tasks
- Recent errors (if any)
- Estimated time remaining
- Next recommended action

**Output:**
```
Feature F001: AI Chat Interface
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Progress: 38% (5/13 tasks)
Time Elapsed: 30 minutes
Estimated Remaining: 49 minutes

Layer 0 (Infrastructure):  ✅ Complete (2/2 tasks)
Layer 1 (Core Services):   🔄 In Progress (3/5 tasks)
Layer 2 (Features):        ⏳ Pending (0/4 tasks)
Layer 3 (Integration):     ⏳ Pending (0/2 tasks)

Currently Executing:
- Create message API endpoint (fastapi-agent, medium) - Started 5m ago

Next 3 Pending Tasks:
1. [L1] Implement chat storage (supabase-agent, easy)
2. [L1] Add user authentication (auth-agent, medium)
3. [L2] Build chat UI component (react-agent, hard)

Errors: 0

Next Action: Continue L1 execution with /implementation:execute F001 --layer=L1
```

## Status File Schema

### Location
`.claude/execution/<spec>.json` (e.g., `.claude/execution/F001.json`)

### Complete Schema
```json
{
  "feature": "F001",
  "feature_name": "AI Chat Interface",
  "started_at": "2025-11-17T12:00:00Z",
  "last_updated": "2025-11-17T12:30:00Z",
  "status": "in_progress",
  "current_layer": "L1",
  "total_tasks": 13,
  "completed_tasks": 5,
  "failed_tasks": 0,
  "skipped_tasks": 0,
  "completion_percentage": 38,
  "average_task_duration_ms": 1450,
  "estimated_remaining_ms": 11600,
  "layers": {
    "L0": {
      "name": "Infrastructure",
      "status": "complete",
      "total_tasks": 2,
      "completed_tasks": 2,
      "failed_tasks": 0,
      "started_at": "2025-11-17T12:00:00Z",
      "completed_at": "2025-11-17T12:10:00Z",
      "duration_ms": 600000,
      "tasks": [
        {
          "index": 0,
          "description": "Setup database schema",
          "command": "/supabase:create-schema chat",
          "agent": "supabase-agent",
          "complexity": "easy",
          "status": "complete",
          "started_at": "2025-11-17T12:00:00Z",
          "completed_at": "2025-11-17T12:05:00Z",
          "duration_ms": 300000,
          "output": "Created schema successfully",
          "files_created": ["supabase/migrations/001_chat_schema.sql"]
        },
        {
          "index": 1,
          "description": "Initialize API structure",
          "command": "/fastapi-backend:init api",
          "agent": "fastapi-agent",
          "complexity": "easy",
          "status": "complete",
          "started_at": "2025-11-17T12:05:00Z",
          "completed_at": "2025-11-17T12:10:00Z",
          "duration_ms": 300000,
          "output": "API structure initialized",
          "files_created": ["backend/app/main.py", "backend/app/routers/__init__.py"]
        }
      ]
    },
    "L1": {
      "name": "Core Services",
      "status": "in_progress",
      "total_tasks": 5,
      "completed_tasks": 3,
      "failed_tasks": 0,
      "started_at": "2025-11-17T12:10:00Z",
      "tasks": [...]
    },
    "L2": {
      "name": "Features",
      "status": "pending",
      "total_tasks": 4,
      "completed_tasks": 0,
      "failed_tasks": 0,
      "tasks": [...]
    },
    "L3": {
      "name": "Integration",
      "status": "pending",
      "total_tasks": 2,
      "completed_tasks": 0,
      "failed_tasks": 0,
      "tasks": [...]
    }
  },
  "errors": [],
  "warnings": [],
  "next_action": "Continue L1: 2 tasks remaining"
}
```

## Metrics Calculation Formulas

### Overall Progress
```
completion_percentage = (completed_tasks / total_tasks) * 100
```

### Layer Progress
```
layer_percentage = (layer.completed_tasks / layer.total_tasks) * 100
```

### Average Task Duration
```
avg_task_duration = sum(all_completed_task_durations) / completed_tasks
```

### Estimated Time Remaining
```
remaining_tasks = total_tasks - completed_tasks
estimated_remaining = avg_task_duration * remaining_tasks
```

### Success Rate
```
attempted_tasks = completed_tasks + failed_tasks + skipped_tasks
success_rate = (completed_tasks / attempted_tasks) * 100
```

### Layer Duration
```
layer_duration = layer.completed_at - layer.started_at
```

## Status Indicators

### Layer Status Icons
- ✅ **Complete** - 100% tasks complete, layer finished
- 🔄 **In Progress** - 1-99% tasks complete, actively working
- ⏳ **Pending** - 0% complete, not yet started
- ❌ **Failed** - Has failed tasks, execution blocked

### Overall Status Values
- `pending` - Not started (0% complete)
- `in_progress` - Some tasks complete (1-99%)
- `paused` - Execution paused (manual intervention needed)
- `complete` - All tasks done (100% complete)
- `failed` - Critical error, cannot continue

### Task Status Values
- `pending` - Not yet started
- `in_progress` - Currently executing
- `complete` - Successfully finished
- `failed` - Execution failed
- `skipped` - Skipped due to dependency

## Usage Patterns

### From /implementation:execute Command
```bash
# Initialize tracking
bash scripts/update-status.sh init F001

# Update tasks as they complete
bash scripts/update-status.sh update F001 L0 0 complete
bash scripts/update-status.sh update F001 L0 1 complete

# Mark layer complete
bash scripts/update-status.sh complete-layer F001 L0

# Generate report
bash scripts/update-status.sh report F001
```

### From progress-tracker Agent
```bash
# Agent reads status file
status=$(cat .claude/execution/F001.json)

# Agent updates task status
bash scripts/update-status.sh update F001 L1 2 complete

# Agent generates report for user
bash scripts/update-status.sh report F001
```

### Error Handling
```bash
# Log error when task fails
bash scripts/update-status.sh error F001 L1 3 "Database connection timeout"

# Check error count before continuing
error_count=$(jq '.errors | length' .claude/execution/F001.json)
if [ "$error_count" -gt 5 ]; then
  echo "Too many errors, pausing execution"
  bash scripts/update-status.sh pause F001
fi
```

## Templates

See `templates/` directory for:
- **execution-status.json** - Complete status file template with all fields
- **status-report.md** - Progress report template for formatting
- **error-log.json** - Error entry template with severity levels

## Examples

See `examples/` directory for:
- **status-examples.md** - Example status files at different execution stages
- **workflow-integration.md** - How to integrate tracking into execution workflow
- **error-scenarios.md** - Common error scenarios and recovery patterns

## Best Practices

1. **Initialize before execution** - Always create status file before starting implementation
2. **Update after each task** - Keep status current by updating immediately after task completion
3. **Log all errors** - Record errors for debugging and troubleshooting
4. **Generate reports regularly** - Create reports to show progress to users
5. **Calculate metrics accurately** - Use formulas consistently for accurate percentages
6. **Handle edge cases** - Account for skipped tasks, failed tasks, and paused execution
7. **Preserve history** - Don't delete status files, archive them after completion
8. **Use timestamps consistently** - All timestamps in ISO 8601 UTC format

## Integration Points

**Used by:**
- `/implementation:execute` command - Main execution orchestrator
- `progress-tracker` agent - Real-time progress monitoring
- `error-handler` agent - Error logging and recovery
- `/implementation:status` command - Status reporting

**Depends on:**
- `layered-tasks.md` - Source of task definitions
- `features.json` - Feature metadata
- Bash shell - Script execution environment

---

**Location:** `plugins/implementation/skills/execution-tracking/`
**Purpose:** Comprehensive execution status management
**Complexity:** Medium - Requires JSON manipulation and metric calculation
