---
name: copy-skill
description: Copy a skill from Product Forge to user or project level
argument-hint: "[<plugin>:<skill-name>] [--user | --project]"
---

# Copy Skill

Copy a skill from Product Forge plugins to your user-level (`~/.claude/`) or project-level (`.claude/`) directory.

## Usage

```bash
# List available skills
/copy-skill

# Copy to project (default)
/copy-skill product-design:python-style

# Copy to user level
/copy-skill product-design:python-style --user

# Explicit project level
/copy-skill git-workflow:commit-patterns --project
```

## Arguments

- `<plugin>:<skill-name>` - The skill to copy in `plugin:name` format
- `--user` - Copy to `~/.claude/{plugin}/skills/{name}/`
- `--project` - Copy to `.claude/{plugin}/skills/{name}/` (default)

## What Gets Copied

Skills are copied as **entire directories**, including:
- `SKILL.md` - The main skill definition
- Any additional files (scripts/, references/, *.yaml, etc.)

Example: `parallel-agents` skill contains both `SKILL.md` and `agent-skills-mapping.yaml`.

## Directory Structure

```
# Project-level (default)
.claude/
└── product-design/
    └── skills/
        └── python-style/
            └── SKILL.md

# User-level (--user)
~/.claude/
└── product-design/
    └── skills/
        └── python-style/
            └── SKILL.md
```

## Execution Instructions

When the user runs this command:

### No Arguments - List Available Skills

1. **Scan Product Forge plugins cache** for all available skills:
   ```bash
   ls ~/.claude/plugins/cache/product-forge-marketplace/*/skills/ 2>/dev/null
   ```

2. **For each plugin with skills**, list them with descriptions:
   - Read `SKILL.md` frontmatter to get `name` and `description`
   - Format as: `{plugin}:{skill-name} - {description}`

3. **Display formatted list**:
   ```
   Available skills from Product Forge:

   product-design:
     python-style - Python coding style and PEP standards
     prd-management - Automatic PRD lifecycle management
     parallel-agents - Multi-agent orchestration patterns
     ...

   git-workflow:
     commit-patterns - Git commit best practices
     ...

   Usage: /copy-skill <plugin>:<skill-name> [--user | --project]
   ```

### With Arguments - Copy Skill

1. **Parse arguments**:
   - Extract `plugin` and `skill-name` from `<plugin>:<skill-name>` format
   - Determine destination: `--user` or `--project` (default)

2. **Locate source skill**:
   ```bash
   SOURCE=~/.claude/plugins/cache/product-forge-marketplace/{plugin}/skills/{skill-name}
   ```
   - If not found, show error with available skills from that plugin

3. **Determine destination path**:
   - `--project`: `.claude/{plugin}/skills/{skill-name}/`
   - `--user`: `~/.claude/{plugin}/skills/{skill-name}/`

4. **Check if destination exists**:
   - If exists, use **AskUserQuestion** to prompt:
     ```
     Skill '{skill-name}' already exists at {destination}.

     Options:
     - Overwrite: Replace existing skill
     - Rename: Save as {skill-name}-copy
     - Cancel: Abort operation
     ```

5. **Create destination directory structure**:
   ```bash
   mkdir -p {destination}
   ```

6. **Copy entire skill directory recursively**:
   ```bash
   cp -r {source}/* {destination}/
   ```

7. **Confirm success**:
   ```
   Skill copied successfully!

   Source: ~/.claude/plugins/cache/product-forge-marketplace/{plugin}/skills/{skill-name}/
   Destination: {destination}

   Files copied:
   - SKILL.md
   - [any additional files]

   The skill is now available in your {project|user} configuration.
   ```

## Error Handling

- **Plugin not found**: Show list of available plugins
- **Skill not found**: Show list of skills in that plugin
- **Invalid format**: Show usage example with correct format
- **Copy failed**: Show error and suggest checking permissions
