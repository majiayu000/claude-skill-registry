---
name: design-patterns
description: Reference library of proven UI design patterns, component templates, and sector-specific conventions for high-quality design generation.
---

# Design Patterns Reference

This skill provides a curated library of proven design patterns that generate high-quality, non-vibe-coded UI.

## Layout Patterns

### Hero Sections

**Pattern 1: Split Hero**
Best for: SaaS, product landing pages
```
┌─────────────────────────────────────────────┐
│  [Content]              [Media]             │
│  Headline               Image/Video/        │
│  Subhead                Illustration        │
│  CTA Buttons                                │
└─────────────────────────────────────────────┘
```

**Pattern 2: Centered Hero**
Best for: Announcements, events, minimal designs
```
┌─────────────────────────────────────────────┐
│              [Eyebrow Badge]                │
│                 Headline                    │
│                 Subhead                     │
│           [CTA]    [Secondary]              │
│              [Social Proof]                 │
└─────────────────────────────────────────────┘
```

**Pattern 3: Product Showcase**
Best for: E-commerce, physical products
```
┌─────────────────────────────────────────────┐
│  [Product Image - Large, High Quality]      │
│  ─────────────────────────────────────────  │
│  Product Name          Price                │
│  Brief Description     [Add to Cart]        │
│  [Feature Icons]                            │
└─────────────────────────────────────────────┘
```

### Navigation Patterns

**Top Navigation (Desktop)**
```
┌─────────────────────────────────────────────┐
│ [Logo]  Nav Items...        [CTA] [Account] │
└─────────────────────────────────────────────┘
```

**Sidebar Navigation (Dashboard)**
```
┌─────────────────────────────────────────────┐
│ [Logo]           │  Page Content            │
│ ───────────────  │                          │
│ Nav Item 1       │                          │
│ Nav Item 2       │                          │
│ Nav Item 3       │                          │
│                  │                          │
│ [Collapsed User] │                          │
└─────────────────────────────────────────────┘
```

### Card Patterns

**Content Card**
```
┌─────────────────┐
│ [Image]         │
│ Category        │
│ Title           │
│ Description...  │
│ [Meta] [Action] │
└─────────────────┘
```

**Feature Card**
```
┌─────────────────┐
│ [Icon]          │
│ Feature Name    │
│ Description     │
│ that explains   │
│ the benefit.    │
└─────────────────┘
```

**Pricing Card**
```
┌─────────────────┐
│ Plan Name       │
│ $XX/mo          │
│ Description     │
│ ─────────────── │
│ ✓ Feature 1     │
│ ✓ Feature 2     │
│ ✓ Feature 3     │
│ [CTA Button]    │
└─────────────────┘
```

## Component Patterns

### Buttons

**Primary Button**
- Background: Primary color
- Text: White/contrast color
- Padding: 12px 24px (or 16px 32px for large)
- Border-radius: 6px (or 8px)
- Font-weight: 500 or 600
- Hover: Darken 10%

**Secondary Button**
- Background: Transparent
- Border: 1px solid primary or gray
- Text: Primary color or gray-700
- Same padding and radius as primary

**Ghost Button**
- Background: Transparent
- No border
- Text: Primary color
- Underline or subtle hover effect

### Forms

**Input Field**
```html
<div class="form-group">
  <label for="input">Label</label>
  <input type="text" id="input" placeholder="Placeholder">
  <span class="hint">Helper text</span>
</div>
```

**Styling:**
- Border: 1px solid gray-300
- Border-radius: 6px
- Padding: 10px 14px
- Focus: Border primary color + ring
- Error: Border red + red text

### Feedback

**Toast Notification**
```
┌────────────────────────────┐
│ [Icon] Message text   [X]  │
└────────────────────────────┘
```
Position: Top-right or bottom-center
Duration: 3-5 seconds

**Alert Banner**
```
┌──────────────────────────────────────────┐
│ [Icon] Alert message with more details.  │
│        [Action Link]                 [X] │
└──────────────────────────────────────────┘
```

## Sector-Specific Patterns

### Fintech

**Trust Indicators:**
- Security badges (SOC2, bank-level encryption)
- Regulatory compliance logos
- Trust pilot/review scores
- "Protected by..." messaging

**Data Display:**
- Clean data tables with sorting
- Clear number formatting (currency, percentages)
- Status indicators (green/yellow/red)
- Trend indicators (arrows, sparklines)

**Color Guidance:**
- Primary: Blues, teals
- Success: Greens (money positive)
- Warning: Amber (caution)
- Avoid: Aggressive reds except for losses

### Healthcare

**Accessibility Priority:**
- WCAG AAA contrast where possible
- Large touch targets (48px minimum)
- Clear, readable fonts (18px+ body)
- High-contrast mode option

**Information Hierarchy:**
- Critical info: Prominent placement
- Warnings: Clear visual distinction
- Patient data: Clear labeling
- Actions: Confirmation for destructive

**Color Guidance:**
- Calming: Soft blues, greens
- Clinical: Clean whites
- Avoid: Harsh, aggressive colors

### E-commerce

**Product Display:**
- High-quality images (multiple angles)
- Clear pricing (original + sale)
- Stock status
- Quick add to cart

**Trust & Conversion:**
- Reviews and ratings
- Free shipping threshold
- Return policy highlight
- Secure checkout badges

**Urgency (use sparingly):**
- Low stock indicators
- Sale countdown
- Limited time offers

### SaaS

**Onboarding:**
- Progressive disclosure
- Progress indicators
- Skip options
- Contextual help

**Dashboard:**
- Key metrics prominent
- Clear navigation
- Quick actions
- Recent activity

**Pricing Page:**
- Clear comparison
- Recommended plan highlight
- Feature differentiation
- FAQ section

## Anti-Patterns (Avoid These)

### Layout Anti-Patterns
- ❌ Walls of text without visual breaks
- ❌ Too many competing focal points
- ❌ Inconsistent alignment
- ❌ Cramped spacing

### Component Anti-Patterns
- ❌ Mystery meat navigation (icons without labels)
- ❌ Infinite scroll without way back
- ❌ Carousel as primary content
- ❌ Pop-ups on page load

### Visual Anti-Patterns
- ❌ Generic purple-blue gradients
- ❌ Floating decorative blobs
- ❌ Stock photos of business handshakes
- ❌ Default framework colors unchanged
