---
name: az-cli-ops
description: Azure CLI (az) operations for resource groups, deployments (ARM/Bicep), app services/container apps, ACR images, Key Vault secrets, role assignments, and operational checks. Use when a request involves `az` commands, Azure deployments, secrets/app settings, or Azure resource management.
---

# Az Cli Ops

## Overview
Use az to manage Azure resources, deployments, and secrets with safe, repeatable workflows.

## Quick start (context)
1. Use the wrapper so commands are logged: `scripts/azx account show`, `scripts/azx account list -o table`, `scripts/azx account set -s <subscription-id>`.
2. Confirm defaults: `scripts/azx configure -d group=<rg> location=<region>` for the current session.
3. For read-heavy tasks, prefer `--query` + `-o jsonc|tsv` to avoid parsing errors.
4. Review `references/auto-summary.md` to adapt based on recent successes/failures.

## Automation wrapper (required)
- Use `scripts/azx` for all az commands to log outcomes to `references/usage-log.jsonl`.
- The wrapper auto-updates `references/auto-summary.md` after each command to capture what worked or failed.
- If you must run `az` directly (e.g., debugging), run `scripts/track_command.sh az ...` afterward with the same args.

## Task map
See `references/az-command-map.md` for task-to-command mappings and safe defaults.

## Deployments (ARM/Bicep)
- Use `az deployment group create` for resource-group scoped deployments.
- Use `az deployment sub create` for subscription-scoped deployments.
- Prefer `--what-if` before destructive changes; capture outputs via `--query`.

## App Services / Container Apps
- Use `az webapp` / `az appservice` for App Service operations.
- Use `az containerapp` for Container Apps; install the extension if needed (`az extension add -n containerapp`).
- Use deployment logs and revision lists when diagnosing rollouts.

## Secrets & config
- Use Key Vault for secrets: `az keyvault secret set/show/list`.
- For app settings:
  - App Service: `az webapp config appsettings set/list`.
  - Container Apps: `az containerapp secret set/list` and `az containerapp update --set-env-vars`.

## Access control
- Use `az role assignment create/list` and `az role definition list` for RBAC.
- Use `az ad` commands sparingly; confirm tenant context with `az account show`.

## Self-improving loop (automated + manual)
Automated (always on when using `scripts/azx`):
1. Command outcomes are logged to `references/usage-log.jsonl`.
2. `scripts/auto_improve.py` updates `references/auto-summary.md` and can append repeatable learnings to `references/az-ops-notes.md`.

Manual (when new patterns are discovered):
1. Append new command patterns, flags, or pitfalls to `references/az-ops-notes.md`.
2. If a command/flag is missing or changed, update `references/az-command-map.md`.
3. Run `scripts/refresh_az_reference.sh` to refresh `references/az-help.md` from the locally installed az.

## Resources
### scripts/
- `scripts/azx`: wrapper that logs az command outcomes and triggers auto-summary updates.
- `scripts/track_command.sh`: logs command outcomes to `references/usage-log.jsonl`.
- `scripts/auto_improve.py`: generates `references/auto-summary.md` and auto-notes.
- `scripts/refresh_az_reference.sh`: regenerate `references/az-help.md` from local az help output.

### references/
- `references/az-command-map.md`: task-to-command map and safe defaults.
- `references/az-help.md`: auto-generated help snapshot from the local az version.
- `references/az-ops-notes.md`: living notes for patterns, pitfalls, and team conventions.
- `references/auto-summary.md`: auto-generated success/failure summary for recent commands.
- `references/usage-log.jsonl`: append-only command log (redacted).
