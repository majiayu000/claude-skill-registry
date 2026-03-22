---
name: disclaw
description: "Manage Discord workspace structure and OpenClaw routing as code. Use when creating/renaming/deleting Discord channels, categories, threads, or managing agent-to-channel bindings. Triggers on: Discord channels, workspace structure, channel setup, routing, binding, disclaw."
metadata:
  openclaw:
    requires:
      bins: [disclaw]
      config: [channels.discord.token]
---

# Disclaw — Discord Structure as Code

Disclaw manages Discord workspace **structure** (categories, channels, threads) and OpenClaw **agent-to-channel bindings** as code via a YAML config file.

**Disclaw vs Discord plugin:** Disclaw manages *structure* (create/rename/delete channels, categories, threads; manage bindings and routing gates). The Discord plugin manages *messaging* (send/receive, reactions, pins, thread replies). They do not conflict.

## Installation

```bash
npm install -g @ofan/disclaw
disclaw --version
```

### Prerequisites

1. **Discord bot token** must be in OpenClaw config at `channels.discord.token`
2. **Gateway API access** — add to `openclaw.json`:
   ```json5
   { gateway: { tools: { allow: ["gateway"] } } }
   ```
   This lets disclaw read/write config via the gateway API. Without it, disclaw falls back to CLI.
3. **Config file** — create `disclaw.yaml` in the workspace (see format below)

### Verify Setup

```bash
disclaw validate -c disclaw.yaml
disclaw diff -c disclaw.yaml
```

## Config File Format

The config file (`disclaw.yaml`) declares the desired state of Discord workspace structure.

```yaml
version: 1
managedBy: disclaw
guild: "YOUR_GUILD_ID"

channels:
  # Standalone channel (no category)
  - name: announcements
    topic: "Important announcements"

  # Category with channels
  - category: Engineering
    channels:
      - name: general
        threads: [Standup, Retro]
      - name: alerts
        topic: "Automated alerts only"

  # Another category
  - category: Support
    channels:
      - name: tickets
      - name: escalations

# OpenClaw agent bindings (optional)
openclaw:
  requireMention: false
  agents:
    main: general              # single channel
    siren: [general, alerts]   # multiple channels
    support:                   # with options
      channel: tickets
      requireMention: true
```

### Key rules

- `guild` is the Discord server ID (right-click server → Copy Server ID)
- Channel names must be lowercase, no spaces (Discord enforces this)
- Thread names can have spaces and mixed case
- Agent bindings reference channel names from the `channels` section
- `requireMention` controls whether the bot needs @mention to respond in that channel

## Commands

### `disclaw diff` — Show what would change

```bash
disclaw diff -c disclaw.yaml
disclaw diff -c disclaw.yaml --json          # structured output
disclaw diff -c disclaw.yaml --channel alerts # filter by channel
```

Shows: managed resources (create/update/delete/noop), unmanaged resources, unbound agents, stale agents, routing health warnings, and pinned messages.

### `disclaw apply` — Apply changes (dry-run by default)

```bash
disclaw apply -c disclaw.yaml          # dry-run (shows what would change)
disclaw apply -c disclaw.yaml --yes    # actually apply changes
disclaw apply -c disclaw.yaml --prune --yes  # also delete unmanaged resources
```

**Safety:** Always takes a snapshot before mutating. Creates before deletes. Bindings and routing gates are updated atomically.

### `disclaw import` — Import unmanaged Discord resources

```bash
disclaw import -c disclaw.yaml          # dry-run (shows what would be imported)
disclaw import -c disclaw.yaml --yes    # write to config file
```

Discovers Discord channels/categories/threads not in the config and adds them. Also finds unbound OpenClaw agents.

### `disclaw rollback` — Restore from snapshot

```bash
disclaw rollback -c disclaw.yaml          # dry-run
disclaw rollback -c disclaw.yaml --yes    # actually rollback
```

Restores Discord state from the most recent pre-apply snapshot. Drift-aware (shows what changed since the snapshot).

### `disclaw validate` — Validate config (no API calls)

```bash
disclaw validate -c disclaw.yaml
disclaw validate -c disclaw.yaml --json
```

Safe for CI. Checks: schema validity, empty names, duplicate channels/threads, binding refs pointing to non-existent channels.

### Filter flags (diff, apply, import)

```bash
--category <names...>   # filter by category name
--channel <names...>    # filter by channel name
--thread <names...>     # filter by thread name
--agent <names...>      # filter by agent name
--json                  # structured JSON output
```

### Gateway options (all commands except validate)

```bash
--gateway-url <url>     # override gateway URL (default: http://127.0.0.1:18789)
--gateway-token <token> # override gateway auth token
```

Also via env vars: `OPENCLAW_GATEWAY_URL`, `OPENCLAW_GATEWAY_TOKEN`.

## Common Workflows

### Add a new channel

1. Edit `disclaw.yaml` — add channel under the appropriate category
2. Validate: `disclaw validate -c disclaw.yaml`
3. Preview: `disclaw diff -c disclaw.yaml`
4. Apply: `disclaw apply -c disclaw.yaml --yes`

### Bind an agent to a channel

1. Edit `disclaw.yaml` — add entry under `openclaw.agents`
2. Preview: `disclaw diff -c disclaw.yaml`
3. Apply: `disclaw apply -c disclaw.yaml --yes`

This creates the binding AND allowlists the channel in routing gates automatically.

### Import existing Discord channels

1. Run: `disclaw import -c disclaw.yaml` (dry-run to preview)
2. Review the output
3. Run: `disclaw import -c disclaw.yaml --yes` (writes to config)
4. Verify: `disclaw diff -c disclaw.yaml`

### Delete a channel

1. Remove the channel from `disclaw.yaml`
2. Preview: `disclaw apply -c disclaw.yaml --prune`
3. Apply: `disclaw apply -c disclaw.yaml --prune --yes`

**Warning:** `--prune` is required for deletions. Without it, removed channels are shown as "unmanaged" but not deleted.

### Rename a channel

1. Change the channel name in `disclaw.yaml`
2. Preview: `disclaw diff -c disclaw.yaml` (shows delete old + create new)
3. Apply: `disclaw apply -c disclaw.yaml --yes`

Note: Discord doesn't support true renames via API — disclaw creates the new channel and (with `--prune`) deletes the old one.

## Troubleshooting

**"Discord bot token not found"**
- Ensure `channels.discord.token` is set in `openclaw.json`
- Or set `DISCORD_BOT_TOKEN` env var

**"Gateway tool not available"**
- Add `gateway.tools.allow: ["gateway"]` to `openclaw.json`
- Or disclaw will fall back to CLI automatically

**"Gateway auth failed"**
- Check `OPENCLAW_GATEWAY_TOKEN` env var matches `gateway.auth.token` in config
- Or pass `--gateway-token <token>`

**"OpenClaw CLI timed out"**
- Check if the gateway is running: `openclaw status`
- Check network: `curl http://127.0.0.1:18789/`

**"Discord connection timed out"**
- Check internet connectivity
- Verify bot token is valid
- Try again (Discord API can be flaky)

**"Permission denied" during apply**
- Bot needs: Manage Channels, Manage Threads permissions
- Check bot role position in Discord server settings

## Safety

- **Dry-run by default** — all mutating commands require `--yes`
- **Snapshot before apply** — automatic, saved to `.disclaw/snapshots/`
- **Rollback available** — `disclaw rollback -c disclaw.yaml --yes`
- **Managed-scope only** — disclaw only touches resources in the config
- **Creates before deletes** — safer ordering during apply
- **Validation** — config is validated before any API calls
