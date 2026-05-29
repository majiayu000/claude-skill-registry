---
name: cli
description: Prefect CLI commands for mutations. The MCP server is read-only - use this skill when you need to trigger deployments, cancel flow runs, create automations, or modify Prefect resources.
---

# Prefect CLI

The MCP server is read-only. For mutations, use the CLI.

**Prefer MCP tools for reads** (e.g., `get_flow_runs`, `get_deployments`). They return structured JSON with full UUIDs. Use `prefect api` only if MCP doesn't expose what you need.

## Critical: Agent-Friendly Usage

The CLI is designed for interactive terminal use. For non-interactive (agent) use:

```bash
# ALWAYS use --no-prompt as a TOP-LEVEL flag to disable confirmations
prefect --no-prompt flow-run delete <uuid>
prefect --no-prompt deployment delete <name>
```

### Avoiding Truncated Output

Rich table output truncates IDs and names, making them useless. Solutions:

```bash
# Use `prefect api` for raw JSON (preferred for agents)
prefect api POST /flow_runs/filter --data '{"limit": 5}'

# Use inspect with -o json for single resources
prefect flow-run inspect <uuid> -o json
prefect deployment inspect <name> -o json
```

### IDs Must Be Complete UUIDs

Partial IDs don't work. Always get full UUIDs from JSON output:

```bash
# Get full flow run ID
prefect api POST /flow_runs/filter --data '{"limit": 1}' | jq -r '.[0].id'
```

## Common Mutations

| Task | Command |
|------|---------|
| Trigger deployment | `prefect deployment run 'flow-name/deployment-name'` |
| Trigger by ID | `prefect deployment run --id <deployment-uuid>` |
| Cancel flow run | `prefect --no-prompt flow-run cancel <uuid>` |
| Delete flow run | `prefect --no-prompt flow-run delete <uuid>` |
| Delete deployment | `prefect --no-prompt deployment delete <name>` |

## Direct API Access

`prefect api` gives full API access with JSON output:

```bash
# List flow runs (with filters)
prefect api POST /flow_runs/filter --data '{"limit": 10}'

# Filter by state
prefect api POST /flow_runs/filter --data '{"flow_runs": {"state": {"type": {"any_": ["FAILED"]}}}}'

# Delete a flow run
prefect api DELETE /flow_runs/<uuid>

# Cancel a flow run
prefect api POST /flow_runs/<uuid>/set_state --data '{"state": {"type": "CANCELLING"}}'
```

## Automation Creation

Create from JSON string (inline):

```bash
prefect automation create --from-json '{
  "name": "notify-on-failure",
  "trigger": {
    "posture": "Reactive",
    "expect": ["prefect.flow-run.Failed"],
    "match": {"prefect.resource.id": "prefect.flow-run.*"}
  },
  "actions": [{"type": "send-notification", ...}]
}'
```

Or from file:

```bash
prefect automation create --from-file automation.yaml
```

Use `get_automations()` from the MCP server to inspect existing automation schemas.

## Efficient Inspection

The `get_flow_runs` tool returns summarized data to save tokens:
- It omits full deployment and work pool schemas.
- If you see a "Late" run or need concurrency details, follow up with:
  - `get_work_pools(filter={"name": ...})`
  - `get_deployments(filter={"id": ...})`
  - `get_dashboard()`

<!-- ref: https://github.com/pydantic/pydantic-ai/pull/3780 -->
