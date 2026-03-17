---
name: cron-ops
cluster: core-openclaw
description: "Cron job lifecycle: create, update, remove, debug, fix false positives, sanitize payloads"
tags: ["cron","jobs","automation","scheduling"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "cron job create update delete debug schedule automation"
---

# cron-ops

## Purpose
This skill handles the complete lifecycle of cron jobs in OpenClaw, including creation, updates, removal, debugging, fixing false positives, and sanitizing payloads to ensure secure and reliable automation.

## When to Use
Use this skill for scheduling repetitive tasks like backups, data syncs, or alerts in production environments; when troubleshooting cron failures; or to maintain job hygiene in automated workflows. Apply it in scenarios involving system automation, such as server maintenance or API polling.

## Key Capabilities
- Create cron jobs with custom schedules and commands.
- Update jobs to modify schedules, commands, or parameters.
- Remove jobs to clean up unused schedules.
- Debug jobs by logging outputs and inspecting errors.
- Fix false positives by analyzing execution logs and adjusting filters.
- Sanitize payloads to prevent injection attacks, ensuring commands are safe.

## Usage Patterns
Always authenticate using the `$OPENCLAW_API_KEY` environment variable. For CLI, prefix commands with `openclaw cron`. For API, use HTTPS endpoints like `https://api.openclaw.com/cron`. Start with job creation, then use IDs for updates or deletions. In code, import OpenClaw SDK and handle responses synchronously. Example pattern: Check job status before updating to avoid conflicts.

## Common Commands/API
Use the OpenClaw CLI for quick operations or the REST API for programmatic access. Authentication requires setting `$OPENCLAW_API_KEY`.

- **Create a job (CLI):**  
  `openclaw cron create --schedule "0 0 * * *" --command "echo 'Hello'" --payload '{"key": "value"}'`  
  This schedules a job to run daily at midnight.

- **Update a job (API):**  
  `curl -X PUT https://api.openclaw.com/cron/jobs/{jobId} -H "Authorization: Bearer $OPENCLAW_API_KEY" -d '{"schedule": "0 30 * * *", "command": "backup.sh"}'`  
  Updates the schedule of an existing job to run every hour at 30 minutes.

- **Remove a job (CLI):**  
  `openclaw cron delete --job-id 12345 --force`  
  Deletes the specified job, using `--force` to bypass confirmation.

- **Debug a job (API):**  
  `curl -X GET https://api.openclaw.com/cron/jobs/{jobId}/logs -H "Authorization: Bearer $OPENCLAW_API_KEY"`  
  Retrieves logs for debugging; parse JSON output for error details.

- **Fix false positives (CLI):**  
  `openclaw cron fix --job-id 12345 --filter "error_type=timeout"`  
  Applies fixes by updating filters in the job config to ignore common false positives.

- **Sanitize payloads (code snippet):**  
  ```python
  import openclaw
  client = openclaw.Client(api_key=os.environ['OPENCLAW_API_KEY'])
  sanitized_payload = client.sanitize({'command': 'echo "unsafe"; rm -rf /'})
  print(sanitized_payload)  # Outputs a safe version
  ```
  Use this to clean user-input payloads before job creation.

Config format for jobs is JSON, e.g., `{"schedule": "cron_expression", "command": "shell_command", "payload": {"key": "value"}}`.

## Integration Notes
Integrate with other OpenClaw skills by referencing job IDs in workflows. For example, link to `logging` skill for enhanced monitoring. Use webhooks by adding a `--webhook-url` flag in CLI commands, e.g., `openclaw cron create --webhook-url "https://your.service/webhook"`. In multi-service setups, pass `$OPENCLAW_API_KEY` via environment variables in Docker or CI/CD pipelines. Ensure compatibility by using the latest OpenClaw SDK version (v2.5+). For external systems, map cron schedules to standard formats like Unix crontab.

## Error Handling
Common errors include authentication failures (HTTP 401), invalid schedules (HTTP 400), or job conflicts (HTTP 409). Handle by checking response codes: if status is 401, verify `$OPENCLAW_API_KEY`. For invalid schedules, validate with `openclaw cron validate --schedule "invalid"`. In code, use try-except blocks:  
```python
try:
    response = client.create_job(schedule="0 0 * * *")
except openclaw.AuthError as e:
    print("Auth failed: Set $OPENCLAW_API_KEY")
except openclaw.ValidationError as e:
    print(f"Invalid input: {e}")
```
Retry transient errors with exponential backoff. Log all errors using the job ID for traceability.

## Concrete Usage Examples
1. **Create a daily backup job:**  
   First, set `$OPENCLAW_API_KEY`. Then run: `openclaw cron create --schedule "0 2 * * *" --command "rsync -a /data/ /backup/"`. Verify with `openclaw cron list`. This automates daily backups at 2 AM, and you can debug logs if it fails.

2. **Debug and fix a failed cron job:**  
   Identify the job with `openclaw cron list --status failed`. Debug: `curl -X GET https://api.openclaw.com/cron/jobs/12345/logs -H "Authorization: Bearer $OPENCLAW_API_KEY"`. If it's a false positive, fix with `openclaw cron fix --job-id 12345 --filter "status=timeout"`. This resolves issues like network timeouts in scheduled tasks.

## Graph Relationships
- Depends on: core-openclaw (for base API)
- Relates to: scheduling (for advanced timers), automation (for workflow integration)
- Conflicts with: none
- Extends: jobs (for general task management)
