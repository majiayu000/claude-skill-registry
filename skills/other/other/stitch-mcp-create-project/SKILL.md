---
name: stitch-mcp-create-project
description: Creates a new Stitch project container (a design workspace). Call this when starting a new design session to get a projectId for screen generation.
allowed-tools:
  - "stitch*:*"
---

# Stitch MCP — Create Project

Creates a new Stitch project. A project is a container that holds one or more generated screens. You need a projectId before you can call `generate_screen_from_text`.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch"** in their request. Never trigger Stitch operations silently during regular conversation.

## When to use

- Starting a new design task or app concept
- The user says "create a Stitch project", "start a new project in Stitch", "design X using Stitch"
- You need a `projectId` before calling `generate_screen_from_text`
- Starting work in a new domain (keep related screens in one project)

## Step 1: Extract a meaningful title

Infer a descriptive project title from the user's request:

| User says | → title |
|-----------|---------|
| "Design a pet adoption app" | `"PawPals"` or `"Pet Adoption App"` |
| "Make a login page" | `"Login Page"` |
| "SaaS dashboard for analytics" | `"Analytics Dashboard"` |
| "E-commerce product listing" | `"Product Listing"` |

If no clear name is evident, use a descriptive label: `"Design Project [date]"`.

## Step 2: Call the MCP tool

```json
{
  "name": "create_project",
  "arguments": {
    "title": "[Descriptive project title]"
  }
}
```

## Step 3: Extract and store the project ID — CRITICAL

The tool returns a `name` field in the format `projects/NUMERIC_ID`. You must extract the numeric portion:

**Tool response:**
```json
{
  "name": "projects/3780309359108792857",
  "title": "Analytics Dashboard"
}
```

**Extract:**
- **Full name:** `projects/3780309359108792857` → use for `list_screens`, `get_project`
- **Numeric ID:** `3780309359108792857` → use for `generate_screen_from_text`, `get_screen`

Store both values. Announce to the user:
> "Created project **'Analytics Dashboard'** (ID: `3780309359108792857`). Ready to generate screens."

## ID format rules (critical — different tools need different formats)

| Tool | ID format required |
|------|-------------------|
| `generate_screen_from_text` | Numeric only: `3780309359108792857` |
| `get_screen` | Numeric only: `3780309359108792857` |
| `list_screens` | Full path: `projects/3780309359108792857` |
| `get_project` | Full path: `projects/3780309359108792857` |

## Integration

After creating a project, the next step is always `stitch-mcp-generate-screen-from-text` to generate the first screen.
