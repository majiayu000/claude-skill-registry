---
name: nix-environment
description: Nix flakes, home-manager, and reproducible environment management
icon: ❄️
category: environment
tools:
  - nix
  - nom
  - direnv
  - home-manager
---

# Nix Environment Skills

## Overview

This skill provides expertise in Nix-based environment management including flakes, home-manager, and cross-platform configurations.

## Development Shell

### Enter Environment
```bash
nom develop                           # Preferred (with progress UI)
nix develop                           # Standard
direnv allow                          # Automatic via direnv
```

### Shell Commands (defined in devshell)
| Command | Description |
|---------|-------------|
| `cb` | `colcon build --symlink-install` |
| `ct` | `colcon test` |
| `ctr` | `colcon test-result --verbose` |
| `ros2-env` | Show ROS2 environment variables |
| `update-deps` | Run `pixi update` |
| `ai` | AI chat assistant (aichat) |
| `pair` | AI pair programming (aider) |

## Flake Operations

### Check and Validate
```bash
nix flake check                       # Validate flake
nix flake check --no-build            # Quick syntax check
nix flake show                        # Show flake outputs
```

### Update Dependencies
```bash
nix flake update                      # Update all inputs
nix flake lock --update-input nixpkgs # Update specific input
```

### Build Outputs
```bash
nix build .#package                   # Build specific output
nix build -L                          # Build with logs
nix log /nix/store/...                # View build log
```

## Package Management

### Nix Profile
```bash
nix profile install nixpkgs#package   # Install package
nix profile remove package            # Remove package
nix profile list                      # List installed
nix profile upgrade '.*'              # Upgrade all
```

### Search Packages
```bash
nix search nixpkgs package            # Search nixpkgs
nix search nixpkgs#python3Packages.X  # Search Python packages
```

## Home Manager

### Importing Modules
This flake exports home-manager modules that can be imported:

```nix
{
  inputs = {
    ripple-env.url = "github:FlexNetOS/ripple-env";
    home-manager.url = "github:nix-community/home-manager";
  };

  outputs = { self, nixpkgs, home-manager, ripple-env, ... }: {
    homeConfigurations.myuser = home-manager.lib.homeManagerConfiguration {
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
      modules = [
        ripple-env.homeManagerModules.default
        # Your modules...
      ];
    };
  };
}
```

### Available Exports
| Export | Description |
|--------|-------------|
| `homeManagerModules.default` | All modules (platform-detected) |
| `homeManagerModules.common` | Cross-platform modules only |
| `homeManagerModules.linux` | Linux-specific modules |
| `homeManagerModules.macos` | macOS-specific modules |
| `nixosModules.default` | NixOS system module |
| `darwinModules.default` | nix-darwin module |
| `lib` | Utility functions |

### Module Options

Each module supports enable/disable:
```nix
{
  ros2-env.shell.zsh.enable = true;
  ros2-env.shell.nushell.enable = true;
  ros2-env.editor.helix.enable = true;
  ros2-env.direnv.enable = true;
}
```

## Pixi Integration

### Package Management
```bash
pixi add <package>                    # Add package
pixi remove <package>                 # Remove package
pixi search <pattern>                 # Search packages
pixi update                           # Update lockfile
pixi install                          # Install from lockfile
pixi info                             # Environment info
```

### ROS2 Packages
```bash
pixi add ros-humble-desktop           # Full desktop
pixi add ros-humble-rviz2             # Visualization
pixi search ros-humble-*              # List all ROS packages
```

## direnv Configuration

### Setup
```bash
direnv allow                          # Allow directory
direnv deny                           # Deny directory
direnv reload                         # Reload environment
```

### .envrc File
```bash
# Standard flake integration
use flake

# With nix-direnv caching
use flake . --impure
```

## Cross-Platform Support

### Platform Detection in Nix
```nix
{ pkgs, lib, ... }:
let
  isLinux = pkgs.stdenv.isLinux;
  isDarwin = pkgs.stdenv.isDarwin;
in {
  config = lib.mkMerge [
    (lib.mkIf isLinux { /* Linux config */ })
    (lib.mkIf isDarwin { /* macOS config */ })
  ];
}
```

### Windows/WSL2
- Use `bootstrap.ps1` for automated setup
- NixOS-WSL provides full Nix experience
- See: `.github/docs/self-hosted-runner-setup.md`

## Debugging

### Flake Issues
```bash
nix flake check                       # Check for errors
nix flake show                        # Show structure
nix eval .#someOutput                 # Evaluate expression
nix repl                              # Interactive REPL
```

### Build Issues
```bash
nix build -L                          # Verbose build output
nix log /nix/store/hash-name          # View stored log
nix-store -q --references /nix/store/path  # Show dependencies
```

### Cache Issues
```bash
nix store gc                          # Garbage collect
nix store optimise                    # Deduplicate store
nix-collect-garbage -d               # Remove old generations
```

## Module Structure

### Creating a New Module
```nix
{ config, lib, pkgs, ... }:
{
  options.mymodule = {
    enable = lib.mkEnableOption "my module";

    setting = lib.mkOption {
      type = lib.types.str;
      default = "value";
      description = "Setting description";
    };
  };

  config = lib.mkIf config.mymodule.enable {
    # Implementation
    home.packages = [ pkgs.sometool ];
  };
}
```

### Module Location
- Cross-platform: `modules/common/`
- Linux-specific: `modules/linux/`
- macOS-specific: `modules/macos/`

## Best Practices

1. **Lock dependencies** - Commit `flake.lock`
2. **Use mkIf** - For conditional configuration
3. **Type options** - Use `lib.types.*` for validation
4. **Document options** - Add description to each option
5. **Platform check** - Use `stdenv.isLinux/isDarwin`

## Related Skills

- [ROS2 Development](../ros2-development/SKILL.md) - Using the environment
- [DevOps](../devops/SKILL.md) - CI/CD integration
