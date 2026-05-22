---
name: design-handoff-spec
description: Эксперт по design handoff. Используй для спецификаций дизайна, Figma annotations и developer handoff.
---

# Design Handoff Specialist

Эксперт по созданию спецификаций для передачи дизайна в разработку.

## Core Competencies

### Precision & Clarity
- Exact measurements and spacing
- Consistent units (px, rem, em)
- Color values in multiple formats
- Absolute and relative measurements

### Developer-Focused
- CSS-structured properties
- Component hierarchies
- Interactive state transitions
- Responsive breakpoints

### Asset Management
- Export formats and sizes
- Naming conventions
- Compression requirements
- Accessibility considerations

## Component Specification Template

```markdown
# Component: [Name]

## Overview
- **Type:** Atom / Molecule / Organism
- **Status:** Ready for development
- **Figma Link:** [link]

## Usage Context
- Where this component appears
- Related components
- Usage guidelines

## Variants
| Variant | Description | Use Case |
|---------|-------------|----------|
| Primary | Main action | CTAs, forms |
| Secondary | Alternative action | Cancel, back |
| Tertiary | Low emphasis | Links in text |
| Destructive | Dangerous action | Delete, remove |
```

## Layout & Positioning

```css
/* Component Structure */
.button {
  /* Box Model */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  /* Dimensions */
  min-width: 120px;
  height: 44px;
  padding: 12px 24px;

  /* Position Context */
  position: relative;
  z-index: 1;
}

/* Spacing Relationships */
.button-group {
  display: flex;
  gap: 12px; /* Between buttons */
}

.form-field + .button {
  margin-top: 24px; /* Form to button */
}
```

## Typography Specifications

```yaml
Button Text:
  font-family: "Inter", -apple-system, sans-serif
  font-size: 14px / 0.875rem
  font-weight: 600
  line-height: 20px / 1.43
  letter-spacing: 0.01em
  text-transform: none
  color: #FFFFFF

Label Text:
  font-family: "Inter", sans-serif
  font-size: 12px / 0.75rem
  font-weight: 500
  line-height: 16px / 1.33
  letter-spacing: 0.02em
  color: #6B7280
```

## Color Specifications

```yaml
Primary Button:
  background:
    default: "#2563EB"  # Blue-600
    hover: "#1D4ED8"    # Blue-700
    active: "#1E40AF"   # Blue-800
    disabled: "#93C5FD" # Blue-300

  text:
    default: "#FFFFFF"
    disabled: "#DBEAFE" # Blue-100

  border:
    default: "transparent"
    focus: "#3B82F6"    # Blue-500 (ring)

Secondary Button:
  background:
    default: "#F3F4F6"  # Gray-100
    hover: "#E5E7EB"    # Gray-200
    active: "#D1D5DB"   # Gray-300
    disabled: "#F9FAFB" # Gray-50

  text:
    default: "#374151"  # Gray-700
    disabled: "#9CA3AF" # Gray-400
```

## Interactive States

```yaml
States:
  default:
    description: "Initial state"
    cursor: pointer

  hover:
    description: "Mouse over"
    transition: "all 150ms ease-in-out"
    transform: "translateY(-1px)"
    shadow: "0 4px 6px -1px rgba(0,0,0,0.1)"

  active:
    description: "Mouse down / touch"
    transform: "translateY(0)"
    shadow: "0 1px 2px 0 rgba(0,0,0,0.05)"

  focus:
    description: "Keyboard focus"
    outline: "none"
    ring: "2px solid #3B82F6"
    ring-offset: "2px"

  disabled:
    description: "Not interactive"
    cursor: "not-allowed"
    opacity: 0.5
    pointer-events: "none"

  loading:
    description: "Action in progress"
    cursor: "wait"
    content: "Spinner icon"
```

## Responsive Breakpoints

```yaml
Breakpoints:
  mobile:
    range: "320px - 767px"
    button-height: 48px
    button-padding: "14px 20px"
    font-size: 16px
    full-width: true

  tablet:
    range: "768px - 1023px"
    button-height: 44px
    button-padding: "12px 24px"
    font-size: 14px
    full-width: false

  desktop:
    range: "1024px+"
    button-height: 40px
    button-padding: "10px 20px"
    font-size: 14px
    full-width: false
```

## Asset Requirements

```yaml
Icons:
  format: SVG (preferred), PNG fallback
  sizes:
    - 16x16 (small)
    - 20x20 (default)
    - 24x24 (large)
  naming: "icon-{name}-{size}.svg"
  color: "currentColor" for flexibility

Images:
  format: WebP (preferred), JPEG fallback
  sizes:
    - 1x: base size
    - 2x: retina
    - 3x: high-density mobile
  naming: "{name}@{scale}x.{format}"
  compression: 80% quality

Exports from Figma:
  - Export as SVG for icons
  - Export as PNG 1x, 2x, 3x for images
  - Use "Export for Web" preset
```

## Animation Specifications

```css
/* Transition Tokens */
:root {
  --transition-fast: 150ms ease-in-out;
  --transition-normal: 250ms ease-in-out;
  --transition-slow: 350ms ease-in-out;
}

/* Button Hover Animation */
.button {
  transition:
    background-color var(--transition-fast),
    transform var(--transition-fast),
    box-shadow var(--transition-fast);
}

.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Loading Spinner */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.button-spinner {
  animation: spin 1s linear infinite;
}
```

## Accessibility Requirements

```yaml
WCAG Compliance:
  contrast:
    normal-text: "4.5:1 minimum"
    large-text: "3:1 minimum"
    ui-components: "3:1 minimum"

  focus:
    indicator: "visible focus ring"
    style: "2px solid, 2px offset"
    color: "meets contrast requirement"

  touch-target:
    minimum: "44x44px"
    recommended: "48x48px"

  screen-reader:
    - Meaningful button text
    - aria-label for icon-only buttons
    - aria-disabled for disabled state
    - aria-busy for loading state

Example:
  ```html
  <button
    class="button button--primary"
    aria-label="Submit form"
    aria-busy="false"
  >
    <span class="button__text">Submit</span>
  </button>
  ```
```

## Design Tokens

```json
{
  "color": {
    "primary": {
      "50": "#EFF6FF",
      "100": "#DBEAFE",
      "500": "#3B82F6",
      "600": "#2563EB",
      "700": "#1D4ED8"
    },
    "gray": {
      "50": "#F9FAFB",
      "100": "#F3F4F6",
      "700": "#374151",
      "900": "#111827"
    }
  },
  "spacing": {
    "1": "4px",
    "2": "8px",
    "3": "12px",
    "4": "16px",
    "6": "24px",
    "8": "32px"
  },
  "borderRadius": {
    "sm": "4px",
    "md": "6px",
    "lg": "8px",
    "full": "9999px"
  },
  "shadow": {
    "sm": "0 1px 2px 0 rgba(0,0,0,0.05)",
    "md": "0 4px 6px -1px rgba(0,0,0,0.1)",
    "lg": "0 10px 15px -3px rgba(0,0,0,0.1)"
  }
}
```

## Implementation Notes

```markdown
## Z-Index Hierarchy
| Element | Z-Index |
|---------|---------|
| Base content | 0 |
| Dropdown | 10 |
| Sticky header | 20 |
| Modal backdrop | 30 |
| Modal content | 40 |
| Tooltip | 50 |
| Toast notification | 60 |

## Performance Considerations
- Use CSS transforms over position changes
- Avoid layout shifts on state changes
- Lazy load images below the fold
- Preload critical fonts

## Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Dependencies
- Inter font (Google Fonts)
- Heroicons for icons
- Tailwind CSS utilities (optional)
```

## QA Checklist

```markdown
## Visual Verification
- [ ] Matches Figma design at all breakpoints
- [ ] Colors match specifications exactly
- [ ] Typography matches specs
- [ ] Spacing is pixel-perfect
- [ ] Icons render correctly

## Interactive Verification
- [ ] All states work correctly
- [ ] Transitions are smooth
- [ ] Focus states visible
- [ ] Touch targets adequate

## Accessibility Verification
- [ ] Contrast ratios pass WCAG AA
- [ ] Focus indicators visible
- [ ] Screen reader announces correctly
- [ ] Keyboard navigation works

## Cross-Browser
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile Safari
- [ ] Chrome Android
```

## Лучшие практики

1. **Single source of truth** — Figma как источник правды
2. **Design tokens** — переменные вместо хардкода
3. **Component-first** — документируйте компоненты, не страницы
4. **State completeness** — все состояния задокументированы
5. **Accessibility built-in** — a11y с самого начала
6. **Developer communication** — регулярные синки с разработкой
