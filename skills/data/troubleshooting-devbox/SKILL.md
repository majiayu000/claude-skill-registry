---
name: troubleshooting-devbox
description: Use when SSH connection fails, host key mismatch, NixOS issues, or verifying devbox is properly configured
---

# Troubleshooting Devbox

## Overview

Common issues and fixes for the Hetzner NixOS remote development environment.

## Port Forwarding

The devbox connection uses several port forwards for development tools:

| Port | Direction | Purpose |
|------|-----------|---------|
| 4000 | Local (-L) | eternal-machinery dev server |
| 4003 | Local (-L) | eternal-machinery (secondary) |
| 1455 | Local (-L) | OpenCode OAuth callback for ChatGPT Plus authentication |
| 9222 | Remote (-R) | Chrome DevTools Protocol - control macOS browser from devbox |
| 3033 | Remote (-R) | chatgpt-relay - `/ask-question` CLI talks to macOS daemon |

**Local forwards (-L):** devbox service → accessible on macOS localhost
**Remote forwards (-R):** macOS service → accessible on devbox localhost

These should be configured in `~/.ssh/config` (see below) so every `ssh devbox` includes them automatically.

## Can't SSH After Recreate

Host key changed because server was recreated with new IP or reinstalled.

```bash
# Remove old host key
ssh-keygen -R devbox
ssh-keygen -R $(hcloud server ip devbox)

# Reconnect with new key acceptance
ssh -o StrictHostKeyChecking=accept-new devbox
```

## Verify NixOS Installation

Check NixOS version:

```bash
ssh devbox 'nixos-version'
# Expected: 24.11... (Vicuna)
```

Check tools are installed:

```bash
ssh devbox 'tmux -V && nvim --version | head -1 && mise --version'
```

## NixOS Configuration Issues

View current system generation:

```bash
ssh devbox 'sudo nix-env --list-generations --profile /nix/var/nix/profiles/system'
```

Rollback to previous generation:

```bash
ssh devbox 'sudo nixos-rebuild switch --rollback'
```

Check system journal for errors:

```bash
ssh devbox 'journalctl -b --priority=err'
```

## nixos-anywhere Deployment Failed

If deployment fails mid-way, the server may be in an inconsistent state.

Check if server is accessible:

```bash
# Try root (during nixos-anywhere)
ssh root@$(hcloud server ip devbox) 'uname -a'

# Try dev (after completion)
ssh dev@$(hcloud server ip devbox) 'uname -a'
```

If stuck, use Hetzner rescue mode:

```bash
hcloud server enable-rescue devbox --type linux64
hcloud server reboot devbox
# Then SSH as root with rescue password from console
```

Or just destroy and recreate:

```bash
/rebuild
```

## Verify SSH Hardening

```bash
# Should fail (root login disabled):
ssh root@$(hcloud server ip devbox) 'echo test'

# Should work:
ssh dev@$(hcloud server ip devbox) 'echo test'
```

## Connection Timeout / Slow

Check latency:

```bash
ping -c 5 $(hcloud server ip devbox)
```

Helsinki datacenter latency from US East: ~100-150ms (acceptable for terminal work).

## Server Not Responding

Check Hetzner console:

```bash
hcloud server list
hcloud server describe devbox
```

Power cycle if needed:

```bash
hcloud server reboot devbox
```

## Disk Space Issues

NixOS can accumulate old generations. Clean up:

```bash
ssh devbox 'sudo nix-collect-garbage --delete-older-than 7d'
ssh devbox 'sudo nix-store --optimise'
```

Check disk usage:

```bash
ssh devbox 'df -h /'
```

## Systemd User Timers

The devbox runs several user-level timers for automation.

### Check Timer Status

```bash
# List all user timers
systemctl --user list-timers

# Specific timers
systemctl --user status pull-workstation.timer
systemctl --user status home-manager-auto-expire.timer
```

### View Timer Logs

```bash
# Auto-update pull logs
journalctl --user -u pull-workstation -n 50

# Generation cleanup logs
journalctl --user -u home-manager-auto-expire -n 50
```

### Timer Not Running

If a timer isn't active after `home-manager switch`:

```bash
# Reload systemd
systemctl --user daemon-reload

# Enable and start timer
systemctl --user enable --now pull-workstation.timer
```

See [Automated Updates](.claude/skills/automated-updates/SKILL.md) for full details on the update pipeline.
