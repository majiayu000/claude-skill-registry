---
name: apply-trustee
description: Apply 45Black Trustee Edition (v1.0) design system with 'The Clarity Standard' aesthetic
allowed-tools: Read, Write, Glob, Bash, Edit
context: fork
agent: general-purpose
model: claude-sonnet-4-20250514
---

# apply-trustee

Apply 45Black's Trustee Edition v1.0 "The Clarity Standard" design system.

**Designation:** External / User-Facing Framework

## Brand Reference

**IMPORTANT**: Always read the brand specification first:
```
~/.45black/brand/TRUSTEE.md
```

For framework comparison and selection guidance:
```
~/.45black/brand/README.md
```

This file contains the authoritative design tokens, colour values, and implementation guidance. Do NOT use hardcoded values from this skill - always reference the brand file.

**Note:** For internal/ops products, use the Saville Edition instead (`/apply-saville`).

## When To Use

- Building client-facing products
- Trustee dashboards
- Compliance tracking interfaces
- External reports
- Marketing materials
- User mentions: "apply trustee", "client design", "external design", "user-facing"

## Workflow

### 1. Read Brand Specification
```bash
cat ~/.45black/brand/TRUSTEE.md
```
Extract current version, colour palette, typography, and token values.

### 2. Detect Project Type
Identify framework (React/Next/Vite) and styling approach (Tailwind/CSS/etc).

### 3. Install Typography
Set up Inter font stack with appropriate fallbacks.

### 4. Generate Design Tokens
Create CSS custom properties or Tailwind config from brand spec values.

### 5. Apply Light Mode Default
Ensure light mode is the default, with optional dark mode support.

### 6. Create Base Components
Provide Trustee-styled components using tokens from brand spec.

### 7. Implement Status Colours
Apply compliance status colours (Compliant, In Progress, Overdue, etc.).

### 8. Verify WCAG Compliance
Check contrast ratios against brand spec requirements (AA minimum, AAA where practical).

### 9. Add Print Styles
Include print stylesheet for board meeting documents.

### 10. Document
Create DESIGN_SYSTEM.md referencing brand spec version.

## Key v1.0 Principles

- **Light-First** — Trustees work in offices, not terminals
- **Paper White** backgrounds, not warm carbon
- **Governance Blue** primary, not Saville Blue
- **Inter** typography, not IBM Plex Sans
- **Compliance Status Colours** — Clear visual hierarchy
- **Print-Ready** — Reports often printed for meetings
- **Touch Targets** — 44px minimum (trustees use iPads)

## Quality Gates

Before completion, verify:
- [ ] Brand spec file was read for current values
- [ ] Light mode is default
- [ ] Inter font loading correctly
- [ ] Status colours implemented
- [ ] WCAG AA contrast ratios pass (AAA for important content)
- [ ] Touch targets >= 44px
- [ ] Print stylesheet included
- [ ] Focus indicators visible

## Colour Quick Reference

| Purpose | Hex |
|---------|-----|
| Primary | `#1A4F7A` (Governance Blue) |
| Success | `#2E7D32` (Fiduciary Green) |
| Secondary | `#00695C` (Trustee Teal) |
| Warning | `#F57C00` (Advisory Amber) |
| Error | `#C62828` (Alert Red) |
| Text | `#212121` (Primary) |
| Background | `#FFFFFF` (Paper White) |

## Model Preference

**sonnet** — Design implementation is procedural, not reasoning-heavy

---
*References ~/.45black/brand/TRUSTEE.md for authoritative values*
