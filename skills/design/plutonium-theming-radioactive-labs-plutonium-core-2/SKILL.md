---
name: plutonium-theming
description: Plutonium design token system - CSS custom properties, component classes, and consistent styling patterns
---

# Plutonium Design Token System

Plutonium uses a comprehensive CSS design token system for consistent, themeable UI components. This system provides CSS custom properties and reusable component classes that automatically support light and dark modes.

## CSS Design Tokens

Design tokens are defined in `src/css/tokens.css` and provide the foundation for all UI styling.

### Surface & Background Colors

```css
/* Light mode */
--pu-body: #f8fafc;              /* Page background */
--pu-surface: #ffffff;            /* Main surface (cards, panels) */
--pu-surface-alt: #f1f5f9;        /* Alternate surface (headers) */
--pu-surface-raised: #ffffff;     /* Elevated elements */
--pu-surface-overlay: rgba(255, 255, 255, 0.95);

/* Dark mode (.dark class) */
--pu-body: #0f172a;
--pu-surface: #1e293b;
--pu-surface-alt: #0f172a;
--pu-surface-raised: #334155;
--pu-surface-overlay: rgba(30, 41, 59, 0.95);
```

### Text Colors

```css
/* Light mode */
--pu-text: #0f172a;               /* Primary text */
--pu-text-muted: #64748b;         /* Secondary text */
--pu-text-subtle: #94a3b8;        /* Tertiary/disabled text */

/* Dark mode */
--pu-text: #f8fafc;
--pu-text-muted: #94a3b8;
--pu-text-subtle: #64748b;
```

### Border Colors

```css
/* Light mode */
--pu-border: #e2e8f0;             /* Standard borders */
--pu-border-muted: #f1f5f9;       /* Subtle borders */
--pu-border-strong: #cbd5e1;      /* Emphasized borders */

/* Dark mode */
--pu-border: #334155;
--pu-border-muted: #1e293b;
--pu-border-strong: #475569;
```

### Form Tokens

```css
--pu-input-bg: #ffffff;           /* Input background */
--pu-input-border: #e2e8f0;       /* Input border */
--pu-input-focus-ring: theme(colors.primary.500);
--pu-input-placeholder: #94a3b8;  /* Placeholder text */
```

### Card Tokens

```css
--pu-card-bg: #ffffff;
--pu-card-border: #e2e8f0;
```

### Shadow System

```css
--pu-shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.03), 0 1px 3px 0 rgb(0 0 0 / 0.05);
--pu-shadow-md: 0 2px 4px -1px rgb(0 0 0 / 0.04), 0 4px 6px -1px rgb(0 0 0 / 0.06);
--pu-shadow-lg: 0 4px 6px -2px rgb(0 0 0 / 0.03), 0 10px 15px -3px rgb(0 0 0 / 0.08);
```

### Border Radius

```css
--pu-radius-sm: 0.375rem;         /* 6px */
--pu-radius-md: 0.5rem;           /* 8px */
--pu-radius-lg: 0.75rem;          /* 12px */
--pu-radius-xl: 1rem;             /* 16px */
--pu-radius-full: 9999px;         /* Fully rounded */
```

### Spacing

```css
--pu-space-xs: 0.25rem;           /* 4px */
--pu-space-sm: 0.5rem;            /* 8px */
--pu-space-md: 1rem;              /* 16px */
--pu-space-lg: 1.5rem;            /* 24px */
--pu-space-xl: 2rem;              /* 32px */
```

### Transitions

```css
--pu-transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
--pu-transition-normal: 200ms cubic-bezier(0.4, 0, 0.2, 1);
--pu-transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
```

## Component Classes

Component classes are defined in `src/css/components.css` and provide ready-to-use styled components.

### Buttons

Base class with size variants:

```css
.pu-btn        /* Base button styles */
.pu-btn-md     /* Medium size (default) */
.pu-btn-sm     /* Small size */
.pu-btn-xs     /* Extra small size */
```

Solid variants (with hover lift animation):

```css
.pu-btn-primary    /* Primary action */
.pu-btn-secondary  /* Secondary action */
.pu-btn-danger     /* Destructive action */
.pu-btn-success    /* Success action */
.pu-btn-warning    /* Warning action */
.pu-btn-info       /* Informational action */
.pu-btn-accent     /* Accent action */
```

Other variants:

```css
.pu-btn-ghost      /* Minimal, text-like */
.pu-btn-outline    /* Bordered, transparent background */
```

Soft variants (tinted backgrounds for secondary contexts):

```css
.pu-btn-soft-primary
.pu-btn-soft-danger
.pu-btn-soft-success
.pu-btn-soft-warning
.pu-btn-soft-info
.pu-btn-soft-secondary
.pu-btn-soft-accent
```

Usage:

```erb
<%= form.submit "Save", class: "pu-btn pu-btn-md pu-btn-primary" %>
<%= form.submit "Delete", class: "pu-btn pu-btn-md pu-btn-danger" %>
<%= form.submit "Disable", class: "pu-btn pu-btn-md pu-btn-warning" %>
```

### Form Inputs

```css
.pu-input          /* Base input styles */
.pu-input-invalid  /* Error state */
.pu-input-valid    /* Valid state */
```

Usage:

```erb
<%= form.text_field :name, class: "pu-input #{errors? ? 'pu-input-invalid' : ''}" %>
```

### Labels & Text

```css
.pu-label          /* Form labels */
.pu-label-required /* Adds red asterisk after label */
.pu-hint           /* Helper text below inputs */
.pu-error          /* Error messages */
```

Usage:

```erb
<%= form.label :email, class: "pu-label" %>
<span class="pu-error">Email is required</span>
```

### Checkboxes

```css
.pu-checkbox       /* Styled checkbox/radio */
```

Usage:

```erb
<%= form.check_box :remember_me, class: "pu-checkbox" %>
```

### Cards

```css
.pu-card           /* Card container with border, shadow, radius */
.pu-card-body      /* Card content padding */
```

### Panels

```css
.pu-panel-header      /* Panel header with background */
.pu-panel-title       /* Panel title text */
.pu-panel-description /* Panel description text */
```

### Tables

```css
.pu-table-wrapper     /* Scrollable container with card styling */
.pu-table             /* Base table styles */
.pu-table-header      /* Header row */
.pu-table-header-cell /* Header cell */
.pu-table-body-row    /* Body row with hover */
.pu-table-body-row-selected /* Selected row */
.pu-table-body-cell   /* Body cell */
.pu-selection-cell    /* Checkbox column */
```

### Toolbar

```css
.pu-toolbar        /* Toolbar container with gradient */
.pu-toolbar-text   /* Toolbar text */
.pu-toolbar-actions /* Toolbar action buttons */
```

### Empty State

```css
.pu-empty-state             /* Centered container */
.pu-empty-state-icon        /* Icon styling */
.pu-empty-state-title       /* Title text */
.pu-empty-state-description /* Description text */
```

## Ruby Component Classes

The `Plutonium::UI::ComponentClasses` module provides Ruby constants for consistent class usage.

Location: `lib/plutonium/ui/component_classes.rb`

### Button Classes

```ruby
ComponentClasses::Button::BASE          # "pu-btn"
ComponentClasses::Button::SIZE_DEFAULT  # "pu-btn-md"
ComponentClasses::Button::SIZE_SM       # "pu-btn-sm"
ComponentClasses::Button::SIZE_XS       # "pu-btn-xs"

ComponentClasses::Button::VARIANTS[:primary]   # "pu-btn-primary"
ComponentClasses::Button::VARIANTS[:danger]    # "pu-btn-danger"
ComponentClasses::Button::SOFT_VARIANTS[:primary] # "pu-btn-soft-primary"

# Helper method
ComponentClasses::Button.classes(variant: :primary, size: :default, soft: false)
# => "pu-btn pu-btn-md pu-btn-primary"
```

### Form Classes

```ruby
ComponentClasses::Form::INPUT         # "pu-input"
ComponentClasses::Form::INPUT_INVALID # "pu-input pu-input-invalid"
ComponentClasses::Form::INPUT_VALID   # "pu-input pu-input-valid"
ComponentClasses::Form::LABEL         # "pu-label"
ComponentClasses::Form::HINT          # "pu-hint"
ComponentClasses::Form::ERROR         # "pu-error"
ComponentClasses::Form::BUTTON        # "pu-btn pu-btn-md pu-btn-primary"
```

### Table Classes

```ruby
ComponentClasses::Table::WRAPPER          # "pu-table-wrapper"
ComponentClasses::Table::BASE             # "pu-table"
ComponentClasses::Table::HEADER           # "pu-table-header"
ComponentClasses::Table::HEADER_CELL      # "pu-table-header-cell"
ComponentClasses::Table::BODY_ROW         # "pu-table-body-row"
ComponentClasses::Table::BODY_ROW_SELECTED # "pu-table-body-row-selected"
ComponentClasses::Table::BODY_CELL        # "pu-table-body-cell"
ComponentClasses::Table::CHECKBOX         # "pu-checkbox"
```

### Card Classes

```ruby
ComponentClasses::Card::BASE        # "pu-card"
ComponentClasses::Card::BODY        # "pu-card-body"
ComponentClasses::Card::HEADER      # "pu-panel-header"
ComponentClasses::Card::TITLE       # "pu-panel-title"
ComponentClasses::Card::DESCRIPTION # "pu-panel-description"
```

## Using Tokens in Templates

### ERB Templates

```erb
<%# Text colors %>
<h1 class="text-[var(--pu-text)]">Title</h1>
<p class="text-[var(--pu-text-muted)]">Description</p>

<%# Surfaces %>
<div class="bg-[var(--pu-surface)] border border-[var(--pu-border)] rounded-[var(--pu-radius-lg)]">
  Content
</div>

<%# With shadows %>
<div class="bg-[var(--pu-card-bg)]" style="box-shadow: var(--pu-shadow-md)">
  Card content
</div>

<%# Form fields %>
<%= form.label :name, class: "pu-label" %>
<%= form.text_field :name, class: "pu-input" %>
<span class="pu-error">Error message</span>

<%# Buttons %>
<%= form.submit "Save", class: "w-full pu-btn pu-btn-md pu-btn-primary" %>
```

### Phlex Components

```ruby
class MyComponent < Plutonium::UI::Component::Base
  def view_template
    div(class: "bg-[var(--pu-surface)] border border-[var(--pu-border)] rounded-[var(--pu-radius-lg)]",
        style: "box-shadow: var(--pu-shadow-md)") {
      h2(class: "text-lg font-semibold text-[var(--pu-text)]") { "Title" }
      p(class: "text-[var(--pu-text-muted)]") { "Description" }
    }
  end
end
```

## Link Styling Patterns

Plutonium uses consistent link styling patterns:

```erb
<%# Primary links %>
<%= link_to "Link", path, class: "font-medium text-secondary-600 dark:text-secondary-400 hover:underline transition-colors" %>

<%# Muted links %>
<%= link_to "Link", path, class: "text-[var(--pu-text-muted)] hover:text-primary-600 transition-colors" %>
```

## Dark Mode

All tokens automatically switch values when the `.dark` class is present on `<html>`:

```html
<!-- Light mode -->
<html>
  <body class="bg-[var(--pu-body)]">...</body>
</html>

<!-- Dark mode -->
<html class="dark">
  <body class="bg-[var(--pu-body)]">...</body>
</html>
```

No additional classes needed - tokens handle the switch automatically.

## Customizing Tokens

Override tokens in your application CSS:

```css
/* app/assets/stylesheets/application.tailwind.css */
@import "gem:plutonium/src/css/plutonium.css";
@import "tailwindcss";

:root {
  /* Override light mode tokens */
  --pu-surface: #fafafa;
  --pu-border: #d1d5db;
}

.dark {
  /* Override dark mode tokens */
  --pu-surface: #111827;
  --pu-border: #374151;
}
```

## Migration from Hardcoded Classes

When updating views to use the design token system:

| Old Pattern | New Pattern |
|-------------|-------------|
| `text-gray-900 dark:text-white` | `text-[var(--pu-text)]` |
| `text-gray-500 dark:text-gray-400` | `text-[var(--pu-text-muted)]` |
| `bg-gray-50 dark:bg-gray-700` | `bg-[var(--pu-surface)]` |
| `border-gray-300 dark:border-gray-600` | `border-[var(--pu-border)]` |
| `bg-gray-50 border ... (long input class)` | `pu-input` |
| `block mb-2 text-sm font-semibold ...` | `pu-label` |
| `text-red-600 dark:text-red-400` | `pu-error` |
| `(long button class)` | `pu-btn pu-btn-md pu-btn-primary` |

## Related Skills

- `plutonium-assets` - TailwindCSS configuration and asset setup
- `plutonium-forms` - Form component customization
- `plutonium-views` - View and layout customization
