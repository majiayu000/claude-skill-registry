---
name: codex-setup
description: "Codex CLI 用の .codex/ と AGENTS.md を導入・更新する。Use when user mentions '/codex-setup', codex cli setup, codex config, or wants Codex CLI compatibility. Do NOT load for: opencode setup, harness init without codex, or MCP-only setup."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob"]
argument-hint: "[--with-mcp|--skip-mcp]"
disable-model-invocation: true
---

# Codex Setup Skill

Set up Codex CLI compatibility for the current project.

## Deliverables

- `.codex/skills/` - Harness skills for Codex
- `.codex/rules/` - Temporary guardrails
- `AGENTS.md` - Codex rules file
- Optional: `.codex/config.toml` (MCP template)

## Usage

```bash
/codex-setup
/codex-setup --with-mcp
/codex-setup --skip-mcp
```

## Execution Flow

1. Confirm user wants Codex CLI setup/update
2. Ask whether to copy MCP template (`--with-mcp`)
3. Run setup script
4. Verify files exist
5. Report completion + next steps

## Script Execution

Prefer running from plugin root:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/codex-setup-local.sh" --skip-mcp
```

If `CLAUDE_PLUGIN_ROOT` is unavailable, run from plugin repo root:

```bash
bash ./scripts/codex-setup-local.sh --skip-mcp
```

## Verification

```bash
ls -la .codex/skills
ls -la .codex/rules
ls -la AGENTS.md
```

## Completion Message

> Codex CLI setup complete.
>
> - `.codex/skills/` / `.codex/rules/` installed
> - `AGENTS.md` updated (backup created if existed)
> - Use `$plan-with-agent`, `$work`, `$harness-review` in Codex
