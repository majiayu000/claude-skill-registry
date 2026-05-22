---
name: ui-creator
description: This skill should be used when users want to create new UIs, improve existing UIs, compare UI variations (A/B testing), or build component libraries. Combines visual design principles with code implementation (React/Vue) and Playwright-based evaluation to objectively assess UI quality through accessibility audits, performance metrics, and visual regression testing. Use when tasks involve UI design, component creation, accessibility testing, or design system development.
---

# UI Creator

## Overview

To create high-quality user interfaces, combine visual design principles with practical implementation and objective evaluation. This skill provides comprehensive guidance for creating new UIs from descriptions, analyzing and improving existing interfaces, A/B testing variations, and building accessible component libraries. Uniquely integrates Playwright automation to objectively evaluate UI quality through accessibility audits, performance metrics, and visual regression testing.

**Current Standards (2025):**
- **Design**: WCAG 2.2 Level AA accessibility
- **Frameworks**: React 18+, Vue 3.5+
- **Testing**: Playwright 1.48+, axe-core
- **Styling**: Tailwind CSS, CSS Modules, Styled Components
- **Performance**: Core Web Vitals (LCP < 2.5s, CLS < 0.1, FID < 100ms)

## Decision Tree: Choosing Your Workflow

```
User Request → What is the goal?
    |
    ├─ Creating new UI from description?
    │   ├─ Simple component? → Quick Start: Component Creation
    │   └─ Full page/app? → Workflow 1: Full UI Creation
    │
    ├─ Analyzing existing UI?
    │   └─ Use Workflow 2: UI Analysis & Evaluation
    │       └─ Run scripts/evaluate-ui.ts for objective metrics
    │
    ├─ Improving existing UI?
    │   └─ Use Workflow 3: UI Improvement
    │       ├─ Load references/anti-patterns.md (common mistakes)
    │       ├─ Load references/accessibility-guidelines.md (a11y issues)
    │       └─ Load references/ui-design-principles.md (design improvements)
    │
    ├─ Comparing UI variations (A/B testing)?
    │   └─ Use Workflow 4: A/B Testing Comparison
    │       └─ Run scripts/compare-variations.ts for side-by-side analysis
    │
    ├─ Building component library?
    │   └─ Use Workflow 5: Component Library Creation
    │       ├─ Use assets/component-templates/ as starting point
    │       ├─ Use assets/design-tokens.json for consistency
    │       └─ Run scripts/init-component.ts to scaffold components
    │
    ├─ Need design system guidance?
    │   └─ Load references/ui-design-principles.md
    │
    ├─ Need accessibility help?
    │   └─ Load references/accessibility-guidelines.md
    │
    └─ Need component patterns?
        └─ Load references/component-patterns.md
```

## Quick Start: Component Creation

### Creating a Button Component

To create an accessible button component quickly:

```typescript
import React from 'react';

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  ...rest
}: ButtonProps) {
  return (
    <button
      className={`button button-${variant} button-${size}`}
      {...rest}
    >
      {children}
    </button>
  );
}
```

**Use the component scaffolding script for complex components:**

```bash
npx tsx scripts/init-component.ts button --type button --framework react
```

This generates a production-ready component with:
- Full TypeScript types
- Accessibility features (ARIA, keyboard support)
- Multiple variants and states
- Test file
- Documentation

### Evaluating the Component

After creating the component, evaluate its quality:

```bash
npx tsx scripts/evaluate-ui.ts http://localhost:3000/components/button
```

This provides:
- Accessibility score (WCAG 2.2 compliance)
- Performance metrics (load time, responsiveness)
- Screenshot for visual review
- Detailed recommendations

## Workflow 1: Full UI Creation

To create a complete UI from a description, follow this systematic approach.

### Step 1: Understand Requirements

To begin UI creation:

1. **Clarify user needs**: What problem does this UI solve?
2. **Identify user personas**: Who will use this interface?
3. **Define success criteria**: What makes this UI effective?
4. **List required components**: Buttons, forms, navigation, etc.
5. **Determine constraints**: Platform, browser support, performance budgets

**Example conversation:**
- User: "Create a dashboard for tracking fitness goals"
- Claude: "I'll create a fitness dashboard. A few questions:
  - What metrics should be displayed? (steps, calories, weight, etc.)
  - What's the primary action users should take?
  - Mobile-first or desktop-first design?
  - Any brand colors or design preferences?"

### Step 2: Design the UI

To design the interface:

1. **Apply design principles**:
   - Visual hierarchy (most important elements larger/bolder)
   - Consistent spacing (8-point grid: 8px, 16px, 24px, 32px)
   - Color psychology (blue for trust, green for success, red for errors)
   - Whitespace for breathing room
   - Load `references/ui-design-principles.md` for comprehensive guidance

2. **Ensure accessibility**:
   - Sufficient color contrast (4.5:1 for text, 3:1 for UI elements)
   - Semantic HTML structure
   - Keyboard navigation support
   - Screen reader compatibility
   - Load `references/accessibility-guidelines.md` for WCAG 2.2 requirements

3. **Choose design tokens**:
   - Use `assets/design-tokens.json` as a starting point
   - Define colors, spacing, typography, border radius, shadows
   - Maintain consistency across components

4. **Create visual mockup** (optional):
   - Describe layout and visual design
   - Use design principles to guide decisions
   - Consider responsive breakpoints (mobile: 375px, tablet: 768px, desktop: 1280px)

### Step 3: Implement the Code

To implement the UI:

1. **Choose framework**:
   - React (most common, 2025): Component-based, hooks, TypeScript
   - Vue 3.5+: Composition API, `<script setup>` syntax

2. **Structure components**:
   - Break UI into small, focused components
   - Use composition over configuration
   - Follow single responsibility principle
   - Load `references/component-patterns.md` for patterns

3. **Implement with accessibility**:
   - Use semantic HTML (`<button>`, `<nav>`, `<main>`)
   - Add ARIA attributes where needed
   - Ensure keyboard navigation
   - Include focus indicators

4. **Style with consistency**:
   - Use design tokens from Step 2
   - Choose styling approach (Tailwind, CSS Modules, Styled Components)
   - Apply consistent spacing and typography
   - Support dark mode (2025 expectation)

**Example implementation:**

```typescript
// Dashboard.tsx
import { Card, CardHeader, CardBody } from '@/components/Card';
import { MetricCard } from '@/components/MetricCard';

export function FitnessDashboard() {
  return (
    <main className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Fitness Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard
          title="Steps Today"
          value="8,432"
          goal="10,000"
          icon={<StepsIcon />}
        />
        <MetricCard
          title="Calories Burned"
          value="420"
          goal="500"
          icon={<CaloriesIcon />}
        />
        <MetricCard
          title="Active Minutes"
          value="45"
          goal="60"
          icon={<TimeIcon />}
        />
      </div>
    </main>
  );
}
```

### Step 4: Evaluate with Playwright

To objectively assess UI quality:

```bash
# Evaluate accessibility and performance
npx tsx scripts/evaluate-ui.ts http://localhost:3000/dashboard --a11y --performance --screenshot

# Results:
# - Accessibility: 0 violations (100% WCAG 2.2 AA compliant)
# - Performance: LCP 1.2s, CLS 0.02
# - Score: 95/100
# - Screenshots saved to ./ui-evaluation/
```

Load `references/playwright-evaluation.md` for detailed evaluation patterns.

### Step 5: Iterate Based on Evaluation

To improve based on evaluation results:

1. **Fix accessibility violations**: Address any WCAG failures
2. **Optimize performance**: Reduce LCP, improve CLS
3. **Refine visual design**: Adjust based on screenshots
4. **Re-evaluate**: Run evaluation script again to verify improvements

## Workflow 2: UI Analysis & Evaluation

To analyze an existing UI objectively:

### Run Automated Evaluation

```bash
npx tsx scripts/evaluate-ui.ts https://example.com/page \
  --viewport 1920x1080 \
  --a11y \
  --performance \
  --screenshot \
  --output-dir ./analysis
```

This generates:
- **HTML report**: Visual report with screenshots and metrics
- **JSON data**: Structured evaluation data
- **Recommendations**: Specific improvements needed

### Interpret Results

To understand evaluation output:

**Accessibility Violations:**
- Critical/Serious: Fix immediately (blocks some users)
- Moderate: Fix soon (impacts user experience)
- Minor: Fix when possible (best practice)

**Performance Metrics:**
- TTFB (Time to First Byte): < 500ms good, < 200ms excellent
- FCP (First Contentful Paint): < 1.8s good, < 1.0s excellent
- LCP (Largest Contentful Paint): < 2.5s good, < 1.8s excellent
- CLS (Cumulative Layout Shift): < 0.1 good, < 0.05 excellent

**Overall Score:**
- 85-100: Excellent UI quality
- 70-84: Good, room for improvement
- 50-69: Fair, needs optimization
- < 50: Poor, significant issues

Load `references/playwright-evaluation.md` for advanced evaluation techniques.

## Workflow 3: UI Improvement

To improve an existing UI based on analysis:

### Step 1: Identify Issues

From evaluation report, categorize issues:

1. **Accessibility issues**: Load `references/accessibility-guidelines.md`
2. **Design problems**: Load `references/ui-design-principles.md`
3. **Common mistakes**: Load `references/anti-patterns.md`
4. **Performance issues**: Review performance metrics

### Step 2: Prioritize Improvements

Order by impact:

1. **Critical accessibility**: Blocks users with disabilities
2. **Major performance**: Slow load times (> 3s)
3. **Usability issues**: Confusing navigation, unclear CTAs
4. **Visual polish**: Inconsistent spacing, color contrast
5. **Nice-to-haves**: Animations, micro-interactions

### Step 3: Implement Fixes

Apply improvements systematically:

**Accessibility fixes:**
```typescript
// Before: Missing alt text
<img src="chart.png" />

// After: Descriptive alt text
<img src="chart.png" alt="Sales chart showing 25% increase in Q4" />
```

**Performance optimizations:**
```typescript
// Before: Eager loading all images
<img src="large-image.jpg" />

// After: Lazy loading with responsive images
<img
  src="large-image.jpg"
  srcSet="small.jpg 400w, medium.jpg 800w, large.jpg 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  loading="lazy"
  alt="Description"
/>
```

**Design improvements:**
```css
/* Before: Poor contrast */
.text {
  color: #999999; /* Contrast ratio: 2.3:1 (fails WCAG) */
  background: #ffffff;
}

/* After: Sufficient contrast */
.text {
  color: #333333; /* Contrast ratio: 7.0:1 (passes AAA) */
  background: #ffffff;
}
```

### Step 4: Verify Improvements

Re-run evaluation to confirm fixes:

```bash
npx tsx scripts/evaluate-ui.ts https://example.com/page --threshold 85
```

Exit code 0 if score >= 85, exit code 1 otherwise (useful for CI/CD).

## Workflow 4: A/B Testing Comparison

To compare multiple UI variations objectively:

### Create Variations

Implement design variations:

```typescript
// Variation A: Traditional button
<button className="bg-blue-600 text-white px-6 py-3 rounded">
  Sign Up
</button>

// Variation B: Outline button
<button className="border-2 border-blue-600 text-blue-600 px-6 py-3 rounded">
  Sign Up
</button>

// Variation C: Gradient button
<button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg">
  Sign Up
</button>
```

### Run Comparison

```bash
npx tsx scripts/compare-variations.ts \
  https://example.com/signup?variant=a \
  https://example.com/signup?variant=b \
  https://example.com/signup?variant=c \
  --labels "Traditional,Outline,Gradient" \
  --viewport 1920x1080
```

### Analyze Results

Comparison report shows:
- **Side-by-side screenshots**: Visual comparison
- **Accessibility scores**: Which variation is most accessible
- **Performance metrics**: Which loads fastest
- **Overall winner**: Highest combined score

**Example output:**
```
Variant A (Traditional): 90/100
Variant B (Outline): 88/100
Variant C (Gradient): 85/100 (slower FCP due to gradient rendering)

Winner: Variant A
```

## Workflow 5: Component Library Creation

To build a reusable component library:

### Step 1: Define Design System

Use `assets/design-tokens.json` as foundation:

1. **Colors**: Primary, neutral, semantic (success, error, warning)
2. **Typography**: Font families, sizes, weights, line heights
3. **Spacing**: 8-point grid system
4. **Shadows**: Elevation levels for depth
5. **Border radius**: Consistent rounded corners
6. **Animation**: Duration and easing curves

### Step 2: Create Base Components

Start with foundational components:

```bash
# Generate button component
npx tsx scripts/init-component.ts button --type button --tests --stories

# Generate input component
npx tsx scripts/init-component.ts input --type input --tests --stories

# Generate card component
npx tsx scripts/init-component.ts card --type card --tests --stories

# Generate modal component
npx tsx scripts/init-component.ts modal --type modal --tests --stories
```

Or copy from `assets/component-templates/` for reference.

### Step 3: Build Composition

Create complex components from base components:

```typescript
// Form built from Input, Button components
export function SignupForm() {
  return (
    <form>
      <Input
        label="Email"
        type="email"
        required
        helperText="We'll never share your email"
      />
      <Input
        label="Password"
        type="password"
        required
        helperText="Minimum 8 characters"
      />
      <Button variant="primary" type="submit">
        Create Account
      </Button>
    </form>
  );
}
```

### Step 4: Test & Document

For each component:

1. **Write tests**: Unit tests, accessibility tests
2. **Document props**: JSDoc comments, TypeScript types
3. **Create examples**: Storybook stories or example usage
4. **Evaluate quality**: Run Playwright evaluation

Load `references/component-patterns.md` for advanced patterns.

## Playwright Evaluation Integration

Playwright enables objective UI evaluation beyond manual review.

### Key Evaluation Capabilities

**Accessibility Auditing:**
- Automated WCAG 2.2 compliance testing with axe-core
- Detects missing alt text, poor contrast, keyboard issues
- Generates actionable violation reports

**Visual Regression Testing:**
- Screenshot capture with masking for dynamic content
- Pixel-perfect comparison for detecting unintended changes
- Cross-browser consistency testing

**Performance Measurement:**
- Core Web Vitals: LCP, CLS, FID
- TTFB, FCP, page weight
- Performance budgets enforcement

**Responsive Testing:**
- Test across multiple viewport sizes
- Validate mobile, tablet, desktop layouts
- Screenshot comparison per breakpoint

### Evaluation Scripts Usage

**evaluate-ui.ts** - Comprehensive UI evaluation:
```bash
npx tsx scripts/evaluate-ui.ts <url> [options]

Options:
  --viewport 1920x1080  # Desktop viewport
  --mobile             # Use mobile viewport (375x667)
  --a11y               # Run accessibility checks
  --performance        # Measure performance
  --screenshot         # Capture screenshots
  --threshold 85       # Minimum score (CI/CD)
```

**compare-variations.ts** - A/B testing comparison:
```bash
npx tsx scripts/compare-variations.ts <url-a> <url-b> [options]

Options:
  --labels "A,B,C"     # Custom labels
  --mobile             # Mobile comparison
  --viewport 1920x1080 # Custom viewport
```

**init-component.ts** - Component scaffolding:
```bash
npx tsx scripts/init-component.ts <name> [options]

Options:
  --type button|input|card|modal|dropdown|custom
  --framework react|vue
  --typescript true|false
  --tests true|false
  --stories true|false
```

## Resources

This skill includes comprehensive reference materials, evaluation scripts, and component templates:

### references/ui-design-principles.md
Modern UI design principles including color theory, typography, layout, spacing, visual hierarchy, and 2025 design trends (glassmorphism, minimalism, bold typography). Covers design tokens and component libraries.

**Load when:** Creating new UIs, making design decisions, choosing colors/fonts, implementing design systems, need visual design guidance.

### references/accessibility-guidelines.md
Complete WCAG 2.2 accessibility guide covering semantic HTML, ARIA patterns, keyboard navigation, screen reader support, color contrast, and common component accessibility patterns. Includes testing strategies.

**Load when:** Ensuring accessibility compliance, fixing a11y violations, implementing accessible components, keyboard navigation issues, screen reader testing.

### references/playwright-evaluation.md
Comprehensive guide to using Playwright for UI evaluation including visual regression testing, accessibility auditing with axe-core, performance measurement, responsive testing, and automated quality scoring.

**Load when:** Setting up evaluation workflows, understanding Playwright capabilities, writing visual tests, measuring performance, A/B testing comparisons.

### references/component-patterns.md
Reusable component design patterns covering props design, composition patterns, styling approaches (Tailwind, CSS Modules, CSS-in-JS), common components (Button, Input, Modal, Card), and advanced patterns (compound components, render props).

**Load when:** Building component libraries, designing component APIs, implementing complex components, composition strategies, styling decisions.

### references/anti-patterns.md
Common UI/UX mistakes to avoid including accessibility anti-patterns, design mistakes, form errors, performance issues, and mobile problems. Provides bad vs. good examples for 30+ anti-patterns.

**Load when:** Reviewing existing UIs, debugging issues, learning what to avoid, code review feedback, improving UI quality.

### scripts/evaluate-ui.ts
Playwright script for comprehensive UI evaluation with accessibility audits (axe-core), performance metrics (LCP, CLS, FCP, TTFB), screenshot capture, and HTML/JSON report generation. Includes quality scoring system.

**Use when:** Evaluating UI quality objectively, measuring accessibility compliance, checking performance, generating evaluation reports, CI/CD quality gates.

### scripts/compare-variations.ts
A/B testing comparison script for evaluating multiple UI variations side-by-side. Compares screenshots, accessibility scores, performance metrics. Generates visual comparison report with winner determination.

**Use when:** A/B testing designs, comparing UI iterations, choosing between design options, presenting options to stakeholders.

### scripts/init-component.ts
Component scaffolding tool that generates production-ready React/Vue components with TypeScript, accessibility features, tests, and documentation. Supports multiple component types (button, input, card, modal, dropdown).

**Use when:** Creating new components quickly, scaffolding component boilerplate, ensuring accessibility from the start, maintaining consistency.

### assets/component-templates/
Production-ready component templates (Button, Input) with full TypeScript types, accessibility features (ARIA, keyboard support), multiple variants, and comprehensive documentation.

**Use when:** Need reference implementations, building component libraries, learning component patterns, starting new components.

### assets/design-tokens.json
Comprehensive design token system with colors (primary, neutral, semantic), spacing (8-point grid), typography (fonts, sizes, weights), shadows, border radius, animations, and breakpoints. JSON format compatible with design tools.

**Use when:** Setting up design system, maintaining consistency, defining brand tokens, integrating with design tools, theme creation.

## Tips for Success

1. **Start with accessibility**: Design inclusively from the beginning (easier than retrofitting)
2. **Use design tokens**: Maintain consistency with centralized design values
3. **Evaluate objectively**: Use Playwright scripts for data-driven decisions
4. **Mobile-first**: Design for smallest screen, progressively enhance
5. **Test early and often**: Run evaluations during development, not just at the end
6. **Learn from templates**: Study `assets/component-templates/` for best practices
7. **Avoid anti-patterns**: Review `references/anti-patterns.md` before implementing
8. **Measure performance**: Core Web Vitals matter for user experience and SEO
9. **Document decisions**: Use design tokens and component JSDoc comments
10. **Iterate based on data**: Let evaluation scores guide improvements

## When to Load Reference Files

To optimize context usage, load reference files strategically:

- **Load ui-design-principles.md** when:
  - Creating new UI designs
  - Choosing colors, typography, spacing
  - Need design system guidance
  - Making visual design decisions

- **Load accessibility-guidelines.md** when:
  - Ensuring WCAG 2.2 compliance
  - Fixing accessibility violations
  - Implementing accessible components
  - Questions about ARIA or keyboard navigation

- **Load playwright-evaluation.md** when:
  - Setting up UI evaluation
  - Understanding Playwright capabilities
  - Writing visual regression tests
  - Measuring performance metrics

- **Load component-patterns.md** when:
  - Building component libraries
  - Designing component APIs
  - Implementing complex components
  - Composition or styling questions

- **Load anti-patterns.md** when:
  - Reviewing existing code
  - Debugging UI issues
  - Learning what to avoid
  - Improving UI quality
