---
name: configuration-patterns
description: Enforce Nix + Pixi + direnv + Home-manager configuration patterns
icon: "shield"
category: infrastructure
tools:
  - conftest
  - nix
  - pixi
  - direnv
---

# Configuration Patterns Skill

> **Hard Guardrails** for configuration management in this repository.
> Reference: `docs/adr/adr-003-version-management.md`

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                      USER ENVIRONMENT                             │
├──────────────────────────────────────────────────────────────────┤
│  direnv (.envrc)                                                  │
│    └── `use flake` → Automatic environment activation             │
├──────────────────────────────────────────────────────────────────┤
│  Nix Flake (flake.nix)                    Pixi (pixi.toml)       │
│  ├── System packages (git, helix)         ├── ROS2 Humble         │
│  ├── Development tools (cargo, gcc)       ├── Python packages     │
│  ├── LSP servers (pyright, nil)           ├── Node.js             │
│  └── Home-manager modules                 └── Conda ecosystem     │
├──────────────────────────────────────────────────────────────────┤
│  Home-manager Modules (modules/)                                  │
│  ├── common/    Cross-platform (shells, editor, direnv)          │
│  ├── linux/     Linux-specific (systemd, docker, udev)           │
│  └── macos/     macOS-specific (homebrew, system.nix)            │
├──────────────────────────────────────────────────────────────────┤
│  DevPod (.devcontainer/devcontainer.json)                        │
│    └── Remote development with Nix + volume caching              │
└──────────────────────────────────────────────────────────────────┘
```

## Hard Guardrails

### MUST USE

| Tool | File | Purpose |
|------|------|---------|
| **Nix flakes** | `flake.nix` | System packages, dev shells |
| **Pixi** | `pixi.toml` | ROS2, Python, conda packages |
| **direnv** | `.envrc` | Auto-activate `use flake` |
| **Home-manager** | `modules/` | User configuration |
| **Lock files** | `*.lock` | Reproducibility |

### MUST NOT USE

| Tool | File | Violation |
|------|------|-----------|
| **mise/rtx** | `.mise.toml`, `.tool-versions` | Redundant with Nix + Pixi |
| **asdf** | `.asdfrc` | Superseded by mise, which is superseded by Nix |
| **0install** | `*.0install.xml` | Conflicts with Nix store |
| **pyenv** | `.python-version` | Use pixi.toml Python version |
| **nvm** | `.nvmrc` | Use pixi.toml or flake.nix Node.js |
| **Symlinks** | `*` (type=symlink) | Causes Git/Windows/tooling issues |

### Symlink Warning

**Nix and Home-manager use symlinks by design:**
- `~/.config/*` → `/nix/store/...-home-manager-files/...`
- `~/.nix-profile` → `/nix/var/nix/profiles/...`

If symlinks are unacceptable:
- **For project configs**: Use actual files, not symlinks
- **For user dotfiles**: Consider **chezmoi** instead of Home-manager
- **For Nix itself**: No alternative - Nix fundamentally uses symlinks

## Responsibility Matrix

| Category | Primary Tool | File Location |
|----------|-------------|---------------|
| System CLI tools | Nix | `flake.nix` |
| Development shells | Nix devshell | `flake.nix` |
| ROS2 packages | Pixi + RoboStack | `pixi.toml` |
| Python packages | Pixi + conda-forge | `pixi.toml` |
| Node.js runtime | Pixi or Nix | `pixi.toml` or `flake.nix` |
| Rust toolchain | Nix | `flake.nix` |
| Shell configuration | Home-manager | `modules/common/shell/` |
| Editor configuration | Home-manager | `modules/common/editor/` |
| Docker images | DevContainer | `.devcontainer/` |

## Validation Commands

```bash
# Validate configuration policies
conftest test . --policy .claude/policies/configuration.rego

# Check for forbidden files
ls .tool-versions .mise.toml .asdfrc 2>/dev/null && echo "VIOLATION!" || echo "OK"

# Verify direnv integration
grep -q "use flake" .envrc && echo "OK" || echo "VIOLATION: .envrc missing 'use flake'"

# Verify lock files exist
[[ -f flake.lock && -f pixi.lock ]] && echo "OK" || echo "VIOLATION: Missing lock files"

# Verify Home-manager module structure
find modules/ -name "*.nix" -exec grep -L "lib\|mkDefault\|mkOption" {} \;
```

## When to Consider Alternatives

### chezmoi (Dotfile Management)

**Consider When:**
- Users need portable dotfiles across non-Nix systems
- Template-heavy per-user configuration is needed
- 1Password/pass secret integration required

**Do NOT Use For:**
- Project configuration (use `flake.nix`)
- Development shells (use devshell)
- Package management (use Nix/Pixi)

### mise (Runtime Version Manager)

**Consider When:**
- Non-Nix users need quick onboarding
- Runtime version switching during active development
- CI environments without Nix available

**Do NOT Use For:**
- ROS2 packages (no RoboStack equivalent)
- Reproducible builds (less rigorous than Nix)
- Primary development workflow

### Decision Tree

```
Need to manage configuration?
├── Project-level packages → Nix (flake.nix) or Pixi (pixi.toml)
├── Project-level shells → Nix devshell
├── User-level dotfiles?
│   ├── Nix system available → Home-manager
│   └── Portable/non-Nix → chezmoi
├── Runtime version switching?
│   ├── Reproducibility critical → Nix + pixi environments
│   └── Quick switching needed → mise (fallback only)
└── Remote development → DevPod with .devcontainer/
```

## Module Patterns

### Home-manager Module Template

```nix
# modules/common/example.nix
{ config, lib, pkgs, ... }:
let
  inherit (lib) mkDefault mkOption types;
in
{
  options.example = {
    enable = mkOption {
      type = types.bool;
      default = true;
      description = "Enable example configuration";
    };
  };

  config = lib.mkIf config.example.enable {
    # Configuration here
  };
}
```

### direnv stdlib Extensions

```bash
# In modules/common/direnv.nix → programs.direnv.stdlib

# Enhanced use_flake with pixi integration
use_flake_pixi() {
  use flake
  if [[ -f pixi.toml ]]; then
    eval "$(pixi shell-hook)"
  fi
}

# ROS2 workspace layout
layout_ros2() {
  export ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-0}
  if [[ -f install/local_setup.bash ]]; then
    source install/local_setup.bash
  fi
}
```

### DevContainer Requirements

```json
{
  "name": "project-name",
  "features": {
    "ghcr.io/devcontainers/features/nix:1": {
      "extraNixConfig": "experimental-features = nix-command flakes"
    }
  },
  "mounts": [
    "source=nix-store,target=/nix,type=volume"
  ],
  "postCreateCommand": "direnv allow && nix develop"
}
```

## Enforcement Integration

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: config-policy-check
        name: Configuration Policy Check
        entry: conftest test --policy .claude/policies/configuration.rego
        language: system
        files: '(flake\.nix|pixi\.toml|\.envrc|modules/.*\.nix)$'
```

### CI Workflow

```yaml
# .github/workflows/config-check.yml
name: Configuration Policy Check

on:
  push:
    paths:
      - 'flake.nix'
      - 'pixi.toml'
      - '.envrc'
      - 'modules/**'
      - '.devcontainer/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check forbidden files
        run: |
          ! ls .tool-versions .mise.toml .asdfrc 2>/dev/null
      - name: Validate with conftest
        run: |
          conftest test . --policy .claude/policies/configuration.rego
```

## Routing Command

```
@config - Route to Configuration Patterns validation
```

## References

- ADR-003: `docs/adr/adr-003-version-management.md`
- Tooling Analysis: `docs/TOOLING-ANALYSIS.md`
- OPA Policies: `.claude/policies/configuration.rego`
- direnv config: `modules/common/direnv.nix`
