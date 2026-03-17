---
name: frontend-ui-ux-design
description: Creates comprehensive frontend UI/UX designs including user interfaces, design systems, component libraries, responsive layouts, and accessibility implementations. Produces wireframes, mockups, design specifications, and implementation guidelines. Use when designing user interfaces, creating design systems, building component libraries, implementing responsive designs, ensuring accessibility compliance, or when users mention UI design, UX design, interface design, design systems, user experience, or frontend design patterns.
---

# Frontend UI/UX Design

## Overview

This skill enables creation of production-ready frontend UI/UX designs from research through implementation. Follow a structured design process that balances user needs, business goals, technical constraints, and accessibility requirements.

## Design Workflow

## 1. Understand Requirements

**Gather Context:**

- Project goals and success metrics
- Target audience and user personas
- Technical constraints (frameworks, browsers, devices)
- Brand guidelines and design language
- Accessibility requirements (WCAG level)

**Clarify Scope:**

- Type of deliverable (wireframes, mockups, design system, component library)
- Fidelity level (low, medium, high)
- Responsive breakpoints needed
- Browser and device support

### 2. Research & Strategy

**User Research:**

- Analyze user needs, goals, and pain points
- Review existing analytics or user feedback
- Identify key user journeys and scenarios
- Define information architecture

**For complete research process**: See [uiux-design-process.md](references/uiux-design-process.md) for detailed research, personas, journey mapping, and information architecture guidelines.

### 3. Design & Prototype

**Create Wireframes:**

- Start with low-fidelity layouts
- Focus on content hierarchy and structure
- Define user flows for key tasks
- Iterate based on feedback

**Apply Visual Design:**

- Define color palette (primary, secondary, semantic colors)
- Establish typography scale and spacing system
- Design components with variants and states
- Ensure visual hierarchy and consistency

**For design principles**: See [design-principles.md](references/design-principles.md) for visual hierarchy, consistency, simplicity, feedback, and error prevention guidelines.

**For design systems**: See [design-systems.md](references/design-systems.md) when building comprehensive design systems with design tokens, governance, and documentation.

### 4. Ensure Accessibility

**WCAG Compliance:**

- Minimum contrast ratios (4.5:1 for text, 3:1 for large text/UI)
- Keyboard navigation support
- Screen reader compatibility (semantic HTML, ARIA labels)
- Focus indicators and skip links
- Alternative text for images

**For complete accessibility guidance**: See [accessibility-guide.md](references/accessibility-guide.md) for WCAG 2.1/2.2 standards, ARIA patterns, keyboard navigation, testing tools, and compliance checklists.

### 5. Design Responsive Layouts

**Mobile-First Approach:**

- Start with mobile design (320px minimum)
- Progressively enhance for tablets (768px+)
- Optimize for desktop (1024px+, 1440px+)
- Use fluid grids and flexible images
- Apply appropriate layout patterns

**For responsive patterns**: See [responsive-design.md](references/responsive-design.md) for breakpoints, layout patterns (fluid grid, column drop, off-canvas), responsive navigation, typography, images, tables, forms, and container queries.

### 6. Build Component Libraries

**Component Design:**

- Design atomic components (buttons, inputs, icons)
- Create molecule components (form fields, cards, menus)
- Build organism components (headers, forms, sections)
- Define component variants, states, and props
- Document component usage patterns

**For component details**: See [component-library.md](references/component-library.md) and [component-patterns.md](references/component-patterns.md) for comprehensive component catalogs with specifications, variants, states, and usage guidelines.

### 7. Optimize Performance

**Performance Considerations:**

- Optimize images (WebP/AVIF, lazy loading, responsive images)
- Minimize CSS/JS bundle sizes
- Implement critical CSS for above-the-fold content
- Use efficient animations (transform, opacity)
- Monitor Core Web Vitals (LCP, FID, CLS)

**For optimization details**: See [performance-optimization.md](references/performance-optimization.md) for image optimization, code splitting, caching strategies, and performance budgets.

### 8. Document & Handoff

**Design Deliverables:**

- Design specifications (colors, typography, spacing)
- Component documentation with variants
- Responsive breakpoint designs
- Accessibility report and compliance checklist
- Implementation guidelines and design tokens

**For output format**: See [output-format.md](references/output-format.md) for structured deliverable formats including design briefs, wireframes, visual designs, component libraries, and developer handoff materials.

## Quick Reference

### When to Load References

- **[uiux-design-process.md](references/uiux-design-process.md)** - Full design process from research through prototyping and user testing
- **[design-principles.md](references/design-principles.md)** - Core design principles (hierarchy, consistency, simplicity, feedback)
- **[design-systems.md](references/design-systems.md)** - Building comprehensive design systems with tokens and governance
- **[accessibility-guide.md](references/accessibility-guide.md)** - WCAG compliance, ARIA patterns, keyboard navigation, testing
- **[responsive-design.md](references/responsive-design.md)** - Breakpoints, layout patterns, responsive components
- **[component-library.md](references/component-library.md)** - Atomic/molecular component catalog with specifications
- **[component-patterns.md](references/component-patterns.md)** - Component patterns (forms, navigation, data display, feedback)
- **[performance-optimization.md](references/performance-optimization.md)** - Image optimization, code splitting, Core Web Vitals
- **[design-tools-and-resources.md](references/design-tools-and-resources.md)** - Design tools, frameworks, icon libraries, resources
- **[output-format.md](references/output-format.md)** - Structured deliverable formats for handoff
- **[examples.md](references/examples.md)** - Real-world design examples and patterns
- **[design-checklist.md](references/design-checklist.md)** - Quality checklist before finalizing designs

## Key Principles

**1. User-Centered Design**

- Always start with user needs and goals
- Validate assumptions through research and testing
- Prioritize usability over aesthetics

**2. Accessibility First**

- Design for all users, including those with disabilities
- Follow WCAG 2.1 AA standards minimum
- Test with keyboard navigation and screen readers

**3. Mobile-First Responsive**

- Start with smallest screen sizes
- Progressively enhance for larger screens
- Ensure touch-friendly interactions (44x44px minimum)

**4. Design System Thinking**

- Build reusable, consistent components
- Document patterns and usage guidelines
- Maintain design token systems

**5. Performance Matters**

- Optimize images and assets
- Keep bundle sizes small
- Monitor and improve Core Web Vitals

**6. Iterative Process**

- Start with low-fidelity, iterate to high-fidelity
- Gather feedback early and often
- Refine based on user testing and metrics
