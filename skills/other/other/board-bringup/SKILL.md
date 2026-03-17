---
name: board-bringup
description: Custom board bringup for Zephyr RTOS using Hardware Model v2 (HWMv2). Covers directory structure, board.yml metadata, core configuration files (Kconfig, defconfig, CMake), and revision management. Trigger when creating new board definitions or porting Zephyr to custom hardware.
---

# Zephyr Board Bringup (HWMv2)

Bring your custom hardware into the Zephyr ecosystem using modern Hardware Model v2 standards.

## Core Workflows

### 1. Planning the Structure
Organize your board files by vendor and board name.
- **Reference**: **[hwmv2_structure.md](references/hwmv2_structure.md)**
- **Key Tools**: `board.yml`, naming conventions.

### 2. Defining Configuration
Implement the essential Kconfig and CMake logic.
- **Reference**: **[board_files.md](references/board_files.md)**
- **Key Tools**: `Kconfig.board`, `_defconfig`, `CMakeLists.txt`.

### 3. Managing Revisions & Variants
Handle hardware iterations and SoC variants cleanly.
- **Reference**: **[hwmv2_structure.md](references/hwmv2_structure.md#revision-management)**
- **Key Tools**: Multi-revision `board.yml`, revision-specific overlays.

## Best Practices
- **Use `_common.dtsi`**: Share devicetree definitions across all board revisions.
- **Follow HWMv2**: Avoid the legacy board structure (`Kconfig.defconfig`, etc.).
- **Keep it minimal**: Only define what is unique to the board; let the SoC files handle chip-level configuration.

## Resources

- **[References](references/)**:
  - `hwmv2_structure.md`: Directory layout and `board.yml`.
  - `board_files.md`: Kconfig, defconfig, and CMake configuration.
