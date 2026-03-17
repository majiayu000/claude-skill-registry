---
name: angular-lucide-icons-setup
description: Install, repair, or verify `lucide-angular` wiring in Angular 20 workspaces with deterministic checks, minimal-icon registration, template integration, and build/test verification. Use when users ask to add Lucide icons, fix broken Lucide usage, migrate icon setup between standalone and NgModule apps, or validate bundle-safe icon registration.
---

# Angular Lucide Icons Setup

## Goal

Set up `lucide-angular` in an Angular 20 workspace so icons render correctly while keeping bundle impact low by registering only required icons.

## Inputs

- `projectRoot` (string, default: current working directory)
- `targetMode` (`standalone` | `ngmodule` | `auto`, default: `auto`)
- `icons` (array of icon names in PascalCase, default: `['House', 'Menu', 'User', 'File']`)
- `runVerification` (boolean, default: `true`)

## Success Criteria

- `lucide-angular` is installed with the repo package manager.
- Workspace Angular major version is `20`.
- Registration follows the detected app architecture:
  - NgModule app uses `LucideAngularModule.pick({...})` in module imports.
  - Standalone app imports `LucideAngularModule` and binds icon objects via `[img]`.
- At least one icon is rendered in a template.
- Build/test complete without Lucide-related errors.

## Workflow

### 1. Validate workspace and prerequisites

- Confirm `angular.json` and `package.json` exist in `projectRoot`.
- Read `package.json` and verify `@angular/core` major version is `20`.
- Abort with a clear reason if workspace validation fails.

### 2. Determine package manager and app mode

- Detect package manager from lock files:
  - `pnpm-lock.yaml` -> `pnpm`
  - `yarn.lock` -> `yarn`
  - otherwise -> `npm`
- Resolve `targetMode`:
  - If input is `standalone` or `ngmodule`, honor it.
  - If `auto`, detect from app bootstrap/module structure.

### 3. Install `lucide-angular`

Run in `projectRoot` using the detected package manager:

```bash
npm install lucide-angular
```

Equivalent commands:

```bash
pnpm add lucide-angular
yarn add lucide-angular
```

### 4. Integrate for NgModule mode

Use `LucideAngularModule.pick` with explicit icons in the root or feature module where icons are needed:

```ts
import { NgModule } from '@angular/core';
import { LucideAngularModule, House, Menu, User, File } from 'lucide-angular';

@NgModule({
  imports: [
    LucideAngularModule.pick({ House, Menu, User, File }),
  ],
})
export class AppModule {}
```

Template usage (name-based):

```html
<lucide-icon name="house"></lucide-icon>
<lucide-icon name="menu"></lucide-icon>
```

### 5. Integrate for standalone mode

Import `LucideAngularModule` in the standalone component and bind icon objects to `[img]`:

```ts
import { Component } from '@angular/core';
import { LucideAngularModule, House } from 'lucide-angular';

@Component({
  standalone: true,
  selector: 'app-root',
  imports: [LucideAngularModule],
  templateUrl: './app.component.html',
})
export class AppComponent {
  readonly houseIcon = House;
}
```

Template usage (object-based):

```html
<lucide-icon [img]="houseIcon"></lucide-icon>
```

### 6. Apply accessibility and styling defaults

- Use `size`, `color`, and `strokeWidth` inputs where required by design.
- Add `aria-label` for meaningful icons.
- Treat decorative icons as hidden from assistive tech.

Example:

```html
<lucide-icon
  [img]="houseIcon"
  [size]="20"
  color="#0f172a"
  aria-label="Home"
></lucide-icon>
```

### 7. Verify and report

If `runVerification` is `true`:

- Run build (`npm run build` or package-manager equivalent).
- If a start/serve script exists, run it and confirm icon rendering.
- If tests exist, run tests and confirm no regressions.

Report:

- Files changed
- Icons registered
- Mode selected (`standalone`/`ngmodule`)
- Verification command outcomes

## Guardrails

- Do not register all icons unless explicitly requested.
- If user requests all icons, warn about bundle-size impact before applying.
- Merge with existing imports/declarations/providers; avoid destructive rewrites.
- Preserve project style and formatting conventions.
- Re-running should be idempotent: avoid duplicate imports, duplicate template snippets, or duplicate module registration.

## References

- Lucide Angular Guide: `https://lucide.dev/guide/packages/lucide-angular`
- lucide-angular npm package: `https://www.npmjs.com/package/lucide-angular`
- Angular Workspace Configuration: `https://angular.dev/reference/configs/workspace-config`
