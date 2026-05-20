---
name: Rebuilding the Devbox
description: This skill covers how to apply configuration changes to the devbox, including full rebuilds with nixos-anywhere. Use this when you need to update the system or recover from issues.
---

# Rebuilding the Devbox

## Quick Reference

| Action | Command | When to use |
|--------|---------|-------------|
| Apply system changes | `sudo nixos-rebuild switch --flake .#devbox` | Changed hosts/devbox/* |
| Apply user changes | `home-manager switch --flake .#dev` | Changed users/dev/* |
| Full rebuild from scratch | See "Nuclear Option" below | Corrupted system, fresh start |

## Applying Changes

### System Changes (requires sudo)

After editing files in `hosts/devbox/`:

```bash
cd ~/projects/workstation
sudo nixos-rebuild switch --flake .#devbox
```

This rebuilds the NixOS system. May require reboot if kernel changed.

### User Changes (no sudo, fast)

After editing files in `users/dev/` or `assets/`:

```bash
cd ~/projects/workstation
home-manager switch --flake .#dev
```

This is fast (~10 seconds) and doesn't affect system services.

## Updating Packages

To update all flake inputs (nixpkgs, home-manager, etc.):

```bash
nix flake update
git add flake.lock
git commit -m "Update flake.lock"
```

Then apply as above.

## Nuclear Option: Full Rebuild with nixos-anywhere

If the devbox is corrupted or you want a fresh start:

### Prerequisites (on your Mac)

1. Ensure you have the latest config committed and pushed
2. Run `scripts/update-ssh-config.sh` to get current IP
3. Have `nixos-anywhere` available: `nix-shell -p nixos-anywhere`

### Steps

```bash
# From your Mac, targeting the devbox
nixos-anywhere --flake .#devbox root@devbox

# Wait for reboot, then SSH in
ssh devbox

# Apply home-manager (not included in nixos-anywhere)
cd ~/Code/workstation  # clone if needed
home-manager switch --flake .#dev
```

### After Rebuild

1. Re-authenticate GitHub: `gh auth login`
2. Clone workstation repo if needed
3. Apply home-manager config

## Troubleshooting

### "flake.nix not found"

Make sure you're in the workstation repo directory.

### Home-manager errors about missing files

The `assets/` directory must exist. Check that `assets/claude/skills/` exists.

### System won't boot after rebuild

Boot into previous generation from bootloader menu, then fix config.
