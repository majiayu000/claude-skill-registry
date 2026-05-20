---
name: mockup-extraction
description: Extract reusable components from approved HTML mockups during implementation. Identifies patterns, maps CSS to Tailwind, and populates prototype-patterns.md for visual fidelity. Use at start of /implement for UI-first features.
---

<objective>
The mockup-extraction skill guides Claude in analyzing approved HTML mockups and extracting reusable components for implementation.

**Purpose**: Bridge the gap between visual mockups and production code by:
1. Identifying repeated UI patterns across mockup screens
2. Mapping mockup CSS classes to Tailwind utilities
3. Documenting component variants and states
4. Creating extraction tasks for systematic implementation

**When to invoke**: At the start of `/implement` phase when mockups exist and are approved (UI-first features).
</objective>

<quick_start>
<prerequisites>
Before extraction, verify:
1. Mockups exist in `specs/NNN-slug/mockups/` or `design/prototype/screens/`
2. Mockup approval gate passed in state.yaml
3. Theme files exist (theme.yaml, theme.css)
</prerequisites>

<basic_workflow>
1. **Inventory** - List all mockup HTML files
2. **Scan** - Parse HTML for component patterns
3. **Classify** - Categorize by component type
4. **Count** - Track occurrence frequency
5. **Map** - Convert CSS to Tailwind utilities
6. **Document** - Populate prototype-patterns.md
7. **Generate Tasks** - Create extraction tasks for tasks.md
</basic_workflow>

<extraction_output>
Generate `prototype-patterns.md` in feature directory:

```markdown
# Prototype Patterns: {FEATURE_NAME}

## Component Inventory
| Component | Source Screens | Occurrences | Priority |
|-----------|---------------|-------------|----------|
| Button Primary | login, signup, dashboard | 12 | Must extract |
| Card | dashboard, settings | 8 | Must extract |
| Form Input | login, signup, profile | 15 | Must extract |
| Alert | all screens | 6 | Consider extraction |

## Component Details

### Button Primary
- **CSS Classes**: `.btn`, `.btn-primary`
- **Tailwind**: `px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-hover`
- **States**: default, hover, focus, disabled, loading
- **Props**: `variant`, `size`, `icon`, `loading`

### Card
- **CSS Classes**: `.card`, `.card-elevated`
- **Tailwind**: `bg-surface p-4 rounded-lg shadow-md`
- **Variants**: default, elevated, bordered
- **Props**: `padding`, `shadow`, `header`, `footer`

## CSS to Tailwind Mapping
| CSS Variable | Tailwind Utility |
|--------------|------------------|
| var(--color-primary) | bg-primary, text-primary |
| var(--space-4) | p-4, m-4, gap-4 |
| var(--radius-md) | rounded-md |
| var(--shadow-md) | shadow-md |

## Visual Fidelity Checklist
- [ ] Spacing matches 8pt grid
- [ ] Colors use design tokens
- [ ] All states implemented (hover, focus, disabled)
- [ ] Typography uses scale
- [ ] Responsive breakpoints match
```
</extraction_output>
</quick_start>

<detailed_procedures>
<component_identification>
## Component Identification Rules

Scan mockup HTML for these patterns:

### Buttons
```
Selectors: button, [role="button"], .btn, .button
Variants: primary, secondary, outline, ghost, danger
States: default, hover, focus, active, disabled, loading
```

### Cards
```
Selectors: .card, [role="article"], .panel, .tile
Variants: default, elevated, bordered, interactive
Components: header, body, footer, actions
```

### Forms
```
Selectors: form, .form-group, .form-field, .input-group
Elements: input, textarea, select, checkbox, radio
States: default, focus, error, disabled, readonly
```

### Alerts/Notifications
```
Selectors: .alert, [role="alert"], .toast, .notification
Variants: info, success, warning, error
Components: icon, message, dismiss button
```

### Navigation
```
Selectors: nav, .nav, .navbar, .sidebar, .menu
Elements: links, dropdowns, icons, badges
States: active, hover, expanded
```

### Data Display
```
Selectors: table, .table, .list, .grid
Elements: header, rows, cells, pagination
States: loading, empty, error
```

### Modals/Dialogs
```
Selectors: .modal, [role="dialog"], .dialog, .drawer
Components: backdrop, header, body, footer, close button
States: open, closing
```
</component_identification>

<reusability_scoring>
## Reusability Scoring

Score components by occurrence frequency:

| Occurrences | Score | Action |
|-------------|-------|--------|
| 1 | Low | Inline styles OK |
| 2 | Medium | Consider extraction |
| 3+ | High | **Must extract** |
| 5+ | Critical | Extract with variants |

**Priority order for extraction:**
1. Components appearing on 5+ screens (Critical)
2. Components with 3+ variants (High)
3. Interactive components with multiple states (High)
4. Layout components (containers, grids) (Medium)
5. Static display components (Medium)
</reusability_scoring>

<css_tailwind_mapping>
## CSS to Tailwind Mapping

### Color Mappings
```
var(--color-primary) → bg-primary, text-primary, border-primary
var(--color-secondary) → bg-secondary, text-secondary
var(--color-neutral-*) → bg-neutral-*, text-neutral-*
var(--color-success) → bg-success, text-success
var(--color-error) → bg-error, text-error
```

### Spacing Mappings (8pt grid)
```
var(--space-1) → p-1, m-1, gap-1 (8px)
var(--space-2) → p-2, m-2, gap-2 (16px)
var(--space-3) → p-3, m-3, gap-3 (24px)
var(--space-4) → p-4, m-4, gap-4 (32px)
var(--space-6) → p-6, m-6, gap-6 (48px)
var(--space-8) → p-8, m-8, gap-8 (64px)
```

### Typography Mappings
```
var(--text-xs) → text-xs
var(--text-sm) → text-sm
var(--text-base) → text-base
var(--text-lg) → text-lg
var(--text-xl) → text-xl
var(--text-2xl) → text-2xl
var(--font-semibold) → font-semibold
var(--font-bold) → font-bold
```

### Border & Shadow Mappings
```
var(--radius-sm) → rounded-sm
var(--radius-md) → rounded-md
var(--radius-lg) → rounded-lg
var(--radius-full) → rounded-full
var(--shadow-sm) → shadow-sm
var(--shadow-md) → shadow-md
var(--shadow-lg) → shadow-lg
```

### Layout Mappings
```
display: flex → flex
display: grid → grid
flex-direction: column → flex-col
justify-content: center → justify-center
align-items: center → items-center
gap: var(--space-*) → gap-*
```
</css_tailwind_mapping>

<extraction_output_format>
## Extraction Output Format

For each extracted component, document:

```markdown
### Component: {NAME}

**Source Screens**: {list of mockup files}
**Occurrences**: {count}
**Priority**: {Must extract | Consider | Low}

**HTML Structure**:
```html
<button class="btn btn-primary">
  <span class="btn-icon">{icon}</span>
  <span class="btn-label">{label}</span>
</button>
```

**CSS Classes**:
- `.btn` - Base button styles
- `.btn-primary` - Primary variant
- `.btn-icon` - Icon container
- `.btn-label` - Label text

**Tailwind Equivalent**:
```tsx
<button className="inline-flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-hover focus:ring-2 focus:ring-primary/30 disabled:opacity-50">
  {icon && <span>{icon}</span>}
  <span>{label}</span>
</button>
```

**States to Implement**:
- [ ] Default
- [ ] Hover (bg-primary-hover)
- [ ] Focus (ring-2 ring-primary/30)
- [ ] Active (scale-95)
- [ ] Disabled (opacity-50, cursor-not-allowed)
- [ ] Loading (animate-spin icon)

**Props Interface**:
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'outline' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  icon?: React.ReactNode;
  loading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
}
```
```
</extraction_output_format>

<tailwind_variants_output>
## tailwind-variants (tv) Output Format

When `tailwind-variants` is detected in the project (or recommended for new projects), generate tv() component definitions:

### Single-Part Component (Button)

```typescript
// components/ui/button.ts
import { tv, type VariantProps } from 'tailwind-variants';

export const button = tv({
  base: 'inline-flex items-center justify-center gap-2 rounded-md font-medium transition-all duration-100 focus:outline-none focus:ring-2 focus:ring-offset-2',
  variants: {
    variant: {
      primary: 'bg-primary text-white hover:bg-primary-hover focus:ring-primary/30',
      secondary: 'bg-secondary text-white hover:bg-secondary-hover focus:ring-secondary/30',
      outline: 'border border-primary text-primary bg-transparent hover:bg-primary/10',
      ghost: 'text-primary bg-transparent hover:bg-primary/10',
      danger: 'bg-error text-white hover:bg-error-hover focus:ring-error/30'
    },
    size: {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg'
    },
    disabled: {
      true: 'opacity-50 cursor-not-allowed pointer-events-none'
    },
    loading: {
      true: 'pointer-events-none'
    }
  },
  compoundVariants: [
    {
      loading: true,
      class: 'relative text-transparent'
    }
  ],
  defaultVariants: {
    variant: 'primary',
    size: 'md'
  }
});

export type ButtonVariants = VariantProps<typeof button>;
```

### Multi-Part Component with Slots (Card)

```typescript
// components/ui/card.ts
import { tv, type VariantProps } from 'tailwind-variants';

export const card = tv({
  slots: {
    base: 'rounded-lg bg-surface overflow-hidden',
    header: 'px-4 py-3 border-b border-neutral-200',
    body: 'px-4 py-4',
    footer: 'px-4 py-3 border-t border-neutral-200 bg-neutral-50',
    title: 'text-lg font-semibold text-neutral-900',
    description: 'text-sm text-neutral-500'
  },
  variants: {
    variant: {
      default: { base: 'border border-neutral-200' },
      elevated: { base: 'shadow-md' },
      bordered: { base: 'border-2 border-neutral-300' }
    },
    padding: {
      sm: { body: 'px-3 py-2' },
      md: { body: 'px-4 py-4' },
      lg: { body: 'px-6 py-6' }
    }
  },
  defaultVariants: {
    variant: 'default',
    padding: 'md'
  }
});

export type CardVariants = VariantProps<typeof card>;
```

### Component Usage

```tsx
// Usage in React component
import { button, type ButtonVariants } from '@/components/ui/button';
import { card } from '@/components/ui/card';

// Button
<button className={button({ variant: 'primary', size: 'lg' })}>
  Click me
</button>

// Card with slots
const { base, header, body, title } = card({ variant: 'elevated' });
<div className={base()}>
  <div className={header()}>
    <h3 className={title()}>Card Title</h3>
  </div>
  <div className={body()}>Content here</div>
</div>
```

### Form Input with Compound Variants

```typescript
// components/ui/input.ts
import { tv } from 'tailwind-variants';

export const input = tv({
  base: 'w-full rounded-md border bg-surface px-3 py-2 text-base transition-colors focus:outline-none focus:ring-2',
  variants: {
    variant: {
      default: 'border-neutral-300 focus:border-primary focus:ring-primary/30',
      error: 'border-error focus:border-error focus:ring-error/30',
      success: 'border-success focus:border-success focus:ring-success/30'
    },
    size: {
      sm: 'px-2 py-1 text-sm',
      md: 'px-3 py-2 text-base',
      lg: 'px-4 py-3 text-lg'
    },
    disabled: {
      true: 'bg-neutral-100 cursor-not-allowed opacity-60'
    }
  },
  compoundVariants: [
    {
      variant: 'error',
      disabled: false,
      class: 'text-error'
    }
  ],
  defaultVariants: {
    variant: 'default',
    size: 'md'
  }
});
```
</tailwind_variants_output>

<brownfield_integration>
## Brownfield Project Integration

When extracting components for existing codebases, perform gap analysis first.

### Detection Phase

Check for existing component libraries:

```bash
# Detect from package.json
COMPONENT_LIB=$(jq -r '
  if .dependencies["@radix-ui/react-dialog"] then "radix"
  elif .dependencies["@chakra-ui/react"] then "chakra"
  elif .dependencies["@mui/material"] then "mui"
  elif .dependencies["tailwind-variants"] then "tv-ready"
  else "custom"
  end
' package.json 2>/dev/null || echo "none")

# Detect shadcn/ui (check for components/ui directory)
if [ -d "src/components/ui" ] || [ -d "components/ui" ]; then
  COMPONENT_LIB="shadcn"
fi
```

### Gap Analysis Output

Generate gap analysis in prototype-patterns.md:

```markdown
## Gap Analysis: Mockup vs Existing Components

### Brownfield Context
- **Component Library**: shadcn/ui
- **Design Tokens**: tailwind.config.js
- **Variant API**: tailwind-variants installed

### Component Comparison

| Mockup Component | Existing Match | Integration Mode | Gap Details |
|-----------------|----------------|------------------|-------------|
| Button (5 variants) | button.tsx (3 variants) | **Extend** | +ghost, +danger variants |
| Card (elevated) | card.tsx (flat only) | **Extend** | +elevated, +bordered variants |
| Avatar | ❌ None | **Create** | New component needed |
| Alert (4 types) | toast.tsx (2 types) | **Wrap** | Different API, wrap for compat |
| Modal | dialog.tsx | **Map** | Same function, different name |
| Badge | badge.tsx | **Use** | Exact match |

### Integration Modes

#### Extend (add variants to existing)
```typescript
// Existing: button.tsx has primary, secondary, outline
// Add: ghost, danger variants

// Option 1: Extend tv() definition
export const button = tv({
  extend: existingButton,  // Import existing
  variants: {
    variant: {
      ghost: 'text-primary bg-transparent hover:bg-primary/10',
      danger: 'bg-error text-white hover:bg-error-hover'
    }
  }
});

// Option 2: Merge variants
export const button = tv({
  ...existingButton.config,
  variants: {
    ...existingButton.config.variants,
    variant: {
      ...existingButton.config.variants.variant,
      ghost: '...',
      danger: '...'
    }
  }
});
```

#### Wrap (different API, create compatibility layer)
```typescript
// Existing: toast.tsx uses different props
// Mockup: Alert with variant="info|success|warning|error"

import { toast } from '@/components/ui/toast';

export const alert = tv({
  base: 'p-4 rounded-lg border',
  variants: {
    variant: {
      info: 'bg-info/10 border-info text-info',
      success: 'bg-success/10 border-success text-success',
      warning: 'bg-warning/10 border-warning text-warning',
      error: 'bg-error/10 border-error text-error'
    }
  }
});

// Wrapper component uses alert tv() but can fall back to toast
```

#### Create (no existing component)
```typescript
// No existing Avatar component - create new
export const avatar = tv({
  base: 'relative inline-flex shrink-0 overflow-hidden rounded-full',
  variants: {
    size: {
      sm: 'h-8 w-8',
      md: 'h-10 w-10',
      lg: 'h-12 w-12',
      xl: 'h-16 w-16'
    }
  },
  defaultVariants: { size: 'md' }
});
```

#### Map (same function, document alias)
```typescript
// Existing: dialog.tsx
// Mockup: calls it "Modal"
// Action: Create alias export

export { dialog as modal } from './dialog';
export type { DialogProps as ModalProps } from './dialog';
```
```

### Extraction Task Priority (Brownfield)

| Priority | Integration Mode | Action |
|----------|-----------------|--------|
| P0 | Create | New components (no existing match) |
| P1 | Extend | Add missing variants to existing |
| P2 | Wrap | Create compatibility layer |
| P3 | Map | Document alias only |

### Skip List

Components to skip extraction (exact match exists):

```yaml
skip_extraction:
  - badge        # Exact match in components/ui/badge.tsx
  - separator    # Exact match in components/ui/separator.tsx
  - skeleton     # Exact match in components/ui/skeleton.tsx
```
</brownfield_integration>
</detailed_procedures>

<validation>
## Validation Checklist

After extraction, verify:

### Pattern Coverage
- [ ] All repeated components identified
- [ ] Variant analysis complete
- [ ] State documentation complete
- [ ] Props interface defined

### Tailwind Mapping
- [ ] All CSS variables mapped
- [ ] No hardcoded values remain
- [ ] Responsive classes documented
- [ ] Dark mode considerations noted

### Visual Fidelity
- [ ] Spacing follows 8pt grid
- [ ] Colors use theme tokens
- [ ] Typography uses scale
- [ ] Shadows and borders consistent
</validation>

<references>
## Related Resources

- **Theme Definition**: `design/prototype/theme.yaml`
- **CSS Variables**: `design/prototype/theme.css`
- **Shared Styles**: `design/prototype/shared.css`
- **Extraction Rules**: `resources/extraction-rules.md`
- **CSS-Tailwind Mapping**: `resources/css-tailwind-mapping.md`
- **tailwind-variants Docs**: https://www.tailwind-variants.org/
- **tv() Slots API**: https://www.tailwind-variants.org/docs/slots
- **tv() Variants API**: https://www.tailwind-variants.org/docs/variants
</references>
