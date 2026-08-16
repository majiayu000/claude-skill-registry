---
name: univer-plugin-dev
description: Develop custom plugins for Univer sheets, docs, slides, bases, boards, and PDFs. Use when implementing a Plugin lifecycle, dependency injection, commands/mutations/operations, undo/redo, Facade extensions or custom events, toolbar/context-menu items, shortcuts, icons, popups, or when diagnosing plugin API and registration errors.
---

# Univer Plugin Development

Build plugins against the APIs exported by the target application's installed Univer packages.

> **Compatibility**: The checked source baseline is Univer and Univer Pro `1.0.0-beta.0`. Keep release-train packages such as `@univerjs/core`, `@univerjs/sheets`, `@univerjs/ui`, and `@univerjs-pro/*` on that same exact version. Independently versioned packages such as `@univerjs/icons` must follow the target manifest instead. If the target project differs, inspect its manifests and source exports before copying an example.

## Scaffold a Sheet UI plugin

Run the bundled generator:

```bash
npx tsx <skills-repo>/skills/univer-plugin-dev/scripts/scaffold-plugin.ts my-plugin --path ./packages
```

It creates a buildable Sheet UI plugin package. For docs, slides, bases, boards, or PDFs, first choose the product type and official core/UI plugin family in [plugin-architecture.md](references/plugin-architecture.md), then adapt the generated dependencies and `UniverInstanceType`.

```text
my-plugin/
├── src/
│   ├── commands/my-command.ts
│   ├── controllers/menu.controller.ts
│   ├── facade/f-univer.ts
│   ├── index.ts
│   └── plugin.ts
├── package.json
└── tsconfig.json
```

Register the plugin and explicitly load its Facade extension:

```ts
import { UniverMyPlugin } from './packages/my-plugin/src';
import './packages/my-plugin/src/facade/f-univer';

univer.registerPlugin(UniverMyPlugin);
```

When consuming a built package, import its public subpath instead:

```ts
import { UniverMyPlugin } from 'my-plugin';
import 'my-plugin/facade';
```

The scaffold has no stylesheet. Product/preset styles belong to the host; if the plugin adds CSS, publish a CSS entry with a CSS-aware build and require the host to import it. See [ui-customization.md](references/ui-customization.md) for the 1.0 preset/plugin-mode CSS boundary.

## Core rules

### Plugin lifecycle

Extend `Plugin`, provide a unique `pluginName`, choose a `UniverInstanceType`, and inject `Injector` as the protected `_injector` required by the base class. The 1.0 product matrix is sheets, docs, slides, bases, boards, and PDFs; do not copy the Sheet scaffold unchanged for another product.

| Hook | Use it for |
| --- | --- |
| `onStarting()` | Register DI dependencies, commands, menus, shortcuts, icons, and components. Do not read a workbook or the DOM. |
| `onReady()` | Initialize logic that requires a created unit of the plugin's product type. |
| `onRendered()` | Register render modules or other renderer/DOM-dependent logic. |
| `onSteady()` | Start non-critical work after all plugins have rendered. |

Own every disposable subscription, listener, shortcut, command, component, icon, render module, timer, and worker with `disposeWithMe()`. `IMenuManagerService.mergeMenu()` is the notable exception: it currently returns `void`.

Read [plugin-architecture.md](references/plugin-architecture.md) when adding lifecycle logic, DI services, configuration, dependencies, or controllers.

### Command model

- `COMMAND` orchestrates validation and business flow.
- `MUTATION` deterministically changes persisted model state and is the collaboration changeset unit.
- `OPERATION` changes transient UI state.

A mutation is not automatically undoable. Capture undo parameters before executing redo mutations, then push symmetric `undoMutations` and `redoMutations` through `IUndoRedoService` from the command.

Use `executeCommand()` for async execution and `syncExecuteCommand()` only when the full handler chain is synchronous. Both return the handler result directly; there is no `.result` wrapper.

Read [command-system.md](references/command-system.md) before changing persisted data, implementing undo/redo, invoking built-in commands, or listening to command execution.

### Facade extensions

When the target Facade class explicitly exposes static `extend()`, subclass it, call `extend()`, and augment the module that owns the class. Not every public Facade class is a mixin target; check [facade-extension.md](references/facade-extension.md) first.

```ts
import { FWorksheet } from '@univerjs/sheets/facade';

export interface IFWorksheetMyMixin {
    markHeader(color: string): this;
}

export class FWorksheetMyMixin extends FWorksheet implements IFWorksheetMyMixin {
    override markHeader(color: string): this {
        this.getRange(0, 0, 1, this.getMaxColumns()).setBackground(color).setFontWeight('bold');
        return this;
    }
}

FWorksheet.extend(FWorksheetMyMixin);

declare module '@univerjs/sheets/facade' {
    interface FWorksheet extends IFWorksheetMyMixin {}
}
```

Consumers must side-effect import the extension module. Read [facade-extension.md](references/facade-extension.md) when extending `FUniver`, `FWorkbook`, `FWorksheet`, `FRange`, `FDocument`, Pro product Facades such as `FPresentation`, or Facade events.

### UI extensions

Register toolbar and context-menu items by merging a menu schema. A menu item's `id` (or `commandId`) selects the registered command. A shortcut also executes the command whose ID it carries; `IShortcutItem` has no custom handler.

```ts
this._menuManagerService.mergeMenu({
    [RibbonOthersGroup.OTHERS]: {
        [MyCommand.id]: {
            order: 10,
            menuItemFactory: () => ({
                id: MyCommand.id,
                title: 'my-plugin.menu.run',
                type: MenuItemType.BUTTON,
            }),
        },
    },
});
```

Use `IconManager` for icons and `ComponentManager` for React/Vue/custom components. Keep their returned disposables. Read [ui-customization.md](references/ui-customization.md) for current menu nesting, context-menu positions, shortcuts, components, and range popups.

### Events

Prefer typed Facade events through `univerAPI.addEvent()`. Load the owning Facade side-effect module so its event names and parameter types are installed. Filter `ICommandService` listeners by exported command constants when no semantic Facade event exists.

Read [event-system.md](references/event-system.md) for current event names, cancellation, custom events, and cleanup.

## Validation

After generating or editing a plugin:

1. Build or typecheck it against the target project's exact Univer versions.
2. Register it in a minimal app and exercise the command, menu/shortcut, Facade side-effect import, and disposal path.
3. Verify persisted changes round-trip and undo/redo when applicable.
4. Run the skill validator after editing this skill:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/univer-plugin-dev
```
