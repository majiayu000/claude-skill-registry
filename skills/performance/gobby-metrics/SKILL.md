---
name: gobby-metrics
description: This skill should be used when the user asks to "/gobby-metrics", "tool metrics", "usage stats", "performance report". View tool usage metrics, performance statistics, and identify failing tools.
---

# /gobby-metrics - Metrics and Statistics Skill

This skill retrieves usage metrics via the gobby-metrics MCP server. Parse the user's input to determine which subcommand to execute.

## Subcommands

### `/gobby-metrics tools` - Tool usage statistics
Call `gobby-metrics.get_tool_metrics` with:
- `server_name`: Optional filter by server name
- `tool_name`: Optional filter by tool name
- `project_id`: Optional project scope

Returns per-tool statistics:
- Call count
- Success rate
- Average latency
- Last used

Example: `/gobby-metrics tools` → `get_tool_metrics()`
Example: `/gobby-metrics tools gobby-tasks` → `get_tool_metrics(server_name="gobby-tasks")`
Example: `/gobby-metrics tools gobby-tasks create_task` → `get_tool_metrics(server_name="gobby-tasks", tool_name="create_task")`

### `/gobby-metrics top` - Get top tools by usage
Call `gobby-metrics.get_top_tools` with:
- `limit`: Max tools to show (default 10)
- `order_by`: Sort by "usage" (default), "success_rate", or "latency"
- `project_id`: Optional project scope

Returns tools ranked by the specified metric.

Example: `/gobby-metrics top` → `get_top_tools()`
Example: `/gobby-metrics top 20 by latency` → `get_top_tools(limit=20, order_by="latency")`

### `/gobby-metrics failing` - Get failing tools
Call `gobby-metrics.get_failing_tools` with:
- `threshold`: Failure rate threshold (default 0.1 = 10%)
- `limit`: Max results
- `project_id`: Optional project scope

Returns tools with failure rates above the threshold.

Example: `/gobby-metrics failing` → `get_failing_tools()`
Example: `/gobby-metrics failing 0.05` → `get_failing_tools(threshold="0.05")`

### `/gobby-metrics success <server> <tool>` - Get tool success rate
Call `gobby-metrics.get_tool_success_rate` with:
- `server_name`: (required) Server name
- `tool_name`: (required) Tool name
- `project_id`: (required) Project ID

Returns detailed success rate for a specific tool.

Example: `/gobby-metrics success gobby-tasks create_task` → `get_tool_success_rate(server_name="gobby-tasks", tool_name="create_task", project_id="<project_id>")`

### `/gobby-metrics reset` - Reset metrics
Call `gobby-metrics.reset_metrics` with:
- `project_id`: Optional - reset for specific project
- `server_name`: Optional - reset for specific server
- `tool_name`: Optional - reset for specific tool

Clears metrics data. Can scope to project, server, or specific tool.

Example: `/gobby-metrics reset` → `reset_metrics()`
Example: `/gobby-metrics reset gobby-tasks` → `reset_metrics(server_name="gobby-tasks")`

### `/gobby-metrics cleanup` - Clean up old metrics
Call `gobby-metrics.cleanup_old_metrics` to delete metrics older than retention period (default 7 days).

Example: `/gobby-metrics cleanup` → `cleanup_old_metrics()`

### `/gobby-metrics retention` - Get retention statistics
Call `gobby-metrics.get_retention_stats` to see metrics age distribution and storage info.

Example: `/gobby-metrics retention` → `get_retention_stats()`

## Response Format

After executing the appropriate MCP tool, present the results clearly:
- For tools: Table with tool name, call count, success rate, avg latency
- For top: Ranked list with the sorting metric highlighted
- For failing: Table of failing tools with failure rates
- For success: Detailed success rate with context
- For reset: Confirmation of what was reset
- For cleanup: Summary of deleted metrics
- For retention: Statistics about metrics age

## Metrics Concepts

- **Call count**: Total number of tool invocations
- **Success rate**: Percentage of calls that completed without error
- **Latency**: Response time in milliseconds
- **Retention**: How long metrics are kept (default 7 days)

## Error Handling

If the subcommand is not recognized, show available subcommands:
- tools, top, failing, success, reset, cleanup, retention
