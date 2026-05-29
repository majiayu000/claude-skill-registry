---
name: stitch-mcp-list-projects
description: Lists all Stitch projects accessible to the user. Use this to find an existing project ID before resuming work or generating new screens in an existing project.
allowed-tools:
  - "stitch*:*"
---

# Stitch MCP — List Projects

Lists Stitch projects available to the user. Use this when you need to find an existing projectId rather than creating a new project.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch".**

## When to use

- User says "continue working on my Stitch project" without providing an ID
- User says "list my Stitch projects" or "what projects do I have?"
- You need to find an existing projectId before calling `generate_screen_from_text`
- Checking whether a project already exists before creating a new one

## Call the MCP tool

**To list owned projects (default):**
```json
{
  "name": "list_projects",
  "arguments": {
    "filter": "view=owned"
  }
}
```

**To list projects shared with the user:**
```json
{
  "name": "list_projects",
  "arguments": {
    "filter": "view=shared"
  }
}
```

**To list all accessible projects (owned + shared):**
```json
{
  "name": "list_projects",
  "arguments": {}
}
```

## Output schema

```json
{
  "projects": [
    {
      "name": "projects/3780309359108792857",
      "title": "Analytics Dashboard",
      "updateTime": "2024-11-15T10:30:00Z"
    }
  ]
}
```

## After listing

1. Present the project list to the user with titles and last-updated timestamps
2. Ask which project to work in (if multiple)
3. Extract the numeric ID from the chosen `name` field: `projects/ID` → `ID`
4. Store both the full name and numeric ID for subsequent calls

## ID format reminder

- `list_screens`, `get_project` → use `projects/NUMERIC_ID`
- `generate_screen_from_text`, `get_screen` → use `NUMERIC_ID` only
