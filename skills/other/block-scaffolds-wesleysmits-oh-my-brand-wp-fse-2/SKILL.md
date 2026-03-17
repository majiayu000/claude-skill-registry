---
name: block-scaffolds
description: Copy-paste scaffolds for Oh My Brand! blocks. Templates for block.json, render.php, helpers.php, view.ts, style.css, and tests. Use when creating new blocks.
metadata:
  author: Wesley Smits
  version: "1.0.0"
---

# Block Scaffolds

Ready-to-use templates for creating new blocks in the Oh My Brand! FSE theme.

## When to Use

- Creating a new native WordPress block
- Creating a new ACF block
- Starting test files for blocks
- Quick copy-paste for block files

## Placeholders

Replace these placeholders in all templates:

| Placeholder | Replace With | Example |
|-------------|--------------|---------|
| `BLOCK_NAME` | kebab-case name | `gallery`, `hero-section` |
| `BLOCK_TITLE` | Human-readable title | `Gallery Carousel` |
| `BLOCK_CLASS` | PascalCase class | `GalleryCarousel` |
| `BLOCK_DESCRIPTION` | Short description | `Image gallery with carousel` |
| `CATEGORY` | Block category | `media`, `text`, `design` |
| `ICON` | Dashicon name | `format-gallery`, `admin-home` |
| `FIELD_NAME` | ACF field name | `gallery_images` |

## Native Block Scaffolds

For blocks built with `@wordpress/scripts` in `src/blocks/`:

| File | Template | Purpose |
|------|----------|---------|
| `block.json` | [block-json-native.json](references/block-json-native.json) | Block metadata |
| `render.php` | [render-native.php](references/render-native.php) | Server-side render |
| `helpers.php` | [helpers-native.php](references/helpers-native.php) | Helper functions |
| `view.ts` | [view.ts](references/view.ts) | Frontend Web Component |
| `style.css` | [style.css](references/style.css) | Frontend styles |
| `edit.tsx` | [edit.tsx](references/edit.tsx) | Editor component |

## ACF Block Scaffolds

For ACF PRO blocks in `blocks/acf-{name}/`:

| File | Template | Purpose |
|------|----------|---------|
| `block.json` | [block-json-acf.json](references/block-json-acf.json) | ACF block metadata |
| `render.php` | [render-acf.php](references/render-acf.php) | Render template |
| `helpers.php` | [helpers-acf.php](references/helpers-acf.php) | Helper functions |

## Test Scaffolds

| File | Template | Purpose |
|------|----------|---------|
| `view.test.ts` | [view.test.ts](references/view.test.ts) | Vitest Web Component tests |
| `HelpersTest.php` | [helpers.test.php](references/helpers.test.php) | PHPUnit helper tests |

## Quick Start

### Native Block

```bash
# 1. Create directory
mkdir -p src/blocks/my-block

# 2. Copy templates from references/
# 3. Replace placeholders
# 4. Build: pnpm run build
```

### ACF Block

```bash
# 1. Create directory
mkdir -p blocks/acf-my-block

# 2. Copy templates from references/
# 3. Replace placeholders
# 4. Create field group in WP Admin > ACF
# 5. Register in functions.php $acf_blocks array
```

## Related Skills

- [native-block-development](../native-block-development/SKILL.md) - Block structure guide
- [acf-block-registration](../acf-block-registration/SKILL.md) - ACF blocks guide
- [web-components](../web-components/SKILL.md) - View script patterns
- [block-editor-components](../block-editor-components/SKILL.md) - Edit component patterns
- [vitest-testing](../vitest-testing/SKILL.md) - TypeScript testing
- [phpunit-testing](../phpunit-testing/SKILL.md) - PHP testing
