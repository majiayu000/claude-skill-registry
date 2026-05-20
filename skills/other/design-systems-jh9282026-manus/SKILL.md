---
name: design-systems
description: "Build, maintain, and scale design systems including component libraries, design tokens, documentation, and governance models. Use for creating design systems from scratch, establishing component architecture, implementing design tokens for multi-brand/multi-theme support, building scalable component libraries, setting up design-to-code workflows, creating design system documentation, establishing governance processes, managing design system teams, and ensuring consistency across products and platforms."
---

# Design Systems

Build and maintain scalable design systems that ensure consistency, accelerate development, and bridge design and code.

## Overview

Design systems are comprehensive collections of reusable components, design tokens, documentation, and governance models that enable teams to build consistent user experiences at scale. This skill covers the complete design system lifecycle: architecture planning, component library development, design token implementation, documentation creation, and governance establishment. It emphasizes modern approaches including logic-driven systems, headless component architecture, automated governance, and seamless design-to-code workflows.

## Design System Components

A functional design system consists of four core elements:

| Component | Purpose | Key Deliverables |
|-----------|---------|------------------|
| **Design Tokens** | Centralized design decisions (colors, spacing, typography) | Token files (JSON), platform exports (CSS, iOS, Android) |
| **Component Library** | Reusable UI elements | Design components (Figma), code components (React, Vue, etc.) |
| **Documentation** | Usage guidelines and principles | Component docs, pattern library, design principles |
| **Governance** | Processes and standards | Contribution guidelines, review process, versioning strategy |

### Design System Maturity Levels

**Level 1: Style Guide** — Static documentation of colors, typography, spacing
- Useful for: Small teams, early-stage products
- Limitation: No reusable components, manual implementation

**Level 2: Component Library** — Reusable design and code components
- Useful for: Growing teams, multiple products
- Limitation: Components may drift between design and code

**Level 3: Design System** — Integrated tokens, components, documentation, governance
- Useful for: Large teams, enterprise products
- Benefit: Single source of truth, automated updates, scalable

**Level 4: Logic-Driven System** (2026 standard) — Connected to code, governed by data, AI-assisted
- Useful for: Mature organizations, multi-brand products
- Benefit: Design-code parity, automated governance, dynamic theming

## Design Token Architecture

Design tokens are the foundation of modern design systems, treating design decisions as data.

### Token Hierarchy

**Three-tier token structure:**

1. **Primitive tokens** — Raw values, brand-specific
   - Example: `color-blue-500: #0066CC`
   - Purpose: Reduce infinite possibilities to brand-relevant options

2. **Semantic tokens** — Meaningful, context-aware references to primitives
   - Example: `color-text-primary: {color-gray-900}`
   - Purpose: Provide guidance on usage, reduce ambiguity

3. **Component tokens** — Component-specific references to semantic tokens
   - Example: `button-background-primary: {color-action-primary}`
   - Purpose: Enable component-level theming

### Token Naming Conventions

**Semantic naming over descriptive:**

❌ **Poor:** `Blue-500`, `Gray-300`, `Font-Large`
- Problem: Changing brand color requires updating every reference

✅ **Good:** `color-action-primary`, `color-text-secondary`, `font-size-heading-1`
- Benefit: Change token value once, entire system updates

**Naming structure:**
```
[category]-[property]-[variant]-[state]

Examples:
color-background-primary
color-background-primary-hover
spacing-padding-large
font-size-body-small
border-radius-medium
```

### Multi-Mode Token Architecture

Use "Modes" (Figma Variables) for multi-brand and multi-theme support:

**Single token, multiple values:**
```
color-background-primary:
  - Light mode: #FFFFFF
  - Dark mode: #1A1A1A
  - Brand A: #F5F5F5
  - Brand B: #FAFAFA
```

**Benefits:**
- Switch entire system with one mode change
- No component instance swapping required
- Automatic cascade to all child components

### Token Distribution

**Storage format:** JSON (most flexible, platform-agnostic)

**Transformation tools:**
- **Style Dictionary** — Transform tokens to any platform format
- **Knapsack** — Token management and distribution
- **Figr Identity** — Automated token generation and sync

**Export targets:**
- CSS variables (`--color-action-primary`)
- SCSS variables (`$color-action-primary`)
- iOS (Swift objects)
- Android (XML resources)
- React Native (JavaScript objects)
- Figma Variables (design tool sync)

## Component Library Architecture

### Atomic Component Foundation

Build scalable libraries starting with atomic components:

**Atomic elements:**
- Buttons (primary, secondary, tertiary, icon)
- Typography (headings, body, labels, captions)
- Input fields (text, number, email, password)
- Icons (consistent set, multiple sizes)
- Layout containers (grid, flex, stack)
- Colors and spacing (from design tokens)

**Benefits of atomic approach:**
- Updates cascade to all variants
- Consistency enforced at foundation
- Easier to maintain (fewer base components)

### Headless Component Architecture

Separate structure from style for maximum flexibility:

**Traditional approach:**
- Create separate components for each variation
- Example: `CardWithImage`, `CardWithVideo`, `CardWithText`
- Problem: Exponential variant explosion

**Headless approach:**
- Create one "shell" component with slots
- Example: `Card` with `header`, `media`, `content`, `actions` slots
- Benefit: Infinite combinations without new components

**Implementation example:**
```
Card Shell (rigid structure + basic styling)
├─ Slot: Header (accepts any component)
├─ Slot: Media (accepts image, video, icon)
├─ Slot: Content (accepts text, lists, etc.)
└─ Slot: Actions (accepts buttons, links)

Usage:
<Card>
  <Header>Product Title</Header>
  <Media><VideoPlayer /></Media>
  <Content>Description text</Content>
  <Actions><Button>Buy Now</Button></Actions>
</Card>
```

**Benefits:**
- Drastically reduces variant count
- Greater design flexibility
- Easier to maintain (one component, not dozens)

### Component Documentation Requirements

Each component needs comprehensive documentation:

**Essential documentation:**
1. **Purpose** — What is this component for?
2. **Usage guidelines** — When to use (and when not to use)
3. **Variants** — All available variations
4. **Properties/Props** — Configurable options
5. **Accessibility** — ARIA labels, keyboard navigation, screen reader support
6. **Examples** — Common use cases with code
7. **Do's and Don'ts** — Visual examples of correct and incorrect usage

**Documentation tools:**
- **Storybook** — Interactive component documentation for developers
- **Zeroheight** — Design system documentation platform
- **Supernova** — Design-to-code documentation
- **Notion/Confluence** — General documentation (less specialized)

### Design-to-Code Workflow

**Traditional workflow (problematic):**
1. Designer creates mockups in Figma
2. Developer builds components in code
3. Design and code drift over time
4. Manual effort to keep in sync

**Modern workflow (2026 best practice):**
1. Design tokens as single source of truth (JSON)
2. Tokens sync to both Figma (Variables) and code (CSS/JS)
3. Components built in code first (or simultaneously)
4. Figma components reference code components (UXPin Merge) OR
5. Figma components generate code (Framer, Plasmic)

**Tools for design-code parity:**
- **UXPin Merge** — Design with actual React components
- **Framer** — Design components that export to React
- **Storybook** — Developer component documentation
- **Chromatic** — Visual regression testing
- **Figma Dev Mode** — Improved developer handoff

## Governance Models

### Governance Model Comparison

| Model | Structure | Pros | Cons | Best For |
|-------|-----------|------|------|----------|
| **Centralized (top-down)** | DS team controls everything | Consistency, quality control | Bottleneck, slow iteration | Small teams, strict brand requirements |
| **Centralized (service)** | DS team serves feature teams | Responsive to needs | System bloat, hard to say no | Medium teams, diverse needs |
| **Federated** | Multiple teams manage system | Distributed ownership | Inconsistency, duplication | Small organizations, early stage |
| **Hybrid** | Central team + feature team contributions | Balance of control and flexibility | Requires clear guidelines | Growing teams, maturing systems |
| **Distributed** (recommended) | Specialized roles, clear boundaries | Scalable, collaborative, innovative | Requires strong communication | Large teams, enterprise scale |

### Distributed Governance Model (2026 Best Practice)

Divide responsibilities into three pillars:

**1. Design System Team**
- **Responsibility:** Core components, primitives, design tokens, documentation
- **Goal:** Cover 80% of use cases with core system
- **Focus:** Quality, consistency, accessibility, performance

**2. Framework Team**
- **Responsibility:** Implementation across feature teams and app shells
- **Goal:** Ensure design standards met in production
- **Focus:** Code quality, integration, technical support

**3. Feature Teams**
- **Responsibility:** Product features using core components
- **Goal:** Build features quickly with system components
- **Freedom:** Extend system with localized shared libraries when needed
- **Contribution:** Propose new components for core system

**Benefits:**
- High collaboration without bottlenecks
- Teams can innovate within guardrails
- Core system stays focused and high-quality
- Feature teams not blocked by central team

### Contribution Process

**For new components:**

1. **Proposal** — Feature team proposes new component
   - Use case description
   - Frequency of need (how often will this be used?)
   - Alternatives considered (can existing components work?)

2. **Review** — Design system team evaluates
   - Does this belong in core system? (80% rule)
   - Is it generalizable beyond one feature?
   - Does it align with system principles?

3. **Decision:**
   - **Accept** → DS team builds and maintains in core system
   - **Defer** → Feature team builds in local library, revisit later
   - **Reject** → Use existing components or alternative approach

4. **Implementation** — If accepted, DS team builds to system standards
   - Design and code components
   - Documentation
   - Accessibility testing
   - Version and release

### Versioning Strategy

**Semantic versioning (MAJOR.MINOR.PATCH):**

- **MAJOR (1.0.0 → 2.0.0)** — Breaking changes (component API changes, removed props)
- **MINOR (1.0.0 → 1.1.0)** — New features (new components, new props, backward compatible)
- **PATCH (1.0.0 → 1.0.1)** — Bug fixes (no API changes)

**Release cadence:**
- **Patch releases** — As needed (bug fixes)
- **Minor releases** — Every 2-4 weeks (new features)
- **Major releases** — Every 6-12 months (breaking changes, batched)

**Communication:**
- Changelog for every release
- Migration guides for major versions
- Deprecation warnings (1-2 versions before removal)
- Slack/email announcements for significant changes

## Automated Governance

Prevent design drift through automation:

### Component Auditing

**Tools:**
- **Component Auditor Toolkit** (Figma plugin) — Scans files for detached instances and overrides
- **Design Lint** (Figma plugin) — Identifies inconsistencies in spacing, colors, typography
- **Chromatic** — Visual regression testing for code components

**Audit process:**
1. **Scan files weekly** — Automated or manual
2. **Generate report** — List of detached instances, overrides, inconsistencies
3. **Review with teams** — Understand why drift occurred
4. **Fix or formalize** — Either fix the drift or add variant to system

### Automated Testing

**Visual regression testing:**
- Take screenshots of components
- Compare to baseline on every code change
- Flag visual differences for review
- Tools: Chromatic, Percy, BackstopJS

**Accessibility testing:**
- Automated checks (axe, WAVE, Lighthouse)
- Catch contrast issues, missing labels, keyboard navigation problems
- Run on every pull request

**Code quality:**
- Linting (ESLint, Stylelint)
- Type checking (TypeScript)
- Unit tests for component logic
- Integration tests for complex interactions

## AI-Assisted Design Systems (2026)

### AI Documentation

**Automated documentation generation:**
- AI scans component sets
- Generates usage guidelines
- Identifies accessibility requirements (contrast ratios, ARIA labels)
- Creates change logs from version diffs

**Tools:**
- Figma AI plugins
- GPT-based documentation assistants
- Automated accessibility annotation

**Benefits:**
- Frees DS team to focus on architecture and strategy
- Keeps documentation up-to-date automatically
- Reduces manual documentation burden

**Limitations:**
- AI-generated docs need human review
- May miss nuanced usage guidelines
- Best for initial drafts, not final documentation

## Accessibility in Design Systems

Build accessibility into the foundation:

### Component-Level Accessibility

**Every component must include:**
- Proper ARIA labels and roles
- Keyboard navigation support
- Focus indicators (3:1 contrast minimum)
- Screen reader announcements
- Color contrast compliance (WCAG AA minimum)
- Touch target sizes (44×44px mobile, 24×24px desktop)

**Accessibility documentation:**
- Keyboard shortcuts for each component
- Screen reader behavior
- ARIA attributes required
- Contrast requirements
- Motion/animation considerations (prefers-reduced-motion)

### System-Level Accessibility

**Design tokens for accessibility:**
- Contrast-compliant color palettes
- Sufficient spacing for touch targets
- Readable font sizes (16px minimum for body text)
- Focus indicator styles

**Testing requirements:**
- Automated testing (axe DevTools) on all components
- Manual keyboard testing
- Screen reader testing (NVDA, VoiceOver)
- User testing with people with disabilities

**Accessibility champions:**
- Designate accessibility expert on DS team
- Regular accessibility audits
- Training for all contributors

## Using the Reference Files

### When to Read Each Reference

**`/references/system-architecture.md`** — Read when planning a new design system from scratch, restructuring an existing system, deciding on token architecture, or establishing design-to-code workflows. Contains detailed architectural patterns, decision frameworks, and implementation strategies for scalable design systems.

**`/references/component-libraries.md`** — Read when building component libraries, establishing component standards, implementing headless architecture, or setting up component documentation. Provides comprehensive component patterns, atomic design methodology, variant strategies, and maintenance best practices.

**`/references/design-tokens.md`** — Read when implementing design tokens, setting up multi-brand/multi-theme systems, establishing naming conventions, or configuring token distribution pipelines. Covers token types, transformation tools, platform-specific exports, and advanced token strategies.

**`/references/documentation-governance.md`** — Read when creating design system documentation, establishing governance processes, setting up contribution workflows, or building design system teams. Includes documentation templates, governance models, versioning strategies, and team structure recommendations.
