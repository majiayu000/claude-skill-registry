---
name: mcp-status
description: Check connectivity status of all Jocko Fuel MCP servers
user-invocable: true
---

You are helping the user check the health and connectivity of all Jocko Fuel MCP servers.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool to load each MCP server's tools. Run these four ToolSearch calls:
1. `+snowflake`
2. `+promo-order`
3. `+product-research`
4. `+jocko-imagery`

Follow these steps:

### Step 1: Check Each Server

For each MCP server, attempt to call its status or help tool:

- **Snowflake**: Call `mcp__snowflake__check_status` to verify database connectivity and role/warehouse configuration
- **Promo Order**: Call `mcp__promo-order__get_help` or any lightweight read tool to verify connectivity
- **Product Research**: Call `mcp__product-research__get_help` or any lightweight read tool to verify connectivity
- **Jocko Imagery**: Call `mcp__jocko-imagery__get_help` or any lightweight read tool to verify connectivity

### Step 2: Report Status

Present a status table:

| Server | Status | Details |
|--------|--------|---------|
| Snowflake | OK / ERROR | Database, role, warehouse info |
| Promo Order | OK / ERROR | Connection details |
| Product Research | OK / ERROR | Connection details |
| Jocko Imagery | OK / ERROR | Connection details |

### Step 3: Diagnose Issues

If any server is unreachable:
- Check if the ToolSearch found tools for that server (tools not found = server not registered)
- Check if the tool call returned an auth error (token may be expired or missing)
- Suggest verifying the relevant environment variable (`HORIZON_SNOWFLAKE_TOKEN`, `HORIZON_PROMO_TOKEN`, `HORIZON_RESEARCH_TOKEN`, `HORIZON_IMAGERY_TOKEN`)

### Error Handling

- If ToolSearch fails to find tools for a server, report it as "NOT REGISTERED" rather than "ERROR"
- If a tool call times out, report it as "TIMEOUT" and suggest retrying
- If all servers fail, suggest checking network connectivity and Horizon platform status
