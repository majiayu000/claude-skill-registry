---
name: m3-expressive-typography-enhancer
description: Elevate typography with variable fonts, extreme weight contrasts (100 vs 900), and emotional tone guidance. Validates against generic fonts (Inter, Roboto) and enforces M3 expressive principles with high-contrast pairings.
---

# M3 Expressive Typography Enhancer

## Purpose

Elevate typography beyond basic token replacement with variable fonts, extreme weight contrasts, and emotional tone mapping. Transforms boring typography (Inter 400 vs 500) into expressive, memorable typography (100 vs 900) that conveys personality and meaning.

## When to Use

Use this skill when you need to:

- **Choose expressive fonts** that avoid generic defaults (Inter, Roboto, Arial)
- **Implement variable fonts** with fluid weight transitions
- **Create extreme contrasts** (9x weight difference, not 1.25x)
- **Map typography to emotion** (playful, confident, elegant, technical)
- **Validate font choices** against M3 Expressive principles
- **Establish font pairings** (display + monospace, serif + geometric)
- **Upgrade existing typography** from timid to dramatic

**Trigger scenarios:**

- "This typography feels generic and boring"
- "How do I make typography more expressive?"
- "What font conveys confidence and professionalism?"
- "Replace Inter with something distinctive"

## Overview

This skill enhances M3 typography with M3 Expressive principles:

1. **Variable Font Integration** - Font-variation-settings for fluid weight/width transitions
2. **Extreme Weight Contrasts** - 100 vs 900 (not 400 vs 600), 3x+ size jumps
3. **Emotional Tone Mapping** - Typography that conveys personality
4. **Anti-Slop Validation** - Reject generic fonts (Inter, Roboto, Arial)
5. **Expressive Font Pairing** - High-contrast combinations

## M3 Expressive Typography Principles

### 1. Variable Fonts (Fluid Typography)

**Recommended Variable Fonts:**

- **Plus Jakarta Sans** (200-800) - Modern, professional
- **Poppins** (100-900) - Elegant, versatile
- **Montserrat** (100-900) - Bold, geometric
- **Sora** (100-800) - Tech-forward, unique

**Example:**

```css
.expressive-heading {
  font-family: "Plus Jakarta Sans Variable", sans-serif;
  font-variation-settings: "wght" 800;
  transition: font-variation-settings 300ms var(--sys-motion-easing-expressive);
}

.expressive-heading:hover {
  font-variation-settings: "wght" 900;
}
```

### 2. Extreme Weight Contrasts

**Anti-Pattern (Boring):**

```tsx
// ❌ Timid contrast - 1.25x ratio
<h1 style={{ fontWeight: 400 }}>Heading</h1>
<p style={{ fontWeight: 500 }}>Body</p>
```

**M3 Expressive (Dramatic):**

```tsx
// ✅ Extreme contrast - 9x ratio
<h1 style={{
  fontWeight: 100,
  fontSize: 'var(--sys-type-display-large-size)',
  letterSpacing: '-0.02em'
}}>Heading</h1>
<p style={{
  fontWeight: 900,
  fontSize: 'var(--sys-type-body-small-size)'
}}>Subtext</p>
```

### 3. Emotional Tone Mapping

**Playful & Energetic** → Montserrat 900 + Nunito 400
**Confident & Professional** → Plus Jakarta Sans 800 + Inter 400
**Elegant & Premium** → Poppins 300 + Open Sans 400
**Tech-Forward** → Sora 700 + Inter 400

### 4. Anti-Slop Validation

**FORBIDDEN FONTS:**

- ❌ Inter (alone), Roboto, Open Sans, Arial, Helvetica, System fonts

**Alternatives:**

- Inter → Plus Jakarta Sans Variable
- Roboto → Poppins
- Arial → Montserrat

### 5. Expressive Font Pairing

**Display + Monospace:** Plus Jakarta Sans + JetBrains Mono
**Serif + Geometric:** Playfair Display + Poppins
**Variable Across Weights:** Montserrat 900 + Montserrat 300

## Usage

```bash
m3-expressive-typography-enhancer \
  --file frontend/src/components/ui/Card/Card.tsx \
  --tone "confident-professional" \
  --validate-anti-slop
```

## Validation Checklist

- [ ] No forbidden fonts used alone
- [ ] Weight contrast ratio ≥ 3x
- [ ] Size contrast ratio ≥ 3x
- [ ] Variable fonts enabled
- [ ] Emotional tone matches context
- [ ] High-contrast font pairing
- [ ] Letter spacing applied correctly

## Troubleshooting

### Variable Fonts Not Loading

**Solution:**

```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@200..800&display=swap" rel="stylesheet" />
```

### Weight Contrast Too Extreme

**Solution:**
Start with 300 vs 700, gradually increase to 100 vs 900

### Font Pairing Incoherent

**Solution:**
Use same family at different weights or ensure emotional tone consistency

## Related Skills

- [m3-anti-slop-validator](../m3-anti-slop-validator/SKILL.md) - Validate typography against slop patterns

---

**Version:** 2.0.0 (Optimized)
**Status:** Production Ready
