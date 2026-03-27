---
name: ln-011-agent-installer
description: "Installs or updates Codex CLI, Gemini CLI, and Claude Code. Use when CLI agents need installation or update."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# Agent Installer

**Type:** L3 Worker
**Category:** 0XX Shared

Installs or updates CLI agents via npm and Claude CLI. Single pass per agent: install then immediately verify.

---

## Input / Output

| Direction | Content |
|-----------|----------|
| **Input** | OS info, `disabled` flags per agent, `dry_run` flag, optional `runId`, optional `summaryArtifactPath` |
| **Output** | Structured summary envelope with per-agent status: `installed` / `updated` / `skipped` / `disabled` / `failed` |

If `summaryArtifactPath` is provided, write the same summary JSON there. If not provided, return the summary inline and remain fully standalone.

---

## Agent Registry

| Agent | Install Command | Health Check |
|-------|----------------|---------------|
| Codex | `npm i -g @openai/codex` | `codex --version` |
| Gemini | `npm i -g @google/gemini-cli` | `gemini --version` |
| Claude | `claude update` | `claude --version` |

---

## Workflow

```
For each agent: Install → Verify → Record
```

### Phase 1: Install & Verify

For each agent in registry, apply first matching rule:

| Condition | Action | Report |
|-----------|--------|--------|
| `disabled: true` | SKIP | "disabled by user" |
| `dry_run: true` | Show planned command | "dry run" |
| npm agent | `npm install -g {pkg}` then `{cmd} --version` | version or error |
| Claude | `claude update` then `claude --version` | version or error |

**Single pass:** install and verify happen atomically per agent. No separate scan phase — the install result IS the state.

**Error handling:**

| Error | Detection | Response |
|-------|-----------|----------|
| npm not in PATH | `npm --version` fails | FAIL gracefully, report "npm not found in PATH" |
| Permission denied | stderr contains "EACCES" | FAIL, suggest `npm install -g --prefix ~/.local {pkg}` |
| Network error | stderr contains "ETIMEDOUT" or "ENETUNREACH" | FAIL, report "network error" |
| Unknown error | Any other non-zero exit | FAIL, include stderr |

**Output table:**

```
Agent Installation:
| Agent  | Action    | Version  | Status |
|--------|-----------|----------|--------|
| Codex  | installed | 0.1.2503 | ok     |
| Gemini | skipped   | -        | disabled by user |
| Claude | updated   | 1.0.30   | ok     |
```

---

## Critical Rules

1. **Never modify `disabled` flags.** Respect them, never change them
2. **Fail gracefully.** One agent failure does not block others
3. **Global install only.** Always `npm install -g` (CLI tools must be in PATH)
4. **No side effects.** Only npm global packages touched. No config files modified
5. **Idempotent.** Safe to run multiple times

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Separate check/install/verify phases | Single pass: install then verify |
| Retry failed installs automatically | One attempt, report failure |
| Use `sudo npm install` | Suggest `--prefix` for permission issues |
| Install agents marked `disabled` | Skip with clear report |

---

## Definition of Done

- [ ] All agents processed in single pass (install + verify)
- [ ] Disabled agents skipped with report
- [ ] Version verified immediately after each install
- [ ] Status table displayed

---

**Version:** 1.1.0
**Last Updated:** 2026-03-23
