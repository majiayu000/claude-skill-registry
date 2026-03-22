---
name: opencrow-utility-toolbox
description: Use the OpenCROW utility stack for shell-heavy CTF workflows. Use when Codex needs `jq`, `yq`, `xxd`, `tmux`, `screen`, `rg`, or `fzf` to glue a larger workflow together.
---

# OpenCROW Utility Toolbox

Use this skill when the blocker is shell ergonomics or structured-data processing rather than a challenge-specific exploit primitive. It covers the “glue” layer that makes larger CTF workflows faster: `jq`, `yq`, `xxd`, `tmux`, `screen`, `ripgrep`, `fzf`, `opencrow-autosetup`, and `opencrow-exploit`.

## Quick Start

Start the MCP server from the installed CLI:

```bash
opencrow-utility-mcp
```

Verify the mapped stack:

```bash
python ~/.codex/skills/opencrow-utility-toolbox/scripts/verify_toolkit.py
```

## Workflow

1. Start with the MCP server and call `toolbox_info`, `toolbox_verify`, and `toolbox_capabilities`.
2. Use `utility_search` first when a workspace is large and you need to narrow the problem before opening files manually.
3. Use `utility_json_query` or `utility_yaml_query` when configs, API responses, or challenge metadata need slicing before deeper analysis.
4. Use `utility_hexdump` when you need a fast bounded hex view of a file region.
5. Use `tmux` or `screen` when the task benefits from persistent panes or background sessions.
6. Use `opencrow-autosetup` to seed a standard challenge workspace with OpenCROW reconnaissance artifacts, maintain `HANDOFF.md`, and launch a reconnaissance-only Codex pass that selects the final category-specific `AGENTS.md`.
7. Use `opencrow-exploit` to launch the follow-up Codex solve pass from the `AGENTS.md` and `HANDOFF.md` artifacts created by autosetup.

## Resources

- `opencrow-utility-mcp`: stdio MCP server for typed workspace search, jq/yq queries, and xxd hexdumps.
- `scripts/verify_toolkit.py`: confirm that the mapped workflow helpers are installed.
- `references/tooling.md`: quick guidance for common shell utility choices.
