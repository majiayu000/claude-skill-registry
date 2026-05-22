---
name: layout-composition-critic
description: Critique UI layouts and provide specific, actionable fixes. Use when something feels off but you can't articulate why, before finalizing designs, or after adding new components. Outputs diagnosis of visual hierarchy, spacing, alignment, color balance issues with exact CSS/Tailwind fixes.
---

# Composition & Layout Critic (Layout-Kritiker)

Critique UI layouts and provide specific, actionable fixes.

## When to Use

- Something feels "off" but can't articulate why
- Before finalizing a design
- After adding new components
- Quick design review needed

## Process

### 1. Analyze Core Principles

#### Visual Hierarchy
- Is there a clear focal point?
- Can you identify primary, secondary, tertiary elements?
- Does the eye flow naturally?

#### Spacing & Rhythm
- Is whitespace consistent?
- Are related elements grouped?
- Is there breathing room?

#### Alignment
- Are elements on a grid?
- Do edges align vertically/horizontally?
- Are there orphaned elements?

#### Color Balance
- Is there a dominant color?
- Are accents used sparingly?
- Do colors compete for attention?

#### Contrast & Legibility
- Is text readable on backgrounds?
- Are interactive elements obvious?
- Is there enough visual contrast?

### 2. Diagnose Issues

| Symptom | Likely Cause |
|---------|--------------|
| "Too busy" | Too many focal points, not enough whitespace |
| "Boring" | No visual hierarchy, monotone colors |
| "Muddy" | Low contrast, competing colors |
| "Cluttered" | Insufficient spacing |
| "Unfinished" | Inconsistent spacing, misaligned elements |

### 3. Prescribe Specific Fixes

```
❌ Instead of: "Add more whitespace"
✅ Say: "Increase padding from 16px to 32px on the main card"

❌ Instead of: "Fix the colors"
✅ Say: "Desaturate the blue (#3498db → #5d7a8c) so it doesn't compete with the orange CTA"

❌ Instead of: "Improve hierarchy"
✅ Say: "Make the title 24px→32px, reduce subtitle opacity to 70%"
```

### 4. Provide Code

Show the actual CSS/Tailwind changes:

```css
/* Before */
.card { padding: 16px; }
.title { font-size: 18px; }

/* After */
.card { padding: 32px; }
.title { font-size: 24px; font-weight: 600; }
```

## Critique Template

```markdown
## Layout Critique: [Screen Name]

### What's Working
- [positive 1]
- [positive 2]

### Issues Found

**1. [Issue Name]**
- Problem: [specific description]
- Impact: [why it matters]
- Fix: [exact change]

### Priority Fixes
1. [Most impactful]
2. [Second priority]

### Code Changes
[Tailwind/CSS snippets]
```

## Red Flags Checklist

Immediate fixes if:
- [ ] Text on image with no overlay
- [ ] More than 3 competing colors at same saturation
- [ ] Elements touching edges with no padding
- [ ] Inconsistent border-radius
- [ ] Mixed spacing units (8px, 10px, 15px)
- [ ] No distinction between interactive and static elements
