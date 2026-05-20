---
name: modern-c-makefile
description: Create, analyze, or improve Makefiles for modern C/C++ projects using best practices from the gnaro project template. Use when working with C/C++ projects that need clean, maintainable build systems for creating new Makefiles, improving existing ones, understanding modern patterns, or setting up comprehensive build workflows with testing and code quality tools.
---

# Modern C Makefile

## Overview

This skill provides guidance and templates for creating clean, maintainable Makefiles for modern C/C++ projects, based on the best practices demonstrated in the [gnaro project](https://github.com/lucavallin/gnaro). It helps structure build systems that integrate compilation, testing, linting, formatting, and dependency management in a clear and organized way.

## Core Concepts

Understand these key Makefile concepts before implementing:

- **Variables**: Centralize project settings like compiler flags, directories, and tool paths
- **Wildcards**: Use patterns like `*.c` and `**/*.c` to automatically find source files
- **Automatic Variables**: Leverage `$@` (target), `$<` (first dependency), `$*` (stem), `$(@D)` (target directory)
- **Phony Targets**: Declare `.PHONY` targets for actions like `clean`, `format`, `lint` that don't produce files
- **Conditionals**: Use `ifeq`/`else`/`endif` for debug/release builds or platform-specific configurations
- **Pattern Rules**: Create generic rules for compiling `.c` to `.o` files

## Makefile Template

The complete gnaro Makefile template is available in [references/gnaro_makefile.md](references/gnaro_makefile.md). Key sections include:

### Project Structure Variables
```makefile
debug ?= 0
NAME := your-project
SRC_DIR := src
BUILD_DIR := build
INCLUDE_DIR := include
LIB_DIR := lib
TESTS_DIR := tests
BIN_DIR := bin
```

### Automatic Object File Generation
```makefile
OBJS := $(patsubst %.c,%.o, $(wildcard $(SRC_DIR)/*.c) $(wildcard $(LIB_DIR)/**/*.c))
```

### Compiler and Tool Configuration
```makefile
CC := clang
LINTER := clang-tidy
FORMATTER := clang-format
CFLAGS := -std=gnu17 -D _GNU_SOURCE -D __STDC_WANT_LIB_EXT1__ -Wall -Wextra -pedantic
LDFLAGS := -lm
```

### Core Targets
- `$(NAME)`: Build executable with dependencies on format, lint, and object files
- `$(OBJS)`: Pattern rule for compiling object files with directory creation
- `test`: Compile and run CUnit tests
- `lint`: Run static analysis with clang-tidy
- `format`: Apply code formatting with clang-format
- `check`: Run valgrind memory checks
- `setup`: Install development dependencies (Debian/Ubuntu)
- `clean`: Remove build artifacts
- `bear`: Generate compile_commands.json for tooling

## Customization Guide

### Adapting to Your Project

1. **Basic Configuration**:
   - Update `NAME` to your project name
   - Adjust directory variables to match your project structure
   - Modify `CFLAGS` for your C standard and feature requirements

2. **Compiler and Tools**:
   - Change `CC`, `LINTER`, `FORMATTER` to match your installed versions
   - For GCC projects: `CC := gcc`
   - Adjust tool paths for non-Debian systems

3. **Cross-Platform Considerations**:
   - Replace apt-based `setup` target with appropriate package manager commands
   - Use conditionals for platform-specific configurations:
   ```makefile
   ifeq ($(OS),Windows_NT)
       # Windows-specific settings
   else ifeq ($(shell uname -s),Darwin)
       # macOS-specific settings  
   else
       # Linux-specific settings
   endif
   ```

4. **Adding Features**:
   - **Documentation**: Add `docs` target for Doxygen or other documentation generators
   - **Packaging**: Add `package` target for creating distributable archives
   - **Installation**: Add `install` and `uninstall` targets for system installation

### Common Modifications

**Multiple Executables**:
```makefile
EXECUTABLES := app1 app2
all: $(EXECUTABLES)

app1: $(APP1_OBJS)
	$(CC) $(CFLAGS) -o $(BIN_DIR)/$@ $^ $(LDFLAGS)

app2: $(APP2_OBJS)
	$(CC) $(CFLAGS) -o $(BIN_DIR)/$@ $^ $(LDFLAGS)
```

**Header Dependency Generation**:
```makefile
DEPFILES := $(OBJS:.o=.d)
-include $(DEPFILES)

%.d: %.c
	@$(CC) $(CFLAGS) -MM -MP -MT $*.o -MF $@ $<
```

**Verbose Mode**:
```makefile
V ?= 0
ifeq ($(V),1)
    Q :=
else
    Q := @
endif

$(OBJS): dir
	$(Q)mkdir -p $(BUILD_DIR)/$(@D)
	$(Q)$(CC) $(CFLAGS) -o $(BUILD_DIR)/$@ -c $*.c
```

## Usage Examples

### Example 1: Creating a New Makefile
```
User: Create a Makefile for my C project "calculator" with source files in src/, headers in include/, tests in tests/
Assistant: Creates Makefile based on template with customized variables
```

### Example 2: Adding Testing to Existing Makefile
```
User: Add CUnit testing support to my existing Makefile
Assistant: Adds test target and updates dependencies
```

### Example 3: Improving Build Performance
```
User: My Makefile rebuilds everything when headers change
Assistant: Adds automatic dependency generation with -MM flags
```

### Example 4: Cross-Platform Support
```
User: Make my Makefile work on both Linux and macOS
Assistant: Adds OS detection and conditional tool paths
```

## Quick Reference

### Essential Commands
```bash
make              # Build project (default target)
make debug=1      # Build with debug symbols, no optimization
make test         # Run tests
make lint         # Run static analysis
make format       # Format code
make check        # Run memory checks
make clean        # Clean build artifacts
```

### Project Structure Convention
```
project/
├── Makefile
├── src/          # Source files (*.c)
├── include/      # Header files (*.h)
├── lib/          # Third-party libraries
├── tests/        # Test files
├── build/        # Object files (generated)
└── bin/          # Executables (generated)
```

## Resources

This skill includes the following bundled resources:

### references/
Reference documentation for Makefile best practices and templates:

- **[gnaro_makefile.md](references/gnaro_makefile.md)**: Complete Makefile from the gnaro project with detailed analysis and adaptation notes. Use this as the primary reference template.
- **[best_practices.md](references/best_practices.md)**: Comprehensive guide to modern C Makefile design patterns, advanced techniques, and common solutions.

**When to load references:** Read these files when you need detailed analysis of Makefile patterns, adaptation guidance, or advanced techniques beyond what's covered in the main skill.

### assets/
Template files and guides for project setup:

- **[basic_makefile.template](assets/basic_makefile.template)**: Simplified Makefile template ready for customization. Replace `PROJECT_NAME` and adjust directories as needed.
- **[project_structure_example.md](assets/project_structure_example.md)**: Recommended project structure with variations for different project types (single-header libraries, applications with resources, multi-target projects).
- **[cross_platform_guide.md](assets/cross_platform_guide.md)**: Guide for adapting Makefiles to different operating systems (Linux, macOS, Windows) with platform detection, package manager integration, and cross-compilation support.

**When to use assets:** These files provide starting points and templates that can be copied and adapted for specific projects. They're particularly useful when creating new projects or porting existing ones to different platforms.

### scripts/
This skill doesn't include scripts since Makefile creation is primarily about configuration and structure rather than automated processing. However, consider creating custom scripts for:
- Project scaffolding (generating directory structure)
- Dependency management
- Build automation beyond Makefile capabilities
