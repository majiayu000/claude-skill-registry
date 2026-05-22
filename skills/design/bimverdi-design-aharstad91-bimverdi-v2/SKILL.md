---
name: bimverdi-design
description: Generate BIM Verdi UI components and pages following the established design system. Use when building templates, components, or any frontend for bimverdi.no. Enforces enterprise-calm aesthetics and avoids generic AI patterns.
---

# BIM Verdi Design Skill

This skill generates frontend code for BIM Verdi (bimverdi.no) that follows the established design system and avoids generic "AI slop" aesthetics.

## Anti-Pattern Awareness

LLMs naturally converge toward high-probability outputs. In frontend design, this creates generic results. **Avoid these AI defaults:**

| AI Default | BIM Verdi Instead |
|------------|-------------------|
| Inter font everywhere | Moderat (fallback: Inter) |
| Purple/blue gradients | Warm orange #FF8B5E accent |
| Cards with shadows everywhere | Borderless sections + dividers |
| Rounded corners (16px+) | Subtle radius (8px buttons, 12px cards) |
| Heavy drop shadows | No shadows or very subtle |
| Hover on containers | Hover ONLY on interactive elements |
| Generic placeholder text | Real Norwegian content |

## Design Philosophy

**Variant B: Dividers & Whitespace** is the standard.

Core principles:
- **P1:** Whitespace + hairline dividers are primary structure (not boxes)
- **P2:** Only buttons, links, menu items are clickable
- **P3:** Information = borderless sections; Actions = buttons/links
- **P4:** Never show empty fields (hide or show "Ikke oppgitt")
- **P5:** Calm, consistent enterprise style (minimal visual noise)

## Color Palette

```css
/* Primary */
--color-primary: #FF8B5E;        /* Warm orange - main accent */
--color-primary-dark: #E67A4E;
--color-primary-light: #FFBFA8;

/* Neutrals */
--color-black: #1A1A1A;          /* Primary text */
--color-gray-dark: #383838;
--color-gray-medium: #888888;
--color-gray-light: #D1D1D1;
--color-white: #FFFFFF;

/* Backgrounds */
--color-beige: #F7F5EF;          /* Warm off-white */
--color-beige-dark: #EFE9DE;
body background: #FAFAF8;

/* State */
--color-success: #B3DB87;
--color-error: #772015;
--color-alert: #FFC845;
--color-info: #005898;
```

**Usage rules:**
- Primary orange: CTA buttons, active states, important links
- Never introduce new accent colors without explicit decision
- Text is always #1A1A1A or #383838
- Backgrounds are warm (beige family), never pure white or gray

## Typography

**Font stack:** `'Moderat', 'Inter', system-ui, -apple-system, sans-serif`

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 | 3rem (48px) | 700 | 1.2 |
| H2 | 2rem (32px) | 700 | 1.2 |
| H3 | 1.5rem (24px) | 600 | 1.2 |
| H4 | 1.25rem (20px) | 600 | 1.2 |
| Body | 1rem (16px) | 400 | 1.5-1.75 |
| Small | 0.875rem (14px) | 400 | 1.5 |

**Rules:**
- No ALL CAPS except sparingly for labels/overlines
- Semantic heading order (H1 -> H2 -> H3)
- Good line height for readability

## Spacing System

8px base scale: `4, 8, 12, 16, 24, 32, 40, 48, 64`

```css
--spacing-xs: 0.5rem;   /* 8px */
--spacing-sm: 1rem;     /* 16px */
--spacing-md: 1.5rem;   /* 24px */
--spacing-lg: 2rem;     /* 32px */
--spacing-xl: 3rem;     /* 48px */
--spacing-2xl: 4rem;    /* 64px */
```

**Use few, consistent spacing values per page.**

## Layout Widths

| Context | Max Width |
|---------|-----------|
| Standard content | 1200-1280px |
| Forms/flows | 960px |
| Side gutters | Consistent, responsive |

## Buttons

**Standard button:** 36px height, 8px radius, Inter Medium 14px

```html
<!-- Primary (filled black) -->
<a href="#" class="bv-btn bv-btn--primary">
  <span class="bv-btn__text">Lagre</span>
</a>

<!-- Secondary (outline) -->
<a href="#" class="bv-btn bv-btn--secondary">
  <span class="bv-btn__text">Avbryt</span>
</a>

<!-- Tertiary (ghost) -->
<a href="#" class="bv-btn bv-btn--tertiary">
  <span class="bv-btn__text">Se mer</span>
</a>

<!-- With icon -->
<a href="#" class="bv-btn bv-btn--primary">
  <span class="bv-btn__icon">[lucide-icon]</span>
  <span class="bv-btn__text">Nytt verktoy</span>
</a>
```

**Sizes:** `--small` (28px), `--medium` (36px), `--large` (44px)

## Icons

**Framework:** Lucide Icons (https://lucide.dev)

| Icon | Usage |
|------|-------|
| `layout-dashboard` | Dashboard |
| `wrench` | Verktoy |
| `file-text` | Artikler |
| `lightbulb` | Prosjektideer |
| `calendar` | Arrangementer |
| `user` | Brukerprofil |
| `building-2` | Bedrift/Foretak |
| `chevron-right` | Navigate |
| `plus` | Add new |
| `pencil` | Edit |
| `trash-2` | Delete |

**Sizes:** 16px (small), 20px (medium), 24px (large)

## Containers & Sections

**Default:** Borderless sections with dividers

```html
<!-- Standard section -->
<section class="bv-section">
  <h2 class="bv-section__title">Oversikt</h2>
  <p class="bv-section__helper">Valgfri hjelpetekst</p>
  <div class="bv-section__content">
    <!-- Content here -->
  </div>
</section>
<hr class="bv-divider">
```

**Soft panels** (rare, only for action groups):
- No shadow
- Subtle background (#F7F5EF) or hairline border
- Never hoverable

## Cards

**Cards are NOT clickable** unless explicitly designed with:
1. Explicit "Se detaljer" link + chevron
2. Defined hover/focus states
3. Documented as exception

```html
<!-- Non-clickable info card -->
<div class="bv-card">
  <div class="bv-card__header">
    <h3 class="bv-card__title">Tittel</h3>
  </div>
  <div class="bv-card__body">
    <p>Innhold</p>
  </div>
  <div class="bv-card__footer">
    <a href="#" class="bv-btn bv-btn--tertiary">
      Se detaljer
      <span class="bv-btn__icon">[chevron-right]</span>
    </a>
  </div>
</div>
```

## Dividers

Hairline divider: 1px, low contrast (#E5E5E5 or similar)

```html
<hr class="bv-divider">
```

## Forms

**Layout:** 960px max-width, centered

```html
<div class="bv-form-layout">
  <div class="bv-form-section">
    <h3>Seksjonstittel</h3>
    <div class="bv-form-group">
      <label for="field">Feltnavn</label>
      <input type="text" id="field" name="field">
    </div>
  </div>
  <hr class="bv-divider">
  <!-- More sections -->
</div>
```

**Sticky actions bar:**
```html
<div class="bv-form-actions bv-form-actions--sticky">
  <a href="#" class="bv-btn bv-btn--tertiary">Avbryt</a>
  <a href="#" class="bv-btn bv-btn--secondary">Lagre som kladd</a>
  <button type="submit" class="bv-btn bv-btn--primary">Lagre</button>
</div>
```

## Page Templates

### Archive page (e.g., /deltakere/)
```
PageHeader: Title + count + primary action button
|
Filter/search (if applicable)
|
Grid/List of items
|
Pagination
```

### Single page (e.g., /deltakere/firmanavn/)
```
Breadcrumb
|
PageHeader: Title + actions (Edit, etc.)
|
Two-column layout:
  Left: Borderless sections (Oversikt, Detaljer)
  Right: Aside blocks (Status, Snarveier)
```

### Form page (e.g., /min-side/nytt-verktoy/)
```
Breadcrumb
|
PageHeader: Title + helper text
|
960px form layout with sections + dividers
|
Sticky action bar
```

## Interaction Rules

**Clickable elements MUST be:**
- `<button>` or button component
- `<a>` or link component
- Menu item
- Explicit row action with icon + label

**Hover states:**
- ONLY on interactive elements
- Links: underline on hover
- Buttons: background change
- Containers: NEVER hover

**Focus states:**
- Always visible (outline/ring)
- WCAG AA compliant

## WordPress/PHP Context

This is a WordPress theme. Use:
- PHP for templates (`single-foretak.php`, `archive-foretak.php`)
- ACF fields for custom data
- Existing CSS classes from design-system.php
- Lucide icons as inline SVG

**Template structure:**
```php
<?php get_header(); ?>

<main class="bv-main">
  <div class="bv-container">
    <!-- Page content -->
  </div>
</main>

<?php get_footer(); ?>
```

## Checklist Before Generating

When generating UI code, verify:

- [ ] Using existing CSS classes from design-system.php
- [ ] Following Variant B (dividers/whitespace, not boxes)
- [ ] Containers are NOT clickable
- [ ] Only interactive elements have hover/pointer
- [ ] Empty fields hidden or show "Ikke oppgitt"
- [ ] Layout widths: 1200-1280 standard, 960 for forms
- [ ] Spacing on 8px scale
- [ ] Colors from palette only
- [ ] Lucide icons only
- [ ] Norwegian text (not lorem ipsum)
- [ ] Semantic HTML (proper headings, buttons vs links)
- [ ] Accessible (labels, focus states, contrast)
