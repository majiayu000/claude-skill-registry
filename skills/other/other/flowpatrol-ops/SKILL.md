---
name: flowpatrol-ops
cluster: financial
description: "Manages operational monitoring and compliance for FlowPatrol financial systems using automated tools."
tags: ["financial","operations","flowpatrol"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "financial operations flowpatrol monitoring compliance automation"
---

# flowpatrol-ops

## Purpose
This skill automates operational monitoring and ensures compliance for FlowPatrol financial systems, using tools to track transactions, detect anomalies, and enforce regulatory standards.

## When to Use
Use this skill for real-time monitoring of financial operations, compliance audits in production environments, or automating alerts for suspicious activities in FlowPatrol systems. Apply it when integrating with financial workflows to maintain security and regulatory adherence.

## Key Capabilities
- Monitor system logs and transactions in real-time using FlowPatrol's API to detect anomalies like unusual transaction volumes.
- Enforce compliance by checking against rulesets (e.g., PCI DSS) and generating automated reports.
- Automate alerts via email or webhook for events like threshold breaches.
- Integrate with external tools for data aggregation, such as pulling metrics from Prometheus.
- Handle batch processing for compliance checks on historical data.
- Support configurable thresholds, e.g., set via JSON config files for custom monitoring rules.
- Provide API-based querying for on-demand status checks.
- Generate audit trails with timestamps and user IDs for all operations.
- Scale monitoring across multiple FlowPatrol instances.
- Use embedded analytics to visualize compliance metrics.

## Usage Patterns
Invoke the skill via CLI for quick tasks or through API calls for programmatic integration. Always set environment variables for authentication first, like `export FLOWPATROL_API_KEY=$SERVICE_API_KEY`. For repeated tasks, use scripts that chain commands, such as monitoring followed by compliance checks. Pass configurations via files (e.g., JSON) to customize behavior, and handle outputs in JSON format for easy parsing.

## Common Commands/API
Use the FlowPatrol CLI with these commands; ensure the tool is installed via `pip install flowpatrol-ops`. Authentication requires `$FLOWPATROL_API_KEY` as an environment variable.

- CLI command for monitoring: `flowpatrol monitor --system prod --interval 5m --threshold 100` (flags: --system for environment, --interval for check frequency, --threshold for alert level).
- CLI for compliance check: `flowpatrol check-compliance --ruleset pci --output report.json` (snippet:  
  ```bash
  export FLOWPATROL_API_KEY=your_key
  flowpatrol check-compliance --ruleset pci
  ```
  ).
- API endpoint for starting a monitor: POST to `/api/v1/monitor` with JSON body `{ "system": "prod", "interval": "5m" }` (e.g., using curl:  
  ```bash
  curl -X POST -H "Authorization: Bearer $FLOWPATROL_API_KEY" -d '{"system":"prod"}' https://api.flowpatrol.com/api/v1/monitor
  ```
  ).
- API for retrieving reports: GET `/api/v1/reports/{reportId}` with query params like `?format=json`.
- Command to generate alerts: `flowpatrol alert-setup --webhook https://your.webhook.url --event anomaly` (config format: JSON file like `{ "events": ["anomaly"], "webhook": "url" }`).
- Batch processing command: `flowpatrol process-batch --file transactions.csv --rules compliance_rules.json` (snippet:  
  ```bash
  flowpatrol process-batch --file data.csv
  echo "Processing complete"
  ```
  ).
- Stop monitoring: `flowpatrol stop --id monitor123` (uses --id flag for specific instance).
- Query status: `flowpatrol status --system prod` (returns JSON output).

## Integration Notes
Integrate with financial tools by exporting data to formats like CSV or JSON for tools like Excel or Tableau. Use `$FLOWPATROL_API_KEY` for auth in scripts; example: set in .env files for Docker containers. For webhooks, ensure URLs are HTTPS and handle payloads in JSON. When combining with other skills (e.g., in the "financial" cluster), chain API calls, like calling FlowPatrol after data ingestion from a database. Config files should follow this format: `{ "apiEndpoint": "https://api.flowpatrol.com", "key": "$FLOWPATROL_API_KEY" }`. Avoid hardcoding keys; use environment variables for security.

## Error Handling
Check CLI exit codes: 0 for success, 1-9 for errors (e.g., 1 for auth failure). For API calls, handle HTTP status codes like 401 (unauthorized) by re-authenticating, or 500 (server error) by retrying with exponential backoff. In scripts, use try-catch blocks (e.g., in Python:  
```python
try:
    response = requests.post(url, headers=headers)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"Error: {err}")
```
). Parse error responses, which are JSON like `{ "error": "Invalid key", "code": 401 }`. Log all errors with timestamps and retry transient issues up to 3 times. For CLI, use `--verbose` flag to debug.

## Concrete Usage Examples
1. **Monitoring transactions in production:** Export your API key, then run `flowpatrol monitor --system prod --interval 1m` to start real-time monitoring. This detects anomalies; pipe output to a file: `flowpatrol monitor ... > logs.txt`. Follow up with `flowpatrol alert-setup --webhook your_url` to notify on breaches.
2. **Running a compliance audit:** Use `flowpatrol check-compliance --ruleset gdpr --output audit.json` on a dataset. In a script, combine it:  
   ```bash
   export FLOWPATROL_API_KEY=key
   flowpatrol check-compliance --ruleset gdpr
   cat audit.json | jq '.results'
   ```
   This generates a report for reviewing compliance issues.

## Graph Relationships
- Related to cluster: "financial" (e.g., shares tools with other financial monitoring skills).
- Connected via tags: "operations" (links to operational tools), "flowpatrol" (specific to FlowPatrol ecosystem).
- Potential edges: Integrates with "compliance-checker" skill for enhanced auditing, and "alert-system" for notification workflows.
