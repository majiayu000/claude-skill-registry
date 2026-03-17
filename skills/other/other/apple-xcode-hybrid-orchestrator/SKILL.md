---
name: apple-xcode-hybrid-orchestrator
description: Orchestrate Apple and Swift development workflows with an Xcode MCP-first policy and automatic fallback to official Apple and Swift CLI tooling. Use when tasks involve Xcode, SwiftPM, build or test execution, toolchain checks, docs lookup, or mutation-risk decisions across mixed MCP and CLI environments.
---

# Apple Xcode Hybrid Orchestrator

Use this skill as the entrypoint for Apple and Swift tasks.

## Workflow

1. Classify intent:
- session/workspace
- read/search
- build/test/run
- packaging/toolchain
- docs lookup
- mutation request

2. Route execution:
- Use `$xcode-mcp-first-executor` first for anything supported by Xcode MCP.
- If MCP is unavailable, times out, or lacks needed capability, hand off to `$apple-swift-cli-fallback` immediately.

3. Apply docs policy:
- Use `$apple-dev-safety-and-docs` for Dash local-first docs routing and advisory cooldown handling.

4. Apply mutation safety:
- If request can touch Xcode-managed scope, use `$apple-dev-safety-and-docs` hard 2-step consent gate before any direct filesystem fallback.

## Required Policy

- Always prefer Xcode MCP when it can perform the action.
- Fallback to official tooling automatically when MCP path is blocked.
- On fallback, include concise MCP setup guidance only if cooldown allows.
- Never perform direct mutation in Xcode-managed scope unless safety policy conditions are satisfied.

## References

- `references/workflow-policy.md`
- `references/mcp-setup-advisory.md`
- `references/skills-discovery.md`

## Scripts

- `scripts/advisory_cooldown.py`
