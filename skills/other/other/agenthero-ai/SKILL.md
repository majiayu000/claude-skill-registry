---
name: agenthero-ai
description: AgentHero AI - Hierarchical multi-agent orchestration system with PM coordination, file-based state management, and interactive menu interface. Use when managing complex multi-agent workflows, coordinating parallel sub-agents, or organizing large project tasks with multiple specialists. All created agents use aghero- prefix.
version: 2.0.0
---

# AgentHero AI Skill (V2.0)

Comprehensive orchestration utilities for managing hierarchical multi-agent systems with PM coordination, state management, and topic-based organization.

## Overview

This skill provides Python-based utilities for:
- **State Management**: Create, read, update state files for orchestration (V2.0)
- **Topic Lifecycle**: Initialize, resume, archive project topics
- **Task Coordination**: Manage sub-agent tasks and dependencies
- **Token Tracking**: Monitor and report token usage across agents
- **SessionStart Hook**: Display active topics on Claude Code startup

## When Claude Should Use This Skill

Auto-activate when:
- PM orchestrator needs to manage state files
- Creating or updating topic metadata
- Initializing sub-agent task states
- Archiving completed topics
- Reading orchestration state for resume

## Directory Structure (V2.0)

```
.claude/
├── agents/
│   ├── agenthero-ai/                    # PM agent
│   │   ├── agent.md
│   │   └── orchestrated-sub-agent-template.md
│   └── state/                            # Runtime state
│       └── agenthero-ai/                # V2.0 namespace
│           ├── topics.json               # ✅ Single source of truth
│           ├── topics/                   # Topic directories
│           │   └── {topic-slug}/
│           │       ├── task-{id}-{name}.json
│           │       └── messages.json
│           └── archive/                  # Completed topics
│
└── skills/
    └── agenthero-ai/
        ├── skill.md                      # This file
        ├── scripts/                      # Python utilities (V2.0)
        │   ├── topic_manager.py          # Topic lifecycle
        │   ├── state_manager.py          # State CRUD operations
        │   ├── utils.py                  # Shared utilities
        │   ├── setup_project_structure.py # Directory setup
        │   ├── finalize_topic.py         # Topic completion
        │   ├── check_topics_file.py      # Validation
        │   └── get_topics_quiet.sh       # SessionStart hook
        └── templates/
            └── state-templates.json      # State file schemas
```

## Python Utilities (V2.0)

### 1. Topic Manager (`scripts/topic_manager.py`)

**Purpose**: Manage topic lifecycle (V2.0 - uses topics.json)

**Commands**:
- `create_topic <title>` - Initialize new topic in topics.json
- `list_active_topics` - List non-completed topics
- `list_completed_topics` - List completed topics
- `get_topic_status <slug>` - Get topic progress and metrics
- `touch_topic <slug>` - Update last active time
- `update_topic_progress <slug>` - Recalculate progress from tasks
- `archive_topic <slug>` - Move topic to archive directory
- `resume_topic <slug>` - Update last active and return status
- `get_active_topics_summary` - Get summary for SessionStart hook
- `complete_topic <slug>` - Mark as completed and archive
- `delete_topic <slug>` - Delete topic (use with caution)

**Usage Examples**:
```bash
# Create new topic (V2.0)
python .claude/skills/agenthero-ai/scripts/topic_manager.py \
  create_topic \
  "Add JWT authentication" \
  --description "Implement JWT-based auth with tokens and middleware"

# List active topics
python .claude/skills/agenthero-ai/scripts/topic_manager.py \
  list_active_topics

# Get topic status (reads from topics.json)
python .claude/skills/agenthero-ai/scripts/topic_manager.py \
  get_topic_status \
  "auth-system-jwt"

# Archive completed topic
python .claude/skills/agenthero-ai/scripts/topic_manager.py \
  archive_topic \
  "auth-system-jwt"

# Get active topics summary (SessionStart hook)
python .claude/skills/agenthero-ai/scripts/topic_manager.py \
  get_active_topics_summary
```

### 2. State Manager (`scripts/state_manager.py`)

**Purpose**: CRUD operations for state files (V2.0)

**Commands**:
- `create_state_file <path> <template>` - Initialize state file from template
- `read_state <path> <field>` - Read specific field from state
- `update_state <path> <field> <value>` - Update state field
- `append_log <path> <level> <message>` - Append log entry
- `set_task_status <path> <status>` - Update task status
- `track_file_change <path> <file> <change_type>` - Track file change
- `update_progress <path> <progress>` - Update progress (0-100)
- `validate_state <path>` - Validate JSON structure
- `set_blocking_question <path> <question>` - Set blocking question
- `answer_question <path> <answer>` - Answer blocking question
- `set_task_result <path> <result>` - Set task completion result

**Usage Examples**:
```bash
# Create new task state
python .claude/skills/agenthero-ai/scripts/state_manager.py \
  create_state_file \
  ".claude/agents/state/agenthero-ai/topics/auth-system/task-001-backend.json" \
  "task-state"

# Append log entry
python .claude/skills/agenthero-ai/scripts/state_manager.py \
  append_log \
  ".claude/agents/state/agenthero-ai/topics/auth-system/task-001-backend.json" \
  "info" \
  "Starting database schema design"

# Read current status
python .claude/skills/agenthero-ai/scripts/state_manager.py \
  read_state \
  ".claude/agents/state/agenthero-ai/topics/auth-system/task-001-backend.json" \
  "status"

# Update progress
python .claude/skills/agenthero-ai/scripts/state_manager.py \
  update_progress \
  ".claude/agents/state/agenthero-ai/topics/auth-system/task-001-backend.json" \
  50
```

### 3. Utility Functions (`scripts/utils.py`)

**Purpose**: Shared helper functions

**Functions**:
- `find_project_root()` - Find project root by locating .claude directory
- `slugify(text)` - Convert text to URL-safe slug
- `generate_task_id(topic_slug)` - Generate unique task ID
- `timestamp_iso()` - Get ISO 8601 timestamp with timezone
- `atomic_write(path, content)` - Atomic file write (supports dict/list/str)
- `ensure_directory(path)` - Create directory if needed
- `read_json_file(path)` - Read and parse JSON file
- `read_json_field(path, field)` - Read specific JSON field
- `update_json_field(path, field, value)` - Update JSON field
- `append_json_array(path, field, value)` - Append to JSON array
- `validate_json(path)` - Validate JSON structure

**Usage** (imported by other scripts):
```python
from utils import (
    find_project_root, slugify, timestamp_iso,
    atomic_write, read_json_file
)

# Generate slug
slug = slugify("Add JWT Authentication")
# Returns: "add-jwt-authentication"

# Atomic write (prevents corruption)
atomic_write("state.json", {"status": "completed"})

# Find project root
project_root = find_project_root()
# Returns: Path to directory containing .claude/
```

### 4. Setup Project Structure (`scripts/setup_project_structure.py`)

**Purpose**: Create initial directory structure for topics

**Usage**:
```bash
# Create Project-tasks/{slug}/ structure
python .claude/skills/agenthero-ai/scripts/setup_project_structure.py \
  "landing-page-builder"

# Creates:
# - Project-tasks/landing-page-builder/
# - Project-tasks/landing-page-builder/spec/
# - Project-tasks/landing-page-builder/deliverables/
```

### 5. Finalize Topic (`scripts/finalize_topic.py`)

**Purpose**: Mark topic as completed and archive

**Usage**:
```bash
# Finalize topic (V2.0)
python .claude/skills/agenthero-ai/scripts/finalize_topic.py \
  "landing-page-builder"

# Actions:
# 1. Marks status as "completed" in topics.json
# 2. Sets completedAt timestamp
# 3. Archives topic directory
```

### 6. Check Topics File (`scripts/check_topics_file.py`)

**Purpose**: Validate topics.json structure

**Usage**:
```bash
# Validate topics registry (V2.0)
python .claude/skills/agenthero-ai/scripts/check_topics_file.py --summary

# Returns summary of topics.json health
```

### 7. SessionStart Hook (`scripts/get_topics_quiet.sh`)

**Purpose**: Display active topics on Claude Code startup

**Usage** (configured in `.claude/settings.local.json`):
```bash
bash .claude/skills/agenthero-ai/scripts/get_topics_quiet.sh

# Output (if topics exist):
# Found 2 active topic(s):
#   • Landing Page Builder (45% complete, 3/5 tasks)
#   • API Integration (20% complete, 1/4 tasks)

# Output (if no topics):
# No pending topics - ready for new work!
```

## State File Templates (V2.0)

Templates are stored in `templates/state-templates.json`:

### Task State Template
```json
{
  "taskId": "",
  "focusArea": "",
  "agentName": "",
  "status": "pending",
  "assignedAt": "",
  "startedAt": null,
  "completedAt": null,
  "progress": 0,
  "currentOperation": null,
  "logs": [],
  "filesCreated": [],
  "filesModified": [],
  "blockingQuestion": null,
  "result": null,
  "error": null,
  "tokenUsage": {
    "total": 0,
    "operations": []
  }
}
```

## Integration with PM Orchestrator

The PM agent (`agenthero-ai`) uses these utilities for:

### 1. Topic Initialization
```bash
# PM creates new topic (V2.0)
python .claude/skills/agenthero-ai/scripts/topic_manager.py \
  create_topic "User login feature" \
  --description "Create login with validation"

# Returns: user-login-feature (slug)
```

### 2. Directory Setup
```bash
# PM creates Project-tasks structure
python .claude/skills/agenthero-ai/scripts/setup_project_structure.py \
  "user-login-feature"
```

### 3. Task State Management
```bash
# PM initializes sub-agent task
python .claude/skills/agenthero-ai/scripts/state_manager.py \
  create_state_file \
  ".claude/agents/state/agenthero-ai/topics/login-feature/task-001-frontend.json" \
  "task-state"
```

### 4. Progress Monitoring
```bash
# PM reads task status
python .claude/skills/agenthero-ai/scripts/state_manager.py \
  read_state \
  ".claude/agents/state/agenthero-ai/topics/login-feature/task-001-frontend.json" \
  "status"
```

### 5. Topic Completion
```bash
# PM finalizes topic (V2.0)
python .claude/skills/agenthero-ai/scripts/finalize_topic.py \
  "login-feature"
```

## Integration with Sub-Agents

Sub-agents use state_manager for logging and updates:

```bash
# Sub-agent logs progress
python .claude/skills/agenthero-ai/scripts/state_manager.py \
  append_log \
  "$STATE_FILE" \
  "info" \
  "Creating LoginForm component"

# Sub-agent updates progress
python .claude/skills/agenthero-ai/scripts/state_manager.py \
  update_progress \
  "$STATE_FILE" \
  40

# Sub-agent tracks file changes
python .claude/skills/agenthero-ai/scripts/state_manager.py \
  track_file_change \
  "$STATE_FILE" \
  "src/components/LoginForm.tsx" \
  "created"
```

## Best Practices

1. **Always validate JSON** before writing (automatic in atomic_write)
2. **Use atomic writes** to prevent corruption (built-in)
3. **Log regularly** (every 30-60 seconds minimum)
4. **Update progress milestones** (25%, 50%, 75%, 100%)
5. **Track file changes** in state files
6. **Archive completed topics** for history (automatic via finalize_topic.py)

## Error Handling

All scripts include error handling:
- Validate input parameters
- Check file existence
- Verify JSON structure (automatic validation)
- Return meaningful error codes (0 = success, 1 = error)
- Log errors to stderr (colored output)

## Performance

State operations are optimized:
- Atomic writes prevent corruption
- Minimal file I/O
- Path resolution caches project root
- JSON validation only when needed

## Security

State files may contain sensitive data:
- Gitignored by default (`.claude/agents/state/`)
- File permissions: 644 (owner read/write)
- No credentials stored in state
- Audit trail via logs array

## Troubleshooting

**Invalid JSON error:**
```bash
# Validate state file
python .claude/skills/agenthero-ai/scripts/state_manager.py \
  validate_state \
  ".claude/agents/state/agenthero-ai/topics/my-topic/task-001.json"
```

**State file not found:**
```bash
# Check topics registry
cat .claude/agents/state/agenthero-ai/topics.json | python -m json.tool
```

**Wrong directory created:**
```bash
# Ensure scripts run from project root OR
# Use absolute paths (scripts auto-detect project root via find_project_root())
```

## Version

**Version**: 2.0.0
**Created**: 2025-10-22
**Updated**: 2025-10-24 (Python migration complete)

## Migration Notes (V1 → V2)

**Key Changes**:
- ✅ Bash scripts → Python scripts
- ✅ Individual topic.json files → Single topics.json registry
- ✅ Relative paths → Absolute path resolution
- ✅ Manual JSON handling → Atomic write with validation
- ✅ List support added to atomic_write()

## Support

For issues:
1. Check JSON validity: `python -m json.tool < file.json`
2. Validate topics.json: `check_topics_file.py --summary`
3. Review state structure: See `STATE-STRUCTURE-V2.md`
4. Verify directory structure exists
5. Check file permissions

---

**Part of**: Hierarchical Multi-Agent Orchestration System V2.0
**Related**: agenthero-ai agent, orchestrated-sub-agent-template
