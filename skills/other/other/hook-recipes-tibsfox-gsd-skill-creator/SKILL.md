---
name: hook-recipes
description: Curated collection of ready-to-use Claude Code hook recipes for safety, automation, formatting, logging, and context injection. Use when configuring hooks, setting up safety guards, automating workflows, or when user mentions 'hooks', 'PreToolUse', 'PostToolUse', 'guard', 'automation', 'claude hooks'.
---

# Hook Recipes

A curated collection of ready-to-use Claude Code hook configurations. Each recipe is a complete JSON snippet you can add to your `.claude/settings.json` or project-level `.claude/settings.local.json`.

## Hook Types Reference

| Hook Type | Fires When | Common Use |
|-----------|-----------|------------|
| `PreToolUse` | Before any tool executes | Block dangerous commands, inject context |
| `PostToolUse` | After any tool executes | Log actions, format output, validate results |
| `Notification` | Claude wants to notify the user | Custom notification routing |
| `Stop` | Claude is about to stop responding | Enforce checklists, add summaries |

### Tool Names for Matching

| Tool Name | What It Does |
|-----------|-------------|
| `Bash` | Shell command execution |
| `Read` | File reading |
| `Write` | File writing (full file) |
| `Edit` | File editing (partial) |
| `Glob` | File pattern matching |
| `Grep` | Content searching |
| `WebFetch` | HTTP requests |

## Safety Hooks

### Block Destructive Git Commands

Prevents accidental force pushes, hard resets, and branch deletions.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "intercept",
            "command": "bash -c '[[ \"$CLAUDE_TOOL_INPUT\" =~ (git\\s+push\\s+--force|git\\s+push\\s+-f|git\\s+reset\\s+--hard|git\\s+clean\\s+-f|git\\s+checkout\\s+\\.|git\\s+restore\\s+\\.) ]]'",
            "timeout": 5000,
            "description": "Block destructive git commands"
          }
        ]
      }
    ]
  }
}
```

**What it does:** Intercepts Bash tool calls and blocks commands matching force push, hard reset, clean, and restore patterns. The hook exits 0 (block) if a destructive pattern is found, exit non-zero (allow) otherwise.

**When to use:** Always. This is a foundational safety hook for any project.

### Block Database Destructive Operations

Prevents DROP TABLE, TRUNCATE, and DELETE without WHERE.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "intercept",
            "command": "bash -c '[[ \"$CLAUDE_TOOL_INPUT\" =~ (DROP\\s+TABLE|DROP\\s+DATABASE|TRUNCATE|DELETE\\s+FROM\\s+\\w+\\s*;) ]]'",
            "timeout": 5000,
            "description": "Block destructive SQL operations"
          }
        ]
      }
    ]
  }
}
```

**What it does:** Blocks SQL commands that would destroy data. Catches `DELETE FROM table;` (no WHERE clause) but allows `DELETE FROM table WHERE ...`.

**When to use:** Any project that interacts with databases.

### Block Secret File Access

Prevents reading or writing sensitive files.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Write|Edit",
        "hooks": [
          {
            "type": "intercept",
            "command": "bash -c '[[ \"$CLAUDE_TOOL_INPUT\" =~ (\\.env|\\.env\\.local|credentials|secrets\\.json|private[_-]?key|\\.pem$|\\.key$) ]]'",
            "timeout": 5000,
            "description": "Block access to secret files"
          }
        ]
      }
    ]
  }
}
```

**What it does:** Intercepts Read, Write, and Edit operations targeting files that commonly contain secrets.

**When to use:** Projects with sensitive configuration files.

### Block Force Install and Audit Fix

Prevents potentially dangerous package manager operations.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "intercept",
            "command": "bash -c '[[ \"$CLAUDE_TOOL_INPUT\" =~ (npm\\s+audit\\s+fix\\s+--force|npm\\s+install\\s+--force|--legacy-peer-deps) ]]'",
            "timeout": 5000,
            "description": "Block force install and audit fix --force"
          }
        ]
      }
    ]
  }
}
```

**What it does:** Blocks `npm audit fix --force` (can introduce breaking changes), `npm install --force` (bypasses version checks), and `--legacy-peer-deps` (ignores peer dependency conflicts).

**When to use:** Any Node.js project where dependency integrity matters.

## Formatting Hooks

### Auto-Format on File Write

Runs Prettier on files after Claude writes or edits them.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'FILE=$(echo \"$CLAUDE_TOOL_INPUT\" | jq -r \".file_path // .filePath // empty\"); if [[ -n \"$FILE\" && \"$FILE\" =~ \\.(ts|tsx|js|jsx|json|css|md)$ ]]; then npx prettier --write \"$FILE\" 2>/dev/null; fi'",
            "timeout": 10000,
            "description": "Auto-format files with Prettier after write/edit"
          }
        ]
      }
    ]
  }
}
```

**What it does:** After every Write or Edit, extracts the file path and runs Prettier if the file matches supported extensions. Fails silently if Prettier is not installed.

**When to use:** Projects with Prettier configured. Ensures Claude's output matches project formatting.

### Auto-Lint on File Write

Runs ESLint fix on written files.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'FILE=$(echo \"$CLAUDE_TOOL_INPUT\" | jq -r \".file_path // .filePath // empty\"); if [[ -n \"$FILE\" && \"$FILE\" =~ \\.(ts|tsx|js|jsx)$ ]]; then npx eslint --fix \"$FILE\" 2>/dev/null; fi'",
            "timeout": 15000,
            "description": "Auto-lint files with ESLint after write/edit"
          }
        ]
      }
    ]
  }
}
```

**When to use:** Projects with ESLint configured. Pairs well with the Prettier hook above.

## Logging Hooks

### Audit Log of All Tool Usage

Logs every tool invocation to a file for review.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo \"$(date -u +\"%Y-%m-%dT%H:%M:%SZ\") [PRE] $CLAUDE_TOOL_NAME: $(echo $CLAUDE_TOOL_INPUT | head -c 200)\" >> /tmp/claude-audit.log'",
            "timeout": 3000,
            "description": "Log all tool usage to audit file"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo \"$(date -u +\"%Y-%m-%dT%H:%M:%SZ\") [POST] $CLAUDE_TOOL_NAME: exit=$CLAUDE_TOOL_EXIT_CODE\" >> /tmp/claude-audit.log'",
            "timeout": 3000,
            "description": "Log tool completion to audit file"
          }
        ]
      }
    ]
  }
}
```

**What it does:** Creates a timestamped audit trail of every tool call (before and after) in `/tmp/claude-audit.log`. Truncates input to 200 chars to keep logs manageable.

**When to use:** During development and debugging of hook configurations. Also useful for compliance and audit trails.

### Log Only Write Operations

Lighter logging focused on mutations.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo \"$(date -u +\"%Y-%m-%dT%H:%M:%SZ\") [$CLAUDE_TOOL_NAME] $(echo $CLAUDE_TOOL_INPUT | jq -r \".file_path // .filePath // .command // empty\" 2>/dev/null | head -c 200)\" >> .claude/mutations.log'",
            "timeout": 3000,
            "description": "Log write operations for change tracking"
          }
        ]
      }
    ]
  }
}
```

**When to use:** When you want to track what Claude changed without the noise of read operations.

## Context Injection Hooks

### Inject Project Context on Session Start

Automatically load project context when a Claude session begins.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Read|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'if [ ! -f /tmp/.claude-context-loaded ]; then cat .claude/project-context.md 2>/dev/null; touch /tmp/.claude-context-loaded; fi'",
            "timeout": 5000,
            "description": "Inject project context on first tool use"
          }
        ]
      }
    ]
  }
}
```

**What it does:** On the first tool invocation of a session, outputs the contents of a project context file. Uses a flag file to avoid repeating. Output is included in Claude's context.

**When to use:** Projects with important conventions or context that Claude should always know about.

### Inject Recent Git Context

Provides recent commit context before writes.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'FILE=$(echo \"$CLAUDE_TOOL_INPUT\" | jq -r \".file_path // .filePath // empty\" 2>/dev/null); if [[ -n \"$FILE\" && -f \"$FILE\" ]]; then echo \"Recent changes to $FILE:\"; git log --oneline -3 -- \"$FILE\" 2>/dev/null; fi'",
            "timeout": 5000,
            "description": "Show recent git history for files being modified"
          }
        ]
      }
    ]
  }
}
```

**When to use:** When you want Claude to be aware of recent changes to files it's about to modify.

## Stop Criteria Hooks

### Enforce Checklist Before Stopping

Reminds Claude to verify its work before finishing.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo \"Before stopping, verify: 1) All tests pass 2) No lint errors 3) Changes committed 4) Summary provided\"'",
            "timeout": 3000,
            "description": "Remind Claude to verify work before stopping"
          }
        ]
      }
    ]
  }
}
```

**What it does:** When Claude is about to stop, injects a checklist reminder into the context. Claude will see this and either confirm or address missing items.

**IMPORTANT WARNING about Stop hooks:** A Stop hook that causes Claude to continue, combined with conditions that always re-trigger the Stop hook, creates an infinite loop. Always ensure Stop hooks have a termination condition or are purely informational (exit non-zero to allow stopping).

**When to use:** When you want consistent completion behavior.

### Enforce Test Run Before Stopping

Blocks Claude from stopping until tests pass.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "intercept",
            "command": "bash -c 'if [ -f /tmp/.claude-tests-passed ]; then exit 1; fi; echo \"Tests have not been verified. Run tests before completing.\"; exit 0'",
            "timeout": 5000,
            "description": "Require tests to pass before stopping"
          }
        ]
      }
    ]
  }
}
```

**What it does:** Blocks Claude from stopping unless a flag file exists. Claude must run tests and create the flag (e.g., `npm test && touch /tmp/.claude-tests-passed`) before it can complete.

**IMPORTANT:** This hook has a built-in escape via the flag file. Without an escape condition, Stop intercept hooks create infinite loops.

**When to use:** Strict TDD workflows where tests must always be green before session ends.

## Notification Hooks

### Desktop Notification on Completion

Sends a system notification when Claude finishes a task.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'notify-send \"Claude Code\" \"Task completed\" 2>/dev/null || osascript -e \"display notification \\\"Task completed\\\" with title \\\"Claude Code\\\"\" 2>/dev/null || true'",
            "timeout": 5000,
            "description": "Send desktop notification on task completion"
          }
        ]
      }
    ]
  }
}
```

**What it does:** Sends a desktop notification using `notify-send` (Linux) or `osascript` (macOS). Falls back silently if neither is available.

**When to use:** When running long tasks and you want to be notified upon completion.

## Composing Hooks

You can combine multiple hooks on the same event. They execute in order.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "intercept",
            "command": "...",
            "description": "Safety: block destructive commands"
          },
          {
            "type": "command",
            "command": "...",
            "description": "Logging: audit all bash commands"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "...",
            "description": "Format: auto-prettier"
          },
          {
            "type": "command",
            "command": "...",
            "description": "Logging: track mutations"
          }
        ]
      }
    ]
  }
}
```

**Execution order:** Hooks within the same matcher run in array order. An `intercept` hook that blocks (exit 0) prevents subsequent hooks from running.

## Testing and Debugging

### Debug Flag

Test hooks by running Claude Code with the `--debug` flag:

```bash
claude --debug
```

This prints hook execution details including matched hooks, exit codes, and output.

### Manual Hook Testing

Test hook commands directly in your terminal:

```bash
# Simulate the environment variables Claude sets
export CLAUDE_TOOL_NAME="Bash"
export CLAUDE_TOOL_INPUT='{"command": "git push --force"}'

# Run your hook command
bash -c '[[ "$CLAUDE_TOOL_INPUT" =~ (git\s+push\s+--force) ]]'
echo "Exit code: $?"  # 0 = blocked, 1 = allowed
```

### Common Debugging Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Hook never fires | Wrong matcher pattern | Check tool name spelling, use `.*` to test |
| Hook blocks everything | Regex too broad | Narrow the pattern, test with real inputs |
| Infinite loop on Stop | Stop hook always exits 0 | Add escape condition (flag file, counter) |
| Timeout errors | Command too slow | Increase `timeout` or optimize command |
| Hook output not visible | Using `intercept` type | Switch to `command` type for output |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Stop hook with no escape | Infinite loop | Always include termination condition |
| Overly broad interceptors | Blocks legitimate operations | Use specific regex patterns |
| No timeout on hooks | Hung hook blocks all tool use | Always set `timeout` (5000ms default) |
| Secrets in hook commands | Exposed in config files | Use environment variables |
| Heavy computation in hooks | Slows every tool call | Keep hooks fast (<1s), offload work |
| Modifying files in PreToolUse | Unexpected side effects | Use PostToolUse for mutations |
| No description field | Hard to debug which hook fired | Always add `description` |

## Recommended Starter Set

For most projects, start with these three hooks:

1. **Block destructive git commands** (Safety)
2. **Auto-format on file write** (Consistency)
3. **Audit log of all tool usage** (Visibility)

Add more hooks as specific needs arise. Fewer well-tested hooks are better than many untested ones.
