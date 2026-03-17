---
name: Nix Ecosystem
description: This skill should be used when the user asks to "write nix", "nix expression", "flake.nix", "home-manager config", "programs.*", "services.*", or works with Nix language, flakes, or Home Manager. Provides comprehensive Nix ecosystem patterns and best practices.
---

# Nix Ecosystem

## Core Concepts

- **Lazy evaluation**: Expressions computed only when needed
- **Pure functions**: Same inputs always produce same outputs
- **Attribute sets**: Primary data structure `{ attr = value; }`
- **Reproducibility**: Builds are deterministic and cacheable

## Language Patterns

```nix
# let-in for local bindings
let
  helper = x: x + 1;
in helper 5

# with brings set into scope (avoid nesting)
with pkgs; [ git vim tmux ]

# inherit copies attributes
{ inherit (pkgs) git vim; inherit name; }

# Overlay for extending nixpkgs
final: prev: {
  myPackage = prev.myPackage.override { ... };
}

# callPackage for dependency injection
myPackage = pkgs.callPackage ./package.nix { };
```

## mkDerivation

```nix
pkgs.stdenv.mkDerivation {
  pname = "mypackage";
  version = "1.0.0";
  src = fetchFromGitHub { ... };

  nativeBuildInputs = [ pkgs.cmake ];  # Build-time tools
  buildInputs = [ pkgs.openssl ];       # Runtime libraries

  installPhase = ''
    mkdir -p $out/bin
    cp mypackage $out/bin/
  '';
}
```

## Flake Structure

```nix
{
  description = "Project description";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, ... }:
  let
    systems = [ "x86_64-linux" "aarch64-darwin" ];
    forAllSystems = nixpkgs.lib.genAttrs systems;
  in {
    packages = forAllSystems (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in { default = pkgs.hello; }
    );

    devShells = forAllSystems (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in {
        default = pkgs.mkShell {
          packages = [ pkgs.nodejs ];
        };
      }
    );
  };
}
```

## Home Manager

```nix
{ config, pkgs, lib, ... }:
{
  home.stateVersion = "24.11";  # Don't change after initial setup

  programs.git = {
    enable = true;
    userName = "name";
    userEmail = "email";
    extraConfig.init.defaultBranch = "main";
  };

  programs.neovim = {
    enable = true;
    viAlias = true;
    plugins = with pkgs.vimPlugins; [ vim-commentary ];
  };

  programs.direnv = {
    enable = true;
    nix-direnv.enable = true;
  };

  home.sessionVariables = { EDITOR = "nvim"; };
  home.sessionPath = [ "$HOME/.local/bin" ];

  # Manual dotfiles
  xdg.configFile."app/config".source = ./config;
}
```

## Module Structure

```nix
{ config, lib, pkgs, ... }:
{
  options.myModule = {
    enable = lib.mkEnableOption "my module";
    setting = lib.mkOption {
      type = lib.types.str;
      default = "value";
    };
  };

  config = lib.mkIf config.myModule.enable {
    # configuration when enabled
  };
}
```

## Anti-Patterns

- **Impure paths**: Use fetchurl, fetchFromGitHub instead of absolute paths
- **Nested with**: Prefer explicit `pkgs.git` for clarity
- **rec overuse**: Use let-in for complex recursive definitions

## Commands

- `nix flake update` - Update all inputs
- `nix flake show` - Display outputs
- `nix flake check` - Validate flake
- `nix build` / `nix develop` / `nix run`

## NixOS with Home Manager

```nix
# As NixOS module
{
  imports = [ home-manager.nixosModules.home-manager ];

  home-manager.useGlobalPkgs = true;
  home-manager.useUserPackages = true;
  home-manager.users.username = import ./home.nix;
}

# Standalone
homeConfigurations."user@host" = home-manager.lib.homeManagerConfiguration {
  pkgs = nixpkgs.legacyPackages.x86_64-linux;
  modules = [ ./home.nix ];
};
```
