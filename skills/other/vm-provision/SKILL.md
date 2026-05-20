---
name: vm-provision
description: Provision and integrate new VMs into the NixOS Proxmox fleet
---

# VM Provisioning Skill

This skill guides you through creating and integrating new VMs into the NixOS homelab fleet on Proxmox.

## Overview

The VM automation system uses:
- **Template 9002**: Ubuntu cloud image with UEFI for initial bootstrap
- **nixos-anywhere**: Two-phase deployment (kexec → disko+install)
- **Cloud-init**: SSH key injection for initial access
- **Disko**: Declarative disk partitioning

## Workflow

### Step 1: Define the VM

Add entry to `vms/definitions.nix` under `managed`:

```nix
managed = {
  my-vm = {
    vmid = 111;           # Unique, check vmidRanges (100-199 for production)
    cores = 4;
    memory = 8192;        # MB
    disk = "32G";
    storage = "nvmeprom";
    nixosConfig = "my-vm"; # Must match hosts/{name}
    purpose = "Description of VM purpose";
    services = ["service1" "service2"];
  };
};
```

### Step 2: Create Host Configuration

Create `hosts/{name}/` with four files:

**configuration.nix**:
```nix
{pkgs, inputs, ...}: {
  imports = [
    inputs.disko.nixosModules.disko
    ./disko.nix
    ./hardware-configuration.nix
  ];

  boot = {
    loader.systemd-boot.enable = true;
    loader.efi.canTouchEfiVariables = true;
  };

  homelab = {
    ssh = {
      enable = true;
      secure = false;  # or true for password auth disabled
    };
    tailscale.enable = true;
    nixCaches = {
      enable = true;
      profile = "internal";
    };
  };

  services.qemuGuest.enable = true;

  system.stateVersion = "25.05";
}
```

**disko.nix** (standard for all VMs):
```nix
{
  disko.devices = {
    disk = {
      main = {
        type = "disk";
        device = "/dev/sda";
        content = {
          type = "gpt";
          partitions = {
            ESP = {
              size = "512M";
              type = "EF00";
              content = {
                type = "filesystem";
                format = "vfat";
                mountpoint = "/boot";
                mountOptions = ["umask=0077"];
              };
            };
            root = {
              size = "100%";
              content = {
                type = "filesystem";
                format = "ext4";
                mountpoint = "/";
              };
            };
          };
        };
      };
    };
  };
}
```

**hardware-configuration.nix**:
```nix
{config, lib, modulesPath, ...}: {
  imports = [(modulesPath + "/profiles/qemu-guest.nix")];

  boot.initrd.availableKernelModules = ["ata_piix" "uhci_hcd" "virtio_pci" "virtio_scsi" "sd_mod" "sr_mod"];
  boot.initrd.kernelModules = [];
  boot.kernelModules = [];
  boot.extraModulePackages = [];

  # Filesystem definitions handled by disko.nix
  swapDevices = [];
  nixpkgs.hostPlatform = lib.mkDefault "x86_64-linux";
}
```

**home.nix**:
```nix
{...}: {
  imports = [
    ../../home/home.nix
    ../../home/utils/common.nix
  ];
}
```

### Step 3: Add to hosts.nix

Add placeholder entry to `hosts.nix`:

```nix
my-vm = {
  configurationFile = ./hosts/my-vm/configuration.nix;
  homeFile = ./hosts/my-vm/home.nix;
  user = "abl030";
  homeDirectory = "/home/abl030";
  hostname = "my-vm";
  sshAlias = "my-vm";
  sshKeyName = "ssh_key_abl030";
  publicKey = "ssh-ed25519 PLACEHOLDER_KEY_WILL_BE_ADDED_DURING_PROVISIONING";
  authorizedKeys = masterKeys;
};
```

### Step 4: Provision

```bash
nix run .#provision-vm my-vm
```

This will:
1. Clone template 9002
2. Configure resources (CPU, RAM, disk)
3. Inject SSH keys via cloud-init
4. Install NixOS via nixos-anywhere (two-phase)
5. Reboot and verify SSH access

### Step 5: Post-Provision (Fleet Integration)

After provisioning completes, note the IP address and run:

```bash
nix run .#post-provision-vm my-vm <IP> <VMID>
```

This will:
1. Extract SSH host key from VM
2. Update hosts.nix with real public key
3. Convert SSH key to age key
4. Update secrets/.sops.yaml with age key
5. Re-encrypt all secrets with new key
6. Commit changes to git

### Step 6: Deploy with Secrets

```bash
nixos-rebuild switch --flake .#my-vm --target-host my-vm
```

## Key Files

| File | Purpose |
|------|---------|
| `vms/definitions.nix` | VM specs (source of truth) |
| `vms/provision.sh` | Main provisioning script |
| `vms/post-provision.sh` | Fleet integration |
| `vms/proxmox-ops.sh` | Proxmox SSH wrapper |
| `hosts.nix` | Host definitions with SSH keys |
| `secrets/.sops.yaml` | Age keys for secrets |

## Safety Notes

- **Imported VMs** (in `vms/definitions.nix` under `imported`) have `readonly = true` - automation will refuse to touch them
- **VMID conflicts** are checked before provisioning
- **Confirmation prompt** required before creating VM
- SSH access is via `abl030` user, not root

## Troubleshooting

- **IP changes during provisioning**: Normal - the script handles this automatically via MAC/ARP lookup
- **SSH host key verification fails**: Run `ssh-keygen -R <ip>` to clear old key
- **sops updatekeys fails**: Ensure you're using `--config secrets/.sops.yaml`
