---
name: react-testing-library
description: "React Testing Library patterns and best practices. User-centric testing, queries, events, and assertions. Trigger: When testing React components with RTL."
skills:
  - conventions
  - react
  - jest
dependencies:
  "@testing-library/react": ">=14.0.0 <15.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# React Testing Library Skill

## When to Use

- Testing React components
- Simulating user interactions
- Writing maintainable tests

## Critical Patterns

- Use screen and queries
- Prefer user-event over fireEvent
- Test from user perspective

## Decision Tree

- Render or shallow? → Always render
- Need async? → Use findBy\*
- Accessibility? → Use role/label queries

## Edge Cases

- Portal/modal testing
- Async UI updates
- Custom hook testing
