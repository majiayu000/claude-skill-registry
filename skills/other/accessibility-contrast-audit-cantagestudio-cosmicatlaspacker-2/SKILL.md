---
name: accessibility-contrast-audit
description: "[Design System] Quantitative accessibility audit for UI - contrast ratios, font sizes, tap targets, heading hierarchy. Use when (1) checking WCAG color contrast compliance, (2) auditing text sizes for readability, (3) validating touch/click target sizes, (4) reviewing heading structure and landmarks, (5) user asks to 'check accessibility', 'audit contrast', 'WCAG compliance', or 'a11y check'."
---

# Accessibility & Contrast Audit

Quantitative accessibility checks for contrast, font size, hit areas, and semantic structure.

## Quick Start

```bash
python3 scripts/audit_accessibility.py --source src/ --tokens tokens.json
```

## WCAG Standards Reference

| Criterion | Level AA | Level AAA |
|-----------|----------|-----------|
| Normal text contrast | 4.5:1 | 7:1 |
| Large text contrast (18px+ or 14px bold) | 3:1 | 4.5:1 |
| UI components/graphics | 3:1 | 3:1 |
| Minimum touch target | 44×44px | 44×44px |
| Minimum font size (body) | 16px | 16px |

## Problem Types

| Type | Severity | Description |
|------|----------|-------------|
| `low-contrast` | error | Text/background contrast below WCAG threshold |
| `text-too-small` | warning | Font size below recommended minimum |
| `hit-area-too-small` | warning | Touch/click target below 44×44px |
| `heading-skip` | warning | Heading levels skipped (h1→h3) |
| `missing-alt` | error | Image missing alt text |