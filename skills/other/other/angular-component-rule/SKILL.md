---
name: angular-component-rule
description: Enforce Angular 20 component companion-file and structure rules across `src/app/**` with deterministic, non-destructive auto-fix behavior. Use when users ask to create/fix missing component companions, enforce one-component-per-file conventions, externalize inline template/styles, remove static `host.class` styling, standardize `.component.variants.ts` extraction, or run CI/component-hygiene audits.
---

# Angular 20 Component File Completeness and Structure Rule

Enforce deterministic component companion files in Angular workspaces.
Auto-fix by creating missing files without overwriting existing files.

## Scope and Matching

Scan only these roots when present:
1. `src/app/**`

Define a component as any file matching `**/*.component.ts`.
Define a variant companion as `**/*.component.variants.ts`.

Exclude:
1. `**/node_modules/**`
2. `**/dist/**`
3. `**/.angular/**`
4. `**/.storybook/**`
5. `**/coverage/**`

## Enforcement Rules

For each `X.component.ts`, require:
1. `X.component.ts`
2. `X.component.html`
3. `X.component.spec.ts`
4. Exactly one accepted style companion:
   `X.component.scss` or `X.component.css` (compatibility rule applies)
5. `X.component.stories.ts` only when Storybook is installed
6. Exactly one Angular component class (`@Component`) per `X.component.ts`
7. Component variants must live in `X.component.variants.ts`, not in `X.component.ts`

Structural constraints:
1. `X.component.ts` must declare exactly one `@Component`-decorated class
2. `X.component.ts` must not declare additional `@Component`, `@Directive`, or `@Pipe` classes
3. Variant unions, variant maps, variant option arrays, and variant class lookup objects must be declared in `X.component.variants.ts`
4. `X.component.ts` may import and use variant exports, but should not define variant constants/types inline except for trivial one-off local values
5. Do not use inline template or inline styles in `@Component` metadata (`template`, `styles`)
6. Do not place static host utility classes in `@Component({ host: { class: '...' } })`; move them to template and/or stylesheet

## Step 1: Determine Environment

Read root `package.json`.
Read root `angular.json` when present.

If either file is missing or unreadable, continue with best-effort fallbacks and record the limitation in the completion report.

Compute and report:
1. `storybookInstalled`
2. preferred style extension `styleExt` (`scss` or `css`)

### Storybook detection

Set `storybookInstalled = true` if any condition is true:
1. `package.json` has `@storybook/angular` in dependencies or devDependencies
2. `.storybook/` exists in workspace root
3. `package.json` scripts include `storybook` or `build-storybook`

Else set `storybookInstalled = false`.

### Style extension detection (`styleExt`)

Resolve in strict priority order.

1. Primary rule: `angular.json`
   1. Check `projects[*].schematics['@schematics/angular:component'].style`
   2. Else check top-level `schematics['@schematics/angular:component'].style`
   3. Else check `projects[*].architect.build.options.inlineStyleLanguage`
   4. If resolved value is `scss`, choose `scss`
   5. If resolved value is `css`, choose `css`
2. Secondary rule: package dependencies
   1. If `sass` exists in dependencies or devDependencies, choose `scss`
   2. Otherwise choose `css`
3. Tertiary rule: repository convention fallback
   1. Compare counts of `*.component.scss` and `*.component.css` in repo scope
   2. If `scss` count is greater, choose `scss`
   3. Otherwise choose `css`

Failure and fallback handling:
1. If `angular.json` is unreadable or malformed, skip primary rule and continue with secondary rule
2. If `package.json` is unreadable or missing, skip package-based Storybook and dependency checks
3. If both primary and secondary style rules are unavailable, run tertiary rule
4. If tertiary counts cannot be computed, default `styleExt = css`

### Compatibility rule

Never force existing components to switch style extension.
1. If `X.component.scss` exists, accept it even when preferred style is `css`
2. If `X.component.css` exists, accept it even when preferred style is `scss`
3. Create a style file only when both are missing, using resolved `styleExt`

### Multi-project rule

If multiple Angular projects use different component style settings, infer component ownership by path using `angular.json` project `root`/`sourceRoot` and prefer per-project style. Fall back to global rules only when ownership or project-level style is not inferable.

## Step 2: Scan and Compute Expected Files

For each `X.component.ts`, compute required companions in the same folder:
1. `X.component.html`
2. `X.component.spec.ts`
3. Style file:
   1. Accept existing `.component.scss` or `.component.css`
   2. If neither exists, require `X.component.<styleExt>`
4. `X.component.stories.ts` when `storybookInstalled` is true

Then validate structure:
1. Count `@Component` decorators in `X.component.ts` and require count = 1
2. Detect variant declarations in `X.component.ts` (for example: `variant`, `size`, `tone`, `intent`, `state` unions or maps) and mark for extraction
3. If variant declarations are present in `X.component.ts`, require `X.component.variants.ts`
4. Detect `@Component.template` and `@Component.styles`; mark as inline violations
5. Detect `@Component.host.class` string literals; mark as host-class-inline violations

If no files match `**/*.component.ts`, produce a completion report with zero counts and no file changes.

## Step 3: Validate and Auto-Fix

Default behavior is auto-fix. Create missing files without overwriting any existing file.

### Create missing template file

Create `X.component.html` with:

```html
<div class="component">
  <!-- TODO: implement template -->
</div>
```

### Create missing style file

If resolved extension is `scss`, create:

```scss
:host {
  display: block;
}
```

If resolved extension is `css`, create:

```css
:host {
  display: block;
}
```

### Create missing spec file

Create a minimal TestBed test that compiles and asserts `should create`.
Prefer a standalone-friendly template first:

```ts
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExampleComponent } from './example.component';

describe('ExampleComponent', () => {
  let component: ExampleComponent;
  let fixture: ComponentFixture<ExampleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExampleComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ExampleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
```

If constructor dependencies or non-standalone setup break compilation, do not invent mocks. Add a TODO comment indicating missing providers/imports to be filled intentionally.

### Create missing story file (only when Storybook is installed)

Create `X.component.stories.ts` with minimal story metadata:

```ts
import type { Meta, StoryObj } from '@storybook/angular';

import { ExampleComponent } from './example.component';

const meta: Meta<ExampleComponent> = {
  title: 'Components/Example',
  component: ExampleComponent,
};

export default meta;
type Story = StoryObj<ExampleComponent>;

export const Default: Story = {
  args: {},
};
```

Detect obvious `@Input` values only as an optional enhancement. Default to empty `args`.

### Enforce one component per `.component.ts`

If more than one `@Component` class is found in a single file:
1. Do not auto-split classes blindly
2. Report file as unfixable automatically
3. Provide targeted follow-up action:
   1. Keep one component class in `X.component.ts`
   2. Move each additional component into its own `Y.component.ts` with companions

### Enforce variants in separate TypeScript file

If component variants are defined inline in `X.component.ts`:
1. Create `X.component.variants.ts` when missing
2. Move variant-related types/constants/helpers into `X.component.variants.ts`
3. Update `X.component.ts` imports to consume moved exports
4. Preserve runtime behavior and public API names
5. If safe automated extraction is ambiguous, do not rewrite; report as manual follow-up

When creating `X.component.variants.ts`, use this skeleton:

```ts
export type ExampleVariant = 'default';

export const EXAMPLE_VARIANTS = {
  default: '',
} as const;
```

### Enforce no inline template/styles and no inline host class strings

For `X.component.ts`, enforce:
1. `templateUrl` must be used instead of `template`
2. `styleUrl`/`styleUrls` must be used instead of `styles`
3. Static class strings in `host.class` must not be used for styling distribution

Auto-fix policy:
1. If `template` is inline and `X.component.html` is missing, create `X.component.html` with inline content and switch metadata to `templateUrl`
2. If `styles` is inline and style companion is missing, create `X.component.<styleExt>` with inline content and switch metadata to `styleUrl`
3. If `host.class` contains static classes, move classes to:
   1. Root element in `X.component.html` when a stable root exists
   2. `:host` in `X.component.<styleExt>` when classes map to host-level behavior
4. Remove migrated inline metadata after successful move
5. If safe migration target is ambiguous, do not rewrite; report manual follow-up with exact location

If host-class migration is ambiguous, keep behavior unchanged and include the exact metadata path and a one-step manual recommendation.

## Step 4: Non-Destructive Guarantees

1. Never overwrite files
2. Never delete files
3. Never rename files
4. Inline metadata migration is allowed only for safe, deterministic conversions (`template` -> `templateUrl`, `styles` -> `styleUrl`/`styleUrls`, `host.class` extraction). Otherwise report as manual follow-up.

## Required Completion Report

Always output:
1. Storybook detection result (`installed` or `not installed`) plus reason
2. Style enforcement decision (`css` or `scss`) plus reason
3. Total components scanned
4. Missing-file summary by type
5. Created files with full paths
6. Skipped or unfixable items with reasons
7. Structural violations found:
   1. Files with multiple `@Component` classes
   2. Files with inline variant declarations
   3. Variant files created or updated
8. Inline-metadata violations found:
   1. Files using inline `template`
   2. Files using inline `styles`
   3. Files using static `host.class` strings
9. Environment limitations and fallback paths used:
   1. Missing or unreadable config files
   2. Any fallback rule selected because of parse/read failures

## Verification Gates

Before finalizing, verify these gates:
1. Every `*.component.ts` in scope has required companions or is listed as skipped/unfixable
2. No existing file was overwritten, deleted, or renamed
3. Style companion decisions obey compatibility and per-project ownership rules
4. Story files were created only when Storybook detection is `true`
5. Any structural rewrite performed (`template`/`styles` extraction, variant extraction) is deterministic and behavior-preserving, otherwise reported as manual follow-up
6. Required completion report is fully populated with concrete counts and paths (not placeholders)

## Assistant Portability Rules

1. Use deterministic, file-system-based checks and avoid assumptions about specific editors or IDE integrations.
2. Keep auto-fix behavior non-destructive and idempotent across repeated runs.
3. If a safe rewrite cannot be proven, skip mutation and report an exact manual action with file path.

## Edge Cases

1. Component has neither `.css` nor `.scss`
   Create exactly one style file using `styleExt`
2. Component already has `.css` but preferred style is `scss`
   Accept existing `.css`; do not create `.scss`
3. Component already has `.scss` but preferred style is `css`
   Accept existing `.scss`; do not create `.css`
4. Multiple `@Component` classes in one file
   Do not perform unsafe split automatically; report required manual split plan
5. Variants declared inline in `X.component.ts`
   Extract to `X.component.variants.ts` when safe; otherwise report exact declarations requiring manual extraction
6. Component metadata uses `host.class` with Tailwind utility string
   Treat as violation; migrate classes to `X.component.html` root or `:host` in `X.component.<styleExt>`
7. Existing inline template/styles in legacy components
   Convert to external companion files when safe; otherwise report with explicit manual conversion steps

## References

[1]: https://angular.dev/style-guide
[2]: https://angular.dev/guide/components
[3]: https://storybook.js.org/docs/get-started/frameworks/angular
