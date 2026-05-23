---
name: commerce-autonomous-runbook
description: Runbook for operating the StateSet autonomous engine. Use for incident response, stuck jobs, approval backlogs, or autonomous operations with `stateset-autonomous`.
---

# Commerce Autonomous Runbook

Operational runbook for running and troubleshooting the autonomous engine.

## How It Works

1. Start the autonomous engine with the correct database and store path.
2. Verify scheduler, workflows, policies, approvals, and webhooks are enabled.
3. Monitor job runs and workflow instances.
4. Handle approvals or disable subsystems if needed.

## Usage

Use this runbook when:
- The autonomous engine fails to start.
- Jobs or workflows are stuck.
- Approval queues are growing.
- You need to disable scheduling or webhooks.

## Output

```json
{"status":"running","scheduler":"enabled","approvals":0}
```

## Present Results to User

- Current engine status and enabled subsystems.
- Jobs or workflows affected.
- Remediation steps executed.

## Troubleshooting

- DB path invalid: confirm `--db` points to a writable file.
- Port conflict: change `--port` or stop the conflicting service.
- Approval backlog: pause jobs and clear approvals.

## References

- references/runbook.md
- /home/dom/stateset-icommerce/cli/bin/stateset-autonomous.js
