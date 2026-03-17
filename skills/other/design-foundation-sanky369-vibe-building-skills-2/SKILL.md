---
name: design-foundation
description: Establish or formalize your design system foundation. Create design tokens (color, typography, spacing, shadows, borders), define component architecture, document design principles, and build the structure that enables consistency and scalability. Works with Tailwind CSS and framework-agnostic approaches.
---

# Design Foundation

## Overview

A design foundation is the bedrock upon which all great products are built. It's not just a collection of colors and fonts—it's a system of decisions that enables your team to build consistently, quickly, and with intention.

This skill helps you create or formalize your design foundation, whether you're starting from scratch or documenting what already exists. It covers design tokens, component structure, design principles documentation, and the governance model for your system.

## Core Methodology: Token-Based Design Systems

Modern design systems are built on the concept of **design tokens**—named entities that store design decisions. Rather than hardcoding colors or spacing values throughout your codebase, tokens centralize these decisions, making them easy to maintain, theme, and scale.

### The Token Hierarchy

Design tokens are organized in layers, from most abstract to most concrete:

**Layer 1: Global Tokens (The Foundation)**
These are your base design decisions—the raw materials of your system.

```
Global Tokens:
├── Colors
│   ├── Primary: #3B82F6
│   ├── Secondary: #8B5CF6
│   ├── Success: #10B981
│   ├── Warning: #F59E0B
│   ├── Error: #EF4444
│   ├── Neutral-50: #F9FAFB
│   ├── Neutral-100: #F3F4F6
│   └── ... (up to Neutral-950)
├── Typography
│   ├── Font-Family-Base: Inter, system-ui, sans-serif
│   ├── Font-Size-Base: 16px
│   ├── Line-Height-Base: 1.5
│   └── Font-Weight: (300, 400, 500, 600, 700, 800)
├── Spacing
│   ├── Space-0: 0
│   ├── Space-1: 0.25rem (4px)
│   ├── Space-2: 0.5rem (8px)
│   ├── Space-3: 0.75rem (12px)
│   └── ... (up to Space-12+)
├── Shadows
│   ├── Shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05)
│   ├── Shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1)
│   └── ...
└── Border Radius
    ├── Radius-sm: 0.25rem (4px)
    ├── Radius-md: 0.375rem (6px)
    ├── Radius-lg: 0.5rem (8px)
    └── ...
```

**Layer 2: Semantic Tokens (The Meaning)**
These tokens assign meaning to global tokens based on context and usage.

```
Semantic Tokens:
├── Colors
│   ├── Background-Primary: {Global.Neutral-50}
│   ├── Background-Secondary: {Global.Neutral-100}
│   ├── Text-Primary: {Global.Neutral-950}
│   ├── Text-Secondary: {Global.Neutral-600}
│   ├── Border-Primary: {Global.Neutral-200}
│   ├── Interactive-Primary: {Global.Primary}
│   ├── Interactive-Hover: {Global.Primary-600}
│   ├── Interactive-Active: {Global.Primary-700}
│   ├── State-Success: {Global.Success}
│   ├── State-Warning: {Global.Warning}
│   └── State-Error: {Global.Error}
├── Typography
│   ├── Heading-1: (Font-Size: 32px, Line-Height: 1.2, Font-Weight: 700)
│   ├── Heading-2: (Font-Size: 24px, Line-Height: 1.3, Font-Weight: 600)
│   ├── Body-Large: (Font-Size: 18px, Line-Height: 1.5, Font-Weight: 400)
│   ├── Body-Regular: (Font-Size: 16px, Line-Height: 1.5, Font-Weight: 400)
│   ├── Body-Small: (Font-Size: 14px, Line-Height: 1.5, Font-Weight: 400)
│   └── Caption: (Font-Size: 12px, Line-Height: 1.4, Font-Weight: 500)
├── Spacing
│   ├── Padding-Component: {Global.Space-4}
│   ├── Padding-Section: {Global.Space-8}
│   ├── Margin-Component: {Global.Space-3}
│   └── Gap-Component: {Global.Space-4}
└── Shadows
    ├── Elevation-1: {Global.Shadow-sm}
    ├── Elevation-2: {Global.Shadow-md}
    └── Elevation-3: {Global.Shadow-lg}
```

**Layer 3: Component Tokens (The Application)**
These tokens are specific to individual components and use semantic tokens as their values.

```
Component Tokens:
├── Button
│   ├── Button-Primary-Background: {Semantic.Interactive-Primary}
│   ├── Button-Primary-Background-Hover: {Semantic.Interactive-Hover}
│   ├── Button-Primary-Text: {Semantic.Text-Inverse}
│   ├── Button-Padding: {Semantic.Padding-Component}
│   └── Button-Border-Radius: {Global.Radius-md}
├── Card
│   ├── Card-Background: {Semantic.Background-Primary}
│   ├── Card-Border: {Semantic.Border-Primary}
│   ├── Card-Padding: {Semantic.Padding-Component}
│   ├── Card-Border-Radius: {Global.Radius-lg}
│   └── Card-Shadow: {Semantic.Elevation-1}
└── Input
    ├── Input-Background: {Semantic.Background-Primary}
    ├── Input-Border: {Semantic.Border-Primary}
    ├── Input-Border-Hover: {Semantic.Border-Secondary}
    ├── Input-Text: {Semantic.Text-Primary}
    ├── Input-Padding: {Semantic.Padding-Component}
    └── Input-Border-Radius: {Global.Radius-md}
```

### Implementing Tokens with Tailwind CSS

Tailwind CSS is designed around the concept of tokens. Your `tailwind.config.js` file is essentially your token system:

```javascript
module.exports = {
  theme: {
    // Global Tokens
    colors: {
      primary: {
        50: '#EFF6FF',
        100: '#DBEAFE',
        500: '#3B82F6',
        600: '#2563EB',
        700: '#1D4ED8',
        950: '#0C2340',
      },
      secondary: {
        50: '#F3E8FF',
        500: '#8B5CF6',
        600: '#7C3AED',
        950: '#2E1065',
      },
      success: '#10B981',
      warning: '#F59E0B',
      error: '#EF4444',
      neutral: {
        50: '#F9FAFB',
        100: '#F3F4F6',
        600: '#4B5563',
        950: '#030712',
      },
    },
    // Semantic Tokens (via CSS variables or custom utilities)
    extend: {
      backgroundColor: {
        'bg-primary': 'var(--color-bg-primary)',
        'bg-secondary': 'var(--color-bg-secondary)',
      },
      textColor: {
        'text-primary': 'var(--color-text-primary)',
        'text-secondary': 'var(--color-text-secondary)',
      },
      spacing: {
        'component': 'var(--space-component)',
        'section': 'var(--space-section)',
      },
    },
  },
};
```

## Design System Audit: What to Document

When formalizing your design foundation, audit and document these elements:

### 1. Design Principles
These are the "why" behind your design decisions. They guide all future work.

**Example Design Principles:**
- **Clarity First** — Every element should communicate its purpose clearly. Remove ambiguity.
- **Consistency Builds Trust** — Patterns should be predictable. Users should recognize patterns across the product.
- **Accessibility is Foundational** — Design for all users, including those with disabilities. Accessibility is not a feature; it's a requirement.
- **Simplicity Through Reduction** — Remove everything that doesn't serve the user's goal. Simplicity is the result of careful reduction.
- **Intentionality Matters** — Every decision should have a reason. Avoid arbitrary choices.
- **Performance is Part of Design** — A beautiful interface that's slow is not good design. Speed matters.

### 2. Color System
Document your color palette, including:
- Primary, secondary, and accent colors
- Neutral/grayscale colors (for text, backgrounds, borders)
- Semantic colors (success, warning, error, info)
- Color usage guidelines (when to use which color)
- Contrast ratios for accessibility (WCAG AA or AAA)
- Dark mode variants (if applicable)

**Audit Questions:**
- How many colors are actually used in your product?
- Are colors used consistently?
- Do all color combinations meet WCAG AA contrast requirements?
- Do you have a dark mode? If so, are tokens defined for it?

### 3. Typography System
Document your typography, including:
- Font families (primary, secondary, monospace)
- Font sizes (and the logic behind them—e.g., modular scale)
- Font weights and their usage
- Line heights and letter spacing
- Type scales for different contexts (headings, body, captions)

**Audit Questions:**
- How many different font sizes are used?
- Is there a logical progression (e.g., 12px, 14px, 16px, 18px, 20px, 24px, 32px)?
- Are font weights used consistently?
- Is line height appropriate for readability?

### 4. Spacing System
Document your spacing, including:
- Base unit (e.g., 4px, 8px)
- Spacing scale (e.g., 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px)
- Padding conventions (inside components)
- Margin conventions (between components)
- Gap conventions (between grid items, flex items)

**Audit Questions:**
- How many different spacing values are used?
- Is there a consistent scale?
- Are padding, margin, and gap used consistently?

### 5. Component Library
Document your components, including:
- Component name and purpose
- Component variants (primary, secondary, small, large, etc.)
- Component states (default, hover, active, disabled, loading, error)
- Component props and their defaults
- Accessibility considerations
- Usage examples

**Audit Questions:**
- What components exist in your product?
- Are they documented?
- Are they reusable or one-off?
- Are they accessible?

### 6. Responsive Breakpoints
Document your responsive design strategy:
- Breakpoints (mobile, tablet, desktop, wide)
- How components behave at each breakpoint
- Mobile-first vs. desktop-first approach
- Responsive typography strategy

### 7. Shadows, Borders, and Other Details
Document:
- Shadow system (elevation levels)
- Border radius scale
- Border styles and widths
- Transition and animation durations
- Z-index scale

## How to Use This Skill with Claude Code

### Audit Your Current Design

```
"I'm using the design-foundation skill. Can you audit my current design system?
- Analyze my Tailwind config
- Identify inconsistencies in colors, spacing, typography
- Suggest improvements
- Create a design token system based on what I have"
```

Claude Code will:
1. Analyze your current design
2. Identify inconsistencies and opportunities
3. Create a comprehensive design token system
4. Suggest a migration path if you're formalizing an existing design

### Create a Design System from Scratch

```
"I'm starting from scratch. Can you help me create a design foundation?
- Define design principles for my product
- Create a color system (I want a modern, professional look)
- Create a typography system
- Create a spacing system
- Create a component library structure"
```

Claude Code will:
1. Create design principles tailored to your product
2. Generate a complete color system with accessibility considerations
3. Define typography scales and usage
4. Create spacing systems
5. Scaffold a component library structure

### Formalize Existing Design

```
"We have a design system that's not well-documented. Can you:
- Extract design tokens from our current Tailwind config
- Document our component library
- Create design principles based on our current design
- Suggest improvements and inconsistencies"
```

Claude Code will:
1. Extract and organize your existing tokens
2. Document your components
3. Create design principles that reflect your current design
4. Identify and suggest fixes for inconsistencies

### Generate Design System Documentation

```
"Can you create comprehensive documentation for our design system?
- Design principles
- Color system with usage guidelines
- Typography system with examples
- Spacing system with examples
- Component library with all variants and states
- Accessibility guidelines
- Responsive design guidelines"
```

Claude Code will generate:
1. Markdown documentation for your design system
2. Code examples for each section
3. Visual examples (if using Claude's image generation)
4. Accessibility guidelines integrated throughout

## Design Critique: Evaluating Your Foundation

Claude Code can critique your design foundation:

```
"Can you evaluate my design foundation?
- Is my color system coherent?
- Are my typography scales appropriate?
- Is my spacing system logical?
- Are there inconsistencies I'm missing?
- What's one thing I could improve immediately?"
```

## Integration with Other Skills

The design-foundation skill is foundational to all other skills:
- **layout-system** — Uses tokens for spacing and responsive behavior
- **typography-system** — Refines and extends the typography foundation
- **color-system** — Refines and extends the color foundation
- **component-architecture** — Uses tokens for component styling
- **accessibility-excellence** — Ensures tokens support accessibility
- **interaction-design** — Uses tokens for transitions and animations

## Key Principles

**1. Tokens Enable Consistency**
When design decisions are centralized in tokens, consistency becomes automatic.

**2. Semantic Tokens Enable Flexibility**
By separating global tokens from semantic tokens, you can support dark mode, theming, and accessibility features without duplicating code.

**3. Documentation Enables Adoption**
A design system that's not documented won't be used. Invest in clear, comprehensive documentation.

**4. Governance Enables Scale**
As your team grows, clear guidelines for adding new tokens and components prevent chaos.

**5. Accessibility is Foundational**
Design tokens should encode accessibility from the start (e.g., color contrast ratios, readable font sizes).

## Common Patterns

### Pattern 1: Light and Dark Mode
Define tokens for both light and dark modes:

```javascript
// Global tokens (same for both modes)
colors: {
  primary: '#3B82F6',
  neutral: { 50: '#F9FAFB', 950: '#030712' },
}

// Semantic tokens (mode-specific)
// Light mode
backgroundColor: { 'bg-primary': '{neutral.50}' }
textColor: { 'text-primary': '{neutral.950}' }

// Dark mode
@media (prefers-color-scheme: dark) {
  backgroundColor: { 'bg-primary': '{neutral.950}' }
  textColor: { 'text-primary': '{neutral.50}' }
}
```

### Pattern 2: Component Variants
Define tokens for component variants:

```javascript
// Button variants
button: {
  primary: {
    background: '{interactive.primary}',
    text: '{text.inverse}',
  },
  secondary: {
    background: '{background.secondary}',
    text: '{text.primary}',
  },
  ghost: {
    background: 'transparent',
    text: '{interactive.primary}',
  },
}
```

### Pattern 3: Responsive Tokens
Define tokens that change at different breakpoints:

```javascript
// Typography that scales with viewport
fontSize: {
  'heading-1': ['32px', { lineHeight: '1.2' }], // desktop
  '@sm': { fontSize: '24px' }, // tablet
  '@xs': { fontSize: '20px' }, // mobile
}
```

## Checklist: Is Your Design Foundation Ready?

- [ ] Design principles are documented and shared with the team
- [ ] Color system is defined with accessibility considerations
- [ ] Typography system is defined with clear scales
- [ ] Spacing system is defined with clear logic
- [ ] All tokens are centralized (Tailwind config, CSS variables, or design tool)
- [ ] Component library is documented
- [ ] Responsive breakpoints are defined
- [ ] Dark mode (if applicable) is defined
- [ ] Accessibility guidelines are documented
- [ ] Design system governance is defined (how to add new tokens, approve changes, etc.)
- [ ] Team has access to and understands the design system
- [ ] Design system is integrated into your development workflow

A strong design foundation is not built overnight, but the investment pays dividends in consistency, speed, and team alignment.
