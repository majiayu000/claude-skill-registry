---
name: zephyr-module
description: Creating and integrating out-of-tree Zephyr modules. Covers module.yml configuration, Kconfig and CMake integration within a module, and West manifest inclusion. Trigger when developing reusable libraries, driver packages, or external software components for Zephyr.
---

# Zephyr Modules

Extend the Zephyr RTOS with reusable, out-of-tree modules that integrate seamlessly with the build system.

## Core Workflows

### 1. Defining a Module
Create the directory structure and metadata required for auto-discovery.
- **Reference**: **[module_definition.md](references/module_definition.md)**
- **Key Tools**: `zephyr/module.yml`, `zephyr/Kconfig`, `zephyr/CMakeLists.txt`.

### 2. West Manifest Integration
Adding your module to a workspace for distribution and versioning.
- **Reference**: **[west_integration.md](references/west_integration.md)**
- **Key Tools**: `west.yml`, `west update`, `west build -t list_modules`.

### 3. Library Wrapping (Glue Code)
Wrapping external C/C++ libraries as Zephyr modules.
- **Reference**: **[module_definition.md](references/module_definition.md#the-glue-pattern)**
- **Key Tools**: `zephyr_library()`, `zephyr_include_directories()`.

## Quick Start (module.yml)
```yaml
build:
  cmake: .
  kconfig: zephyr/Kconfig
```

## Validation Checklist
- [ ] `west update` fetches module source from manifest without conflicts.
- [ ] `west build -t list_modules` shows the module as discovered.
- [ ] Module Kconfig options appear and can be enabled in build configuration.
- [ ] Module sources are compiled and linked into the target application as expected.

## Automation Tools
- **[module_manifest_check.py](scripts/module_manifest_check.py)**: Validate required `build.cmake` and `build.kconfig` fields in `module.yml`.

## Examples & Templates
- **[module_yml_template.yml](assets/module_yml_template.yml)**: Starter module manifest for out-of-tree integration.

## Resources

- **[References](references/)**:
  - `module_definition.md`: Structure and module.yml specification.
  - `west_integration.md`: Manifest configuration and discovery tools.
- **[Scripts](scripts/)**:
  - `module_manifest_check.py`: Module manifest consistency checker.
- **[Assets](assets/)**:
  - `module_yml_template.yml`: Minimal `zephyr/module.yml` template.
