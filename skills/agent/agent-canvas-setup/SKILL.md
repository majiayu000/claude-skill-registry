---
name: agent-canvas-setup
description: Dependency checker and installer for agent-canvas, agent-eyes, and canvas-edit skills. Use BEFORE running any canvas skill for the first time, or when canvas skills fail with import/browser errors. Triggers on "setup agent canvas", "install canvas dependencies", "canvas not working", "playwright not found", or any setup/installation request for canvas skills.
---

# Agent Canvas Setup

Checks and installs dependencies for the agent-canvas visual editing skills (agent-eyes, agent-canvas, canvas-edit).

## Quick Check

Run this first to see what's needed:

```bash
uv run .claude/skills/agent-canvas-setup/scripts/check_setup.py check
```

**If all checks pass** → Ready to use canvas skills.  
**If checks fail** → Ask user about installation scope.

## Installation Scopes

**ALWAYS ask the user which scope they prefer before installing:**

| Scope | What it does | Best for |
|-------|--------------|----------|
| `temporary` | Browsers installed globally, Python deps cached by uv on-demand (~/.cache/uv) | Most users - minimal footprint |
| `local` | Creates `.venv` in project with playwright installed | Projects wanting isolated deps |
| `global` | Installs browsers globally only (Python deps via uv) | Shared workstations |

### Recommended Prompt to User

```
Agent Canvas needs some dependencies. How would you like to install them?

1. **temporary** (recommended) - Minimal footprint. Browsers installed to system cache, 
   Python packages managed on-demand by uv. Nothing added to your project.

2. **local** - Creates a .venv in this project with playwright. Good if you want 
   all dependencies tracked with the project.

3. **global** - Same as temporary. Browsers go to system cache.

Which do you prefer? (1/2/3 or temporary/local/global)
```

## Multi-Agent Support

Agent Canvas can install skills for multiple AI agents. Use `--agents` to specify which agents:

| Agent | Skills Directory | Description |
|-------|------------------|-------------|
| `claude` | `.claude/skills/` | Claude Code / Claude Desktop (default) |
| `codex` | `.codex/skills/` | OpenAI Codex CLI |
| `copilot` | `.github/skills/` | GitHub Copilot |
| `cursor` | `.cursor/skills/` | Cursor IDE |
| `windsurf` | `.windsurf/skills/` | Windsurf IDE |
| `aider` | `.aider/skills/` | Aider |

### Examples

```bash
# Install for Claude only (default)
uv run .claude/skills/agent-canvas-setup/scripts/check_setup.py install --scope temporary

# Install for Claude and Copilot
uv run .claude/skills/agent-canvas-setup/scripts/check_setup.py install --scope temporary --agents claude,copilot

# Install for all supported agents
uv run .claude/skills/agent-canvas-setup/scripts/check_setup.py install --scope temporary --agents claude,copilot,cursor,windsurf,aider
```

## Install Commands

```bash
SKILL_DIR=".claude/skills/agent-canvas-setup/scripts"

# Temporary (recommended) - uv handles Python deps on-demand
uv run $SKILL_DIR/check_setup.py install --scope temporary

# With multi-agent support
uv run $SKILL_DIR/check_setup.py install --scope temporary --agents claude,copilot

# Local - creates .venv in project
uv run $SKILL_DIR/check_setup.py install --scope local

# Global - browsers only (Python via uv)
uv run $SKILL_DIR/check_setup.py install --scope global
```

## What Gets Installed

### Always Required
- **uv** - Must be pre-installed by user (provides instructions if missing)
- **Python 3.10+** - Must be pre-installed

### Installed by Setup
- **Playwright Chromium** (~200MB) - Browser binary for automation
  - Location: `~/.cache/ms-playwright/` (Mac/Linux)
  - This is the main "weight" of the installation

### Python Packages (handled by uv)
- `playwright` - Browser automation
- `axe-playwright-python` - Accessibility scanning

For `temporary` and `global` scopes, these are cached in `~/.cache/uv/` and loaded on-demand when running scripts.

For `local` scope, these are installed to `.venv/` in the project.

## Error Recovery

If canvas skills fail, run check first:

```bash
uv run .claude/skills/agent-canvas-setup/scripts/check_setup.py check --json
```

Common issues:
- `Playwright Chromium: not found` → Run install with any scope
- `uv package manager: not found` → User must install uv first
- `Python 3.10+: need 3.10+` → User must upgrade Python

## Workflow Integration

Before running any canvas skill for the first time:

1. Run `check_setup.py check`
2. If not ready, ask user about preferred scope
3. Run `check_setup.py install --scope <choice>`
4. Verify with `check_setup.py check` again
5. Proceed to canvas skill
