---
name: delegation-autopilot
description: In Codex interactive mode, call delegate_autopilot automatically for multi-step or cross-cutting requests (including research-only), otherwise work normally.
delegator_exclude: true
---

# Delegation autopilot (parent-agent only)

This skill is meant for the **parent** Codex agent in interactive mode.

## Prerequisites (avoid common first-run failures)

Delegated runs can take minutes. If tool calls fail around ~60s with an error like `timed out awaiting tools/call after 60s`, increase the MCP tool timeout for this server in `${CODEX_HOME:-~/.codex}/config.toml`:

```toml
[mcp_servers.codex-specialized-subagents]
tool_timeout_sec = 600
```

## When to call `delegate_autopilot`
- The user request is **multi-step** ("and", "then", "also", "plus") or touches **multiple areas** (code + tests + docs).
- The change is **cross-cutting** (multiple files/modules) or likely needs **specialist** attention (security/perf/research).
- The user explicitly asks to delegate / use subagents.

**Default rules:**
- If the request includes **code changes** *and* (tests or docs), call `delegate_autopilot` **before** running shell commands or editing files.
- If the request is **multi-step research-only** and you want consistent “scan/implement/verify” decomposition or per-job `thinking_level` behavior, call `delegate_autopilot` with `sandbox="read-only"`.

## When not to call
- The user is asking a **simple question** or wants a short explanation.
- The change is **tiny and local** (single file, trivial edit) and you can do it directly.

## How to call (minimal)
Call MCP tool `delegate_autopilot` with:
- `task`: the user request (verbatim)
- `cwd`: current workspace directory (optional; defaults are OK)

Optional knobs:
- `sandbox`: use `"workspace-write"` when you want subagents to edit files; `"read-only"` for analysis-only delegation; avoid `"danger-full-access"` unless absolutely necessary.
- `max_agents`: default `3` (use `1` when you want a single subagent run).
- `skills_mode`: default `"auto"` (use `"none"` to disable skill selection).

## After calling
- If `structuredContent.decision.should_delegate` is `false`: continue normally without delegation.
- Otherwise: use `structuredContent.aggregate` as the consolidated result, and inspect `structuredContent.run_dir` for artifacts.

## If you choose `delegate_run` anyway

- If you need higher/lower reasoning for a one-off run, pass `reasoning_effort` (or a `model_reasoning_effort=...` entry in `config_overrides`).
- If you want a default for manual runs, set `CODEX_DELEGATE_REASONING_EFFORT` on the MCP server process.

## Safety
- Never paste secrets from `${CODEX_HOME:-~/.codex}` or any local config.
- Avoid pasting full `codex mcp list` output or entire config files; redact anything that looks like a token/key.
- Do not recurse: delegated subagents must not call any `delegate_*` tools.
