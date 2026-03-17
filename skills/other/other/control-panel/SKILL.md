---
name: control-panel-ui-ux
description: "Minimal UI/UX rules for BuckyOS control_panel: pick a style, build a design system, and keep RPC-aligned."
---

# Control Panel UI/UX Skill

Use this when designing or implementing control_panel UI.

## When to Apply

- New UI page or component
- Visual refresh or UX fix
- Aligning UI with RPC data

## Rule Priorities

1. Accessibility: contrast, focus, keyboard nav
2. Interaction: touch targets >= 44x44px, no layout shift on hover
3. Layout: responsive, no horizontal scroll
4. Typography & color: consistent scale and palette
5. Motion: respect prefers-reduced-motion

## Design System (current)

- Primary color: #0f766e
- Accent color: #f59e0b
- Fonts: Space Grotesk (headings), Work Sans (body)

## Design Tokens (add/update)

- Neutrals: #0f172a (ink), #52606d (muted), #d7e1df (border), #f4f8f7 (surface muted), #ffffff (surface)
- Radius scale: 8 / 12 / 18 / 24
- Shadow scale: soft / strong (avoid heavy blur)
- Spacing scale: 4 / 8 / 12 / 16 / 24 / 32

## Typography Scale

- Sizes: 12 / 14 / 16 / 20 / 24 / 32
- Line-height: body 1.5, headings 1.2

## Icon System

- Use one SVG icon set only
- Sizes: 16 / 20 / 24
- No emoji icons

## Layout Rules

- Max content width: 1280
- Sidebar width: 260
- Card gap: 16-24
- Page padding: 24 (desktop), 16 (mobile)

## Component Rules

- Buttons: >= 44px touch target, clear hover/active/disabled
- Tables: header sticky when overflow, row height >= 44px
- Forms: label + helper text, error in place

## Data Density

- Default density: medium
- Keep line length <= 75 chars

## States

- Loading: skeleton or subtle shimmer
- Empty: explain why + next action
- Error: clear message + retry

## Charts

- Series colors: primary then accent, avoid low-contrast pairs
- Gridlines light, labels muted

## Motion

- 150-300ms transitions
- Respect prefers-reduced-motion

## Workflow

1. Define a design system (style, palette, typography, spacing).
2. Apply UX rules above while building components.
3. Match UI data fields to backend contracts (see `doc/dashboard/control_panel.md`).

## Quick Checks

- No emoji icons; use one SVG icon set.
- 375/768/1024/1440 widths verified.
- Focus states visible.

## References

- `doc/dashboard/control_panel.md`
