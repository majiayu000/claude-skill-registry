---
name: build-commands
description: Reference for NixOS build, test, and flake commands. Use when asked about rebuilding, checking config, formatting, or flake operations.
user-invocable: true
---

# Build/Test Commands

## NixOS Operations

- **Rebuild system**: `sudo nixos-rebuild switch`
- **Link dotfiles**: `sudo ln -s /home/cgeorgii/dots/* /etc/nixos`
- **Dry-run config check**: `nixos-rebuild dry-build`
- **Build specific config**: `nix build .#nixosConfigurations.coco.config.system.build.toplevel`

## Flake Operations

- **Check flake**: `nix flake check`
- **Update flake inputs**: `nix flake update`
- **Setup dev environment**: `nix develop` (enables pre-commit hooks and development tools)

## Formatting

- **Format Nix files**: `nixfmt file.nix`

## Important Notes

- User prefers to run sudo commands manually in a separate terminal
- Always ask before running system-level commands
- All configuration changes should be done declaratively through Nix files
