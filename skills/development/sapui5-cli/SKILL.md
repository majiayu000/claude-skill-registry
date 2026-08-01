---
name: sapui5-cli
description: Manages SAPUI5/OpenUI5 projects using the UI5 Tooling CLI (@ui5/cli).
  Use when initializing UI5 projects, configuring ui5.yaml or ui5-workspace.yaml files,
  building UI5 applications or libraries, runn
---

---
name: sapui5-cli
description: Manages SAPUI5/OpenUI5 projects using the UI5 Tooling CLI (@ui5/cli). Use when initializing UI5 projects, configuring ui5.yaml or ui5-workspace.yaml files, building UI5 applications or libraries, running development servers with HTTP/2 support, creating custom build tasks or server middleware, managing workspace/monorepo setups, troubleshooting UI5 CLI errors, migrating between UI5 CLI versions, or optimizing build performance. Supports both OpenUI5 and SAPUI5 frameworks with complete configuration and extensibility guidance.
license: GPL-3.0
metadata:
  version: 4.0.0
  lastUpdated: 2025-11-21
  officialDocs: [https://ui5.github.io/cli/stable/](https://ui5.github.io/cli/stable/)
---

# SAPUI5/OpenUI5 CLI Management Skill

## Table of Contents
- [Overview](#overview)
- [When to Use This Skill](#when-to-use-this-skill)
- [Quick Start Workflow](#quick-start-workflow)
- [Project Types](#project-types)
- [Bundled Resources](#bundled-resources)

## Overview

This skill provides comprehensive guidance for working with the UI5 CLI (UI5 Tooling), the official command-line interface for developing, building, and deploying SAPUI5 and OpenUI5 applications and libraries.

**Current CLI Version**: 4.0.0+ (Released July 24, 2024)
**Node.js Requirements**: v20.11.0+ or v22.0.0+ (v21 not supported)
**npm Requirements**: v8.0.0+

## When to Use This Skill

Use this skill when you need to:

- **Initialize** new UI5 projects or enable CLI support for existing projects
- **Configure** ui5.yaml for applications, libraries, theme-libraries, or modules
- **Build** UI5 projects with optimization, bundling, and minification
- **Run** local development servers with HTTP/2, SSL, and CSP support
- **Extend** build processes with custom tasks or server middleware
- **Manage** monorepo/workspace configurations with multiple UI5 projects
- **Troubleshoot** common UI5 CLI errors and build issues
- **Migrate** between CLI versions (v1 → v2 → v3 → v4)
- **Optimize** build performance and analyze dependencies

## Quick Start Workflow

### New Project Setup

```bash
# 1. Install UI5 CLI (choose one)
npm install --global @ui5/cli          # Global installation
npm install --save-dev @ui5/cli        # Project-level installation

# 2. Initialize project (if new)
npm init --yes                          # Initialize npm
ui5 init                                # Create ui5.yaml

# 3. Select framework variant
ui5 use openui5@latest                  # For OpenUI5
ui5 use sapui5@latest                   # For SAPUI5

# 4. Add framework libraries
ui5 add sap.ui.core sap.m sap.ui.table themelib_sap_fiori_3

# 5. Start development
ui5 serve                               # Start dev server
ui5 serve --open index.html            # Start and open browser

# 6. Build for production
ui5 build --all                         # Build with dependencies
ui5 build --clean-dest                  # Clean before building
```

### Existing Project Setup

```bash
# 1. Enable CLI support
ui5 init

# 2. Configure framework (if ui5.yaml exists)
ui5 use openui5@latest                  # or sapui5@latest

# 3. Verify setup
ui5 tree                                # Show dependency tree
ui5 serve                               # Test development server
```

## Project Types

UI5 CLI supports four project types, each with specific configurations:

### 1. Application
Standard UI5 applications with a `webapp` directory.
- Virtual path mapping: `webapp/` → `/`
- Generates Component-preload.js when Component.js exists
- See `templates/ui5.yaml.application` for configuration template

### 2. Library
Reusable component libraries for sharing across projects.
- Virtual path mappings: `src/` → `/resources`, `test/` → `/test-resources`
- Requires namespace directory structure (e.g., `src/my/company/library/`)
- See `templates/ui5.yaml.library` for configuration template

### 3. Theme Library
Provides theming resources for libraries.
- Same virtual mappings as standard libraries
- Resources organized by namespace (e.g., `my/library/themes/custom_theme/`)
- See `references/configuration.md` for detailed configuration

### 4. Module
Third-party resources with flexible path mapping.
- Resources copied without modification
- Custom virtual-to-physical path mappings
- See `references/project-types.md` for module configuration

## Core Commands Reference

### Project Initialization
```bash
ui5 init                                # Initialize UI5 CLI configuration
ui5 use <framework>[@version]           # Set framework (openui5/sapui5)
ui5 add <libraries...>                  # Add framework libraries
ui5 remove <libraries...>               # Remove framework libraries
```

### Development
```bash
ui5 serve [options]                     # Start development server
  --port <number>                       # Specify port (default: 8080)
  --open <path>                         # Open browser to path
  --h2                                  # Enable HTTP/2
  --accept-remote-connections           # Allow non-localhost access

ui5 tree [options]                      # Display dependency tree
  --flat                                # Show flat list
  --level <number>                      # Limit tree depth
```

### Building
```bash
ui5 build [child-command] [options]     # Build project
  preload                               # Create preload bundles (default)
  self-contained                        # Create standalone bundle
  jsdoc                                 # Generate JSDoc documentation

  --all                                 # Include all dependencies
  --include-dependency <names>          # Include specific dependencies
  --exclude-dependency <names>          # Exclude dependencies
  --dest <path>                         # Output directory (default: ./dist)
  --clean-dest                          # Clean destination before build
  --create-build-manifest               # Store build metadata
  --experimental-css-variables          # Generate CSS variable artifacts [experimental]
```

### Configuration
```bash
ui5 config set <key> [value]            # Set configuration value
ui5 config get <key>                    # Get configuration value
ui5 config list                         # List all settings

# Common configurations
ui5 config set ui5DataDir /path/.ui5    # Change cache directory
```

### Utility
```bash
ui5 versions                            # Display all module versions
ui5 --help                              # Display help
ui5 --version                           # Display version
```

For complete command reference, see `references/cli-commands.md`.

## Configuration File Structure

### Basic ui5.yaml Structure

```yaml
specVersion: "4.0"                      # Specification version (required)
type: application                       # Project type (required)
metadata:
  name: my.project.name                 # Project name (required)
  copyright: "© ${currentYear} Company" # Optional copyright

framework:
  name: SAPUI5                          # OpenUI5 or SAPUI5
  version: "1.120.0"                    # Framework version
  libraries:
    - name: sap.ui.core
    - name: sap.m
    - name: sap.ui.table
    - name: themelib_sap_fiori_3
      optional: true                    # Optional library

resources:
  configuration:
    paths:
      webapp: webapp                    # Path mapping
    propertiesFileSourceEncoding: UTF-8 # Encoding (default: UTF-8)

builder:
  resources:
    excludes:
      - "index.html"                    # Exclude from build
      - "/resources/my/project/test/**"

server:
  settings:
    httpPort: 8080                      # HTTP port
    httpsPort: 8443                     # HTTPS port
```

For complete configuration reference, see `references/configuration.md`.

## Progressive Disclosure: Detailed References

This main skill file provides essential workflows and quick reference. For detailed information on specific topics, refer to these reference files:

### Core References
- **`references/cli-commands.md`**: Complete CLI command reference with all options and examples
- **`references/configuration.md`**: Comprehensive ui5.yaml configuration guide (includes workspace config)
- **`references/project-structures.md`**: Detailed project types with directory structures and build output styles

### Advanced Topics
- **`references/extensibility.md`**: Custom tasks, middleware, and project shims with complete API documentation
- **`references/filesystem-api.md`**: Complete FileSystem API for custom task/middleware development
- **`references/build-process.md`**: Complete build process including tasks, minification, source maps, and bundling
- **`references/server-features.md`**: Complete server documentation with middleware stack, HTTP/2, SSL, and CSP
- **`references/code-analysis.md`**: Dependency analyzers, JSDoc generation, and code analysis features
- **`references/es-support.md`**: Complete ECMAScript version support, restrictions, and module format requirements

### Performance & Troubleshooting
- **`references/benchmarking.md`**: Performance testing and benchmarking with hyperfine
- **`references/migration-guides.md`**: Complete version migration guides (v1→v2→v3→v4)
- **`references/troubleshooting.md`**: Common issues, errors, and solutions with exact error messages

## Common Workflows

### Workflow 1: Setting Up a New Application

**When to use**: Starting a new SAPUI5/OpenUI5 application from scratch.

**Steps**:
1. Initialize npm project: `npm init --yes`
2. Install UI5 CLI: `npm install --save-dev @ui5/cli`
3. Initialize UI5 configuration: `ui5 init`
4. Select framework: `ui5 use sapui5@latest` (or `openui5@latest`)
5. Add required libraries: `ui5 add sap.ui.core sap.m themelib_sap_fiori_3`
6. Create application structure (webapp/, Component.js, manifest.json)
7. Start development server: `ui5 serve`
8. Commit configuration: `git add ui5.yaml package.json && git commit`

### Workflow 2: Enabling CLI for Existing Project

**When to use**: Adding UI5 CLI support to an existing UI5 project.

**Steps**:
1. Navigate to project root
2. Run `ui5 init` to create ui5.yaml
3. Configure framework: `ui5 use sapui5@latest`
4. Add libraries: `ui5 add sap.ui.core sap.m sap.ui.table`
5. Adjust ui5.yaml `resources.configuration.paths` if needed
6. Test with `ui5 serve`
7. Build with `ui5 build --all`

### Workflow 3: Creating a Custom Build Task

**When to use**: Extending the build process with custom processing.

**Steps**:
1. Create task file (e.g., `lib/tasks/customTask.js`)
2. Implement task using Task API (see `templates/custom-task-template.js`)
3. Create task extension in ui5.yaml or separate file
4. Configure task in builder.customTasks section
5. Test with `ui5 build`
6. For details, see `references/extensibility.md`

### Workflow 4: Setting Up a Workspace/Monorepo

**When to use**: Managing multiple related UI5 projects in a single repository.

**Steps**:
1. Create ui5-workspace.yaml in root project
2. Define workspace name and dependency resolutions
3. Point to local project directories using relative paths
4. Use `--workspace <name>` flag to activate specific workspace
5. Run `ui5 tree` to verify dependency resolution
6. For details, see `references/configuration.md` (workspace section)

### Workflow 5: Migrating to UI5 CLI v4

**When to use**: Upgrading from UI5 CLI v3 to v4.

**Prerequisites**:
- Verify Node.js v20.11.0+ or v22.0.0+
- Verify npm v8.0.0+

**Steps**:
1. Update CLI: `npm install --save-dev @ui5/cli@latest`
2. Update specVersion in ui5.yaml to `"4.0"`
3. Review breaking changes in `references/migration-guides.md`
4. Remove `usePredefineCalls` bundle option if present
5. Update bundle sections to use `async: true` for modern loading
6. Test build: `ui5 build --all`
7. Test server: `ui5 serve`
8. Verify application functionality

## Decision Trees

### Framework Selection Decision

**Question**: Which framework should I use?

```
Does project need SAP-specific components (e.g., sap.ui.comp, sap.ushell)?
├─ YES → Use SAPUI5
│  └─ Command: ui5 use sapui5@latest
└─ NO → Can use OpenUI5
   └─ Command: ui5 use openui5@latest

Note: SAPUI5 projects can depend on OpenUI5, but not vice versa.
```

### Build Type Decision

**Question**: Which build type should I use?

```
What is the deployment target?
├─ Standard deployment (with separate framework loading)
│  └─ Use: ui5 build --all
│
├─ Standalone deployment (single bundle with framework)
│  └─ Use: ui5 build self-contained --all
│
├─ Documentation generation
│  └─ Use: ui5 build jsdoc
│
└─ Development/testing (no build needed)
   └─ Use: ui5 serve
```

### Custom Extension Decision

**Question**: Should I create a custom task or middleware?

```
What do you need to extend?
├─ Build process (modify/generate resources during build)
│  └─ Create custom task (see templates/custom-task-template.js)
│     Examples: Transpiling, image optimization, file generation
│
├─ Development server (modify requests/responses during dev)
│  └─ Create custom middleware (see templates/custom-middleware-template.js)
│     Examples: Proxying, authentication, dynamic content
│
└─ Third-party library configuration
   └─ Create project shim (see references/extensibility.md)
      Examples: Configuring non-UI5 npm packages
```

## Templates

This skill provides working templates for common configurations:

- **`templates/ui5.yaml.application`**: Complete application configuration
- **`templates/ui5.yaml.library`**: Complete library configuration
- **`templates/ui5-workspace.yaml`**: Monorepo workspace setup
- **`templates/custom-task-template.js`**: Custom build task boilerplate
- **`templates/custom-middleware-template.js`**: Custom server middleware boilerplate

## Important Notes

### Specification Versions

UI5 CLI uses specification versions to manage features:
- **4.0**: Current version (requires CLI v4.0.0+, Node.js v20.11.0+)
- **3.0-3.2**: Compatible with CLI v3.0.0+
- **2.0-2.6**: Compatible with CLI v2.0.0+
- **0.1-1.1**: Legacy versions (automatic migration attempted)

Always use the latest specVersion for new projects.

### Framework Version Requirements

- **OpenUI5**: Minimum version 1.52.5
- **SAPUI5**: Minimum version 1.76.0

### Development vs. Build

**Important**: During development, always use `ui5 serve` instead of `ui5 build`. Building should only occur when deploying to production. The development server provides:
- Faster reload times
- On-the-fly resource processing
- Better debugging experience
- Automatic dependency resolution

### Global vs. Local Installation

When both global and local UI5 CLI installations exist, the local version takes precedence automatically. This allows different projects to use different CLI versions.

Override behavior: `UI5_CLI_NO_LOCAL=X ui5 serve`

### Cache Management

UI5 CLI caches framework versions in `~/.ui5/` (configurable via `ui5DataDir`).

Clear cache: `rm -rf ~/.ui5/framework/`

## Known Issues & Limitations

### ECMAScript Module Limitations

UI5 CLI **does not support** JavaScript modules with `import`/`export` syntax. All modules must use `sap.ui.define` format.

**Unsupported**:
```javascript
import Module from './module.js';
export default MyClass;
```

**Supported**:
```javascript
sap.ui.define(['./module'], function(Module) {
    return MyClass;
});
```

### Template Literal Restrictions

Expressions in template literals cannot be used in:
- Dependency declarations
- Smart Template names
- Library initialization calls

**Unsupported**:
```javascript
sap.ui.define([`modules/${moduleName}`], ...);  // Will fail
```

### Bundling Restrictions (v4.0+)

JavaScript modules requiring 'top level scope' cannot be bundled as strings. They will be omitted from bundles with error logging.

### Manifest Version Compatibility

For UI5 1.71, manifest `_version` property must be ≤ 1.17.0 for `supportedLocales` generation. Update manifest version to match UI5 framework version.

## Troubleshooting Quick Reference

For detailed troubleshooting, see `references/troubleshooting.md`.

### Common Issues

**Issue**: `ERR_SSL_PROTOCOL_ERROR` in Chrome when accessing HTTP server

**Solution**: Chrome enforces HTTPS via HSTS. Clear HSTS settings:
1. Navigate to `chrome://net-internals/#hsts`
2. Enter domain (e.g., localhost)
3. Click "Delete"

**Issue**: Excessive disk space in `~/.ui5/`

**Solution**: Clear cached framework versions:
```bash
rm -rf ~/.ui5/framework/
```

**Issue**: Build fails with "TypeError: invalid input"

**Solution**: Check manifest `_version` compatibility with UI5 framework version. For UI5 1.71, use manifest version ≤ 1.17.0.

**Issue**: Custom task not executing

**Solution**: Verify task configuration:
1. Check task is properly defined in ui5.yaml
2. Verify `beforeTask` or `afterTask` references valid task name
3. Check task file exports async function with correct signature
4. Use `ui5 build --verbose` for detailed logging

## Environment Variables

- **`UI5_LOG_LVL`**: Set log level (silent/error/warn/info/perf/verbose/silly)
- **`UI5_DATA_DIR`**: Override default data directory (~/.ui5)
- **`UI5_CLI_NO_LOCAL`**: Disable local CLI precedence (use global)

Examples:
```bash
UI5_LOG_LVL=verbose ui5 build
UI5_DATA_DIR=/custom/.ui5 ui5 serve
```

## Best Practices

1. **Always commit ui5.yaml and package.json** to version control
2. **Use local CLI installation** for project consistency (`--save-dev`)
3. **Pin framework versions** for production builds
4. **Use workspaces** for monorepo setups instead of npm linking
5. **Enable HTTP/2** during development (`ui5 serve --h2`)
6. **Clean builds** for production (`ui5 build --clean-dest --all`)
7. **Validate configurations** before committing (use validation scripts)
8. **Test with multiple browsers** when using CSP policies
9. **Document custom tasks** and middleware in project README
10. **Keep CLI updated** to benefit from latest features and fixes

## Additional Resources

- **Official Documentation**: [https://ui5.github.io/cli/stable/](https://ui5.github.io/cli/stable/)
- **API Reference**: [https://ui5.github.io/cli/v4/api/](https://ui5.github.io/cli/v4/api/)
- **JSON Schema**: [https://ui5.github.io/cli/schema/ui5.yaml.json](https://ui5.github.io/cli/schema/ui5.yaml.json)
- **GitHub Repository**: [https://github.com/SAP/ui5-tooling](https://github.com/SAP/ui5-tooling)
- **SAP Community**: [https://community.sap.com/](https://community.sap.com/)
- **npm Registry**: [https://www.npmjs.com/package/@ui5/cli](https://www.npmjs.com/package/@ui5/cli)

## Bundled Resources

### Reference Documentation
- `references/cli-commands.md` - Complete CLI command reference
- `references/configuration.md` - Configuration options and ui5.yaml
- `references/project-structures.md` - Project structure patterns
- `references/server-features.md` - Development server features
- `references/build-process.md` - Build process and optimization
- `references/es-support.md` - ES module support
- `references/extensibility.md` - Extensibility options
- `references/code-analysis.md` - Code analysis tools
- `references/migration-guides.md` - Migration from older versions
- `references/troubleshooting.md` - Common issues and solutions
- `references/benchmarking.md` - Performance benchmarking

### Templates
- `templates/package.json.template` - Package.json template

## Version Information

- **Skill Version**: 1.0.0
- **CLI Version Covered**: 4.0.0+
- **Last Updated**: 2025-11-21
- **Next Review**: 2026-02-21 (Quarterly)

---

*This skill follows official Anthropic Agent Skills best practices and SAP UI5 CLI documentation standards.*
