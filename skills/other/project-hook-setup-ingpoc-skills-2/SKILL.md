---
name: project-hook-setup
description: "Use when setting up project-specific hooks for Claude Code enforcement. Load during INIT state when .claude/hooks/ is missing, or when creating new project. Installs 5 hooks that read from .claude/config/project.json (tests, health, dependencies)."
keywords: hooks, project, setup, enforcement, testing, health-check, dependencies
---

# Project Hook Setup

Per-project setup for Claude Code hooks. These hooks read from `.claude/config/project.json` for project-specific settings.

## Purpose

Installs 5 project-specific hooks that enforce:

- Test verification before marking tested
- File existence before marking complete
- Health checks for API projects
- Dependency validation
- Session entry protocol

## When to Use

| Situation | Action |
| --------- | ------ |
| New project | Run during INIT |
| .claude/hooks/ missing | Run setup |
| Project config changed | Re-run setup |
| Adding dependencies | Update config, re-run |

## Quick Check

```bash
# Check if project hooks exist
ls .claude/hooks/

# Check if config exists
cat .claude/config/project.json
```

## Interactive Config

Setup prompts for project configuration:

| Setting | Description | Example |
| ------- | ----------- | ------- |
| Project type | Framework used | `fastapi`, `django`, `node` |
| Dev server port | Local development port | `8000` |
| Health check | Command to verify server | `curl -sf http://localhost:8000/health` |
| Test command | How to run tests | `pytest` |
| Required env | Environment variables needed | `DATABASE_URL`, `API_KEY` |
| Required services | Services to be running | `redis://localhost:6379` |

## Setup Steps

### 1. Install Hooks

```bash
# Interactive mode (prompts for config)
.skills/project-hook-setup/scripts/setup-project-hooks.sh

# Non-interactive mode (for agents/automation)
.skills/project-hook-setup/scripts/setup-project-hooks.sh --non-interactive

# Auto-confirm prompts
.skills/project-hook-setup/scripts/setup-project-hooks.sh --yes

# Use existing config
.skills/project-hook-setup/scripts/setup-project-hooks.sh --config /path/to/config.json

# Environment variable (agent mode)
CLAUDE_NON_INTERACTIVE=1 .skills/project-hook-setup/scripts/setup-project-hooks.sh
```

**Non-interactive flags:**

| Flag | Purpose |
| ---- | ------- |
| `--non-interactive` / `-n` | Skip all prompts (keeps existing config) |
| `--yes` / `-y` | Auto-confirm all prompts |
| `--config` / `-c` \<path\> | Use existing config file |

This:

- Creates `.claude/config/project.json` (or uses provided config)
- Copies 5 hook templates to `.claude/hooks/`
- Sets executable permissions

### 2. Verify Installation

```bash
.skills/project-hook-setup/scripts/verify-project-hooks.sh
```

## Hooks Installed

| Hook | Event | Purpose | Reads From |
| ---- | ----- | ------- | ---------- |
| `verify-tests.py` | PreToolUse | Run tests before tested | project.json → test_command |
| `verify-files-exist.py` | PreToolUse | Check files before complete | feature-list.json |
| `verify-health.py` | PreToolUse | Check server health | project.json → health_check |
| `require-dependencies.py` | PreToolUse | Validate env, services | project.json |
| `session-entry.sh` | CLI utility | Session entry protocol | project.json |

**Note**: `session-entry.sh` is a CLI utility. Use: `.claude/hooks/session-entry.sh`

## Settings.json Configuration

Setup script configures `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify-tests.py"},
          {"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify-files-exist.py"},
          {"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify-health.py"},
          {"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/require-dependencies.py"}
        ]
      }
    ]
  }
}
```

**Note**: Uses `$CLAUDE_PROJECT_DIR` for project-relative paths.

## Exit Criteria (Code Verified)

```bash
# Config exists with required fields
[ -f ".claude/config/project.json" ]
jq -e '.project_type' .claude/config/project.json >/dev/null
jq -e '.health_check' .claude/config/project.json >/dev/null
jq -e '.test_command' .claude/config/project.json >/dev/null

# Hooks exist and executable
[ -d ".claude/hooks" ]
[ -x ".claude/hooks/verify-tests.py" ]
[ -x ".claude/hooks/verify-files-exist.py" ]
[ -x ".claude/hooks/verify-health.py" ]
[ -x ".claude/hooks/require-dependencies.py" ]
[ -x ".claude/hooks/session-entry.sh" ]

# Verify script passes
.skills/project-hook-setup/scripts/verify-project-hooks.sh
```

## Scripts

| Script | Purpose |
| ------ | ------- |
| `setup-project-hooks.sh` | Main setup (config + hooks + settings + validate) |
| `configure-project-settings.py` | Configure .claude/settings.json |
| `validate-settings.py` | Validate hooks configured in settings.json |
| `prompt-project-config.sh` | Interactive config creation |
| `verify-project-hooks.sh` | Verify hook files exist |
| `install-hooks.sh` | Copy templates to .claude/hooks/ |

## Project Config Schema

`.claude/config/project.json`:

```json
{
  "project_type": "fastapi|django|node|python|other",
  "dev_server_port": 8000,
  "health_check": "curl -sf http://localhost:8000/health",
  "test_command": "pytest",
  "required_env": ["DATABASE_URL", "API_KEY"],
  "required_services": ["redis://localhost:6379"]
}
```

## Troubleshooting

| Problem | Solution |
| ------- | -------- |
| Config missing | Run `setup-project-hooks.sh` to create |
| Hook can't read config | Check JSON syntax, verify required fields |
| Tests not found | Update test_command in project.json |
| Health check fails | Server not running or wrong port |
| Permission denied | Run: `chmod +x .claude/hooks/*` |

## Integration

This skill is called by the `initializer` skill during INIT state:

```markdown
5. Setup hooks:
   - Check: ~/.claude/hooks/verify-state-transition.py exists (global)
   - Check: .claude/hooks/verify-tests.py exists (project)
   - If missing, load respective setup skill
```

## Next Steps

After project hooks: Continue with feature breakdown and implementation.
