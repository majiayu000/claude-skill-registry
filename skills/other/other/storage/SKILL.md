---
name: storage
description: Storage management for Zephyr RTOS. Covers Non-Volatile Storage (NVS) for persistent settings, flash partition management in Devicetree, and runtime flash layout access. Trigger when implementing persistent data storage, managing flash wear leveling, or configuring device partitions.
---

# Zephyr Storage

Implement reliable persistent data handling using Zephyr's storage subsystem and flash management utilities.

## Core Workflows

### 1. NVS Storage
Utilize Non-Volatile Storage (NVS) for efficient, wear-leveled data persistence.
- **Reference**: **[nvs_storage.md](references/nvs_storage.md)**
- **Key Tools**: `nvs_mount()`, `nvs_read()`, `nvs_write()`.

### 2. Flash Management
Configure and manage flash partitions and hardware page layouts.
- **Reference**: **[flash_management.md](references/flash_management.md)**
- **Key Tools**: `fixed-partitions`, `FLASH_MAP`, `flash_get_page_info_by_offs()`.

## Quick Start (NVS Write)
```c
#include <zephyr/storage/nvs/nvs.h>

void save_data(struct nvs_fs *fs, uint16_t id, void *data, size_t len) {
    nvs_write(fs, id, data, len);
}
```

## Professional Patterns (Reliability)
- **Settings Integration**: Use NVS as the backend for the `settings` subsystem for a standard key-value configuration experience.
- **Collision Prevention**: Define NVS Entry IDs in a centralized header file to prevent accidental overwrites across modules.
- **Runtime Layout Checks**: Always query the flash controller for page sizes (`flash_get_page_layout`) rather than assuming hardcoded sector sizes.

## Automation Tools
- **[nvs_id_lint.py](scripts/nvs_id_lint.py)**: Detect duplicate `NVS_ID_*` macro values across source/header files.

## Examples & Templates
- **[partition_overlay_template.overlay](assets/partition_overlay_template.overlay)**: Starter fixed-partitions overlay for app + storage.

## Validation Checklist
- [ ] `nvs_mount()` succeeds on boot for the configured storage partition.
- [ ] Written values survive reset and read back with matching length and content.
- [ ] Partition layout in DTS matches runtime flash-map queries.
- [ ] Repeated write cycles do not produce mount/read corruption errors.

## Resources

- **[References](references/)**:
  - `nvs_storage.md`: Using NVS for data blobs and integers.
  - `flash_management.md`: Devicetree partitions and page information.
- **[Scripts](scripts/)**:
  - `nvs_id_lint.py`: Duplicate ID detector for NVS namespaces.
- **[Assets](assets/)**:
  - `partition_overlay_template.overlay`: Flash partitioning template.
