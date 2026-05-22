---
name: create-package
description: Scaffold, build, and publish a Datagrok package with functions, viewers, and panels
---

# Create a Datagrok Package

Help the user scaffold a new Datagrok package, add functions to it, build, and publish.

## Usage
```
/create-package [package-name] [--test] [--js]
```

## Instructions

### 1. Scaffold the package

Run from the directory where the package folder should be created:

```shell
grok create <PackageName> --test
```

- Package name must be **PascalCase** (e.g., `TextStats`, `MyAnalysis`).
- The `--test` flag adds a test scaffold. Use `--js` for plain JavaScript instead of TypeScript.
- After creation, install dependencies:

```shell
cd <PackageName>
npm install
```

### 2. Understand the package structure

The created package contains:
- `src/package.ts` -- main entry point for functions, viewers, panels, apps
- `detectors.js` -- semantic type detectors (loaded separately from the bundle)
- `webpack.config.js` -- webpack configuration (do not modify the externals)
- `package.json` -- metadata and dependencies

### 3. Add functions to the package

Functions are defined with annotation comments above the export. Common types:

**Panel function** (appears in context panel for matching data):
```typescript
//name: MyPanel
//tags: panel, widgets
//input: string str {semType: text}
//output: widget result
export function myPanel(str: string) {
  return new DG.Widget(ui.divV([
    ui.divText('Result: ' + str.length)
  ]));
}
```

**Add more function types via CLI:**
```shell
grok add app <name>        # Application entry point
grok add viewer <name>     # Custom viewer
grok add detector <name>   # Semantic type detector
```

### 4. Build the package

```shell
npm run build
```

This runs `grok api` (auto-generates wrappers), `grok check --soft` (validates), and `webpack` (bundles). Do not modify the `build` script in `package.json`.

### 5. Publish the package

Publish to a configured server:

```shell
grok publish dev           # Debug mode (only visible to you)
grok publish dev --release # Release mode (visible to shared groups)
```

Return code `0` means success. After publishing in debug mode, find the package under `Manage | Packages` prefixed with `v.`.

### 6. Share and release

- Share the package to user groups via right-click menu on the package in `Manage | Packages`.
- For public release: `grok publish public --release`.

## Behavior

- Always ask for the package name if not provided.
- Use PascalCase for the package name.
- Default to TypeScript unless the user requests JavaScript.
- Include the `--test` flag unless the user says otherwise.
- After scaffolding, remind the user to run `npm install`.
- Follow Datagrok coding conventions: no excessive comments, no curly brackets for one-line if/for, catch/else-if on new line.
- When adding functions, use the annotation comment format (`//name:`, `//tags:`, `//input:`, `//output:`).
- Warn if webpack externals are modified (datagrok-api, rxjs, cash-dom, dayjs, wu, openchemlib/full are provided by the platform).
