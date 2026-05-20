---
name: tool-selection
description: "CLI-first tool selection policy for Claude Code. Use when choosing between CLI tools and MCP servers, designing new agents, or reviewing agent tool configurations. Do NOT use for executing commands or running tools -- this is for tool selection decisions during agent/config design only."
durability: encoded-preference
---

# Tool Selection Policy

## CLI-First Principle

Prefer CLI tools over MCP servers when a CLI equivalent exists. CLI tools are more token-efficient and avoid MCP server startup overhead.

| Tool Need | CLI (Preferred) | MCP (When CLI Insufficient) |
|-----------|----------------|----------------------------|
| Screenshots & screen analysis | `peekaboo` CLI via Bash | N/A (removed) |
| Web research | WebSearch, WebFetch (built-in) | N/A |
| Library API docs | See web-research skill | context7 MCP (see web-research skill) |
| Interactive browser control | N/A | Playwright MCP |
| E2E testing | Playwright CLI (`npx playwright test`) | N/A |
| Slack communication | N/A | Slack MCP (no CLI substitute) |
| Confluence wiki | N/A | Confluence MCP (no CLI substitute) |

## Playwright MCP vs CLI

**Use Playwright MCP** (`mcp__playwright__*`) ONLY for:
- Interactive browser inspection (snapshots, clicking, form filling)
- Live debugging of web pages
- Visual verification requiring human-in-the-loop

**Use Playwright CLI** for:
- E2E test execution (`npx playwright test`)
- Test report generation
- CI/CD pipeline testing

## Playwright MCP Output Management

The `.playwright-mcp/` directory in the project root is gitignored. All Playwright MCP artifacts belong there.

- **Screenshots**: Use `.playwright-mcp/` prefix in the filename parameter (e.g., `.playwright-mcp/screenshot.png`). Without a filename, screenshots go to `.playwright-mcp/` automatically via `--output-dir`. With a filename, the path is resolved relative to cwd, so the prefix is required
- **Cleanup**: Delete `.playwright-mcp/` when Playwright MCP work is complete for the session
- **Never commit**: `.playwright-mcp/` is gitignored

## MCP Graceful Degradation

If an MCP server is unavailable, do not fail the workflow. Fall back to CLI alternatives or skip the MCP-dependent step with a note to the user.

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|-------------|------------------|
| Using MCP when CLI exists | Use CLI — lower token cost, no server overhead |
| Adding MCP tools to agent frontmatter when CLI works | Use Bash tool with CLI commands |
| Proposing new MCP servers without CLI evaluation | Always check for CLI alternative first |
