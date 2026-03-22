---
name: "aelfscan-skill"
description: "AelfScan explorer data retrieval and analytics skill for agents."
---

# AelfScan Skill

## When to use
- Use this skill when you need AelfScan explorer search and analytics data retrieval tasks.

## Capabilities
- Domain coverage: search, blockchain, address, token, NFT, statistics
- Single tool descriptor source for SDK/CLI/MCP/OpenClaw
- MCP output governance controls and standardized trace-aware errors
- Supports SDK, CLI, MCP, and OpenClaw integration from one codebase.

## Safe usage rules
- Never print private keys, mnemonics, or tokens in channel outputs.
- This skill is read-only; do not attempt to execute chain writes via this package.
- If user intent requires writes, route to wallet + domain write skills and keep this skill for analytics.

## Command recipes
- Start MCP server: `bun run mcp`
- Run CLI entry: `bun run cli`
- Generate OpenClaw config: `bun run build:openclaw`
- Verify OpenClaw config: `bun run build:openclaw:check`
- Run CI coverage gate: `bun run test:coverage:ci`

## Limits / Non-goals
- This skill focuses on domain operations and adapters; it is not a full wallet custody system.
- It does not consume signer context for transaction signing.
- Do not hardcode environment secrets in source code or docs.
- Avoid bypassing validation for external service calls.
