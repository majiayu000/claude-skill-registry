---
name: observability-analyzer
description: Query and analyze Claude Code observability data (metrics, logs, traces). Use when analyzing performance, costs, errors, tool usage, sessions, conversations, or subagents.
---

# Observability Analyzer

Query Claude Code telemetry and generate insights from metrics, logs, and traces. Works with both default OTEL telemetry and enhanced hook-based telemetry.

## Data Sources

| Source | Job Name | Contains |
|--------|----------|----------|
| Default OTEL | `claude_code` | API metrics, token usage, costs |
| Enhanced Hooks | `claude_code_enhanced` | Sessions, conversations, tools, subagents |

## Operations

### `query-metrics <promql>`
Execute PromQL query against Prometheus.
```bash
query-metrics 'sum(claude_code_token_usage)[7d]'
```

### `query-logs <logql>`
Execute LogQL query against Loki.
```bash
query-logs '{job="claude_code_enhanced", event_type="tool_call"} | json' --since 24h
```

### `analyze-errors`
Detect and group error patterns from enhanced telemetry.
```logql
{job="claude_code_enhanced", event_type="tool_result", status="error"} | json
```
**Output**: Error types, frequencies, affected tools, recommendations.

### `analyze-performance`
Identify slow operations and response sizes.
```logql
{job="claude_code_enhanced", event_type="tool_result"} | json | response_length > 50000
```
**Output**: Large responses, estimated token costs, slow patterns.

### `analyze-costs`
Calculate token usage from content size estimates.
```logql
sum by (repo) (sum_over_time({job="claude_code_enhanced", event_type="context_utilization"} | json | unwrap estimated_session_tokens [24h]))
```
**Output**: Token estimates by repo, session costs, projections.

### `analyze-tools`
Tool usage statistics and sequences.
```logql
sum by (tool) (count_over_time({job="claude_code_enhanced", event_type="tool_call"} | json [24h]))
```
**Output**: Call frequency, success rates, tool sequences, common patterns.

### `analyze-sessions`
Session lifecycle and duration analytics.
```logql
{job="claude_code_enhanced", event_type="session_end"} | json
```
**Output**: Session durations, turn counts, tools per session, termination reasons.

### `analyze-conversations`
Conversation and prompt analytics.
```logql
sum by (pattern) (count_over_time({job="claude_code_enhanced", event_type="user_prompt"} | json [24h]))
```
**Output**: Prompt patterns (question/debugging/creation/ultrathink), turn distribution.

### `analyze-subagents`
Subagent/Task tool usage.
```logql
{job="claude_code_enhanced", event_type="tool_call", tool="Task"} | json
```
**Output**: Subagent types used, completion rates, parallel execution patterns.

### `analyze-skills`
Skill invocation analytics.
```logql
sum by (skill_name) (count_over_time({job="claude_code_enhanced", event_type="skill_usage"} | json [24h]))
```
**Output**: Most used skills, skill usage by repo, trends.

### `analyze-context`
Context window utilization.
```logql
{job="claude_code_enhanced", event_type="context_utilization"} | json | context_percentage > 50
```
**Output**: High utilization sessions, compaction events, token efficiency.

### `analyze-repos`
Repository/project activity.
```logql
sum by (repo, tool) (count_over_time({job="claude_code_enhanced", event_type="tool_call"} | json [24h]))
```
**Output**: Activity per repo, tool usage by project, branch patterns.

### `generate-report`
Comprehensive analysis report (all dimensions).
**Output**: Markdown report with errors, performance, costs, sessions, conversations, tools.

## Key Queries

### Enhanced Telemetry (Loki)

```logql
# All events (last hour)
{job="claude_code_enhanced"} | json

# Session analytics
{job="claude_code_enhanced", event_type="session_end"} | json | duration_seconds > 300

# Tool errors
{job="claude_code_enhanced", event_type="tool_result", status="error"} | json

# High context usage
{job="claude_code_enhanced", event_type="context_utilization"} | json | context_percentage > 75

# Subagent spawns
{job="claude_code_enhanced", event_type="tool_call", tool="Task"} | json

# Skill invocations
{job="claude_code_enhanced", event_type="skill_usage"} | json

# Prompt patterns
{job="claude_code_enhanced", event_type="user_prompt"} | json | pattern="ultrathink"

# Tool sequences
{job="claude_code_enhanced", event_type="tool_call"} | json | line_format "{{.tool_name}} → {{.previous_tool}}"

# Context compaction
{job="claude_code_enhanced", event_type="context_compact"} | json

# Permission requests
{job="claude_code_enhanced", event_type="permission_request"} | json
```

### Default OTEL (Prometheus)

```promql
# Total token usage (7 days)
sum(increase(claude_code_token_usage[7d]))

# Error rate by tool
sum by (tool_name) (rate(claude_code_tool_result{status="failure"}[1h]))

# P95 tool latency
histogram_quantile(0.95, claude_code_tool_duration_bucket)

# Daily costs
sum(increase(claude_code_cost_usage[24h]))
```

## Event Types Reference

| Event Type | Description | Key Fields |
|------------|-------------|------------|
| `session_start` | Session initialization | source, permission_mode |
| `session_end` | Session termination | duration_seconds, turn_count, tools_used |
| `user_prompt` | User message submitted | pattern, prompt_length, estimated_tokens |
| `tool_call` | Tool invocation | tool_name, tool_details, sequence_position |
| `tool_result` | Tool completion | status, response_length, is_error |
| `skill_usage` | Skill invoked | skill_name |
| `context_utilization` | Token estimate | estimated_session_tokens, context_percentage |
| `context_compact` | Compaction event | trigger (manual/auto) |
| `subagent_complete` | Task agent finished | total_subagents |
| `permission_request` | Permission dialog | notification_type |
| `notification` | System notification | notification_type |

## Grafana Dashboards

- **Claude Code Overview** - High-level metrics
- **Tool Performance** - Tool latencies and success rates
- **Cost Analysis** - Token usage and costs
- **Error Tracking** - Error patterns and trends
- **Session Analytics** - Session-level insights
- **Enhanced Analytics** - Model/skill/context/repo tracking
- **Deep Analytics** - Comprehensive conversation and tool analysis

Access: http://localhost:3000 (admin/admin)

## Scripts

- `scripts/query-prometheus.sh` - PromQL query helper
- `scripts/query-loki.sh` - LogQL query helper
- `scripts/analyze-errors.sh` - Error analysis automation
- `scripts/analyze-sessions.sh` - Session analytics
- `scripts/generate-report.sh` - Full analysis report
