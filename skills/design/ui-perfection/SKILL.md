---
name: ui_perfection
description: Enforce the "Premium" aesthetic and accessibility standards.
allowed-tools: Read, Edit, Write
---

# UI Perfection Protocol

## 1. "Premium" Aesthetic Rules

- **Typography**: Use defined font stacks (Inter/Roboto). No default Times New Roman.
- **Spacing**: Use standard Tailwind spacing (e.g. `p-4`, `m-6`). Avoid magic numbers.
- **Colors**: Use the project's color palette (e.g. `bg-primary-500`). Avoid raw hex codes unless absolutely necessary for specific branding.
- **Interaction**:
  - All interactive elements must have `:hover` and `:active` states.
  - Transitions should be smooth (`transition-all duration-200`).

## 2. Mobile Responsiveness

- **Mobile-First**: Design for mobile `base` styles first, then add `md:`, `lg:` modifiers.
- **Touch Targets**: Buttons must be at least 44x44px usable area.
- **No Overflow**: Check for horizontal scrollbars on mobile.

## 3. Accessibility (A11y)

- **Alt Text**: Images must have `alt` attributes.
- **Contrast**: Text color must pass WCAG AA contrast ratio against background.
- **Forms**: Inputs must have associated labels (visible or `aria-label`).
- **Keyboard**: All interactive elements must be reachable via Tab.

## 4. Perfection Checklist

- [ ] Is it responsive on mobile (320px+)?
- [ ] Are hover states present?
- [ ] Are transitions smooth?
- [ ] Do images have alt text?
- [ ] Does it look "Premium"? (Subjective check - ask yourself: "Would Apple/Linear ship this?")
