# TaskMaster Skill

> Agent-optimized task management system for AgentFabric.

---

## Setup

### Prerequisites

- Node.js 22+
- Working directory: `docs/plans/`

### Installation

#### Option 1: Direct Node.js (Agent Recommended)

```bash
cd docs/plans/taskmaster-skill/cli
npm install
```

Then use CLI via:
```bash
node cli/task.js <command>
```

#### Option 2: Shortcut Scripts (Install Dependencies Automatically)

```bash
cd docs/plans

# Windows
taskmaster-skill\task.bat <plan> <command>

# Linux/Mac
./taskmaster-skill/task.sh <plan> <command>
```

### Quick Start

```bash
# View all plans
node cli/task.js plans

# Check progress
node cli/task.js progress mvp_v1

# List tasks
node cli/task.js list mvp_v1

# List ready-to-start tasks (dependencies completed)
node cli/task.js ready mvp_v1
node cli/task.js ready mvp_v1 --limit 20
```

### Configuration (REQUIRED)

**Before using TaskMaster, you MUST configure the plan mapping:**

#### Step 1: Copy template
```bash
cp config.json.template config.json
```

#### Step 2: Edit config.json
```json
{
  "version": "1.0.0",
  "plans": {
    "mvp_v1": {
      "path": "E:\\Agent\\agent-fabric\\docs\\plans\\mvp_v1",
      "description": "AgentFabric MVP v1 实施计划"
    }
  },
  "settings": {
    "defaultPlan": "mvp_v1",
    "autoCreatePlan": false,
    "logRetentionDays": 30
  }
}
```

**Replace the path with your actual plan directory (absolute path).**

#### Step 3: Verify configuration
```bash
# List configured plans
node cli/task.js config list

# Add additional plans if needed
node cli/task.js config add <name> <path> --description "<desc>"

# Set default plan
node cli/task.js config set-default <name>
```

---

## Documentation Index

### Agent Instruction Manuals

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[COMMANDS.md](./COMMANDS.md)** | Complete command specifications | Need detailed syntax for any command |
| **[WORKFLOWS.md](./WORKFLOWS.md)** | Standard operation procedures | User asks to start/complete/audit tasks |
| **[BEST_PRACTICES.md](./BEST_PRACTICES.md)** | Operational rules and constraints | Need to validate operation against rules |

### Reference Data

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[DATA_FORMAT.md](./DATA_FORMAT.md)** | JSON schema specifications | Need to parse or construct data |
| **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** | Error codes and resolution procedures | Command returns error |

### Quick Reference

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[EXAMPLES.md](./EXAMPLES.md)** | Scenario-based execution patterns | User intent matches example scenario |
| **[TEMPLATES.md](./TEMPLATES.md)** | Copy-paste command templates | Need ready-to-use command |

---

## Quick Decision Map

```
User Request
    |
    +-- "查看/查询/了解..." ──► Read COMMANDS.md "Query Commands" section
    +-- "有哪些任务可以开始" ──► Read COMMANDS.md "ready" command
    +-- "开始/做...任务" ──► Read WORKFLOWS.md "Start Task Workflow"
    +-- "完成/做完了..." ──► Read WORKFLOWS.md "Complete Task Workflow"
    +-- "添加/新建...任务" ──► Read COMMANDS.md "add" + EXAMPLES.md "Adding New Task"
    +-- "归档..." ──► Verify done + verified ──► Read COMMANDS.md "archive"
    +-- "检查/核验..." ──► Read COMMANDS.md "verify"
    +-- "遇到问题/报错..." ──► TROUBLESHOOTING.md
```

---

## Command Syntax

All commands follow this pattern:
```bash
node cli/task.js <command> [options]
```

Or via shortcut scripts:
```bash
# Windows
taskmaster-skill\task.bat <plan> <command>

# Linux/Mac
./taskmaster-skill/task.sh <plan> <command>
```

## Execution Rules

**ALWAYS:**
1. Check dependencies before `start` (run `deps` first)
2. Verify before `archive` (run `verify` first)
3. Parse command output to determine next action
4. Confirm with user for `--force` operations

**NEVER:**
1. Skip `verify` before `archive` (unless user explicitly confirms `--force`)
2. Assume task ID without confirming
3. Ignore error messages in command output

---

## File Locations

```
docs/plans/
├── taskmaster-skill/
│   ├── cli/task.js        # CLI entry point
│   ├── config.json        # Plan configurations
│   ├── logs/              # Operation logs
│   │   ├── operations.log
│   │   └── operations.jsonl
│   └── *.md               # This documentation
│
└── <plan-name>/
    ├── data.json          # Task data (JSON format)
    └── README.md          # Plan description
```

---

## Version

- CLI Version: 1.1.0
- Data Format: 1.0.0
- Last Updated: 2026-03-04
