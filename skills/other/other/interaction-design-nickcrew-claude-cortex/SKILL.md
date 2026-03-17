---
name: interaction-design
description: User flow design, micro-interactions, and interface behavior patterns with state management for all interaction conditions. Use when designing natural interactions, feedback systems, or handling error states.
keywords:
  - interaction design
  - micro-interactions
  - state transitions
  - user flows
  - animation
  - feedback patterns
triggers:
  - interaction design
  - micro-interaction
  - loading state
  - error state
  - empty state
  - user flow
---

# Interaction Design

Design natural interactions with clear feedback that gracefully handle all states. Covers user flows, micro-interactions, state transitions, and interface behavior patterns for web and mobile applications.

## When to Use This Skill

- Designing interaction flows for new features (drag-and-drop, wizards, modals)
- Creating loading, empty, error, and success states
- Improving micro-interactions on forms, buttons, or navigation
- Designing undo/redo and recovery patterns for destructive actions
- Reviewing interaction clarity in multi-step flows
- Planning animation and transition behavior
- Designing accessible interaction patterns

## Quick Reference

| Task | Load reference |
| --- | --- |
| State patterns and micro-interactions | `skills/interaction-design/references/state-patterns.md` |

## Workflow

1. **Map all states**: What states can this element be in? (loading, empty, partial, full, error, success, disabled, offline)
2. **Design feedback**: How does the user know their action worked?
3. **Handle errors**: What happens when things go wrong? How do users recover?
4. **Consider edge cases**: Empty data, slow connections, partial failures, concurrent actions.
5. **Add delight**: Where can micro-interactions improve the experience without adding noise?

## Domain Vocabulary

**user flows**, **interaction patterns**, **micro-interactions**, **state transitions**, **feedback loops**, **error states**, **empty states**, **loading states**, **progressive disclosure**, **gesture design**, **affordances**, **haptic feedback**, **animation timing**, **skeleton screens**

## Guiding Questions

Ask these when designing any interaction:

1. "What is the natural interaction pattern here?"
2. "How do we provide feedback at each step?"
3. "What happens in error and edge cases?"

## Capabilities

### Interaction Patterns
- Natural gesture and input design (touch, mouse, keyboard)
- Multi-modal interaction design
- Voice and conversational UI patterns
- Accessibility-first interaction design

### State Design
- Loading state optimization (skeleton screens, spinners, progress bars)
- Empty state design that guides users toward action
- Error state recovery patterns
- Success state celebration and next steps
- Offline state and sync indication

### Micro-interactions
- Button and input feedback (hover, focus, active, disabled)
- Form validation feedback timing
- Progress indicators and completion signals
- Notification and alert patterns
- Transition and animation design

### Flow Design
- Multi-step wizard patterns
- Progressive disclosure implementation
- Modal and overlay interaction patterns
- Navigation and wayfinding
- Undo/redo and recovery patterns

## Example Interactions

- "Design the interaction flow for a drag-and-drop file upload"
- "Create loading and error states for this API call"
- "Improve the micro-interactions on this form"
- "Design an undo pattern for destructive actions"
- "Review this wizard flow for interaction clarity"
