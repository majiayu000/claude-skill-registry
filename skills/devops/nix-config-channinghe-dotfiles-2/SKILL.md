---
name: nix-config
description: This skill provides comprehensive guidance for working with the nix-config framework - a platform-agnostic modular configuration system for NixOS and Darwin (macOS). Use this skill when adding new modules, hosts, users, or services; when troubleshooting configuration issues; or when modifying any aspect of the nix-config/nix-secrets ecosystem.
---

# Nix-Config Framework

## Overview

This skill provides comprehensive knowledge of the nix-config framework - a platform-agnostic modular configuration system that supports both NixOS and Darwin (macOS) through a unified architecture. The framework separates public configuration logic (`nix-config`) from private sensitive data (`nix-secrets`) using a three-file pattern for platform-agnostic design.

## Core Architecture

### Three-File Pattern

Each module uses three files to separate platform-specific logic:

- `default.nix` - Platform-agnostic common logic
- `nixos.nix` - Linux-specific (systemd, NetworkManager)
- `darwin.nix` - macOS-specific (launchd, Homebrew paths)

**Priority System**: `lib.mkDefault` (low) → normal → `lib.mkForce` (high)

### Configuration Inheritance Hierarchy

```
Layer 1: hosts/common/core/           - Core system configuration
Layer 2: hosts/common/optional/        - Optional services
Layer 3: hosts/common/users/           - User configurations
Layer 4: hosts/nixos/${hostname}/      - Host-specific config
```

### Separation of Concerns

| Location | Type | Content |
|----------|------|---------|
| `nix-config/` | Public | Module logic, configuration structure |
| `nix-secrets/` | Private | Sensitive data (IPs, passwords, keys) |

## Quick Task Guide

### Adding a New NixOS Host

To add a new NixOS host:

1. Create host directory: `hosts/nixos/${hostname}/`
2. Copy or generate `hardware-configuration.nix`:
   - From existing host: `cp hosts/nixos/ExistingHost/hardware-configuration.nix hosts/nixos/NewHost/`
   - From target machine: Run `sudo nixos-generate-config --root /mnt` on the host
3. Create `default.nix` with host-specific imports and settings
4. Add host entry to `nix-secrets/nix/network.nix` (network info)
5. Create encrypted secrets file: `nix-secrets/secrets/${hostname}.yaml`
6. Test build: `./scripts/rebuild.sh NewHost build`

### Adding a New Darwin Host

To add a new Darwin (macOS) host:

1. Create host directory: `hosts/darwin/${hostname}/`
2. Create `default.nix` with host-specific imports
3. **Critical**: Set `hostSpec.isDarwin = true`
4. Add host entry to `nix-secrets/nix/network.nix`
5. Create encrypted secrets file: `nix-secrets/secrets/${hostname}.yaml`
6. Test build: `./scripts/rebuild.sh NewMac build`

### Adding a New User

To add a new user:

1. Create user directories:
   - `hosts/common/users/${username}/`
   - `home/${username}/common/{core,dotfiles,optional}/`
2. Create platform-agnostic config: `hosts/common/users/${username}/default.nix`
3. Create platform-specific configs: `nixos.nix` and `darwin.nix`
4. Add SSH public keys to: `hosts/common/users/${username}/keys/`
5. Create Home Manager config: `home/${username}/common/core/default.nix`
6. Update `hosts/common/core/default.nix` to import the new user

### Adding a New Service Module

To create a reusable service module:

1. Determine module type:
   - **Optional service**: Place in `hosts/common/optional/services/`
   - **Reusable module**: Place in `modules/hosts/common/`, `modules/hosts/nixos/`, or `modules/hosts/darwin/`
2. Create module file with options and config
3. Reference in host config via imports or hostSpec flags

## Common Patterns

### lib.custom Functions

```nix
# Relative path from project root
lib.custom.relativeToRoot "modules/common"

# Scan directory for .nix files
lib.custom.scanPaths ./optional
```

### Import Patterns

```nix
# Flatten nested imports
imports = lib.flatten [
  ./hardware-configuration.nix
  (map lib.custom.relativeToRoot [
    "hosts/common/core"
    "hosts/common/optional/services/docker.nix"
  ])
];

# Conditional imports
imports = lib.optionals (!isDarwin) [
  (lib.custom.relativeToRoot "hosts/common/core/openssh-server.nix")
];
```

### Platform Detection

```nix
# Method 1: hostSpec
lib.mkIf (!config.hostSpec.isDarwin) { ... }

# Method 2: pkgs.stdenv
lib.optionalAttrs pkgs.stdenv.isLinux { ... }

# Method 3: File-level separation
hosts/common/users/${username}/default.nix   # Always imported
hosts/common/users/${username}/nixos.nix     # Only NixOS
hosts/common/users/${username}/darwin.nix    # Only Darwin
```

## Key Files and Locations

### Critical Files

| File | Purpose |
|------|---------|
| `flake.nix` | Root configuration, defines inputs and outputs |
| `modules/common/host-spec.nix` | Host specification module (username, network info, flags) |
| `hosts/common/core/default.nix` | Core system config, imports HM and SOPS |
| `scripts/rebuild.sh` | Cross-platform rebuild script |

### nix-secrets Structure

```
nix-secrets/
├── nix/                       # Nix-exposed configuration
│   ├── network.nix             # Network config per host (no sensitive data)
│   ├── network-storage.nix       # NFS/Samba configurations
│   └── services.nix            # Service-specific secrets
└── secrets/                    # SOPS encrypted files
    └── ${hostname}.yaml         # Host-specific encrypted secrets
```

## Common Pitfalls and Solutions

| Issue | Solution |
|-------|----------|
| Option conflicts | Use `lib.mkDefault` in base config |
| Missing `group` on Darwin | Use `lib.optionalAttrs pkgs.stdenv.isLinux { group = "wheel"; }` |
| Wrong `stateVersion` type | NixOS = string, Darwin = integer |
| Auto-optimise-store on Darwin | Use `nix.optimise.automatic` instead |
| SOPS SSH key paths differ | Conditional `sshKeyPaths` in sops.nix |
| Secrets not decrypting | Check AGE key recipients and SSH agent |

## Essential Commands

### System Rebuild

```bash
# On NixOS
sudo nixos-rebuild switch --flake .#hostname

# On Darwin
sudo darwin-rebuild switch --flake .#hostname

# Cross-platform script
./scripts/rebuild.sh [hostname] [trace|build]

# Using nh (if installed)
nh os switch .
nh darwin switch .
```

### Secrets Management

```bash
# Edit secret
sops secrets/${hostname}.yaml

# Encrypt file
sops -e -i secrets.txt

# Decrypt file
sops -d -i secrets.txt

# Add new AGE key
sops keys add age1...

# Rotate keys
sops rotate -i secrets.yaml
```

### Development

```bash
# Enter dev shell
nix develop

# Format code
nix fmt

# Run checks
nix flake check

# Build ISO
nix build --impure .#nixosConfigurations.iso.config.system.build.isoImage
```

## Platform-Specific Notes

### NixOS
- Use `system.stateVersion = "25.05"` (string)
- Use `fileSystems.*` for mounting
- Use `systemd.services.*` for services
- Use `networking.networkd` or `NetworkManager`
- SSH keys go to `/etc/ssh/authorized_keys.d/`

### Darwin (macOS)
- Use `system.stateVersion = 6` (integer; 5 = nix-darwin 25.05)
- Use `launchd.agents.*` for services
- No NetworkManager (uses macOS networking)
- SSH keys managed differently
- Homebrew paths in config
- Touch ID integration available

## Additional Resources

For detailed documentation and references, consult the bundled resources in the `references/` directory:

- `architecture.md` - Detailed architecture and design patterns
- `directory-structure.md` - Complete directory structure reference
- `hostspec-reference.md` - hostSpec module options reference
- `module-creation.md` - Module creation patterns and examples
- `network-storage.md` - Network storage module documentation

These files provide in-depth information for complex operations and should be referenced when detailed guidance is needed beyond this quick guide.
