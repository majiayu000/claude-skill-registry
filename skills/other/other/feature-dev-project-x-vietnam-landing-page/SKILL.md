---
name: feature-dev
description: End-to-end feature implementation workflow. Triggers on "implement feature", "build feature", "develop", "create feature".
---

# Feature Development

A structured 7-phase workflow for implementing features from discovery to completion.

## When to Use

- Implementing a new page or section
- Adding a significant component or feature
- Building an integration (API, form, etc.)
- Any task that touches 3+ files

## When NOT to Use

- Bug fixes (just fix directly)
- Simple text/style changes
- Adding a single small component

## Core Principles

- Reuse existing components before creating new ones
- Follow the PXV design system (colors, typography, spacing)
- Mobile-first responsive design
- Animate thoughtfully with Framer Motion

## The 7 Phases

### Phase 1: Discovery

**Goal**: Understand what needs to be built.

1. Read the user's request carefully
2. Identify the feature's purpose and scope
3. List expected deliverables (pages, components, API routes)
4. Identify any external dependencies or data sources

### Phase 2: Exploration

**Goal**: Understand the existing codebase context.

**Actions**:
1. Read `AGENTS.md` for architecture overview
2. Identify similar existing implementations (reference examples)
3. Check `components/ui/` for reusable primitives
4. Check `components/` for reusable custom components
5. Review `tailwind.config.ts` and `globals.css` for available design tokens

**Output**: List of reusable code and patterns found.

### Phase 3: Questions

**Goal**: Resolve ambiguity before coding.

1. List any unclear requirements
2. Ask the user targeted questions (max 3-5)
3. Propose defaults for minor decisions
4. Confirm the approach before proceeding

### Phase 4: Architecture

**Goal**: Design the solution structure.

**Actions**:
1. Define the component tree
2. List new files to create and existing files to modify
3. Define TypeScript interfaces for data shapes
4. Plan the responsive layout (mobile → desktop)
5. Plan animations and transitions

**Output**: Component tree + file list + key interfaces.

### Phase 5: Implementation

**Goal**: Write the code.

**Order**:
1. Types/interfaces
2. Utility functions (`lib/`)
3. UI components (bottom-up: primitives → composites → page)
4. Page assembly
5. API routes (if needed)
6. Animations (last)

**Rules**:
- Use `"use client"` only when needed (state, effects, browser APIs)
- Use shadcn/ui primitives as building blocks
- Use `cn()` for conditional classes
- Use Framer Motion `whileInView` for scroll animations
- Test each component as you build

### Phase 6: Review

**Goal**: Self-review the implementation.

**Checklist**:
- [ ] TypeScript: no `any` types, proper interfaces
- [ ] Responsive: works on mobile (320px), tablet (768px), desktop (1280px)
- [ ] Design system: uses PXV brand colors and typography
- [ ] Components: reuses existing ui/ components
- [ ] Accessibility: alt text, semantic HTML, keyboard navigation
- [ ] Performance: images optimized, no unnecessary re-renders
- [ ] Animations: smooth, no layout shifts, `viewport={{ once: true }}`

### Phase 7: Summary

**Goal**: Report what was built.

**Output**:
- Files created/modified
- Components added
- Key decisions made
- Any follow-up tasks or known limitations

## Related Skills

| Skill | When to Chain |
|-------|--------------|
| planning | Before feature-dev, to break a large feature into phases |
| web-test | After feature-dev, to test in browser |
| review-pr | After feature-dev, to review code quality |
| git-commit | After feature-dev, to commit and push |
