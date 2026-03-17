---
name: security-updates
description: Secure boot and firmware update workflows for Zephyr RTOS. Covers MCUboot integration, production image signing, DFU protocols (MCUmgr), fail-safe rollback mechanisms, and mbedTLS crypto basics. Trigger when implementing over-the-air (OTA) updates, securing the boot process, or managing cryptographic keys.
---

# Zephyr Security & Updates

Build production-ready, secure embedded systems using Zephyr's modular security stack and MCUboot bootloader.

## Core Workflows

### 1. MCUboot Integration
Set up the secure bootloader and define fail-safe flash partitions.
- **Reference**: **[mcuboot_integration.md](references/mcuboot_integration.md)**
- **Key Tools**: `CONFIG_BOOTLOADER_MCUBOOT`, `fixed-partitions`, Devicetree.

### 2. Image Signing
Ensure firmware integrity with production-grade digital signatures.
- **Reference**: **[image_signing.md](references/image_signing.md)**
- **Key Tools**: `imgtool.py`, ECDSA-P256, RSA.

### 3. DFU Protocols
Transport updates securely using MCUmgr or cloud-based OTA.
- **Reference**: **[dfu_protocols.md](references/dfu_protocols.md)**
- **Key Tools**: `mcumgr`, Golioth OTA, SMP transport.

### 4. Rollback Protection
Implement atomic swaps and image confirmation to prevent bricking devices.
- **Reference**: **[rollback_protection.md](references/rollback_protection.md)**
- **Key Tools**: `boot_write_img_confirmed()`, `mcumgr image test`.

### 5. Crypto Basics
Implement secure storage and cryptographic operations using mbedTLS.
- **Reference**: **[crypto_basics.md](references/crypto_basics.md)**
- **Key Tools**: `CONFIG_MBEDTLS`, TF-M, secure storage.

## Quick Start (Kconfig for Secure Boot)
```kconfig
# Enable MCUboot support in application
CONFIG_BOOTLOADER_MCUBOOT=y
```
```bash
# Build with MCUboot using Sysbuild
west build -b nucleo_f401re --sysbuild samples/basic/blinky
```

## Professional Patterns (Security-First)
- **Production Keys**: Never use default MCUboot keys. Provision unique keys during manufacturing.
- **Heartbeat Confirmation**: Only confirm a new image after the application has successfully connected to its cloud backend.
- **Version Integrity**: Enable version monotonicity to prevent accidental or malicious firmware downgrades.

## Resources

- **[References](references/)**:
  - `mcuboot_integration.md`: Partition layouts and setup.
  - `image_signing.md`: Key management and `imgtool` usage.
  - `dfu_protocols.md`: MCUmgr commands and cloud OTA.
  - `rollback_protection.md`: Swap mechanisms and confirmation code.
  - `crypto_basics.md`: mbedTLS and secure storage.
