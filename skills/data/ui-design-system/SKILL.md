---
name: ui-design-system
description: "React UI component systems with TailwindCSS + Radix + shadcn/ui. Stack: TailwindCSS (styling), Radix UI (primitives), shadcn/ui (components), React/Next.js. Capabilities: design system architecture, accessible components, responsive layouts, theming, dark mode, component composition. Actions: review, design, build, improve, refactor UI components. Keywords: TailwindCSS, Radix UI, shadcn/ui, design system, component library, accessibility, ARIA, responsive, dark mode, theming, CSS variables, component architecture, atomic design, design tokens, variant, slot, composition. Use when: building component libraries, implementing shadcn/ui, creating accessible UIs, setting up design systems, adding dark mode/theming, reviewing UI component architecture."
license: MIT
version: 2.0.0
---

# UI/UX Design & Development Expert

**Comprehensive UI/UX design, review, and improvement for modern web applications.**

Production-ready implementations with **TailwindCSS + Radix UI + shadcn/ui** and modern React patterns.

## Stack Architecture

### The Three Pillars

**Layer 1: TailwindCSS (Styling Foundation)**
- Utility-first CSS framework with build-time generation
- Zero runtime overhead, minimal production bundles
- Design tokens: colors, spacing, typography, breakpoints
- Responsive utilities and dark mode support

**Layer 2: Radix UI (Behavior & Accessibility)**
- Unstyled, accessible component primitives
- WAI-ARIA compliant with keyboard navigation
- Focus management and screen reader support
- Unopinionated - full styling control

**Layer 3: shadcn/ui (Beautiful Components)**
- Pre-built components = Radix primitives + Tailwind styling
- Copy-paste distribution (you own the code)
- Built-in React Hook Form + Zod validation
- Customizable variants with type safety

### Architecture Hierarchy

```
Application Layer
    ↓
shadcn/ui Components (Beautiful defaults, ready-to-use)
    ↓
Radix UI Primitives (Accessible behavior, unstyled)
    ↓
TailwindCSS Utilities (Design system, styling)
```

**Key Principle:** Each layer enhances the one below. Start with Tailwind for styling, add Radix for accessible behavior, use shadcn/ui for complete components.

## Core Capabilities

### UI/UX Review & Audit
Systematic evaluation of existing interfaces:
- **Component Architecture Review:** Analyze component composition, reusability, and single responsibility
- **Accessibility Audit:** WCAG 2.1/2.2 AA/AAA compliance, keyboard navigation, screen reader support
- **Performance Analysis:** Core Web Vitals (LCP, FID, CLS), bundle size, render performance
- **Responsive Design Review:** Mobile-first implementation, breakpoint usage, container queries
- **Design System Consistency:** Token usage, spacing scale adherence, color palette compliance
- **Code Quality:** React best practices, hooks usage, state management patterns
- **Visual Hierarchy:** Typography scale, spacing rhythm, color contrast, focus indicators

### UI/UX Design
Creating production-ready interface designs:
- **Component Design:** Atomic design principles, composition patterns, variant systems
- **Layout Architecture:** Grid systems, flexbox patterns, responsive containers
- **Interaction Design:** Hover states, focus states, loading states, error states
- **Design Tokens:** Three-tier token system (primitive → semantic → component)
- **Color Systems:** OKLCH color space, accessible palettes, dark mode support
- **Typography Systems:** Scale design, hierarchy, readability optimization
- **Animation & Transitions:** Micro-interactions, loading feedback, state changes

### UI/UX Improvement
Enhancing existing implementations:
- **Accessibility Enhancement:** ARIA patterns, semantic HTML, keyboard navigation
- **Performance Optimization:** Code splitting, lazy loading, virtualization, image optimization
- **Responsive Refinement:** Breakpoint optimization, mobile-first improvements
- **Component Refactoring:** Extract shared patterns, reduce complexity, improve reusability
- **Visual Polish:** Spacing consistency, typography refinement, color harmony
- **State Management:** Optimistic updates, error handling, loading states
- **Developer Experience:** Component documentation, Storybook stories, type safety

### Styling Integration
Framework-agnostic styling approaches:
- **Tailwind with Components:** Utility-first styling for any framework
- **CSS-in-JS:** emotion, styled-components, vanilla-extract
- **CSS Modules:** Scoped styles without runtime overhead
- **Design System Integration:** Token-based styling across frameworks

## When to Use Each Layer

### Use TailwindCSS Directly When:
- Building custom layouts and spacing
- Styling static content and containers
- Rapid prototyping without complex interactions
- Non-interactive UI elements

**Example scenarios:** Hero sections, grid layouts, cards without interaction, text styling

### Use Radix UI Primitives When:
- Building custom component libraries
- Need accessibility but require custom design
- shadcn/ui doesn't have the component you need
- Full control over component structure required

**Example scenarios:** Custom date picker, unique navigation pattern, specialized modal behavior

### Use shadcn/ui Components When:
- Building standard UI components quickly
- Need beautiful defaults with customization options
- Enterprise application development
- Form-heavy applications with validation

**Example scenarios:** Admin dashboards, CRUD applications, settings pages, data tables

## Critical Design Principles

### 1. Progressive Enhancement
Start simple, enhance as needed:
1. Tailwind utilities for basic styling
2. Add Radix primitives for interaction
3. Use shadcn/ui for complete solutions
4. Customize components in your codebase

### 2. Composition Over Complexity
Build complex UIs from simple, reusable components:
- Small, focused components (single responsibility)
- Compose primitives rather than creating monoliths
- Leverage component slots and children patterns

### 3. Accessibility First
Radix UI handles accessibility automatically:
- ARIA attributes applied correctly
- Keyboard navigation built-in
- Focus management and trapping
- Screen reader compatibility

**Never override accessibility features** - enhance them.

### 4. Design Token Consistency
Use Tailwind's design system consistently:
- Stick to spacing scale (4, 8, 16, 24px)
- Use color palette (50-950 shades)
- Apply typography scale systematically
- Avoid arbitrary values unless necessary

### 5. Mobile-First Responsive
Always design mobile-first, scale up:
- Base styles for mobile
- Use breakpoints (sm, md, lg, xl, 2xl) to enhance
- Test on actual devices, not just browser resize

## Setup Strategy

### Installation Order
1. **TailwindCSS** - Foundation
2. **shadcn/ui CLI** - Includes Radix dependencies
3. **Add components** - Install only what you need
4. **Configure theme** - CSS variables + Tailwind config
5. **Setup dark mode** - Theme provider + toggle

### Configuration Best Practices

**Tailwind Config:**
- Use `content` paths correctly (scan all component files)
- Extend theme with CSS variables, not hardcoded values
- Enable dark mode with `class` strategy
- Install `tailwindcss-animate` plugin

**CSS Variables (Three-Tier System):**
```css
:root {
  /* Tier 1: Primitives (immutable) */
  --gray-50: 250 250 250;
  --gray-900: 24 24 27;
  --blue-500: oklch(0.55 0.22 264);

  /* Tier 2: Semantics (theme-aware) */
  --background: var(--gray-50);
  --foreground: var(--gray-900);
  --primary: var(--blue-500);

  /* Tier 3: Components */
  --button-height: 2.5rem;
  --card-padding: 1.5rem;
}

.dark {
  /* Only semantic tokens change */
  --background: var(--gray-900);
  --foreground: var(--gray-50);
}
```

**Color Space Recommendation:**
- **Modern**: Use OKLCH for perceptual uniformity
- **Legacy support**: Use HSL with fallbacks
- **Avoid**: RGB/HEX for design tokens (not human-readable)

**Token Storage:**
- Store in JSON for platform-agnostic distribution
- Transform to CSS variables, Swift, XML using Style Dictionary
- Version control tokens separately from component code

**Path Aliases:**
- Configure `@/components` and `@/lib` in tsconfig
- Ensure consistency between Next.js and TypeScript configs
- Use aliases in imports for cleaner code

## Integration Patterns

### Pattern 1: shadcn/ui + Custom Tailwind
Use shadcn/ui components as base, customize with Tailwind classes:
- Apply custom spacing, colors via className prop
- Override default styles with Tailwind utilities
- Maintain component accessibility

### Pattern 2: Radix Primitives + Tailwind
Build custom components from scratch:
- Use Radix for behavior (Dialog, Dropdown, etc.)
- Style completely with Tailwind utilities
- Full control over structure and appearance

### Pattern 3: Hybrid Approach
Modify shadcn/ui components in your codebase:
- Edit component files in `components/ui/`
- Add new variants, sizes, or styles
- Maintain type safety with CVA (Class Variance Authority)

### Pattern 4: Component Composition
Combine multiple primitives for complex UIs:
- Popover + Select for searchable dropdown
- Dialog + Form for modal forms
- Tabs + Cards for multi-section interfaces

## Design Token Architecture

Use three-tier token system for scalable, maintainable design systems:
- **Tier 1 (Primitive)**: Raw values (`gray-50`, `spacing-4`)
- **Tier 2 (Semantic)**: Purpose-driven (`background-primary`, `text-error`)
- **Tier 3 (Component)**: Component-specific (`button-height`, `card-padding`)

**Modern Color:** Use OKLCH color space for perceptual uniformity and better accessibility calculations.

**📖 See [DESIGN_TOKENS.md](references/DESIGN_TOKENS.md) for:**
- Complete three-tier token system implementation
- OKLCH color space guide and examples
- Token naming conventions and best practices
- CSS variable configuration
- Multi-theme support patterns

## Responsive Design Strategy

**Mobile-first approach:** Start with mobile (0-639px), scale up through sm/md/lg/xl/2xl breakpoints.

**Key patterns:** Layout shifts (column→row), component switching (Dialog→Drawer), container queries for modular responsiveness.

**📖 See [RESPONSIVE_PATTERNS.md](references/RESPONSIVE_PATTERNS.md) for:**
- Complete breakpoint strategy and implementation
- Responsive component patterns and examples
- Container queries guide
- Image optimization strategies
- Performance considerations for responsive design
- Comprehensive testing checklist

## Form Architecture

**Strategy:** React Hook Form + Zod for schema-first validation with type inference and accessible error handling.

**📖 See [CUSTOMIZATION.md](references/CUSTOMIZATION.md#form-architecture) for:**
- Complete React Hook Form + Zod setup
- Reusable field wrapper patterns
- Multi-step form implementation
- Accessibility requirements checklist

## Performance Best Practices

**Core strategies:** Code splitting (React.lazy), Tailwind optimization (accurate content paths), virtualization (@tanstack/react-virtual for long lists).

**📖 See [PERFORMANCE_OPTIMIZATION.md](references/PERFORMANCE_OPTIMIZATION.md) for:**
- Complete performance optimization guide
- Core Web Vitals optimization strategies
- Bundle analysis and tree shaking
- Common pitfalls and solutions
- Performance monitoring setup

## Component Customization & Dark Mode

### Customization Strategies
1. **Direct Modification**: Edit shadcn/ui files in your codebase
2. **Variant Extension**: Use CVA for type-safe variants
3. **Wrapper Components**: Add custom logic around base components
4. **Theme Customization**: Modify CSS variables globally

### Dark Mode Setup
1. **ThemeProvider** with next-themes
2. **Class strategy** (`class`, not media query)
3. **CSS variables** in `.dark` class
4. **Accessible toggle** component

**📖 See [CUSTOMIZATION.md](references/CUSTOMIZATION.md) for:**
- Complete customization strategies with examples
- CVA variant implementation guide
- Dark mode setup and configuration
- Design considerations and testing
- Form architecture patterns

## Accessibility Standards

### Radix UI Built-In Guarantees
- ✅ ARIA attributes applied correctly
- ✅ Keyboard navigation functional
- ✅ Focus management and trapping automatic
- ✅ Screen reader compatible

### WCAG Contrast Requirements (Critical)

**WCAG 2.1 Level AA (Legal Minimum):**
- Normal text: **4.5:1** minimum contrast ratio
- Large text (18pt/14pt bold+): **3:1** minimum
- UI components/graphics: **3:1** minimum
- **Industry standard**: Most legal requirements specify AA

**WCAG Level AAA (Enhanced):**
- Normal text: **7:1** contrast ratio
- Large text: **4.5:1** contrast ratio
- **Best practice**: Aim for AAA when design constraints allow

**Measurement:**
- Contrast ratio range: 1:1 (white on white) to 21:1 (black on white)
- Use tools: WebAIM Color Contrast Checker, browser DevTools
- Test during design phase, not after implementation

**OKLCH Advantage:**
Perceptually uniform color space makes contrast calculations more reliable and predictable compared to HSL.

### Implementation Checklist
- ✅ All text meets 4.5:1 minimum (AA standard)
- ✅ Interactive elements meet 3:1 minimum
- ✅ Provide descriptive labels (`aria-label`, `<label>`)
- ✅ Test complete keyboard navigation flow
- ✅ Verify visible focus indicators (not just browser default)
- ✅ Test with screen readers (NVDA, JAWS, VoiceOver)
- ✅ Use semantic HTML elements (`<button>`, `<nav>`, `<main>`)
- ✅ Provide alternative text for images and icons
- ✅ Ensure dark mode maintains contrast standards

### Testing Strategy
1. **Automated**: Use contrast checkers during design
2. **Manual**: Tab through entire interface
3. **Screen readers**: Test with at least one screen reader
4. **Real users**: Include users with disabilities in testing

## Common Pitfalls

Avoid these frequent issues:
1. **Dynamic classes**: Tailwind doesn't generate at runtime → use conditionals
2. **Content config**: Verify paths include all component files
3. **Import paths**: Check tsconfig.json aliases
4. **Dark mode**: Ensure ThemeProvider setup and CSS variables
5. **Accessibility**: Never remove ARIA attributes

**📖 See [PERFORMANCE_OPTIMIZATION.md](references/PERFORMANCE_OPTIMIZATION.md#common-pitfalls) for complete troubleshooting guide with 10+ common issues and solutions.**

## Resources

### Official Documentation
- **TailwindCSS:** https://tailwindcss.com/docs
- **Radix UI:** https://www.radix-ui.com/primitives
- **shadcn/ui:** https://ui.shadcn.com | https://ui.shadcn.com/llms.txt

### Authoritative Design System Sources
- **USWDS Design Tokens:** https://designsystem.digital.gov/design-tokens/
- **Smashing Magazine Naming:** https://www.smashingmagazine.com/2024/05/naming-best-practices/
- **OKLCH Color Space:** https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl
- **WCAG Contrast:** https://webaim.org/articles/contrast/

### Reference Files (Detailed Guides & Patterns)

**Core Concepts:**
- **[DESIGN_TOKENS.md](references/DESIGN_TOKENS.md)** - Three-tier token system, OKLCH, naming
- **[RESPONSIVE_PATTERNS.md](references/RESPONSIVE_PATTERNS.md)** - Breakpoints, container queries, testing
- **[CUSTOMIZATION.md](references/CUSTOMIZATION.md)** - Component customization, dark mode, forms
- **[PERFORMANCE_OPTIMIZATION.md](references/PERFORMANCE_OPTIMIZATION.md)** - Performance, Core Web Vitals, pitfalls

**Implementation References:**
- **[TAILWIND_REFERENCE.md](references/TAILWIND_REFERENCE.md)** - Complete utilities
- **[RADIX_REFERENCE.md](references/RADIX_REFERENCE.md)** - Primitives with code
- **[SHADCN_REFERENCE.md](references/SHADCN_REFERENCE.md)** - Components with install
- **[INTEGRATION_PATTERNS.md](references/INTEGRATION_PATTERNS.md)** - Advanced patterns

## Triggers & Use Cases

**Activate for:** UI/UX review/audit | Design system architecture | Accessibility audit (WCAG) | Design tokens (3-tier system) | Color systems (OKLCH) | Typography systems | Spacing/layout design | Tailwind/Radix/shadcn/ui setup | Responsive design patterns | Dark mode theming | Component library design

**Do NOT activate for:** React/Next.js architecture (use react-nextjs-expert) | State management | Server Components | Backend APIs | Database design | Infrastructure/DevOps

## Behavioral Traits

**Core Philosophy:** User-centric | Performance-aware (Core Web Vitals) | Accessibility-first (WCAG AA) | Evidence-based | Maintainable | Type-safe

**Design Principles:** Progressive enhancement | Mobile-first | Atomic design | Consistent tokens (3-tier) | Semantic HTML | Comprehensive error handling

**Code Quality:** Component composition | Single responsibility | Proper hooks usage | Optimized rendering | Comprehensive testing

## Response Approach

**Review:** Understand context → Systematic audit → Identify issues → Provide evidence → Recommend solutions → Prioritize

**Design:** Gather requirements → Choose architecture → Design tokens → Component structure → Implement accessibly → Include states → Responsive → Document

**Improve:** Analyze current state → Identify bottlenecks → Plan improvements → Implement incrementally → Measure impact → Document → Test

**Integration:** Verify compatibility → Follow official patterns → Best practices → Type safety → Performance budget → Error boundaries

## Implementation Checklist

**Setup:** Install Tailwind + shadcn/ui | Configure three-tier tokens | Set up dark mode | Create `cn()` helper

**Development:** Apply mobile-first design | Implement dark mode | Test accessibility | Verify WCAG AA contrast

**Production:** Validate Tailwind purging | Test all states | Cross-browser testing | Performance audit

**📖 Detailed checklists available in:**
- [DESIGN_TOKENS.md](references/DESIGN_TOKENS.md#implementation-checklist)
- [RESPONSIVE_PATTERNS.md](references/RESPONSIVE_PATTERNS.md#testing-checklist)
- [CUSTOMIZATION.md](references/CUSTOMIZATION.md#accessibility-requirements)
- [PERFORMANCE_OPTIMIZATION.md](references/PERFORMANCE_OPTIMIZATION.md#optimization-checklist)

## Best Practices Summary

**Design Tokens:** Three-tier system | OKLCH color space | Purpose-driven naming
**Accessibility:** WCAG AA minimum (4.5:1 text, 3:1 UI) | Keyboard navigation | Screen readers
**Performance:** Code splitting | Virtualization | Tailwind optimization
**Maintenance:** Modular components | Documentation | Version control tokens

## Skill Summary

**Primary Functions:**
1. **Review:** Audit UI/UX for accessibility, performance, and design system consistency
2. **Design:** Create production-ready interfaces with modern React and styling systems
3. **Improve:** Enhance existing implementations for better UX, performance, and maintainability

**Technology Focus:**
- TailwindCSS, Radix UI, shadcn/ui (styling layer)
- Design tokens and design systems
- Accessibility standards (WCAG 2.1/2.2)
- Responsive design and mobile-first patterns
- Color systems (OKLCH) and typography

**Activation Triggers:**
- UI/UX review, audit, or analysis requests
- Design system architecture and token design
- Accessibility improvements (WCAG compliance)
- Tailwind/Radix/shadcn/ui implementation
- Responsive design and mobile-first development
- Color system and typography design

**Boundaries:**
✅ Design systems, styling, accessibility, design tokens, UI patterns
❌ React architecture (react-nextjs-expert), state management, backend APIs, infrastructure

---

**Skill Version:** 2.1.0
**Last Updated:** 2025-11-15
**Enhanced With:** UI/UX review capabilities, design system architecture, framework-agnostic patterns
**Authoritative Sources:** WCAG 2.1/2.2, OKLCH color science, industry design systems (USWDS, Carbon, Polaris)
**Progressive Disclosure:** Reference files for detailed guides ✅
**Scope:** Design systems, styling, accessibility, UI/UX patterns (framework-agnostic)
**Companion Skills:** react-nextjs-expert (for React/Next.js architecture and state management)
