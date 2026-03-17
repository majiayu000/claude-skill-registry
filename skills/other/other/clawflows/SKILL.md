---
name: clawflows
cluster: community
description: "OpenClaw workflow automation: multi-step task chains, conditional logic, triggers, schedule"
tags: ["openclaw","workflow","automation","flows"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "openclaw workflow automation chain conditional trigger schedule"
---

# clawflows

## Purpose
This skill automates workflows in OpenClaw by defining multi-step task chains, incorporating conditional logic, triggers, and scheduling to streamline complex operations.

## When to Use
Use this skill for repetitive task sequences, like processing data pipelines, conditional decision-making (e.g., if a file exists, then execute), event-driven triggers (e.g., on API call), or scheduled jobs (e.g., daily reports). Apply it in scenarios requiring orchestration, such as integrating multiple OpenClaw tools or external services.

## Key Capabilities
- Define task chains: Specify steps in a JSON config, e.g., {"steps": [{"name": "step1", "action": "run_script"}, {"name": "step2", "action": "send_email"}]}
- Conditional logic: Use if-else in configs, e.g., {"condition": "if status == 'success' then next: step2 else: abort"}
- Triggers: Set event-based triggers like webhooks or file changes, e.g., via {"trigger": {"type": "http", "endpoint": "/webhook"}}
- Scheduling: Use cron-style schedules, e.g., {"schedule": "0 0 * * *"} for midnight daily runs
- Error recovery: Built-in retries for failed steps, configurable per step

## Usage Patterns
To create and run a workflow, start by defining a config file (JSON/YAML), then use CLI or API to execute. For simple flows, use CLI directly; for programmatic use, integrate via API. Always set environment variables for authentication, e.g., export CLAWFLOWS_API_KEY=$SERVICE_API_KEY. Test flows in isolation before scheduling. Common pattern: Load config, validate, run, and monitor output.

## Common Commands/API
Use the OpenClaw CLI for quick operations:
- Create a flow: `clawflows create --name myworkflow --config path/to/config.json --cluster community`
- Run a flow: `clawflows run --flow-id 123 --env VAR=VALUE` (outputs status JSON)
- Schedule a flow: `clawflows schedule --flow-id 123 --cron "0 9 * * *" --trigger-type http`
- API endpoints: POST /api/workflows to create (body: {"name": "myworkflow", "steps": [...] }), GET /api/workflows/{id} to retrieve
Code snippet for API call in Python:
```python
import requests
headers = {"Authorization": f"Bearer {os.environ['CLAWFLOWS_API_KEY']}"}
response = requests.post("https://api.openclaw.com/api/workflows", headers=headers, json={"name": "test", "steps": [{"action": "echo hello"}]})
print(response.json())
```
Config format example (JSON):
{
  "steps": [
    {"name": "step1", "action": "run_command", "command": "ls -l"},
    {"name": "step2", "condition": "step1.success", "action": "log_message", "message": "Success!"}
  ]
}

## Integration Notes
Integrate clawflows with other OpenClaw skills by referencing them in step actions, e.g., {"action": "call_skill", "skill_id": "another_skill"}. For authentication, use env vars like $CLAWFLOWS_API_KEY for API requests. When combining with external tools, map outputs via JSON paths, e.g., in config: {"input_mapping": {"var1": "$.output.data"}}. Ensure compatibility by specifying cluster in commands, e.g., --cluster community. For webhooks, expose an endpoint that triggers flows via POST /api/triggers/{flow-id}.

## Error Handling
Common errors include authentication failures (HTTP 401), invalid configs (e.g., syntax errors in JSON), or step timeouts. To handle: Check for $CLAWFLOWS_API_KEY before running; use `clawflows validate --config path/to/config.json` to catch issues early. In code, wrap API calls in try-except blocks:
```python
try:
    response = requests.post("https://api.openclaw.com/api/workflows", headers=headers, json=data)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"Error: {e.response.status_code} - {e.response.text}")
```
For runtime errors, configure retries in config, e.g., {"step": {"action": "...", "retries": 3, "timeout": 30}}. Monitor logs with `clawflows logs --flow-id 123` and abort on critical failures using conditional steps.

## Concrete Usage Examples
Example 1: Automate a data backup flow. Create a config file: {"steps": [{"name": "backup", "action": "run_command", "command": "rsync /data/ backup-server:"}, {"condition": "backup.success", "action": "send_email", "to": "admin@example.com", "subject": "Backup complete"}]} Then run: `clawflows create --name backupflow --config backup.json` and schedule: `clawflows schedule --flow-id 456 --cron "0 2 * * *"`
Example 2: Trigger a workflow on file change. Define: {"trigger": {"type": "file_watch", "path": "/monitored/dir"}, "steps": [{"action": "process_file", "file": "$.trigger.file"}]} Execute via API: POST /api/workflows with the config, then monitor with `clawflows run --flow-id 789 --watch`.

## Graph Relationships
- Relates to: openclaw-core (for basic task execution), openclaw-triggers (for event handling), community-cluster (as part of the ecosystem)
- Depends on: authentication services for API access
- Integrates with: external APIs via steps, e.g., for data fetching or notifications
