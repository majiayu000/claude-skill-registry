---
name: headless-component-architecture
description: Design components that provide logic and accessibility without prescribing UI styling.
---

# Headless Component Architecture

## Summary
Design components that provide logic and accessibility without prescribing UI styling.

## Key Capabilities
- Expose state and handlers via Render Props or Hooks.
- Ensure accessible aria attributes are correctly applied.
- Support total styling inversion by consumers.

## PhD-Level Challenges
- Design an API that supports all valid user interactions.
- Prevent internal state inconsistencies in controlled mode.
- Type-check slot props for type-safe consumption.

## Acceptance Criteria
- Provide a library of headless UI primitives.
- Demonstrate two distinct visual implementations of one primitive.
- Pass accessibility audits on both implementations.
