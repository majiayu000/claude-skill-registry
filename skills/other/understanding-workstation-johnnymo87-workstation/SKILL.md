---
name: Understanding Workstation Config
description: This skill explains the workstation monorepo structure, how NixOS (devbox) and nix-darwin (macOS) are organized with standalone home-manager, and how to navigate the configuration. Use this when onboarding or trying to understand how either platform is configured.
---

# Understanding Workstation Config

This repo manages two platforms with standalone home-manager:
- **NixOS devbox** — Hetzner ARM server (system: `aarch64-linux`)
- **nix-darwin macOS** — MacBook Pro (system: `aarch64-darwin`)

Both share the same home-manager base config. Platform differences are isolated in dedicated modules.

## Repository Structure

```
workstation/
├── flake.nix                 # Single flake: NixOS + nix-darwin + home-manager
├── flake.lock                # Pinned nixpkgs version
├── projects.nix              # Declarative project list (consumed by both platforms)
│
├── hosts/                    # System-level configurations
│   ├── devbox/               # NixOS system config
│   │   ├── configuration.nix # System packages, SSH, firewall, users
│   │   ├── hardware.nix      # Hetzner ARM-specific (boot, kernel)
│   │   └── disko.nix         # Disk partitioning
│   └── Y0FMQX93RR-2/        # macOS nix-darwin config
│
├── users/                    # Home-manager configurations
│   └── dev/
│       ├── home.nix           # Entry point (imports all modules below)
│       ├── home.base.nix      # Shared: git, bash, tmux, neovim, packages
│       ├── home.linux.nix     # Linux-only: systemd services, ensure-projects script
│       ├── home.darwin.nix    # macOS-only: launchd, ensure-projects activation, dotfiles migration
│       ├── opencode-config.nix # OpenCode managed config
│       ├── claude-skills.nix  # Claude Code skills deployed to ~/.claude/
│       ├── claude-hooks.nix   # Claude Code hooks (session start/stop)
│       ├── tmux.linux.nix     # Linux tmux extras
│       └── tmux.darwin.nix    # macOS tmux extras
│
├── assets/                   # Content deployed by home-manager
│   ├── claude/               # Claude skills and commands
│   ├── opencode/             # OpenCode config templates, prompts, agents
│   └── nvim/                 # Neovim Lua config (lua/user/)
│
├── secrets/                  # sops-nix encrypted secrets (devbox only)
│
├── scripts/                  # Helper scripts
│
└── .claude/                  # THIS REPO's Claude documentation
    ├── skills/               # How to understand/modify this config
    └── commands/             # Quick actions for this repo
```

## Key Concepts

### Standalone Home-Manager

Home-manager is NOT a NixOS module here. This means:

| Platform | System changes | User changes |
|----------|---------------|--------------|
| Devbox | `sudo nixos-rebuild switch --flake .#devbox` | `home-manager switch --flake .#dev` |
| macOS | `sudo darwin-rebuild switch --flake .#Y0FMQX93RR-2` | Included in darwin-rebuild |

On devbox, system and user are independent (faster iteration on user config).
On macOS, `darwin-rebuild` handles both system and home-manager in one command.

### Modular home.nix Structure

`home.nix` is just an import list:
```nix
imports = [
  ./home.base.nix      # Cross-platform (always applied)
  ./home.linux.nix     # Guarded with lib.mkIf isLinux
  ./home.darwin.nix    # Guarded with lib.mkIf isDarwin
  ./claude-skills.nix
  ./claude-hooks.nix
  ./opencode-config.nix
  ./tmux.linux.nix
  ./tmux.darwin.nix
];
```

All modules are imported on both platforms. Platform-specific modules use `lib.mkIf isLinux` or `lib.mkIf isDarwin` at the top level, so they evaluate to `{}` on the wrong platform.

### Platform Identity

| Property | Devbox | macOS |
|----------|--------|-------|
| Username | `dev` | `jonathan.mohrbacher` |
| Home dir | `/home/dev` | `/Users/jonathan.mohrbacher` |
| Projects dir | `~/projects/` | `~/Code/` |
| System type | `aarch64-linux` | `aarch64-darwin` |

**CRITICAL**: Never hardcode paths like `/home/dev` or `/Users/jonathan.mohrbacher`. Always use `config.home.homeDirectory`.

### projects.nix — Declarative Project List

`projects.nix` is a simple attrset consumed by both platforms:
```nix
{
  my-project = { url = "git@github.com:org/repo.git"; };
}
```

How each platform uses it:

| Platform | Mechanism | Clone target | Trigger |
|----------|-----------|-------------|---------|
| Devbox | `~/.local/bin/ensure-projects` script + systemd service | `~/projects/` | Login (systemd) or manual script |
| macOS | `home.activation.ensureProjects` in `home.darwin.nix` | `~/Code/` | `darwin-rebuild switch` |

### assets/ vs .claude/

- `assets/claude/` — Skills/commands deployed TO the user's `~/.claude/`
- `assets/opencode/` — OpenCode config templates, prompts, custom agents
- `.claude/` — Skills for working WITH this repo (not deployed anywhere)

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
| opencode | llm-agents.nix | OpenCode editor |
| devenv | nixpkgs | Development environments |

**Important:** We do NOT use `inputs.nixpkgs.follows` for llm-agents. This preserves binary cache hits from Numtide's cache.

### Merge-on-Activate Pattern

Both Claude Code and OpenCode settings use the same merge strategy:

1. Nix generates a `*.managed.json` (read-only, in Nix store)
2. On `home-manager switch`, an activation script merges managed → runtime
3. Managed keys win on conflict; runtime-only keys are preserved
4. This lets Claude Code / OpenCode write their own runtime state without clobbering

Files using this pattern:
- `~/.claude/settings.managed.json` → `~/.claude/settings.json`
- `~/.config/opencode/opencode.managed.json` → `~/.config/opencode/opencode.json`

### mkOutOfStoreSymlink — Out-of-Flake Paths

When `xdg.configFile.*.source` points to a path outside the flake (e.g., a cloned project), Nix pure evaluation fails:

```
access to absolute path '/Users' is forbidden in pure evaluation mode
```

**Solution**: Use `config.lib.file.mkOutOfStoreSymlink` — it defers path resolution to activation time:
```nix
xdg.configFile."opencode/plugins/opencode-pigeon.ts".source =
  config.lib.file.mkOutOfStoreSymlink (
    if isDarwin
    then "${config.home.homeDirectory}/Code/opencode-pigeon/src/index.ts"
    else "${config.home.homeDirectory}/projects/opencode-pigeon/src/index.ts"
  );
```

### Darwin Gradual Migration

On macOS, existing dotfiles may conflict with home-manager. The strategy is:

1. Disable conflicting HM programs with `lib.mkForce false`
2. Migrate one program at a time by removing the override
3. `home.activation.prepareForHM` removes stale symlinks before HM link-checking

Currently disabled on Darwin: `bash`, `ssh`, `neovim` (using existing dotfiles instead).

### Secrets

| Platform | Mechanism | Storage |
|----------|-----------|---------|
| Devbox | sops-nix | `/run/secrets/<name>`, env vars in `.bashrc` |
| macOS | macOS Keychain | `security find-generic-password -s <service> -w` |

## Common Tasks

| Task | Devbox | macOS |
|------|--------|-------|
| Apply system changes | `sudo nixos-rebuild switch --flake .#devbox` | `sudo darwin-rebuild switch --flake .#Y0FMQX93RR-2` |
| Apply user changes | `home-manager switch --flake .#dev` | (included in darwin-rebuild) |
| Update nixpkgs | `nix flake update` | `nix flake update` |
| Check flake | `nix flake check` | `nix flake check` |
| Add a project | Edit `projects.nix`, push, apply | Edit `projects.nix`, push, apply |

## Files to Edit

| Want to change... | Edit this file |
|-------------------|----------------|
| System packages (devbox) | `hosts/devbox/configuration.nix` |
| System packages (macOS) | `hosts/Y0FMQX93RR-2/configuration.nix` |
| User packages (both) | `users/dev/home.base.nix` |
| Bash aliases (both) | `users/dev/home.base.nix` (programs.bash) |
| Git config (both) | `users/dev/home.base.nix` (programs.git) |
| Linux systemd services | `users/dev/home.linux.nix` |
| macOS launchd agents | `users/dev/home.darwin.nix` |
| macOS dotfiles migration | `users/dev/home.darwin.nix` (disabled programs) |
| Declared projects | `projects.nix` |
| OpenCode agent models | `users/dev/opencode-config.nix` (ohMyManaged) |
| OpenCode MCP servers | `users/dev/opencode-config.nix` (opencodeBase) |
| OpenCode plugins | `users/dev/opencode-config.nix` (xdg.configFile plugins) |
| Claude skills (deployed) | `assets/claude/skills/` |
| Claude hooks | `users/dev/claude-hooks.nix` |
| Neovim config | `assets/nvim/lua/user/` |
| SSH settings | `users/dev/home.base.nix` (programs.ssh) |
| Flake inputs | `flake.nix` |
| Claude Code statusline | `users/dev/home.base.nix` (managedSettings) |
| Tmux config (shared) | `users/dev/home.base.nix` (programs.tmux) |
| Tmux config (Linux) | `users/dev/tmux.linux.nix` |
| Tmux config (macOS) | `users/dev/tmux.darwin.nix` |
