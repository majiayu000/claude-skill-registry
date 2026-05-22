---
name: frontend-design
description: "Front-end design patterns and best practices. UI/UX principles, layout, color, typography, and interaction. Trigger: When designing user interfaces, creating design systems, or improving usability."
skills:
  - conventions
  - a11y
  - humanizer
allowed-tools:
  - documentation-reader
  - web-search
---

# Frontend Design Skill

## Overview

This skill provides universal patterns for front-end design, UI/UX, and usability. It is technology-agnostic and focuses on principles, layout, accessibility, and user experience for any web or mobile interface.

## When to Use

- Designing or reviewing user interfaces (web/mobile)
- Creating or maintaining design systems and style guides
- Improving accessibility, usability, or visual consistency
- Planning responsive/adaptive layouts

## Critical Patterns

### Layout & Spacing

- Use a consistent spacing system (tokens, scale)
- Align elements to a grid or baseline
- Group related content visually

### Color & Contrast

- Ensure sufficient contrast for text and UI elements
- Use color intentionally for meaning, not decoration
- Provide alternatives for color-only cues

### Typography

- Limit font families and sizes for clarity
- Use hierarchy (headings, body, captions) for structure
- Ensure readable line length and spacing

### Accessibility

- Use semantic HTML or native components
- Provide ARIA labels and roles where needed
- Ensure keyboard and screen reader navigation

### Responsiveness

- Design for multiple breakpoints and device types
- Use fluid layouts and flexible images
- Test with real content and edge cases

## Decision Tree

- New component? → Follow design tokens and spacing system
- Accessibility needed? → Use semantic elements and ARIA
- Responsive? → Use media queries or adaptive layouts
- Visual bug? → Check contrast, spacing, and alignment

## Edge Cases

- Color contrast for vision impairments
- Touch target sizing for mobile
- Internationalization (RTL, long text)
- Overlapping or hidden content on small screens

## Practical Examples

### Before (inconsistent spacing)

> Elements are randomly spaced, making the UI look cluttered.

### After (consistent spacing)

> All elements use an 8px spacing scale, aligned to a grid, improving clarity and balance.

### Before (poor contrast)

> Light gray text on white background.

### After (accessible contrast)

> Text uses #222 on #fff, passing WCAG AA contrast.

## References

- Use with conventions, a11y, and technical-communication for best results.
