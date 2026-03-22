---
name: logfire
description: Use for Pydantic Logfire observability, tracing, and debugging. Query exceptions, spans, logs with SQL. View traces in Logfire UI. 4 tools for application monitoring and error analysis.
version: 1.0.0
title: "Logfire"
status: active
---

# logfire Skill

Pydantic Logfire observability and tracing. Query application logs, find exceptions, analyze spans with SQL, and generate trace links.

## Context Efficiency

Traditional MCP approach:
- All 4 tools loaded at startup
- Estimated context: 2000 tokens

This skill approach:
- Metadata only: ~100 tokens
- Full instructions (when used): ~5k tokens
- Tool execution: 0 tokens (runs externally)

## How This Works

Instead of loading all MCP tool definitions upfront, this skill:
1. Tells you what tools are available (just names and brief descriptions)
2. You decide which tool to call based on the user's request
3. Generate a JSON command to invoke the tool
4. The executor handles the actual MCP communication

## Available Tools

- `find_exceptions_in_file`: Get the details about the 10 most recent exceptions on the file.
- `arbitrary_query`: Run an arbitrary query on the Pydantic Logfire database.

The SQL reference is available via the `sql_reference` tool.

- `logfire_link`: Creates a link to help the user to view the trace in the Logfire UI.
- `schema_reference`: The database schema for the Logfire DataFusion database.

This includes all tables, columns, and their types as well as descriptions.
For example:

```sql
-- The records table contains spans and logs.
CREATE TABLE records (
    message TEXT, -- The message of the record
    span_name TEXT, -- The name of the span, message is usually templated from this
    trace_id TEXT, -- The trace ID, identifies a group of spans in a trace
    exception_type TEXT, -- The type of the exception
    exception_message TEXT, -- The message of the exception
    -- other columns...
);
```
The SQL syntax is similar to Postgres, although the query engine is actually Apache DataFusion.

To access nested JSON fields e.g. in the `attributes` column use the `->` and `->>` operators.
You may need to cast the result of these operators e.g. `(attributes->'cost')::float + 10`.

You should apply as much filtering as reasonable to reduce the amount of data queried.
Filters on `start_timestamp`, `service_name`, `span_name`, `metric_name`, `trace_id` are efficient.


## Usage Pattern

When the user's request matches this skill's capabilities:

**Step 1: Identify the right tool** from the list above

**Step 2: Generate a tool call** in this JSON format:

```json
{
  "tool": "tool_name",
  "arguments": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**Step 3: Execute via bash:**

```bash
python .claude/skills/mcp-skills/executor.py --skill logfire --call 'YOUR_JSON_HERE'
```


## Getting Tool Details

If you need detailed information about a specific tool's parameters:

```bash
python .claude/skills/mcp-skills/executor.py --skill logfire --describe tool_name
```

This loads ONLY that tool's schema, not all tools.

## Examples

### Example 1: Simple tool call

User: "Find recent exceptions in main.py"

Your workflow:
1. Identify tool: `find_exceptions_in_file`
2. Generate call JSON
3. Execute:

```bash
python .claude/skills/mcp-skills/executor.py --skill logfire --call '{"tool": "find_exceptions_in_file", "arguments": {"filepath": "main.py"}}'
```

### Example 2: Get tool details first

```bash
python .claude/skills/mcp-skills/executor.py --skill logfire --describe arbitrary_query
```

Returns the full schema, then you can generate the appropriate call.

## Error Handling

If the executor returns an error:
- Check the tool name is correct
- Verify required arguments are provided
- Ensure the MCP server is accessible

## Performance Notes

Context usage comparison for this skill:

| Scenario | MCP (preload) | Skill (dynamic) |
|----------|---------------|-----------------|
| Idle | 2000 tokens | 100 tokens |
| Active | 2000 tokens | 5k tokens |
| Executing | 2000 tokens | 0 tokens |

Savings: ~-150% reduction in typical usage

---

*This skill was auto-generated from an MCP server configuration.*
*Generator: mcp_to_skill.py*
