---
name: commerce-autonomous-engine
description: Operate the StateSet autonomous engine (jobs, workflows, policies, approvals). Use when starting/stopping `stateset-autonomous`, inspecting scheduler state, or running autonomous MCP tools.
---

# Commerce Autonomous Engine

Operate the autonomous engine that runs scheduled jobs, workflows, policies, and approvals.

## How It Works

1. Start the autonomous engine with a database and store path.
2. Configure scheduler, workflows, policies, approvals, and webhooks.
3. Monitor job runs and workflow instances.
4. Approve or deny gated operations.

## Usage

- CLI: `stateset-autonomous start`, `stateset-autonomous status`, `stateset-autonomous init`.
- Skill script: `bash /mnt/skills/user/commerce-autonomous-engine/scripts/autonomous-status.sh`.
- MCP tools: `list_scheduled_jobs`, `create_scheduled_job`, `run_job_now`, `list_workflows`, `list_policies`, `list_pending_approvals`.

## Output

```json
{"status":"running","scheduler_jobs":4,"pending_approvals":0}
```

## Present Results to User

- Engine status and enabled subsystems.
- Jobs or workflows created/updated.
- Approval decisions and impact.

## Troubleshooting

- Engine fails to start: verify DB path and store directory permissions.
- Webhook errors: confirm port availability and event payloads.

## References
- references/autonomous-ops.md
- /home/dom/stateset-icommerce/cli/bin/stateset-autonomous.js
- /home/dom/stateset-icommerce/cli/src/autonomous/mcp-tools.js
