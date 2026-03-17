---
name: nixtla-skills-index
description: Lists all installed Nixtla Skills and provides guidance on which skill to use for specific tasks. Scans skills directory, reads frontmatter, outputs formatted index with categories and usage recommendations. Activates when user wants to see available skills, needs guidance on skill selection, or asks about Nixtla capabilities.
allowed-tools: "Read,Glob"
version: "1.0.0"
license: MIT
---

# Nixtla Skills Index

List all installed Nixtla Skills and provide usage guidance.

## Overview

This skill generates a directory of available Nixtla Skills:

- **Discovery**: Scans `.claude/skills/nixtla-*/` directories
- **Classification**: Categorizes by type (mode, utility, infrastructure)
- **Guidance**: Recommends skills based on user tasks
- **Formatted output**: Human-readable index table

## Prerequisites

**Required**:
- Nixtla Skills installed via `nixtla-skills init`
- Skills in `.claude/skills/nixtla-*/` directories

**No Additional Packages**: Uses only Read and Glob tools

## Instructions

### Step 1: Scan for Skills

Find all Nixtla skill directories:
```
Glob pattern: .claude/skills/nixtla-*/SKILL.md
```

### Step 2: Read Frontmatter

For each skill, extract:
- `name`: Skill identifier
- `description`: Purpose and triggers
- `mode`: Whether it's a mode skill
- `version`: Current version

### Step 3: Classify Skills

Organize into categories:
- **Mode Skills**: Change overall behavior
- **Utility Skills**: Perform specific tasks
- **Infrastructure Skills**: System operations

### Step 4: Generate Index

Output formatted markdown table with skill details.

## Output

Formatted markdown listing:

```markdown
## Nixtla Skills Index

| Skill | Description | When to Use |
|-------|-------------|-------------|
| nixtla-timegpt-lab | Forecasting expert mode | Starting Nixtla work |
| nixtla-schema-mapper | Data transformation | Converting data format |
| nixtla-experiment-architect | Experiment setup | Model comparisons |
```

## Error Handling

1. **Error**: `No skills found`
   **Solution**: Run `nixtla-skills init` to install

2. **Error**: `Malformed SKILL.md`
   **Solution**: Run `nixtla-skills update` to refresh

3. **Error**: `Skills directory not found`
   **Solution**: Verify `.claude/skills/` exists

4. **Error**: `Permission denied`
   **Solution**: Check directory permissions

## Examples

### Example 1: List All Skills

**User**: "What Nixtla skills are available?"

**Output**:
```
Nixtla Skills Index (8 skills installed):

Mode Skills:
- nixtla-timegpt-lab: Forecasting expert mode

Utility Skills:
- nixtla-schema-mapper: Data transformation
- nixtla-experiment-architect: Experiment setup
- nixtla-timegpt-finetune-lab: Fine-tuning
- nixtla-prod-pipeline-generator: Production deployment
- nixtla-usage-optimizer: Cost optimization
- nixtla-skills-index: This index

Infrastructure:
- nixtla-skills-bootstrap: Install/update skills
```

### Example 2: Find Right Skill

**User**: "Which skill for converting CSV to Nixtla format?"

**Output**:
```
Use: nixtla-schema-mapper

This skill transforms data to Nixtla schema (unique_id, ds, y).
Activate with: "Map my data to Nixtla format"
```

## Resources

- Skills Directory: `.claude/skills/nixtla-*/`
- Installer: `pip install nixtla-claude-skills-installer`

**Related Skills**:
- `nixtla-skills-bootstrap`: Install or update skills
