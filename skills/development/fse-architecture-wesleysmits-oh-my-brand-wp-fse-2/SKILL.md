---
name: fse-architecture
description: Oh My Brand! theme architecture and project structure. Directory layout, data flow, asset pipeline, and theme.json configuration. Use for understanding project organization.
metadata:
  author: Wesley Smits
  version: "1.0.0"
---

# FSE Architecture

Project architecture and structure for the Oh My Brand! WordPress FSE theme.

---

## When to Use

- Understanding the project directory structure
- Locating files and understanding their purpose
- Understanding how blocks are organized
- Understanding the build process and asset flow
- Configuring theme.json settings

---

## Reference Files

| File | Purpose |
|------|---------|
| [theme.json](references/theme.json) | theme.json structure and tokens |

---

## Project Structure

```
oh-my-brand/
├── AGENT.md               # AI assistant guidelines
├── functions.php          # Theme setup, hooks, registration
├── style.css              # Theme metadata (required by WP)
├── theme.json             # Global styles, settings, blocks
│
├── src/                   # Source files (@wordpress/scripts)
│   └── blocks/           # Native WordPress blocks
│       ├── gallery/      # Gallery carousel block
│       ├── faq/          # FAQ accordion block
│       └── utils/        # Shared utilities
│
├── build/                 # Compiled output (generated)
│   └── blocks/           # Built block assets
│
├── blocks/                # ACF custom blocks
│   ├── acf-faq/          # FAQ ACF block
│   └── acf-gallery-block/# Gallery ACF block
│
├── assets/                # Static assets
│   ├── css/              # Global stylesheets
│   ├── js/               # Compiled JavaScript
│   └── icons/            # SVG icons
│
├── includes/              # PHP includes
│   ├── assets.php        # Asset registration
│   └── block-helpers.php # Block utilities
│
├── acf-json/              # ACF field groups (auto-sync)
├── patterns/              # Block patterns
├── tests/                 # Test files
└── docs/                  # Documentation
```

---

## Theme Architecture

### Parent-Child Relationship

```
WordPress Core
      │
      ▼
Ollie Parent Theme
  • Base FSE templates
  • Default block styles
      │
      ▼
Oh My Brand! Child Theme
  • Custom blocks (native + ACF)
  • Extended theme.json
  • Brand-specific styles
```

### File Loading Order

1. WordPress Core loads first
2. Ollie Parent Theme `functions.php`
3. Oh My Brand! `functions.php`
4. theme.json merges (child overrides parent)
5. Block assets loaded per-block when rendered

---

## Block Organization

### Native Blocks (src/blocks/)

Built with `@wordpress/scripts`, compiled to `build/blocks/`:

| File | Purpose |
|------|---------|
| `block.json` | Block metadata |
| `index.js` | Registration entry |
| `edit.tsx` | Editor component |
| `render.php` | Server-side render |
| `helpers.php` | Helper functions |
| `style.css` | Frontend styles |
| `view.ts` | Frontend Web Component |

### ACF Blocks (blocks/)

ACF PRO blocks, not compiled:

| File | Purpose |
|------|---------|
| `block.json` | ACF block metadata |
| `render.php` | Render template |
| `helpers.php` | Helper functions |
| `style.css` | Block styles |

### Key Differences

| Aspect | Native Block | ACF Block |
|--------|--------------|-----------|
| Location | `src/blocks/` | `blocks/` |
| Name prefix | `theme-oh-my-brand/` | `acf/` |
| Data source | `$attributes` | `get_field()` |
| Editor UI | React component | ACF fields |
| Build | Required | Not required |

---

## Asset Pipeline

### Build Process

```
Source                    Build Output
──────                    ────────────
src/blocks/gallery/
├── index.js         →    build/blocks/gallery/
├── edit.tsx              ├── index.js
├── view.ts               ├── view.js
├── style.css             ├── style-index.css
└── editor.css            └── index.css
```

### Commands

| Command | Purpose |
|---------|---------|
| `pnpm run build` | Production build |
| `pnpm run start` | Watch mode |
| `pnpm run lint` | Run all linters |

### Asset Loading

| Property | When Loaded |
|----------|-------------|
| `style` | Block rendered (frontend + editor) |
| `editorStyle` | Block in editor |
| `viewScript` | Block on frontend page |

---

## Data Flow

### Native Block Data Flow

```
block.json (attributes) → edit.tsx (editor state)
      ↓
$attributes (saved to post)
      ↓
render.php (server render)
      ↓
view.ts (frontend interactivity)
```

### ACF Block Data Flow

```
ACF Field Group (acf-json/) → WordPress Editor (ACF forms)
      ↓
get_field() (post meta)
      ↓
render.php (server render)
```

---

## theme.json Configuration

### Structure

See [theme.json](references/theme.json) for complete structure example.

### Design Tokens

| Token Type | CSS Variable |
|------------|--------------|
| Colors | `var(--wp--preset--color--primary)` |
| Spacing | `var(--wp--preset--spacing--20)` |
| Typography | `var(--wp--preset--font-family--body)` |
| Layout | `var(--wp--style--global--content-size)` |

---

## Related Skills

- [native-block-development](../native-block-development/SKILL.md) - Block creation
- [acf-block-registration](../acf-block-registration/SKILL.md) - ACF blocks
- [css-standards](../css-standards/SKILL.md) - CSS and theme.json tokens
- [fse-git-workflow](../fse-git-workflow/SKILL.md) - Development workflow

---

## References

- [WordPress FSE Documentation](https://developer.wordpress.org/block-editor/how-to-guides/themes/)
- [theme.json Reference](https://developer.wordpress.org/block-editor/how-to-guides/themes/theme-json/)
- [@wordpress/scripts](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-scripts/)
