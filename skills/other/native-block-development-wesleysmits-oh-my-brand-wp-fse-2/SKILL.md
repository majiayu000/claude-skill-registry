---
name: native-block-development
description: Guide for creating native WordPress blocks in Oh My Brand! FSE theme. Block structure, block.json configuration, render.php templates, and asset registration. Use when building new blocks.
metadata:
  author: Wesley Smits
  version: "1.0.0"
---

# Native Block Development

Creating native WordPress blocks for the Oh My Brand! FSE theme using `@wordpress/scripts`.

---

## When to Use

- Creating new WordPress blocks with editor and frontend components
- Configuring block metadata and supports
- Writing PHP render templates for server-side rendering
- Registering block assets (styles, scripts)

---

## Block File Structure

Every block lives in `src/blocks/{block-name}/`:

```
src/blocks/gallery/
├── block.json          # Block metadata and registration
├── index.js            # Block registration entry point
├── edit.tsx            # Editor React component
├── render.php          # Server-side render template
├── helpers.php         # Block-specific helper functions
├── style.css           # Frontend styles (auto-enqueued)
├── editor.css          # Editor-only styles (optional)
├── view.ts             # Frontend TypeScript (Web Component)
└── view.test.ts        # Unit tests
```

---

## File Templates

Use templates from [block-scaffolds](../block-scaffolds/SKILL.md):

| File | Template | Purpose |
|------|----------|---------|
| `block.json` | [block-json-native.json](../block-scaffolds/references/block-json-native.json) | Block metadata |
| `render.php` | [render-native.php](../block-scaffolds/references/render-native.php) | Server-side render |
| `helpers.php` | [helpers-native.php](../block-scaffolds/references/helpers-native.php) | Helper functions |
| `view.ts` | [view.ts](../block-scaffolds/references/view.ts) | Frontend Web Component |
| `style.css` | [style.css](../block-scaffolds/references/style.css) | Frontend styles |
| `edit.tsx` | [edit.tsx](../block-scaffolds/references/edit.tsx) | Editor component |

---

## block.json Key Properties

| Property | Required | Description |
|----------|----------|-------------|
| `$schema` | Yes | `https://schemas.wp.org/trunk/block.json` |
| `apiVersion` | Yes | Always use `3` |
| `name` | Yes | Format: `theme-oh-my-brand/{block-name}` |
| `version` | Yes | Semantic version (e.g., `1.0.0`) |
| `textdomain` | Yes | `theme-oh-my-brand` |
| `render` | Yes | `file:./render.php` |
| `editorScript` | Yes | `file:./index.js` |
| `viewScript` | Optional | `file:./view.js` for frontend JS |
| `style` | Yes | `file:./style.css` |

### Common Supports

```json
"supports": {
    "align": ["wide", "full"],
    "anchor": true,
    "className": true,
    "color": {
        "background": true,
        "text": true
    },
    "spacing": {
        "margin": true,
        "padding": true,
        "blockGap": true
    }
}
```

---

## Render Template Guidelines

| Guideline | Description |
|-----------|-------------|
| `declare(strict_types=1)` | Always include at top |
| Early return | Return early if no data to display |
| `get_block_wrapper_attributes()` | Use for consistent wrapper |
| Escape all output | `esc_html()`, `esc_attr()`, `esc_url()` |
| Unique IDs | Use `wp_unique_id()` for instances |
| Web Component wrapper | Use `<omb-{block-name}>` for frontend JS |

---

## Helper Function Guidelines

| Guideline | Description |
|-----------|-------------|
| Function prefix | Use `omb_{block_name}_` prefix |
| `function_exists()` guard | Wrap in existence check |
| Type hints | Use parameter and return types |
| DocBlocks | Include `@param` and `@return` |

---

## Asset Handling

### Automatic Loading

Assets defined in `block.json` are automatically enqueued:

| Property | When Loaded |
|----------|-------------|
| `style` | Frontend and editor |
| `editorStyle` | Editor only |
| `editorScript` | Editor only |
| `viewScript` | Frontend only |

Assets only load when the block is present on the page.

---

## Step-by-Step Creation

1. **Create directory**: `mkdir -p src/blocks/my-block`
2. **Add block.json**: Copy from [template](../block-scaffolds/references/block-json-native.json), replace placeholders
3. **Create edit.tsx**: See [block-editor-components](../block-editor-components/SKILL.md)
4. **Create render.php**: Copy from [template](../block-scaffolds/references/render-native.php)
5. **Create helpers.php**: Copy from [template](../block-scaffolds/references/helpers-native.php)
6. **Create view.ts**: See [web-components](../web-components/SKILL.md)
7. **Add style.css**: See [css-standards](../css-standards/SKILL.md)
8. **Write tests**: See [vitest-testing](../vitest-testing/SKILL.md)
9. **Build**: `pnpm run build`
10. **Verify**: Check block appears in editor

---

## Related Skills

- [block-scaffolds](../block-scaffolds/SKILL.md) - Copy-paste templates
- [web-components](../web-components/SKILL.md) - Frontend view scripts
- [block-editor-components](../block-editor-components/SKILL.md) - Editor components
- [php-standards](../php-standards/SKILL.md) - PHP conventions
- [css-standards](../css-standards/SKILL.md) - CSS conventions
- [acf-block-registration](../acf-block-registration/SKILL.md) - ACF blocks

---

## References

- [WordPress Block API](https://developer.wordpress.org/block-editor/reference-guides/block-api/)
- [block.json Specification](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-metadata/)
- [@wordpress/scripts](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-scripts/)
