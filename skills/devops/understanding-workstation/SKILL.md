---
name: Understanding Workstation Config
description: This skill explains the workstation monorepo structure, how NixOS and home-manager are organized, and how to navigate the configuration. Use this when onboarding or trying to understand how the devbox is configured.
---

# Understanding Workstation Config

This repo manages a NixOS devbox with standalone home-manager.

## Repository Structure

```
workstation/
├── flake.nix                 # Single flake: system + home-manager
├── flake.lock                # Pinned nixpkgs version
│
├── hosts/                    # NixOS system configurations
│   └── devbox/
│       ├── configuration.nix # System packages, SSH, firewall, users
│       ├── hardware.nix      # Hetzner ARM-specific (boot, kernel)
│       └── disko.nix         # Disk partitioning
│
├── users/                    # Home-manager configurations
│   └── dev/
│       └── home.nix          # User env: git, tmux, nvim, bash
│
├── assets/                   # Content deployed by home-manager
│   ├── claude/               # Claude skills and commands
│   └── nvim/                 # Neovim Lua config (lua/user/)
│
├── secrets/                  # sops-nix encrypted secrets (skeleton)
│
├── scripts/                  # Helper scripts
│   └── update-ssh-config.sh
│
└── .claude/                  # THIS REPO's Claude documentation
    ├── skills/               # How to understand/modify this config
    └── commands/             # Quick actions for this repo
```

## Key Concepts

### Standalone Home-Manager

Home-manager is NOT a NixOS module here. This means:
- `sudo nixos-rebuild switch` only applies system changes
- `home-manager switch` applies user changes (faster, no sudo)
- They share the same nixpkgs pin via `pkgsFor` pattern

### assets/ vs .claude/

- `assets/claude/` — Skills deployed TO the devbox user (~/.claude/skills)
- `.claude/` — Skills for working WITH this repo (not deployed)

### pkgsFor Pattern

The flake defines `pkgsFor` once to prevent drift:

```nix
pkgsFor = system: import nixpkgs {
  inherit system;
  config.allowUnfree = true;
};
```

Both NixOS and home-manager use this, ensuring consistent packages.

### External Flake Inputs

LLM tools come from `numtide/llm-agents.nix`, passed to home-manager via `extraSpecialArgs`:

| Package | Source | Notes |
|---------|--------|-------|
| claude-code | llm-agents.nix | Daily updates, binary cache at cache.numtide.com |
| ccusage | llm-agents.nix | Usage analytics, statusline for Claude Code |
| beads | llm-agents.nix | Distributed issue tracker for AI workflows |
| devenv | nixpkgs | Development environments |

**Important:** We do NOT use `inputs.nixpkgs.follows` for llm-agents. This preserves binary cache hits from Numtide's cache.

### Claude Code Settings

The `~/.claude/settings.json` uses a "managed fragment + merge" pattern because Claude Code writes runtime state to this file:

- `~/.claude/settings.managed.json` — Nix-managed config (read-only symlink)
- `~/.claude/settings.json` — Mutable file Claude Code can write to
- On `home-manager switch`, managed keys are merged into settings.json
- Claude Code's runtime state (`feedbackSurveyState`, `enabledPlugins`, etc.) is preserved
- Our managed keys (like `statusLine`) win on conflict

## Common Tasks

| Task | Command |
|------|---------|
| Apply system changes | `sudo nixos-rebuild switch --flake .#devbox` |
| Apply user changes | `home-manager switch --flake .#dev` |
| Update nixpkgs | `nix flake update` |
| Check flake | `nix flake check` |

## Files to Edit

| Want to change... | Edit this file |
|-------------------|----------------|
| System packages | `hosts/devbox/configuration.nix` |
| User packages | `users/dev/home.nix` |
| Bash aliases | `users/dev/home.nix` (programs.bash) |
| Git config | `users/dev/home.nix` (programs.git) |
| Claude skills (deployed) | `assets/claude/skills/` |
| Neovim config | `assets/nvim/lua/user/` |
| SSH server settings | `hosts/devbox/configuration.nix` |
| Flake inputs | `flake.nix` |
| Claude Code statusline | `users/dev/home.nix` (managedSettings) |
