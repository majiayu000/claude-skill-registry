---
name: Documentation README Sync
description: Automatically regenerate README.md from Betty Framework registries
---

# docs.sync.readme

## Overview

**docs.sync.readme** is the documentation synchronization tool that regenerates the top-level `README.md` to reflect all current registered skills and agents. It ensures that the README stays in sync with the actual state of the Betty Framework by pulling from registry files.

## Purpose

Automates the maintenance of `README.md` to keep documentation accurate and up-to-date with:
- **Skill Registry** (`registry/skills.json`) – All registered skills
- **Agent Registry** (`registry/agents.json`) – All registered agents

This eliminates manual editing of the README and prevents documentation drift as skills and agents are added, modified, or removed.

## What It Does

1. **Reads Registries**: Loads `skills.json` and `agents.json`
2. **Categorizes Skills**: Groups skills by tag/category:
   - Foundation (skill.*, registry.*, workflow.*)
   - API Development (api.*)
   - Infrastructure (agents, commands, hooks, policy)
   - Governance (policy, audit)
3. **Updates Sections**:
   - Current Core Skills table with categorized skills
   - Agents documentation links
   - Skills documentation references
4. **Maintains Style**: Preserves README tone, formatting, and structure
5. **Generates Report**: Creates sync report with statistics

## Usage

### Basic Usage

```bash
python skills/docs.sync.readme/readme_sync.py
```

No arguments required - reads from standard registry locations.

### Via Betty CLI

```bash
/docs/sync/readme
```

### Expected Registry Structure

```
betty/
├── registry/
│   ├── skills.json      # Skills registry
│   └── agents.json      # Agents registry
└── README.md            # File to update
```

## Behavior

### 1. Registry Loading

Reads JSON files from:
- `registry/skills.json` – Skills registry
- `registry/agents.json` – Agents registry

If a registry file is missing, logs a warning and continues with empty data.

### 2. Skill Categorization

**Foundation Skills**:
- Matches: `skill.*`, `registry.*`, `workflow.*`
- Examples: `skill.create`, `workflow.compose`

**API Development Skills**:
- Matches: `api.*` or tags: `api`, `openapi`, `asyncapi`
- Examples: `api.define`, `api.validate`

**Infrastructure Skills**:
- Matches tags: `agents`, `command`, `hook`, `policy`, `plugin`
- Examples: `agent.define`, `hook.register`, `plugin.sync`

**Governance Skills**:
- Matches tags: `governance`, `policy`, `audit`
- Examples: `policy.enforce`, `audit.log`

Only **active** skills are included. Test skills (starting with `test.`) are filtered out.

### 3. Skills Section Update

Replaces the "## 🧩 Current Core Skills" section with:

```markdown
## 🧩 Current Core Skills

Betty's self-referential "kernel" of skills bootstraps the rest of the system:

### Foundation Skills

| Skill | Purpose |
|--------|----------|
| **skill.create** | Generates a new Betty Framework Skill directory and manifest. |
| **skill.define** | Validates and registers skill manifests (.skill.yaml) for the Betty Framework. |
| **registry.update** | Updates the Betty Framework Skill Registry by adding or modifying entries. |

### API Development Skills

| Skill | Purpose |
|--------|----------|
| **api.define** | Create OpenAPI and AsyncAPI specifications from templates |
| **api.validate** | Validate OpenAPI and AsyncAPI specifications against enterprise guidelines |

### Infrastructure Skills

| Skill | Purpose |
|--------|----------|
| **agent.define** | Validates and registers agent manifests for the Betty Framework. |
| **hook.define** | Create and register validation hooks for Claude Code |

These skills form the baseline for an **AI-native SDLC** where creation, validation, registration, and orchestration are themselves skills.
```

### 4. Agents Section Update

Updates the "### Agents Documentation" subsection with current agents:

```markdown
### Agents Documentation

Each agent has a `README.md` in its directory:
* [api.designer](agents/api.designer/README.md) — Design RESTful APIs following enterprise guidelines with iterative refinement
* [api.analyzer](agents/api.analyzer/README.md) — Analyze API specifications for backward compatibility and breaking changes
```

Includes both `active` and `draft` agents.

### 5. Report Generation

Creates `sync_report.json` with statistics:

```json
{
  "skills_by_category": {
    "foundation": 5,
    "api": 4,
    "infrastructure": 9,
    "governance": 1
  },
  "total_skills": 19,
  "agents_count": 2,
  "timestamp": "2025-10-23T20:30:00.123456+00:00"
}
```

## Outputs

### Success Response

```json
{
  "ok": true,
  "status": "success",
  "readme_path": "/home/user/betty/README.md",
  "report": {
    "skills_by_category": {
      "foundation": 5,
      "api": 4,
      "infrastructure": 9,
      "governance": 1
    },
    "total_skills": 19,
    "agents_count": 2,
    "timestamp": "2025-10-23T20:30:00.123456+00:00"
  }
}
```

### Failure Response

```json
{
  "ok": false,
  "status": "failed",
  "error": "README.md not found at /home/user/betty/README.md"
}
```

## What Gets Updated

### ✅ Updated Sections

- **Current Core Skills** (categorized tables)
- **Agents Documentation** (agent links list)
- Skills documentation references

### ❌ Not Modified

- Mission and inspiration
- Purpose and scope
- Repository structure
- Design principles
- Roadmap
- Contributing guidelines
- Requirements

The skill only updates specific documentation sections while preserving all other README content.

## Examples

### Example 1: Sync After Adding New Skills

**Scenario**: You've added several new skills and want to update the README

```bash
# Create and register new skills
/skill/create data.transform "Transform data between formats"
/skill/define skills/data.transform/skill.yaml

/skill/create telemetry.report "Generate telemetry reports"
/skill/define skills/telemetry.report/skill.yaml

# Sync README to include new skills
/docs/sync/readme
```

**Output**:
```
INFO: Starting README.md sync from registries...
INFO: Loading registry files...
INFO: Generating updated README content...
INFO: ✅ Updated README.md
INFO:    - Foundation skills: 5
INFO:    - API skills: 4
INFO:    - Infrastructure skills: 11
INFO:    - Governance skills: 1
INFO:    - Total active skills: 21
INFO:    - Agents: 2
```

### Example 2: Sync After Adding New Agent

**Scenario**: A new agent has been registered and needs to appear in README

```bash
# Define new agent
/agent/define agents/workflow.optimizer/agent.yaml

# Sync README
/docs/sync/readme
```

The new agent will appear in the "### Agents Documentation" section.

### Example 3: Automated Sync in Workflow

**Scenario**: Include README sync as a workflow step after registering skills

```yaml
# workflows/skill_release.yaml
steps:
  - skill: skill.define
    args: ["skills/new.skill/skill.yaml"]

  - skill: plugin.sync
    args: []

  - skill: docs.sync.readme
    args: []
```

This ensures README, plugin.yaml, and registries stay in sync.

## Integration

### With skill.define

After defining skills, sync the README:

```bash
/skill/define skills/my.skill/skill.yaml
/docs/sync/readme
```

### With agent.define

After defining agents, sync the README:

```bash
/agent/define agents/my.agent/agent.yaml
/docs/sync/readme
```

### With Hooks

Auto-sync README when registries change:

```yaml
# .claude/hooks.yaml
- event: on_file_save
  pattern: "registry/*.json"
  command: python skills/docs.sync.readme/readme_sync.py
  blocking: false
  description: Auto-sync README when registries change
```

### With plugin.sync

Chain both sync operations:

```bash
/plugin/sync && /docs/sync/readme
```

## Categorization Rules

### Foundation Category

**Criteria**:
- Skill name starts with: `skill.`, `registry.`, `workflow.`
- Core Betty framework functionality

**Examples**:
- `skill.create`, `skill.define`
- `registry.update`, `registry.query`
- `workflow.compose`, `workflow.validate`

### API Category

**Criteria**:
- Skill name starts with: `api.`
- Tags include: `api`, `openapi`, `asyncapi`

**Examples**:
- `api.define`, `api.validate`
- `api.generate-models`, `api.compatibility`

### Infrastructure Category

**Criteria**:
- Tags include: `agents`, `command`, `hook`, `policy`, `plugin`, `registry`
- Infrastructure and orchestration skills

**Examples**:
- `agent.define`, `agent.run`
- `hook.define`, `hook.register`
- `plugin.sync`, `plugin.build`

### Governance Category

**Criteria**:
- Tags include: `governance`, `policy`, `audit`
- Policy enforcement and audit trails

**Examples**:
- `policy.enforce`
- `audit.log`

## Filtering Rules

### ✅ Included

- Skills with `status: active`
- Agents with `status: active` or `status: draft`
- Skills with meaningful descriptions

### ❌ Excluded

- Skills with `status: draft`
- Skills starting with `test.`
- Skills without names or descriptions

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "README.md not found" | Missing README file | Ensure README.md exists in repo root |
| "Registry file not found" | Missing registry | Run skill.define to populate registry |
| "Failed to parse JSON" | Invalid JSON | Fix JSON syntax in registry files |

## Files Read

- `README.md` – Current README content
- `registry/skills.json` – Skills registry
- `registry/agents.json` – Agents registry

## Files Modified

- `README.md` – Updated with current skills and agents
- `skills/docs.sync.readme/sync_report.json` – Sync statistics

## Exit Codes

- **0**: Success (README updated successfully)
- **1**: Failure (error during sync)

## Logging

Logs sync progress:

```
INFO: Starting README.md sync from registries...
INFO: Loading registry files...
INFO: Generating updated README content...
INFO: ✅ Updated README.md
INFO:    - Foundation skills: 5
INFO:    - API skills: 4
INFO:    - Infrastructure skills: 9
INFO:    - Governance skills: 1
INFO:    - Total active skills: 19
INFO:    - Agents: 2
```

## Best Practices

1. **Run After Registry Changes**: Sync README whenever skills or agents are added/updated
2. **Include in CI/CD**: Add README sync to deployment pipelines
3. **Review Before Commit**: Check updated README before committing changes
4. **Use Hooks**: Set up auto-sync hooks for convenience
5. **Combine with plugin.sync**: Keep both plugin.yaml and README in sync
6. **Version Control**: Always commit README changes with skill/agent changes

## Troubleshooting

### README Not Updating

**Problem**: Changes to registry don't appear in README

**Solutions**:
- Ensure skills have `status: active`
- Check that skill names and descriptions are present
- Verify registry files are valid JSON
- Run `/skill/define` before syncing README

### Skills in Wrong Category

**Problem**: Skill appears in unexpected category

**Solutions**:
- Check skill tags in skill.yaml
- Verify tag categorization rules above
- Add appropriate tags to skill.yaml
- Re-run skill.define to update registry

### Section Markers Not Found

**Problem**: "Section marker not found" warnings

**Solutions**:
- Ensure README has expected section headers
- Check for typos in section headers
- Restore original README structure if modified
- Update section_marker strings in code if intentionally changed

## Architecture

### Skill Categories

**Documentation** – docs.sync.readme maintains the README documentation layer by syncing registry state to the top-level README.

### Design Principles

- **Single Source of Truth**: Registries are the source of truth
- **Preserve Structure**: Only update specific sections
- **Maintain Style**: Keep original tone and formatting
- **Clear Categorization**: Logical grouping of skills by function
- **Idempotent**: Can be run multiple times safely

## See Also

- **plugin.sync** – Sync plugin.yaml with registries ([SKILL.md](../plugin.sync/SKILL.md))
- **skill.define** – Validate and register skills ([SKILL.md](../skill.define/SKILL.md))
- **agent.define** – Validate and register agents ([SKILL.md](../agent.define/SKILL.md))
- **registry.update** – Update registries ([SKILL.md](../registry.update/SKILL.md))
- **Betty Architecture** – Framework overview ([betty-architecture.md](../../docs/betty-architecture.md))

## Dependencies

- **registry.update**: Registry management
- **betty.config**: Configuration constants and paths
- **betty.logging_utils**: Logging infrastructure

## Status

**Active** – Production-ready documentation skill

## Version History

- **0.1.0** (Oct 2025) – Initial implementation with skills categorization and agents documentation
