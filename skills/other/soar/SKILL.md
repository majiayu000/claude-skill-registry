---
name: soar
cluster: blue-team
description: "Implements Security Orchestration, Automation, and Response for blue-team incident handling."
tags: ["soar","blue-team","automation"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "soar security automation response blue-team incident"
---

# soar

## Purpose
This skill automates security incident response by orchestrating workflows, integrating tools, and executing actions for blue-team operations. It handles tasks like alerting, enrichment, and remediation to streamline incident handling.

## When to Use
Use this skill during active security incidents for rapid response, such as when detecting anomalies in logs, escalating threats, or automating containment. It's ideal for environments with high alert volumes where manual intervention is inefficient.

## Key Capabilities
- Orchestrate playbooks: Define and run multi-step workflows using YAML config files, e.g., a playbook for isolating compromised hosts.
- Integrate with tools: Connect to SIEMs, firewalls, and threat intel via APIs, supporting protocols like REST and WebSockets.
- Incident enrichment: Automatically fetch data from sources like VirusTotal or internal databases using predefined connectors.
- Automation rules: Set up triggers based on conditions, e.g., if an alert matches a signature, execute a response.
- Reporting: Generate summaries of executed actions and outcomes via JSON outputs.

## Usage Patterns
To use this skill, first configure authentication via environment variables like `$SOAR_API_KEY`. Then, load playbooks from files or APIs and trigger them based on events. For example, integrate with a monitoring tool to call SOAR endpoints on alerts. Always test playbooks in a staging environment before production. Common pattern: Poll for incidents, evaluate conditions, and run actions sequentially.

## Common Commands/API
Use the CLI for quick tasks or the API for programmatic access. Authentication requires `$SOAR_API_KEY` in requests.

- CLI Command: Run a playbook  
  `soar run --playbook-id 123 --params '{"ip": "192.168.1.1"}'`  
  This executes playbook ID 123 with custom parameters; output is JSON with status and results.

- API Endpoint: Trigger playbook  
  POST https://api.openclaw.com/soar/playbooks/{id}/run  
  Headers: `Authorization: Bearer $SOAR_API_KEY`  
  Body: `{"params": {"action": "isolate", "target": "host-01"}}`  
  Response: 200 OK with JSON like `{"status": "success", "details": {...}}`.

- CLI Command: Query incidents  
  `soar list-incidents --filter "status=active" --limit 10`  
  Filters incidents by status; use `--output json` for structured data.

- API Endpoint: Get incidents  
  GET https://api.openclaw.com/soar/incidents?status=active&limit=10  
  Headers: `Authorization: Bearer $SOAR_API_KEY`  
  Response: Array of incident objects in JSON.

Config formats: Playbooks are defined in YAML, e.g.:  
```yaml
name: Isolate Host
steps:
  - action: block-ip
    params:
      ip: "{{params.ip}}"
```
Keep snippets under 4 lines; reference full docs for more.

## Integration Notes
Integrate SOAR by setting up webhooks or API calls. For example, export `$SOAR_API_KEY` and use it in scripts:  
```bash
export SOAR_API_KEY=your_api_key_here
curl -X POST https://api.openclaw.com/soar/webhooks -H "Authorization: Bearer $SOAR_API_KEY" -d '{"event": "alert", "data": {...}}'
```
Common integrations: Link with SIEM tools like Splunk via HTTP endpoints, or databases for enrichment. Ensure TLS is enabled for all connections. For custom connectors, provide a JSON config file, e.g., `{"type": "rest", "endpoint": "https://example.com/api"}`.

## Error Handling
Handle errors by checking HTTP status codes or CLI exit codes. Common errors: 401 Unauthorized (fix by verifying `$SOAR_API_KEY`), 404 Not Found (check playbook ID), or invalid YAML (validate with `soar validate --file playbook.yaml`). In code, wrap API calls in try-catch blocks:  
```python
import requests
try:
    response = requests.post('https://api.openclaw.com/soar/playbooks/123/run', headers={'Authorization': f'Bearer {os.environ["SOAR_API_KEY"]}'})
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"Error: {e.response.status_code} - {e.response.text}")
```
Log errors with timestamps and retry transient failures up to 3 times.

## Concrete Usage Examples
1. **Automate Incident Response for a Suspicious Login:**  
   First, set `$SOAR_API_KEY`. Then, run:  
   `soar run --playbook-id 456 --params '{"user": "admin", "ip": "10.0.0.1"}'`  
   This triggers a playbook to block the IP and notify the team via email. Monitor output for success.

2. **Enrich and Escalate an Alert:**  
   Use API to query and act:  
   ```bash
   curl -H "Authorization: Bearer $SOAR_API_KEY" https://api.openclaw.com/soar/incidents?severity=high
   # Parse response, then POST to run enrichment: curl -X POST https://api.openclaw.com/soar/playbooks/789/run -d '{"params": {"incident_id": "12345"}}'
   ```
   This fetches high-severity incidents and enriches them, e.g., checking against threat feeds.

## Graph Relationships
- Related to: blue-team cluster (e.g., skills like 'threat-detection' for input data, 'incident-response' for follow-up actions).
- Depends on: authentication services for API keys.
- Integrates with: external tools via APIs, such as SIEM systems for event triggers.
