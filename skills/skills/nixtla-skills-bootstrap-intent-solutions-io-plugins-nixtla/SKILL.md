---
name: nixtla-skills-bootstrap
description: "Generate and configure Nixtla Skills using the CLI for forecasting workflows. Use when installing or updating skills. Trigger with 'install nixtla skills' or 'update nixtla'."
allowed-tools: "Read,Glob,Grep"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Nixtla Skills Bootstrap

Install or update Nixtla Skills in the current project using the nixtla-skills CLI.

## Overview

This skill manages Nixtla Skills installation:

- **Init**: First-time installation to `.claude/skills/`
- **Update**: Refresh existing skills to latest versions
- **Verify**: Check installation status and available skills

Skills persist locally until explicitly updated or removed.

## Prerequisites

**Required**:
- Python 3.8+
- `nixtla-skills` CLI tool

**Installation**:
```bash
pip install nixtla-claude-skills-installer
```

**Verify CLI**:
```bash
which nixtla-skills || echo "NOT_FOUND"
```

## Instructions

### Step 1: Choose Action

Select installation mode:
- `init` - First-time installation
- `update` - Refresh existing skills

### Step 2: Check CLI Availability

Verify nixtla-skills CLI is installed:
```bash
nixtla-skills --version
```

If not found, install with: `pip install nixtla-claude-skills-installer`

### Step 3: Run Installer

**For init**:
```bash
nixtla-skills init
```

**For update**:
```bash
nixtla-skills update
```

### Step 4: Verify Installation

```bash
ls -1d .claude/skills/nixtla-* 2>/dev/null | sort
```

## Output

After installation:
- `.claude/skills/nixtla-timegpt-lab/` - Core forecasting skill
- `.claude/skills/nixtla-experiment-architect/` - Experiment scaffolding
- `.claude/skills/nixtla-schema-mapper/` - Data transformation
- `.claude/skills/nixtla-skills-bootstrap/` - This skill

## Error Handling

1. **Error**: `nixtla-skills: command not found`
   **Solution**: `pip install nixtla-claude-skills-installer`

2. **Error**: `Permission denied`
   **Solution**: Check write permissions on `.claude/skills/`

3. **Error**: `Skills directory already exists`
   **Solution**: Use `update` instead of `init`

4. **Error**: `No skills installed after completion`
   **Solution**: Verify CLI version: `nixtla-skills --version`

## Examples

### Example 1: First-Time Installation

```bash
nixtla-skills init
```

**Output**:
```
Installing Nixtla Skills...
Created .claude/skills/nixtla-timegpt-lab/
Created .claude/skills/nixtla-experiment-architect/
Created .claude/skills/nixtla-schema-mapper/
Created .claude/skills/nixtla-skills-bootstrap/
Installation complete!
```

### Example 2: Update Existing Skills

```bash
nixtla-skills update
```

**Output**:
```
Updating Nixtla Skills...
Updated 4 skills to latest version.
```

## Resources

- PyPI Package: https://pypi.org/project/nixtla-claude-skills-installer/
- Skills Documentation: See individual skill SKILL.md files
- GitHub: https://github.com/Nixtla/nixtla-claude-skills

**Installed location**: `.claude/skills/nixtla-skills-bootstrap/`
