---
name: apply-saville
description: Apply 45Black Saville Edition (v5.0) design system with 'The Clarity Standard' aesthetic
allowed-tools: Read, Write, Glob, Bash, Edit
context: fork
agent: general-purpose
model: claude-sonnet-4-20250514
---

# apply-saville

Apply 45Black's Saville Edition v5.0 "The Clarity Standard" unified design system.

## Brand Reference

**IMPORTANT**: Always read the brand specification first:
```
~/.45black/brand/SAVILLE-v5.md
```

For framework comparison and selection guidance:
```
~/.45black/brand/README.md
```

This file contains the authoritative design tokens, colour values, and implementation guidance. Do NOT use hardcoded values from this skill - always reference the brand file.

## Variant Selection

v5.0 introduces **two variants**:

| Variant | Codename | Use For | Key Differences |
|---------|----------|---------|-----------------|
| **Core** | "The Matte Machine" | Internal tools, CLI, Archon | Matte ON, weight 300 |
| **Clarity** | "The Legal Workhorse" | External products, Apex, 8hr daily use | Matte OFF, weight 500 |

**Selection Rule:** If users spend 8+ hours daily in the interface, use **Clarity**.

For client-facing/external products, consider Trustee Edition instead (`/apply-trustee`).

## When To Use

- Starting new 45Black project
- Rebranding existing project
- User mentions: "apply saville", "45black brand", "design system"

## Workflow

### 1. Read Brand Specification
```bash
cat ~/.45black/brand/SAVILLE-v5.md
```
Extract current version, colour palette, typography, and token values.

### 2. Select Variant
Ask user or determine based on product type:
- **Internal tool?** → Core variant
- **External/client-facing?** → Clarity variant
- **Data-dense dashboard?** → Clarity variant (no matte)
- **Marketing/brand site?** → Core variant (with matte)

### 3. Detect Project Type
Identify framework (React/Next/Vite) and styling approach (Tailwind/CSS/etc).

### 4. Install Typography
Set up IBM Plex Sans and Mono fonts (+ Merriweather for document reading panes).

### 5. Generate Design Tokens
Create CSS custom properties or Tailwind config from brand spec values.

Include mode-specific tokens:
- Home Strip (dark mode)
- Away Strip (light mode)
- High Contrast mode

### 6. Apply Code Bar
Implement 6px code bar with correct colour order:
Green → Teal → Blue → Purple → Coral → Orange

### 7. Configure Matte Texture
- **Core variant:** Enable matte texture (15% dark, 8% light)
- **Clarity variant:** Disable matte texture

### 8. Set Typography Weights
- **Core variant:** Hero text weight 300
- **Clarity variant:** Hero text weight 500

### 9. Create Base Components
Provide Saville-styled components using tokens from brand spec.

### 10. Verify WCAG Compliance
Check contrast ratios against brand spec requirements:
- Primary text: 4.5:1 minimum
- Orange (#F57C00): 19pt+ only
- Touch targets: 44px minimum

### 11. Document
Create DESIGN_SYSTEM.md referencing brand spec version and variant used.

## Key v5.0 Changes from v4.4

| Element | v4.4 | v5.0 |
|---------|------|------|
| Variants | Single | Core + Clarity |
| Hero weight (Clarity) | 300 | **500** |
| Code bar height | 4px | **6px** |
| Light blue | Mixed | **#1565C0** unified |
| Matte texture | Always | **Optional** |

## Quality Gates

Before completion, verify:

### Universal
- [ ] Brand spec file was read (`~/.45black/brand/SAVILLE-v5.md`)
- [ ] Variant selected (Core or Clarity)
- [ ] Warm carbon backgrounds (not #0F0F0F)
- [ ] Code bar height is 6px
- [ ] IBM Plex fonts load correctly
- [ ] WCAG AA contrast ratios pass
- [ ] Orange only used at 19pt+
- [ ] Focus indicators visible (2px ring)
- [ ] Border radius ≤ 12px
- [ ] Animation duration ≤ 300ms

### Core Variant
- [ ] Matte texture enabled at correct opacity
- [ ] Hero typography weight 300

### Clarity Variant
- [ ] Matte texture disabled
- [ ] Hero typography weight 500
- [ ] Touch targets 44px minimum

## Model Preference

**sonnet** - Design implementation is procedural, not reasoning-heavy

---
*References ~/.45black/brand/SAVILLE-v5.md for authoritative values*
*v5.0 "The Clarity Standard" - Unified Design System*
