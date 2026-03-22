---
name: ln-011-agent-installer
description: "Installs or updates Codex CLI, Gemini CLI, and Claude Code to latest versions. Use when CLI agents need installation or update."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# Agent Installer

**Type:** L3 Worker
**Category:** 0XX Shared

Installs or updates CLI agents (Codex, Gemini) via npm and updates Claude Code via its built-in command. Checks current state, performs install/update, verifies result.

---

## Input / Output

| Direction | Content |
|-----------|---------|
| **Input** | OS info, `disabled` flags per agent, `dry_run` flag |
| **Output** | Per-agent status: `installed` / `updated` / `skipped` / `disabled` / `failed` |

---

## Agent Registry

### npm Agents

| Agent | npm Package | Health Check |
|-------|-------------|--------------|
| Codex | `@openai/codex` | `codex --version` |
| Gemini | `@google/gemini-cli` | `gemini --version` |

### Claude CLI

| Agent | Update Command | Health Check |
|-------|---------------|--------------|
| Claude | `claude update` | `claude --version` |

---

## Workflow

```
Check Current State  -->  Install/Update  -->  Verify
```

### Phase 1: Check Current State

For each agent in the registry:

1. Run `{cmd} --version` to detect installed version (first line of output)
2. Build state table:

```
Current Agent State:
| Agent  | Installed | Version  |
|--------|-----------|----------|
| Codex  | yes       | 0.1.2503 |
| Gemini | no        | -        |
| Claude | yes       | 1.0.30   |
```

### Phase 2: Install/Update

**npm Agents** (Codex, Gemini) -- for each agent, apply the first matching rule:

| Condition | Action | Report |
|-----------|--------|--------|
| `disabled: true` | SKIP | "disabled by user" |
| `dry_run: true` | Show planned command | "dry run" |
| Any other state | `npm install -g {pkg}` | "installed/updated" |

**Claude CLI:**

| Condition | Action | Report |
|-----------|--------|--------|
| `disabled: true` | SKIP | "disabled by user" |
| `dry_run: true` | Show planned command | "dry run" |
| Any other state | `claude update` | "updated" |

**Error handling:**

| Error | Detection | Response |
|-------|-----------|----------|
| npm not in PATH | `npm --version` fails | FAIL gracefully, report "npm not found in PATH" |
| Permission denied | npm exit code + stderr contains "EACCES" | FAIL, suggest `npm install -g --prefix ~/.local {pkg}` |
| Network error | npm exit code + stderr contains "ETIMEDOUT" or "ENETUNREACH" | FAIL, report "network error - check connectivity" |
| Unknown error | Any other non-zero exit | FAIL, include stderr in report |

### Phase 3: Verify

1. Re-run `{cmd} --version` for each agent that was installed/updated
2. Confirm version output matches expected (non-empty, no error)
3. Display final report:

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

1. **Never modify `disabled` flags.** This skill respects them, never changes them
2. **Fail gracefully.** One agent failure does not block the other
3. **Global install only.** Always `npm install -g` (CLI tools must be in PATH)
4. **No side effects.** Only npm global packages are touched. No config files modified
5. **Idempotent.** Safe to run multiple times. `npm install -g` and `claude update` handle already-current versions gracefully

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Install without checking current state | Always check version first |
| Retry failed installs automatically | One attempt, report failure |
| Use `sudo npm install` | Suggest `--prefix` for permission issues |
| Install agents marked `disabled` | Skip with clear report |

---

## Definition of Done

- [ ] All agents checked (Codex, Gemini, Claude)
- [ ] Disabled agents skipped with report
- [ ] Install/update commands executed for eligible agents
- [ ] Version verified after install/update
- [ ] Final status table displayed

---

**Version:** 1.0.0
**Last Updated:** 2026-03-20
