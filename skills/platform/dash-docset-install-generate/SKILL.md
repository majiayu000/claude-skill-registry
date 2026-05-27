---
name: dash-docset-install-generate
description: Install, guide installation, and generate Dash.app docsets or cheatsheets on macOS. Use when the user asks to add missing Dash docsets, install from built-in or contributed sources, install cheat sheets, subscribe to feeds, or generate custom docsets and then verify installation.
---

# Dash Install and Generate

## Overview

Use this skill for install and generation workflows after discovery from `$dash-docset-search` or direct user request.

Defaults:

- confirmation-first installs
- no silent installation
- hybrid generation: automate known CLI paths, otherwise guide manual Dash generator steps

Use `references/dash_url_and_service.md`, `references/dash_http_api.md`, and `references/dash_mcp_tools.md` during execution.

## Automation Prompting

- Codex App automation fit: Guarded. Install and generation flows can require user approval or UI-level interaction.
- Codex CLI automation fit: Guarded. Prefer dry-run or planning mode unless explicit install approval is provided.
- Use `references/automation-prompts.md` for Codex App and Codex CLI templates with placeholders and stop conditions.
- Default automation behavior should be non-destructive unless install mode is explicitly approved.

## Install Workflow

### 1) Resolve candidate

1. Match request against catalog snapshots:
   - `uv run python scripts/dash_catalog_match.py --query "<text>"`
2. Prefer in this order:
   - built-in Dash Downloads
   - user-contributed
   - cheatsheet
   - generation path

### 2) Perform install (confirmation-first)

Preferred automation path:

- `uv run python scripts/dash_url_install.py --repo-name "<repo>" --entry-name "<entry>"`
- add `--version "<version>"` when explicit version is required
- use `--yes` only when explicit user approval exists

If URL install details are ambiguous:

- switch to guide mode
- provide exact Dash UI path in Settings > Downloads

### 3) Verify install

Use this order:

1. Dash MCP `list_installed_docsets`
2. local HTTP `/docsets/list` (after `scripts/dash_api_probe.py`)
3. if API unavailable, ask user to confirm from Dash UI

## Generation Workflow (Hybrid)

### 1) Decide automation vs guide

Automate only when there is a documented and stable toolchain for the target source.

Typical examples:

- Sphinx/PyDoctor via docset tooling
- Javadoc pipelines
- GoDoc/Rust/Scaladoc/HexDoc toolchains
- cheat sheet authoring via cheatset

If the path is unclear or brittle:

- guide through Dash Docset Generator and official docs

### 2) Generation sources to cover

- Swift packages
- Ruby gems
- Python/Sphinx docs
- PHP packages
- Java packages
- Go packages
- Rust crates
- Scala packages
- Dart packages
- Haskell packages
- Hex packages
- Clojure libraries
- generic HTML docs

### 3) Last-resort generation

Suggest GitHub-based or Stack Overflow-based generation only when built-in, contributed, and known generator paths are exhausted.

## API and Service Fallbacks

If MCP is unavailable:

1. run `uv run python scripts/dash_api_probe.py`
2. use local HTTP API if healthy
3. otherwise provide:
   - AppleScript `open location "dash://?query=..."`
   - terminal `open "dash://?query=..."`
   - macOS `Look Up in Dash` service guidance

## Scripts

- `scripts/dash_api_probe.py`
- `scripts/dash_catalog_refresh.py`
- `scripts/dash_catalog_match.py`
- `scripts/dash_url_search.py`
- `scripts/dash_url_install.py`

## References

- `references/dash_mcp_tools.md`
- `references/dash_http_api.md`
- `references/dash_url_and_service.md`
- `references/automation-prompts.md`
- `references/catalog_built_in_docsets.json`
- `references/catalog_user_contrib_docsets.json`
- `references/catalog_cheatsheets.json`

## Optional Visual Troubleshooting

If Dash interface behavior needs verification, use the `$screenshot` skill if it is available in the user's environment.
