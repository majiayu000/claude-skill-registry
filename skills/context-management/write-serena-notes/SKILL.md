---
name: write-serena-notes
description: Write notes and documentation to Serena memory. Use this skill when you need to persist information like technical debt, architecture decisions, meeting notes, or any other documentation to the project's Serena memory.
---

# Serena Notes

## Overview

This skill provides the workflow and templates for writing notes to Serena memory. Serena is a semantic coding tool that stores project-related memories for future reference.

## Workflow

### Step 1: Activate the Project

**REQUIRED before any memory operation.** You must activate the Serena project first.

```bash
mcp-cli call plugin_serena_serena/activate_project '{"project": "dssk-multichannel-gui"}'
```

**Schema:**
```json
{
  "project": "string (required) - The project name to activate"
}
```

### Step 2: Write the Memory

After activation, write the note using `write_memory`:

```bash
mcp-cli call plugin_serena_serena/write_memory '{"memory_file_name": "your-note-name", "content": "Your content here..."}'
```

**Schema:**
```json
{
  "memory_file_name": "string (required) - Filename without extension, use kebab-case",
  "content": "string (required) - The markdown content of the note"
}
```

### Step 3: Verify (Optional)

List memories to confirm the note was created:

```bash
mcp-cli call plugin_serena_serena/list_memories '{}'
```

Or read the specific note:

```bash
mcp-cli call plugin_serena_serena/read_memory '{"memory_file_name": "your-note-name"}'
```

## Templates

Use the appropriate template from the `templates/` directory based on your note type:

| Template | Use When |
|----------|----------|
| `technical-debt.md` | Documenting code that needs future improvement |

## Common Errors

### "No active project"

**Cause:** Forgot to activate the project first.
**Fix:** Run `activate_project` before `write_memory`.

### Invalid parameter name

**Cause:** Using wrong parameter names (e.g., `project_name` instead of `project`).
**Fix:** Use exact parameter names from schemas above.

## Resources

### templates/

Markdown templates for different types of notes. Copy and fill in the placeholders.
