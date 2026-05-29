---
name: agentic-export
description: "Export reusable assets from a project into this repository's v0.2 plugin architecture (skills, templates, agents)."
project-agnostic: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Skill
---

# Agentic Export

Export assets from a project into this repository.

## Arguments

- **asset_type**: `skill` | `template` | `agent`
- **asset_name_or_path**: source asset name/path in project
- **agentic_config_path**: optional path to this repository
- **options**: optional flags (`--plugin`, `--force`, `--dry-run`)

Request: `$ARGUMENTS`

## Execution

Delegate to shared logic via explicit skill invocation:

```python
Skill(skill="agentic-share", args="export $ARGUMENTS")
```

## Examples

```bash
# Export project skill into ac-tools plugin
/agentic-export skill my-skill --plugin ac-tools

# Export template directory
/agentic-export template templates/release-checklist

# Export an agent markdown file
/agentic-export agent /absolute/path/to/spec-reviewer.md

# Dry run preview
/agentic-export skill my-skill --plugin ac-qa --dry-run
```

## Pre-Flight Check

Before delegating, verify:

1. Source asset exists in the project.
2. Destination repository path is resolvable.
3. For `skill`, destination plugin is explicit or inferable.

If checks fail, provide a clear error and stop.

## Path Resolution

Repository path resolution order:

1. Explicit argument
2. Current working directory (skill runs inside repo)
3. Abort if not in agentic-config repo
