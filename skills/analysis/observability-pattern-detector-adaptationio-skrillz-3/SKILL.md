---
name: observability-pattern-detector
description: Automated pattern recognition in Claude Code telemetry. Use when detecting failures, slowness, anomalies, trends, inefficiencies, conversation patterns, or tool sequences.
---

# Observability Pattern Detector

Automated pattern recognition and anomaly detection in Claude Code telemetry data from enhanced hooks.

## Data Source

Primary: `{job="claude_code_enhanced"}` in Loki

## Operations

### `detect-failures`
Group similar failures and identify patterns.
```logql
{job="claude_code_enhanced", event_type="tool_result", status="error"} | json
```
**Algorithm**: Group by error_type → Calculate frequency → Rank by impact.
**Output**: Failure patterns with occurrences, affected tools, first/last seen, trend.

### `detect-slowness`
Identify large response patterns (proxy for slowness).
```logql
{job="claude_code_enhanced", event_type="tool_result"} | json | response_length > 100000
```
**Algorithm**: Flag responses >100k chars → Group by tool → Identify patterns.
**Output**: Slow operations with response sizes, affected tools.

### `detect-anomalies`
Statistical anomaly detection in sessions.
```logql
{job="claude_code_enhanced", event_type="session_end"} | json | turn_count > 50
```
**Methods**: High turn count, long duration, many errors per session.
**Output**: Anomalous sessions with metrics, likely cause.

### `detect-trends`
Long-term trend analysis.
```logql
sum(count_over_time({job="claude_code_enhanced", event_type="tool_call"} [1d]))
```
**Metrics**: Tool usage trend, error rate trend, session frequency trend.
**Output**: Trends with direction (increasing/decreasing/stable), rate.

### `detect-waste`
Identify inefficiencies (redundant operations).
```logql
{job="claude_code_enhanced", event_type="tool_call"} | json | line_format "{{.tool_name}}:{{.previous_tool}}"
```
**Patterns**:
- Multiple reads of same file (Read→Read)
- Repeated failed operations
- Excessive Glob before Read
- Many small edits vs one large edit
**Output**: Waste patterns with occurrences, recommendations.

### `detect-conversation-patterns`
Analyze user prompt patterns.
```logql
sum by (pattern) (count_over_time({job="claude_code_enhanced", event_type="user_prompt"} | json [24h]))
```
**Patterns**:
- Question frequency (pattern="question")
- Debugging sessions (pattern="debugging")
- Creation tasks (pattern="creation")
- Ultrathink usage (pattern="ultrathink")
**Output**: Conversation style distribution, trends.

### `detect-tool-sequences`
Identify common tool call sequences.
```logql
{job="claude_code_enhanced", event_type="tool_call"} | json | line_format "{{.previous_tool}} → {{.tool_name}}"
```
**Common Patterns**:
- Glob → Read (file discovery)
- Read → Edit (modify after read)
- Grep → Read (search then open)
- Task → Task (parallel agents)
**Output**: Sequence frequencies, unusual patterns.

### `detect-subagent-patterns`
Analyze Task tool usage patterns.
```logql
{job="claude_code_enhanced", event_type="tool_call", tool="Task"} | json
```
**Patterns**:
- Subagent types distribution
- Parallel spawning patterns
- Subagent success rates
**Output**: Subagent usage analytics, recommendations.

### `detect-context-issues`
Identify context window problems.
```logql
{job="claude_code_enhanced", event_type="context_compact"} | json
```
**Patterns**:
- Frequent auto-compaction
- High context usage sessions
- Large response accumulation
**Output**: Context management issues, optimization suggestions.

### `detect-permission-patterns`
Analyze permission request patterns.
```logql
{job="claude_code_enhanced", event_type="permission_request"} | json
```
**Patterns**:
- Frequent permission requests
- Permission types distribution
- Permission denials
**Output**: Permission friction points, automation opportunities.

### `detect-repo-patterns`
Repository activity patterns.
```logql
sum by (repo) (count_over_time({job="claude_code_enhanced", event_type="tool_call"} | json [7d]))
```
**Patterns**:
- Most active repos
- Tool usage by repo
- Error rates by repo
**Output**: Project-level insights, cross-repo comparisons.

## Example Output

```json
{
  "failure_patterns": [
    {
      "pattern_id": "file_not_found",
      "signature": "File does not exist",
      "occurrences": 23,
      "affected_tools": ["Read", "Edit"],
      "trend": "stable",
      "recommendation": "Add file existence check before operations"
    }
  ],
  "tool_sequence_patterns": [
    {
      "sequence": "Glob → Read → Edit",
      "occurrences": 156,
      "context": "Standard file modification flow"
    }
  ],
  "conversation_patterns": [
    {
      "pattern": "debugging",
      "percentage": 35,
      "avg_turns": 12,
      "common_tools": ["Bash", "Read", "Grep"]
    }
  ],
  "context_issues": [
    {
      "issue": "auto_compaction_frequent",
      "sessions_affected": 5,
      "recommendation": "Use more focused queries, split large tasks"
    }
  ]
}
```

## Pattern Detection Queries

### Failure Patterns
```logql
# Group errors by type
sum by (error_type, tool) (count_over_time({job="claude_code_enhanced", event_type="tool_result", status="error"} | json [24h]))

# Error timeline
{job="claude_code_enhanced", event_type="tool_result", status="error"} | json | line_format "{{.timestamp}} {{.tool_name}}: {{.error_type}}"
```

### Tool Sequence Patterns
```logql
# Most common transitions
{job="claude_code_enhanced", event_type="tool_call"} | json | previous_tool != "" | line_format "{{.previous_tool}} → {{.tool_name}}"
```

### Session Anomalies
```logql
# Long sessions
{job="claude_code_enhanced", event_type="session_end"} | json | duration_seconds > 3600

# High error sessions
{job="claude_code_enhanced", event_type="session_end"} | json | error_count > 5

# High turn sessions
{job="claude_code_enhanced", event_type="session_end"} | json | turn_count > 30
```

### Context Patterns
```logql
# Auto compactions
{job="claude_code_enhanced", event_type="context_compact", trigger="auto"} | json

# High utilization
{job="claude_code_enhanced", event_type="context_utilization"} | json | context_percentage > 80
```

## Scripts

- `scripts/detect-failures.sh` - Failure pattern detection
- `scripts/detect-anomalies.sh` - Statistical anomaly detection
- `scripts/detect-trends.sh` - Trend analysis
- `scripts/detect-sequences.sh` - Tool sequence analysis
- `scripts/generate-pattern-report.sh` - Full pattern report
