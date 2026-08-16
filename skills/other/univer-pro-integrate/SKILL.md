---
name: univer-pro-integrate
description: Integrate current Univer Pro features into browser applications. Use for licensed Sheets, Docs, Slides, Bases, Boards, or PDFs; advanced Sheets presets; collaboration and edit history; Office import/export; printing; pivot tables; charts; sparklines; shapes; Pro workers; license ordering; or Pro Facade APIs.
---

# Univer Pro Integrate

Add licensed Univer Pro capabilities to an existing Univer application.

> **Source baseline**: Univer and Univer Pro `1.0.0-beta.0`, synchronized with the current `dream-num/univer` and `dream-num/univer-pro` sources. Inspect the target project's installed versions first and preserve that exact release line.

> **Prerequisite**: Use `univer-integrate` for the base application, container, locale, unit creation, and ordinary Facade patterns. Use `univer-customize-theme` for application palettes, dark mode, and the separate Pro Chart theme registry.

## Choose the integration path

- Use `@univerjs/preset-sheets-advanced` for ordinary Pro Sheets integration. It composes the license, Pro formula, pivot table, print, chart, outline, shape, sparkline, and Sheets exchange plugins plus their Facade extensions.
- Add `@univerjs/preset-sheets-collaboration` for collaboration and edit history. Register it after the Advanced preset.
- Use `@univerjs/preset-docs-advanced` and `@univerjs/preset-docs-collaboration` for ordinary Pro Docs integration.
- Use Plugin Mode only for custom loading, exact bundle composition, or hosts without a matching Pro preset, such as Slides, Bases, Boards, and PDFs.
- Never register both a preset and a plugin already owned by that preset.

In `1.0.0-beta.0`, Slides, Bases, Boards, and PDFs are real Pro product hosts with their own runtime/UI packages, host `/facade` entry, and creation method (`createPresentation`, `createBase`, `createBoard`, and `createPdf`). They do not have unified Pro presets. Follow the product matrix and Plugin Mode chains in `references/pro-features-guide.md`; do not infer a preset merely because a product or Facade exists.

## Version policy

1. Read `package.json`, the lockfile, or an installed Univer package manifest.
2. Keep every `@univerjs/*`, `@univerjs-pro/*`, and `@univerjs/preset-*` package on the same exact Univer version.
3. For a new project targeting this source baseline, use `1.0.0-beta.0`.
4. Treat a package-version mismatch as an integration error; Univer validates plugin versions at runtime.

## Quick start: add Pro Sheets to the base preset

Install the Pro preset at the same version as the base preset:

```bash
npm install @univerjs/preset-sheets-advanced@1.0.0-beta.0
```

Extend the `univer-integrate` Sheets preset example with the Advanced locale, stylesheet, and preset:

```ts
import { UniverSheetsAdvancedPreset } from '@univerjs/preset-sheets-advanced';
import UniverPresetSheetsAdvancedEnUS from '@univerjs/preset-sheets-advanced/locales/en-US';

import '@univerjs/preset-sheets-advanced/lib/index.css';

declare const clientLicense: string;

const { univer, univerAPI } = createUniver({
  locale: LocaleType.EN_US,
  locales: {
    [LocaleType.EN_US]: mergeLocales(
      UniverPresetSheetsCoreEnUS,
      UniverPresetSheetsAdvancedEnUS,
    ),
  },
  theme: defaultTheme,
  presets: [
    UniverSheetsCorePreset({ container: 'app' }),
    UniverSheetsAdvancedPreset({
      license: clientLicense,
      universerEndpoint: 'https://your-universer.example.com',
    }),
  ],
});
```

Keep the license outside source control. `universerEndpoint` is the Universer origin; the preset derives the upload, import, export, task, sign, and download routes from it.

## Add collaboration

```bash
npm install @univerjs/preset-sheets-collaboration@1.0.0-beta.0
```

```ts
import { UniverSheetsCollaborationPreset } from '@univerjs/preset-sheets-collaboration';
import UniverPresetSheetsCollaborationEnUS from '@univerjs/preset-sheets-collaboration/locales/en-US';

import '@univerjs/preset-sheets-collaboration/lib/index.css';

const collaborationPreset = UniverSheetsCollaborationPreset({
  universerEndpoint: 'https://your-universer.example.com',
  univerContainerId: 'app',
  enableOfflineEditing: true,
});
```

Set `collaboration: true` in the top-level `createUniver` options, merge the collaboration locale, and append `collaborationPreset` after `UniverSheetsAdvancedPreset(...)`. Pass `collaboration: true` to OSS feature presets that expose that option, such as the Drawing preset. Load a shared server unit with `univerAPI.loadServerUnit(unitId, type)` rather than creating a blank local workbook with the same ID.

## Plugin Mode rules

Register a configured license before every Pro plugin:

```ts
import { UniverLicensePlugin } from '@univerjs-pro/license';
import { UniverSheetsPrintPlugin } from '@univerjs-pro/sheets-print';

import '@univerjs-pro/sheets-print/facade';

univer.registerPlugin(UniverLicensePlugin, { license: clientLicense });
univer.registerPlugin(UniverSheetsPrintPlugin);
```

Many Pro plugins declare `UniverLicensePlugin` as a dependency. If a dependent plugin runs first, Univer can auto-register the license plugin with default empty configuration; a later explicit registration is then a duplicate. Configure dependencies before dependents, register all plugins before creating units, and import each required `/facade` side-effect entry before calling its Facade methods.

Plugin registration, Facade side-effect imports, CSS, and locales are independent requirements. In particular, importing `@univerjs-pro/<package>/facade` does not register its plugin or load its stylesheet. Import each selected CSS-owning package's `/lib/index.css` in Plugin Mode; a preset integration instead imports that preset's aggregate `/lib/index.css`.

## Current Facade examples

Import and export Sheets:

```ts
const unitId = await univerAPI.importSheetToUnitIdAsync(file);
if (!unitId) throw new Error('The workbook could not be imported');

const exported = await univerAPI.exportSheetByUnitIdAsync(unitId);
if (!exported) throw new Error('The workbook could not be exported');

univerAPI.downloadFile(exported, 'report', 'xlsx');
```

Print the active workbook:

```ts
const workbook = univerAPI.getActiveWorkbook();
if (!workbook) throw new Error('No active workbook');

workbook.openPrintDialog();
```

Insert a chart:

```ts
const worksheet = workbook.getActiveSheet();
if (!worksheet) throw new Error('No active worksheet');

const chartInfo = worksheet
  .newChart(univerAPI.Enum.ChartTypeString.Column)
  .setSource({
    range: 'A1:D8',
    orientation: univerAPI.Enum.ChartSourceOrientation.Columns,
  })
  .setPosition('F2')
  .setSize(640, 360)
  .setTitle('Quarterly sales')
  .build();

await worksheet.insertChart(chartInfo);
```

## Feature routing

- Read `references/pro-features-guide.md` for presets, worker composition, and the current package families.
- Read `references/collaboration-guide.md` for server routes, loading shared units, status, collaborators, and flushing pending changes.
- Read `references/exchange-guide.md` for Sheets, Docs, Slides, Bases, Boards, and PDFs exchange methods and snapshot conversion.
- Read `references/print-guide.md` for Sheets print configuration, range screenshots, and Slides print.
- Read `references/license-guide.md` for registration order and worker-license propagation.
- Read `references/facade-extension-pro.md` for current pivot, chart, shape, sparkline, and collaboration Facade methods.

## Anti-patterns

- Do not migrate a `0.25.0` entry by changing only version strings. Current presets, aggregate CSS, Facade export surfaces, product hosts, and registration composition differ; use the verified comparison in `pro-features-guide.md`.
- Do not copy `0.x` method names such as `importXLSXToUnitIdAsync`, `newChart()` without a type, `setChartType`, `newShape`, or `PrintOrientation` into a `1.0.0-beta.0` project.
- Do not put Sheets-specific exchange options on `UniverExchangeClientPlugin`; configure `UniverSheetsExchangeClientPlugin` instead.
- Do not instantiate or mutate internal models for an operation that has a Facade or Command API.
- Do not commit client licenses or embed server-license files in frontend bundles.
- Do not omit Pro locale bundles or package styles in browser integrations.
