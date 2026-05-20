---
name: siem
cluster: blue-team
description: "Monitors and analyzes security events and logs for real-time threat detection and incident response."
tags: ["siem","blue-team","security-monitoring"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "siem blue-team security event management monitoring logs threats detection"
---

## siem

### Purpose
This skill monitors and analyzes security events and logs in real-time to detect threats and enable incident response, focusing on blue-team operations.

### When to Use
Use this skill during active security monitoring, such as investigating anomalies in network logs, responding to potential breaches, or correlating events across systems. Apply it in environments with high log volumes, like enterprise networks, to prioritize alerts over manual reviews.

### Key Capabilities
- Real-time log ingestion and parsing from sources like syslog, Windows Event Logs, or cloud APIs.
- Threat detection rules based on Sigma or YARA formats for custom signatures.
- Alert generation and escalation via email, Slack, or webhook integrations.
- Correlation of events to identify patterns, such as failed logins followed by data exfiltration.
- Dashboard visualization using tools like Kibana for quick insights into metrics like event frequency and top threats.

### Usage Patterns
To set up monitoring, configure data sources first, then define queries or rules. For ongoing use, run periodic queries in scripts or integrate via API calls. Pattern 1: Query logs for specific events. Pattern 2: Automate alerts by scheduling rule checks. Always use environment variables for authentication, e.g., set `$SIEM_API_KEY` before operations.

### Common Commands/API
Use the SIEM CLI for quick tasks or the REST API for programmatic access. Authentication requires the `$SIEM_API_KEY` env var in all requests.

- CLI Command: Query logs with filters. Example:  
  `siem query --index security-logs --filter 'event_type=login AND status=failure' --limit 100 --output json`
  
- CLI Command: Create an alert rule. Example:  
  `siem rule add --name suspicious-activity --query 'source_ip=unknown AND action=access' --threshold 5 --action webhook --url https://webhook.example.com`

- API Endpoint: Submit events (POST /api/v1/events). Example code snippet:  
  ```python
  import requests; import os
  headers = {'Authorization': f'Bearer {os.environ["SIEM_API_KEY"]}'}
  response = requests.post('https://api.siem.com/api/v1/events', headers=headers, json={'event': 'login_failure', 'details': {'ip': '192.168.1.1'}})
  ```

- API Endpoint: Query events (GET /api/v1/query). Example code snippet:  
  ```python
  import requests; import os
  params = {'filter': 'event_type=access', 'time_range': 'last_hour'}
  response = requests.get('https://api.siem.com/api/v1/query', headers={'Authorization': f'Bearer {os.environ["SIEM_API_KEY"]}'}, params=params)
  print(response.json())
  ```

Config formats: Use JSON for rules, e.g., `{"name": "rule1", "query": "event_type=login", "threshold": 10}`. Store in a file and load via `siem config load --file rules.json`.

### Integration Notes
Integrate SIEM with tools like firewalls or IDS by configuring webhooks or API polling. For authentication, always use `$SIEM_API_KEY` in env vars; example: export SIEM_API_KEY=your_key. To link with other blue-team tools, use the SIEM webhook endpoint (e.g., POST /api/v1/webhook) for incoming events. For data forwarding, set up exporters in config files like:  
```
[exporter]
type = "splunk"
url = "https://splunk.example.com"
auth_key = "$SIEM_API_KEY"
```
Test integrations by sending a test event: `siem test-integration --type splunk --payload '{"event": "test"}'`.

### Error Handling
Common errors include authentication failures (e.g., 401 Unauthorized) from missing `$SIEM_API_KEY`, resolved by verifying env vars. For query errors (e.g., invalid filters), check syntax and use `siem query --debug` for logs. API timeouts (e.g., 504) can be handled by retrying with exponential backoff in code:  
```python
import time; import requests
try: response = requests.get('https://api.siem.com/api/v1/query', timeout=5)
except requests.exceptions.Timeout: time.sleep(2); response = requests.get('https://api.siem.com/api/v1/query', timeout=5)
```
Parse error responses for details, e.g., if response.status_code == 400, log the JSON error message. Always wrap CLI commands in scripts with error checking, like `if [ $? -ne 0 ]; then echo "Command failed"; fi`.

### Concrete Usage Examples
Example 1: Detect failed logins in the last hour.  
First, set env var: export SIEM_API_KEY=your_api_key  
Then, run: siem query --index auth-logs --filter 'event_type=login AND status=failure AND timestamp>now-1h' --output json  
Analyze output: Pipe to jq for parsing, e.g., `siem query ... | jq '.events[] | select(.ip=="suspicious")'`

Example 2: Set up an alert for high-severity events.  
Create rule: siem rule add --name high-severity-alert --query 'severity>7' --action email --recipients alerts@team.com  
Schedule it: Use cron to run `siem rule check --name high-severity-alert` every 5 minutes.  
Verify: Check logs with `siem logs --rule high-severity-alert` for triggered events.

### Graph Relationships
- Connected to: blue-team cluster
- Related tags: siem, blue-team, security-monitoring
- Links: Integrates with other blue-team skills via shared APIs; depends on security-monitoring for event sources
