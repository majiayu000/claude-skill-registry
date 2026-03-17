---
name: alto-dev-guide
description: Use when developing ALTO itself - editing devenv.nix, hooks/*.py, agents/*.md, or checking Claude Code hook/agent syntax. Reference guide with documentation URLs and patterns.
---

# ALTO Development Guide

Reference for developing ALTO. Use URLs for authoritative docs, summaries for quick reference.

---

## Devenv MCP (always available)

ALTO configures the devenv MCP server automatically. Use it for:

- **Package search** - Find packages and their configuration options
- **Config understanding** - Understand devenv syntax and patterns
- **Config generation** - Generate valid devenv configurations

The MCP is available as `devenv` server. Use MCP tools to query it when you need:
- What packages are available for a language/tool
- How to configure a specific service
- Valid options for a devenv setting

---

## Documentation Sources

### Devenv (authoritative)
| Topic | URL |
|-------|-----|
| All options | https://devenv.sh/reference/options/ |
| Scripts | https://devenv.sh/reference/options/#scripts |
| Tasks | https://devenv.sh/reference/options/#tasks |
| Imports | https://devenv.sh/composing-using-imports/ |
| Claude Code integration | https://devenv.sh/integrations/claude-code/ |

### Claude Code (authoritative)
| Topic | URL |
|-------|-----|
| Hooks reference | https://code.claude.com/docs/en/hooks |
| Subagents | https://code.claude.com/docs/en/sub-agents |
| Skills | https://code.claude.com/docs/en/skills |
| CLI reference | https://code.claude.com/docs/en/cli-reference |
| Settings | https://code.claude.com/docs/en/settings |

### Community resources
| Topic | URL |
|-------|-----|
| Full stack overview | https://alexop.dev/posts/understanding-claude-code-full-stack/ |
| Hooks mastery | https://github.com/disler/claude-code-hooks-mastery |
| Config showcase | https://github.com/ChrisWiles/claude-code-showcase |

---

## Devenv Quick Reference

### Scripts
```nix
scripts.<name> = {
  exec = ''
    echo "script body"
  '';
  description = "Shown in devenv info";
};
```
- Available as commands in shell
- Use `${variable}` for nix interpolation
- Use `''$` to escape `$` in bash

### Tasks
```nix
tasks."namespace:name" = {
  exec = ''
    echo "task body"
  '';
  before = [ "devenv:enterShell" ];  # Run before shell entry
  # after = [ "other:task" ];        # Run after another task
};
```
- Run automatically on shell entry (if `before` includes enterShell)
- Good for setup/deployment that should happen every time

### Native Imports (not flakes)
```yaml
# devenv.yaml
inputs:
  alto:
    url: github:gonzaloetjo/alto
    flake: false  # Critical: native import mode

imports:
  - alto  # References the input name
```
- `flake: false` = use devenv's native import system
- ALTO activates on import, configure with `alto.orchestrator`

---

## Claude Code Quick Reference

### Hook Types
| Type | When | Can Block | Receives |
|------|------|-----------|----------|
| SessionStart | Session begins | No | `{session_id, resume}` |
| PreToolUse | Before tool runs | Yes | `{tool, input, ...}` |
| PostToolUse | After tool runs | No | `{tool, result, ...}` |
| Stop | Session ends | No | `{session_id, ...}` |
| SubagentStop | Agent completes | No | `{agent, ...}` |
| Notification | Claude notifies | No | `{message, ...}` |
| PermissionRequest | Permission asked | Yes | `{tool, ...}` |

### Hook Configuration (devenv)
```nix
claude.code.hooks.<name> = {
  hookType = "PostToolUse";  # Required
  matcher = "Bash";          # Tool name, or "*" for all
  command = "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/script.py";
};
```

### Hook Script Pattern
```python
#!/usr/bin/env python3
import json, sys, os
from pathlib import Path

def main():
    hook_data = json.load(sys.stdin)
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))

    # Do work...

    # For SessionStart: print context for Claude to see
    print("Context message")

if __name__ == "__main__":
    main()
```

### Agents (devenv)
```nix
claude.code.agents.<name> = {
  description = "Shown when listing agents";
  tools = [ "Read" "Edit" "Bash" "Grep" "Glob" "WebFetch" ];
  model = "opus";  # or "sonnet", "haiku"
  prompt = ''
    Agent system prompt here.
    This defines behavior, not user request.
  '';
};
```

### Available Tools
`Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`, `LS`, `WebFetch`, `WebSearch`, `Task`, `TodoWrite`, `AskUserQuestion`

### Skills
Place `SKILL.md` in `.claude/skills/<name>/`
- Invoked with `/<skill-name>` or automatically by context
- Content is instructions for Claude

### MCP Servers
```nix
claude.code.mcpServers.<name> = {
  type = "stdio";  # or "http"
  command = "devenv";
  args = [ "mcp" ];
  env = { DEVENV_ROOT = "."; };
};
```

### Permissions
```nix
claude.code.permissions = {
  Bash = {
    allow = [ "git:*" "npm:*" ];
    deny = [ "rm -rf:*" "sudo:*" ];
  };
  Read = {
    deny = [ ".env" "secrets/**" ];
  };
};
```

---

## ALTO File Reference

| What | Where | Purpose |
|------|-------|---------|
| Module options | `devenv.nix` -> `options.alto` | All configurable settings |
| Scripts | `devenv.nix` -> `scripts.*` | Shell commands |
| Deploy task | `devenv.nix` -> `tasks."alto:deploy"` | File deployment |
| Agent configs | `devenv.nix` -> `claude.code.agents` | Agent wiring |
| Hook configs | `devenv.nix` -> `claude.code.hooks` | Hook wiring |
| Agent prompts | `agents/*.md` | Agent behavior |
| Hook logic | `hooks/*.py` | Hook implementation |
| Skills | `skills/*/SKILL.md` | Skill content |
| Setup orchestrator | `templates/CLAUDE.md.setup` | Human-interactive mode |
| Build orchestrator | `templates/CLAUDE.md.build` | Autonomous mode |
| Dev orchestrator | `templates/CLAUDE.md.dev` | ALTO development mode |
| User template | `templates/default/` | `nix flake init` output |
| Architecture | `ARCHITECTURE.md` | Design docs |

---

## Testing Workflows

### Fresh install
```bash
mkdir /tmp/test && cd /tmp/test
nix --extra-experimental-features 'nix-command flakes' flake init -t github:gonzaloetjo/alto --refresh
devenv shell
# Check: ls .claude/ runs/ CLAUDE.md
```

### Local development
```yaml
# test project's devenv.yaml - use local path
imports:
  - /absolute/path/to/alto
```
Then `devenv shell` to rebuild with local changes.

### Verify deployment
```bash
ls -la .claude/agents/     # Symlinks to nix store
ls -la .claude/hooks/      # Python files
cat runs/state.json        # ALTO state
cat .claude/settings.json  # Permissions + hooks
```

---

## Common Issues

| Problem | Solution |
|---------|----------|
| jq escaping in nix | Use `echo "$(jq ...)"` not complex jq strings |
| Changes not applied | Run `devenv shell` again |
| Remote changes not applied | Use `--refresh` flag |
| Hook not running | Check settings.json, verify hookType matches |
| Files read-only | Expected - nix store symlinks |

### Nix String Escaping (`''` strings)
- `''$` -> `$` (escape dollar)
- `'''` -> `''` (escape quotes)
- `\n` -> literal `\n` (not newline)
- Use actual newlines for line breaks
