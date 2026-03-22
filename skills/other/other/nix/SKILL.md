---
name: nix
description: Nix package manager for reproducible builds, flakes, nix-shell development environments, and declarative package management
category: DevOps Operations
---

# Skill: nix

## What I do

I provide reproducible, declarative package management and build systems. Every build is deterministic, isolated, and pinned to exact versions. I eliminate "works on my machine" problems by treating packages as immutable values built from pure functions.

## When to use me

- Creating reproducible development environments across teams and CI.
- Managing complex dependency trees with potential version conflicts.
- Building hermetic, bit-reproducible artefacts and immutable containers.
- Pinning exact dependencies for long-term project stability.
- Running multiple versions of tools side-by-side without interference.

## Core principles

1. **Reproducibility** - Same inputs always produce identical outputs, regardless of machine state.
2. **Purity** - Builds are hermetic; they cannot access the network or undeclared system state.
3. **Declarative** - Configuration is expressed as pure functions in the Nix language.
4. **Immutability** - Packages in `/nix/store` are never modified; upgrades create new versions.
5. **Atomic Operations** - Installations and upgrades succeed completely or leave the system unchanged.

## Patterns & examples

**Pattern: flake.nix for Go projects (Modern)**

```nix
{
  description = "Go project flake";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in {
        packages.default = pkgs.buildGoModule {
          pname = "myapp";
          version = "0.1.0";
          src = ./.;
          vendorHash = "sha256-abc123..."; # Pin dependencies
        };
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [ go_1_21 gopls golangci-lint ];
          shellHook = "echo 'Go development environment loaded'";
        };
      });
}
```

**Pattern: buildGoModule with testing**

```nix
pkgs.buildGoModule {
  pname = "myapp";
  version = "1.0.0";
  src = ./.;
  vendorHash = "sha256-abc...";
  checkPhase = ''
    go test -v ./...
  '';
  installPhase = ''
    install -Dm755 $GOPATH/bin/myapp $out/bin/myapp
  '';
}
```

**Pattern: Docker image from Nix**

```nix
pkgs.dockerTools.buildImage {
  name = "myapp";
  tag = "latest";
  contents = [ self.packages.${system}.default ];
  config.Cmd = [ "/bin/myapp" ];
}
```

## Anti-patterns

- ❌ **Impure Builds** - Accessing network/system state without declaring it in inputs.
- ❌ **Imperative Usage** - Using `nix-env -i` instead of declarative `flake.nix` or `shell.nix`.
- ❌ **Hardcoded Paths** - Using `/usr/bin/` instead of `${pkgs.package}/bin/command`.
- ❌ **Missing Lockfiles** - Not committing `flake.lock`, leading to non-deterministic builds.
- ❌ **Mixing Package Managers** - Using `apt` or `brew` alongside Nix for the same dependencies.


## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/DevOps-Operations/Nix.md`

## Related skills

- `infrastructure-as-code` - Declarative patterns for system state.
- `dependency-management` - Pinning and updating software versions.
- `docker` - Creating minimal, reproducible container images.
- `automation` - Scripting reproducible workflows.
