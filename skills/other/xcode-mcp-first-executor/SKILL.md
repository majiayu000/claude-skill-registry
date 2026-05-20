---
name: xcode-mcp-first-executor
description: Execute Apple and Swift tasks through Xcode MCP tools first, with strict workspacePath-based tab resolution and structured fallback handoff when MCP tools are unavailable, time out, or cannot satisfy the requested operation.
---

# Xcode MCP First Executor

Use this skill when a task can be performed through Xcode MCP.

## Core Rules

- Resolve target workspace by `workspacePath` from `XcodeListWindows`.
- Do not trust stale tab index assumptions.
- Use MCP tools first for supported actions.
- If MCP fails after retry policy, output structured handoff to `$apple-swift-cli-fallback`.

## Workflow

1. Resolve active tab:
- call `XcodeListWindows`
- pick tab by matching `workspacePath`

2. Execute via MCP matrix:
- use `references/mcp-tool-matrix.md`

3. Retry on transient MCP failures:
- one immediate retry for timeout or transport error
- if still failing, generate fallback handoff payload

4. Handoff payload:
- include intent category
- include preferred official CLI command(s)
- include reason MCP path failed

## Mutation Note

For mutation requests in Xcode-managed scope, continue through MCP mutation tools if available. If falling back to direct filesystem edits, route to `$apple-dev-safety-and-docs` first.

## References

- `references/mcp-tool-matrix.md`
- `references/mcp-failure-handoff.md`
- `references/mutation-via-mcp.md`
