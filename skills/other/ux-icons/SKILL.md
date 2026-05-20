---
name: ux-icons
description: Symfony UX Icons for rendering SVG icons in Twig templates. Supports 200,000+ Iconify icons (Lucide, Heroicons, Tabler, Material Design, etc.), local SVG files, and custom icon sets with aliases. Use when displaying icons, configuring icon defaults, importing or locking on-demand icons, creating icon aliases, or styling SVG icons with CSS. Code triggers: <twig:ux:icon />, ux_icon(), UX_ICONS_DEFAULT_ICON_ATTRIBUTES, icon.yaml, icons/, iconify:, lucide:, heroicons:, tabler:, mdi:, bin/console ux:icons:lock, bin/console ux:icons:import. Also trigger when the user asks "how to add an icon", "how to use Lucide/Heroicons/Tabler icons", "how to render an SVG icon in Twig", "how to lock icons for production", "how to create icon aliases", "how to style an icon", "icon not found", "icon not rendering". Do NOT trigger for interactive maps (use ux-map) or general Twig components (use twig-component).
license: MIT
metadata:
  author: Simon Andre
  email: smn.andre@gmail.com
  url: https://smnandre.dev
  version: "1.0"
---

# UX Icons

Render local and remote SVG icons in Twig templates. Icons can come from local files, Iconify.design (200+ icon sets, 200,000+ icons), or custom icon sets. Icons are inlined as `<svg>` elements -- no icon fonts, no external requests at runtime.

## Installation

```bash
composer require symfony/ux-icons
```

## Quick Reference

```
ux_icon('name')                        Twig function
ux_icon('name', {class: 'w-4 h-4'})   with HTML attributes
<twig:ux:icon name="name" />           Twig component (requires ux-twig-component)
<twig:ux:icon name="set:name" />       icon from a specific set
```

## Rendering Icons

### Twig Function

```twig
{{ ux_icon('menu') }}
{# renders <svg ...>...</svg> #}

{{ ux_icon('user-profile', {class: 'w-4 h-4'}) }}
{# renders <svg class="w-4 h-4"> ... </svg> #}

{{ ux_icon('user-profile', {height: '16px', width: '16px', 'aria-hidden': true}) }}
{# renders <svg height="16" width="16" aria-hidden="true"> ... </svg> #}
```

### Twig Component (HTML Syntax)

Requires `symfony/ux-twig-component`.

```html
<twig:ux:icon name="user-profile" class="w-4 h-4" />

<twig:ux:icon name="flowbite:user-solid" />

<twig:ux:icon name="user-profile" height="16" width="16" aria-hidden="true" />
```

Any HTML attribute added to the component or passed to the function is rendered on the `<svg>` element.

## Icon Names

### Local Icons

Stored in `assets/icons/` by default. The file path (minus `.svg`) becomes the icon name:

```
assets/icons/
  ├─ close.svg           → ux_icon('close')
  ├─ menu.svg            → ux_icon('menu')
  └─ header/
     └─ logo.svg         → ux_icon('header:logo')
```

Subdirectories become prefixes separated by `:`. Use local icons for your own project-specific SVGs (app logo, custom illustrations).

### Iconify (On-Demand)

Use `prefix:name` syntax to pull icons from any Iconify set:

```twig
{# UI icons #}
{{ ux_icon('lucide:arrow-right') }}     {# Lucide #}
{{ ux_icon('tabler:heart') }}           {# Tabler #}
{{ ux_icon('heroicons:star-solid') }}   {# Heroicons #}
{{ ux_icon('mdi:check') }}              {# Material Design Icons #}

{# Country flags #}
<twig:ux:icon name="flagpack:fr" />
<twig:ux:icon name="flagpack:{{ country.code|lower }}" />

{# Brand logos #}
<twig:ux:icon name="simple-icons:symfony" />
<twig:ux:icon name="simple-icons:github" />

{# File type icons #}
<twig:ux:icon name="bi:filetype-pdf" />
<twig:ux:icon name="bi:filetype-{{ file.extension }}" />
```

On-demand icons are fetched from the Iconify API, cached locally, and inlined as SVG. No runtime HTTP requests in production.

Browse all available sets at https://icon-sets.iconify.design/

## Configuration

```yaml
# config/packages/ux_icons.yaml
ux_icons:
    # Local directory for icon SVG files
    icon_dir: '%kernel.project_dir%/assets/icons'

    # Default HTML attributes added to every icon
    default_icon_attributes:
        fill: currentColor
        'font-size': '1.25em'

    # Aliases: shortcut name => full icon name
    aliases:
        dots: 'clarity:ellipsis-horizontal-line'
        'tabler:save': 'tabler:device-floppy'

    # Iconify integration
    iconify:
        enabled: true
        on_demand: true
        endpoint: 'https://api.iconify.design'

    # Silently ignore missing icons (renders nothing instead of throwing)
    ignore_not_found: false
```

### Icon Sets

Define custom icon sets with their own prefix, source, and default attributes:

```yaml
ux_icons:
    icon_sets:
        # Local directory with custom attributes
        flags:
            path: '%kernel.project_dir%/assets/images/flags'
            icon_attributes:
                class: 'flag'
                fill: false           # "false" removes a default attribute

        # Alias an entire Iconify set under a shorter prefix
        icons:
            alias: 'lucide'           # ux_icon('icons:arrow-right') → lucide:arrow-right
```

### Aliases

Create shortcuts for frequently used icons:

```yaml
ux_icons:
    aliases:
        dots: 'clarity:ellipsis-horizontal-line'
        save: 'lucide:save'
        delete: 'lucide:trash-2'
        'tabler:save': 'tabler:device-floppy'   # can also remap within a set
```

```twig
{{ ux_icon('dots') }}    {# resolves to clarity:ellipsis-horizontal-line #}
{{ ux_icon('save') }}    {# resolves to lucide:save #}
```

## CLI Commands

### Import Icons Locally

Download icons from Iconify into your local `assets/icons/` directory:

```bash
# Import a single icon
php bin/console ux:icons:import flowbite:user-solid

# Import multiple icons
php bin/console ux:icons:import flowbite:user-solid flowbite:home-solid

# Force overwrite existing files
php bin/console ux:icons:import flowbite:user-solid --force
```

### Lock All On-Demand Icons

Download all icons currently used via on-demand into local files (similar to a dependency lock):

```bash
php bin/console ux:icons:lock

# Force overwrite
php bin/console ux:icons:lock --force

# Verbose output (helps spot invalid icon names)
php bin/console ux:icons:lock -v
```

## Accessibility

Icons are decorative by default. For meaningful icons, add `aria-label`:

```twig
{# Decorative (hidden from screen readers) #}
{{ ux_icon('lucide:star', {'aria-hidden': true}) }}

{# Meaningful (announced by screen readers) #}
{{ ux_icon('lucide:star', {'aria-label': 'Favorite', role: 'img'}) }}
```

## Key Principles

**Icons are inlined SVG.** No icon fonts, no `<img>` tags, no external HTTP requests at runtime. The SVG markup is embedded directly in your HTML. This means icons inherit `currentColor`, can be styled with CSS, and work offline.

**On-demand is for development.** During development, on-demand mode fetches icons from Iconify as needed. For production, run `ux:icons:lock` to download all used icons locally.

**Attributes cascade.** Default attributes from config < icon set attributes < per-icon attributes. Use `false` to remove a default attribute for a specific set or icon.

**Prefer the HTML syntax.** `<twig:ux:icon name="..." />` reads better in templates and is consistent with other UX components.

## References

- **API & Configuration** (all options, attributes, icon sets): [references/api.md](references/api.md)
- **Patterns** (common recipes, styling, dynamic icons): [references/patterns.md](references/patterns.md)
- **Gotchas** (common mistakes, debugging, caching): [references/gotchas.md](references/gotchas.md)
