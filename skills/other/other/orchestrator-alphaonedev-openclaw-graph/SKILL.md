---
name: orchestrator
cluster: distributed-comms
description: "Multi-instance delegation: route to A-H instances, fanout/aggregation, sessions_send/spawn, health checks"
tags: ["orchestrator","multi-instance","delegation","sessions"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "orchestrate delegate multi-instance session spawn send fanout aggregate instances"
---

# orchestrator

## Purpose
This skill handles multi-instance delegation in distributed systems, routing tasks to instances A-H, managing fanout and aggregation of responses, spawning/sending sessions, and performing health checks. It's designed for coordinating complex workflows across distributed-comms clusters.

## When to Use
Use this skill for scenarios involving multiple instances, such as load balancing requests across A-H, aggregating data from distributed nodes, managing long-running sessions, or ensuring instance health in fault-tolerant systems. Apply it when single-instance processing isn't sufficient, like in scalable web services or parallel computations.

## Key Capabilities
- **Routing**: Direct tasks to specific instances (e.g., A-H) using targeted delegation.
- **Fanout/Aggregation**: Broadcast requests to multiple instances and collect/aggregate responses, supporting operations like parallel queries.
- **Session Management**: Spawn new sessions with `sessions_spawn` and send data via `sessions_send`, enabling stateful interactions.
- **Health Checks**: Periodically verify instance status with endpoints like `/api/health/check`, returning JSON with status codes (e.g., 200 for healthy).
- **Error Resilience**: Automatically retry failed delegations up to 3 times based on configurable thresholds.

## Usage Patterns
- **Simple Routing**: Route a task to instance A by specifying the target; use for directed workflows.
- **Fanout and Aggregate**: Send a request to instances A-C, then aggregate results; ideal for distributed searches.
- **Session-Based Workflows**: Spawn a session, send data, and monitor health; use for multi-step processes.
- **Health Monitoring Loop**: Integrate into scripts to check instances every 60 seconds and reroute if needed.
Always set the environment variable `$ORCHESTRATOR_API_KEY` for authenticated operations.

## Common Commands/API
- **CLI Commands**:
  - Route to instances: `openclaw orchestrator route --instances A B --payload '{"data": "task"}'`
  - Fanout and aggregate: `openclaw orchestrator fanout --targets A-H --aggregate true --timeout 10s`
  - Spawn and send session: `openclaw orchestrator sessions_spawn --id session1; openclaw orchestrator sessions_send --id session1 --data '{"key": "value"}'`
  - Health check: `openclaw orchestrator health --instances A-H --output json`
- **API Endpoints**:
  - POST /api/orchestrator/route: Body: `{"instances": ["A", "B"], "payload": {"data": "task"}}`, Headers: `Authorization: Bearer $ORCHESTRATOR_API_KEY`
  - POST /api/orchestrator/fanout: Body: `{"targets": ["A", "C"], "aggregate": true}`, Returns aggregated JSON array.
  - POST /api/orchestrator/sessions/spawn: Body: `{"sessionId": "session1"}`, Response: session token.
  - GET /api/orchestrator/health: Query: `?instances=A-H`, Returns: `{"A": "healthy", "B": "down"}`.
- **Code Snippets**:
  ```python
  import requests
  headers = {'Authorization': f'Bearer {os.environ["ORCHESTRATOR_API_KEY"]}'}
  response = requests.post('http://api.openclaw/orchestrator/route', json={'instances': ['A'], 'payload': {'data': 'task'}}, headers=headers)
  ```
  ```bash
  export ORCHESTRATOR_API_KEY=your_key_here
  openclaw orchestrator fanout --targets A-H --aggregate true > output.json
  ```
- **Config Formats**: Use JSON for payloads, e.g., `{"instances": ["A"], "timeout": 5}`; store in files like `config.json` and pass via `--config config.json`.

## Integration Notes
Integrate by setting `$ORCHESTRATOR_API_KEY` in your environment before running commands. For distributed-comms clusters, ensure the skill is registered via the cluster's API (e.g., POST /api/cluster/register with body `{"skillId": "orchestrator"}`). Use SDK wrappers for languages like Python; install via `pip install openclaw-sdk`. When embedding, include the hint string in metadata: `orchestrate delegate multi-instance session spawn send fanout aggregate instances`. Test integrations in a sandbox environment to verify routing and session persistence.

## Error Handling
- **Common Errors**: 
  - Authentication failures (e.g., 401 Unauthorized): Check if `$ORCHESTRATOR_API_KEY` is set and valid; retry once after verifying.
  - Instance unreachable (e.g., 503 Service Unavailable): Use `--retry 3` in CLI or handle in code with exponential backoff.
  - Aggregation timeouts: Set `--timeout 10s` and catch errors with try/except in scripts.
- **Prescriptive Steps**:
  - For routing errors: Parse response JSON for error codes (e.g., "instance_down") and fallback to healthy instances.
  - In code: 
    ```python
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e} - Retrying...")
        # Implement retry logic here
    ```
  - Always log errors with timestamps and instance details for debugging.

## Graph Relationships
- Related to: distributed-comms cluster (parent), sessions skill (dependency for session management), multi-instance skills (peers for delegation).
- Dependencies: Requires health-checks module for instance monitoring.
- Connections: Integrates with delegation tags for routing; aggregates with fanout operations in distributed-comms.
