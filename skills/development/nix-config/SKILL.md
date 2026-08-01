---
name: nix-config
description: Declarative macOS environment management via Nix. Use when user wants
  to install packages, add CLI tools, configure programs, manage dotfiles, or modify
  their development environment. Covers adding pa
---

---
name: nix-config
description: Declarative macOS environment via Nix. Manages CLI packages, GUI apps (Homebrew/MAS), system settings, program configs, dotfiles, and services. Use when: (1) Adding packages, tools, or apps, (2) Configuring programs (Git, SSH, shells, etc.), (3) Modifying dotfiles or system settings, (4) Permission denied on config files (indicates Nix-managed), (5) Rebuilding system.
---

# Nix Config

Declarative macOS environment at `~/nix-config`. See the repo's CLAUDE.md for full architecture.

## Adding Packages

**CLI tools** → `users/tengjizhang/home/packages.nix`
```nix
home.packages = with pkgs; [
  ripgrep
  jq
  # ...
];
```

**GUI apps** → `users/tengjizhang/darwin.nix`
```nix
homebrew.casks = [ "raycast" "obsidian" ];
```

**Third-party taps** → Use full `tap/cask` path:
```nix
homebrew.casks = [ "steipete/tap/codexbar" ];
```

**Mac App Store** → `users/tengjizhang/darwin.nix`
```nix
homebrew.masApps = { "Things" = 904280696; };
```

## npm Package Pattern

For latest npm packages, use `pnpm dlx` wrapper:

```nix
(writeShellScriptBin "toolname" ''
  exec ${pnpm}/bin/pnpm dlx @scope/package@latest "$@"
'')
```

Examples in packages.nix: `claude`, `codex`, `gemini`, `gccli`

## Rebuild

```bash
cd ~/nix-config && make switch > /tmp/nix-switch.log 2>&1 && echo "✓ Switch succeeded" || echo "✗ Switch failed (see /tmp/nix-switch.log)"
```

## Workflow

1. Edit the appropriate .nix file
2. Commit changes (keeps git clean before rebuild)
3. `make switch` to rebuild and activate
4. Push changes

## Key Files

- `flake.nix` - Inputs/outputs, system definition
- `users/tengjizhang/home/packages.nix` - CLI packages
- `users/tengjizhang/home/programs.nix` - Program configs (git, neovim, etc.)
- `users/tengjizhang/darwin.nix` - Homebrew, macOS settings
