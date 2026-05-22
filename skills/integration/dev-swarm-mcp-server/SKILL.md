---
name: dev-swarm-mcp-server
description: Add and manage Model Context Protocol (MCP) servers for AI agents, including transports, scopes, and config files. Use when extending agent capabilities with new tools or data sources.
---

# AI Builder - MCP Server Management

This skill assists in adding MCP servers to CLI AI agents (Claude, Codex, Gemini, etc.) with the correct transport, scope, and configuration locations.

## When to Use This Skill

- User wants to add new MCP server to extend agent capabilities
- User needs to list installed MCP servers
- User wants to integrate new tools or data sources through MCP
- User asks to configure MCP servers for different AI agents
- User needs help choosing transport types or config scopes

## Your Roles in This Skill

- **DevOps Engineer**: Install and configure MCP servers for CLI AI agents, manage configuration files, and validate connectivity.
- **Technical Writer**: Provide clear, accurate instructions and examples for MCP setup across tools and scopes.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.

## Instructions

Follow these steps in order:

### Step 1: Detect the AI Agent Type

- Identify the current CLI agent (Claude Code, Codex CLI, Gemini CLI, or other).
- If Claude Code, refer to `references/mcp-server-claude.md`.
- If Codex CLI, refer to `references/mcp-server-codex.md`.
- If Gemini CLI, refer to `references/mcp-server-gemini.md`.
- If other, refer to `references/mcp-server-other-cli.md`.

### Step 2: Confirm Requirements

- Confirm transport type (stdio, HTTP, SSE), scope (project/user), and any required environment variables.
- For general guidance, refer to `references/mcp-server-general.md`.

### Step 3: Inspect Existing Configuration

- Run the CLI list command to verify whether the server already exists.
- If a server already exists, confirm whether to update, remove, or leave it.

### Step 4: Configure the MCP Server

- Use the correct CLI command and flags for the chosen transport and scope.
- If configuration is file-based, update the correct file location.
- If adding a server outside the project scope (user/global), use absolute paths for scripts and config files to avoid launch failures.
- Keep sensitive values in environment variables, not committed files.

### Step 5: Validate and Restart

- Re-run the list command to confirm the server appears.
- Instruct the user to restart the CLI so changes take effect.
- If the server has a long startup time, set or recommend timeout options.

## Best Practices

1. **Check installation first**: Always verify existing MCP servers before changing configurations.
2. **Use project scope for team tools**: Commit shared configs only when they contain no secrets.
3. **Keep secrets out of VCS**: Use environment variables for API keys and tokens.
4. **Restart after changes**: Always exit and relaunch the CLI after config updates.
5. **Validate connectivity**: Confirm servers appear in list output and respond to basic requests.
