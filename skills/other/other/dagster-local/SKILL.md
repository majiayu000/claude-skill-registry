---
name: dagster-local
description: Interact with Dagster data orchestration platform running locally or on Kubernetes. Use when Claude needs to monitor Dagster runs, get run logs, list assets/jobs, materialize assets, launch jobs, or debug pipeline failures. Supports both local Dagster dev server and Kubernetes deployments where each job run is a separate pod.
---

# Dagster Local Skill

Programmatic interaction with Dagster via GraphQL API and Kubernetes for pod-level logs.

## Quick Start

```python
from scripts.dagster_client import DagsterClient

client = DagsterClient()  # defaults to http://localhost:8000/graphql

# List all assets
assets = client.list_assets()

# Get recent runs
runs = client.get_recent_runs(limit=10)

# Get logs for a specific run
logs = client.get_run_logs(run_id="abc123")
```

## Configuration

```python
client = DagsterClient(graphql_url="http://localhost:8000/graphql")
```

## Available Operations

### Query Operations
| Function | Purpose |
|----------|---------|
| `list_repositories()` | List all code locations/repositories |
| `list_jobs(repo_location, repo_name)` | List jobs in a repository |
| `list_assets(repo_location, repo_name)` | List assets in a repository |
| `get_recent_runs(limit)` | Get recent run history |
| `get_run_info(run_id)` | Get detailed run info and status |
| `get_run_logs(run_id)` | Get event logs for a run |
| `get_asset_info(asset_key)` | Get asset details and dependencies |

### Mutation Operations
| Function | Purpose |
|----------|---------|
| `launch_job(repo_location, repo_name, job_name, config)` | Launch a job run |
| `materialize_asset(asset_key, repo_location, repo_name)` | Materialize an asset |
| `terminate_run(run_id)` | Terminate an in-progress run |

## Kubernetes Integration

When Dagster runs on K8s (each run = separate pod):

```python
from scripts.k8s_logs import get_pod_logs_for_run, get_dagster_pods

# Get pod logs for a specific run
logs = get_pod_logs_for_run(run_id="abc123", namespace="dagster")

# List all Dagster-related pods
pods = get_dagster_pods(namespace="dagster")
```

## Debugging Workflow

1. **Check recent runs**: `get_recent_runs()` to find failed runs
2. **Get run details**: `get_run_info(run_id)` for status and error summary
3. **Get Dagster logs**: `get_run_logs(run_id)` for step-level events
4. **Get pod logs** (K8s): `get_pod_logs_for_run(run_id)` for stdout/stderr

## Common Patterns

### Wait for Run Completion
```python
import time

def wait_for_run(client, run_id, timeout=300):
    start = time.time()
    while time.time() - start < timeout:
        info = client.get_run_info(run_id)
        status = info.get("status")
        if status in ["SUCCESS", "FAILURE", "CANCELED"]:
            return info
        time.sleep(5)
    raise TimeoutError(f"Run {run_id} did not complete")
```

### Get Failure Reason
```python
def get_failure_reason(client, run_id):
    logs = client.get_run_logs(run_id)
    failures = [e for e in logs.get("events", []) if "error" in e]
    return failures[-1] if failures else None
```

## GraphQL Reference

For advanced queries, see `references/graphql_queries.md`.
