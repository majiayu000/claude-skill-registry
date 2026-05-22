---
name: wp-block-themes
description: "Use when developing WordPress block themes: theme.json (global settings/styles), templates and template parts, patterns, style variations, and Site Editor troubleshooting (style hierarchy, overrides, caching)."
compatibility: "Targets WordPress 6.9+ (PHP 8.0+). Filesystem-based agent with bash + node."
---

# WP Block Themes

## When to use

Use this skill for block theme work such as:

- Editing `theme.json` (presets, settings, styles, per-block styles)
- Adding or changing templates (`templates/*.html`) and template parts (`parts/*.html`)
- Adding patterns (`patterns/*.php`) and controlling inserter visibility
- Adding style variations (`styles/*.json`)
- Debugging "styles not applying" / "editor doesn't reflect theme.json"

## Inputs required

- Repo root and which theme is targeted
- Target WordPress version range (theme.json version varies by core version)
- Where the issue manifests: Site Editor, post editor, frontend, or all

## Procedure

### 1) Verify block theme structure

Required structure:

```
theme-name/
├── style.css          # Theme header (required)
├── theme.json         # Global settings and styles (required)
├── templates/         # Full page templates
│   ├── index.html     # Fallback template (required)
│   ├── single.html
│   ├── archive.html
│   └── ...
├── parts/             # Template parts
│   ├── header.html
│   ├── footer.html
│   └── ...
├── patterns/          # Block patterns (optional)
│   └── *.php
└── styles/            # Style variations (optional)
    └── *.json
```

### 2) theme.json structure

**Settings** (what the UI allows):

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "color": {
      "palette": [
        { "slug": "primary", "color": "#0073aa", "name": "Primary" }
      ]
    },
    "typography": {
      "fontSizes": [
        { "slug": "small", "size": "14px", "name": "Small" }
      ]
    },
    "layout": {
      "contentSize": "800px",
      "wideSize": "1200px"
    }
  }
}
```

**Styles** (how it looks by default):

```json
{
  "styles": {
    "color": {
      "background": "var(--wp--preset--color--base)",
      "text": "var(--wp--preset--color--contrast)"
    },
    "elements": {
      "link": {
        "color": { "text": "var(--wp--preset--color--primary)" }
      }
    },
    "blocks": {
      "core/button": {
        "color": {
          "background": "var(--wp--preset--color--primary)"
        }
      }
    }
  }
}
```

### 3) Templates and template parts

**Templates** (`templates/*.html`):

```html
<!-- wp:template-part {"slug":"header"} /-->

<!-- wp:group {"tagName":"main"} -->
<main class="wp-block-group">
  <!-- wp:post-title /-->
  <!-- wp:post-content /-->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer"} /-->
```

**Template parts** (`parts/*.html`):
- Must NOT be nested in subdirectories
- Must have matching `slug` in template-part block

### 4) Patterns

Create patterns in `patterns/*.php`:

```php
<?php
/**
 * Title: Hero Section
 * Slug: theme-name/hero
 * Categories: featured
 * Keywords: hero, banner
 */
?>
<!-- wp:cover {"url":"..."} -->
...
<!-- /wp:cover -->
```

### 5) Style variations

Create variations in `styles/*.json`:

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "title": "Dark Mode",
  "settings": {},
  "styles": {
    "color": {
      "background": "#1a1a1a",
      "text": "#ffffff"
    }
  }
}
```

### 6) Style hierarchy (debugging)

Styles apply in this order (later overrides earlier):

1. Core defaults
2. theme.json (parent theme)
3. theme.json (child theme)
4. User customizations (stored in DB)

If your theme.json changes don't appear:
- Check if user customizations override them
- Clear any caches
- Validate JSON syntax

## Verification

- Site Editor reflects changes (Styles UI, templates, patterns)
- Frontend renders with expected styles
- If styles aren't changing, confirm user customizations don't override

## Failure modes / debugging

Common issues:

- **Wrong theme root**: Editing inactive theme
- **User overrides**: Customizations in DB override theme.json
- **Invalid JSON**: Typos prevent application
- **Wrong folder**: Templates/parts in wrong location or nested

Debug commands:

```bash
# Validate theme.json
cat theme.json | python3 -m json.tool

# Check template files
ls -la templates/ parts/

# Verify theme is active
wp theme list --status=active
```

## Escalation

Consult canonical docs:
- [Theme Handbook - Block Themes](https://developer.wordpress.org/themes/block-themes/)
- [theme.json Reference](https://developer.wordpress.org/block-editor/reference-guides/theme-json-reference/)
