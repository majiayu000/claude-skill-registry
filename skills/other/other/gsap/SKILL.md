---
name: gsap
description: >-
  Comprehensive GSAP v3 best-practices skill covering fundamentals, plugins, and
  useful features/tools. Use when the user mentions GSAP, GreenSock, gsap.to,
  gsap.timeline, ScrollTrigger, ScrollSmoother, Flip, SplitText, MorphSVG,
  DrawSVG, Draggable, useGSAP, or asks to build, review, or optimize
  animations, motion, or scroll-driven interactions.
---

# GSAP Best Practices

Comprehensive best-practices guide for GSAP v3, organized as modular rules for agents. The structure mirrors the docs taxonomy (fundamentals, plugins, useful features/tools) while prioritizing implementation decisions and code quality.

## Rule categories by priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Fundamentals | CRITICAL | `core-` |
| 2 | Plugin architecture | HIGH | `plugin-` |
| 3 | Useful features & tools | HIGH | `tools-` |
| 4 | Performance | HIGH | `perf-` |
| 5 | Accessibility | MEDIUM-HIGH | `a11y-` |
| 6 | Debug workflow | MEDIUM | `debug-` |

## How to use this skill

Read these files first:

```text
rules/_sections.md
rules/core-animation-model.md
rules/plugin-registration-and-loading.md
rules/tools-utils-function-pipelines.md
```

Then load only category-specific rules relevant to the current task.

## Rule index

| Topic | Description | Reference |
|------|-------------|-----------|
| Sections overview | Categories and recommended reading order | [rules/_sections.md](rules/_sections.md) |
| Fundamentals | Core GSAP/Tween/Timeline/Easing rules | [rules/core-animation-model.md](rules/core-animation-model.md) |
| Plugins | Registration + plugin family rules | [rules/plugin-registration-and-loading.md](rules/plugin-registration-and-loading.md) |
| Useful tools | Utility methods, helper functions, React/stagger patterns | [rules/tools-utils-function-pipelines.md](rules/tools-utils-function-pipelines.md) |
| Perf/a11y/debug | Cross-cutting quality rules | [rules/perf-rendering-and-lifecycle.md](rules/perf-rendering-and-lifecycle.md) |

## Coverage and maintenance

- Coverage map: `rules/_coverage-map.md`
- Source index: https://gsap.com/llms.txt
- Update this skill when GSAP docs version changes or when plugin APIs evolve.

## Framework note

For SSR/component frameworks (Nuxt, React, Vue, etc.), apply client-only lifecycle guards and strict teardown (`context/revert`) to prevent leaks and duplicate animations.
