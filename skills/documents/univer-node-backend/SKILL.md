---
name: univer-node-backend
description: Run Univer Sheets, Docs, Slides, Bases, Boards, or PDFs in Node.js without browser UI. Use for server-side or backend Univer, OSS Sheets or Docs Node presets, Pro product Facades and collaboration, JSON snapshot processing, formula or Base child-process workers, or automated unit manipulation with @univerjs/rpc-node.
---

# Univer Node.js Backend

Run Univer without browser UI for data, document, presentation, Base, Board, and PDF automation.

> **Compatibility**: Synced to the current Univer and Univer Pro source baseline, `1.0.0-beta.0`. Keep every `@univerjs/*` and `@univerjs-pro/*` package on exactly the same version. The public OSS headless runtime supports Node.js `>=18.17.0`; developing the current Univer source checkout requires Node.js `>=22.18` and pnpm `>=10`.

> **Public setup**: Prefer `createUniver` with `@univerjs/preset-sheets-node-core` or `@univerjs/preset-docs-node-core` when either OSS preset fits. `createUniverOnNode` is the name of an example-local helper in the Univer repositories, not an exported npm API. The other four product hosts currently use manual Pro plugin stacks.

## Choose the product path

Package existence, headless model/Facade support, browser rendering, and a maintained preset are separate facts:

| Product | Current Node path | Verified current example boundary |
| --- | --- | --- |
| Sheets | OSS `UniverSheetsNodeCorePreset`; manual Pro stack for licensed features | Local OSS workbooks; the Pro example loads a collaborative Sheet |
| Docs | OSS `UniverDocsNodeCorePreset`; manual Pro stack for licensed Docs features | Local document model through the OSS preset; the Pro example loads a collaborative Doc |
| Slides | Manual `@univerjs-pro/slides` stack and `@univerjs-pro/slides/facade` | The current Pro example loads a collaborative Slide |
| Bases | Manual `@univerjs-pro/bases` stack and `@univerjs-pro/bases/facade`; the current example pairs a Node formula worker | The current Pro example loads a collaborative Base |
| Boards | Manual `@univerjs-pro/boards` stack and `@univerjs-pro/boards/facade` | The current Pro example can call local `createBoard(...)` or load a collaborative Board |
| PDFs | Manual `@univerjs-pro/pdfs` stack and `@univerjs-pro/pdfs/facade` | The current Pro example loads a collaborative PDF and edits its model |

Slides, Bases, Boards, and PDFs have no unified Node preset in the checked source. Their current Node examples register runtime/model plugins and Facade side effects without `*-ui` plugins or CSS. A registered render engine satisfies model dependencies in some examples; it does not establish browser canvas rendering, screenshots, print, or exchange-client support. Read the [Node plugin registry](references/node-plugin-registry.md) and [Pro Node.js integration](references/node-pro-integration.md) before composing one of these hosts.

## Quick Start

### 1. Install the current Node preset

```bash
npm install @univerjs/core@1.0.0-beta.0 @univerjs/presets@1.0.0-beta.0 @univerjs/preset-sheets-node-core@1.0.0-beta.0 rxjs@^7.8.2
```

### 2. Create and process a workbook

```ts
import { LocaleType } from '@univerjs/core';
import { UniverSheetsNodeCorePreset } from '@univerjs/preset-sheets-node-core';
import UniverSheetsNodeCoreEnUS from '@univerjs/preset-sheets-node-core/locales/en-US';
import { createUniver } from '@univerjs/presets';

const { univer, univerAPI } = createUniver({
  locale: LocaleType.EN_US,
  locales: {
    [LocaleType.EN_US]: UniverSheetsNodeCoreEnUS,
  },
  presets: [UniverSheetsNodeCorePreset()],
});

try {
  const workbook = univerAPI.createWorkbook({});
  const sheet = workbook.getActiveSheet();

  sheet.getRange('A1').setValue(123);
  sheet.getRange('B1').setValue('=SUM(A1) * 6');
  await univerAPI.getFormula().onCalculationResultApplied();

  console.log(sheet.getRange('B1').getValue()); // 738
  console.log(workbook.save());
} finally {
  univer.dispose();
}
```

The preset registers the core Sheets, formula, data-validation, filter, hyperlink, drawing, sort, and thread-comment plugins plus their Node-safe Facade extensions.

## Formula Worker

Pass a built JavaScript worker path to the preset. `@univerjs/rpc-node` uses `node:child_process.fork()`, not a browser `Worker`.

```ts
// main.ts (ESM)
import { fileURLToPath } from 'node:url';
import { LocaleType } from '@univerjs/core';
import { UniverSheetsNodeCorePreset } from '@univerjs/preset-sheets-node-core';
import UniverSheetsNodeCoreEnUS from '@univerjs/preset-sheets-node-core/locales/en-US';
import { createUniver } from '@univerjs/presets';

const workerSrc = fileURLToPath(new URL('./formula-worker.js', import.meta.url));
const { univer, univerAPI } = createUniver({
  locale: LocaleType.EN_US,
  locales: {
    [LocaleType.EN_US]: UniverSheetsNodeCoreEnUS,
  },
  presets: [UniverSheetsNodeCorePreset({ workerSrc })],
});
```

```ts
// formula-worker.ts; compile it to formula-worker.js before running main.ts
import { LocaleType } from '@univerjs/core';
import { UniverSheetsNodeCoreWorkerPreset } from '@univerjs/preset-sheets-node-core/worker';
import { createUniver } from '@univerjs/presets';

createUniver({
  locale: LocaleType.EN_US,
  presets: [UniverSheetsNodeCoreWorkerPreset()],
});
```

The worker preset includes `UniverRPCNodeWorkerPlugin` and `UniverRemoteSheetsFormulaPlugin`. Do not replace the latter with the main-thread `UniverSheetsFormulaPlugin`.

## Node-Specific Rules

| Concern | Browser | Node.js |
| --- | --- | --- |
| Setup | Browser preset or manual UI plugins | Sheets/Docs Node preset, or a source-verified manual Pro product stack |
| UI | `UniverUIPlugin`, `*-ui`, CSS | Omit |
| RPC main | `UniverRPCMainThreadPlugin` with `workerURL` | `UniverRPCNodeMainPlugin` with `workerSrc` |
| RPC worker | `UniverRPCWorkerThreadPlugin` | `UniverRPCNodeWorkerPlugin` |
| Formula worker bridge | `UniverRemoteSheetsFormulaPlugin` | `UniverRemoteSheetsFormulaPlugin` |
| Theme | Runtime theme and CSS required for UI | Not needed for data-only processing |

### Facade imports

The Sheets Node preset loads its documented Facade side effects. The Docs Node preset loads only the formula Facade; import `@univerjs/docs/facade` before calling `createDocument(...)`. With manual registration, import the Facade entry for every API surface used and exclude `@univerjs/ui/facade` and `*-ui/facade`. Read the [Node plugin registry](references/node-plugin-registry.md) before assembling a manual plugin or Facade list.

## Pro on Node.js

For the six-product Pro Node matrix, exact runtime/Facade stacks, formula and Base workers, model-only chart/shape boundaries, and collaboration, read [Pro Node.js integration](references/node-pro-integration.md).

## References

- [Node plugin registry](references/node-plugin-registry.md) — six-product support matrix, current preset contents, manual plugins, Facade allowlist, worker pairing, and browser-only exclusions
- [Node common tasks](references/node-common-tasks.md) — batch reports, JSON snapshots, formula barriers, custom functions, events, and resource cleanup
- [Pro Node.js integration](references/node-pro-integration.md) — exact six-product Pro stacks, formula/Base workers, collaboration socket adapter, license handling, and current headless limitations
