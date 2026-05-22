---
name: react-native-testing-library
description: "React Native Testing Library patterns and best practices. User-centric testing, queries, events, and assertions for React Native. Trigger: When testing React Native components with RNTL."
skills:
  - conventions
  - react-native
  - jest
dependencies:
  "@testing-library/react-native": ">=12.0.0 <13.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# React Native Testing Library Skill

## When to Use

- Testing React Native components
- Simulating user interactions
- Writing maintainable tests

## Critical Patterns

- Use queries for selection
- Prefer user-event for actions
- Test from user perspective

## Decision Tree

- Render or shallow? → Always render
- Need async? → Use findBy\*
- Accessibility? → Use accessibilityLabel queries

## Edge Cases

- Native module mocks
- Async UI updates
- Platform-specific UI
