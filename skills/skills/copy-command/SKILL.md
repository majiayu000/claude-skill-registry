---
name: copy-command
description: Copy a command from Product Forge to user or project level
argument-hint: "[<plugin>:<command-name>] [--user | --project]"
---

# Copy Command

Copy a command from Product Forge plugins to your user-level (`~/.claude/`) or project-level (`.claude/`) directory.

## Usage

```bash
# List available commands
/copy-command

# Copy to project (default)
/copy-command product-design:create-prd

# Copy to user level
/copy-command git-workflow:commit --user

# Explicit project level
/copy-command devops-data:create-rfc --project
```

## Arguments

- `<plugin>:<command-name>` - The command to copy in `plugin:name` format
- `--user` - Copy to `~/.claude/{plugin}/commands/{name}.md`
- `--project` - Copy to `.claude/{plugin}/commands/{name}.md` (default)

## What Gets Copied

Commands are single markdown files (`.md`) containing:
- YAML frontmatter with description and argument hints
- Documentation and usage examples
- Execution instructions for Claude Code

## Directory Structure

```
# Project-level (default)
.claude/
└── git-workflow/
    └── commands/
        └── commit.md

# User-level (--user)
~/.claude/
└── git-workflow/
    └── commands/
        └── commit.md
```

## Execution Instructions

When the user runs this command:

### No Arguments - List Available Commands

1. **Scan Product Forge plugins cache** for all available commands:
   ```bash
   ls ~/.claude/plugins/cache/product-forge-marketplace/*/commands/*.md 2>/dev/null
   ```

2. **For each plugin with commands**, list them with descriptions:
   - Read command file frontmatter to get `description`
   - Format as: `{plugin}:{command-name} - {description}`

3. **Display formatted list**:
   ```
   Available commands from Product Forge:

   product-design:
     create-prd - Interactive PRD creation wizard
     create-qa-test - Create a new QA test procedure
     task-focus - Focus on a specific task with context
     ...

   git-workflow:
     commit - Guided git commit with atomic commit analysis
     rebase - Rebase local changes on remote updates
     code-review - Review code changes for issues
     ...

   devops-data:
     create-rfc - Create a new RFC technical specification
     create-tech-spec - Create a new Technical Specification
     ...

   Usage: /copy-command <plugin>:<command-name> [--user | --project]
   ```

### With Arguments - Copy Command

1. **Parse arguments**:
   - Extract `plugin` and `command-name` from `<plugin>:<command-name>` format
   - Determine destination: `--user` or `--project` (default)

2. **Locate source command**:
   ```bash
   SOURCE=~/.claude/plugins/cache/product-forge-marketplace/{plugin}/commands/{command-name}.md
   ```
   - If not found, show error with available commands from that plugin

3. **Determine destination path**:
   - `--project`: `.claude/{plugin}/commands/{command-name}.md`
   - `--user`: `~/.claude/{plugin}/commands/{command-name}.md`

4. **Check if destination exists**:
   - If exists, use **AskUserQuestion** to prompt:
     ```
     Command '{command-name}' already exists at {destination}.

     Options:
     - Overwrite: Replace existing command
     - Rename: Save as {command-name}-copy.md
     - Cancel: Abort operation
     ```

5. **Create destination directory structure**:
   ```bash
   mkdir -p {destination_dir}
   ```

6. **Copy command file**:
   ```bash
   cp {source} {destination}
   ```

7. **Confirm success**:
   ```
   Command copied successfully!

   Source: ~/.claude/plugins/cache/product-forge-marketplace/{plugin}/commands/{command-name}.md
   Destination: {destination}

   The command is now available as /{command-name} in your {project|user} configuration.
   ```

## Error Handling

- **Plugin not found**: Show list of available plugins
- **Command not found**: Show list of commands in that plugin
- **Invalid format**: Show usage example with correct format
- **Copy failed**: Show error and suggest checking permissions
