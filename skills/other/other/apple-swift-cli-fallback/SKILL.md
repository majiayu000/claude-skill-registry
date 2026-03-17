---
name: apple-swift-cli-fallback
description: Execute automatic fallback through official Apple and Swift CLI tooling when Xcode MCP paths are unavailable or insufficient. Use for xcodebuild, xcrun, SwiftPM, swiftly toolchain workflows, and command-availability or allowlist remediation guidance.
---

# Apple Swift CLI Fallback

Use this skill when MCP-first execution cannot complete the requested task.

## Core Rules

- Fallback must be automatic and use official tooling.
- Keep fallback commands explicit and reproducible.
- Include concise MCP advisory only if cooldown allows.
- If CLI command is unavailable or blocked, provide `~/.codex/rules` allowlist guidance.

## Workflow

1. Receive handoff from `$xcode-mcp-first-executor` or detect MCP unavailability.
2. Select official command path from `references/cli-fallback-matrix.md`.
3. Execute fallback command.
4. Check advisory cooldown via `scripts/advisory_cooldown.py`.
5. If eligible, include short MCP setup benefit note.
6. If command blocked/missing, provide minimal allowlist and setup actions.

## Toolchain Policy

- Prefer `swiftly` when available.
- Otherwise use official Xcode toolchain and CLT guidance from `references/toolchain-management.md`.

## References

- `references/cli-fallback-matrix.md`
- `references/toolchain-management.md`
- `references/allowlist-guidance.md`

## Scripts

- `scripts/advisory_cooldown.py`
