---
name: hook-scope-guide
description: 'Decision framework to select hook scope (plugin, project, global) by audience. Use when placing a hook; for syntax see hook-authoring.'
---

# Hook Scope Decision Guide

This skill helps you choose the right location for Claude Code hooks based on their purpose, audience, and persistence needs.

## Important: Auto-Loading Behavior

> **`hooks/hooks.json` is automatically loaded** by Claude Code when the plugin is enabled.
> Do NOT add `"hooks": "./hooks/hooks.json"` to your `plugin.json` - this causes duplicate load errors.
> The `hooks` field in `plugin.json` is only needed for additional hook files beyond the standard `hooks/hooks.json`.

## The Three Scopes

| Scope | Location | Audience | Committed? | Persistence |
|-------|----------|----------|------------|-------------|
| **Plugin** | `hooks/hooks.json` in plugin | Plugin users | With plugin | When plugin enabled |
| **Project** | `.claude/settings.json` | Team members | Yes (repo) | Per project |
| **Global** | `~/.claude/settings.json` | Only you | Never | All sessions |

## Decision Framework

### Question 1: Who needs this hook?

**Only plugin users** → Plugin hooks
- Hook is part of plugin's core functionality
- Users expect it when they enable your plugin
- Example: A YAML plugin validates YAML syntax on edit

**All team members on this project** → Project hooks
- Codebase-specific rules or protections
- Team conventions that should be enforced
- Example: Block modifications to `/src/production/` configs

**Only me, everywhere** → Global hooks
- Personal preferences or workflow optimizations
- Cross-project utilities like logging
- Example: Log all bash commands to personal audit trail

### Question 2: Should this be version controlled?

**Yes, as part of a distributable plugin** → Plugin hooks
**Yes, shared with team in repo** → Project hooks
**No, keep private** → Global hooks

### Question 3: What's the persistence requirement?

**Only when my plugin is active** → Plugin hooks
**Always in this specific project** → Project hooks
**Always, in every project I work on** → Global hooks

## Scope Details

### Plugin Hooks

**Location**: `<plugin-root>/hooks/hooks.json`

**When to use**:
- The hook is intrinsic to your plugin's functionality
- It should automatically activate when users enable your plugin
- It only makes sense in the context of your plugin's features

**Configuration**:
```json
{
  "PreToolUse": [
    {
      "matcher": "Read",
      "hooks": [{
        "type": "command",
        "command": "echo 'Plugin reading: $CLAUDE_TOOL_INPUT' >> ${CLAUDE_PLUGIN_ROOT}/log.txt"
      }]
    }
  ]
}
```

> **Note**: Use string matchers (`"Read"`) not object matchers (`{"toolName": "Read"}`).

**Key features**:
- Use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths
- Auto-merges when plugin is enabled
- Deactivates when plugin is disabled

**Examples**:
- Validation hook for a linting plugin
- Auto-formatting hook for a code style plugin
- Logging hook for a debugging plugin

### Project Hooks

**Location**: `.claude/settings.json` (in project root)

**When to use**:
- Enforcing team-wide policies
- Protecting project-specific resources
- Codebase conventions that should survive across team members
- Rules that should be reviewed in PRs

**Configuration**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "if [[ \"$CLAUDE_TOOL_INPUT\" == *\"production\"* ]]; then echo 'BLOCKED: Production access requires approval'; exit 1; fi"
        }]
      }
    ]
  }
}
```

> **Note**: Use string matchers (`"Bash"`) not object matchers.

**Key features**:
- Committed to version control
- Shared across all team members
- Changes are visible in PRs (governance trail)
- Project-specific, not personal

**Examples**:
- Block modifications to production configs
- Require test commands before completion
- Warn about editing sensitive directories
- Enforce project naming conventions

### Global Hooks

**Location**: `~/.claude/settings.json`

**When to use**:
- Personal workflow preferences
- Cross-project utilities
- Organization-wide compliance you want everywhere
- Private rules that shouldn't be shared

**Configuration**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [{
          "type": "command",
          "command": "echo \"$(date): $CLAUDE_TOOL_NAME\" >> ~/.claude/audit.log"
        }]
      }
    ]
  }
}
```

**Key features**:
- Never committed to any repo
- Applies to ALL Claude Code sessions
- Personal to your user account
- Survives across projects

**Examples**:
- Personal audit logging
- Cross-project safety rules
- Custom notification integrations
- Development environment preferences

## Loading Order & Precedence

Claude Code loads settings in this priority (highest first):

1. **Enterprise policies** (organization-managed)
2. **Command-line arguments** (`claude --flag`)
3. **Local project settings** (`.claude/settings.local.json`)
4. **Shared project settings** (`.claude/settings.json`)
5. **User settings** (`~/.claude/settings.json`)

**Important**: Multiple hooks from different scopes can respond to the same event. When they do, **all matching hooks execute in parallel**.

## Quick Reference: Scope Selection

```
Is this hook part of a plugin's core functionality?
├─ YES → Plugin hooks (hooks/hooks.json in plugin)
└─ NO ↓

Should all team members on this project have this hook?
├─ YES → Project hooks (.claude/settings.json)
└─ NO ↓

Should this hook apply to all my Claude sessions?
├─ YES → Global hooks (~/.claude/settings.json)
└─ NO → Reconsider if you need a hook at all
```

## Security Considerations

**Plugin hooks**:
- Audited as part of plugin installation
- Users consent when enabling plugin
- Scope limited to plugin's purpose

**Project hooks**:
- Visible to all team members
- Changes reviewed in PRs
- Should reflect team consensus

**Global hooks**:
- Execute with your credentials everywhere
- Can affect all projects unexpectedly
- Review security implications carefully
- Test thoroughly before adding

## Common Patterns by Scope

### Plugin Hook Patterns
- **Validation**: Check files match plugin's format
- **Auto-completion**: Suggest plugin-specific completions
- **Logging**: Track plugin-specific operations

### Project Hook Patterns
- **Protection**: Block dangerous operations on sensitive paths
- **Enforcement**: Require tests, linting, or builds
- **Conventions**: Warn about style or naming violations

### Global Hook Patterns
- **Auditing**: Log all operations for personal review
- **Safety**: Universal dangerous command detection
- **Integration**: Personal tool notifications

## SessionStart Hook Enhancements (Claude Code 2.1.2+)

SessionStart hooks now receive additional input fields via stdin:

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | Unique session identifier |
| `source` | enum | `"startup"` \| `"resume"` \| `"clear"` \| `"compact"` |
| `agent_type` | string | Agent name if `--agent` flag used, empty otherwise |

### Agent-Aware Hooks

The `agent_type` field enables scope-appropriate context injection:

```python
# Skip heavy context for review agents
input_data = json.loads(sys.stdin.read())
if input_data.get("agent_type") in ["code-reviewer", "quick-query"]:
    print(json.dumps({"hookSpecificOutput": {"additionalContext": "Minimal"}}))
```

This is particularly useful for:
- **Plugin hooks**: Reduce overhead for lightweight agents
- **Project hooks**: Skip governance for review-only agents
- **Global hooks**: Customize logging verbosity per agent

## Related Skills

- **abstract:hook-authoring** - For hook rule syntax and patterns
- **abstract:validate-plugin** - For validating plugin structure including hooks

## References

- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Settings Configuration](https://docs.anthropic.com/en/docs/claude-code/settings)
