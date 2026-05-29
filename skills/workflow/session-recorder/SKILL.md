---
name: session-recorder
description: This skill should be used when the user asks to "record session", "log interactions", "track session activity", "audit Claude usage", "create session logs", or when session recording is enabled. Provides instructions for the hybrid recording approach where Claude self-reports summaries of completed work.
version: 0.1.0
allowed-tools:
  - Bash
---

# Session Recorder

Records all Claude Code session interactions using a hybrid approach: automated hooks capture user messages and tool calls, while explicit self-reporting captures summaries of completed work.

## How It Works

The session recorder uses two complementary mechanisms:

### Automated Recording (via Hooks)

Four hooks automatically capture events without any action required:

| Hook | Event | What It Records |
|------|-------|-----------------|
| `SessionStart` | Session begins | Creates log file, records session ID and start time |
| `UserPromptSubmit` | User sends message | Records user message content and timestamp |
| `PostToolUse` | Tool completes | Records tool name, arguments, and result |
| `SessionEnd` | Session ends | Updates end timestamp, calculates statistics |

### Self-Reporting (Explicit)

Self-report summaries of completed work to capture reasoning and context that hooks cannot observe. This provides the "why" behind the "what" recorded by hooks.

## Self-Reporting Instructions

### When to Self-Report

Report after completing significant work:

1. **Multi-step operations** - After completing a sequence of related actions
2. **Feature implementations** - After implementing new functionality
3. **Bug fixes** - After identifying and resolving issues
4. **Refactoring** - After restructuring code
5. **Configuration changes** - After modifying settings or environment
6. **Research conclusions** - After investigating and reaching decisions

### How to Self-Report

Execute the helper script with summary information:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/session-recorder/scripts/add_assistant_response.sh \
  --summary "Brief description of what was accomplished" \
  --actions "Specific actions taken" \
  --tools "Tool1,Tool2,Tool3"
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--summary` | Recommended | Brief description of accomplishment (1-2 sentences) |
| `--actions` | Optional | Comma-separated list of specific actions taken |
| `--tools` | Optional | Comma-separated list of tools used |

### Examples

**After implementing a feature:**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/session-recorder/scripts/add_assistant_response.sh \
  --summary "Implemented user authentication with JWT tokens" \
  --actions "Created auth middleware, added token validation, updated routes" \
  --tools "Write,Edit,Bash"
```

**After fixing a bug:**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/session-recorder/scripts/add_assistant_response.sh \
  --summary "Fixed race condition in database connection pool" \
  --actions "Added mutex lock, implemented connection timeout" \
  --tools "Edit,Read"
```

**After research and decision:**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/session-recorder/scripts/add_assistant_response.sh \
  --summary "Analyzed performance bottleneck - recommending Redis caching" \
  --actions "Profiled application, identified database queries as bottleneck"
```

**After configuration:**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/session-recorder/scripts/add_assistant_response.sh \
  --summary "Configured CI/CD pipeline with GitHub Actions" \
  --actions "Created workflow file, added test and deploy stages" \
  --tools "Write"
```

## Log File Structure

Logs are stored in `.claude/session_logs/session_YYYY-MM-DD.json`:

```json
{
  "session_id": "UUID",
  "start_timestamp": "ISO-8601",
  "end_timestamp": "ISO-8601",
  "project_path": "/absolute/path",
  "interactions": [
    {
      "interaction_id": "UUID",
      "timestamp": "ISO-8601",
      "type": "user_message|tool_call|tool_result|assistant_summary",
      "content": "...",
      "metadata": {}
    }
  ]
}
```

### Interaction Types

| Type | Source | Content |
|------|--------|---------|
| `user_message` | UserPromptSubmit hook | User's message text |
| `tool_call` | PostToolUse hook | Tool name and arguments |
| `tool_result` | PostToolUse hook | Tool output (truncated if large) |
| `assistant_summary` | Self-reporting | Summary, actions, tools used |

## Best Practices

### Effective Summaries

Write summaries that capture intent and context:

- **Good**: "Refactored authentication to use middleware pattern for better separation of concerns"
- **Poor**: "Changed some files"

- **Good**: "Fixed XSS vulnerability by sanitizing user input in comment form"
- **Poor**: "Fixed bug"

### When NOT to Self-Report

Skip self-reporting for:

- Simple file reads (already captured by hooks)
- Single tool calls (already captured by hooks)
- Trivial operations with no decision-making
- Intermediate steps within a larger operation (report at completion)

### Frequency

Self-report at natural completion points, not after every action. One summary per logical unit of work is ideal.

## Troubleshooting

### Logs Not Created

Verify `jq` is installed:
```bash
which jq
```

Check directory permissions:
```bash
ls -la .claude/session_logs/
```

### Self-Report Fails

Ensure script is executable:
```bash
chmod +x ${CLAUDE_PLUGIN_ROOT}/skills/session-recorder/scripts/add_assistant_response.sh
```

Test manually:
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/session-recorder/scripts/add_assistant_response.sh --summary "Test"
```

## Dependencies

- `jq` - JSON processing (required)
- `uuidgen` - UUID generation (usually pre-installed)

Install on Ubuntu/Debian:
```bash
sudo apt-get install jq uuid-runtime
```

Install on macOS:
```bash
brew install jq
```

## Additional Resources

### Reference Files

- **`references/log-analysis.md`** - Guide to analyzing session logs
- **`references/integration.md`** - Integrating with external tools

### Scripts

- **`scripts/add_assistant_response.sh`** - Self-reporting helper
- **`hooks/session_init.sh`** - Session initialization
- **`hooks/record_user_prompt.sh`** - User message recording
- **`hooks/record_tool_result.sh`** - Tool usage recording
- **`hooks/session_finalize.sh`** - Session finalization
