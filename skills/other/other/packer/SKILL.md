---
name: packer
description: HashiCorp Packer image building. Use for machine images.
---

# Packer

Packer automates the creation of Machine Images (AMI, VMDK, ISO) for multiple platforms from a single configuration. In 2025, **HCL2** is the standard for configuration.

## When to Use

- **Immutable Infrastructure**: Bake your app code into the OS image. Booting a pre-baked AMI is faster than running Ansible on boot.
- **Golden Images**: Create hardened, secure base images for your organization.
- **Multi-Cloud**: Build an AMI for AWS and a VHD for Azure from the same script.

## Quick Start (HCL2)

```hcl
source "amazon-ebs" "ubuntu" {
  ami_name      = "my-app-{{timestamp}}"
  instance_type = "t3.micro"
  region        = "us-west-2"
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/*ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"] # Canonical
  }
  ssh_username = "ubuntu"
}

build {
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    inline = ["sudo apt-get update", "sudo apt-get install -y nginx"]
  }
}
```

## Core Concepts

### Builders

Cloud-specific components (e.g., `amazon-ebs`, `azure-arm`) that launch a VM.

### Provisioners

Tools to configure the VM (Shell, Ansible, Chef) before it is turned into an image.

### Post-Processors

What to do with the image (Upload to S3, Vagrant Box, Docker Push).

## Best Practices (2025)

**Do**:

- **Use HCL2**: JSON templates are legacy. HCL2 supports variables and logic.
- **CI Integration**: Run Packer in CI pipeline to produce new AMIs on every release.
- **Cleanup**: Ensure Packer cleans up temporary resources (Security Groups, Key Pairs) after build.

**Don't**:

- **Don't bake secrets**: Never put passwords in the image. Use Cloud-init or User Data to inject them at runtime.

## References

- [Packer Documentation](https://developer.hashicorp.com/packer)
