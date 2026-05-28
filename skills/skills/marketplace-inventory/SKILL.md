---
name: marketplace-inventory
description: Scans and reports complete marketplace inventory (bundles, agents, commands, skills, scripts)
allowed-tools:
  - Read
  - Bash
  - Glob
---

# Marketplace Inventory Skill

Provides complete marketplace inventory scanning capabilities using the scan-marketplace-inventory.py script.

## Purpose

This skill scans the marketplace directory structure and returns a comprehensive JSON inventory of all bundles and their resources (agents, commands, skills, scripts).

## When to Use This Skill

Activate this skill when you need to:
- Get a complete inventory of marketplace bundles
- Discover all available agents, commands, and skills
- Validate marketplace structure
- Generate reports on marketplace contents

## Workflow

When activated, this skill scans the marketplace and returns structured JSON inventory.

### Step 1: Execute Inventory Scan

Run the marketplace inventory scanner script:

**Script**: `plan-marshall:marketplace-inventory`

```bash
python3 .plan/execute-script.py plan-marshall:marketplace-inventory:scan-marketplace-inventory --scope marketplace
```

**Direct execution (bootstrap only - before executor exists):**

First, get the plugin root (or read from `.plan/marshall-state.toon` if cached):
```bash
python3 ~/.claude/plugins/cache/*/plan-marshall/*/skills/marshall-steward/scripts/bootstrap-plugin.py get-root
```

Then execute with the resolved path (auto-detects marketplace or plugin-cache):
```bash
python3 ${PLUGIN_ROOT}/plan-marshall/*/skills/marketplace-inventory/scripts/scan-marketplace-inventory.py
```

The script will:
- Discover all bundles in marketplace/bundles/
- Enumerate agents, commands, and skills in each bundle
- Identify bundled scripts
- Return complete JSON structure

### Step 2: Parse and Return Results

The script outputs JSON in this format:

```json
{
  "scope": "marketplace",
  "base_path": "/path/to/marketplace/bundles",
  "bundles": [
    {
      "name": "bundle-name",
      "path": "marketplace/bundles/bundle-name",
      "agents": [...],
      "commands": [...],
      "skills": [...],
      "scripts": [...],
      "statistics": {...}
    }
  ],
  "statistics": {
    "total_bundles": 8,
    "total_agents": 28,
    "total_commands": 46,
    "total_skills": 30,
    "total_scripts": 7,
    "total_resources": 111
  }
}
```

Return this JSON output to the invoking command for further processing.

## Script Parameters

### --scope (optional)

Directory scope to scan. Default: `auto`

| Value | Description |
|-------|-------------|
| `auto` | **Default**. Tries `marketplace/bundles/` first, falls back to `plugin-cache` |
| `marketplace` | Explicit: scans marketplace/bundles/ directory only |
| `plugin-cache` | Explicit: scans ~/.claude/plugins/cache/plan-marshall/ only |
| `global` | Scans ~/.claude directory |
| `project` | Scans .claude directory in current working directory |

The `auto` default makes the script work in both the marketplace repo and other projects without specifying a scope.

**Example**:
```bash
python3 .plan/execute-script.py plan-marshall:marketplace-inventory:scan-marketplace-inventory --scope marketplace
python3 .plan/execute-script.py plan-marshall:marketplace-inventory:scan-marketplace-inventory --scope project
```

### --resource-types (optional)

Filter which resource types to include in the inventory. Default: `all`

| Value | Description |
|-------|-------------|
| `all` | Include all resource types (default) |
| `agents` | Include only agents |
| `commands` | Include only commands |
| `skills` | Include only skills |
| `scripts` | Include only scripts |

Multiple types can be combined with commas:
```bash
python3 .plan/execute-script.py plan-marshall:marketplace-inventory:scan-marketplace-inventory --resource-types agents,skills
```

### --include-descriptions (optional flag)

When specified, extracts description fields from YAML frontmatter of each resource file.

**Example**:
```bash
python3 .plan/execute-script.py plan-marshall:marketplace-inventory:scan-marketplace-inventory --include-descriptions
```

**Output with descriptions**:
```json
{
  "agents": [
    {
      "name": "java-implement-agent",
      "path": "marketplace/bundles/pm-dev-java/agents/java-implement-agent.md",
      "description": "Implements Java code following CUI standards"
    }
  ]
}
```

### --name-pattern (optional)

Filter resources by name using fnmatch glob patterns. Use pipe (`|`) to separate multiple patterns.

| Pattern | Matches |
|---------|---------|
| `*-plan-*` | Names containing "-plan-" |
| `plan-*` | Names starting with "plan-" |
| `*-agent` | Names ending with "-agent" |

**Examples**:
```bash
# Single pattern
python3 .plan/execute-script.py plan-marshall:marketplace-inventory:scan-marketplace-inventory --name-pattern "*-plan-*"

# Multiple patterns (pipe-separated)
python3 .plan/execute-script.py plan-marshall:marketplace-inventory:scan-marketplace-inventory --name-pattern "*-plan-*|*-specify-*|plan-*|manage-*"
```

### --bundles (optional)

Filter to specific bundles by name (comma-separated).

**Example**:
```bash
# Single bundle
python3 .plan/execute-script.py plan-marshall:marketplace-inventory:scan-marketplace-inventory --bundles planning

# Multiple bundles
python3 .plan/execute-script.py plan-marshall:marketplace-inventory:scan-marketplace-inventory --bundles "planning,pm-dev-java,pm-dev-frontend"
```

## Error Handling

If the script fails:
- Check that the working directory is the repository root
- Verify marketplace/bundles/ directory exists
- Ensure script has execute permissions

## Non-Prompting Requirements

This skill is designed to run without user prompts. Required permissions:

**Script Execution:**
- `Bash(bash:*)` - Bash interpreter
- Script permissions synced via `/tools-setup-project-permissions`

**Ensuring Non-Prompting:**
- Resolve script paths from `.plan/scripts-library.toon` (system convention)
- Script only reads marketplace directory structure (no writes)
- All output is JSON to stdout

## References

- Script location: scripts/scan-marketplace-inventory.py
- Marketplace root: marketplace/bundles/
