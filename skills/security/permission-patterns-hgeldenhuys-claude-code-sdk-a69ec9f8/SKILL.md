---
name: permission-patterns
description: Guide for configuring Claude Code permissions effectively. Use when setting up security policies, configuring allow/deny patterns, managing tool permissions, or implementing team security standards. Covers permission modes, sandboxing, and settings.json configuration.
allowed-tools: ["Read"]
---

# Permission Patterns

Configure Claude Code permissions for security, productivity, and team compliance.

## Quick Reference

| Aspect | Options |
|--------|---------|
| Permission Modes | `default`, `plan`, `acceptEdits`, `dontAsk`, `bypassPermissions` |
| Settings Files | `~/.claude/settings.json` (user), `.claude/settings.json` (project) |
| Rule Types | `allow`, `ask`, `deny` |
| Pattern Types | Tool names, Bash commands, file paths, MCP tools |

## Permission Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `default` | Prompts on first use of each tool | Standard development |
| `plan` | Read-only, no modifications | Code review, analysis |
| `acceptEdits` | Auto-accepts file edits | Trusted editing sessions |
| `dontAsk` | Auto-denies unless pre-approved | Restricted environments |
| `bypassPermissions` | Skips all prompts | Trusted automation (use with caution) |

For detailed mode behaviors and switching, see [MODES.md](./MODES.md).

## Permission Rule Precedence

Rules are evaluated in this order (highest to lowest):

1. **Deny** - Blocks tool use (highest priority)
2. **Ask** - Requires confirmation
3. **Allow** - Permits without prompting

Settings file precedence:
1. Managed settings (enterprise)
2. Command line arguments
3. `.claude/settings.local.json` (local project)
4. `.claude/settings.json` (shared project)
5. `~/.claude/settings.json` (user)

## Basic Configuration

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Read"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  },
  "defaultMode": "default"
}
```

## Common Permission Patterns

### Git Operations

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git branch:*)",
      "Bash(git checkout:*)"
    ],
    "ask": [
      "Bash(git push:*)",
      "Bash(git commit:*)"
    ]
  }
}
```

### Package Managers

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(npm test:*)",
      "Bash(bun *)",
      "Bash(yarn *)"
    ]
  }
}
```

### File Operations

```json
{
  "permissions": {
    "allow": [
      "Edit(/src/**/*.ts)",
      "Edit(/tests/**)",
      "Read"
    ],
    "deny": [
      "Edit(/.env)",
      "Edit(/secrets/**)"
    ]
  }
}
```

For comprehensive patterns including Bash, file paths, and MCP tools, see [PATTERNS.md](./PATTERNS.md).

## Tool Permission Categories

| Category | Default | Examples |
|----------|---------|----------|
| Read-only | No approval | `Read`, `Glob`, `Grep`, `LS` |
| File modification | Session approval | `Edit`, `Write` |
| Bash commands | Per-command approval | `Bash` |
| Network | Per-request approval | `WebFetch` |
| MCP tools | Per-tool approval | `mcp__server__tool` |

## Sandboxing

Enable sandboxing for filesystem and network isolation:

```bash
/sandbox
```

Benefits:
- Filesystem isolation (writes restricted to project)
- Network access controls
- Reduced permission prompts
- Maintained security boundaries

Claude Code restricts writes to the project directory and subdirectories by default. Parent directories are protected.

## Security Essentials

### Always Deny

```json
{
  "permissions": {
    "deny": [
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(rm -rf *)",
      "Edit(/.env)",
      "Edit(/secrets/**)"
    ]
  }
}
```

### Principle of Least Privilege

Start restrictive, add permissions as needed:

```json
{
  "defaultMode": "dontAsk",
  "permissions": {
    "allow": [
      "Read",
      "Bash(git status)",
      "Bash(npm test)"
    ]
  }
}
```

For comprehensive security guidance, see [SECURITY.md](./SECURITY.md).

## CLI Permission Flags

| Flag | Purpose |
|------|---------|
| `--permission-mode <mode>` | Start in specific mode |
| `--allowedTools <patterns>` | Pre-approve tools |
| `--disallowedTools <patterns>` | Block tools |
| `--tools <list>` | Restrict available tools |
| `--dangerously-skip-permissions` | Skip all prompts (use with caution) |

Example:
```bash
claude --permission-mode plan
claude --allowedTools "Bash(git:*)" "Read"
claude --tools "Bash,Edit,Read"
```

## Managing Permissions

View and manage permissions interactively:

```bash
/permissions
```

Shows:
- All permission rules
- Source settings file for each rule
- Current permission mode

## Workflow: Setting Up Project Permissions

### Prerequisites
- [ ] Identify tools needed for the project
- [ ] Determine security requirements
- [ ] Check for enterprise managed settings

### Steps

1. **Create project settings**
   - [ ] Create `.claude/settings.json`
   - [ ] Set appropriate `defaultMode`
   - [ ] Add `allow` rules for common operations

2. **Configure sensitive operations**
   - [ ] Add `ask` rules for risky operations
   - [ ] Add `deny` rules for blocked operations

3. **Test configuration**
   - [ ] Run Claude Code with `/permissions`
   - [ ] Verify expected prompts appear
   - [ ] Adjust rules as needed

### Validation
- [ ] Common operations work without excessive prompts
- [ ] Sensitive operations require confirmation
- [ ] Blocked operations are denied

## Reference Files

| File | Contents |
|------|----------|
| [MODES.md](./MODES.md) | Detailed permission mode behaviors and switching |
| [PATTERNS.md](./PATTERNS.md) | Comprehensive pattern syntax for all tool types |
| [SECURITY.md](./SECURITY.md) | Security best practices and enterprise policies |
