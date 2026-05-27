---
name: create-slash-command
description: Create new slash commands for DevAgent workflows. Use when you need to create a new command file in .agents/commands/ and symlink it to .cursor/commands/ for Cursor IDE integration. This skill handles the complete command creation workflow including file generation, symlink creation, and structure validation.
---

# Create Slash Command

## Overview

This skill automates the creation of DevAgent slash commands, which are standardized command files that provide interfaces for executing workflows. Commands are created in `.agents/commands/` and symlinked to `.cursor/commands/` for Cursor IDE integration.

**Important**: Commands are **snippets/templates** that get inserted into the chat conversation when invoked in Cursor IDE. The entire command file content is inserted, and users fill in placeholder areas (like "Input Context:") with their specific information. Keep commands simple and self-contained—they should be ready to paste into chat.

## Quick Start

To create a new command:

1. **Create the command file**:
   ```bash
   python3 scripts/create_command.py <command-name> [--workflow <workflow-name>]
   ```

2. **Create the symlink**:
   ```bash
   python3 scripts/create_symlink.py <command-name>
   ```

3. **Update README**: Add the new command to `.agents/commands/README.md`

## Command Creation Workflow

### Step 1: Create Command File

Run `scripts/create_command.py` with the command name:

```bash
python3 scripts/create_command.py my-new-command
```

This creates a command file at `.agents/commands/my-new-command.md` following the standard template. The command will reference a workflow file at `.devagent/core/workflows/my-new-command.md` by default.

**Specify a different workflow**:
```bash
python3 scripts/create_command.py my-command --workflow different-workflow
```

### Step 2: Create Symlink

Run `scripts/create_symlink.py` to create the symlink:

```bash
python3 scripts/create_symlink.py my-new-command
```

This creates a symlink from `.cursor/commands/my-new-command.md` to `.agents/commands/my-new-command.md`, making the command available in Cursor IDE.

### Step 3: Update Documentation

Manually add the new command to `.agents/commands/README.md` in the "Available Commands" section.

## Command Structure

Commands follow a standardized structure that functions as a snippet template. See `references/command-structure.md` for complete details. The template includes:

- Command title (Title Case with "(Command)" suffix)
- Instructions section (can include workflow-specific guidance about required inputs)
- Workflow reference to `.devagent/core/workflows/[workflow-name].md`
- Input Context placeholder (simple, single placeholder area for user input)

Since commands are snippets that get inserted into chat, keep the structure simple:
- Provide workflow-specific guidance in the Instructions section
- Use a single "Input Context:" placeholder for user input
- Avoid complex multi-field forms; explain in instructions what information is needed

The command template is available in `assets/command-template.md` for reference.

## Naming Conventions

- **Format**: Kebab-case (lowercase with hyphens)
- **Examples**: `create-plan.md`, `research.md`, `clarify-feature.md`
- **Avoid**: Generic names like `help.md` or `test.md`

## Validation

Before completing command creation, verify:

- [ ] Command file exists in `.agents/commands/[command-name].md`
- [ ] Command structure matches workflow requirements (use template as starting point, keep snippet-friendly)
- [ ] Workflow file is referenced correctly
- [ ] Instructions clearly guide agent and explain required inputs
- [ ] Input placeholder is simple and easy to fill in (commands are snippets)
- [ ] Symlink exists in `.cursor/commands/[command-name].md`
- [ ] Command is listed in `.agents/commands/README.md`

## Resources

### Scripts

- **`scripts/create_command.py`**: Creates a new command file in `.agents/commands/` following the standard template
- **`scripts/create_symlink.py`**: Creates a symlink from `.cursor/commands/` to `.agents/commands/`

### References

- **`references/command-structure.md`**: Complete reference documentation for command structure, naming conventions, and integration requirements

### Assets

- **`assets/command-template.md`**: Template file for command structure (used by create_command.py)
