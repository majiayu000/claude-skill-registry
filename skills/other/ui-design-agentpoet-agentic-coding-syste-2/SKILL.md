---
name: UI Design
description: Create beautiful, production-ready interfaces using Gemini with design system constraints
triggers:
  - "design ui"
  - "create interface"
  - "implement frontend"
  - "gemini design"
  - "build component"
---

# UI Design Skill

Generate beautiful, non-generic UI using Gemini CLI with strict design system adherence and Apple-level simplicity.

## Philosophy

**Principles**:
- Zero learning curve
- Instant value
- Delightful micro-interactions
- Beautiful by default

**Anti-Patterns to Avoid**:
- Generic purple gradients
- Overused glassmorphism
- Stock AI imagery
- Cluttered interfaces
- Too many CTAs

## Workflow

### 1. Design System Check
Read `.ai/design.json` (if exists) for:
- Brand colors
- Typography
- Component patterns
- Animation standards
- Spacing system

### 2. Inspiration Research (Optional)
```bash
"scrape design inspiration from:
 - bubble.io (clean SaaS)
 - shadcn.com (component excellence)
 - ui.aceternity.com (unique animations)
 Save screenshots to: temp/design-inspiration/"
```

### 3. Gemini Implementation
```bash
"fork terminal use gemini to implement UI:
 Component: {Name}
 Purpose: {Description}
 Requirements: {List}
 Read: .ai/design.json (if exists)
 Reference: temp/design-inspiration/ (if exists)
 Create: src/components/{ComponentName}.tsx
 Apply: Framer Motion for animations
 Ensure: TypeScript strict, accessible (WCAG AA)"
```

### 4. Claude Review
```bash
"Review Gemini's implementation:
 Check: TypeScript types, accessibility, performance
 Test: npm run build && npm run lint
 Validate: Matches design system
 If issues: Provide feedback to Gemini for fixes"
```

## Design System Enforcement

If `.ai/design.json` exists:
```typescript
// GOOD: Using design system
import design from '@/ai/design.json';
const className = `bg-[${design.colors.primary[500]}]`;

// BAD: Hard-coded colors
const className = "bg-purple-500"; // Generic!
```

## Quality Checklist

Before accepting UI implementation:
- [ ] Uses design system colors (if defined)
- [ ] Framer Motion animations present
- [ ] TypeScript strict (no `any`)
- [ ] Accessible (WCAG AA)
- [ ] Responsive (tested on mobile)
- [ ] Performance <100ms interactions
- [ ] No generic/stock elements
- [ ] Delightful micro-interactions

## Example Prompts for Gemini

### Input Component
```bash
"Create PromptInput component:
Purpose: Main input where users enter requests
Inspiration: Linear command palette + Raycast search

Requirements:
- Large textarea (4 lines, auto-expand to 12)
- Floating placeholder animation
- Gradient border on focus
- Character counter (subtle, bottom-right)
- Submit button with loading state
- Cmd+Enter shortcut

Interactions:
- Focus: Border gradient animates in
- Placeholder: Slides up and shrinks
- Auto-save: localStorage every 2s
- Loading: Pulsing gradient on border

Create: src/components/PromptInput.tsx"
```

---

**Remember**: Gemini excels at UI. Use it for all frontend work, but always Claude-review for quality!
