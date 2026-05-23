---
name: omc
description: oh-my-claudecode — Teams-first multi-agent orchestration layer for Claude Code. 32 specialized agents, smart model routing, persistent execution loops, and real-time HUD visibility. Zero learning curve.
allowed-tools: Read Write Bash Grep Glob Edit
metadata:
  tags: omc, oh-my-claudecode, claude-code, multi-agent, orchestration, team, autopilot, ralph, ultrawork
  platforms: Claude Code
  keyword: omc
  version: 4.2.15
  source: Yeachan-Heo/oh-my-claudecode
---


# omc (oh-my-claudecode) — Claude Code Multi-Agent Orchestration

## When to use this skill

- You want Teams-first multi-agent orchestration inside Claude Code
- You need 32 specialized agents with smart model routing (Haiku → Opus)
- Complex tasks that benefit from parallel agent execution with verification loops
- Any Claude Code workflow that needs persistent, guaranteed-completion execution

---

## 1. Installation (3 Steps)

**Step 1: Install plugin**
```bash
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode
```

**Step 2: Run setup**
```bash
/omc:omc-setup
```

**Step 3: Build something**
```text
autopilot: build a REST API for managing tasks
```

> **npm alternative**: `npm install -g oh-my-claude-sisyphus`

---

## 2. Orchestration Modes

| Mode | What it is | Use For |
|------|-----------|---------|
| **Team** (recommended) | Staged pipeline: `team-plan → team-prd → team-exec → team-verify → team-fix` | Coordinated agents on shared task list |
| **Autopilot** | Autonomous single lead agent | End-to-end feature work with minimal ceremony |
| **Ultrawork** | Maximum parallelism (non-team) | Burst parallel fixes/refactors |
| **Ralph** | Persistent mode with verify/fix loops | Tasks that must complete fully |
| **Pipeline** | Sequential staged processing | Multi-step transformations |
| **Swarm/Ultrapilot** | Legacy facades → route to Team | Existing workflows |

Enable Claude Code native teams in `~/.claude/settings.json`:
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

---

## 3. Magic Keywords

| Keyword | Effect | Example |
|---------|--------|---------|
| `team` | Canonical Team orchestration | `/omc:team 3:executor "fix all TypeScript errors"` |
| `autopilot` | Full autonomous execution | `autopilot: build a todo app` |
| `ralph` | Persistence mode | `ralph: refactor auth` |
| `ulw` | Maximum parallelism | `ulw fix all errors` |
| `plan` | Planning interview | `plan the API` |
| `ralplan` | Iterative planning consensus | `ralplan this feature` |
| `swarm` | Legacy (routes to Team) | `swarm 5 agents: fix lint errors` |
| `ultrapilot` | Legacy (routes to Team) | `ultrapilot: build a fullstack app` |

> **Note**: `ralph` includes ultrawork — activating ralph mode automatically includes ultrawork's parallel execution.

---

## 4. Team Mode (Canonical)

```bash
/omc:team 3:executor "fix all TypeScript errors"
```

Runs as a staged pipeline:
```
team-plan → team-prd → team-exec → team-verify → team-fix (loop)
```

---

## 5. Utilities

### Rate Limit Wait
Auto-resume Claude Code sessions when rate limits reset:
```bash
omc wait          # Check status, get guidance
omc wait --start  # Enable auto-resume daemon
omc wait --stop   # Disable daemon
```

### Notifications (Telegram/Discord)
```bash
omc config-stop-callback telegram --enable --token <bot_token> --chat <chat_id>
omc config-stop-callback discord --enable --webhook <url>
```

---

## 6. Updating

```bash
# 1. Sync latest version
/plugin marketplace update omc

# 2. Re-run setup
/omc:omc-setup

# If issues after update
/omc:omc-doctor
```

---

## 7. Optional: Multi-AI Orchestration

OMC can optionally orchestrate external AI providers (not required):

| Provider | Install | What it enables |
|----------|---------|----------------|
| Gemini CLI | `npm install -g @google/gemini-cli` | Design review, UI consistency (1M token context) |
| Codex CLI | `npm install -g @openai/codex` | Architecture validation, code review cross-check |

---

## Why OMC?

- **Zero configuration** — works out of the box with intelligent defaults
- **Team-first orchestration** — Team is the canonical multi-agent surface
- **Natural language interface** — no commands to memorize
- **Automatic parallelization** — complex tasks distributed across 32 specialized agents
- **Persistent execution** — won't stop until the job is verified complete
- **Cost optimization** — smart model routing saves 30–50% on tokens
- **Real-time visibility** — HUD statusline shows what's happening under the hood

---

## Quick Reference

| Action | Command |
|--------|---------|
| Install | `/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode` |
| Setup | `/omc:omc-setup` |
| Team mode | `/omc:team N:executor "task"` |
| Autopilot | `autopilot: <task>` |
| Ralph loop | `ralph: <task>` |
| Ultrawork | `ulw <task>` |
| Update | `/plugin marketplace update omc && /omc:omc-setup` |
| Debug | `/omc:omc-doctor` |

→ [Full documentation](https://yeachan-heo.github.io/oh-my-claudecode-website) · [GitHub](https://github.com/Yeachan-Heo/oh-my-claudecode)
