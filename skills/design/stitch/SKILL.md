---
name: stitch
description: "Google Stitch UI design tool. Generate screens from text prompts, convert designs to React components, create DESIGN.md design systems. Use when: designing UI, generating screens, converting Stitch to code, creating design tokens. Keywords: stitch, design, UI, screen, generate, react, components, DESIGN.md, wireframe, prototype, mockup."
allowed-tools:
  - "stitch:*"
  - "Read"
  - "Write"
  - "Bash"
  - "WebFetch"
---

# Stitch UI Design Skill

Google Stitch MCP integration for AI-powered UI design generation.

## Workflows

### 1. Generate New Screen
```bash
mcp-cli call stitch/generate_screen_from_text '{"projectId": "ID", "prompt": "description", "deviceType": "DESKTOP"}'
```

### 2. Export to React
→ Invoke `react:components` skill after getting screen

### 3. Create Design System
→ Invoke `design-md` skill to generate DESIGN.md

## MCP Tools

| Tool | Parameters |
|------|------------|
| `stitch/list_projects` | filter: "view=owned" or "view=shared" |
| `stitch/create_project` | title: string |
| `stitch/get_project` | name: "projects/{id}" |
| `stitch/list_screens` | projectId: "projects/{id}" |
| `stitch/get_screen` | projectId, screenId |
| `stitch/generate_screen_from_text` | projectId, prompt, deviceType, modelId |

## Related Skills
- `design-md` - Extract design tokens → DESIGN.md
- `react:components` - Convert screens → React code
