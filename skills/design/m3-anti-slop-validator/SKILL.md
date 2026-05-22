---
name: m3-anti-slop-validator
description: Detect and prevent generic AI aesthetics (purple gradients, flat layouts, predictable patterns) in M3 components. Validates typography, colors, and layout against expressive design standards with 0-100 quality scoring.
---

# M3 Anti-Slop Validator

## Purpose

Enforce M3 Expressive aesthetic standards by detecting and preventing generic "AI slop" patterns: purple gradients, flat layouts, timid contrasts, and cookie-cutter designs. Provides automated validation with aesthetic quality scoring (0-100) and actionable remediation steps.

## When to Use

Use this skill when you need to:

- **Validate component aesthetics** against M3 Expressive standards before deployment
- **Detect generic AI patterns** (Inter fonts, purple gradients, flat backgrounds)
- **Score design quality** with objective 0-100 aesthetic rating
- **Generate remediation reports** with specific improvement recommendations
- **Prevent design system drift** by catching slop before it ships
- **Enforce expressive standards** in CI/CD pipelines
- **Audit existing components** for M3 compliance

**Trigger scenarios:**

- "Is this component too generic?"
- "Validate this design against M3 Expressive standards"
- "Why does this feel like AI-generated slop?"
- "Score this component's aesthetic quality"

## Overview

This skill enforces M3 Expressive aesthetic standards by:

1. **Detecting Generic Fonts** - Flag Inter, Roboto, Arial, system fonts (unless paired with distinctive display fonts)
2. **Identifying Clichéd Colors** - Detect purple gradients on white, timid palettes, boring color schemes
3. **Spotting Flat Layouts** - Find solid backgrounds, lack of depth, no layering
4. **Flagging Predictable Patterns** - Generic component arrangements, cookie-cutter designs
5. **Scoring Aesthetic Quality** - Overall creativity and distinctiveness rating (0-100)

## Core Validation Categories

### 1. Generic Fonts (Critical)

**Forbidden Fonts (Without Distinctive Pairing):**

- ❌ Inter, Roboto, Open Sans, Arial, Helvetica, Lato
- ❌ System fonts (-apple-system, BlinkMacSystemFont, etc.)

**Detection:**
Scans code for forbidden font families. If found alone (without distinctive display font), flags as critical violation.

**Pass:** Plus Jakarta Sans, Poppins, Montserrat, Sora, Crimson Pro
**Fail:** Inter alone, Roboto alone, system fonts

### 2. Clichéd Colors (Critical)

**Forbidden Color Patterns:**

- ❌ Purple gradient on white (#7C4DFF → #9C27B0 on #FFFFFF)
- ❌ Generic Material Blue (#2196F3, #1976D2)
- ❌ Timid palettes (all colors < 20% saturation)
- ❌ Evenly distributed colors (no dominant color)

**Pass:** Vibrant, personalized palettes (teal/coral, magenta/cyan)
**Fail:** Purple gradients, desaturated colors, no dominant color

### 3. Flat Layouts (Warning)

**Forbidden Layout Patterns:**

- ❌ Solid backgrounds (no gradients, no patterns)
- ❌ No elevation (all elements at same z-level)
- ❌ Uniform spacing (all gaps identical, no rhythm)

**Pass:** Layered gradients, elevation tokens, varied spacing
**Fail:** Flat solids, no depth effects, mechanical spacing

### 4. Predictable Patterns (Warning)

**Forbidden Design Patterns:**

- ❌ Monotone font pairing (Roboto display + Roboto body)
- ❌ Timid weight contrasts (400 vs 500, ratio < 1.5x)
- ❌ Timid size contrasts (24px vs 16px, ratio < 2x)
- ❌ No hover states (static components)

**Pass:** High-contrast pairings, extreme weights (100 vs 900), spring-physics hover
**Fail:** Same font family, timid contrasts, no interactions

## Aesthetic Quality Score (0-100)

**Scoring Algorithm:**

- **Typography (25 points)**: Font distinctiveness, weight contrast, size contrast
- **Color (25 points)**: Palette vibrancy, saturation, dominance
- **Layout (25 points)**: Depth effects, elevation, spacing rhythm
- **Interaction (25 points)**: Hover states, animations, spring physics

**Grade Scale:**

- **A (90-100)**: Exceptional - Strong M3 Expressive principles
- **B (80-89)**: Good - Minor improvements possible
- **C (70-79)**: Acceptable - Needs improvement
- **D (60-69)**: Below standards - Review violations
- **F (<60)**: Critical - Complete redesign recommended

## Validation Report Format

```json
{
  "aestheticQuality": {
    "total": 72,
    "breakdown": {
      "typography": 18,
      "color": 20,
      "layout": 15,
      "interaction": 19
    },
    "grade": "C",
    "recommendation": "Acceptable design. Focus on improving typography and color for more impact."
  },
  "violations": [
    {
      "category": "typography",
      "pattern": "Generic font detected",
      "severity": "critical",
      "details": {
        "fontFamily": "Inter, sans-serif",
        "location": "Line 42",
        "suggestion": "Replace 'Inter' with 'Plus Jakarta Sans Variable'."
      }
    }
  ],
  "remediationSteps": ["1. Replace Inter with Plus Jakarta Sans Variable", "2. Use vibrant color palette: teal + coral + purple", "3. Add layered background gradients", "4. Apply elevation tokens for depth", "5. Add spring-physics hover effects"]
}
```

## Usage

### Basic Validation

```bash
# Validate aesthetic quality and detect AI slop
m3-anti-slop-validator \
  --file frontend/src/components/ui/Card/Card.tsx \
  --tokens design-system/tokens-expressive.json \
  --report validation-report.json
```

### Within Design Systems

```javascript
// Run after M3 migrations to validate final output
const validation = await runSkill("m3-anti-slop-validator", {
  code: finalCode,
  tokens: tokensExpressive,
});

if (validation.aestheticQuality.total < 80) {
  console.warn("⚠️ Low aesthetic quality score. Review violations.");
}
```

## Validation Checklist

- [ ] No forbidden fonts (Inter, Roboto, Arial) without distinctive pairing
- [ ] No purple gradients on white backgrounds
- [ ] Color saturation ≥ 30% (vibrant, not timid)
- [ ] Dominant color palette (not evenly distributed)
- [ ] Layered backgrounds (gradients, patterns, not flat solids)
- [ ] Elevation tokens used for depth
- [ ] Varied spacing rhythm (not uniform)
- [ ] Weight contrast ≥ 3x (100 vs 900, not 400 vs 500)
- [ ] Size contrast ≥ 3x (57px vs 12px, not 24px vs 16px)
- [ ] Hover states with spring physics
- [ ] Aesthetic quality score ≥ 80

## Troubleshooting

### Issue: False Positive on Inter Font

**Solution:**

- Ensure distinctive display font is clearly defined in code
- Pair with Playfair Display, Crimson Pro, or similar high-contrast font

### Issue: Low Color Score Despite Vibrant Palette

**Solution:**

- Check for dominant color (avoid evenly distributed colors)
- Ensure 40-80% saturation range
- Avoid generic Material Blue (#2196F3)

### Issue: Layout Score Low Despite Using Elevation

**Solution:**

- Add layered backgrounds (gradients, patterns)
- Vary spacing scales (8px, 16px, 24px, 40px)
- Ensure visual hierarchy is clear

## Related Skills

- [m3-expressive-typography-enhancer](../m3-expressive-typography-enhancer/SKILL.md) - Enhance typography with variable fonts
- [m3-atmospheric-backgrounds](../m3-atmospheric-backgrounds/SKILL.md) - Create layered atmospheric effects
- [m3-spring-motion-choreography](../m3-spring-motion-choreography/SKILL.md) - Add spring-physics interactions

---

**Version:** 2.0.0 (Optimized)
**Status:** Production Ready
