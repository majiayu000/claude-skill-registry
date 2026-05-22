---
name: design-qa-skill
description: >
  Skill providing design QA checklists and principles for visual review across
  lanes. Used by design-review agents to enforce hierarchy, spacing, color, and
  responsiveness.
---

# Design QA Skill – Visual Review Checklists

This skill equips design-review agents (e.g. `nextjs-design-reviewer`) with
structured design QA knowledge without bloating their prompts.

It draws on established UX/UI best practices and visual design principles.

## Core QA Areas

Design review should cover:

- **Visual Hierarchy & Typography**
  - Clear heading/body/meta distinctions,
  - Appropriate type scales and weights,
  - Legibility and line height.

- **Spacing & Alignment**
  - Consistent spacing grid adherence,
  - Optical vs mathematical alignment,
  - Visual rhythm and breathing room.

- **Color & Contrast**
  - Design token compliance,
  - Sufficient contrast (WCAG AA/AAA),
  - Semantic color usage.

- **Responsive Behavior**
  - Common breakpoints: 375px (mobile), 768px (tablet), 1440px (desktop), 1920px (wide),
  - Layout reflow and component adaptation,
  - Touch targets and mobile usability.

- **Interaction & Accessibility**
  - Keyboard navigation,
  - Focus states and indicators,
  - ARIA attributes where needed,
  - Loading and error states.

## Usage Pattern

When performing design QA:

1. Load this skill and build a short internal checklist for this task based on the areas above.

2. Apply that checklist to:
   - Live UI (via Puppeteer/browser tools),
   - Screenshots or visual artifacts,
   - Code-level hints (where necessary).

3. Score issues by severity:
   - **Blocker**: Breaks core functionality or accessibility
   - **High**: Major design violations or UX problems
   - **Medium**: Noticeable inconsistencies
   - **Nit**: Minor polish issues

4. Provide a `design_score` (0-100) based on:
   - Adherence to design system tokens
   - Visual hierarchy and clarity
   - Responsive behavior
   - Overall polish and attention to detail

This skill centralizes design QA knowledge so that visual review agents remain
lightweight and focused on applying these checklists to the implementation.
