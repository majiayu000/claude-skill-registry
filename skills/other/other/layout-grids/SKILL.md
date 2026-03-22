---
name: layout-grids
description: "Create and apply grid systems, spacing rules, and layout structures for consistent, balanced designs. Use for: establishing grid systems, defining spacing scales, layout composition, responsive breakpoints, and visual rhythm."
---

# Layout Grids

## Description

Layout Grids establish the underlying structure for all visual layouts. A well-defined grid system ensures consistency, alignment, and predictable responsive behavior across all screens and components.

## When to Use

- After wireframes establish basic layout needs
- Setting up design system foundations
- Before designing detailed components
- Ensuring responsive design consistency
- When layouts feel misaligned or chaotic

---

## Instructions for AI Agents

### Step 1: Determine Grid Type

**Grid types by project:**

| Project Type | Recommended Grid | Rationale |
|--------------|------------------|----------|
| Marketing/Landing | 12-column | Flexible for varied layouts |
| Dashboard/App | 12-column with sidebar | Consistent app structure |
| Content/Blog | 12-column, content-centered | Reading focus |
| E-commerce | 12-column | Product grids flexibility |
| Mobile App | 4-column | Touch-friendly sizing |

### Step 2: Define Grid Specifications

**Grid system template:**

```markdown
## Grid System: [PROJECT]

### Desktop (1280px+)
| Property | Value |
|----------|-------|
| Container width | 1200px (max) |
| Columns | 12 |
| Column width | 72px (fluid) |
| Gutter | 24px |
| Margin (outside) | 32px |

### Tablet (768px - 1279px)
| Property | Value |
|----------|-------|
| Container width | 100% - 48px |
| Columns | 12 (or 8) |
| Gutter | 20px |
| Margin | 24px |

### Mobile (320px - 767px)
| Property | Value |
|----------|-------|
| Container width | 100% - 32px |
| Columns | 4 |
| Gutter | 16px |
| Margin | 16px |
```

### Step 3: Define Breakpoints

**Standard breakpoint system:**

```markdown
### Breakpoints

| Name | Min Width | Target Devices |
|------|-----------|----------------|
| xs | 0px | Small phones |
| sm | 640px | Large phones |
| md | 768px | Tablets portrait |
| lg | 1024px | Tablets landscape, laptops |
| xl | 1280px | Desktops |
| 2xl | 1536px | Large desktops |

### Mobile-First Approach
```css
/* Base styles: Mobile */
.element { ... }

/* Tablet and up */
@media (min-width: 768px) { ... }

/* Desktop and up */
@media (min-width: 1024px) { ... }
```
```

### Step 4: Column Layouts

**Common layout patterns:**

```markdown
### Layout Patterns

#### Full Width
```
│──────────── 12 columns ────────────│
```
Use: Hero sections, full-width images

#### Two Column (Equal)
```
│─── 6 col ───││─── 6 col ───│
```
Use: Feature comparisons, side-by-side content

#### Two Column (Sidebar)
```
│─ 3 ─││────── 9 columns ──────│
```
Use: Dashboard with navigation sidebar

#### Content + Sidebar
```
│───── 8 col ─────││─ 4 col ─│
```
Use: Blog posts with sidebar, forms with help

#### Three Column
```
│─ 4 col ─││─ 4 col ─││─ 4 col ─│
```
Use: Feature cards, product grid

#### Four Column
```
│ 3 ││ 3 ││ 3 ││ 3 │
```
Use: Stats, icon features, footer links

#### Centered Content
```
│ 2 ││───── 8 col ─────││ 2 │
```
Use: Article content, focused forms
```

### Step 5: Application Examples

**Grid in context:**

```markdown
### Page Layouts

#### Dashboard Layout
```
+---+----------------------------------+
|   |  Header (full width)             |
| S +----------------------------------+
| i |                                  |
| d |     Main Content Area            |
| e |     (9 columns)                  |
| b |                                  |
| a +----------------------------------+
| r |  (3 col spans height)            |
+---+----------------------------------+

Sidebar: 240px fixed
Content: Fluid (12-col grid within)
```

#### Landing Page
```
+--------------------------------------+
|  Nav (12 col, constrained center)    |
+--------------------------------------+
|                                      |
|  Hero (12 col, may break grid)       |
|                                      |
+--------------------------------------+
|  Features (4+4+4 or 6+6)             |
+--------------------------------------+
|  CTA (centered, 8 col)               |
+--------------------------------------+
|  Footer (12 col, 4+4+4)              |
+--------------------------------------+
```
```

---

## Example Input/Output

### Example Input

```markdown
**Project**: TaskFlow dashboard application
**Key layouts**: Dashboard, project list, task detail
**Sidebar needed**: Yes, persistent navigation
**Priority**: Desktop-first but responsive
```

### Example Output

```markdown
## Grid System: TaskFlow

### Overview

**Grid Type**: 12-column with fixed sidebar
**Approach**: Desktop-first with fluid content area

---

### Breakpoints

| Name | Width | Columns | Sidebar |
|------|-------|---------|--------|
| Mobile | <768px | 4 | Hidden (hamburger) |
| Tablet | 768-1023px | 8 | Collapsed (icons only) |
| Desktop | 1024-1439px | 12 | Full (240px) |
| Large | 1440px+ | 12 | Full (280px) |

---

### Grid Specifications

#### Desktop (1024px+)

```
┌───────┬─────────────────────────────────────────────┐
│       │  24px  │ col │ 24px │ col │ 24px │...     24px │
│ 240px │ margin │     │gutter│     │gutter│      margin │
│sidebar│        │     │      │     │      │             │
└───────┴────────┴─────┴──────┴─────┴──────┴─────────────┘

         │──────── 12-column grid ─────────│
```

**Specifications:**
| Property | Value |
|----------|-------|
| Sidebar width | 240px fixed |
| Content area | Fluid (remaining) |
| Columns in content | 12 |
| Gutter | 24px |
| Content margin | 24px (left/right) |
| Content max-width | 1200px |

#### Tablet (768-1023px)

**Specifications:**
| Property | Value |
|----------|-------|
| Sidebar width | 64px (icons only) |
| Columns | 8 |
| Gutter | 20px |
| Margin | 20px |

#### Mobile (<768px)

**Specifications:**
| Property | Value |
|----------|-------|
| Sidebar | Hidden (hamburger menu) |
| Columns | 4 |
| Gutter | 16px |
| Margin | 16px |

---

### Layout Templates

#### Dashboard Main
```
Desktop:
┌───────┬──────────────────────────────────────┐
│ Side  │  Page Header (12 col)              │
│  bar  ├────────────┬────────────┬────────────┤
│       │   Stat    │    Stat   │   Stat    │
│       │  (4 col)  │  (4 col)  │  (4 col)  │
│       ├────────────┴────────────┴────────────┤
│       │                                    │
│       │   Main Content (12 col)           │
│       │                                    │
└───────┴──────────────────────────────────────┘

Mobile:
┌───────────────┐
│  [☰] Header  │
├───────────────┤
│  Stat (full) │
├───────────────┤
│  Stat (full) │
├───────────────┤
│  Main (full) │
├───────────────┤
│  [Tab Bar]   │
└───────────────┘
```

#### Project List
```
Desktop: 4-column card grid
│ Card │ Card │ Card │ Card │  (3-col each)
│ Card │ Card │ Card │ Card │

Tablet: 2-column
│ Card │ Card │  (4-col each)
│ Card │ Card │

Mobile: 1-column
│ Card (full) │
│ Card (full) │
```

#### Task Detail (Side Panel)
```
Desktop:
┌───────┬────────────────────┬──────────────┐
│ Side  │   Task List      │  Task Detail  │
│  bar  │   (7 col)        │   (5 col)     │
│       │                  │   Slides in   │
└───────┴────────────────────┴──────────────┘

Mobile: Full-screen overlay
```

---

### CSS Implementation

```css
/* Grid Container */
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
  padding: 0 24px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Span utilities */
.col-span-12 { grid-column: span 12; }
.col-span-8 { grid-column: span 8; }
.col-span-6 { grid-column: span 6; }
.col-span-4 { grid-column: span 4; }
.col-span-3 { grid-column: span 3; }

/* Responsive */
@media (max-width: 1023px) {
  .grid-container {
    grid-template-columns: repeat(8, 1fr);
    gap: 20px;
    padding: 0 20px;
  }
}

@media (max-width: 767px) {
  .grid-container {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    padding: 0 16px;
  }
  
  .col-span-6,
  .col-span-4,
  .col-span-3 {
    grid-column: span 4; /* Full width on mobile */
  }
}
```

---

### Design Tokens

```json
{
  "grid": {
    "columns": 12,
    "gutter": {
      "desktop": "24px",
      "tablet": "20px",
      "mobile": "16px"
    },
    "margin": {
      "desktop": "24px",
      "tablet": "20px", 
      "mobile": "16px"
    },
    "maxWidth": "1200px"
  },
  "sidebar": {
    "widthFull": "240px",
    "widthCollapsed": "64px"
  },
  "breakpoints": {
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
    "2xl": "1536px"
  }
}
```
```

---

## Prompts Library

### Quick Grid Setup
```
Create a grid system for [PROJECT TYPE]:
- Primary device: [Desktop/Mobile]
- Sidebar needed: [Yes/No]
- Max content width: [Width]

Provide: breakpoints, column count, gutter sizes, margin sizes
```

### Layout Pattern
```
How should this content be laid out:
[CONTENT DESCRIPTION]

On:
- Desktop (12 columns)
- Tablet (8 columns)
- Mobile (4 columns)

Provide column spans for each element at each breakpoint.
```

---

## Success Criteria

### Minimum Requirements
- [ ] Column system defined
- [ ] Gutter sizes specified
- [ ] Breakpoints established
- [ ] Key layouts mapped to grid
- [ ] Responsive behavior documented

### Quality Indicators
- [ ] Grid supports all wireframed layouts
- [ ] Consistent spacing throughout
- [ ] Mobile-friendly column collapse
- [ ] Flexible for future layouts

---

## Related Skills

- **Previous**: `wireframing.md` - Layout structure to formalize
- **Next**: `spacing_rhythm.md` - Vertical spacing complements grid
- **Related**: `responsive_design.md` - Grid enables responsiveness
