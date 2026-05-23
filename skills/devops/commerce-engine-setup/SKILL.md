---
name: commerce-engine-setup
description: Set up and run the StateSet iCommerce engine locally (CLI install, DB init, demo data, sync). Use when bootstrapping an environment, running `stateset-doctor`, or starting `stateset-autonomous`.
---

# Commerce Engine Setup

Set up local iCommerce runtime, CLI tooling, and optional sync.

## How It Works

1. Install or link the CLI and choose a SQLite database path.
2. Initialize sync and keys if you need sequencer replication.
3. Seed demo data and verify the environment.
4. Start CLI commands or the autonomous engine.

## Usage

- Install CLI locally: `cd /home/dom/stateset-icommerce/cli && npm install && npm link`
- Use `stateset --db ./store.db "list customers"` for read-only actions.
- Add `--apply` for writes and `stateset-doctor` for checks.
- Seed demo data: `bash /mnt/skills/user/commerce-engine-setup/scripts/seed-demo.sh`
- Verify setup: `bash /mnt/skills/user/commerce-engine-setup/scripts/verify-setup.sh`
- Start autonomous mode: `stateset-autonomous start --db ./.stateset/commerce.db`

## Output

```json
{"status":"ok","db":"./store.db","sync":"disabled","autonomous":"stopped"}
```

## Present Results to User

- Steps completed and any scripts run.
- Database path and whether sync is initialized.
- Autonomous engine status if started.

## Troubleshooting

- CLI not found: re-run `npm link` or install `@stateset/cli` globally.
- Database locked: close other processes using the DB file.
- Sequencer unreachable: verify Docker services and URLs.

## References
- references/setup-runbook.md
- /home/dom/stateset-icommerce/examples/README.md
- /home/dom/stateset-icommerce/examples/getting-started-sync.md
- /home/dom/stateset-icommerce/cli/README.md
- /home/dom/stateset-icommerce/cli/bin/stateset-autonomous.js
