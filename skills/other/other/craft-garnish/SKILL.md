---
name: craft-garnish
description: "Garnish — Craft CMS's built-in JavaScript UI toolkit for the control panel. Covers the full Garnish surface: class system (Garnish.Base.extend, init, setSettings, addListener, on/off/trigger, destroy), UI widgets (Modal, HUD, DisclosureMenu, MenuBtn, CustomSelect, ContextMenu, Select), drag system (BaseDrag, DragSort, DragDrop, DragMove), form widgets (NiceText, CheckboxSelect, MixedInput, MultiFunctionBtn), utilities (key constants, ARIA helpers, focus management), and Craft integration (GarnishAsset, webpack externals, Craft.* class pattern). Triggers on: Garnish.Base.extend, Garnish.Modal, Garnish.HUD, Garnish.DragSort, Garnish.Select, Garnish.DisclosureMenu, Garnish.MenuBtn, Garnish.CustomSelect, addListener, removeListener, removeAllListeners, Garnish.ESC_KEY, Garnish.RETURN_KEY, activate event, textchange event, UiLayerManager, registerShortcut, trapFocusWithin, garnishjs, GarnishAsset, CpAsset, CP JavaScript, control panel JS, drag and drop, sortable, modal dialog, HUD popover, disclosure menu, menu button, Craft.CP, Craft.Slideout, Craft.ElementEditor, onSortChange, onOptionSelect, onSelectionChange, aria-modal, focus trap, keyboard navigation CP, this.base(), window.Garnish, expose-loader, CP memory leak, event listener cleanup, jQuery .on() in CP, selection interface, multi-select grid. Always use when writing, editing, or reviewing JavaScript that runs in the Craft CMS control panel — including plugin CP assets, custom field type JS, element index JS, CP webpack config, or code that imports garnishjs or references window.Garnish. Also trigger for Craft CP accessibility, keyboard interactions, drag-sort behavior, or CP JS memory issues. Do NOT trigger for front-end JavaScript (Alpine, Vue, htmx) or Twig templates."
---

# Garnish — Craft CMS Control Panel JavaScript Toolkit

Reference for Garnish, Craft CMS's built-in JavaScript UI framework. Covers the class system, UI widgets, drag interactions, form components, accessibility helpers, and integration with Craft's CP.

This skill is scoped to **Garnish itself** — the JavaScript library at `src/web/assets/garnish/`. For PHP-side plugin development (elements, controllers, services), see the `craftcms` skill. For CP template markup that Garnish widgets attach to, see the `craftcms` skill's `cp.md` reference.

## Companion Skills — Load When Needed

- **`craftcms`** — Load when the task involves PHP asset bundle classes, plugin architecture, or CP template markup that Garnish widgets attach to. Skip for pure JavaScript refactoring, Garnish API questions, or JS-only tasks.
- **`craft-php-guidelines`** — Load only when editing PHP files (asset bundle classes, controllers that register JS). Skip for pure JS work.

## Documentation

- Garnish source: `src/web/assets/garnish/src/` in the Craft CMS repository
- No official external documentation exists — this skill IS the documentation.

Use `WebFetch` on Craft's class reference (https://docs.craftcms.com/api/v5/) when looking up PHP-side asset bundle registration.

## Common Pitfalls (Cross-Cutting)

- Using jQuery `.on()` directly instead of `this.addListener()` — listeners added via jQuery won't auto-clean on `destroy()`, causing memory leaks.
- Forgetting `this.base()` when overriding `destroy()` — parent cleanup (listener removal, event teardown) gets skipped.
- Using `click` instead of `activate` event on non-`<button>` elements — `activate` handles both click and keyboard (Space/Enter), making the UI accessible.
- Fighting `UiLayerManager` by binding ESC directly — use `Garnish.uiLayerManager.registerShortcut(Garnish.ESC_KEY, callback)` so escape routes through the layer stack correctly.
- Magic key code numbers instead of `Garnish.ESC_KEY`, `Garnish.RETURN_KEY`, etc. — constants are self-documenting and consistent.
- Instantiating Garnish widgets before the DOM is ready — Garnish requires jQuery and all dependencies loaded first; in plugin assets, rely on `CpAsset` dependency chain.
- Not calling `destroy()` when removing widgets — orphaned listeners accumulate, especially in slideouts and live preview where DOM is repeatedly created/destroyed.
- Importing Garnish into webpack bundles instead of using the external — `import Garnish from 'garnishjs'` resolves to `window.Garnish` via webpack externals; bundling it duplicates 134KB.
- Using deprecated `Garnish.Menu` instead of `Garnish.CustomSelect` — `Menu` is an alias kept for BC only.
- Using deprecated `Garnish.escManager` or `Garnish.shortcutManager` instead of `Garnish.uiLayerManager` — the newer manager provides layer-aware keyboard routing that respects the modal/menu stack.

## Reference Files

Read the relevant reference file(s) for your task. Multiple files often apply together.

**Task examples:**
- "Create a modal dialog in a plugin's CP JS" → read `class-system.md` + `ui-widgets.md`
- "Add drag-to-reorder to a custom field type" → read `drag-system.md` + `class-system.md`
- "Build a custom CP widget class" → read `class-system.md` + `integration.md`
- "Add a disclosure menu to a CP template" → read `ui-widgets.md` + `integration.md`
- "Handle keyboard events in CP JavaScript" → read `utilities.md` + `class-system.md`
- "Create an inline editor HUD" → read `ui-widgets.md` (HUD section)
- "Make a selection interface for elements" → read `ui-widgets.md` (Select section)
- "Set up a plugin's webpack config for Garnish" → read `integration.md`
- "Custom element index class isn't loading" → read `integration.md` (Element Index JS Loading)
- "Load element index JS with Vite" → read `integration.md` (Element Index JS Loading — Vite doesn't work for element index classes)
- "Add ARIA attributes to a custom modal" → read `utilities.md` (ARIA & Focus section)
- "Understand how Craft.CP extends Garnish" → read `integration.md` + `class-system.md`
- "Build a multi-state submit button" → read `integration.md` (Form Widgets section)
- "Add auto-growing textarea behavior" → read `integration.md` (Form Widgets section)

| Reference | Scope |
|-----------|-------|
| `references/class-system.md` | Garnish.Base, inheritance (extend/init/base), events (on/off/trigger), listeners (addListener/removeListener), settings, namespacing, enable/disable, destroy lifecycle |
| `references/ui-widgets.md` | Modal, HUD, DisclosureMenu, MenuBtn, SelectMenu, CustomSelect, ContextMenu, Select — constructor args, settings/defaults, methods, events, ARIA behavior |
| `references/drag-system.md` | BaseDrag, Drag, DragSort, DragDrop, DragMove — class hierarchy, settings/defaults, events, helper system, insertion points, scroll handling |
| `references/utilities.md` | Garnish namespace object, key constants, custom jQuery events (activate, textchange, resize), ARIA/focus management, geometry/hit testing, animation, form helpers, detection |
| `references/integration.md` | GarnishAsset PHP bundle, webpack externals, loading sequence, Craft.* class pattern, Twig JS blocks, form widgets (NiceText, CheckboxSelect, MultiFunctionBtn, MixedInput) |
