---
name: integrate-command
description: Integrate a user or project command into Product Forge
argument-hint: "<command-name> --plugin=<plugin-name> [--source=user|project]"
---

# Integrate Command

Import a command from your user-level (`~/.claude/`) or project-level (`.claude/`) directory into a Product Forge plugin.

## Usage

```bash
# Integrate from user level (default source)
/integrate-command my-command --plugin=claude-code-dev

# Integrate from project level
/integrate-command my-command --plugin=claude-code-dev --source=project

# Integrate from a specific plugin subdirectory
/integrate-command my-command --plugin=git-workflow --source=user
```

## Arguments

- `<command-name>` - Name of the command to integrate (without .md extension)
- `--plugin=<name>` - Target Product Forge plugin (required)
- `--source=user|project` - Where to find the command (default: `user`)

## Source Locations

- `--source=user`: Searches in `~/.claude/*/commands/` directories
- `--source=project`: Searches in `.claude/*/commands/` directories

## Execution Instructions

When the user runs this command:

### 1. Parse Arguments

- Extract `command-name` from first argument
- Extract `plugin` from `--plugin=` flag (required)
- Extract `source` from `--source=` flag (default: `user`)

### 2. Locate Source Command

Search for the command file:

```bash
# For --source=user
find ~/.claude -path "*/commands/${command-name}.md" -type f 2>/dev/null

# For --source=project
find .claude -path "*/commands/${command-name}.md" -type f 2>/dev/null
```

If multiple matches found, list them and ask user to specify the full path.

If not found:
```
Command '${command-name}' not found in ${source} level.

Searched locations:
- ~/.claude/*/commands/${command-name}.md

Available commands:
[list available .md files in commands directories]
```

### 3. Validate Target Plugin

Check the target plugin exists in Product Forge:

```bash
ls plugins/${plugin}/.claude-plugin/plugin.json
```

If not found:
```
Plugin '${plugin}' not found in Product Forge.

Available plugins:
- claude-code-dev
- product-design
- git-workflow
- python-experts
- ...
```

### 4. Determine Destination

```bash
DESTINATION=plugins/${plugin}/commands/${command-name}.md
```

### 5. Check for Conflicts

If destination exists, use **AskUserQuestion** to prompt:
```
Command '${command-name}' already exists in plugin '${plugin}'.

Options:
- Overwrite: Replace existing command
- Rename: Save as ${command-name}-new.md
- Cancel: Abort operation
```

### 6. Copy Command

```bash
cp ${source_path} plugins/${plugin}/commands/${command-name}.md
```

### 7. Confirm Success

```
Command integrated successfully!

Source: ${source_path}
Destination: plugins/${plugin}/commands/${command-name}.md

Next steps:
1. Review the command: cat plugins/${plugin}/commands/${command-name}.md
2. Refresh plugins: /forge-refresh --force
3. Commit changes: git add plugins/${plugin}/commands/${command-name}.md
```

## Example Workflow

```bash
# 1. Create a command at user level
# (manually or by copying and modifying)

# 2. Test it in your projects

# 3. Once ready, integrate into Product Forge
/integrate-command my-awesome-command --plugin=claude-code-dev

# 4. Refresh to make it available
/forge-refresh --force

# 5. Commit and push
git add plugins/claude-code-dev/commands/my-awesome-command.md
git commit -m "feat(claude-code-dev): add my-awesome-command"
```

## Error Handling

- **Command not found**: Show search locations and available commands
- **Plugin not found**: Show list of available plugins
- **Missing --plugin flag**: Show usage with example
- **Copy failed**: Show error and suggest checking permissions
