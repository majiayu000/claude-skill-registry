---
name: dotfiles-expert
description: "Expert guidance for peterstorm's NixOS dotfiles repository using flake-parts architecture. Use this skill when working with: NixOS system configuration, home-manager user configurations, flake-parts modular architecture, role-based configuration patterns (host.mkHost, user.mkHMUser), SOPS secrets management with Age encryption and template-based API, Terraform infrastructure for Kubernetes, ArgoCD GitOps patterns, k3s homelab setup, xmonad window manager configuration, neovim Lua configuration, or any task involving this dotfiles repository structure. Triggers on questions about adding hosts, users, roles, secrets, understanding the architecture, or debugging NixOS/home-manager builds."
---

# Dotfiles Expert Skill

Expert guidance for peterstorm's NixOS dotfiles repository with flake-parts architecture.

## Repository Architecture

### Core Pattern: Role-Based Modular Configuration
```
flake.nix                 # Main flake with inputs and outputs via flake-parts
├── lib/                  # Utility functions
│   ├── host.nix          # host.mkHost - creates NixOS configurations
│   ├── user.nix          # user.mkHMUser - creates home-manager configs
│   ├── sops.nix          # SOPS template-based secrets API
│   └── default.nix       # Exports: host, user, shell, sops
├── roles/                # NixOS system roles
│   ├── core/             # Essential system config, nix settings, sops
│   ├── efi/              # EFI bootloader
│   ├── wifi/             # Network manager
│   ├── desktop-plasma/   # KDE + xmonad
│   └── ...
├── roles/home-manager/   # User roles
│   ├── core-apps/        # Essential user packages
│   ├── window-manager/   # xmonad config
│   └── ...
├── machines/             # Hardware-specific configs
├── secrets/              # SOPS-encrypted secrets
│   ├── common/           # Shared secrets
│   ├── hosts/{hostname}/ # Host-specific secrets
│   └── users/{username}/ # User-specific secrets
└── k8s/                  # Kubernetes infrastructure
    ├── argocd/           # GitOps app definitions
    └── terraform/        # Infrastructure as code
```

### Configuration Flow
1. `flake.nix` defines hosts via `host.mkHost` and users via `user.mkHMUser`
2. Each takes a `roles` list that maps to directories in `roles/` or `roles/home-manager/`
3. Roles are composed together to build complete configurations
4. `util` object (containing sops helpers) is passed to all roles via `extraSpecialArgs`

## Quick Reference

### Commands
```bash
# NixOS rebuild
sudo nixos-rebuild switch --flake .#HOSTNAME
./system-apply.sh

# Home Manager
nix build .#homeManagerConfigurations.$USER.activationPackage && result/activate
./hm-apply.sh

# Testing (ALWAYS git add new files first!)
nix build .#nixosConfigurations.HOSTNAME.config.system.build.toplevel --dry-run --show-trace
nix build .#homeManagerConfigurations.USERNAME.activationPackage --dry-run --show-trace
nix flake check

# Evaluate specific config
nix eval .#nixosConfigurations.HOSTNAME.config.sops.templates --apply 'builtins.attrNames'
```

### Current Configurations
- **Hosts**: laptop-xps, laptop-work, desktop, homelab
- **Users**: peterstorm, hansen142, homelab
- **Architectures**: x86_64-linux, aarch64-darwin

## Adding New Configurations

### New Host
```nix
# In flake.nix, add to legacyPackages.nixosConfigurations:
new-host = host.mkHost {
  name = "new-host";
  roles = [ "core" "wifi" "efi" "desktop-plasma" ];  # Compose roles
  machine = [ "new-host" ];  # References machines/new-host/default.nix
  NICs = [ "wlp0s20f3" ];
  kernelPackage = pkgs.linuxPackages_latest;
  initrdAvailableMods = [ "xhci_pci" "nvme" ];
  initrdMods = [];
  kernelMods = [];
  kernelPatches = [];
  kernelParams = [];
  users = [{
    name = "username";
    groups = [ "wheel" "networkmanager" "docker" ];
    uid = 1000;
    ssh_keys = [];
  }];
  cpuCores = 8;
};
```

Then create `machines/new-host/default.nix`:
```nix
{ pkgs, lib, config, ...}:
{
  fileSystems."/" = {
    device = "/dev/disk/by-uuid/YOUR-UUID";
    fsType = "ext4";
  };
  fileSystems."/boot" = {
    device = "/dev/disk/by-uuid/YOUR-BOOT-UUID";
    fsType = "vfat";
  };
  hardware.cpu.intel.updateMicrocode = true;
}
```

### New User
```nix
# In flake.nix, add to legacyPackages.homeManagerConfigurations:
newuser = user.mkHMUser {
  roles = [ "core-apps" "window-manager/xmonad" ];  # Compose roles
  username = "newuser";
};
```

### New Role
```nix
# roles/my-new-role/default.nix (NixOS role)
{ config, pkgs, lib, util, ... }:
{
  # util.sops is available for secrets
  environment.systemPackages = [ pkgs.some-package ];
}

# roles/home-manager/my-role/default.nix (home-manager role)
{ config, pkgs, lib, util, ... }:
{
  home.packages = [ pkgs.some-package ];
}
```

Roles support path nesting: `"core-apps/neovim"` → `roles/home-manager/core-apps/neovim/default.nix`

## SOPS Secrets Management

### Template-Based API (Recommended)
Templates prevent secrets from entering the Nix store:

```nix
{ lib, config, pkgs, util, ... }:

(util.sops.mkSecretsAndTemplatesConfig
  # 1. Define secrets (references to encrypted values)
  [
    (util.sops.userSecret "github-token" "personal-github.yaml" "token")
    (util.sops.hostSecret "api-key" "service.yaml" "api_key" { owner = "root"; })
    (util.sops.commonSecret "shared-secret" "common.yaml" "key")
  ]
  
  # 2. Define templates (rendered files with actual values)
  [
    (util.sops.envTemplate "app-env" {
      GITHUB_TOKEN = "github-token";
      API_KEY = "api-key";
    })
    
    (util.sops.configTemplate "app-config" ''
      token = ${config.sops.placeholder."github-token"}
    '')
  ]
  
  # 3. Regular configuration
  {
    systemd.services.myservice = {
      serviceConfig.EnvironmentFile = config.sops.templates."app-env".path;
    };
  }
) { inherit config lib; }
```

### Secret Path Resolution
- `userSecret`: `secrets/users/{current-user}/filename.yaml`
- `hostSecret`: `secrets/hosts/{current-host}/filename.yaml`
- `commonSecret`: `secrets/common/filename.yaml`

### Template Locations
- **NixOS**: `/run/secrets/rendered/{template-name}`
- **Home Manager (Linux)**: `~/.config/sops-nix/secrets/rendered/{template-name}`
- **Home Manager (Darwin)**: `~/.config/sops-nix/secrets/rendered/{template-name}`

### Age Key Locations
- **NixOS/Linux**: `/var/lib/sops-nix/keys.txt`
- **Darwin**: `~/Library/Application Support/sops/age/keys.txt`

### Encrypting Secrets
```bash
# Encrypt new file
sops -e -i secrets/users/username/secret.yaml

# Edit existing
sops secrets/hosts/hostname/secret.yaml

# Update keys after adding recipient to .sops.yaml
sops updatekeys secrets/path/file.yaml
```

## Reference Files

For detailed information on specific domains:

- **[references/nix-patterns.md](references/nix-patterns.md)**: Nix language patterns, flake-parts, overlay creation, debugging
- **[references/kubernetes.md](references/kubernetes.md)**: ArgoCD patterns, Helm values, external-secrets, k3s setup
- **[references/xmonad-config.md](references/xmonad-config.md)**: XMonad keybindings, layouts, scratchpads, xmobar
- **[references/neovim-config.md](references/neovim-config.md)**: Neovim Lua config, lazy.nvim plugins, LSP setup

## Troubleshooting

### Common Issues

**Build fails with "file not found"**
```bash
git add .  # Nix flakes only see git-tracked files
```

**SOPS decryption fails**
```bash
# Check key location and presence
ls -la /var/lib/sops-nix/keys.txt  # Linux
ls -la "$HOME/Library/Application Support/sops/age/keys.txt"  # Darwin

# Verify public key in .sops.yaml
age-keygen -y /path/to/keys.txt

# Re-encrypt with correct keys
sops updatekeys secrets/path/file.yaml
```

**Templates show placeholders at runtime**
```bash
# Restart sops-nix service (Darwin)
launchctl kickstart gui/$(id -u)/org.nix-community.home.sops-nix

# Verify templates rendered
ls -la ~/.config/sops-nix/secrets/rendered/
```

**Nix evaluation errors**
```bash
# Always use --show-trace for debugging
nix build .#nixosConfigurations.HOSTNAME.config.system.build.toplevel --dry-run --show-trace 2>&1 | less

# Test template evaluation without full build
nix eval .#nixosConfigurations.HOSTNAME.config.sops.templates.template-name.content
```

## Code Style

### Nix
- Use `{ config, pkgs, lib, util, ... }:` function arguments
- Prefer `with lib;` only when using many lib functions
- Use `mkIf`, `mkMerge`, `optionalAttrs` for conditional config
- Follow existing role patterns in the repository

### Roles Pattern
- Each role is self-contained in its directory
- Use `imports = [ ... ];` to compose sub-roles
- Put role-specific files (configs, scripts) alongside `default.nix`
- Access SOPS via `util.sops` helpers passed through `extraSpecialArgs`
