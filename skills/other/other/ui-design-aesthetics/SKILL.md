---
name: ui-design-aesthetics
description: Generates high-quality, non-generic UI designs with a focus on performance, progressive disclosure, and distinctive aesthetics.
---

# UI Design & Aesthetics

Expert guidance for designing and implementing beautiful, high-performance user interfaces. This skill enforces distinctive aesthetics while ensuring technical excellence through progressive disclosure and dynamic loading.

## Core Capabilities

- **Aesthetic Direction**: avoiding "AI slop" by enforcing distinctive typography, color, and depth.
- **Performance Architecture**: ensuring UI components load dynamically to minimize initial payload.
- **Progressive Disclosure**: designing interfaces that reveal complexity only when needed.
- **API Contract Validation**: ensuring frontend components align with backend data structures.

## Usage

Use this skill when:
- Designing a new feature or application from scratch.
- Refactoring an existing UI to be more modern and performant.
- Implementing complex dashboards or data-heavy interfaces.

## Quick Reference

| Topic | Reference |
| --- | --- |
| Aesthetic Rules (Typography, Color, Motion) | `skills/ui-design-aesthetics/references/aesthetics.md` |
| Progressive Disclosure & Dynamic Loading | `skills/ui-design-aesthetics/references/progressive-disclosure.md` |
| API Contract Validation | `skills/ui-design-aesthetics/references/api-contracts.md` |

## Design Workflow

1.  **Analyze & Select Aesthetic**: Choose a cohesive theme (Swiss, Neo-Brutalism, etc.) and reject generic defaults.
2.  **Architect for Performance**: Identify heavy components for lazy loading (`React.lazy`, dynamic imports).
3.  **Design Interaction**: Plan staggered reveals and interaction-based loading.
4.  **Validate Data**: Define TypeScript interfaces or Zod schemas for API responses.
5.  **Implement**: Write the code using utility classes (Tailwind) and enforcing the design system.

## Performance Requirements

- **Initial Payload**: Critical path CSS/JS only.
- **Dynamic Loading**: Secondary components MUST load on interaction or visibility (IntersectionObserver).
- **Latency**: Design optimistic UI states for interactions > 100ms.
