---
name: ios-styleguide
description: Design and UI style guide for iOS apps. Premium consumer aesthetic, brand-forward native.
---

## Purpose

Enforce taste, restraint, and platform excellence. Complements security, NFR, and coding standards skills.

For brand identity (colors, fonts, design direction, anti-patterns), see `/shared-brand`.

**Platform addition:** brand-forward native — unmistakably crafted, never templated.

## Typography (iOS-specific)

- System font (San Francisco) preferred for body and controls
- Display typography may be brand-forward and expressive
- Must survive Dynamic Type increases without layout failure

## Liquid Glass (Apple's material system)

### Appropriate uses

- Navigation chrome (top bars, tab bars)
- Sheets, modals, transient overlays
- Elevated surfaces conveying depth
- Hero/focus containers reinforcing hierarchy

### Never use on

- Dense lists
- Primary reading surfaces
- Form fields and input-heavy views
- Backgrounds for long-form text

**Rule:** Liquid Glass must convey hierarchy or focus, not decoration. If the purpose isn't clear, don't use it.

## iOS-specific anti-patterns

- Default SwiftUI previews shipped unchanged
- Boilerplate list-card patterns across screens
- iPhone layouts scaled up for iPad
- Decorative transitions or over-animated navigation
- Translucency that reduces legibility

## Device support (mandatory)

- iPhone and iPad
- Adaptive layouts using size classes
- Support split view and multitasking
- Design for portrait and landscape

If a screen looks identical on iPhone and iPad, it likely underuses the platform.

## Reference

For Swift tokens, adaptive layout patterns, and Liquid Glass examples, see `reference/ios-styleguide-reference.md`
