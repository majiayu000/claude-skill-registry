---
name: univer-integrate
description: Integrate Univer Sheets, Docs, or Slides into React, Vue 3, HTML, or Node.js projects. Use when embedding Univer, choosing preset or plugin mode, initializing instances, configuring themes/locales/workers, or manipulating workbooks, worksheets, ranges, formulas, permissions, and events through the Facade API.
---

# Univer Integrate

Embed Univer in an application and operate it through the public Facade API.

> **Source baseline**: Univer `1.0.0-beta.0`, synchronized with the current `dream-num/univer` source. First inspect the user's installed `@univerjs/*` version and existing setup; preserve that version when modifying an existing project.

## 1.0 product boundary

The product matrix represented by `UniverInstanceType` now covers Sheets, Docs, Slides, Bases, Boards, and PDFs. This OSS skill owns Sheets and Docs preset integration plus the OSS Slides package boundary. Use `univer-pro-integrate` for the current licensed Slides product and for Bases, Boards, or PDFs; those products use separate Pro plugins, Facade entries, CSS, and unit snapshots.

## Choose an integration mode

- Use **Preset Mode** for a new application or ordinary integration. Presets compose the required plugins and Facade registrations; browser styles and locale bundles remain explicit imports.
- Use **Plugin Mode** only when the application needs custom loading, smaller bundles, plugin replacement, or exact registration control. Read `references/plugin-registry.md` before composing plugins manually.
- Use `univer-node-backend` for a dedicated headless Node.js workflow.

## Quick start: Sheets preset

Keep every `@univerjs/*` dependency on one exact version:

```bash
npm install @univerjs/presets@1.0.0-beta.0 @univerjs/preset-sheets-core@1.0.0-beta.0 react@19.2.8 react-dom@19.2.8 rxjs@7.8.2
```

```ts
import { UniverSheetsCorePreset } from '@univerjs/preset-sheets-core';
import UniverPresetSheetsCoreEnUS from '@univerjs/preset-sheets-core/locales/en-US';
import { createUniver, defaultTheme, LocaleType, mergeLocales } from '@univerjs/presets';

import '@univerjs/preset-sheets-core/lib/index.css';

const { univer, univerAPI } = createUniver({
  locale: LocaleType.EN_US,
  locales: {
    [LocaleType.EN_US]: mergeLocales(UniverPresetSheetsCoreEnUS),
  },
  theme: defaultTheme,
  presets: [
    UniverSheetsCorePreset({
      container: 'app',
    }),
  ],
});

const workbook = univerAPI.createWorkbook({
  id: 'workbook-1',
  name: 'Demo',
  sheetOrder: ['sheet-1'],
  sheets: {
    'sheet-1': {
      id: 'sheet-1',
      name: 'Sheet1',
      rowCount: 100,
      columnCount: 20,
    },
  },
});

workbook.getActiveSheet()!.getRange('A1:B2').setValues([
  ['Hello', 'Univer'],
  [1, 2],
]);

window.addEventListener('pagehide', () => univer.dispose(), { once: true });

```

In a component framework, call `univer.dispose()` from the component's own teardown instead.

The page needs a sized container:

```html
<div id="app" style="height: 100vh"></div>
```

## Add features with presets

Install each feature at the same version as `@univerjs/presets`, import its locale, and append its preset:

```ts
import { UniverSheetsDataValidationPreset } from '@univerjs/preset-sheets-data-validation';
import UniverPresetSheetsDataValidationEnUS from '@univerjs/preset-sheets-data-validation/locales/en-US';

import '@univerjs/preset-sheets-data-validation/lib/index.css';

const { univerAPI } = createUniver({
  locale: LocaleType.EN_US,
  locales: {
    [LocaleType.EN_US]: mergeLocales(
      UniverPresetSheetsCoreEnUS,
      UniverPresetSheetsDataValidationEnUS,
    ),
  },
  presets: [
    UniverSheetsCorePreset({ container: 'app' }),
    UniverSheetsDataValidationPreset(),
  ],
});
```

Available OSS presets are listed in `references/plugin-registry.md`. Import the stylesheet owned by every browser preset. Do not register both a preset and the same underlying plugin.

## Facade API rules

Preset packages register their Facade extensions. In Plugin Mode, explicitly import the `/facade` entry for every capability used:

```ts
import { FUniver } from '@univerjs/core/facade';

import '@univerjs/engine-formula/facade';
import '@univerjs/sheets/facade';
import '@univerjs/sheets-formula/facade';
import '@univerjs/ui/facade';

const univerAPI = FUniver.newAPI(univer);
```

Prefer feature-level Facade methods and builders over internal services:

```ts
const workbook = univerAPI.getActiveWorkbook();
if (!workbook) throw new Error('No active workbook');

const worksheet = workbook.getActiveSheet();
if (!worksheet) throw new Error('No active worksheet');

worksheet.getRange('A1')
  .setValue('Hello')
  .setBackground('#ff0000')
  .setFontColor('#ffffff');

const snapshot = workbook.save();
```

Read `references/facade-api-guide.md` for the current method names and feature import map.

## Version policy

1. Inspect `package.json`, the lockfile, or `node_modules/@univerjs/core/package.json`.
2. Reuse the project's exact installed version for every `@univerjs/*` package.
3. For a new project targeting this source baseline, use `1.0.0-beta.0`.
4. Do not mix OSS or preset package versions. If Pro is present, align `@univerjs-pro/*` to the same release line too.

## Runtime compatibility

Current Univer targets Edge 88+, Firefox 90+, Chrome 88+, Safari 14.1+, and Electron 12+. Headless Univer supports Node.js 18.17+. Add an `Intl.Segmenter` polyfill when the target runtime does not provide it.

## Themes and locales

Set the initial theme in `createUniver`. Current source also supports runtime theme changes through the Facade:

```ts
univerAPI.setTheme(defaultTheme);
univerAPI.toggleDarkMode(true);
univerAPI.setLocale(LocaleType.EN_US);
```

Use `univer-customize-theme` for branded palettes, dark mode, plugin CSS variables, six-product theme boundaries, and the installed-release gate for current theme methods.

Verify the installed `FUniver` declarations before emitting `setTheme()`, `getCurrentTheme()`, or `isDarkMode()`; the published npm package carrying the current source's prerelease version label can lag those methods. Initialization remains the portable theme-selection path.

Load every locale bundle owned by the presets or plugins you register. Do not cache translated strings yourself.

## Core model

- `univerAPI.createWorkbook(data)` creates and returns an `FWorkbook`.
- `univerAPI.getWorkbook(id)` retrieves a specific workbook.
- `workbook.getActiveSheet()` and `workbook.getSheetByName(name)` return `FWorksheet` objects.
- `worksheet.getRange('A1:B2')` returns an `FRange`.
- `workbook.save()` returns the current `IWorkbookData` snapshot.
- `univerAPI.disposeUnit(id)` disposes one unit; `univer.dispose()` tears down the application.

Use `createDocument` only after registering the corresponding Docs preset/plugin. Do not represent Bases, Boards, PDFs, or the current Pro Slides product as workbooks; use their product-specific Facade creation methods documented by `univer-pro-integrate`.

## Anti-patterns

- Do not mutate `Workbook` or `Worksheet` models directly. Use Facade methods or Commands so undo/redo and reactive updates remain consistent.
- Do not invent a Facade method from an older release. Check the installed package source or types; several `0.x` method names changed in `1.0.0-beta.0`.
- Do not copy manual plugin lists into new apps when an existing preset already owns the same composition.
- Do not omit the preset or plugin CSS in browser builds.
- Do not retain workbook, worksheet, or range handles after their unit or Univer instance is disposed.
- Do not create a separate Univer instance merely to add another workbook. Use multiple units unless the page genuinely needs independent editor containers.

## Common operations

```ts
const workbook = univerAPI.getActiveWorkbook()!;
const worksheet = workbook.getActiveSheet()!;

worksheet.getRange('A1:D2').setValues([
  ['Product', 'Qty', 'Price', 'Total'],
  ['Apple', 2, 3, '=B2*C2'],
]);

worksheet.setColumnWidth(0, 140);
worksheet.setRowHeight(0, 32);
workbook.undo();
workbook.redo();
```

## References

- `references/facade-api-guide.md` — current Facade hierarchy, method names, imports, and feature examples
- `references/common-tasks.md` — persistence, formatting, hyperlinks, events, CSV, themes, and large datasets
- `references/plugin-registry.md` — current OSS presets and manual plugins
- `references/framework-integration.md` — React, Vue 3, Web Component, iframe, and Node lifecycle patterns
- `references/worker-setup.md` — current browser and Node worker presets
- `references/custom-functions.md` — synchronous and asynchronous custom formula functions
- `references/permissions.md` — workbook, worksheet, and range permission Facades
- `references/multi-unit-management.md` — creating, retrieving, focusing, and disposing multiple units
- `references/network-and-others.md` — Network, Watermark, Action Recorder, and Telemetry boundaries

## Templates

Copy the smallest matching template from `assets/templates/`:

- `react-vite/`
- `vue3-vite/`
- `plain-html/`
- `node/`
