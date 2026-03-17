---
name: nix-patterns
description: NixOS module patterns. Use when creating or editing NixOS/home-manager modules, adding packages, or configuring programs.
---

# NixOS Module Patterns

## Directory structure
- `modules/home/*.nix` - Home-manager modules (user packages, dotfiles)
- `modules/nixos/*.nix` - NixOS modules (system services)
- `hosts/*/` - Machine-specific configuration
- `home/default.nix` - Main home-manager entry point

## Adding packages
```nix
home.packages = with pkgs; [
  package-name
] ++ lib.optionals (stdenv.hostPlatform.system == "x86_64-linux") [
  x86-only-package
];
```

## Creating a module
```nix
{ pkgs, ... }:
{
  home.packages = with pkgs; [ mypackage ];
  xdg.configFile."app/config.json".text = builtins.toJSON { setting = "value"; };
}
```

Import in `home/default.nix`:
```nix
imports = [ ../modules/home/mymodule.nix ];
```
