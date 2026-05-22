---
name: ui-design
description: UI/UX and frontend design best practices guidelines (formerly frontend-design). This skill should be used when writing, reviewing, or designing frontend code to ensure accessibility, performance, and usability. Triggers on tasks involving HTML structure, CSS styling, responsive layouts, form design, animations, or accessibility improvements.
---

# UI/UX Best Practices Frontend Design

Comprehensive UI/UX and frontend design best practices guide. Contains 42 rules across 8 categories, prioritized by impact to guide accessible, performant, and user-friendly interface development.

## When to Apply

Reference these guidelines when:
- Structuring HTML for accessibility and semantics
- Writing CSS for responsive layouts and visual hierarchy
- Optimizing images and fonts for Core Web Vitals
- Designing forms with proper validation and error handling
- Adding animations and interactive elements

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Accessibility & WCAG Compliance | CRITICAL | `access-` |
| 2 | Core Web Vitals Optimization | CRITICAL | `cwv-` |
| 3 | Visual Hierarchy & Layout | HIGH | `layout-` |
| 4 | Responsive & Mobile-First Design | HIGH | `resp-` |
| 5 | Typography & Font Loading | MEDIUM-HIGH | `typo-` |
| 6 | Color & Contrast | MEDIUM | `color-` |
| 7 | Forms & Validation UX | MEDIUM | `form-` |
| 8 | Animation & Performance | LOW-MEDIUM | `anim-` |

## Quick Reference

### 1. Accessibility & WCAG Compliance (CRITICAL)

- `access-semantic-html` - Use semantic HTML elements for screen readers
- `access-keyboard-navigation` - Ensure full keyboard navigation
- `access-focus-indicators` - Provide visible focus indicators
- `access-alt-text` - Provide meaningful alt text for images
- `access-aria-labels` - Use ARIA labels for icon-only controls
- `access-target-size` - Ensure minimum touch target size (24×24px)
- `access-heading-hierarchy` - Maintain logical heading hierarchy

### 2. Core Web Vitals Optimization (CRITICAL)

- `cwv-optimize-lcp` - Optimize Largest Contentful Paint under 2.5s
- `cwv-minimize-cls` - Minimize Cumulative Layout Shift under 0.1
- `cwv-improve-inp` - Improve Interaction to Next Paint under 200ms
- `cwv-responsive-images` - Serve responsive images with srcset
- `cwv-lazy-load-offscreen` - Lazy load offscreen images and iframes
- `cwv-critical-css` - Inline critical CSS and defer the rest

### 3. Visual Hierarchy & Layout (HIGH)

- `layout-visual-hierarchy` - Establish clear visual hierarchy
- `layout-whitespace` - Use whitespace to improve readability
- `layout-f-pattern` - Design for F-pattern reading behavior
- `layout-grid-system` - Use a consistent grid system
- `layout-single-cta` - Limit to one primary CTA per screen
- `layout-proximity-grouping` - Group related elements with proximity

### 4. Responsive & Mobile-First Design (HIGH)

- `resp-mobile-first` - Design mobile-first with min-width queries
- `resp-fluid-typography` - Use fluid typography with clamp()
- `resp-container-queries` - Use container queries for components
- `resp-touch-targets` - Size touch targets for mobile (44×44px)
- `resp-viewport-meta` - Configure viewport meta tag correctly

### 5. Typography & Font Loading (MEDIUM-HIGH)

- `typo-font-display` - Use font-display to control loading behavior
- `typo-preload-fonts` - Preload critical web fonts
- `typo-readable-line-length` - Constrain line length (45-75ch)
- `typo-line-height` - Set appropriate line height (1.5-1.7)
- `typo-system-font-stack` - Use system font stack for UI elements

### 6. Color & Contrast (MEDIUM)

- `color-contrast-ratio` - Meet WCAG contrast ratio requirements (4.5:1)
- `color-not-only-indicator` - Never use color alone to convey information
- `color-dark-mode` - Support dark mode with prefers-color-scheme
- `color-semantic-palette` - Use semantic color names in design tokens

### 7. Forms & Validation UX (MEDIUM)

- `form-inline-validation` - Use inline validation after field blur
- `form-error-messages` - Write actionable error messages
- `form-labels-above` - Place labels above input fields
- `form-input-types` - Use correct HTML input types for mobile
- `form-autocomplete` - Enable browser autocomplete with correct attributes

### 8. Animation & Performance (LOW-MEDIUM)

- `anim-gpu-properties` - Animate only GPU-accelerated properties
- `anim-will-change` - Use will-change sparingly for animation hints
- `anim-reduced-motion` - Respect user motion preferences
- `anim-duration-easing` - Use appropriate animation duration and easing

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules
- Example: [access-semantic-html](references/access-semantic-html.md)

## Full Compiled Document

For the complete guide with all rules expanded: [AGENTS.md](AGENTS.md)
