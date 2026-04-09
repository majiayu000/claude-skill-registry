---
name: quickstart
description: 'New user onboarding. Detect setup, explain what AgentOps does, give one next action. Under 30 seconds. Triggers: "quickstart", "get started", "onboarding", "how do I start".'
skill_api_version: 1
context:
  window: inherit
  intent:
    mode: none
  intel_scope: none
metadata:
  tier: session
  dependencies: []
output_contract: "stdout: onboarding walkthrough"
---

# /quickstart

> **One job:** Tell a new user what AgentOps does and what to do first. Fast.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

## Execution Steps

### Step 1: Detect setup

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1 && echo "GIT=true" || echo "GIT=false"
command -v ao >/dev/null && echo "AO=true" || echo "AO=false"
command -v bd >/dev/null && echo "BD=true" || echo "BD=false"
[ -d .agents ] && echo "AGENTS=true" || echo "AGENTS=false"
[ -n "${CODEX_THREAD_ID:-}" ] || [ "${CODEX_INTERNAL_ORIGINATOR_OVERRIDE:-}" = "Codex Desktop" ] && echo "CODEX=true" || echo "CODEX=false"
```

### Step 2: Show what AgentOps does

Output exactly this (no additions, no diagrams):

```
AgentOps gives your coding agent three things it doesn't have by default:

  Memory    — sessions accumulate learnings in .agents/ and surface them back
  Judgment  — /council spawns independent judges to validate plans and code
  Workflow  — /rpi delegates /discovery → /crank → /validation in one command

Key skills: /rpi  /discovery  /validation  /implement  /research  /council  /swarm  /status
Full reference: /quickstart --catalog
```

### Step 3: One next action

Match the first row that applies. Output only that message — nothing else.

| Condition | Message |
|-----------|---------|
| GIT=false | "⚠ Not in a git repo. Run `git init` first." |
| AO=false + CODEX=true | "📦 Install ao CLI first:\n  brew tap boshu2/agentops https://github.com/boshu2/homebrew-agentops\n  brew install agentops\n  ao init && ao seed\n  ao codex start\nThen: `/rpi \"a small goal\"` to run your first cycle." |
| AO=false | "📦 Install ao CLI first:\n  brew tap boshu2/agentops https://github.com/boshu2/homebrew-agentops\n  brew install agentops\n  ao init --hooks && ao seed\nThen: `/rpi \"a small goal\"` to run your first cycle." |
| AGENTS=false + CODEX=true | "🌱 ao is installed but not initialized here.\n  Run `/bootstrap` to set up GOALS.md, PRODUCT.md, .agents/, and hooks.\n  Or manually: `ao init && ao seed && ao codex start`\nThen: `/rpi \"a small goal\"` to run your first cycle." |
| AGENTS=false | "🌱 ao is installed but not initialized here.\n  Run `/bootstrap` to set up GOALS.md, PRODUCT.md, .agents/, and hooks.\n  Or manually: `ao init --hooks && ao seed`\nThen: `/rpi \"a small goal\"` to run your first cycle." |
| BD=false + CODEX=true | "✅ Codex fallback ready.\n  `ao codex start` — surface prior context and run safe maintenance\n  `/rpi \"your goal\"` — full /discovery → /crank → /validation pipeline\n  `ao codex stop` — close out the session and queue learnings\n  Want issue tracking? `brew install boshu2/agentops/beads && bd init --prefix <prefix>`" |
| BD=false | "✅ Flywheel active. Start now:\n  `/rpi \"your goal\"` — full /discovery → /crank → /validation pipeline\n  `/validation` — close out recent work and capture learnings\n  `/research <topic>` — explore the codebase\n  Want issue tracking? `brew install boshu2/agentops/beads && bd init --prefix <prefix>`" |
| BD=true + CODEX=true | "✅ Codex full stack ready.\n  `ao codex start` — start with prior context\n  `bd ready` — see open work\n  `/rpi \"your goal\"` — start a new goal from scratch\n  `ao codex stop` — close out the session cleanly" |
| BD=true | "✅ Full stack ready.\n  `bd ready` — see open work\n  `/rpi \"your goal\"` — start a new goal from scratch\n  `/status` — see current session state" |

Starting a new project? Run `/scaffold <language> <name>` to generate project structure with best practices.

---

## Examples

### First-Time Setup

**User says:** `/quickstart`

**What happens:** Agent detects tools, shows one-line status, gives the single next action to run.

### Already Set Up

**User says:** `/quickstart`

**What happens:** Agent detects full stack is ready and suggests `/rpi "your goal"` or `bd ready`.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skills not installed | `bash <(curl -fsSL https://raw.githubusercontent.com/boshu2/agentops/main/scripts/install.sh)` |
| Codex hooks on older versions (pre-v0.115.0) | Codex CLI v0.115.0+ has native hooks. For older versions, use `ao codex start` to begin and `ao codex stop` to close out; `ao codex status` shows hookless lifecycle health |
| Flywheel count is 0 | First session — run `/rpi "a small goal"` to start it |
| Want the full skill catalog | Ask: "show me all the skills" or see `references/full-catalog.md` |

## Reference Documents

- [references/getting-started.md](references/getting-started.md)
- [references/troubleshooting.md](references/troubleshooting.md)
- [references/full-catalog.md](references/full-catalog.md)

## See Also

- [scaffold](../scaffold/SKILL.md) — Project scaffolding and component generation
