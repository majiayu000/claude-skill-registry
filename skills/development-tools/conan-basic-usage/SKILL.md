---
name: conan-basic-usage
description: Basic operations for the Conan C++ package manager. Use when the user explicitly asks to 'use conan' for tasks like creating projects, installing dependencies, or building packages, or asks for 'how to' guidance on Conan setup.
---

# Conan Basic Usage

## Overview

This skill provides guidance on using Conan, the C/C++ package manager. It covers project initialization, dependency management, and package creation.

## Quick Start

### 1. Initialize a Project

To create a standard project structure for a C++ library using CMake:

```bash
mkdir myproject && cd myproject
conan new cmake_lib -d name=myproject -d version=0.1
```

This generates:
- `conanfile.py`: The package recipe.
- `CMakeLists.txt`: The build script.
- `src/` & `include/`: Source and header files.
- `test_package/`: A consumer project to verify the package.

### 2. Install Dependencies

To install dependencies defined in `conanfile.py` and build missing binaries:

```bash
conan install . --build=missing
```

### 3. Create/Build Package

To build the package and export it to your local Conan cache:

```bash
conan create .
```

This runs the `build()` method in `conanfile.py`, creates the binary package, and runs the tests in `test_package/`.

## Common Tasks

### Managing Dependencies

- **Install**: Use `conan install .` to resolve and install dependencies. Add `--build=missing` to compile from source if binaries aren't available for your configuration.
- **Inspect**: Use `conan graph info .` to see the dependency tree.

### Remote Management

- **List Remotes**: `conan remote list`
- **Add Remote**: `conan remote add <remote_name> <url>`
- **Upload**: `conan upload <package_name> -r <remote_name>`

## Reference



- **Project Structure**: Best practices for directory layout. See [project-structure.md](references/project-structure.md).

- **Configuration**: Core settings, cache location, and profiles. See [configuration.md](references/configuration.md).

- **Runtime & Build Layout**: Build directory structure and how to find shared libraries. See [runtime-layout.md](references/runtime-layout.md).

- **Internal Files**: Understanding `conanmanifest.txt`, `conaninfo.txt`, etc. See [internal-files.md](references/internal-files.md).

- **Commands**: Comprehensive list of common commands. See [commands.md](references/commands.md).






