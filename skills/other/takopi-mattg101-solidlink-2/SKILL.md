---
name: takopi
description: Use when working through Takopi (Telegram bridge) to route Codex tasks by project, branch worktree, or topic; covers directives like /project, @branch, engine prefixes, ctx footer behavior, and /new resets.
---
# Takopi Context

Use this skill when a request is issued from Takopi or when you need to format guidance for Takopi messages. Keep replies short and compatible with Telegram usage.

## Core Behaviors

- Directives live at the start of the first line: `/project`, `/engine`, and `@branch`.
- Replying to a message that includes a backticked `ctx:` footer keeps the same project/branch; do not restate directives unless asked.
- `@branch` runs in a dedicated git worktree for that branch.

## Quick Patterns

```text
/project task text
/project @branch task text
/engine /project @branch task text
```

Examples:

```text
/solidlink @feat/branch-name update docs
/solidlink fix build warnings
```

## File Operations

When asking the user to download files via Takopi's `/file get` command:
- Use **relative paths** from the current working directory (project root).
- Avoid absolute paths (e.g., `C:\...`) as they are rejected by the harness.
- If a file is in a subdirectory, include the full relative path from the project root.

Examples:
```text
/file get SolidLink.UI/test-results/robot-definition-renders-robot-definition-panel/test-finished-1.png
/file get SolidLink.UI/test-results/viewport-shift-H-hides-sel-3bc76-es-and-updates-bridge-state/video.webm
/file get docs/dev/orchestration/feature-spec__feat-example.md
```

When generating `/file get` commands for test artifacts:
1. Run tests first to generate artifacts
2. Use `find` or `ls` to locate artifact paths
3. Format as relative paths from project root in code blocks

## Topics (Telegram forums)

In topic threads, use `/topic` and `/ctx` to bind a project/branch context. Use `/new` to reset stored session context.

## References

See `references/takopi-context.md` for the concise rules and command list.
