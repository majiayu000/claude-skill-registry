---
name: planning-inventory
description: Scans and reports all planning-related components across marketplace bundles
user-invocable: false
allowed-tools: Read, Bash
---

# Planning Inventory Skill

Provides a unified view of all planning-related components across the marketplace, including core planning infrastructure and derived components in domain bundles.

## Purpose

Planning-related components are distributed across bundles:

| Bundle | Component Types |
|--------|-----------------|
| `pm-workflow` | Core infrastructure (plan-*, manage-*, *-workflow, thin agents) |
| `pm-plugin-development` | plugin-task-plan, plugin-solution-outline, plugin-plan-implement (skills) |

This skill provides a single command to discover all planning components.

**Note**: pm-dev-java and pm-dev-frontend no longer contain planning-specific components. The thin agent architecture in pm-workflow loads domain skills dynamically via references.json.

## When to Use This Skill

Activate this skill when you need to:

- Get a complete inventory of planning-related components
- Understand the planning component ecosystem
- Validate planning system integrity
- Generate reports on planning capabilities

## Workflow

### Step 1: Execute Planning Inventory Scan

Run the planning inventory scanner script:

**Script**: `pm-workflow:planning-inventory`

```bash
python3 .plan/execute-script.py pm-workflow:planning-inventory:scan-planning-inventory scan
```

### Step 2: Parse and Return Results

The script outputs JSON organized into core and derived categories.

## Script Parameters

### --format (optional)

Output format. Default: `full`

| Value | Description |
|-------|-------------|
| `full` | Complete inventory with paths and all details |
| `summary` | Compact summary with component names only |

**Examples**:
```bash
python3 .plan/execute-script.py pm-workflow:planning-inventory:scan-planning-inventory scan --format full
python3 .plan/execute-script.py pm-workflow:planning-inventory:scan-planning-inventory scan --format summary
```

### --include-descriptions (optional flag)

When specified, includes description fields from YAML frontmatter.

```bash
python3 .plan/execute-script.py pm-workflow:planning-inventory:scan-planning-inventory scan --include-descriptions
```

## Output Format

### Full Format

```json
{
  "patterns": ["plan-*", "manage-*", "*-workflow", "*-task-plan", "*-solution-outline", "*-plan-*"],
  "bundles_scanned": ["pm-workflow", "pm-plugin-development"],
  "core": {
    "bundle": "pm-workflow",
    "agents": [{"name": "plan-init-agent"}, {"name": "solution-outline-agent"}, {"name": "task-plan-agent"}, {"name": "task-execute-agent"}],
    "commands": [...],
    "skills": [...],
    "scripts": [...]
  },
  "derived": [
    {
      "bundle": "pm-plugin-development",
      "agents": [],
      "skills": [{"name": "plugin-task-plan"}, {"name": "plugin-solution-outline"}, {"name": "plugin-plan-implement"}]
    }
  ],
  "statistics": {
    "core": {"agents": 4, "commands": 4, "skills": 20, "scripts": 12, "total": 40},
    "derived": {"bundles": 1, "agents": 0, "skills": 3, "total": 3},
    "total_components": 43
  }
}
```

### Summary Format

```json
{
  "core_bundle": "pm-workflow",
  "core_components": [
    {"type": "skills", "names": ["plan-init", "plan-execute", "plan-finalize", ...]},
    {"type": "agents", "names": ["plan-init-agent", "solution-outline-agent", "task-plan-agent", "task-execute-agent"]},
    {"type": "commands", "names": ["task-implement", "plan-marshall", "pr-doctor"]}
  ],
  "derived_bundles": [
    {"bundle": "pm-plugin-development", "agents": [], "skills": ["plugin-task-plan", "plugin-solution-outline", "plugin-plan-implement"]}
  ],
  "statistics": {...}
}
```

## Component Categories

### Core Components (pm-workflow bundle)

| Pattern | Examples |
|---------|----------|
| `plan-*` | plan-init, plan-execute, plan-finalize |
| `manage-*` | manage-tasks, manage-plan-documents, manage-references, manage-lifecycle |
| `*-workflow` | pr-workflow, git-workflow, sonar-workflow |
| `task-*` | task-implement |
| `pr-*` | pr-doctor |

**Thin Agents** (4 generic agents that load domain skills dynamically):
- `plan-init-agent` - Initialize plan, detect domains
- `solution-outline-agent` - Create deliverables
- `task-plan-agent` - Create tasks from deliverables
- `task-execute-agent` - Execute single task

### Derived Components (domain bundles)

| Bundle | Skills |
|--------|--------|
| pm-plugin-development | plugin-task-plan, plugin-solution-outline, plugin-plan-implement |

**Note**: pm-dev-java and pm-dev-frontend no longer have planning-specific components. Domain skills are loaded by thin agents via references.json.

## Dependencies

This skill uses `pm-plugin-development:tools-marketplace-inventory` internally with:

- `--bundles`: Filtered to planning-related bundles
- `--name-pattern`: Filtered to planning-related patterns

## Non-Prompting Requirements

This skill is designed to run without user prompts. Required permissions:

**Script Execution:**
- `Bash(bash:*)` - Bash interpreter
- Script permissions synced via `/tools-setup-project-permissions`

**Script only reads marketplace directory structure (no writes).**
