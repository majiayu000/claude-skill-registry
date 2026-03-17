---
name: use-mcp
version: 1.0.0
description: '[AI & Tools] Utilize tools of Model Context Protocol (MCP) servers'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Utilize MCP (Model Context Protocol) server tools to extend Claude's capabilities.

**Workflow:**
1. **Discover** -- List available MCP tools and their capabilities
2. **Select** -- Choose appropriate tool for the task
3. **Execute** -- Run MCP tool with correct parameters

**Key Rules:**
- Check available MCP servers before attempting to use tools
- Use MCP tools for capabilities not available in built-in tools
- Handle MCP tool errors gracefully with fallback approaches

Execute MCP operations via **Gemini CLI** to preserve context budget.

## Execution Steps

1. **Execute task via Gemini CLI** (using stdin pipe for MCP support):

    ```bash
    # IMPORTANT: Use stdin piping, NOT -p flag (deprecated, skips MCP init)
    echo "$ARGUMENTS. Return JSON only per GEMINI.md instructions." | gemini -y -m gemini-2.5-flash
    ```

2. **Fallback to mcp-manager subagent** (if Gemini CLI unavailable):
    - Use `mcp-manager` subagent to discover and execute tools
    - If the subagent got issues with the scripts of `mcp-management` skill, use `mcp-builder` skill to fix them
    - **DO NOT** create ANY new scripts
    - The subagent can only use MCP tools if any to achieve this task
    - If the subagent can't find any suitable tools, just report it back to the main agent to move on to the next step

## Important Notes

- **MUST use stdin piping** - the deprecated `-p` flag skips MCP initialization
- Use `-y` flag to auto-approve tool execution
- **GEMINI.md auto-loaded**: Gemini CLI automatically loads `GEMINI.md` from project root, enforcing JSON-only response format
- **Parseable output**: Responses are structured JSON: `{"server":"name","tool":"name","success":true,"result":<data>,"error":null}`

## Anti-Pattern (DO NOT USE)

```bash
# BROKEN - deprecated -p flag skips MCP server connections!
gemini -y -m gemini-2.5-flash -p "..."
```

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
