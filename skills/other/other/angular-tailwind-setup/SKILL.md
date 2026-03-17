---

name: angular-tailwind-setup
description: Install, repair, or verify Tailwind CSS v4 in existing Angular 20 workspaces with deterministic PostCSS setup, stylesheet wiring, optional dark-mode class toggling, optional preflight exclusion, and build verification. Use when users ask to set up Tailwind, fix broken Tailwind/PostCSS, migrate v3-style directives to v4 (`@import "tailwindcss"`), or validate dark mode/preflight behavior.
---

# Angular 20 Tailwind v4 Installation

## Goal

Install, configure, and verify Tailwind CSS v4 in an existing Angular 20 project so Tailwind utility classes work immediately in components.

## Inputs

* `projectRoot` (string, default: current working directory)
* `useScss` (boolean, default: auto-detect from `angular.json`)
* `enableDarkMode` (boolean, default: `true`)

  * Tailwind v4 defaults to `prefers-color-scheme`; when `true` we also enable **manual class toggling** via a `@custom-variant dark ...` rule (optional but usually desired).
* `enablePreflight` (boolean, default: `true`)
* `addExamples` (boolean, default: `false`) -> add visible demo markup/styles
* `preferPostcssConfigFile` (boolean, default: `true`) -> use separate PostCSS config (prefer `postcss.config.mjs`)

## Success Criteria

* `tailwindcss`, `@tailwindcss/postcss`, and `postcss` exist as `devDependencies`. ([tailwindcss.com][1])
* PostCSS is configured to run `@tailwindcss/postcss`. ([tailwindcss.com][1])
* Global styles import Tailwind using `@import "tailwindcss";` (v4 style). ([tailwindcss.com][2])
* Build runs without Tailwind or PostCSS errors.
* A visible verification example confirms Tailwind styling is applied.

---

## Workflow

### 1) Validate project

* Check whether `angular.json` exists.
* Read `package.json` and check `@angular/core` major version.
* If major is not `20`, abort with an error.
* Detect the global stylesheet path from `angular.json` (do not assume `src/styles.*`).

### 2) Ensure dependencies (Tailwind v4)

Run in `projectRoot`:

* `npm i -D tailwindcss @tailwindcss/postcss postcss` ([tailwindcss.com][1])

Notes:

* In v4, the PostCSS plugin is **not** `tailwindcss` anymore; it lives in `@tailwindcss/postcss`. ([tailwindcss.com][3])
* `autoprefixer` is typically **not required** in v4 (Tailwind handles prefixing internally). Remove it only if present and you're sure nothing else depends on it. ([tailwindcss.com][3])

If packages already exist, do not force reinstall.
If one or more required packages are missing, install only the missing package set in a single deterministic command.

### 3) Tailwind configuration (v4 default: minimal)

Tailwind v4 is "zero-config" by default (content detection is automatic), so **do not create** `tailwind.config.*` unless you actually need custom theme/plugins/safelists/etc. ([tailwindcss.com][2])

#### If you DO need a JS config file (optional)

* Create `tailwind.config.js` (or update minimally).
* Keep it focused on `theme.extend` and `plugins`.
* **Do not rely on it being auto-detected** in v4; you must load it explicitly from CSS using `@config`. ([tailwindcss.com][3])
* Avoid `corePlugins`, `safelist`, and `separator` - these JS config options aren't supported in v4. ([tailwindcss.com][3])

Example (only if needed):

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: { extend: {} },
  plugins: [],
};
```

### 4) Configure PostCSS (v4)

If `preferPostcssConfigFile = true`, prefer an ESM config file:

**`postcss.config.mjs`** ([tailwindcss.com][1])

```js
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

If your repo is CommonJS-only and Angular tooling won't pick up `.mjs`, you can use **`postcss.config.js`**:

```js
module.exports = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

Guardrail: Merge existing PostCSS configuration instead of overwriting.
Guardrail: If both `postcss.config.js` and `postcss.config.mjs` exist, preserve the file currently used by the repository and update only that file.

### 5) Wire global styles (Tailwind v4 import)

Find the global style file from `angular.json` (e.g. `src/styles.scss` or `src/styles.css`) and add Tailwind.

#### If `enablePreflight = true` (default)

Add at the top-level of the global stylesheet:

```css
@import "tailwindcss";
```

Tailwind v4 replaces the old `@tailwind base/components/utilities` directives with a single import. ([tailwindcss.com][2])

#### If `enablePreflight = false`

Do **not** use `corePlugins.preflight = false` (not supported in v4). ([tailwindcss.com][3])
Instead, import Tailwind pieces **without** Preflight:

```css
@layer theme, base, components, utilities;
@import "tailwindcss/theme.css" layer(theme);
@import "tailwindcss/utilities.css" layer(utilities);
```

This omits `tailwindcss/preflight.css`. ([tailwindcss.com][4])

### 6) Optional: enable manual dark-mode toggling (class-based)

Tailwind v4's `dark:` variant defaults to system preference; if you want "toggle by adding `.dark` to `<html>`", add this near the top of the same global stylesheet (right after the Tailwind import):

```css
@custom-variant dark (&:where(.dark, .dark *));
```

Then you can toggle by adding/removing `class="dark"` on `<html>` (or `<body>`). (This is a v4 CSS-first approach; it replaces `darkMode: 'class'` from v3-era configs.) ([tailwindcss.com][5])

### 7) Optional: load a Tailwind JS config via CSS bridge

If you created/kept `tailwind.config.js`, load it explicitly in the global stylesheet:

```css
@config "../tailwind.config.js";
```

Adjust the relative path based on where your stylesheet lives. JS configs are not detected automatically in v4. ([tailwindcss.com][3])

### 8) Check builder briefly

* Ensure the project uses a standard Angular CLI builder.
* Do not modify exotic/custom builders unless explicitly requested.
* If builder customization blocks Tailwind injection, stop and report the exact blocker instead of guessing.

### 9) Run verification

* Run `npm run build`; optionally `npm start`.
* Verify:

  * no Tailwind/PostCSS errors
  * visible utility classes in rendered output
* If build fails, report the first concrete error and the file requiring remediation.

### 10) Report completion

Return a concise completion report including:
* dependency status (`tailwindcss`, `@tailwindcss/postcss`, `postcss`)
* PostCSS config file used and whether it was created or merged
* global stylesheet path updated
* whether `@custom-variant dark ...` was added
* whether preflight is enabled or intentionally excluded
* verification outcome (`build` pass/fail and reason)

---

## Output Artifacts

* `postcss.config.mjs` (preferred) or `postcss.config.js` (new or merged)
* global style file (`src/styles.css` or `src/styles.scss`) updated with:

  * `@import "tailwindcss";` (or selective imports if preflight disabled)
  * optional `@custom-variant dark ...` for class-based toggling
  * optional `@config ...` if using a JS config
* optional `tailwind.config.js` only when needed (plugins/theme extension)
* optional demo markup in `app.component.html` or a demo component
* short completion summary with:

  * what was installed
  * which file contains Tailwind import
  * whether manual dark mode is enabled (and how to toggle)

---

## Guardrails

* If `src/styles.*` is missing:

  * create it and register it in `angular.json > build.options.styles` only when unambiguous.
* For Nx/monorepo projects:

  * prefer relying on v4 automatic source detection first; only add explicit sources when clearly needed.
* If Tailwind is already installed:

  * avoid duplicates and extend existing configuration minimally.
* Avoid deleting `autoprefixer` if other tooling depends on it; Tailwind v4 doesn't require it, but your project might. ([tailwindcss.com][3])

## Assistant Portability Rules

* Use workspace-relative file paths in reports and avoid editor-specific assumptions.
* Apply idempotent edits only to Tailwind/PostCSS wiring; preserve unrelated build tooling unless the user requests wider changes.
* When setup is blocked, report one precise blocker with the exact file and expected value.

[1]: https://tailwindcss.com/docs/installation/using-postcss "Installing Tailwind CSS with PostCSS - Tailwind CSS"
[2]: https://tailwindcss.com/blog/tailwindcss-v4 "Tailwind CSS v4.0 - Tailwind CSS"
[3]: https://tailwindcss.com/docs/upgrade-guide "Upgrade guide - Getting started - Tailwind CSS"
[4]: https://tailwindcss.com/docs/preflight "Preflight - Base styles - Tailwind CSS"
[5]: https://tailwindcss.com/docs/functions-and-directives "Functions and directives - Core concepts - Tailwind CSS"
