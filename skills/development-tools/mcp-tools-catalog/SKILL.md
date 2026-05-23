---
name: mcp-tools-catalog
description: Build docs/mcp-tools.md from the active MCP servers and available tool functions.
metadata:
  short-description: Generate MCP tool catalog
---

# MCP Tools Catalog

Create a project-local catalog of MCP tools at `docs/mcp-tools.md`.

## Core rules
- Use the runtime MCP tool list and enabled server list to generate the catalog.
- Draft in chat first; ask for one confirmation before writing any files.
- Do not edit other files.
- Exception: if `AGENTS.md` lacks a reference to `docs/mcp-tools.md`, include that update under the same confirmation.

## Steps
1) Run: `codex mcp list --json` to get enabled server names.
2) Use prompt-engineering to list the tool functions currently available **right now** using this exact prompt:

```
list the functions that is CURRENTLY  avalible to you **RIGHT NOW**, starting with the prefix `functions.mcp__`
after each function, provide a clear, concise, and informative overview of what each function is intended for
```

3) Map tool functions to `server:tool` names (e.g., `playwright:browser_click`).
4) Filter out any tools whose server is not enabled.
5) Build `docs/mcp-tools.md` using `assets/mcp-tools-template.md`.
6) If `AGENTS.md` lacks a reference to `docs/mcp-tools.md`, include that change in the draft summary.
7) Ask: "Reply CONFIRM to write docs/mcp-tools.md and update AGENTS.md (if needed)."
8) On confirmation, write the file and update `AGENTS.md` if missing the reference.

## Output requirements
- Use `server:tool` naming per line.
- Include a short description for each tool.
- Include a list of enabled servers at the top.
