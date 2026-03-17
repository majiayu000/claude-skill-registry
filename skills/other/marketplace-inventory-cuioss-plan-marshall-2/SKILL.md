---
name: tools-marketplace-inventory
description: Scans and reports complete marketplace inventory (bundles, agents, commands, skills, scripts)
user-invocable: false
allowed-tools: Read, Bash, Glob
---

# Marketplace Inventory Skill

Provides complete marketplace inventory scanning capabilities using the scan-marketplace-inventory.py script.

## Purpose

This skill scans the marketplace directory structure and returns a comprehensive TOON inventory of all bundles and their resources (agents, commands, skills, scripts).

## When to Use This Skill

Activate this skill when you need to:
- Get a complete inventory of marketplace bundles
- Discover all available agents, commands, and skills
- Validate marketplace structure
- Generate reports on marketplace contents

## Workflow

When activated, this skill scans the marketplace and returns structured TOON inventory.

### Step 1: Execute Inventory Scan

Run the marketplace inventory scanner script:

**Script**: `pm-plugin-development:tools-marketplace-inventory`

```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --scope marketplace
```

The script will:
- Discover all bundles in marketplace/bundles/
- Enumerate agents, commands, and skills in each bundle
- Identify bundled scripts
- Write full TOON inventory to `.plan/temp/tools-marketplace-inventory/inventory-{timestamp}.toon`
- Return TOON summary with file path to stdout

### Step 2: Read Full Inventory

The script outputs a TOON summary to stdout. Bundles are top-level keys (not a list):

```toon
status: success
scope: marketplace
base_path: /path/to/marketplace/bundles

plan-marshall:
  path: marketplace/bundles/plan-marshall
  agents[1]:
    - research-best-practices
  commands[2]:
    - tools-fix-intellij-diagnostics
    - tools-sync-agents-file
  skills[18]:
    - analyze-project-architecture
    - extension-api
    - manage-lessons

pm-dev-java:
  path: marketplace/bundles/pm-dev-java
  agents[9]:
    - java-coverage-agent
    - java-implement-agent
  skills[15]:
    - cui-java-core
    - java-cdi

statistics:
  total_bundles: 8
  total_agents: 28
  total_commands: 46
  total_skills: 30
  total_scripts: 7
```

In file mode (default), a summary is printed and full inventory is written to `.plan/temp/tools-marketplace-inventory/inventory-{timestamp}.toon`.

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
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --scope marketplace
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --scope project
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
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --resource-types agents,skills
```

### --include-descriptions (optional flag)

When specified, extracts description fields from YAML frontmatter of each resource file. Requires `--format json` to see structured output.

**Example**:
```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --include-descriptions --format json
```

### --full (optional flag)

When specified, includes full details: frontmatter fields and skill subdirectory contents with nested file listings. This is useful when you need to see what files exist within skill directories.

**Example**:
```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --full --bundles plan-marshall
```

**Output with --full** (excerpt):
```toon
plan-marshall:
  path: marketplace/bundles/plan-marshall

  skills[18]:
    - name: permission-doctor
      path: marketplace/bundles/plan-marshall/skills/permission-doctor
      description: Diagnose permission issues across settings files
      user_invocable: true
      allowed_tools: Read, Grep, Bash
      standards[2]:
        - permission-syntax.md
        - security-patterns.md
      scripts[1]:
        - permission-doctor.py
```

**Full mode includes:**
- Skill frontmatter: `user_invocable`, `allowed_tools`, `model`
- Skill subdirectories with their files: `standards/`, `templates/`, `scripts/`, `references/`, `knowledge/`, `examples/`, `documents/`

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
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --name-pattern "*-plan-*"

# Multiple patterns (pipe-separated)
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --name-pattern "*-plan-*|*-specify-*|plan-*|manage-*"
```

### --content-pattern (optional)

Filter resources by content using regex patterns. Use pipe (`|`) to separate multiple patterns (OR logic). **Requires `--include-descriptions` or `--full`** to enable path resolution.

| Pattern | Matches |
|---------|---------|
| `` ```json `` | Files containing JSON code blocks |
| `` ```toon `` | Files containing TOON code blocks |
| `## Output.*```json` | Output sections with JSON blocks (multiline) |

**Note**: Uses Python `re.search()` with `re.MULTILINE` flag. Scripts (.py, .sh) are NOT content-filtered.

**Examples**:
```bash
# Find files with JSON code blocks
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --resource-types agents,skills \
  --content-pattern '```json' \
  --include-descriptions \
  --direct-result

# Multiple patterns (OR logic)
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --resource-types skills \
  --content-pattern '```json|```toon' \
  --full \
  --direct-result
```

**Output with content filtering** includes filter stats:
```toon
status: success
scope: marketplace
content_pattern: "```json"
content_filter_stats:
  input_count: 188
  matched_count: 32
  excluded_count: 156
```

### --content-exclude (optional)

Exclude resources matching content patterns (OR logic). Use pipe (`|`) to separate multiple patterns. **Requires `--include-descriptions` or `--full`**.

**Examples**:
```bash
# Find JSON blocks but exclude already-migrated files
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --resource-types agents \
  --content-pattern '```json' \
  --content-exclude 'format: toon|output-format: toon' \
  --include-descriptions \
  --direct-result
```

### Combining --content-pattern and --content-exclude

When both are specified:
1. **Include filter**: File must match at least one include pattern
2. **Exclude filter**: File must NOT match any exclude pattern

```bash
# Find files with JSON but not configuration JSON
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --bundles pm-dev-java,pm-plugin-development \
  --resource-types agents \
  --content-pattern '```json' \
  --content-exclude '## Configuration.*```json' \
  --full \
  --direct-result
```

### --bundles (optional)

Filter to specific bundles by name (comma-separated).

**Example**:
```bash
# Single bundle
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --bundles planning

# Multiple bundles
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --bundles "planning,pm-dev-java,pm-dev-frontend"
```

### --direct-result (optional flag)

Output full TOON directly to stdout instead of writing to file.

| Mode | Behavior |
|------|----------|
| Default (no flag) | Writes to `.plan/temp/tools-marketplace-inventory/inventory-{timestamp}.toon`, prints summary |
| `--direct-result` | Outputs full TOON inventory directly to stdout |

**When to use `--direct-result`**:
- Small inventories (filtered bundles/patterns)
- Piped usage where file I/O is not desired
- Script-to-script calls where caller parses TOON directly

**Example**:
```bash
# Get full TOON directly (for small/filtered results)
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --bundles pm-workflow --direct-result
```

### --format (optional)

Output format. Default: `toon`

| Value | Description |
|-------|-------------|
| `toon` | TOON format with bundles as top-level keys (default) |
| `json` | JSON format with `bundles` as dict keyed by bundle name |

**JSON output structure:**
```json
{
  "status": "success",
  "scope": "marketplace",
  "bundles": {
    "plan-marshall": {
      "path": "marketplace/bundles/plan-marshall",
      "agents": ["research-best-practices"],
      "skills": ["permission-doctor", "manage-lessons"]
    }
  },
  "statistics": {...}
}
```

**Example**:
```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --format json --bundles pm-workflow
```

### --include-tests (optional flag)

When specified, includes test files from `test/{bundle-name}/` directories. Discovers `test_*.py` and `conftest.py` files and adds them as `tests` resource type to each bundle.

**Example**:
```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --include-tests --bundles pm-plugin-development --direct-result
```

**Output with --include-tests** (excerpt):
```toon
pm-plugin-development:
  path: marketplace/bundles/pm-plugin-development
  skills[14]:
    - ext-outline-plugin
    - ...
  tests[12]:
    - conftest
    - test_scan_marketplace_inventory
    - test_filter_inventory
    - ...
```

### --include-project-skills (optional flag)

When specified, includes project-level skills from `.claude/skills/` directory. Creates a `project-skills` pseudo-bundle containing skills and their scripts.

**Example**:
```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --include-project-skills --direct-result
```

**Output with --include-project-skills** (excerpt):
```toon
project-skills:
  path: .claude/skills
  skills[2]:
    - verify-workflow
    - sync-plugin-cache
  scripts[2]:
    - collect-artifacts
    - verify-structure
```

### Combining --include-tests and --include-project-skills

Both flags can be used together for a comprehensive scan:

```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --include-tests \
  --include-project-skills \
  --full \
  --direct-result
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
- Script reads marketplace directory structure
- Writes inventory to `.plan/temp/` (covered by `Write(.plan/**)` permission)
- All output is TOON format

---

## Dependency Resolution

The `resolve-dependencies.py` script tracks and resolves all dependency relationships across marketplace components.

### Dependency Types

| Type | Pattern | Detection Method |
|------|---------|------------------|
| `script` | `bundle:skill:script` | Regex in markdown/python |
| `skill` | `skills:` frontmatter, `Skill: bundle:skill` | YAML + regex |
| `import` | `from module import ...` | AST parsing |
| `path` | `../../skill/file.md` | Markdown link regex |
| `implements` | `implements: bundle:skill/path` frontmatter | YAML parsing |

### Component Notation

```
bundle:skill                    # Skill (e.g., pm-workflow:phase-1-init)
bundle:skill:script             # Script (e.g., pm-workflow:manage-files:manage-files)
bundle:agents:name              # Agent (e.g., pm-workflow:agents:plan-init-agent)
bundle:commands:name            # Command (e.g., plan-marshall:commands:tools-fix)
```

### Subcommands

#### deps - Get Dependencies

Get direct and transitive dependencies of a component:

```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:resolve-dependencies \
  deps --component pm-workflow:manage-files --direct-result
```

**Output**:
```toon
status: success
component: pm-workflow:manage-files
component_type: skill
file_path: marketplace/bundles/pm-workflow/skills/manage-files/SKILL.md

direct_dependencies[4]:
  - target: plan-marshall:ref-toon-format:toon_parser, type: import, context: line:28
  - target: plan-marshall:tools-file-ops:file_ops, type: import, context: line:26

transitive_dependencies[2]:
  - target: plan-marshall:ref-toon-format, depth: 2, via: plan-marshall:ref-toon-format:toon_parser

statistics:
  direct_count: 4
  transitive_count: 2
  by_type: {import: 3, path: 1}
```

#### rdeps - Get Reverse Dependencies

Get components that depend on a given component:

```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:resolve-dependencies \
  rdeps --component plan-marshall:ref-toon-format:toon_parser --direct-result
```

#### tree - Visual Dependency Tree

Generate a visual dependency tree:

```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:resolve-dependencies \
  tree --component pm-workflow:manage-files --depth 3 --direct-result
```

**Output**:
```
pm-workflow:manage-files
├── plan-marshall:ref-toon-format:toon_parser (import)
│   └── plan-marshall:ref-toon-format (skill)
├── plan-marshall:tools-file-ops:file_ops (import)
└── plan-marshall:manage-logging:plan_logging (import)
```

#### validate - Check for Issues

Validate all dependencies and check for broken or circular references:

```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:resolve-dependencies \
  validate --scope marketplace --direct-result
```

**Output**:
```toon
status: success
validation_result: passed
total_components: 95
total_dependencies: 234
resolved: 231
unresolved_count: 3

unresolved[3]:
  - source: pm-workflow:manage-files, target: nonexistent:skill, type: skill, context: frontmatter
```

### Options

| Option | Description |
|--------|-------------|
| `--component <notation>` | Component to resolve (required for deps/rdeps/tree) |
| `--scope <value>` | auto, marketplace, plugin-cache, project (default: auto) |
| `--format <value>` | toon (default), json |
| `--direct-result` | Output to stdout |
| `--depth <N>` | Max transitive depth (default: 10) |
| `--dep-types <types>` | Filter: script,skill,import,path,implements (comma-separated) |

### Examples

```bash
# Get all dependencies of a skill
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:resolve-dependencies \
  deps --component pm-workflow:phase-1-init --direct-result

# Get only import dependencies
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:resolve-dependencies \
  deps --component pm-workflow:manage-files --dep-types import --direct-result

# Find what depends on a module
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:resolve-dependencies \
  rdeps --component plan-marshall:ref-toon-format:toon_parser --direct-result --format json

# Validate entire marketplace
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:resolve-dependencies \
  validate --scope marketplace
```

## References

- Script location: scripts/scan-marketplace-inventory.py
- Dependency resolution: scripts/resolve-dependencies.py
- Marketplace root: marketplace/bundles/
