---
name: global-toolbar-controls
description: Quick global settings — currency, language, region, units — belong in a persistent, low-profile location such as a header toolbar or footer. These controls are frequent but not primary, so they use small typography and stay out of the main content hierarchy. Use when designing global selectors, locale switchers, or user preference controls that apply across the whole product.
metadata:
  priority: 5
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "design-system/**"
    - "ui/**"
  promptSignals:
    phrases:
      - "currency"
      - "language"
      - "locale"
      - "region"
      - "global settings"
      - "toolbar"
      - "header controls"
      - "units"
retrieval:
  aliases:
    - global settings
    - locale switcher
    - currency selector
    - language switcher
    - toolbar controls
    - header utility bar
  intents:
    - add currency switcher
    - design language selector
    - place global settings in layout
    - add locale controls to header
  examples:
    - where should the currency selector go
    - add a language switcher to the header
    - design global settings controls for the toolbar
---

# Global Toolbar Controls

## What Belongs Here

Global controls affect the entire product experience but are not the user's primary task. They are reached occasionally — once per session or less — and should not compete visually with primary navigation or content.

Typical global toolbar controls:
- **Currency selector** (e-commerce, financial tools)
- **Language / locale switcher**
- **Region or market selector**
- **Unit system** (metric / imperial)
- **Theme toggle** (light / dark)
- **Accessibility preferences** (font size, contrast)

These are distinct from user account settings (which live in a profile menu) and from contextual settings (which live adjacent to the feature they affect).

## Where to Place Them

### Header utility strip
A secondary row above or within the main header, right-aligned. Common on e-commerce and international sites.

```
[Logo]                    [EN | EUR | 🌍]  [Account]  [Cart]
────────────────────────────────────────────────────────────
[Main navigation]
```

### Header right — compact
Inline with the main header, far right, using small typography and minimal visual weight.

```
[Logo]  [Nav items ...]              [EUR ▾]  [EN ▾]  [Account ▾]
```

### Footer
For controls the user sets once and rarely revisits. Language and region selectors frequently appear in footers on large international sites (Airbnb, Apple). Appropriate when the control is truly infrequent.

### Dedicated settings area
For more complex preference sets, a Settings page or panel is cleaner than cramming everything into the toolbar. The toolbar should link to it, not contain it.

## Typography and Visual Treatment

Global toolbar controls are secondary UI — they should not draw the eye away from primary content.

- **Font size: 13–14px** — deliberately smaller than body text (14px maximum per the type scale)
- **Colour: muted** — use a secondary text colour (`--color-text-secondary`), not the primary text colour
- **No bold** — regular weight only
- **Compact spacing** — tighter padding than primary navigation items
- **Separator** — a `|` or thin vertical rule between adjacent controls (language | currency) keeps them grouped without using full button chrome

```css
.toolbar-control {
  font-size: var(--text-sm);       /* 13–14px */
  color: var(--color-text-secondary);
  font-weight: 400;
  padding: 4px 8px;
}
```

## Interaction Pattern

Global controls typically use a **compact dropdown** — clicking the label opens a small popover or select with the available options.

- Show the current value as the trigger label: `EUR ▾`, `EN ▾`
- Use a flag icon + language code for locale, or currency symbol + code for currency
- Keep the option list short — if it exceeds ~20 items, add a search input inside the dropdown
- On selection, apply immediately and confirm with a brief status update (toast or inline update) if the change has a visible effect

## Review Checklist

- [ ] Are global controls placed consistently in one location across all pages?
- [ ] Is the typography smaller and more muted than primary navigation?
- [ ] Does the control show the current value as its label?
- [ ] Is the dropdown or popover compact and keyboard-navigable?
- [ ] Are global controls separated from user account settings?
- [ ] On mobile, are global controls accessible without being prominent? (Often moved to a menu or footer on small screens)
