---
name: claude-hook-builder
description: Interactive hook creator for Claude Code. Triggers when user mentions creating hooks, PreToolUse, PostToolUse, hook validation, hook configuration, settings.json hooks, or wants to automate tool execution workflows.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Claude Code Hook Builder

## Purpose

Guide users through creating effective Claude Code hooks for tool validation, automation, and workflow enhancement. Auto-invokes when users want to create or configure hooks.

## When to Use

Auto-invoke when users mention:
- **Creating hooks** - "create hook", "make hook", "new hook", "add hook"
- **Hook events** - "PreToolUse", "PostToolUse", "UserPromptSubmit", "Stop", "SessionStart"
- **Validation** - "validate", "check", "prevent", "block", "approve"
- **Automation** - "auto-format", "auto-lint", "automatic", "trigger"
- **Hook configuration** - "settings.json hooks", "hook matcher", "hook command"

## Knowledge Base

- Official docs: `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_hooks.md`
- Hook guide: `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_hooks-guide.md`
- Project guide: `.claude/docs/creating-components.md`

## Process

### 1. Gather Requirements

Ask the user:

```
Let me help you create a Claude Code hook! I need some details:

1. **What should this hook do?**
   Examples:
   - Auto-format code after editing files
   - Validate bash commands before execution
   - Add context when user submits prompts
   - Prevent access to sensitive files
   - Run tests after file changes

2. **When should it trigger?**
   - PreToolUse (before tool execution)
   - PostToolUse (after tool execution)
   - UserPromptSubmit (when user sends message)
   - Stop (when Claude finishes responding)
   - SubagentStop (when subagent finishes)
   - SessionStart (when session begins)
   - SessionEnd (when session ends)
   - Notification (when notification sent)
   - PermissionRequest (when permission requested)

3. **Which tools should it match?**
   - Specific tool (Write, Edit, Bash, Read, etc.)
   - Multiple tools (Write|Edit)
   - All tools (*)
   - MCP tools (mcp__server__tool)

4. **What should it return?**
   - Simple exit code (0 = success, 2 = block)
   - JSON with decision control
   - Additional context for Claude
   - Modified tool inputs

5. **Scope:**
   - User-level (`~/.claude/settings.json`)
   - Project-level (`.claude/settings.json`)
   - Local project (`.claude/settings.local.json`)
```

### 2. Determine Hook Type

**Bash Command Hook:**
```json
{
  "type": "command",
  "command": "/path/to/script.sh"
}
```
- Runs a shell command
- Fast, deterministic
- Good for validation, formatting

**Prompt-based Hook:**
```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude should stop: $ARGUMENTS"
}
```
- Uses LLM for decision
- Context-aware, intelligent
- Good for complex decisions (Stop, SubagentStop)

### 3. Choose Hook Event

#### PreToolUse
Runs before tool executes.

**Use for:**
- Validate inputs
- Auto-approve safe operations
- Block dangerous commands
- Modify tool parameters

**JSON Output:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "Why this decision",
    "updatedInput": {
      "field": "new value"
    }
  }
}
```

#### PostToolUse
Runs after tool completes.

**Use for:**
- Auto-format code
- Run linters
- Validate outputs
- Log operations

**JSON Output:**
```json
{
  "decision": "block" | undefined,
  "reason": "Why blocking",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Extra info for Claude"
  }
}
```

#### UserPromptSubmit
Runs when user submits prompt.

**Use for:**
- Add context automatically
- Validate prompts
- Block sensitive prompts
- Inject current time/date

**JSON Output:**
```json
{
  "decision": "block" | undefined,
  "reason": "Why blocking",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Extra context"
  }
}
```

#### Stop / SubagentStop
Runs when Claude/subagent finishes.

**Use for:**
- Verify tasks completed
- Continue if work remains
- Intelligent stoppage control

**JSON Output:**
```json
{
  "decision": "block" | undefined,
  "reason": "Why must continue"
}
```

#### SessionStart
Runs when session starts.

**Use for:**
- Load environment variables
- Set up development context
- Install dependencies
- Inject initial context

**JSON Output:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Initial context"
  }
}
```

**Special:** Can persist environment variables:
```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
fi
```

#### SessionEnd
Runs when session ends.

**Use for:**
- Cleanup tasks
- Save session stats
- Log session data

### 4. Create Hook Script

For bash command hooks, create a script:

**Template:**
```bash
#!/usr/bin/env bash

# Read JSON input from stdin
INPUT=$(cat)

# Parse JSON (requires jq)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Your validation logic here
if [[ condition ]]; then
  echo "Error message" >&2
  exit 2  # Block operation
fi

# Success
exit 0
```

**Python Template:**
```python
#!/usr/bin/env python3
import json
import sys

# Read JSON input
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

# Your logic here
if condition:
    # Block with error
    print("Error message", file=sys.stderr)
    sys.exit(2)

# Or return JSON for control
output = {
    "decision": "approve",
    "reason": "Auto-approved"
}
print(json.dumps(output))
sys.exit(0)
```

### 5. Configure in settings.json

Add hook configuration:

**Basic Hook:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh"
          }
        ]
      }
    ]
  }
}
```

**Multiple Hooks:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh",
            "timeout": 30
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/lint.sh",
            "timeout": 60
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py"
          }
        ]
      }
    ]
  }
}
```

**No Matcher (events without tools):**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/add-context.sh"
          }
        ]
      }
    ]
  }
}
```

### 6. Hook Input Reference

Each event receives JSON on stdin:

**Common fields:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/dir",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse"
}
```

**PreToolUse/PostToolUse:**
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": { /* PostToolUse only */
    "success": true
  }
}
```

**UserPromptSubmit:**
```json
{
  "prompt": "User's submitted message"
}
```

**Stop/SubagentStop:**
```json
{
  "stop_hook_active": false
}
```

### 7. Exit Codes

- **0**: Success
  - stdout shown in verbose mode (Ctrl+O)
  - For UserPromptSubmit/SessionStart: stdout added to context
  - JSON parsed if present

- **2**: Blocking error
  - stderr shown to Claude
  - Operation blocked (behavior varies by event)
  - JSON in stdout ignored

- **Other**: Non-blocking warning
  - stderr shown in verbose mode
  - Execution continues

### 8. Test the Hook

**Test script directly:**
```bash
# Create test input
echo '{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "test.txt",
    "content": "hello"
  }
}' | .claude/hooks/your-hook.sh

# Check exit code
echo $?
```

**Test in Claude Code:**
```
1. Add hook to settings.json
2. Restart Claude Code
3. Run /hooks to verify it's loaded
4. Trigger the hook (e.g., write a file)
5. Check verbose mode (Ctrl+O) for output
```

**Debug mode:**
```bash
claude --debug
# Shows hook execution details
```

### 9. Provide Configuration

Show the complete configuration:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

## Hook Examples

### Example 1: Auto-Format Python Files

**Hook script** (`.claude/hooks/format-python.sh`):
```bash
#!/usr/bin/env bash
INPUT=$(cat)

# Get file path
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only process .py files
if [[ "$FILE_PATH" == *.py ]]; then
  # Run black formatter
  python -m black "$FILE_PATH" 2>&1

  if [[ $? -eq 0 ]]; then
    echo "Formatted: $FILE_PATH" >&2
  fi
fi

exit 0
```

**Configuration:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format-python.sh"
          }
        ]
      }
    ]
  }
}
```

### Example 2: Validate Bash Commands

**Hook script** (`.claude/hooks/validate-bash.py`):
```python
#!/usr/bin/env python3
import json
import sys
import re

# Dangerous patterns
DANGEROUS = [
    (r'\brm\s+-rf\s+/', 'Dangerous: rm -rf on root'),
    (r'>\s*/dev/sd[a-z]', 'Dangerous: writing to block device'),
    (r'\bcurl\s+.*\|\s*bash', 'Dangerous: piping curl to bash'),
]

try:
    data = json.load(sys.stdin)
except:
    sys.exit(1)

if data.get('tool_name') != 'Bash':
    sys.exit(0)

command = data.get('tool_input', {}).get('command', '')

# Check for dangerous patterns
for pattern, message in DANGEROUS:
    if re.search(pattern, command):
        print(f"⚠️  {message}", file=sys.stderr)
        print(f"Command: {command}", file=sys.stderr)
        sys.exit(2)  # Block

sys.exit(0)  # Allow
```

**Configuration:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py"
          }
        ]
      }
    ]
  }
}
```

### Example 3: Add Timestamp to Prompts

**Hook script** (`.claude/hooks/add-timestamp.sh`):
```bash
#!/usr/bin/env bash

# Output current timestamp
echo "Current time: $(date '+%Y-%m-%d %H:%M:%S %Z')"

exit 0
```

**Configuration:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/add-timestamp.sh"
          }
        ]
      }
    ]
  }
}
```

### Example 4: Auto-Approve Documentation Reads

**Hook script** (`.claude/hooks/auto-approve-docs.py`):
```python
#!/usr/bin/env python3
import json
import sys

data = json.load(sys.stdin)

if data.get('tool_name') != 'Read':
    sys.exit(0)

file_path = data.get('tool_input', {}).get('file_path', '')

# Auto-approve docs
if any(file_path.endswith(ext) for ext in ['.md', '.txt', '.json', '.yaml']):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Documentation file auto-approved"
        },
        "suppressOutput": True
    }
    print(json.dumps(output))
    sys.exit(0)

sys.exit(0)
```

**Configuration:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/auto-approve-docs.py"
          }
        ]
      }
    ]
  }
}
```

### Example 5: Prevent Sensitive File Access

**Hook script** (`.claude/hooks/block-secrets.sh`):
```bash
#!/usr/bin/env bash
INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Block sensitive files
if [[ "$FILE_PATH" =~ \.env ||
      "$FILE_PATH" =~ secrets/ ||
      "$FILE_PATH" =~ \.aws/ ]]; then
  echo "⛔ Access to sensitive file blocked: $FILE_PATH" >&2
  exit 2
fi

exit 0
```

**Configuration:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block-secrets.sh"
          }
        ]
      }
    ]
  }
}
```

### Example 6: Intelligent Stop Hook (Prompt-based)

**Configuration:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate whether Claude should stop. Context: $ARGUMENTS\n\nCheck if:\n1. All tasks are complete\n2. Tests are passing\n3. No errors need addressing\n\nRespond with JSON: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Example 7: Session Setup Hook

**Hook script** (`.claude/hooks/session-setup.sh`):
```bash
#!/usr/bin/env bash

# Set up environment for session
if [ -n "$CLAUDE_ENV_FILE" ]; then
  # Load nvm
  source ~/.nvm/nvm.sh
  nvm use 20

  # Capture environment changes
  export -p >> "$CLAUDE_ENV_FILE"

  # Add custom variables
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
fi

# Add context
echo "Development environment initialized"
echo "Node version: $(node --version)"

exit 0
```

**Configuration:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-setup.sh"
          }
        ]
      }
    ]
  }
}
```

## Matcher Patterns

**Exact match:**
```json
"matcher": "Write"
```

**Multiple tools (regex):**
```json
"matcher": "Write|Edit|NotebookEdit"
```

**All tools:**
```json
"matcher": "*"
```
Or:
```json
"matcher": ""
```

**MCP tools:**
```json
"matcher": "mcp__github__.*"
"matcher": "mcp__.*__write.*"
```

**Event-specific matchers:**

Notification:
```json
"matcher": "permission_prompt"
"matcher": "idle_prompt"
```

PreCompact:
```json
"matcher": "manual"
"matcher": "auto"
```

SessionStart:
```json
"matcher": "startup"
"matcher": "resume"
"matcher": "clear"
```

## Environment Variables

Available in hook scripts:

- `$CLAUDE_PROJECT_DIR` - Absolute path to project root
- `$CLAUDE_CODE_REMOTE` - "true" if remote/web, empty if local
- `$CLAUDE_ENV_FILE` - (SessionStart only) File to persist env vars
- Standard environment variables

## Best Practices

### DO:
✅ Keep hooks fast (<100ms recommended)
✅ Provide clear error messages
✅ Use appropriate exit codes
✅ Quote variables in bash: `"$VAR"`
✅ Validate inputs before processing
✅ Test thoroughly before deploying
✅ Use `$CLAUDE_PROJECT_DIR` for portability
✅ Document what your hook does

### DON'T:
❌ Run slow operations (full test suites)
❌ Block legitimate operations unnecessarily
❌ Use hooks for everything (be selective)
❌ Forget to handle errors
❌ Skip input validation
❌ Hardcode absolute paths
❌ Leave debug output in production

## Security Considerations

**⚠️ USE AT YOUR OWN RISK**

Hooks execute arbitrary commands:
- Can modify/delete any files
- Can access sensitive data
- Can cause data loss
- Anthropic provides no warranty

**Best practices:**
- Validate and sanitize inputs
- Quote all variables
- Block path traversal (`..`)
- Use absolute paths
- Skip sensitive files
- Test in safe environment first

## Troubleshooting

### Hook Not Running

**Check:**
1. Hook is in `settings.json` correctly
2. Matcher pattern is correct (case-sensitive)
3. Script has execute permissions: `chmod +x script.sh`
4. Script shebang is correct: `#!/usr/bin/env bash`
5. Restart Claude Code after config changes

**Debug:**
```bash
# Run with debug mode
claude --debug

# Check hook execution in output
# Shows: "Executing hooks for PostToolUse:Write"
```

### Hook Errors

**Check:**
1. Script runs standalone: `echo '{}' | ./script.sh`
2. Exit code is correct: `echo $?`
3. JSON output is valid: `./script.sh | jq .`
4. Timeout is sufficient (default: 60s)

**View errors:**
- Verbose mode: Ctrl+O
- Debug mode: `claude --debug`
- Check stderr output

### Permissions Issues

**Check:**
```bash
# Make script executable
chmod +x .claude/hooks/script.sh

# Verify permissions
ls -la .claude/hooks/
```

### JSON Parse Errors

**Validate JSON:**
```bash
# Test JSON output
echo '{}' | ./script.sh | jq .

# Common issues:
# - Missing quotes
# - Trailing commas
# - Single quotes instead of double
```

## Resources

- **Official Hook Docs:** `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_hooks.md`
- **Hook Guide:** `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_hooks-guide.md`
- **Settings Reference:** `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_settings.md`
- **Project Guide:** `.claude/docs/creating-components.md`
