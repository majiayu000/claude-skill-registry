---
name: setup-nx-mcp
description: Setup Nx MCP server for current Nx workspace. Use when user wants to add nx-mcp to their Nx monorepo project.
allowed-tools: Bash, Read, AskUserQuestion
---

## Setup Nx MCP

Configure the Nx MCP server for the current workspace.

### Steps

1. **Verify Nx workspace**: Check if `nx.json` exists in the current directory
   - If not found, stop and inform user this is not an Nx workspace

2. **Check existing configuration**: Run `claude mcp list` to check if nx-mcp is already configured
   - If already configured, inform user and ask if they want to reconfigure

3. **Determine scope**: Ask user which scope to use
   - `project` (default) — creates `.mcp.json`, shareable via git
   - `user` — global, available in all projects

4. **Install nx-mcp**:
   - Project scope: `claude mcp add --scope project nx-mcp -- npx nx-mcp@latest`
   - User scope: `claude mcp add --scope user nx-mcp -- npx nx-mcp@latest`

5. **Verify installation**: Run `claude mcp list` to confirm nx-mcp appears

6. **Optional - Nx AI init**: Ask user if they want to run `npx nx configure-ai-agents` to generate `CLAUDE.md` and `AGENTS.md`

### Prerequisites

- Current directory must be an Nx workspace (has `nx.json`)
- `npx` must be available
