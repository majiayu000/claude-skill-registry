---
name: packer
description: |
  HashiCorp Packer reference for building machine images and VM templates.
  Use when working with Packer configurations (.pkr.hcl files), running packer
  commands, troubleshooting builds, or designing image pipelines.
  Includes Proxmox builder patterns for homelab environments.
  Triggers: packer, pkr.hcl, image, template, ami, builder, provisioner, cloud-init.
agent: packer-expert
---

# Packer Skill

Reference for building machine images with HashiCorp Packer, focusing on VM template creation for homelab environments.

## Quick Reference

```bash
# Core workflow
packer init .               # Initialize, download plugins
packer validate .           # Syntax validation
packer fmt -recursive .     # Format HCL files
packer build .              # Build image(s)

# Debug
packer build -debug .                     # Step through build
PACKER_LOG=1 packer build . 2>debug.log   # Verbose logging

# Specific template
packer build ubuntu-22.04.pkr.hcl
```

## Core Workflow

```
init → fmt → validate → build
```

1. **init**: Download required plugins (builders, provisioners)
2. **fmt**: Format HCL files for consistency
3. **validate**: Check syntax and configuration validity
4. **build**: Execute the build process

## Reference Files

Load on-demand based on task:

| Topic | File | When to Load |
|-------|------|--------------|
| Troubleshooting | [troubleshooting.md](references/troubleshooting.md) | Build failures, SSH issues |
| Proxmox Builder | [proxmox/builder.md](references/proxmox/builder.md) | proxmox-iso builder config |
| Cloud-Init | [cloud-init.md](references/cloud-init.md) | Cloud-init template setup |
| Provisioners | [provisioners.md](references/provisioners.md) | Shell, Ansible, file provisioners |

## HCL2 Syntax

Packer uses HCL2 (same as Terraform). Key blocks:

```hcl
# Required plugins
packer {
  required_plugins {
    proxmox = {
      version = ">= 1.1.0"
      source  = "github.com/hashicorp/proxmox"
    }
  }
}

# Variables
variable "proxmox_api_url" {
  type        = string
  description = "Proxmox API URL"
}

# Local values
locals {
  timestamp = formatdate("YYYYMMDD-hhmm", timestamp())
}

# Builder source
source "proxmox-iso" "ubuntu" {
  # ... builder config
}

# Build definition
build {
  sources = ["source.proxmox-iso.ubuntu"]

  provisioner "shell" {
    scripts = ["scripts/setup.sh"]
  }
}
```

## Proxmox Builder Quick Start

```hcl
source "proxmox-iso" "ubuntu-22-04" {
  # Connection
  proxmox_url              = var.proxmox_api_url
  username                 = var.proxmox_api_token_id
  token                    = var.proxmox_api_token_secret
  insecure_skip_tls_verify = true
  node                     = "pve"

  # VM Settings
  vm_id                    = 9000
  vm_name                  = "ubuntu-22.04-template"
  template_description     = "Ubuntu 22.04 Template - ${local.timestamp}"

  # ISO
  iso_file                 = "local:iso/ubuntu-22.04.3-live-server-amd64.iso"
  iso_storage_pool         = "local"
  unmount_iso              = true

  # System
  qemu_agent              = true
  scsi_controller         = "virtio-scsi-single"

  # Disk
  disks {
    type         = "scsi"
    disk_size    = "20G"
    storage_pool = "local-lvm"
  }

  # Network
  network_adapters {
    model    = "virtio"
    bridge   = "vmbr0"
    firewall = false
  }

  # CPU/Memory
  cores   = 2
  memory  = 2048

  # Cloud-init
  cloud_init              = true
  cloud_init_storage_pool = "local-lvm"

  # SSH
  ssh_username = "ubuntu"
  ssh_password = "packer"
  ssh_timeout  = "20m"

  # Boot
  boot_command = [
    # Autoinstall boot command
  ]
  boot_wait = "5s"
}
```

## Validation Checklist

Before `packer build`:

- [ ] `packer init` completed successfully
- [ ] `packer fmt` applied
- [ ] `packer validate` passes
- [ ] ISO file accessible from Proxmox node
- [ ] API token has required permissions
- [ ] VM ID not in use
- [ ] Storage pools exist and have space
- [ ] Network bridge accessible
- [ ] Boot command tested (or cloud-init/autoinstall configured)
- [ ] SSH credentials match user-data

## Common Build Patterns

### Pattern 1: Ubuntu Autoinstall

Uses cloud-init autoinstall for unattended installation:

```hcl
http_directory = "http"  # Serves user-data, meta-data

boot_command = [
  "<esc><wait>",
  "e<wait>",
  "<down><down><down><end>",
  " autoinstall ds=nocloud-net\\;s=http://{{ .HTTPIP }}:{{ .HTTPPort }}/",
  "<f10>"
]
```

### Pattern 2: Multi-Stage Provisioning

```hcl
build {
  sources = ["source.proxmox-iso.ubuntu"]

  # Stage 1: System updates
  provisioner "shell" {
    inline = ["apt-get update && apt-get upgrade -y"]
  }

  # Stage 2: Ansible configuration
  provisioner "ansible" {
    playbook_file = "ansible/configure.yml"
  }

  # Stage 3: Cleanup
  provisioner "shell" {
    script = "scripts/cleanup.sh"
  }
}
```

### Pattern 3: Variables File

```hcl
# variables.pkrvars.hcl
proxmox_api_url          = "https://pve.local:8006/api2/json"
proxmox_api_token_id     = "packer@pam!packer"
proxmox_api_token_secret = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

```bash
packer build -var-file="variables.pkrvars.hcl" .
```

## Troubleshooting Quick Reference

| Issue | Check |
|-------|-------|
| SSH timeout | boot_wait, boot_command, firewall, cloud-init |
| Permission denied | API token permissions, user-data |
| ISO not found | iso_file path, storage pool permissions |
| Build hangs | boot_command timing, VNC console |
| Cloud-init fails | user-data syntax, meta-data presence |
