---
name: best-practices-react
description: |
  React, Next.js, React Native, and web design best practices from Vercel Engineering.
  Use when writing, reviewing, or refactoring React/Next.js/React Native components,
  optimizing performance, auditing UI accessibility, or designing component APIs.
  Triggers: "review react", "optimize component", "check accessibility", "react best practices",
  "component architecture", "react native performance".
triggers:
  - best practices react
  - react review
  - react component
  - next.js
  - react native
  - component architecture
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
  language: typescript

provides:
  - best-practices-react
composes:
  - task-monitor
---

# React Best Practices Collection

Enterprise-grade React/Next.js/React Native rules from Vercel Engineering. 100+ rules across 4 sub-skills with impact-prioritized categories.

## Sub-Skills

| Sub-Skill | Rules | Focus |
|-----------|-------|-------|
| `react-best-practices` | 40+ | React/Next.js performance optimization |
| `web-design-guidelines` | 100+ | Accessibility, forms, animation, dark mode, i18n |
| `react-native-skills` | 16 | Mobile performance, animations, platform APIs |
| `composition-patterns` | 8+ | Component architecture, prop design, compound components |

## When to Use

- **react-best-practices**: Writing React components, Next.js pages, data fetching, bundle optimization
- **web-design-guidelines**: UI review, accessibility audit, design compliance, UX check
- **react-native-skills**: React Native/Expo apps, mobile performance, native modules
- **composition-patterns**: Refactoring boolean prop proliferation, building component libraries

## Quick Reference

### Critical Impact
- Eliminate request waterfalls (parallel fetching, `Promise.all`)
- Bundle size (dynamic imports, tree shaking, barrel file avoidance)
- Accessibility (aria-labels, semantic HTML, keyboard navigation)
- FlashList over FlatList (React Native)

### High Impact
- Server-side rendering and streaming
- Focus states (`focus-visible` patterns)
- Layout (flex patterns, safe areas)
- Animation (Reanimated, `prefers-reduced-motion`)

### Medium Impact
- Re-render optimization (`useMemo`, `useCallback`, React Compiler)
- Forms (autocomplete, validation, error handling)
- Dark mode (`color-scheme`, `theme-color` meta)
- State management (Zustand patterns)

## File Structure

```
best-practices-react/
├── SKILL.md                          # This file
├── README.md                         # Detailed sub-skill descriptions
├── CLAUDE.md                         # Agent guidance (skill creation)
├── skills/
│   ├── react-best-practices/         # React/Next.js performance rules
│   │   ├── SKILL.md
│   │   └── rules/                    # Atomic rule files
│   ├── web-design-guidelines/        # UI/UX/a11y rules
│   │   ├── SKILL.md
│   │   └── rules/
│   ├── react-native-skills/          # React Native/Expo rules
│   │   ├── SKILL.md
│   │   └── rules/
│   ├── composition-patterns/         # Component architecture rules
│   │   ├── SKILL.md
│   │   └── rules/
│   └── claude.ai/
│       └── vercel-deploy-claimable/  # Vercel deployment skill
└── packages/
    └── react-best-practices-build/   # TypeScript build tooling
```
