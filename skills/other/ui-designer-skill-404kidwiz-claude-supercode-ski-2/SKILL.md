---
name: ui-designer
description: Use when user needs visual UI design, interface creation, component systems, design systems, interaction patterns, or accessibility-focused user interfaces.
---

# UI Designer

## Purpose

Provides comprehensive UI design expertise specializing in creating intuitive, beautiful, and accessible user interfaces. Creates polished, functional interfaces that balance aesthetics with functionality using design systems, interaction patterns, and visual hierarchy.

## When to Use

- Visual UI design for a new feature or product
- Interface redesign or refresh required
- Design system or component library development needed
- Accessibility compliance and WCAG standards required
- Responsive design implementation across devices
- Design documentation and style guide creation

## Quick Start

**Invoke this skill when:**
- Visual UI design for new features or products needed
- Design system or component library creation required
- Accessibility compliance (WCAG 2.1 AA) needed
- Responsive design across mobile/tablet/desktop required
- Dark mode or theme variations needed
- Component specifications for developer handoff
- Interface redesign or visual refresh

**Do NOT invoke when:**
- Only implementation code needed (no design) → Use frontend-ui-ux-engineer
- UX research or user testing required → Use ux-researcher
- Backend API design → Use backend-developer
- Performance optimization without visual changes → Use performance-engineer
- Content strategy or copywriting → Use content-strategist

## Core Capabilities

### Visual Design
- Color theory and palette creation
- Typography selection and hierarchy
- Spacing and layout systems
- Icon design and iconography
- Visual consistency across components
- Brand identity application

### Component Design
- Button styles and states
- Form input patterns
- Navigation components
- Cards and content containers
- Modals and dialogs
- Alerts and notifications
- Data tables and lists

### Interaction Design
- Micro-interactions and animations
- State transitions (hover, focus, active, disabled)
- Loading states and skeletons
- Empty states and error states
- Onboarding and guidance patterns

### Accessibility Design
- WCAG 2.1 AA compliance
- Color contrast requirements
- Keyboard navigation patterns
- Screen reader compatibility
- Focus indicators and skip links

## Decision Framework

### Design System Architecture

```
Design System Scope
├─ New Product (greenfield)
│   ├─ Small startup/MVP (<10 components)
│   │   └─ Lightweight component library
│   │       • Use existing framework (Radix UI, Headless UI)
│   │       • Customize with Tailwind CSS design tokens
│   │       • 10-15 core components
│   │       • Effort: 1-2 weeks
│   │
│   ├─ Medium product (10-30 components)
│   │   └─ Custom design system
│   │       • Design tokens (colors, typography, spacing)
│   │       • 20-30 components with variants
│   │       • Documentation with Storybook
│   │       • Effort: 4-6 weeks
│   │
│   └─ Enterprise/Complex (30+ components)
│       └─ Comprehensive design system
│           • Full design token architecture
│           • 50+ components with all states
│           • Automated testing (visual regression)
│           • Governance and contribution model
│           • Effort: 3-6 months
│
└─ Multi-Platform (web + mobile)
    └─ Cross-platform design system
        • Shared design tokens (JSON)
        • Platform-specific components (where needed)
        • Use Design Tokens Community Group spec
```

### Component State Matrix

| Component | States Required | Accessibility Needs | Complexity |
|-----------|----------------|---------------------|------------|
| **Button** | default, hover, active, focus, disabled, loading | Focus indicator, aria-label | Low |
| **Input** | default, focus, error, disabled, filled | Label association, error message | Medium |
| **Dropdown** | closed, open, hover, focus, disabled, loading | Keyboard nav (↑↓), aria-expanded | High |
| **Modal** | closed, opening, open, closing, minimized | Focus trap, Esc to close, aria-modal | High |
| **Toast/Alert** | info, success, warning, error, dismissing | role="alert", auto-announce | Medium |

### Accessibility Requirements

| Use Case | Contrast Ratio | WCAG Level |
|----------|----------------|------------|
| Body text (16px+) | 4.5:1 | AA |
| Large text (24px+, 18px+ bold) | 3:1 | AA |
| UI components (buttons, inputs) | 3:1 | AA |
| Graphical objects (icons, charts) | 3:1 | AA |
| Enhanced text contrast | 7:1 | AAA |

## Best Practices

### Design Process
- Start with understanding user needs and business goals
- Leverage existing context before asking users questions
- Create multiple design concepts for exploration
- Test designs with actual users when possible
- Document design decisions and rationale

### Visual Design
- Establish clear visual hierarchy
- Use whitespace effectively for clarity
- Maintain consistent spacing rhythm
- Choose colors with contrast in mind
- Use typography to guide user attention

### Accessibility
- Design for keyboard navigation first
- Ensure 4.5:1 color contrast for text and UI
- Provide focus indicators for interactive elements
- Use semantic HTML patterns in design specs
- Support users with motor impairments

### Design Systems
- Use design tokens for consistency
- Create atomic, reusable components
- Document component usage clearly
- Provide code snippets for developers

## Integration with Other Skills

- **ux-researcher**: Collaborate on user insights and research findings
- **frontend-engineer**: Provide component specifications and implementation guidance
- **accessibility-tester**: Work on compliance and accessibility audits
- **product-manager**: Support feature design and user flows
- **react-specialist**: Provide component specs for implementation

## Tool Restrictions

**Primary Tools:**
- Read, Write, Edit, Bash for creating design specifications
- Glob, Grep for analyzing existing design files

**Cannot directly:**
- Create Figma or design software files
- Export images or assets without design tool
- Implement code directly (relies on frontend-engineer)

## Quality Checklist

### Accessibility (WCAG 2.1 AA)
- [ ] Color contrast validated (4.5:1 text, 3:1 UI)
- [ ] Keyboard navigation tested
- [ ] Focus indicators visible (2px outline, 3:1 contrast)
- [ ] Screen reader tested
- [ ] Form labels present
- [ ] Alt text provided
- [ ] Motion preferences respected (prefers-reduced-motion)

### Visual Design
- [ ] Design tokens defined
- [ ] Component states designed (default, hover, active, focus, disabled, loading, error)
- [ ] Responsive breakpoints tested (375px, 768px, 1440px+)
- [ ] Dark mode support (if applicable)
- [ ] Visual hierarchy clear
- [ ] Consistency maintained

### Component Documentation
- [ ] States documented
- [ ] Props/attributes defined
- [ ] Code examples provided
- [ ] Accessibility notes included
- [ ] Usage guidelines clear

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
