---
name: typography
description: "Select typefaces, establish type scales, and create typographic hierarchies for readable, beautiful text. Use for: font selection, type scale creation, hierarchy definition, readability optimization, and typographic systems."
---

# Typography

## Description

Typography creates a hierarchical type system that ensures readability, establishes visual hierarchy, and expresses brand personality through careful font selection, sizing, and spacing.

## When to Use

- After color palette is established
- Setting up design system foundations
- When existing typography needs refinement
- Ensuring reading comfort and accessibility
- Creating consistent content presentation

---

## Instructions for AI Agents

### Step 1: Font Selection Strategy

**Prompt for font direction:**
```
Based on:
- Brand personality: [TRAITS]
- Industry: [INDUSTRY]
- Audience tech level: [LEVEL]
- Comparable brands: [REFERENCES]

Recommend:
1. Heading font characteristics (geometric, humanist, serif, etc.)
2. Body font characteristics (optimized for screens)
3. Accent/display font if needed
4. Specific font suggestions from Google Fonts
```

### Step 2: Font Pairing

**Classic pairing patterns:**

| Pattern | Heading | Body | Personality |
|---------|---------|------|-------------|
| Modern Tech | Geometric sans (Inter, Outfit) | Same | Clean, precise |
| Traditional | Serif (Playfair, Lora) | Sans (Source Sans) | Elegant, trustworthy |
| Friendly | Rounded sans (Nunito) | Clean sans (Open Sans) | Approachable |
| Premium | Elegant sans (Satoshi) | Same | Sophisticated |
| Editorial | Serif (Fraunces) | Serif (Source Serif) | Authoritative |
| Playful | Display (Clash) | Readable (DM Sans) | Creative, bold |

**Pairing rules:**
1. Maximum 2 font families (3 if including code)
2. Contrast in style OR weight, not both
3. Similar x-height for harmony
4. Body font must be highly readable at 16px

### Step 3: Create Type Scale

**Scale generation formula:**

```markdown
## Type Scale

Base size: 16px (1rem)
Scale ratio: 1.25 (Major Third) — Good for web apps

| Name | Size | Line Height | Weight | Usage |
|------|------|-------------|--------|-------|
| Display | 3.815rem (61px) | 1.1 | 700 | Hero headlines |
| H1 | 3.052rem (49px) | 1.2 | 700 | Page titles |
| H2 | 2.441rem (39px) | 1.2 | 600 | Section heads |
| H3 | 1.953rem (31px) | 1.3 | 600 | Subsections |
| H4 | 1.563rem (25px) | 1.4 | 600 | Card titles |
| H5 | 1.25rem (20px) | 1.4 | 600 | Small headings |
| Body Large | 1.125rem (18px) | 1.6 | 400 | Lead paragraphs |
| Body | 1rem (16px) | 1.6 | 400 | Main content |
| Body Small | 0.875rem (14px) | 1.5 | 400 | Secondary content |
| Caption | 0.75rem (12px) | 1.4 | 400 | Labels, captions |
| Overline | 0.75rem (12px) | 1.4 | 500 | Category labels |
```

**Common scale ratios:**
| Ratio | Name | Best For |
|-------|------|----------|
| 1.125 | Major Second | Compact UI, mobile |
| 1.2 | Minor Third | General purpose |
| 1.25 | Major Third | Web apps, dashboards |
| 1.333 | Perfect Fourth | Marketing sites |
| 1.5 | Perfect Fifth | Bold, editorial |

### Step 4: Define Typography Styles

**Complete typography system:**

```markdown
## Typography System: [PROJECT]

### Font Stack

**Primary (Headings + Body)**
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 
             'Segoe UI', Roboto, sans-serif;
```

**Code/Monospace**
```css
font-family: 'JetBrains Mono', 'Fira Code', monospace;
```

### Heading Styles

| Element | Font | Size | Weight | Line Height | Letter Spacing | Color |
|---------|------|------|--------|-------------|----------------|-------|
| H1 | Inter | 48px | 700 | 1.2 | -0.02em | Slate-900 |
| H2 | Inter | 36px | 600 | 1.25 | -0.01em | Slate-900 |
| H3 | Inter | 28px | 600 | 1.3 | 0 | Slate-900 |
| H4 | Inter | 22px | 600 | 1.35 | 0 | Slate-800 |
| H5 | Inter | 18px | 600 | 1.4 | 0 | Slate-800 |
| H6 | Inter | 16px | 600 | 1.4 | 0 | Slate-700 |

### Body Styles

| Style | Font | Size | Weight | Line Height | Color |
|-------|------|------|--------|-------------|-------|
| Body Large | Inter | 18px | 400 | 1.6 | Slate-700 |
| Body | Inter | 16px | 400 | 1.6 | Slate-700 |
| Body Small | Inter | 14px | 400 | 1.5 | Slate-600 |
| Caption | Inter | 12px | 400 | 1.4 | Slate-500 |

### Special Styles

| Style | Font | Size | Weight | Transform | Spacing | Usage |
|-------|------|------|--------|-----------|---------|-------|
| Overline | Inter | 12px | 500 | UPPERCASE | 0.1em | Labels |
| Button | Inter | 14px | 500 | None | 0.02em | Buttons |
| Link | Inter | inherit | 500 | None | 0 | Links |
| Code Inline | JetBrains | 14px | 400 | None | 0 | Code |
```

### Step 5: Responsive Typography

**Fluid typography approach:**

```markdown
### Responsive Adjustments

| Element | Mobile (<768px) | Tablet (768-1024px) | Desktop (>1024px) |
|---------|-----------------|---------------------|-------------------|
| H1 | 32px | 40px | 48px |
| H2 | 26px | 32px | 36px |
| H3 | 22px | 26px | 28px |
| Body | 16px | 16px | 16px |
| Body Small | 14px | 14px | 14px |
```

**CSS Clamp example:**
```css
h1 {
  font-size: clamp(2rem, 5vw + 1rem, 3rem);
}
```

---

## Example Input/Output

### Example Input

```markdown
**Project**: TaskFlow - SaaS project management
**Personality**: Modern, professional, approachable
**Primary device**: Desktop (dashboard heavy)
**Existing colors**: Purple primary, warm amber accent
```

### Example Output

```markdown
## Typography System: TaskFlow

### Font Selection

**Primary Font: Inter**
- Why: Modern, highly readable, excellent for UI
- Variable font for performance
- Great number legibility (important for dashboards)
- Wide language support

**Alternative: Satoshi** (if more personality needed)
- Slightly more distinctive
- Same excellent readability

**Code Font: JetBrains Mono**
- Excellent for any code/technical content
- Clear number differentiation

### Type Scale (Major Third - 1.25)

| Token | Size | Line Height | Weight | Usage |
|-------|------|-------------|--------|-------|
| `text-display` | 48px | 1.1 | 700 | Marketing hero |
| `text-h1` | 36px | 1.2 | 700 | Page titles |
| `text-h2` | 28px | 1.25 | 600 | Section headings |
| `text-h3` | 22px | 1.3 | 600 | Card headings, modals |
| `text-h4` | 18px | 1.35 | 600 | Subsections |
| `text-lg` | 18px | 1.6 | 400 | Lead paragraphs |
| `text-base` | 16px | 1.6 | 400 | Body text |
| `text-sm` | 14px | 1.5 | 400 | Secondary text, forms |
| `text-xs` | 12px | 1.4 | 400 | Captions, timestamps |

### Complete Style Definitions

#### Headings

```css
/* H1 - Page Titles */
.text-h1 {
  font-family: 'Inter', sans-serif;
  font-size: 36px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: #0F172A; /* Slate-900 */
}

/* H2 - Section Headings */
.text-h2 {
  font-family: 'Inter', sans-serif;
  font-size: 28px;
  font-weight: 600;
  line-height: 1.25;
  letter-spacing: -0.01em;
  color: #0F172A;
}

/* H3 - Card/Modal Headings */
.text-h3 {
  font-family: 'Inter', sans-serif;
  font-size: 22px;
  font-weight: 600;
  line-height: 1.3;
  letter-spacing: 0;
  color: #1E293B; /* Slate-800 */
}

/* H4 - Small Headings */
.text-h4 {
  font-family: 'Inter', sans-serif;
  font-size: 18px;
  font-weight: 600;
  line-height: 1.35;
  color: #1E293B;
}
```

#### Body Text

```css
/* Body - Default */
.text-body {
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.6;
  color: #334155; /* Slate-700 */
}

/* Body Small - Secondary */
.text-sm {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.5;
  color: #475569; /* Slate-600 */
}

/* Caption - Tertiary */
.text-caption {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 400;
  line-height: 1.4;
  color: #64748B; /* Slate-500 */
}
```

#### UI Elements

```css
/* Button Text */
.text-button {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 500;
  line-height: 1;
  letter-spacing: 0.02em;
}

/* Label */
.text-label {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.4;
  color: #334155;
}

/* Overline */
.text-overline {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  font-weight: 500;
  line-height: 1.4;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #64748B;
}

/* Link */
.text-link {
  font-weight: 500;
  color: #7C3AED; /* Violet-600 */
  text-decoration: underline;
  text-underline-offset: 2px;
}
.text-link:hover {
  color: #8B5CF6; /* Violet-500 */
}

/* Code Inline */
.text-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  background: #F1F5F9;
  padding: 0.125em 0.375em;
  border-radius: 4px;
}
```

### Responsive Behavior

| Style | Mobile | Tablet | Desktop |
|-------|--------|--------|----------|
| H1 | 28px | 32px | 36px |
| H2 | 24px | 26px | 28px |
| H3 | 20px | 22px | 22px |
| Body | 16px | 16px | 16px |

```css
/* Fluid H1 */
.text-h1 {
  font-size: clamp(1.75rem, 3vw + 0.5rem, 2.25rem);
}
```

### Usage Guidelines

#### Hierarchy in Practice

```
Page Title (H1)
  Section (H2)
    Subsection (H3)
      Card title (H4)
        Body text
          Caption/meta
```

#### Reading Comfort
- Maximum line width: 65-75 characters
- Minimum body size: 16px
- Paragraph spacing: 1em (16px)
- Section spacing: 2-3em

#### Don't
- Never go below 12px for any text
- Don't use more than 3 font weights on one page
- Avoid centered text for paragraphs >3 lines
- Don't mix too many heading levels in one view
```

---

## Prompts Library

### Font Pairing
```
Suggest 3 Google Font pairings for a [PROJECT TYPE] that feels [PERSONALITY]:

1. Option A: [Heading] + [Body] - [Why it works]
2. Option B: [Heading] + [Body] - [Why it works]
3. Option C: [Heading] + [Body] - [Why it works]

Include: Font names, weights to use, sample CSS
```

### Type Scale Generation
```
Generate a type scale for [PROJECT] using:
- Base size: 16px
- Ratio: [1.2/1.25/1.333]
- Platform: [Web app/Marketing/Mobile]

Include sizes from 12px caption to display heading.
```

### Typography Audit
```
Review this typography setup:
[CURRENT STYLES]

Check:
1. Is the hierarchy clear?
2. Are there too many variations?
3. Is it accessible (size, contrast, spacing)?
4. Suggested improvements?
```

---

## Resources

### Google Fonts Recommendations

**Sans-Serif (Modern UI)**
- Inter (excellent all-round)
- DM Sans (friendly)
- Outfit (geometric, modern)
- Plus Jakarta Sans (contemporary)
- Satoshi (distinctive)

**Sans-Serif (Classic)**
- Source Sans 3
- Open Sans
- Lato
- Roboto

**Serif (Elegant)**
- Source Serif 4
- Lora
- Playfair Display (display only)
- Fraunces (variable)

**Monospace**
- JetBrains Mono
- Fira Code
- IBM Plex Mono

### Tools
| Tool | URL | Use |
|------|-----|-----|
| Type Scale | type-scale.com | Calculate scales |
| Fontpair | fontpair.co | Pairing ideas |
| Google Fonts | fonts.google.com | Font library |
| Font Share | fontshare.com | Free quality fonts |
| Archetype | archetypeapp.com | Visual type design |

---

## Success Criteria

### Minimum Requirements
- [ ] 1-2 font families selected
- [ ] Complete type scale defined
- [ ] All heading styles specified
- [ ] Body text styles with good readability
- [ ] Minimum 16px for body text
- [ ] Line heights ensure readability

### Quality Indicators
- [ ] Clear visual hierarchy
- [ ] Consistent with brand personality
- [ ] Works across all breakpoints
- [ ] Passes accessibility (contrast, size)
- [ ] Performance considered (font loading)

---

## Related Skills

- **Previous**: `color_palettes.md` - Colors for text hierarchy
- **Next**: `layout_grids.md` - Grid to align typography
- **Related**: `spacing_rhythm.md` - Vertical rhythm with type
