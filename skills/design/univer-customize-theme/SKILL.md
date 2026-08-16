---
name: univer-customize-theme
description: Customize Univer color themes, branded palettes, dark mode, and theme-aware plugin styles across Sheets, Docs, Slides, Bases, Boards, and PDFs. Use when setting an initial or runtime Theme, consuming ThemeService or --univer-* CSS variables, keeping custom UI or canvas code theme-aware, registering a separate Univer Pro chart theme, or migrating theme code from Univer 0.25.0 to current 1.0 source.
---

# Univer Customize Theme

Build and apply a complete Univer theme without bypassing the public Facade or runtime theme service.

> **Source baseline**: current Univer OSS and Pro source, whose manifests identify as `1.0.0-beta.0`. Inspect the target application's installed declarations first: the npm release with the same version label can lag the current source API.

## Workflow

1. Decide whether the request concerns the application palette, dark mode, plugin styling, or a Pro Chart theme. These are separate contracts.
2. Inspect the exact installed version and integration mode. Presets compose plugins and Facade extensions; Plugin Mode requires explicit plugin and `/facade` imports.
3. Derive a complete `Theme` from a built-in theme. Do not hand-write or cast a partial object.
4. Pass the initial theme to `createUniver`. Use current `FUniver` theme methods only when they exist in the target declarations.
5. Read live colors through `ThemeService` in plugin/render code and through `--univer-*` variables in browser CSS.
6. Verify light and dark appearances in every enabled product host.

## Build a complete brand palette

Import from the owning package and keep it on the target application's exact Univer version:

```ts
import type { Theme } from '@univerjs/themes';
import { defaultTheme } from '@univerjs/themes';

export const brandTheme: Theme = {
  ...defaultTheme,
  primary: {
    ...defaultTheme.primary,
    50: '#F5F3FF',
    100: '#EDE9FE',
    200: '#DDD6FE',
    300: '#C4B5FD',
    400: '#A78BFA',
    500: '#8B5CF6',
    600: '#7C3AED',
    700: '#6D28D9',
    800: '#5B21B6',
    900: '#4C1D95',
  },
};
```

The current source schema also contains `gray`, semantic color ramps, `loop-color`, and `highlight.background`. Preserve every branch unless the design intentionally replaces it. See [Theme API and migration](references/theme-api.md) for the schema, built-ins, and release gate.

## Apply the theme

Add the initial theme to the existing `createUniver` configuration. Keep that integration's locale, preset, container, and explicit stylesheet imports unchanged:

```ts
const { univer, univerAPI } = createUniver({
  locale: LocaleType.EN_US,
  locales,
  presets,
  theme: brandTheme,
  darkMode: false,
});
```

Current source supports runtime changes through the base Facade:

```ts
univerAPI.setTheme(brandTheme);
univerAPI.toggleDarkMode(true);

const currentTheme = univerAPI.getCurrentTheme();
const darkMode = univerAPI.isDarkMode();
```

Theme selection and dark mode are independent. `setTheme()` does not toggle dark mode, and `toggleDarkMode()` does not replace the palette.

Preset Mode constructs the base Facade. In manual Plugin Mode, construct it from the public core entry after registering plugins:

```ts
import { FUniver } from '@univerjs/core/facade';

const univerAPI = FUniver.newAPI(univer);
```

There is no `@univerjs/themes/facade` package. If installed `FUniver` declarations lack `setTheme()`, `getCurrentTheme()`, or `isDarkMode()`, configure the complete theme during initialization or upgrade; do not reach through `univer.__getInjector()`.

## Make custom code theme-aware

For custom DOM, use variables injected by the UI workbench:

```css
.brand-action {
  color: var(--univer-gray-0);
  background: var(--univer-primary-600);
  border-color: var(--univer-primary-700);
}
```

For plugin services, canvas rendering, and model code, inject `ThemeService` and resolve the live token instead of importing a built-in palette as runtime state:

```ts
import { Inject, ThemeService } from '@univerjs/core';

export class SelectionColorProvider {
  constructor(
    @Inject(ThemeService) private readonly _themeService: ThemeService
  ) {}

  getColor(): string {
    return this._themeService.getColorFromTheme('primary.600');
  }
}
```

Observe `currentTheme$` or `darkMode$` when caching derived colors, and release subscriptions with the owner lifecycle. Headless runtimes have `ThemeService` but do not inject browser CSS variables.

## Six products and Pro Charts

One Univer runtime shares its core `ThemeService` across Sheets, Docs, Slides, Bases, Boards, and PDFs. Theme setup does not register product plugins, load locales, or load CSS. Preserve the aggregate preset CSS or every selected Plugin Mode stylesheet.

Slides, Boards, PDF tables, Sheet ranges, and Pro Charts also have content-level theme/style systems. They do not use the same contract as the application palette. Read [Products and Pro themes](references/products-and-pro.md) before changing content or chart colors.

## Browser-global boundary

The current UI workbench writes flattened variables to one `:root` style element and toggles `univer-dark` on `document.documentElement`. Multiple browser UI instances in one document therefore do not have isolated CSS palettes or dark-mode classes; the latest document-level update wins. Current disposal also does not restore the previous document-level style or root class. Use one shared appearance or isolate editors in separate documents such as iframes; do not promise that `univer.dispose()` restores the host page appearance.

## Validate

- Confirm all Univer packages use the target application's exact release.
- Typecheck the complete `Theme`; do not cast a partial object.
- Verify required preset/plugin styles still load.
- Exercise initial theme setup and any supported runtime switch after the workbench mounts.
- Inspect DOM UI and canvas content in light and dark mode.
- Test every enabled product host and Pro Charts separately.
- Check contrast for text, focus, selection, error, and disabled states.

## Avoid

- Do not mutate a built-in theme object; copy it with nested spreads.
- Do not mutate `document.head` or instantiate `ThemeSwitcherService` yourself.
- Do not override generated `--univer-*` values as the source of truth; the next theme emission replaces them.
- Do not read live runtime colors from `defaultTheme` inside a plugin.
- Do not assume changing the application theme rewrites persisted product content colors.
- Do not migrate `0.25.0` code by changing version strings only; the schema, built-ins, and Facade surface changed.

## References

- [Theme API and migration](references/theme-api.md) — exact schema, built-ins, Facade/ThemeService APIs, CSS flattening, dark mode, release gate, and `0.25.0` differences
- [Products and Pro themes](references/products-and-pro.md) — six-product behavior, CSS ownership, product content themes, and the independent Pro Chart theme API
