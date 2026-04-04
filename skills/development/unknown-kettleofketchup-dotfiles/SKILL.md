---
name: nixos
description: NixOS and Nix flake development for multi-repo architectures, airgapped deployments, and K3s infrastructure. Use when working with flake.nix files, NixOS modules, derivations, devShells, overlays, OCI image packaging, building NixOS installer ISOs, or composing multiple flake repositories. Covers Nix language syntax, flake inputs/outputs, nixosModules exports, stdenv.mkDerivation, home-manager integration, ISO closure consistency, and Charmbracelet gum TUI prompts for runtime installer configuration with YAML config persistence.
---

# NixOS Development

## Overview

Build and maintain NixOS configurations using Nix flakes. Focus on multi-repo composition, airgapped deployments, and declarative infrastructure.

## Quick Reference

| Task | Command |
|------|---------|
| Build package | `nix build .#packageName` |
| Enter devShell | `nix develop` |
| Update flake inputs | `nix flake update` |
| Update single input | `nix flake lock --update-input nixpkgs` |
| Show flake outputs | `nix flake show` |
| Check flake | `nix flake check` |
| Rebuild NixOS | `sudo nixos-rebuild switch --flake .#hostname` |
| Build ISO | `nix build .#nixosConfigurations.iso.config.system.build.isoImage` |

## Flake Structure

Standard multi-repo flake pattern:

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    # Pin dependent flakes to same nixpkgs
    other-flake.url = "git+ssh://gitlab.example.com/repo";
    other-flake.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, other-flake, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      # NixOS system configurations
      nixosConfigurations.hostname = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [
          other-flake.nixosModules.default
          ./configuration.nix
        ];
      };

      # Reusable NixOS modules
      nixosModules.default = import ./modules;

      # Packages
      packages.${system} = { /* ... */ };

      # Development shells
      devShells.${system}.default = pkgs.mkShell { /* ... */ };
    };
}
```

## NixOS Module Pattern

Export modules for composition:

```nix
# modules/default.nix
{ config, lib, pkgs, ... }:
{
  imports = [ ./service.nix ];

  options.myModule.enable = lib.mkEnableOption "my module";

  config = lib.mkIf config.myModule.enable {
    # configuration here
  };
}
```

## OCI Image Packaging

For airgapped deployments, package images as store paths:

```nix
# Single image to OCI tarball
imagePackage = pkgs.runCommand "image-name" {
  buildInputs = [ pkgs.skopeo ];
} ''
  skopeo copy docker://registry/image:tag oci-archive:$out
'';
```

## Helm + Kustomize in Nix

Render manifests at build time:

```nix
manifests = pkgs.runCommand "manifests" {
  buildInputs = [ pkgs.kubernetes-helm pkgs.kustomize ];
} ''
  helm template release ${./chart} --namespace ns > base.yaml
  kustomize build ${./overlays} > $out
'';
```

## ISO Building & Runtime Configuration

Build reproducible installer ISOs with runtime user prompts that don't affect the flake closure.

**Closure rule**: Anything resolved at build time (Nix paths, `writeText`, package versions) is part of the closure. Anything resolved at runtime (user input, env vars, files read by scripts) is not.

**Pattern**: Include `gum` (Charmbracelet) in ISO packages → prompt user at boot → write answers to `site-config.yaml` → apply config via activation scripts or systemd services. Same ISO works across all hosts. On upgrades, load existing YAML and pre-fill prompts with current values.

```nix
# Include in ISO module
environment.systemPackages = with pkgs; [ gum yq-go glow ];
```

See `references/iso-building.md` for ISO configuration, closure consistency rules, and bundling flake source.
See `references/gum-prompts.md` for Charmbracelet gum prompt patterns, YAML config persistence, and upgrade flows.

## Private Git Repos (git+ssh://)

Flake input fetching (`builtins.fetchGit`) runs in the **client/evaluator process** as the **calling user** — NOT the nix daemon. The daemon only handles sandboxed builds.

- **Developer**: SSH just works via `~/.ssh/`
- **sudo nixos-rebuild**: Use `--use-remote-sudo` or deploy key in `/root/.ssh/`
- **CI runner**: Set `GIT_SSH_COMMAND` with absolute paths to SSH config/key (bypasses DynamicUser `~` resolution)
- **Never unset `GIT_SSH_COMMAND`** in CI `before_script` — fetchGit needs it
- **Avoid `--override-input`** on CI for production builds — `path:` inputs produce different derivation hashes than `git+ssh://`, breaking binary cache sharing

See `references/private-repos.md` for full setup guide, CI runner NixOS config, and troubleshooting.

## Detailed References

For comprehensive documentation on specific topics:

| Topic | Reference File |
|-------|----------------|
| Nix language syntax | `references/nix-language.md` |
| Flake inputs/outputs | `references/flakes.md` |
| NixOS modules & options | `references/nixos-modules.md` |
| Packaging & derivations | `references/packaging.md` |
| DevShells & overlays | `references/devshells.md` |
| Home Manager | `references/home-manager.md` |
| Private repos & SSH | `references/private-repos.md` |
| ISO building & closure consistency | `references/iso-building.md` |
| Charmbracelet gum prompts & YAML config | `references/gum-prompts.md` |

## Common Patterns

### Pin nixpkgs across repos
Use `inputs.X.inputs.nixpkgs.follows = "nixpkgs"` to ensure consistent package versions.

### Conditional module loading
```nix
imports = lib.optionals config.feature.enable [ ./optional-module.nix ];
```

### Lazy evaluation with mkIf
Always use `lib.mkIf` for conditional config to avoid infinite recursion:
```nix
config = lib.mkIf config.myService.enable { /* ... */ };
```

### Override priorities
- `lib.mkDefault` (priority 1000) - easily overridable defaults
- `lib.mkForce` (priority 50) - force value regardless of other definitions
- `lib.mkOverride N` - custom priority (lower = higher priority)

## Troubleshooting

### "error: getting status of '/nix/store/...': No such file or directory"
Missing store path. Run `nix build` or ensure binary cache is configured.

### "error: infinite recursion encountered"
Using config values in imports or not wrapping conditional config in `lib.mkIf`.

### "error: attribute 'X' missing"
Check flake inputs match expected names. Verify `follows` directives.

### Flake not seeing local changes
Run `git add .` - flakes ignore untracked files.
