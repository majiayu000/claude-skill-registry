---
name: build-system
description: Build system management for Zephyr RTOS. Covers West workspace initialization, manifest management, Sysbuild multi-image builds, Kconfig symbols, and CMake integration. Trigger when setting up workspaces, configuring builds, or troubleshooting build-time errors.
---

# Zephyr Build System

Efficiently manage the complex build and configuration stack of Zephyr RTOS.

## Core Workflows

### 1. West Workspace & Manifests
Manage multi-repo projects and dependency allow-lists.
- **Reference**: **[west.md](references/west.md)**
- **Key Tools**: `west init`, `west update`, `west manifest --resolve`, `name-allowlist`.

### 2. Kconfig Configuration
Tune software features and hardware parameters.
- **Reference**: **[kconfig.md](references/kconfig.md)**
- **Key Tools**: `west build -t menuconfig`, symbol searching (`/`), help (`?`).

### 3. Sysbuild & Multi-Image
Configure complex projects like MCUboot + Application.
- **Reference**: **[cmake.md](references/cmake.md)**
- **Key Tools**: `west build --sysbuild`, `sysbuild.conf`.

### 4. CMake & Project Structure
Core build logic for applications and modules.
- **Reference**: **[cmake.md](references/cmake.md)**
- **Key Tools**: `CMakeLists.txt`, `zephyr_library()`, `target_sources()`.

## Automation Tools

- **[find_modules.sh](scripts/find_modules.sh)**: Scan your `build/` directory to automatically identify which modules you should add to your manifest's `name-allowlist`.

## Resources

- **[References](references/)**:
  - `west.md`: West commands, manifests, and allow-lists.
  - `kconfig.md`: Project configuration and menuconfig usage.
  - `cmake.md`: Sysbuild and CMake API integration.
- **[Scripts](scripts/)**:
  - `find_modules.sh`: Automated allow-list discovery utility.
