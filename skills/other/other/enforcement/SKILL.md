---
name: enforcement
description: "Use when implementing hooks that BLOCK invalid actions, creating quality gates for state transitions, or enforcing tested:true verification. Load when designing enforcement mechanisms. Uses exit code 2 to block, JSON permissionDecision:deny, or updatedInput modification. Rules are instructions; hooks are enforcement."
keywords: hooks, blocking, quality-gates, verification, exit-code-2, deny
---

# Enforcement

Runtime mechanisms that block invalid actions.

## Core Principle

> "Rules are instructions, not enforcements. Systems need verification gates, not more documentation."

## Instructions

1. Identify what needs enforcement (not just documentation)
2. Choose hook timing: PreToolUse, PermissionRequest, SubagentStop
3. Implement blocking logic: `scripts/block-*.sh`
4. Test with invalid action → verify block

## Blocking Mechanisms

| Mechanism | How | Effect |
|-----------|-----|--------|
| Exit code 2 | `exit 2` + stderr | Blocks, feeds stderr to Claude |
| JSON deny | `"permissionDecision": "deny"` | Structured blocking |
| Stop block | `"decision": "block"` | Forces agent to continue |

## Hook Timing

| Event | Can Block? | Use Case |
|-------|------------|----------|
| PreToolUse | Yes | Validate before execution |
| PermissionRequest | Yes | Custom approval logic |
| SubagentStop | Yes | Force quality gates |
| PostToolUse | No | Feedback only |

## References

| File | Load When |
|------|-----------|
| references/blocking-hooks.md | Implementing hook mechanisms |
| references/quality-gates.md | Designing verification loops |
| references/hook-templates.md | Writing hook code |
| references/agent-harness-hooks.md | Agent-harness specific patterns |
| references/sandbox-runtime.md | OS-level MCP server isolation |
| references/sandbox-fast-path.md | Hybrid security (allowlist + sandbox for 2-3x speed) |
