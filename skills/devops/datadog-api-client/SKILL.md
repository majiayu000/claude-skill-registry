---
name: datadog-api-client
description: Query and manage Datadog resources (logs, metrics, monitors, dashboards, incidents, APM traces) using the datadog-api-client Python library. Use when the user asks about Datadog monitoring, wants to search logs, check metrics, manage monitors, investigate incidents, or interact with any Datadog API.
metadata:
  category: tooling
  tools: datadog
---

# Datadog API Client

Write and run Python scripts using the `datadog-api-client` library to interact with Datadog APIs. Covers logs, metrics, monitors, dashboards, incidents, APM, and all other Datadog v1/v2 endpoints.

**Site:** `us5.datadoghq.com` (set via `DD_SITE` env var)
**Library docs:** https://github.com/DataDog/datadog-api-client-python

## Prerequisites

- Python 3.8+
- `datadog-api-client` library installed:
  ```bash
  pip install datadog-api-client
  ```
- Environment variables set (`DD_API_KEY`, `DD_APP_KEY`, `DD_SITE`). Add to a `.env` file or shell profile — avoid pasting keys directly in your shell (they end up in shell history):
  ```bash
  # ~/.env.datadog or add to ~/.zshrc / ~/.bashrc
  export DD_API_KEY="<your-api-key>"
  export DD_APP_KEY="<your-app-key>"
  export DD_SITE="us5.datadoghq.com"
  ```
  Keys: go to https://ls-k.datadoghq.com/organization-settings/api-keys (or https://us5.datadoghq.com/organization-settings/api-keys). Not everyone has access to create keys — ask your Team Lead for a key or permission to create one.

  **IMPORTANT:** Never commit API keys to version control. If using a `.env` file, ensure it's in `.gitignore`.

Verify setup:

```bash
python3 -c "
from datadog_api_client import Configuration, ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi
import time

c = Configuration()
now = int(time.time())
with ApiClient(c) as client:
    resp = MetricsApi(client).query_metrics(_from=now - 60, to=now, query='avg:system.cpu.user{*}')
    print(f'OK: connected to {c.server_variables.get(\"site\", \"datadoghq.com\")}, got {len(resp.series)} series')
"
```

If this fails with 403, check that `DD_API_KEY` and `DD_APP_KEY` are exported. If it hits the wrong site, check `DD_SITE`.

## Usage Pattern

The library reads `DD_API_KEY`, `DD_APP_KEY`, and `DD_SITE` from environment variables automatically. No manual configuration needed:

```python
from datadog_api_client import Configuration, ApiClient

configuration = Configuration()

with ApiClient(configuration) as api_client:
    # use API instances here
    pass
```

Import the specific API and model classes you need from `datadog_api_client.v1.api` or `datadog_api_client.v2.api`.

## Common Operations

### Search Logs

```python
from datadog_api_client import Configuration, ApiClient
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_sort import LogsSort

configuration = Configuration()

with ApiClient(configuration) as api_client:
    body = LogsListRequest(
        filter=LogsQueryFilter(
            query="service:my-service status:error",
            _from="now-1h",
            to="now",
        ),
        sort=LogsSort.TIMESTAMP_DESCENDING,
    )
    response = LogsApi(api_client).list_logs(body=body)
    for log in response.data:
        print(log.attributes.message)
```

### Query Metrics

```python
from datadog_api_client import Configuration, ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi
import time

configuration = Configuration()

with ApiClient(configuration) as api_client:
    now = int(time.time())
    response = MetricsApi(api_client).query_metrics(
        _from=now - 3600,
        to=now,
        query="avg:system.cpu.user{*}",
    )
    for series in response.series:
        print(f"{series.scope}: {len(series.pointlist)} points")
```

### List Monitors

```python
from datadog_api_client import Configuration, ApiClient
from datadog_api_client.v1.api.monitors_api import MonitorsApi

configuration = Configuration()

with ApiClient(configuration) as api_client:
    monitors = MonitorsApi(api_client).list_monitors()
    for m in monitors:
        print(f"[{m.overall_state}] {m.name}")
```

For more examples (incidents, dashboards, pagination), see `references/api-reference.md`.

## Notes

- The library reads `DD_API_KEY`, `DD_APP_KEY`, and `DD_SITE` from the environment -- ensure they're set before running scripts
- Use v2 APIs when available (v1 is legacy for some endpoints)
- For paginated results, prefer `list_*_with_pagination()` methods to avoid silently missing data
- Scripts are written and executed via the terminal -- no MCP server needed
