---
name: react-native-expo-mobile
description: |
  React Native and Expo best practices for Wythm mobile-app.

  **Use this skill when:**
  - Working with files in mobile-app/ directory
  - Implementing React Native components, animations, lists, or navigation
  - Using Reanimated, Gesture Handler, or Expo APIs
  - Optimizing performance (FlatList, ScrollView, animations)
  - Implementing state management with hooks or Zustand
  - Questions about React Native patterns or best practices

  **Contains 35+ rules** for preventing crashes, optimizing lists, GPU-accelerated animations, state architecture, and native UI patterns.

  NOT for web-only React code (use vercel-react-best-practices). NOT for design token naming (use design-tokens).
allowed-tools:
  - Read
  - Grep
---

# React Native + Expo Best Practices

React Native and Expo best practices for building performant mobile apps for Wythm.

## When to use this skill

- When developing React Native components in `mobile-app/` directory
- When optimizing list performance or animations
- When implementing state management with React hooks or Reanimated
- When working with native modules or Expo APIs
- When building mobile UI following platform best practices

## Related skills

- `/design-tokens` - for token naming and theming decisions
- `vercel-react-best-practices` - for web-only React/Next.js code

## Instructions

When this skill is invoked:

1. **Identify the relevant section(s)** from the reference table below
2. **Load only the needed section** from `AGENTS.md` using Grep to find the section header (e.g., `## 3. Animation`), then Read the relevant line range
3. **Apply rules by priority:**
   - **CRITICAL** (prevent crashes): Core Rendering
   - **HIGH** (major performance): List Performance, Animation, Scroll, Navigation
   - **MEDIUM** (moderate impact): State, UI, Design System, React Compiler
   - **LOW** (incremental): Monorepo, Dependencies, JavaScript, Fonts

### Example requests

- *"Optimize this FlatList"* -> Load section 2 (List Performance) from AGENTS.md
- *"Add a press animation to this button"* -> Load sections 3 (Animation) and 7 (State Architecture)
- *"Review this component for RN best practices"* -> Load section 1 (Core Rendering) first, then scan for relevant patterns

## Reference sections

| # | Section | Priority | When to load |
|---|---------|----------|--------------|
| 1 | Core Rendering | CRITICAL | Always scan for `&&` and string-outside-Text issues |
| 2 | List Performance | HIGH | FlatList, FlashList, LegendList, ScrollView+map |
| 3 | Animation | HIGH | Reanimated, CSS transitions, gestures, press states |
| 4 | Scroll Performance | HIGH | Scroll position tracking, scroll events |
| 5 | Navigation | HIGH | Stack, tabs, expo-router, headers |
| 6 | React State | MEDIUM | useState, derived state, stale closures |
| 7 | State Architecture | MEDIUM | Ground truth, shared values as state |
| 8 | React Compiler | MEDIUM | Destructuring, .get()/.set() for Reanimated |
| 9 | User Interface | MEDIUM | Images, menus, modals, styling, safe areas |
| 10 | Design System | MEDIUM | Compound components, component API design |
| 11 | Monorepo | LOW | Native deps in app dir, version alignment |
| 12 | Third-Party Deps | LOW | Import from design system folder |
| 13 | JavaScript | LOW | Intl formatter hoisting |
| 14 | Fonts | LOW | Native font loading at build time |

## Supporting files

- `rules/_sections.md` - Section definitions
- `rules/_template.md` - Template for new rules
