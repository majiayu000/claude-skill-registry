---
name: grafana
cluster: devops-sre
description: "Grafana is an open-source tool for creating dashboards to visualize and query metrics, logs, and traces from various dat"
tags: ["monitoring","dashboards","visualization","observability"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "grafana monitoring dashboards visualization metrics logs traces alerting"
---

# grafana

## Purpose
Grafana is an open-source platform for visualizing and querying metrics, logs, and traces from various data sources. It enables users to create interactive dashboards, set up alerts, and explore data to monitor systems effectively.

## When to Use
Use Grafana when you need to build custom dashboards for real-time monitoring of infrastructure, applications, or services. It's ideal for scenarios involving observability, such as tracking Kubernetes metrics, analyzing server logs, or correlating traces in distributed systems. Avoid it for simple static reporting; opt for it when dynamic querying and visualization are required.

## Key Capabilities
- Create and manage dashboards with panels for graphs, tables, and gauges.
- Integrate with data sources like Prometheus, Loki, Elasticsearch via plugins.
- Set up alerting rules based on thresholds for metrics or logs.
- Support for ad-hoc queries and exploration using query languages like PromQL.
- Role-based access control (RBAC) for securing dashboards and data.
- Export/import dashboards in JSON format for versioning.

## Usage Patterns
To run Grafana as a server, start it with a configuration file: specify the config path and bind to a port. For automation, use the API to create dashboards programmatically. Common pattern: Ingest data from Prometheus, then query it via Grafana's UI or API. For CI/CD, embed Grafana in workflows to generate dashboards on-the-fly. Always run it in a containerized environment for scalability, e.g., using Docker with the official image.

## Common Commands/API
Use the Grafana CLI for administrative tasks. To start the server: `grafana-server --config /etc/grafana/grafana.ini --homepath /usr/share/grafana`. For plugins, run `grafana-cli plugins install <plugin-name>`.

API endpoints require authentication via API keys. Set your key as an environment variable: `export GRAFANA_API_KEY=$YOUR_API_KEY`. Then, use curl for requests.

Example: Create a dashboard via API:
```
curl -H "Authorization: Bearer $GRAFANA_API_KEY" -X POST https://your-grafana-instance/api/dashboards/db -d '{"dashboard": {"id": null, "uid": null, "title": "New Dashboard", "tags": ["example"], "timezone": "browser", "panels": []}, "folderId": 0, "overwrite": false}'
```

Query a data source: `GET https://your-grafana-instance/api/datasources/1`. Config files are in INI format, e.g.:
```
[server]
http_port = 3000
```

## Integration Notes
Integrate Grafana with data sources by adding them via the UI or configuration. For Prometheus, add a data source with URL: `http://prometheus:9090` and enable basic auth if needed. Use environment variables for secrets, e.g., `GF_SECURITY_ADMIN_PASSWORD=$ADMIN_PASSWORD`. For alerting, link to notification channels like Slack or PagerDuty in the config: add under `[alerting]` section in grafana.ini.

To embed in other tools, use the iframe embed option for dashboards. For code integrations, import Grafana dashboards in Terraform: define a resource like `resource "grafana_dashboard" "example" { config_json = file("dashboard.json") }`. Ensure data sources are provisioned first via Grafana's provisioning YAML files, e.g.:
```
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
```

## Error Handling
Common errors include connection failures to data sources; check logs with `journalctl -u grafana-server` or view in the UI under Server Admin > Logs. For API errors (e.g., 401 Unauthorized), verify the API key with `echo $GRAFANA_API_KEY` and ensure it's not expired. Handle query errors by wrapping API calls in try-catch blocks, e.g., in Python:
```
import requests
try:
    response = requests.post('https://your-grafana-instance/api/dashboards/db', headers={'Authorization': f'Bearer {os.environ["GRAFANA_API_KEY"]}'}, json=data)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"Error: {err.response.status_code} - {err.response.text}")
```
For configuration issues, validate grafana.ini with `grafana-server --config /path/to/config.ini --verify-config`.

## Concrete Usage Examples
Example 1: Set up a basic Prometheus dashboard. First, start Grafana: `docker run -d -p 3000:3000 grafana/grafana`. Log in (default user: admin, password: admin), add a data source via UI: Go to Configuration > Data Sources > Add Prometheus with URL `http://your-prometheus-url:9090`. Create a dashboard: Add a panel with query `up{job="prometheus"}`, save it.

Example 2: Automate alert creation via API. Export your API key to env: `export GRAFANA_API_KEY=your_key`. Send a request to create an alert rule:
```
curl -H "Authorization: Bearer $GRAFANA_API_KEY" -X POST https://your-grafana-instance/api/ruler/grafana/default -d '{"name": "High CPU Alert", "condition": "A", "for": "5m", "query": {"params": ["avg", "up", "{job=\"node\"}"], "model": {}}}'
```
This sets up an alert for high CPU usage based on your metrics.

## Graph Relationships
- Related to: Prometheus (provides metrics data), Loki (handles logs), as part of devops-sre cluster.
- Connects with: Elasticsearch (for log visualization), Jaeger/Zipkin (for traces).
- Dependencies: Often paired with monitoring tools like Alertmanager for full observability workflows.
