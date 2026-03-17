---
name: figma-lucide-angular-bridge
description: Bridge Figma-to-Angular icon delivery by converting only high-confidence Lucide candidates to existing `lucide-angular` patterns, while keeping non-Lucide or unresolved icons on the normal asset path. Use when requests include Figma URL/file-key/node-id implementation, Lucide SVG replacement, icon package reuse, or bundle-safe conversion without installing new packages.
---

# Figma Lucide Angular Bridge

## Goal

Prefer `lucide-angular` for Lucide icons during Figma implementation and avoid downloading duplicate icon assets.

## Trigger Signals

Use this skill when the request includes one or more of:
- Implementing UI from Figma in Angular
- Converting downloaded Lucide SVGs to `lucide-angular`
- Replacing icon assets with package-based Lucide components
- Keeping icon delivery bundle-safe while reusing existing project dependencies
- Reusing an already-installed icon package instead of asset downloads

## Workflow

### 1. Confirm context

- Use this skill only when implementing UI from Figma context in an Angular project.
- Treat any of the following as valid Figma context evidence: Figma URL/file key/node-id, Figma MCP tool output, or explicit "implement this Figma design/node" request.
- Read `package.json` first.
- Continue with Lucide bridging only if `lucide-angular` exists in `dependencies` or `devDependencies`.
- If `lucide-angular` is not installed, skip substitution and continue standard asset workflow without package changes.
- If `package.json` is missing or unreadable, treat package status as unknown and keep standard asset workflow (`package_missing` fallback reason).
- If the request is not Figma-driven implementation work, skip this skill.

### 2. Detect Lucide icons in Figma output

Treat an icon as Lucide when at least one is true:

- Node/layer/component name includes `lucide`, `icon/lucide`, or `lucide:`.
- Asset or export name matches known Lucide naming patterns (for example `chevron-left`, `circle-check`, `arrow-up-right`).
- Existing project code already maps the same semantic icon name to a Lucide import.

If confidence is low, keep the asset workflow for that icon.

Confidence rule:
- High confidence: at least 2 Lucide indicators match -> candidate for `lucide-angular`.
- Low confidence: fewer than 2 indicators -> keep original asset.

Apply confidence scoring per icon, not per screen.

### 3. Resolve each icon with deterministic decision order

Run the following sequence per icon:

1. Scope gate: if icon is clearly non-Lucide (brand mark, illustration, photo), keep normal asset path.
2. Package gate: if `lucide-angular` is absent, keep normal asset path.
3. Confidence gate: if fewer than 2 Lucide indicators match, keep normal asset path.
4. Mapping gate: if a Lucide export resolves confidently and exists in `lucide-angular`, use `lucide-angular`.
5. Fallback gate: if export cannot be resolved confidently, keep normal asset path for that icon only.

Do not stop processing remaining icons when one icon falls back.

### 4. Map Figma icon names to Lucide exports

Normalize the name before mapping:

1. Remove vendor prefixes/suffixes like `lucide:`, `icon/`, `.svg`.
2. Convert separators (`-`, `_`, space, `/`) to word boundaries.
3. Convert to PascalCase for export names.

Examples:

- `chevron-left` -> `ChevronLeft`
- `circle_check` -> `CircleCheck`
- `arrow up right` -> `ArrowUpRight`

Resolution order:
1. Prefer an existing project mapping already used in the codebase.
2. Otherwise use normalized PascalCase export candidate.
3. Verify export availability from actual `lucide-angular` exports (for example local typings/index exports, existing imports in project code, or local package metadata).
4. If export availability cannot be verified locally with confidence, fall back to asset for that icon only (`unresolved_export`).

### 5. Implement with `lucide-angular` instead of asset files

Do not download Lucide icon SVG/image assets when mapped successfully.

For standalone components:

```ts
import { LucideAngularModule, ChevronLeft } from 'lucide-angular';

@Component({
  standalone: true,
  imports: [LucideAngularModule],
})
export class ExampleComponent {
  readonly ChevronLeftIcon = ChevronLeft;
}
```

```html
<lucide-icon [img]="ChevronLeftIcon" aria-label="Back"></lucide-icon>
```

For NgModule-based usage:

```ts
import { LucideAngularModule, ChevronLeft } from 'lucide-angular';

@NgModule({
  imports: [LucideAngularModule.pick({ ChevronLeft })],
})
export class ExampleModule {}
```

```html
<lucide-icon name="chevron-left" aria-label="Back"></lucide-icon>
```

Convention rule:
- Preserve the existing project convention when one pattern dominates (for example `[img]` binding or `name` usage).
- Do not introduce a mixed icon pattern in the same file unless the file already mixes patterns.
- Do not switch conventions globally as part of this skill.
- Keep template tag convention consistent too (`lucide-icon`, `lucide-angular`, `i-lucide`, or `span-lucide`) unless the file already mixes tags.

### 6. Keep non-Lucide assets on standard path

- Continue normal Figma asset download for photos, illustrations, brand logos, and non-Lucide iconography.
- Apply this substitution only to icons confidently identified as Lucide.

### 7. Report deterministic substitution results

Final response should include a concise conversion summary:

- Converted icons: list icon names mapped to Lucide exports.
- Fallback icons: list names kept as assets with reason (`low_confidence`, `unresolved_export`, `package_missing`, `non_lucide_asset`).
- Convention used: `[img]` or `name` pattern, based on existing project usage.

## Guardrails

- Never install a new icon package from this skill; it only reuses existing `lucide-angular` installations.
- Never bulk-import all Lucide icons.
- Prefer explicit icon imports and minimal registration.
- Preserve existing project conventions and Angular architecture.
- If a requested icon is not available in Lucide, use the original Figma asset for that icon.
- Do not rewrite unrelated assets, styles, layout, or component structure while applying icon substitution.
- Do not rename unrelated symbols or refactor unrelated files.
- Do not introduce new dependencies, codemods, or repo-wide icon migrations from this skill.

## Self-check Before Final Output

- `package.json` was checked for `lucide-angular`.
- Per-icon decision order was applied (`scope -> package -> confidence -> mapping -> fallback`).
- Only high-confidence Lucide icons were substituted.
- Non-Lucide assets stayed on normal asset path.
- No bulk icon import pattern was introduced.
- Accessibility labels remained intact for icon usage.
- Fallback behavior is explicit for unmapped or missing Lucide exports.
- Final response contains converted and fallback icon lists with explicit fallback reasons.
- Existing icon usage convention was preserved.

## Assistant-Portability Notes

- Keep instructions tool-agnostic: apply the same gates whether the workflow runs in Codex, Cursor, Copilot, or manual implementation.
- If helper tooling differs, preserve the same per-icon decision order and fallback reasons.
- Prefer minimal, local edits over framework-wide refactors.

## Outcome

Angular implementations from Figma use `lucide-angular` for Lucide icons, reduce duplicated SVG assets, and stay consistent with project icon conventions.
