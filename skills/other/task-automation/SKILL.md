---
name: task-automation
description: Automate repetitive tasks and workflows using scripting, file watchers, scheduled jobs, CI triggers, and API polling to eliminate manual toil. Use when the user requests task automation or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Task Automation

This skill enables an AI agent to design and implement automations for repetitive tasks and workflows. The agent identifies manual processes suitable for automation, selects the right automation pattern (scripts, file watchers, cron jobs, CI/CD triggers, API polling), writes the implementation, and validates it works correctly. The goal is to eliminate toil — repetitive, manual work that scales linearly with workload — and replace it with reliable, hands-off automation.

## Workflow

1. **Analyze the Task:** Understand what the user wants to automate, including the trigger (what starts the task), the steps involved, the inputs and outputs, and the current frequency of manual execution. Determine whether the task is event-driven (triggered by a change) or time-driven (runs on a schedule).

2. **Select the Automation Pattern:** Choose the appropriate automation approach based on the trigger type and environment. Common patterns include: shell scripts for one-off or sequential tasks, file watchers (fswatch, inotifywait, chokidar) for reacting to file changes, cron jobs or systemd timers for scheduled recurring tasks, CI/CD pipeline triggers for code-related automation, API polling or webhook listeners for reacting to external service events.

3. **Design the Implementation:** Plan the automation in detail: define the inputs and configuration, error handling strategy (retry logic, alerting, fallback behavior), logging approach, and any secrets or credentials management needed. Consider idempotency — the automation should be safe to run multiple times without side effects.

4. **Write the Automation Code:** Implement the automation using the appropriate tools and languages. Prefer well-established, widely-supported tools: bash/Python for scripts, crontab for scheduling, GitHub Actions or GitLab CI for CI triggers, and standard webhook frameworks for event listeners.

5. **Test and Validate:** Run the automation in a safe environment first. Verify it handles the happy path correctly, then test edge cases: empty inputs, network failures, permission errors, and concurrent executions. Confirm that logging captures enough information for debugging.

6. **Deploy and Monitor:** Deploy the automation to its target environment with appropriate permissions. Set up monitoring or alerting so failures are noticed promptly. Document the automation's purpose, configuration, and how to disable it if needed.

## Usage

Describe the task you want to automate, including what triggers it, what it should do, and where it runs. The agent will select the right pattern and implement it.

```
Automate the following: whenever a new CSV file is added to the ~/data/incoming/
directory, validate the CSV headers, transform the data into JSON, and move the
result to ~/data/processed/. Log any files that fail validation to ~/data/errors/.
```

## Examples

### Example 1: File Watcher with Processing Pipeline

**User Request:**
> Automate processing of incoming CSV files in a directory.

**Implementation:**

```python
#!/usr/bin/env python3
"""File watcher that processes incoming CSVs into JSON.

Usage: python csv_watcher.py
Watches: ~/data/incoming/ for new .csv files
Outputs: ~/data/processed/*.json and ~/data/errors/error.log
"""

import os
import csv
import json
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

INCOMING = Path.home() / "data" / "incoming"
PROCESSED = Path.home() / "data" / "processed"
ERRORS = Path.home() / "data" / "errors"
REQUIRED_HEADERS = ["id", "name", "email", "amount"]

logging.basicConfig(
    filename=ERRORS / "error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s"
)

for d in [INCOMING, PROCESSED, ERRORS]:
    d.mkdir(parents=True, exist_ok=True)


class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.src_path.endswith(".csv"):
            return
        filepath = Path(event.src_path)
        try:
            with open(filepath, "r") as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                missing = set(REQUIRED_HEADERS) - set(headers)
                if missing:
                    raise ValueError(f"Missing headers: {missing}")
                rows = list(reader)

            output = PROCESSED / filepath.with_suffix(".json").name
            with open(output, "w") as f:
                json.dump(rows, f, indent=2)

            filepath.unlink()  # Remove processed file
            print(f"Processed: {filepath.name} -> {output.name}")
        except Exception as e:
            logging.error(f"Failed to process {filepath.name}: {e}")
            filepath.rename(ERRORS / filepath.name)


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(CSVHandler(), str(INCOMING), recursive=False)
    observer.start()
    print(f"Watching {INCOMING} for new CSV files...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

### Example 2: Cron-Based API Polling with Slack Notification

**User Request:**
> Every 6 hours, check our API health endpoint and post to Slack if any service is degraded.

**Implementation:**

Cron entry (added via `crontab -e`):
```cron
0 */6 * * * /usr/bin/python3 /opt/scripts/health_check.py >> /var/log/health_check.log 2>&1
```

Script:
```python
#!/usr/bin/env python3
"""Poll API health endpoint and alert Slack on degraded services.

Runs every 6 hours via cron. Exits 0 on success, 1 on alert sent, 2 on script error.
"""

import os
import json
import urllib.request

HEALTH_URL = "https://api.example.com/health"
SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK_URL"]


def check_health():
    req = urllib.request.Request(HEALTH_URL, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    return data  # e.g., {"services": {"auth": "ok", "payments": "degraded", "db": "ok"}}


def send_slack_alert(degraded_services):
    service_list = "\n".join(f"- *{name}*: {status}" for name, status in degraded_services)
    payload = json.dumps({
        "text": f":warning: *Service Health Alert*\n{service_list}"
    }).encode()
    req = urllib.request.Request(
        SLACK_WEBHOOK,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    urllib.request.urlopen(req)


if __name__ == "__main__":
    health = check_health()
    degraded = [
        (name, status)
        for name, status in health.get("services", {}).items()
        if status != "ok"
    ]
    if degraded:
        send_slack_alert(degraded)
        print(f"Alert sent for {len(degraded)} degraded service(s)")
        exit(1)
    else:
        print("All services healthy")
        exit(0)
```

## Best Practices

- **Make automations idempotent.** Running the same automation twice with the same input should produce the same result without side effects. This prevents data corruption if a job is accidentally retriggered.
- **Log everything, alert selectively.** Write detailed logs for debugging but only send alerts for actionable failures. An inbox full of "all OK" notifications trains people to ignore alerts.
- **Externalize configuration.** Store file paths, URLs, thresholds, and credentials in environment variables or config files, not hardcoded in scripts. This makes automations portable and secrets manageable.
- **Use lock files or mutexes for scheduled jobs.** Cron jobs can overlap if a previous run hasn't finished. Use `flock` or a PID file to ensure only one instance runs at a time.
- **Version-control your automation scripts.** Treat automations as production code — store them in Git, review changes, and tag releases. A broken automation can cause more damage than a broken feature.
- **Include a manual override.** Every automation should have a documented way to pause, skip, or run it manually. This is critical during incidents when automated actions may interfere with manual remediation.

## Edge Cases

- **Partial failures in multi-step automations:** If step 3 of 5 fails, the automation should not silently skip it. Implement checkpointing so the automation can resume from the last successful step rather than restarting from scratch.
- **Concurrent file writes:** File watchers may trigger on partially-written files. Add a brief delay or check file stability (size unchanged for N seconds) before processing.
- **Credential expiration:** API tokens and OAuth credentials expire. Build token refresh logic into automations that run long-term, and alert when refresh fails rather than silently dying.
- **Timezone issues with cron:** Cron uses the system timezone by default. For global teams, use UTC explicitly or document the timezone. Be aware of DST shifts causing jobs to run twice or skip.
- **Rate limits on polled APIs:** API polling can hit rate limits if the interval is too short or multiple instances run. Implement exponential backoff and track rate limit headers.
- **Empty or malformed input:** Automations triggered by external data (files, webhooks, API responses) should validate input schema before processing. Fail gracefully with a clear error message rather than producing corrupt output.
