---
name: flutter-module-creator
description: Create Flutter/Dart modules in Melos monorepo workspaces. Use when the user wants to create new Flutter apps, Dart packages, Flutter plugins, or FFI plugins in a Melos-managed workspace. Triggers on requests like "create a new Flutter app", "add a package", "create a plugin", "add FFI module", or any module creation in Flutter/Dart monorepos.
---

# Flutter Module Creator

Create modules in a Melos monorepo workspace with proper configuration.

## Usage

```bash
dart run <skill_path>/scripts/create_module.dart --type <type> --name <name> [options]
```

## Module Types

- `app`: Flutter application (use `--console` for Dart console app)
- `package`: Dart package (use `--flutter` for Flutter package)
- `plugin`: Flutter plugin
- `ffi`: Flutter FFI plugin

## Options

- `--console`: Create Dart console app (app type only)
- `--flutter`: Create Flutter package (package type only)
- `--platforms <list>`: Comma-separated platforms (plugin/ffi), e.g., `android,ios`
- `--workspace <path>`: Workspace root (auto-detected)
- `--no-bootstrap`: Skip melos bootstrap

## Examples

```bash
# Basic usage
dart run <skill_path>/scripts/create_module.dart --type app --name my_app
dart run <skill_path>/scripts/create_module.dart --type package --name my_utils

# With options
dart run <skill_path>/scripts/create_module.dart --type app --name my_cli --console
dart run <skill_path>/scripts/create_module.dart --type package --name my_widgets --flutter
dart run <skill_path>/scripts/create_module.dart --type plugin --name my_plugin --platforms android,ios
```

## What It Does

1. Detects workspace root (melos/workspace in pubspec.yaml)
2. Creates module in `apps/` or `packages/` directory
3. Configures `analysis_options.yaml` with appropriate lints
4. Adds `resolution: workspace` to module pubspec.yaml
5. Updates root `workspace:` list
6. Copies LICENSE from workspace root
7. Runs `melos bootstrap` (unless `--no-bootstrap`)

## Post-Creation Cleanup (REQUIRED)

After creating a module, you MUST clean up the boilerplate code:

1. Delete or replace generated placeholder source files (e.g., `lib/src/*_base.dart` with `Awesome` class)
2. Update `example/` with actual usage code (remove `Awesome` references)
3. Update the barrel export file (`lib/<name>.dart`) to export real files
4. Run `melos analyze` to verify no dead code or missing references
