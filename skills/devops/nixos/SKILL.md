---
name: nixos
description: NixOS and Nix flake development for multi-repo architectures, airgapped deployments, and K3s infrastructure. Use when working with flake.nix files, NixOS modules, derivations, devShells, overlays, OCI image packaging, or composing multiple flake repositories. Covers Nix language syntax, flake inputs/outputs, nixosModules exports, stdenv.mkDerivation, and home-manager integration.
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
