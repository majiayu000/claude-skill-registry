---
name: Automated Updates
description: How the devbox automatically updates llm-agents (claude-code) via GitHub Actions and systemd timers. Use when debugging update failures or understanding the update flow.
---

# Automated Updates

The devbox automatically keeps `llm-agents` packages up to date via a GitHub Actions + systemd timer pipeline.

## What Gets Updated

The pipeline updates the `llm-agents` input in `flake.lock`, which provides:

- **claude-code**: Official Claude Code CLI
- **ccusage**: Usage analytics and statusline
- **beads**: Distributed issue tracker
- **opencode**: OpenCode CLI (alternative AI coding tool)
- **ccusage-opencode**: Usage tracking for OpenCode

All packages use Numtide's binary cache for fast updates.

**Note**: The oh-my-opencode *plugin* is NOT managed by this pipeline. It's an npm package installed per-machine via `npx oh-my-opencode install`. See the `setting-up-oh-my-opencode` skill for configuration details.

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│ GitHub Actions (every 4 hours)                              │
│                                                             │
│  1. update-llm-agents.yml runs                              │
│  2. Updates flake.lock (llm-agents input only)              │
│  3. Opens/updates PR on auto/update-llm-agents branch       │
│  4. Enables auto-merge (squash)                             │
│                                                             │
│  CI (ci.yml) runs nix flake check on PR                     │
│  ↓                                                          │
│  Checks pass → PR auto-merges to main                       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Devbox (systemd timer, every 4 hours)                       │
│                                                             │
│  1. pull-workstation.timer triggers                         │
│  2. Fetches origin/main                                     │
│  3. If updates: git pull --ff-only                          │
│  4. Runs: home-manager switch --flake .#dev                 │
└─────────────────────────────────────────────────────────────┘
```

## Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `ci.yml` | `.github/workflows/` | Runs `nix flake check` on PRs |
| `update-llm-agents.yml` | `.github/workflows/` | Updates llm-agents, opens PR with auto-merge |
| `UPDATE_TOKEN` | GitHub Secrets | PAT for PR creation + CI triggers |
| `pull-workstation` | `~/.local/bin/` | Script to pull + apply home-manager |
| `pull-workstation.timer` | systemd user | Triggers every 4h + 10min after boot |
| `home-manager-auto-expire.timer` | systemd user | Cleans old generations daily |

## Checking Status

### GitHub Side

```bash
# Recent workflow runs
gh run list --workflow=update-llm-agents.yml --limit=5

# Open update PRs
gh pr list --head auto/update-llm-agents

# CI status on a PR
gh pr checks <pr-number>
```

### Devbox Side

```bash
# Timer status
systemctl --user status pull-workstation.timer
systemctl --user status home-manager-auto-expire.timer

# When timers will next run
systemctl --user list-timers

# Recent pull-workstation runs
journalctl --user -u pull-workstation -n 50

# Recent auto-expire runs
journalctl --user -u home-manager-auto-expire -n 50
```

## Manual Trigger

### Trigger GitHub Update

```bash
gh workflow run update-llm-agents.yml
```

### Trigger Devbox Pull

```bash
~/.local/bin/pull-workstation
```

Or via systemd:

```bash
systemctl --user start pull-workstation
```

## Troubleshooting

### PR not being created

1. Check workflow ran: `gh run list --workflow=update-llm-agents.yml --limit=1`
2. Check for errors: `gh run view <run-id> --log`
3. Verify `UPDATE_TOKEN` secret exists: `gh secret list`

### PR not auto-merging

1. Check CI passed: `gh pr checks <pr-number>`
2. Check auto-merge is enabled: `gh pr view <pr-number>`
3. Check branch protection: Settings → Branches → main

### Devbox not pulling updates

1. Check timer is active: `systemctl --user status pull-workstation.timer`
2. Check for dirty working tree: `git -C ~/projects/workstation status`
3. Check logs: `journalctl --user -u pull-workstation -n 50`
4. Manual test: `~/.local/bin/pull-workstation`

### "Working tree not clean" error

The pull script refuses to run if there are uncommitted changes:

```bash
cd ~/projects/workstation
git status
# Either commit, stash, or discard changes
```

### SSH errors in pull-workstation

The script uses `BatchMode=yes` which fails if:
- SSH key missing: Check `~/.ssh/id_ed25519_github` exists
- Host key missing: Run `ssh -T git@github.com` once manually

### Old generations piling up

Check auto-expire is running:

```bash
systemctl --user status home-manager-auto-expire.timer
journalctl --user -u home-manager-auto-expire -n 20
```

Manual cleanup:

```bash
home-manager expire-generations "-7 days"
nix-collect-garbage
```

## Configuration

### Update Frequency

Both GitHub Action and devbox timer run every 4 hours. To change:

**GitHub Action:** Edit `.github/workflows/update-llm-agents.yml`:
```yaml
schedule:
  - cron: '0 */4 * * *'  # Change */4 to desired interval
```

**Devbox timer:** Edit `users/dev/home.linux.nix`:
```nix
Timer = {
  OnStartupSec = "10min";
  OnUnitInactiveSec = "4h";  # Change to desired interval
};
```

### Generation Retention

Edit `users/dev/home.linux.nix`:
```nix
services.home-manager.autoExpire = {
  frequency = "daily";
  timestamp = "-7 days";  # Keep generations from last 7 days
};
```
