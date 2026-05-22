---
name: developing-ui
description: Strict guidelines for building UI components, pages, and layouts. Ensures adherence to brand-identity tokens, technical constraints, and performance standards.
---

# UI Development & Front-end Engineering

This skill defines the standard operating procedure for front-end development. It ensures all UI code is consistent, performant, accessible, and robust, while strictly adhering to the `brand-identity` skill.

## When to use this skill
- Creating new UI components (Framework agnostic: React, Vue, Svelte, etc.)
- Styling new or existing pages
- Debugging layout, visual, or performance issues
- Refactoring CSS or component logic

## Workflow
When building a new UI element, follow this process:

1.  **Analyze & Plan**
    - Check `brand-identity/resources/design-tokens.json` for available tokens.
    - Define all component states: **Idle, Loading, Error, Empty, Success**.

2.  **Scaffold**
    - Create the file structure.
    - Define the component interface (Props) with strict typing.

3.  **Style**
    - Apply layout (Flex/Grid) first.
    - Apply spacing/sizing using design tokens.
    - **Optimization:** Use CSS variables for theming and avoid heavy animations on non-composite properties (stick to transform/opacity).

4.  **Interact & Logic**
    - Add state and event handlers.
    - Implement accessible focus management.
    - Ensure error handling is graceful (e.g., Error Boundaries or fallback UI).

5.  **Verify & Test**
    - Check responsiveness (Mobile -> Desktop).
    - Check accessibility (ARIA, keyboard navigation, screen reader).
    - **Performance:** Check for unnecessary re-renders or layout shifts (CLS).
    - [ ] Run the **Component Checklist** (see Resources).

## Instructions

### 1. Brand Alignment
You **MUST** use the variables defined in the `brand-identity` skill.
- ❌ `color: #ff0000;`
- ✅ `color: var(--color-error-500);`

### 2. Semantic HTML & Accessibility
- Use semantic tags (`<button>`, `<nav>`, `<article>`) over `<div>`.
- Ensure strict ARIA compliance for interactive elements.
- All images must have `alt` text or `role="presentation"`.
- Touch targets must be at least 44x44px.

### 3. State Management (The "5 States" Rule)
Don't just build the "happy path." You must account for:
1.  **Loading:** Skeletons or spinners.
2.  **Error:** User-friendly error messages/retries.
3.  **Empty:** What happens when there is no data?
4.  **Success:** Feedback for successful actions.
5.  **Idle:** The default state.

### 4. Performance & Optimization
- **Images:** Use optimized formats (WebP/AVIF) and `loading="lazy"` where appropriate.
- **Animations:** Aim for 60fps. Animate only `transform` and `opacity`. Use `will-change` sparingly.
- **Code:** Avoid massive bundles. Lazy load heavy components or routes.

### 5. Testing Requirements
- **Unit Tests:** Logic and state changes must be tested (e.g., Jest/Vitest).
- **Integration:** Critical user flows must be verified.
- **Cross-Browser:** Verify functionality on Chrome, Firefox, Safari (latest 2 versions).

## Resources
- **[Component Checklist](resources/component-checklist.md)**
