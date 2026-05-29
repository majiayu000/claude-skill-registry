---
name: localsetup-cron-orchestrator
description: "Manage cron from a repo-local manifest: time triggers, on-boot-with-delay, sequenced tasks; create, remove, reorder, install."
metadata:
  version: "1.0"
compatibility: "Linux cron; Python 3.10+ and PyYAML (framework). Manifest at cron/manifest.yaml."
---

# Cron orchestrator

Define triggers and tasks in a single YAML manifest. One trigger (e.g. midnight) runs multiple tasks in sequence; supports on-boot with delay. Tooling: create, remove, reorder, enable/disable, install (generate crontab fragment).

## Manifest (cron/manifest.yaml)

```yaml
triggers:
  midnight-utc:
    schedule: "0 0 * * *"
  after-boot:
    on_boot_delay_minutes: 5
tasks:
  - id: snapshot-daily
    trigger: midnight-utc
    sequence_order: 1
    command: "python3 _localsetup/skills/localsetup-system-info/scripts/system_snapshot.py --output-basename \"reports/system-snapshots/$(hostname)/$(date -u +%Y%m%dT%H%M%SZ)\""
    enabled: true
```

- **Triggers:** `schedule` = cron expression; `on_boot_delay_minutes` = run N minutes after reboot (single @reboot + sleep).
- **Tasks:** `trigger`, `sequence_order` (order within trigger), `command` (one line, shell-expanded), `enabled`.

## Commands (from repo root)

All use `--manifest cron/manifest.yaml` (default).

| Command | Purpose |
|---------|---------|
| `validate` | Check manifest and trigger refs |
| `list` [--trigger NAME] | List tasks (optionally for one trigger) |
| `add-task --trigger NAME --command "..."` [--sequence-order N] [--id ID] | Add task |
| `remove-task --id ID` or `--trigger NAME` | Remove by id or all for trigger |
| `reorder --trigger NAME --order id1,id2,id3` | Set run order for that trigger |
| `enable --id ID` / `disable --id ID` | Toggle task |
| `install` [--repo-root PATH] [--output PATH] | Generate crontab fragment (or write to file) |

Runner (used by cron): `run_trigger.py --manifest PATH --repo-root PATH TRIGGER` runs that trigger's tasks in sequence.

## Patterns for agents

1. **Add a daily snapshot at midnight:** `add-task --trigger midnight-utc --command "python3 _localsetup/skills/localsetup-system-info/scripts/system_snapshot.py --output-basename \"reports/system-snapshots/$(hostname)/$(date -u +%Y%m%dT%H%M%SZ)\""`.
2. **Add on-boot trigger:** In manifest, add trigger with `on_boot_delay_minutes: 5`; then add tasks to it.
3. **Reorder:** `reorder --trigger midnight-utc --order snapshot-daily,cleanup,notify`.
4. **Remove one task:** `remove-task --id snapshot-daily`. Remove all for a trigger: `remove-task --trigger midnight-utc`.
5. **Apply cron:** Run `install --output cron/crontab.generated`, then `crontab cron/crontab.generated` or merge into existing crontab.
