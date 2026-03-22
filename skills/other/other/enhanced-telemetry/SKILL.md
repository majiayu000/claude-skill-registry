---
name: enhanced-telemetry
description: Comprehensive Claude Code telemetry via 10 hooks capturing sessions, conversations, tools, subagents, context, permissions, and repository analytics. Use when analyzing detailed usage patterns beyond default OTEL.
---

# Enhanced Telemetry v2

Captures comprehensive Claude Code metrics via ALL 10 available hooks, providing deep observability beyond default OTEL telemetry.

## What It Captures

### Session Analytics
- Session lifecycle (start/end)
- Session duration
- Session source (startup/resume/clear/compact)
- Session termination reason
- Permission mode

### Conversation Analytics
- Turn count per session
- Prompt patterns (question/debugging/creation/ultrathink)
- Prompt length and token estimates
- Conversation style distribution

### Tool Analytics
- Tool call frequency
- Tool sequences (previous → current)
- Tool error rates
- Response sizes and token estimates
- File types accessed

### Subagent Analytics
- Subagents spawned per session
- Subagent types (Explore, Plan, general-purpose, etc.)
- Subagent completion tracking

### Context Analytics
- Estimated token usage
- Context window utilization percentage
- Context compaction events (manual vs auto)
- Token accumulation tracking

### Repository Analytics
- Activity per repository
- Tool usage by project
- Branch-level tracking

### Permission Analytics
- Permission requests
- Permission types
- Notification tracking

## 10 Hooks Instrumented

| Hook | Event Type | What's Captured |
|------|------------|-----------------|
| `SessionStart` | `session_start` | Source, permission mode, git info |
| `SessionEnd` | `session_end` | Duration, turns, tools, errors, subagents |
| `UserPromptSubmit` | `user_prompt` | Pattern, length, tokens, prompt hash |
| `PreToolUse` | `tool_call` | Tool name, details, sequence position |
| `PostToolUse` | `tool_result` | Status, response size, errors |
| `SubagentStop` | `subagent_complete` | Subagent count |
| `PermissionRequest` | `permission_request` | Notification type |
| `PreCompact` | `context_compact` | Trigger (manual/auto), token estimate |
| `Notification` | `notification` | Notification type |
| `Stop` | `session_end` | Same as SessionEnd |

## Configuration

**Settings file**: `.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": ["python3 .claude/hooks/enhanced-telemetry.py SessionStart"],
    "SessionEnd": ["python3 .claude/hooks/enhanced-telemetry.py SessionEnd"],
    "UserPromptSubmit": ["python3 .claude/hooks/enhanced-telemetry.py UserPromptSubmit"],
    "PreToolUse": [{"matcher": ".*", "hooks": ["python3 .claude/hooks/enhanced-telemetry.py PreToolUse"]}],
    "PostToolUse": [{"matcher": ".*", "hooks": ["python3 .claude/hooks/enhanced-telemetry.py PostToolUse"]}],
    "SubagentStop": ["python3 .claude/hooks/enhanced-telemetry.py SubagentStop"],
    "PermissionRequest": ["python3 .claude/hooks/enhanced-telemetry.py PermissionRequest"],
    "PreCompact": ["python3 .claude/hooks/enhanced-telemetry.py PreCompact"],
    "Notification": ["python3 .claude/hooks/enhanced-telemetry.py Notification"],
    "Stop": ["python3 .claude/hooks/enhanced-telemetry.py Stop"]
  }
}
```

## Viewing Data

### Grafana Dashboards
- **Enhanced Analytics**: http://localhost:3000/d/claude-code-enhanced
- **Deep Analytics**: http://localhost:3000/d/claude-code-deep

### LogQL Queries

```logql
# All enhanced telemetry
{job="claude_code_enhanced"} | json

# Session analytics
{job="claude_code_enhanced", event_type="session_end"} | json

# Tool calls
{job="claude_code_enhanced", event_type="tool_call"} | json

# Prompt patterns
sum by (pattern) (count_over_time({job="claude_code_enhanced", event_type="user_prompt"} | json [24h]))

# Skill usage
{job="claude_code_enhanced", event_type="skill_usage"} | json

# Context utilization
{job="claude_code_enhanced", event_type="context_utilization"} | json

# Tool sequences
{job="claude_code_enhanced", event_type="tool_call"} | json | line_format "{{.previous_tool}} → {{.tool_name}}"

# Subagent tracking
{job="claude_code_enhanced", event_type="tool_call", tool="Task"} | json

# Error analysis
{job="claude_code_enhanced", event_type="tool_result", status="error"} | json

# Context compaction
{job="claude_code_enhanced", event_type="context_compact"} | json
```

## Event Schemas

### session_start
```json
{
  "event": "session_start",
  "session_id": "abc123",
  "source": "startup",
  "permission_mode": "default",
  "cwd": "/mnt/c/data/github/project",
  "timestamp": "2025-11-27T08:00:00Z",
  "git": {"repo_name": "project", "branch": "main"}
}
```

### session_end
```json
{
  "event": "session_end",
  "session_id": "abc123",
  "reason": "prompt_input_exit",
  "duration_seconds": 1847.5,
  "turn_count": 25,
  "tools_used": {"Read": 45, "Edit": 12, "Bash": 8},
  "tool_sequence": ["Read", "Edit", "Bash", "Read"],
  "subagents_spawned": 3,
  "error_count": 2,
  "timestamp": "2025-11-27T08:30:00Z"
}
```

### user_prompt
```json
{
  "event": "user_prompt",
  "turn_number": 5,
  "prompt_length": 256,
  "estimated_tokens": 64,
  "prompt_hash": "a1b2c3d4",
  "patterns": ["question", "debugging"],
  "timestamp": "2025-11-27T08:05:00Z"
}
```

### tool_call
```json
{
  "event": "tool_call",
  "tool_name": "Read",
  "tool_use_id": "xyz789",
  "tool_details": {"file_path": "/src/main.py", "file_type": ".py"},
  "sequence_position": 15,
  "previous_tool": "Glob",
  "timestamp": "2025-11-27T08:05:30Z"
}
```

### tool_result
```json
{
  "event": "tool_result",
  "tool_name": "Read",
  "tool_use_id": "xyz789",
  "response_length": 4500,
  "estimated_tokens": 1125,
  "is_error": false,
  "error_type": null,
  "timestamp": "2025-11-27T08:05:31Z"
}
```

### context_utilization
```json
{
  "event": "context_utilization",
  "estimated_session_tokens": 45000,
  "context_percentage": 22.5,
  "last_content_tokens": 5000,
  "turn_count": 15,
  "timestamp": "2025-11-27T08:10:00Z"
}
```

### context_compact
```json
{
  "event": "context_compact",
  "trigger": "auto",
  "has_custom_instructions": false,
  "session_turn_count": 45,
  "estimated_tokens_before": 180000,
  "timestamp": "2025-11-27T08:15:00Z"
}
```

## Files

```
.claude/
├── hooks/
│   └── enhanced-telemetry.py       # Main telemetry script (v2)
├── settings.json                    # Hook configurations
└── skills/
    └── enhanced-telemetry/
        └── SKILL.md                 # This documentation
```

## Requirements

- Python 3.x (in PATH)
- Loki running at localhost:3100
- Claude Code hooks enabled

## Troubleshooting

### No Data in Dashboards

1. **Check hooks configured**:
   ```bash
   cat .claude/settings.json | grep enhanced-telemetry
   ```

2. **Test script manually**:
   ```bash
   echo '{"tool_name":"Test"}' | python3 .claude/hooks/enhanced-telemetry.py PreToolUse
   ```

3. **Check Loki receiving data**:
   ```bash
   curl -s "http://localhost:3100/loki/api/v1/labels"
   # Should include: event_type, tool, repo, pattern, etc.
   ```

4. **Check Loki has enhanced data**:
   ```bash
   curl -s "http://localhost:3100/loki/api/v1/query?query={job=\"claude_code_enhanced\"}&limit=5"
   ```

### Hooks Not Running

- Ensure Claude Code started from project directory with `.claude/settings.json`
- Check settings.json is valid JSON: `python3 -m json.tool .claude/settings.json`
- Verify Python available: `which python3`

### Script Errors

- Check script permissions: `chmod +x .claude/hooks/enhanced-telemetry.py`
- Test with debug output: Run script manually and check stderr

## Integration with Other Skills

- **observability-analyzer**: Uses `{job="claude_code_enhanced"}` queries
- **observability-pattern-detector**: Detects patterns in enhanced data
- **observability-alert-manager**: Alerts on enhanced telemetry events
- **skill-improvement-from-observability**: Uses enhanced data for insights
