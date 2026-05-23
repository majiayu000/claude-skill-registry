---
name: esp-idf-setup
description: Set up ESP-IDF development environment, create new projects, and configure build systems
---

# ESP-IDF Project Setup Guide

## When to Use This Skill

Apply this skill when the user:
- Wants to set up ESP-IDF for the first time
- Needs to create a new ESP32 project
- Wants to configure CMakeLists.txt or component dependencies
- Needs help with sdkconfig or menuconfig
- Wants to add a project to the monorepo

## ESP-IDF Installation

### Automated Installation

Use the Makefile targets:
```bash
# Install ESP-IDF v5.3.2
make setup-idf

# Custom version
make setup-idf IDF_VERSION=v5.4

# Full environment setup
make setup-all
```

### Shell Configuration

After installation, add alias to shell profile (~/.bashrc or ~/.zshrc):
```bash
alias get_idf='. $HOME/repos/esp-idf/export.sh'
```

Important: Do NOT add `export.sh` directly to profile - use an alias instead.

## Creating New Projects

### Minimal Project Structure

```
new-project/
├── CMakeLists.txt
├── main/
│   ├── CMakeLists.txt
│   └── main.c
└── sdkconfig.defaults
```

### Root CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.16)

# For monorepo: use shared components
set(EXTRA_COMPONENT_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/../../shared-libs")

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(new-project)
```

### Main Component CMakeLists.txt

```cmake
idf_component_register(
    SRCS "main.c"
    INCLUDE_DIRS "."
    REQUIRES driver nvs_flash esp_wifi
)
```

### sdkconfig.defaults

```ini
# Target chip
CONFIG_IDF_TARGET="esp32"

# Flash size
CONFIG_ESPTOOLPY_FLASHSIZE_4MB=y

# Partition table
CONFIG_PARTITION_TABLE_SINGLE_APP=y

# Log level
CONFIG_LOG_DEFAULT_LEVEL_INFO=y
```

## Adding to the Monorepo

### Directory Location

Place new ESP32 projects in:
```
packages/esp32-projects/new-project-name/
```

### Create Makefile Target

Add to root Makefile:
```makefile
# New project variables
NEW_PROJECT_DIR = $(ESP32_PACKAGES_DIR)/new-project-name

# Build target
new-project-build: check-idf
	@echo "$(BLUE)Building new-project...$(NC)"
	@cd $(NEW_PROJECT_DIR) && $(IDF_ENV_CMD) && idf.py build

# Flash target
new-project-flash: check-idf
	@echo "$(BLUE)Flashing new-project...$(NC)"
	@cd $(NEW_PROJECT_DIR) && $(IDF_ENV_CMD) && idf.py flash -p $(PORT)

# Add to .PHONY
.PHONY: new-project-build new-project-flash
```

## Component Management

### Using IDF Component Manager

Create `idf_component.yml` in component directory:
```yaml
dependencies:
  # From ESP Component Registry
  espressif/led_strip: "^2.0.0"

  # From GitHub
  my_component:
    git: https://github.com/user/component.git
    version: "v1.0.0"
```

### Local Components

Place in project's `components/` directory:
```
project/
├── components/
│   └── my_component/
│       ├── CMakeLists.txt
│       ├── include/
│       │   └── my_component.h
│       └── my_component.c
└── main/
```

## Common Configuration Tasks

### Setting Target Chip

```bash
# Set target (creates fresh sdkconfig)
idf.py set-target esp32s3

# Or via Makefile
make robocar-set-target TARGET=esp32s3
```

### Menuconfig Options

```bash
idf.py menuconfig
```

Common sections:
- Serial flasher config (port, baud rate)
- Partition table
- Component config (WiFi, Bluetooth, etc.)
- FreeRTOS (tick rate, stack sizes)

### Flash Size Configuration

In sdkconfig.defaults:
```ini
# 4MB flash
CONFIG_ESPTOOLPY_FLASHSIZE_4MB=y

# 16MB flash (for ESP32-S3)
CONFIG_ESPTOOLPY_FLASHSIZE_16MB=y
```

## Best Practices

1. **Use sdkconfig.defaults** - Don't commit sdkconfig, use defaults
2. **Pin ESP-IDF version** - Document which version the project requires
3. **Minimal dependencies** - Only include REQUIRES you actually use
4. **Target-specific configs** - Use `sdkconfig.defaults.esp32s3` for variants
5. **Document GPIO usage** - Create a pinout table in README
