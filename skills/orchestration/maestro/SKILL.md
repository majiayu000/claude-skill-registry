---
name: maestro
description: "Maestro spec-driven development for Gemini CLI. Use when running /maestro* commands or orchestrating tracks; keep LeIndex as the analysis engine and avoid legacy TLDR routing."
---

# Maestro in Gemini CLI

You are operating Maestro inside Gemini CLI. Keep everything native:

- **Commands:** `/maestro`, `/maestro:setup`, `/maestro:newTrack`, `/maestro:implement`, `/maestro:orchestrate`, `/maestro:status`, `/maestro:revert`, `/maestro:leindex`, `/maestro:tui`.
- **Where commands come from:** `~/.gemini/commands/maestro/*.toml` (installed by the Maestro wizard).
- **MCP:** `mcpServers.leindex` → `{ command: "maestro", args: ["mcp", "tool-search"] }` (stdio). Do **not** route to `maestro.tldr` or any archive/tldr paths.
- **Skill location:** `~/.gemini/skills/maestro/` (this skill). Load it whenever a Maestro workflow is requested.

## Quick flow
1) `/maestro setup` — initialize/refresh product, tech stack, workflow, track registry.
2) `/maestro newTrack "<goal>"` — generate spec + plan with clarifying questions.
3) `/maestro implement <track>` — execute plan; rely on LeIndex 5-phase analysis for file scoping.
4) `/maestro orchestrate` — cockpit/orchestrator panel (Rust TUI pane).
5) `/maestro status` — surface phase/task progress and blockers.
6) `/maestro revert [track|phase|task]` — controlled rollback.
7) `/maestro leindex` — LeIndex-first analysis; no TLDR imports.
8) `/maestro tui` — launch Rust cockpit (primary TUI; Go/Python TUIs are deprecated).

## Guardrails
- Avoid `maestro.tldr` and anything under `maestro/archive/tldr`; these are reference-only.
- Keep token usage lean by constraining file scopes via LeIndex queries.
- Respect installed MCP config; if LeIndex is missing, request `/maestro:configure` rerun.
- Do not introduce cross-tool paths (no `~/.claude`, `~/.config/opencode`, etc.).

## Validation checklist
- `~/.gemini/commands/maestro/*.toml` are present and reference `__MAESTRO_HOME__`-substituted paths.
- `~/.gemini/settings.json` contains `mcpServers.leindex` pointing to `maestro mcp tool-search`.
- Skill lives at `~/.gemini/skills/maestro/`.
