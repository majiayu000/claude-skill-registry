---
name: catppuccin-theming
description: Apply Catppuccin color palettes to configs, stylesheets, and terminal themes. This skill should be used when creating or modifying CSS themes, terminal color schemes, shell prompts (Starship, etc.), or any configuration that requires consistent Catppuccin colors. Covers all four official flavors (Latte, Frappe, Macchiato, Mocha) plus ZK's custom variants (rose, sage, grape, honey, blueberry).
---

# Catppuccin Theming

## Overview

Apply Catppuccin's soothing pastel color palettes consistently across CSS, terminal themes, shell configs, and application color schemes. This skill provides exact hex values, generation patterns, and ZK's custom palette variants.

## Core Palette Reference

### Rainbow Colors (accent colors)

Each flavor has these 14 accent colors. Values shown as: `name - frappe macchiato mocha`

| Color     | Frappe    | Macchiato | Mocha     |
|-----------|-----------|-----------|-----------|
| rosewater | `#f2d5cf` | `#f4dbd6` | `#f5e0dc` |
| flamingo  | `#eebebe` | `#f0c6c6` | `#f2cdcd` |
| pink      | `#f4b8e4` | `#f5bde6` | `#f5c2e7` |
| mauve     | `#ca9ee6` | `#c6a0f6` | `#cba6f7` |
| red       | `#e78284` | `#ed8796` | `#f38ba8` |
| maroon    | `#ea999c` | `#ee99a0` | `#eba0ac` |
| peach     | `#ef9f76` | `#f5a97f` | `#fab387` |
| yellow    | `#e5c890` | `#eed49f` | `#f9e2af` |
| green     | `#a6d189` | `#a6da95` | `#a6e3a1` |
| teal      | `#81c8be` | `#8bd5ca` | `#94e2d5` |
| sky       | `#99d1db` | `#91d7e3` | `#89dceb` |
| sapphire  | `#85c1dc` | `#7dc4e4` | `#74c7ec` |
| blue      | `#8caaee` | `#8aadf4` | `#89b4fa` |
| lavender  | `#babbf1` | `#b7bdf8` | `#b4befe` |

### Base/Surface Colors (Mocha - most common dark theme)

| Role      | Hex       | Usage                          |
|-----------|-----------|--------------------------------|
| text      | `#cdd6f4` | Primary text                   |
| subtext1  | `#bac2de` | Secondary text                 |
| subtext0  | `#a6adc8` | Tertiary/muted text            |
| overlay2  | `#9399b2` | Overlays, borders              |
| overlay1  | `#7f849c` | Secondary overlays             |
| overlay0  | `#6c7086` | Tertiary overlays              |
| surface2  | `#585b70` | Elevated surfaces              |
| surface1  | `#45475a` | Cards, panels                  |
| surface0  | `#313244` | Slight elevation               |
| base      | `#1e1e2e` | Main background                |
| mantle    | `#181825` | Slightly darker background     |
| crust     | `#11111b` | Darkest background             |

## Usage Patterns

### CSS Variables

To generate CSS custom properties for a Catppuccin theme:

```css
:root {
  /* Accent Colors - Mocha */
  --ctp-rosewater: #f5e0dc;
  --ctp-flamingo: #f2cdcd;
  --ctp-pink: #f5c2e7;
  --ctp-mauve: #cba6f7;
  --ctp-red: #f38ba8;
  --ctp-maroon: #eba0ac;
  --ctp-peach: #fab387;
  --ctp-yellow: #f9e2af;
  --ctp-green: #a6e3a1;
  --ctp-teal: #94e2d5;
  --ctp-sky: #89dceb;
  --ctp-sapphire: #74c7ec;
  --ctp-blue: #89b4fa;
  --ctp-lavender: #b4befe;

  /* Base Colors - Mocha */
  --ctp-text: #cdd6f4;
  --ctp-subtext1: #bac2de;
  --ctp-subtext0: #a6adc8;
  --ctp-overlay2: #9399b2;
  --ctp-overlay1: #7f849c;
  --ctp-overlay0: #6c7086;
  --ctp-surface2: #585b70;
  --ctp-surface1: #45475a;
  --ctp-surface0: #313244;
  --ctp-base: #1e1e2e;
  --ctp-mantle: #181825;
  --ctp-crust: #11111b;
}
```

### Terminal 16-Color Scheme (JSON format)

Standard ANSI 16-color mapping for terminal emulators:

```json
{
  "name": "catppuccin-mocha",
  "color": [
    "#1e1e2e", "#f38ba8", "#a6e3a1", "#f9e2af",
    "#89b4fa", "#cba6f7", "#94e2d5", "#cdd6f4",
    "#45475a", "#fab387", "#a6e3a1", "#f9e2af",
    "#74c7ec", "#f5c2e7", "#94e2d5", "#b4befe"
  ],
  "foreground": "#cdd6f4",
  "background": "#1e1e2e"
}
```

Color indices: 0=black 1=red 2=green 3=yellow 4=blue 5=magenta 6=cyan 7=white, then bright variants 8-15.

### Starship Prompt

Example Starship config using Catppuccin Mocha:

```toml
format = """$directory$git_branch$git_status$character"""

[directory]
format = "[$path]($style) "
style = "bold #89b4fa"

[git_branch]
format = "[$symbol$branch]($style) "
symbol = " "
style = "bold #a6e3a1"

[git_status]
format = "[$all_status$ahead_behind]($style) "
style = "bold #f38ba8"

[character]
success_symbol = "[>](#cba6f7)"
error_symbol = "[>](#f38ba8)"
```

### Python catppuccin Package

When available, use the `catppuccin` Python package for programmatic palette access:

```python
from catppuccin import PALETTE

# Access a flavor
mocha = PALETTE.mocha

# Iterate colors
for color in mocha.colors:
    print(f'{color.name}: {color.hex}')

# Generate CSS variables
print(':root {')
for color in mocha.colors:
    css_name = color.name.lower().replace(' ', '-')
    print(f'  --ctp-{css_name}: {color.hex};')
print('}')

# Generate JSON
import json
colors = {c.name.lower().replace(' ', '_'): c.hex for c in mocha.colors}
print(json.dumps({'mocha': colors}, indent=2))
```

## ZK Custom Variants

For ZK's custom palette variants (rose, sage, grape, honey, blueberry), refer to `references/🩷Catppuccin.pure.json`.

## Semantic Color Assignments

When applying Catppuccin to UI elements, follow these conventions:

| Element Type      | Recommended Colors           |
|-------------------|------------------------------|
| Primary actions   | blue, sapphire               |
| Success states    | green, teal                  |
| Warning states    | yellow, peach                |
| Error states      | red, maroon                  |
| Links             | blue, sapphire, mauve        |
| Headings          | lavender, mauve              |
| Code/monospace    | pink, flamingo               |
| Selection         | surface2 bg, text fg         |
| Hover states      | surface1 or surface2         |
| Borders           | overlay0, overlay1           |
| Muted text        | subtext0, subtext1           |

## Resources

- `references/🩷Catppuccin.pure.json` - Full palette and example data including ZK's custom variants in **Semantic JSON**
- `assets/palette-mutator.html` - Interactive tool for mutating palettes (hue shift, saturation, lightness, contrast) with export to CSS/JSON/Terminal formats
