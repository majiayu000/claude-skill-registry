---
name: create-interface
description: Renders interactive HTML interfaces in chat using the render_ui tool. Use when the user asks to display UI, create a widget, show a form, render a chart, build an interface, or display interactive content.
version: 1
---

# Create Interface

Render custom HTML interfaces directly in chat using the `mcp__noetect-ui__render_ui` tool. Perfect for forms, charts, tables, dashboards, and interactive widgets.

## Tool Usage

```
Tool: mcp__noetect-ui__render_ui
Input:
  html: "<div class='card'><h2>Hello</h2></div>"   # Required - HTML content (body only, no <html> wrapper)
  title: "My Widget"                                # Optional - header above the UI
  height: 300                                       # Optional - fixed height in pixels (default: auto-resize)
```

## Theme Integration

The UI automatically inherits the app's current theme. Use CSS variables for consistent styling across light/dark modes.

### Surface Colors (backgrounds)
| Variable | Usage |
|----------|-------|
| `var(--surface-primary)` | Main background |
| `var(--surface-secondary)` | Cards, elevated surfaces |
| `var(--surface-tertiary)` | Nested containers |
| `var(--surface-accent)` | Highlighted areas |
| `var(--surface-muted)` | Subtle backgrounds, code blocks |

### Content Colors (text)
| Variable | Usage |
|----------|-------|
| `var(--content-primary)` | Main text |
| `var(--content-secondary)` | Secondary text, labels |
| `var(--content-tertiary)` | Muted text, placeholders |
| `var(--content-accent)` | Highlighted text |

### Border Colors
| Variable | Usage |
|----------|-------|
| `var(--border-default)` | Standard borders |
| `var(--border-accent)` | Emphasized borders |

### Semantic Colors
| Variable | Usage |
|----------|-------|
| `var(--semantic-primary)` | Primary actions, links |
| `var(--semantic-primary-foreground)` | Text on primary background |
| `var(--semantic-destructive)` | Destructive actions, errors |
| `var(--semantic-destructive-foreground)` | Text on destructive background |
| `var(--semantic-success)` | Success states |
| `var(--semantic-success-foreground)` | Text on success background |

### Design Tokens
| Variable | Usage |
|----------|-------|
| `var(--border-radius)` | Standard corner radius |
| `var(--shadow-sm)` | Subtle shadow |
| `var(--shadow-md)` | Medium shadow |
| `var(--shadow-lg)` | Large shadow |

## Built-in Utility Classes

### Text Classes
- `.text-primary` - Main text color
- `.text-secondary` - Secondary text color
- `.text-muted` - Muted/tertiary text color
- `.text-accent` - Accent text color
- `.text-success` - Success color
- `.text-destructive` - Error/destructive color

### Background Classes
- `.bg-primary` - Primary surface background
- `.bg-secondary` - Secondary surface background
- `.bg-muted` - Muted surface background

### Container Classes
- `.card` - Styled container with secondary background, border, border-radius, and 16px padding

## Pre-styled Elements

These elements have default theme-aware styles applied automatically:

- **body** - System font, 14px, primary text color, 12px padding
- **a** - Primary semantic color
- **button** - Secondary background, border, border-radius, hover state
- **button.primary** - Primary semantic background with foreground text
- **button.destructive** - Destructive semantic background with foreground text
- **input, select, textarea** - Primary background, border, focus ring
- **table, th, td** - Full width, border-bottom on rows
- **code** - Monospace font, muted background, 2px/4px padding
- **pre** - Monospace font, muted background, 12px padding, overflow scroll

## Auto-Resize Behavior

By default, the UI auto-resizes to fit its content. The iframe:
1. Measures content height on load
2. Observes DOM mutations and resizes dynamically
3. Responds to window resize events

Set a fixed `height` parameter to disable auto-resize.

## Examples

### Simple Card
```html
<div class="card">
  <h3 style="margin: 0 0 8px 0;">Status</h3>
  <p class="text-secondary" style="margin: 0;">All systems operational</p>
</div>
```

### Form with Inputs
```html
<div class="card">
  <h3 style="margin: 0 0 12px 0;">Contact</h3>
  <input type="text" placeholder="Name" style="width: 100%; margin-bottom: 8px;">
  <input type="email" placeholder="Email" style="width: 100%; margin-bottom: 8px;">
  <textarea placeholder="Message" style="width: 100%; height: 80px; margin-bottom: 12px;"></textarea>
  <button class="primary">Send</button>
</div>
```

### Data Table
```html
<table>
  <thead>
    <tr><th>Name</th><th>Status</th><th>Actions</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Item 1</td>
      <td class="text-success">Active</td>
      <td><button>Edit</button></td>
    </tr>
    <tr>
      <td>Item 2</td>
      <td class="text-muted">Inactive</td>
      <td><button>Edit</button></td>
    </tr>
  </tbody>
</table>
```

### Stats Dashboard
```html
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
  <div class="card" style="text-align: center;">
    <div style="font-size: 24px; font-weight: 600;">128</div>
    <div class="text-secondary">Users</div>
  </div>
  <div class="card" style="text-align: center;">
    <div style="font-size: 24px; font-weight: 600;">1.2k</div>
    <div class="text-secondary">Events</div>
  </div>
  <div class="card" style="text-align: center;">
    <div style="font-size: 24px; font-weight: 600;">99.9%</div>
    <div class="text-secondary">Uptime</div>
  </div>
</div>
```

### Interactive with JavaScript
```html
<div class="card">
  <div id="count" style="font-size: 32px; text-align: center; margin-bottom: 12px;">0</div>
  <div style="display: flex; gap: 8px; justify-content: center;">
    <button onclick="update(-1)">−</button>
    <button class="primary" onclick="update(1)">+</button>
  </div>
</div>
<script>
  let count = 0;
  function update(delta) {
    count += delta;
    document.getElementById('count').textContent = count;
  }
</script>
```

## Security Notes

- UI renders in a **sandboxed iframe** with `allow-scripts allow-forms`
- **No access** to parent window, localStorage, cookies, or parent DOM
- Scripts execute within the iframe only
- Forms work but submissions stay within the iframe
- Safe for displaying user-generated or dynamic content
