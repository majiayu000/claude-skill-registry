---
name: chronos-data-flow
description: Test Chronos Docker stack data flow across container states. Run to verify Core, Query Service, and MCP connectivity, health endpoints, event creation/query, and end-to-end data flow. Triggers on "test data flow", "check data flow", "chronos health", "test chronos stack", "verify containers".
category: testing
color: green
displayName: Chronos Data Flow Test
---

# Chronos Data Flow Test

Tests the full data flow through the Chronos Docker stack across multiple container states.

## When invoked:

1. Run the data flow test script:
   ```bash
   bash tooling/data-flow-test/test-data-flow.sh
   ```

2. Analyze the output and report:
   - Which containers are up/down
   - Whether the stack is running in **standalone** (no PostgreSQL) or **full** mode
   - Which tests passed, failed, or were skipped
   - Root cause analysis for any failures

3. If specific sections were requested, use the appropriate flag:
   - `--state` — container state only
   - `--core` — Core tests only
   - `--query` — Query Service tests only
   - `--mcp` — MCP tests only
   - `--flow` — end-to-end data flow only
   - `--json` — append for machine-readable output

## Test Coverage

The script tests these data flow paths:

| Test Area | What's Checked |
|-----------|---------------|
| **Container State** | Port reachability for Core (3280), Query Service (3283), MCP (3904), PostgreSQL (3284) |
| **Core Health** | `/health`, `/api/v1/stats`, `/api/v1/events/query`, `/api/v1/projections`, `/api/v1/schemas`, `/api/v1/snapshots`, `/api/v1/topology` |
| **Query Service Health** | `/api/health`, `/api/health/live`, `/api/health/ready` |
| **Query Service Proxy** | `/api/tenant`, `/api/tenant/usage`, `/api/events`, `/api/events/streams`, `/api/events/types`, `/api/openapi` |
| **MCP** | `/health` |
| **E2E Write Path** | Create event via Query Service (or Core fallback) |
| **E2E Read Path** | Read event back from Core, read via Query Service, verify in streams/types lists |
| **Query DSL** | Execute DSL query for the test entity |

## Common Failure Patterns

- **Core DOWN, Query Service UP**: Query Service health will show `backend: degraded`. Event proxy calls will fail.
- **Query Service DOWN, Core UP**: Direct Core tests pass. Flow test falls back to writing directly to Core.
- **Standalone mode (no PostgreSQL)**: Tenant/usage endpoints return dev tenant. Usage metering is skipped. This is expected.
- **404 on Query Service endpoints**: Route mismatch — check if MCP is using `/api/v1/` paths instead of `/api/` paths.

## Environment Variables

Override default ports if your Docker mapping differs:

```bash
CORE_PORT=3280 QUERY_PORT=3283 MCP_PORT=3904 bash tooling/data-flow-test/test-data-flow.sh
```

## Docker Compose

To bring the stack up/down for testing:

```bash
# Start
docker compose -f ~/Projects/alphaSigmaPro/wallet/docker/docker-compose.chronos.yml up -d

# Stop
docker compose -f ~/Projects/alphaSigmaPro/wallet/docker/docker-compose.chronos.yml down
```
