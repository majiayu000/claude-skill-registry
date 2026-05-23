---
name: mcp-usage-orchestrator
description: Enforce calling mcp__sequential-thinking__sequentialthinking for every user request and verify configured MCP servers (via .mcp.json or MCP resource listing) to route tasks to the right MCP tools. Use for all tasks in this project, especially when selecting MCP tools, confirming installed MCP servers, orchestrating parallel MCP calls, or choosing between playwright-test and github-fetcher.
---

# MCP Usage Orchestrator

## Goal
Use sequential-thinking on every request and keep MCP tool usage aligned with the MCP servers configured in this repo.

## Mandatory Per-Task Steps
1. Call `mcp__sequential-thinking__sequentialthinking` at the start of every user request. Keep the thoughts concise and action-oriented, even for simple tasks.
2. If this conversation has not yet verified MCP configuration, read `.mcp.json` at the repo root and list the configured `mcpServers` keys. Re-check when the repo changes or the user mentions MCP setup.
   - If `.mcp.json` is missing or unclear, call `list_mcp_resources` to confirm reachable servers and note any gaps.
3. Use MCP tools that match the configured servers and the task intent. Prefer the most direct MCP tool for the job and avoid unnecessary calls.

## Tool Routing Heuristics
- Browser automation, UI flows, or Playwright tests: use `mcp__playwright-test__*`.
- Web page content retrieval: use `mcp__github-fetcher__*`.
- Independent tool calls that can run concurrently: use `multi_tool_use.parallel`.
- If a task requires an MCP server not in `.mcp.json`, say so and ask the user whether to install/configure it.

## Notes
- Keep the MCP inventory in working memory once checked; do not repeatedly read `.mcp.json` unless needed.
- If MCP configuration is missing or invalid, state the problem and proceed with non-MCP tools as appropriate.
