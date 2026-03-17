---
name: design-polish
description: >
  Use when a frontend has placeholder assets (data-asset attributes, empty image slots)
  and needs real generated visuals. Triggers: post-implementation polish, preparing for
  demo/launch, replacing placeholder images with AI-generated assets matching a design system.
user-invocable: true
argument-hint: "[spec-file-path] (optional)"
---

# Design Polish (Asset Generation)

Replace placeholder assets in a React frontend with AI-generated visuals that match the project's design system. Uses `nano-banana-pro` for image generation.

## When to Use

- Frontend has `data-asset` placeholder attributes ready for replacement
- Frontend has existing assets that need regeneration (style refresh, audience change)
- Design system (`design-system/MASTER.md`) exists with style/color definitions
- Preparing for demo, launch, or stakeholder review
- Post-implementation visual polish pass

## When NOT to Use

- No frontend UI exists yet
- No design system defined (create one first)
- Need hand-crafted assets (use a designer)

## Inputs

Resolved automatically. Override with `$ARGUMENTS` if provided.

| Input | Auto-Detection | Fallback |
|-------|---------------|----------|
| Project context | `CLAUDE.md` `## Project` section | Warn — prompts will lack audience/product context |
| Spec | `$ARGUMENTS` or `_docs/*spec*`, `**/SPEC.md` | Skip spec-driven inventory, use placeholders only |
| Design system | `design-system/MASTER.md` | **Required** — abort if missing |
| Frontend root | `frontend/src/` | Scan for `src/` with React components |

## Process

### 1. Resolve Inputs

```
Read CLAUDE.md → extract from "## Project" section:
  - product_description (what the app does)
  - target_users (adults, kids, professionals, etc.)
  - product_type (e.g., recipe app, task manager, marketplace)
  If CLAUDE.md or ## Project missing → WARN: "No project context found. Image prompts will lack audience targeting."

If $ARGUMENTS provided → use as spec path
Else → search for _docs/*spec*, **/SPEC.md
Read design-system/MASTER.md → extract style name, mood, palette, aesthetic
Locate frontend source root
```

### 2. Asset Inventory

Build inventory from two sources:

**From spec** (if available):

| Asset Type | Where to Look in Spec |
|------------|----------------------|
| Hero images | "## Solution" + landing page sections |
| Empty states | "## User Flows" — zero-data scenarios |
| Error states | Standard: 404, 500, network error |
| Success states | Features completing actions |
| Marketing | OG image (1200x630), favicon (32/192/512px) |

**From code — placeholders** (always):

Scan frontend source for `data-asset="{type}-{name}"` attributes. Each placeholder maps to an inventory item. Flag any placeholders that do not match a spec-driven inventory item as "unmatched placeholders" in the inventory file.

**From code — existing assets** (always):

Scan for `<img src="/assets/...">` tags in frontend source. Each existing asset is added to inventory with status `existing`. These will be regenerated with the current design system and project context, replacing the old files in-place.

Also scan `frontend/public/assets/` directory. Files present on disk but not referenced by any component are flagged as "orphaned" in the inventory.

Write inventory to `_docs/design-polish/asset-inventory.md`. Each entry has status: `placeholder` | `existing` | `spec-only` | `orphaned` | `minimum` | `enhancement`.

**Minimum required assets — always generate these regardless of placeholders:**

| Asset | Category | Dimensions | Notes |
|-------|----------|------------|-------|
| App logo | `icons/` | 512x512 PNG | Derived from product name + design system aesthetic |
| Landing hero | `heroes/` | 1920x1080 JPG | Main visual — product concept, mood, audience |
| OG image | `marketing/` | 1200x630 JPG | Social sharing — logo + tagline + brand colors |
| Favicon set | `icons/` | 32, 192, 512 PNG | Simplified logo at each size |

If any of these already exist in inventory (from placeholders or existing assets), skip the duplicate. Otherwise add them with status `minimum`. These are generated even if the project has zero placeholders.

**Creative enhancement scan — proactively find opportunities:**

After building the base inventory, scan the frontend for visual enhancement opportunities. Think hard about what would make this product more polished and professional:

```
Walk through each page/route in the frontend:
  - Landing page → does it have a compelling hero? background texture? section dividers?
  - Empty states → "no items yet" screens benefit from friendly illustrations
  - Loading states → could use branded skeleton/spinner graphics
  - Error pages → 404, 500, offline — each deserves a unique illustration
  - About/info pages → team photos, product story illustrations
  - Feature sections → icons or illustrations per feature highlight
  - Onboarding → step illustrations for first-time users
  - Success confirmations → celebratory illustrations (task complete, purchase done)

For each opportunity found:
  - Add to inventory with status `enhancement`
  - Note which component/page it targets
  - Note what visual would improve the UX
```

The enhancement scan uses project context from CLAUDE.md (target audience, product type) to decide what's appropriate. A kids' app needs playful illustrations everywhere; a B2B dashboard needs subtle, professional graphics.

### 3. Generate Assets

For each asset in inventory (`placeholder`, `existing`, `minimum`, and `enhancement` status):

1. Read MASTER.md for style context
2. Read project context from Step 1 (sourced from CLAUDE.md)
3. Construct prompt:
   ```
   "{style_name} aesthetic. {mood_keywords} mood.
    Colors: {palette}.
    Generate: {asset_description}.
    Dimensions: {width}x{height}.
    Format: PNG transparent (illustrations) / JPG (photos).
    Product: {product_description}.
    Target audience: {target_users}.
    Product type: {product_type}."
   ```
3. Invoke `nano-banana-pro` via Skill tool with the prompt
4. Save to `frontend/public/assets/{category}/{filename}`
5. Verify file exists and has expected dimensions
6. Log to `_docs/design-polish/generation-log.md`
7. If fails after 2 retries → mark "manual needed", continue

### 4. Wire Assets to Components

**Placeholders** — for each `data-asset` placeholder found:
- Replace placeholder div with `<img>` tag:
  ```tsx
  <img src="/assets/{category}/{filename}" alt="{description}" className="..." />
  ```

**Existing assets** — no component rewiring needed. The new file overwrites the old at the same path. Verify the `<img>` tag's `alt` text still matches the regenerated content; update if not.

**Minimum/enhancement assets** — wire into the appropriate component:
- Logo → navbar, footer, favicon, OG image
- Landing hero → landing page hero section (create section if missing)
- Enhancement illustrations → add `<img>` tag in the target component noted in inventory

Update `index.html`:
- `<meta property="og:image" content="/assets/marketing/og-image.jpg" />`
- `<link rel="icon" href="/assets/icons/favicon-32.png" />`

### 5. Verify

- Check for remaining placeholders: search for `data-asset=` in frontend source
- If E2E tests exist: run `cd frontend && npx playwright test`
- If E2E fails → debug and fix (up to 2 attempts)

## Asset Directory Structure

```
frontend/public/assets/
├── heroes/
│   └── landing-hero.jpg
├── illustrations/
│   ├── empty-state.png
│   ├── error-state.png
│   └── success-state.png
├── icons/
│   ├── favicon-32.png
│   ├── favicon-192.png
│   └── favicon-512.png
└── marketing/
    └── og-image.jpg
```

## Output

- `_docs/design-polish/asset-inventory.md` — what was planned
- `_docs/design-polish/generation-log.md` — what was generated (with prompts used)
- `frontend/public/assets/` — populated with generated images
- Components updated with real `<img>` tags
- No `data-asset=` placeholders remaining
- Existing assets regenerated with current design system

## Completion Checklist

- [ ] Asset inventory exists at `_docs/design-polish/asset-inventory.md`
- [ ] Generation log exists at `_docs/design-polish/generation-log.md`
- [ ] Minimum assets generated: logo, landing hero, OG image, favicon set
- [ ] All hero images generated (or marked manual)
- [ ] All illustration assets generated (or marked manual)
- [ ] All existing assets regenerated (or marked manual)
- [ ] Enhancement opportunities identified and generated
- [ ] OG image + favicon generated
- [ ] No `data-asset=` placeholders remaining in code
- [ ] E2E tests still pass (if they exist)

## Common Mistakes

- **Generating before reading MASTER.md** — assets won't match the design system. Always extract style context first.
- **Hardcoding asset paths** — use the `{category}/{filename}` convention so paths stay consistent.
- **Skipping failed assets** — mark them "manual needed" in the log, don't silently skip.
- **Only generating what's explicitly placeholdered** — the skill should proactively enhance the product. Few placeholders ≠ few assets needed. Walk every page and think about what visuals would elevate the experience.
- **Ignoring audience context** — a kids' app needs playful, colorful illustrations; a finance dashboard needs subtle, professional graphics. Always read CLAUDE.md for target audience before generating.
