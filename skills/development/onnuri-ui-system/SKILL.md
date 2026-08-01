---
name: onnuri-ui-system
description: This skill enforces a consistent, mobile-first UI.
---

# Skill: onnuri-ui-system

This skill enforces a consistent, mobile-first UI.

## Global styling
- Background color must be `#F9F8F6` across all pages.
- Prefer simple cards, clear spacing, and readable typography.
- Touch targets must be >= 44px height.

## Component rules
- Keep UI minimal and consistent.
- Avoid heavy animations and complex interactions.
- Use a small number of reusable visual patterns:
  - header area
  - search input
  - chip row
  - list cards
  - empty/error states

## State UI
- Loading: skeleton placeholders.
- Empty: short, clear message.
- Error: short message + keep details in `console.error`.

## Navigation UX
- Preserve list context via URL query params.
- Avoid navigation churn that breaks IME or causes excessive rerenders.
- Do not implement scroll restoration.

## Accessibility basics
- Buttons should have clear labels.
- Inputs should have placeholders and/or labels.
- Keep contrast readable against `#F9F8F6`.
