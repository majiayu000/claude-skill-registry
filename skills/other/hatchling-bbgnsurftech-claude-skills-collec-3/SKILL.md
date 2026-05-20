---
name: hatchling
description: This skill provides comprehensive documentation for Hatchling, the modern Python build backend that implements PEP 517/518/621/660 standards. Use this skill when working with Hatchling configuration, build system setup, Python packaging, pyproject.toml configuration, project metadata, dependencies, entry points, build hooks, version management, wheel and sdist builds, package distribution, setuptools migration, and troubleshooting Hatchling build errors.
---

# Hatchling

## Overview

Hatchling is a modern, standards-compliant Python build backend that replaces legacy setuptools for package building. It provides clear configuration through `pyproject.toml`, intelligent defaults, and extensibility through hooks and plugins. This skill enables understanding Hatchling's architecture, configuration options, and build customization capabilities.

## Key Capabilities

- **Configuration via pyproject.toml**: Standards-compliant PEP 621 metadata with sensible defaults
- **Build Targets**: Wheel and source distribution builds with extensive customization
- **Build Hooks**: Dynamic code execution during build for artifacts, version management, and compilation
- **Version Management**: Multiple version sources with automatic version injection
- **File Selection**: Git-aware VCS integration with glob pattern matching
- **Plugins**: Extensible architecture for custom builders, hooks, and metadata hooks

## Reference Documentation

This skill provides comprehensive reference documentation organized by topic. Each section links to detailed guides covering configuration, usage patterns, and examples.

### Project Configuration

- [Project Metadata & Configuration](./references/project-metadata/index.md) - Package metadata, dependencies, entry points, dynamic fields
- [Build System Configuration](./references/build-system/index.md) - Build backend setup, PEP 517/518, reproducible builds, environment variables

### Build Targets

- [Wheel Build Target](./references/wheel-target/index.md) - Wheel configuration, package discovery, file selection, editable installs
- [Source Distribution (Sdist) Target](./references/sdist-target/index.md) - Sdist configuration, VCS integration, legacy setup.py support
- [Build Target Types](./references/build-targets/index.md) - Wheel, sdist, binary, custom builders, multi-version builds
- [Build Targets Configuration Details](./references/target-config/index.md) - Target-specific hooks, dependencies, versions, precedence

### File Selection & Build Customization

- [File Selection & Patterns](./references/file-selection/index.md) - Git-style globs, include/exclude patterns, VCS integration, force-include
- [Build Hooks](./references/build-hooks/index.md) - Hook interface, execution order, custom hooks, version hooks, build data passing
- [Advanced Build Features](./references/advanced-features/index.md) - Dynamic dependencies, force-include, path rewriting, editable installs, build context

### Version & Metadata Management

- [Version Management](./references/version-management/index.md) - Version sources (code, regex, env), schemes, validation, build hooks
- [Metadata Hooks](./references/metadata-hooks/index.md) - Metadata hook interface, custom hooks, dynamic metadata generation
- [Context Formatting & Dynamic Configuration](./references/context-formatting/index.md) - Context variables, environment-based config, interpolation

### Plugin System

- [Plugin System & Extensibility](./references/plugins/index.md) - Builder, hook, metadata, version plugins, hatch-vcs, plugin development

### Build Environment & Integration

- [Build Environment Internals](./references/build-environment/index.md) - Environment config, dependencies, UV vs pip, Cython integration, isolation
- [Integration & Compatibility](./references/integration/index.md) - PEP standards compliance, setup.py migration, setuptools compatibility, CMake/extensions
- [Special Configuration Options](./references/special-config/index.md) - PEP 561 type hints, SPDX licenses, namespace packages, src-layout, extensions

### Core Concepts & Standards

- [Core Concepts & Best Practices](./references/core-concepts/index.md) - PEP 517 backend, minimal philosophy, VCS file selection, reproducible builds
- [Related Standards & Specifications](./references/standards/index.md) - Python packaging overview, PEP references, metadata specs, distribution formats

### Operational Guides

- [Command-Line Building](./references/cli-building/index.md) - hatch build commands, python -m build, pip install, output customization
- [Error Handling & Validation](./references/error-handling/index.md) - Path validation, file selection errors, version/license validation, heuristic failures
- [Release Notes & Version History](./references/release-notes/index.md) - Hatchling version history, feature additions, PEP 639 support, performance improvements
