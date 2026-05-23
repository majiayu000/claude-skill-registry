---
name: nix-best-practices
description: Nix patterns for flakes, overlays, unfree handling, and binary overlays. Use when working with flake.nix or shell.nix.
---

# Nix Best Practices

## Flake Structure

Standard flake.nix structure:

```nix
{
  description = "Project description";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # packages here
          ];
        };
      });
}
```

## Follows Pattern (Avoid Duplicate Nixpkgs)

When adding overlay inputs, use `follows` to share the parent nixpkgs and avoid downloading multiple versions:

```nix
inputs = {
  nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  # Overlay follows parent nixpkgs
  some-overlay.url = "github:owner/some-overlay";
  some-overlay.inputs.nixpkgs.follows = "nixpkgs";

  # Chain follows through intermediate inputs
  another-overlay.url = "github:owner/another-overlay";
  another-overlay.inputs.nixpkgs.follows = "some-overlay";
};
```

All inputs must be listed in outputs function even if not directly used:

```nix
outputs = { self, nixpkgs, some-overlay, another-overlay, ... }:
```

## Applying Overlays

Overlays modify or add packages to nixpkgs:

```nix
let
  pkgs = import nixpkgs {
    inherit system;
    overlays = [
      overlay1.overlays.default
      overlay2.overlays.default
      # Inline overlay
      (final: prev: {
        myPackage = prev.myPackage.override { ... };
      })
    ];
  };
in
```

## Handling Unfree Packages

### Option 1: nixpkgs-unfree (Recommended for Teams)

Use numtide/nixpkgs-unfree for EULA-licensed packages without requiring user config:

```nix
inputs = {
  nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  nixpkgs-unfree.url = "github:numtide/nixpkgs-unfree/nixos-unstable";
  nixpkgs-unfree.inputs.nixpkgs.follows = "nixpkgs";

  # Unfree overlay follows nixpkgs-unfree
  proprietary-tool.url = "github:owner/proprietary-tool-overlay";
  proprietary-tool.inputs.nixpkgs.follows = "nixpkgs-unfree";
};
```

This chains: `proprietary-tool` → `nixpkgs-unfree` → `nixpkgs`

### Option 2: User Config

Users add to `~/.config/nixpkgs/config.nix`:

```nix
{ allowUnfree = true; }
```

### Option 3: Specific Packages (Flake)

```nix
let
  pkgs = import nixpkgs {
    inherit system;
    config.allowUnfreePredicate = pkg: builtins.elem (lib.getName pkg) [
      "specific-package"
    ];
  };
in
```

Note: `config.allowUnfree` in flake.nix doesn't work with `nix develop` - use nixpkgs-unfree or user config.

## Creating Binary Overlay Repos

When nixpkgs builds a community version lacking features (common with open-core tools), create an overlay that fetches official binaries.

### Pattern (see 0xBigBoss/atlas-overlay, 0xBigBoss/bun-overlay)

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        version = "1.0.0";

        # Platform-specific binaries
        sources = {
          "x86_64-linux" = {
            url = "https://example.com/tool-linux-amd64-v${version}";
            sha256 = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
          };
          "aarch64-linux" = {
            url = "https://example.com/tool-linux-arm64-v${version}";
            sha256 = "sha256-BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=";
          };
          "x86_64-darwin" = {
            url = "https://example.com/tool-darwin-amd64-v${version}";
            sha256 = "sha256-CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC=";
          };
          "aarch64-darwin" = {
            url = "https://example.com/tool-darwin-arm64-v${version}";
            sha256 = "sha256-DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD=";
          };
        };

        source = sources.${system} or (throw "Unsupported system: ${system}");

        toolPackage = pkgs.stdenv.mkDerivation {
          pname = "tool";
          inherit version;

          src = pkgs.fetchurl {
            inherit (source) url sha256;
          };

          sourceRoot = ".";
          dontUnpack = true;

          installPhase = ''
            mkdir -p $out/bin
            cp $src $out/bin/tool
            chmod +x $out/bin/tool
          '';

          meta = with pkgs.lib; {
            description = "Tool description";
            homepage = "https://example.com";
            license = licenses.unfree;  # or appropriate license
            platforms = builtins.attrNames sources;
          };
        };
      in {
        packages.default = toolPackage;
        packages.tool = toolPackage;

        overlays.default = final: prev: {
          tool = toolPackage;
        };
      })
    // {
      overlays.default = final: prev: {
        tool = self.packages.${prev.system}.tool;
      };
    };
}
```

### Getting SHA256 Hashes

```bash
nix-prefetch-url https://example.com/tool-linux-amd64-v1.0.0
# Returns hash in base32, convert to SRI format:
nix hash to-sri --type sha256 <base32-hash>
```

Or use SRI directly:
```bash
nix-prefetch-url --type sha256 https://example.com/tool-linux-amd64-v1.0.0
```

## Dev Shell Patterns

### Basic Shell

```nix
devShells.default = pkgs.mkShell {
  buildInputs = with pkgs; [
    nodejs
    python3
  ];

  shellHook = ''
    echo "Dev environment ready"
  '';
};
```

### With Environment Variables

```nix
devShells.default = pkgs.mkShell {
  buildInputs = with pkgs; [ postgresql ];

  # Set at shell entry
  DATABASE_URL = "postgres://localhost/dev";

  # Or in shellHook for dynamic values
  shellHook = ''
    export PROJECT_ROOT="$(pwd)"
  '';
};
```

### Native Dependencies (C Libraries)

```nix
devShells.default = pkgs.mkShell {
  buildInputs = with pkgs; [
    openssl
    postgresql
  ];

  # Expose headers and libraries
  shellHook = ''
    export C_INCLUDE_PATH="${pkgs.openssl.dev}/include:$C_INCLUDE_PATH"
    export LIBRARY_PATH="${pkgs.openssl.out}/lib:$LIBRARY_PATH"
    export PKG_CONFIG_PATH="${pkgs.openssl.dev}/lib/pkgconfig:$PKG_CONFIG_PATH"
  '';
};
```

## Direnv Integration

`.envrc` for flake projects:

```bash
use flake
```

For unfree packages without nixpkgs-unfree:

```bash
export NIXPKGS_ALLOW_UNFREE=1
use flake --impure
```

## Common Commands

```bash
# Update all inputs
nix flake update

# Update specific input
nix flake update some-input

# Check flake validity
nix flake check

# Show flake metadata
nix flake metadata

# Enter dev shell
nix develop

# Run command in dev shell
nix develop -c <command>

# Build package
nix build .#packageName

# Run package
nix run .#packageName
```

## Troubleshooting

### "unexpected argument" Error

All inputs must be listed in outputs function:
```nix
# Wrong
outputs = { self, nixpkgs }: ...

# Right (if you have more inputs)
outputs = { self, nixpkgs, other-input, ... }: ...
```

### Unfree Package Errors with nix develop

`config.allowUnfree` in flake.nix doesn't propagate to `nix develop`. Use:
1. nixpkgs-unfree input (recommended)
2. User's `~/.config/nixpkgs/config.nix`
3. `NIXPKGS_ALLOW_UNFREE=1 nix develop --impure`

### Duplicate Nixpkgs Downloads

Use `follows` to chain inputs to a single nixpkgs source.

### Overlay Not Applied

Ensure overlay is in the `overlays` list when importing nixpkgs:
```nix
pkgs = import nixpkgs {
  inherit system;
  overlays = [ my-overlay.overlays.default ];
};
```

### Hash Mismatch

Re-fetch with `nix-prefetch-url` and update the hash. Hashes change when upstream updates binaries at the same URL.
