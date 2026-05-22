---
name: ui-ux-designer
description: This skill should be used when users request UI/UX design work, component creation, page layouts, wireframes, or design system implementation for Next.js applications using Tailwind CSS with a custom brand color palette (cream #fbfbee, yellow #ffde59, green #0b6d41).
---

# UI/UX Designer Skill

## Purpose

This skill provides comprehensive UI/UX design expertise for Next.js applications using Tailwind CSS. It focuses on creating beautiful, accessible, and responsive user interfaces using a custom brand color palette while following modern design principles and Next.js best practices.

## When to Use This Skill

Use this skill when:
- Designing or creating React components for Next.js applications
- Building page layouts, sections, or complete page designs
- Creating wireframes or mockups for new features
- Implementing the brand design system with custom colors
- Ensuring accessibility (WCAG) and responsive design standards
- Refactoring UI components to match the design system
- Creating design documentation or style guides

## Design System

The project uses a custom brand color palette:

- **Cream (#fbfbee)**: Primary background color, light surfaces
- **Yellow (#ffde59)**: Primary accent color, call-to-action buttons, highlights
- **Forest Green (#0b6d41)**: Primary text, headers, secondary buttons, important elements

For complete design system details including typography, spacing, component patterns, and accessibility guidelines, refer to `references/design-system.md`.

## Core Principles

### 1. Accessibility First
- Ensure all text meets WCAG AA contrast requirements (minimum 4.5:1)
- Brand green (#0b6d41) on cream (#fbfbee) provides 6.85:1 contrast (AAA compliant)
- Include proper ARIA labels and semantic HTML
- Support keyboard navigation
- Test with screen readers when possible

### 2. Mobile-First Responsive Design
- Start with mobile layouts (320px+)
- Use Tailwind responsive prefixes: `sm:`, `md:`, `lg:`, `xl:`
- Test across breakpoints: mobile (default), tablet (768px), desktop (1024px+)
- Ensure touch targets are minimum 44x44px

### 3. Consistent Component Patterns
- Follow established patterns in `references/design-system.md`
- Use brand colors consistently across components
- Maintain spacing consistency using Tailwind's spacing scale
- Keep component structure predictable and reusable

### 4. Performance Optimization
- Use Next.js Image component for all images
- Implement lazy loading for below-the-fold content
- Minimize layout shift with proper sizing
- Use CSS-in-JS sparingly; prefer Tailwind utilities

## Workflow

### Step 1: Understand Requirements
When asked to design or create UI:
1. Clarify the component/page purpose and user goals
2. Identify required interactive elements
3. Determine responsive behavior needs
4. Note any accessibility requirements
5. Understand data or API integration needs

### Step 2: Reference Design System
Before designing, consult `references/design-system.md` for:
- Exact color values and usage guidelines
- Typography scale and font weights
- Spacing patterns
- Component patterns for buttons, cards, forms, etc.
- Accessibility contrast ratios

### Step 3: Create Component Structure
When building React components:

```tsx
// Example structure for Next.js components
import React from 'react';

interface ComponentProps {
  // TypeScript props
}

export default function ComponentName({ props }: ComponentProps) {
  return (
    <div className="tailwind-classes">
      {/* Component content */}
    </div>
  );
}
```

### Step 4: Apply Brand Styling
Use Tailwind classes with custom brand colors:

```tsx
// Primary button example
<button className="bg-brand-yellow text-brand-green font-semibold px-6 py-3 rounded-lg hover:bg-accent-400 transition-colors">
  Call to Action
</button>

// Card example
<div className="bg-brand-cream border-2 border-brand-green rounded-xl p-6 shadow-lg">
  <h3 className="text-brand-green text-2xl font-bold mb-4">Card Title</h3>
  <p className="text-neutral-700">Card content goes here</p>
</div>
```

### Step 5: Ensure Responsiveness
Apply responsive classes systematically:

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8">
  {/* Responsive grid: 1 column mobile, 2 tablet, 3 desktop */}
</div>

<h1 className="text-2xl md:text-3xl lg:text-4xl font-bold text-brand-green">
  {/* Responsive typography */}
</h1>
```

### Step 6: Add Accessibility Features
Include proper accessibility attributes:

```tsx
<button
  className="..."
  aria-label="Submit form"
  type="submit"
>
  Submit
</button>

<nav aria-label="Main navigation">
  {/* Navigation content */}
</nav>

<img
  src="/image.jpg"
  alt="Descriptive alt text"
  loading="lazy"
/>
```

### Step 7: Optimize for Next.js
Use Next.js-specific features:

```tsx
import Image from 'next/image';
import Link from 'next/link';

// Use Next.js Image component
<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority
  className="rounded-lg"
/>

// Use Next.js Link component
<Link href="/about" className="text-brand-green hover:text-brand-yellow">
  About Us
</Link>
```

## Component Library Patterns

When creating components, follow these common patterns:

### Button Component
```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}

export default function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
  disabled = false
}: ButtonProps) {
  const baseStyles = 'font-semibold rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';

  const variants = {
    primary: 'bg-brand-yellow text-brand-green hover:bg-accent-400 focus:ring-brand-yellow',
    secondary: 'bg-brand-green text-brand-cream hover:bg-primary-700 focus:ring-brand-green',
    outline: 'border-2 border-brand-green text-brand-green hover:bg-brand-green hover:text-brand-cream focus:ring-brand-green'
  };

  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
```

### Card Component
```tsx
interface CardProps {
  children: React.ReactNode;
  variant?: 'default' | 'bordered' | 'elevated';
  className?: string;
}

export default function Card({ children, variant = 'default', className = '' }: CardProps) {
  const variants = {
    default: 'bg-white shadow-md',
    bordered: 'bg-brand-cream border-2 border-brand-green',
    elevated: 'bg-white shadow-xl'
  };

  return (
    <div className={`rounded-xl p-6 ${variants[variant]} ${className}`}>
      {children}
    </div>
  );
}
```

## Page Layout Guidelines

### Standard Page Structure
```tsx
export default function PageName() {
  return (
    <main className="min-h-screen bg-brand-cream">
      {/* Hero Section */}
      <section className="py-12 md:py-20 lg:py-24">
        <div className="container mx-auto px-4 md:px-6 lg:px-8 max-w-7xl">
          {/* Hero content */}
        </div>
      </section>

      {/* Content Sections */}
      <section className="py-12 md:py-16">
        <div className="container mx-auto px-4 md:px-6 lg:px-8 max-w-7xl">
          {/* Section content */}
        </div>
      </section>
    </main>
  );
}
```

### Container Patterns
- Use `container mx-auto` for centered content
- Add `px-4 md:px-6 lg:px-8` for responsive horizontal padding
- Apply `max-w-7xl` or similar for maximum width control
- Use `py-12 md:py-16 lg:py-20` for responsive vertical spacing

## Design Deliverables

When presenting designs, provide:

1. **Component Code**: Complete, working TypeScript/React components
2. **Usage Examples**: Show how to use the component in different contexts
3. **Props Documentation**: Document all component props and their types
4. **Accessibility Notes**: Explain accessibility features included
5. **Responsive Behavior**: Describe how component adapts across breakpoints
6. **Color Usage**: Explain which brand colors are used and why

## Iteration and Feedback

After creating designs:
1. Ask for feedback on layout, spacing, and visual hierarchy
2. Verify color usage aligns with brand expectations
3. Test responsive behavior across device sizes
4. Validate accessibility with user
5. Refine based on feedback

## Resources

- **Design System**: `references/design-system.md` - Complete design system documentation
- **Component Templates**: `assets/` folder - Reusable component templates
- **Tailwind Docs**: https://tailwindcss.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **WCAG Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/

## Best Practices

1. **Always read the design system reference** before starting design work
2. **Use the exact brand colors** - don't approximate or substitute
3. **Test accessibility** - verify contrast ratios and keyboard navigation
4. **Think mobile-first** - start with mobile layout, then enhance for desktop
5. **Keep it simple** - favor clarity and usability over complexity
6. **Use Tailwind utilities** - avoid custom CSS unless necessary
7. **Document your work** - explain design decisions and usage
8. **Iterate based on feedback** - designs evolve through collaboration
