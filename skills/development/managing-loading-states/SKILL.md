---
name: managing-loading-states
description: Logic for Suspense boundaries and skeleton loaders. Use to prevent layout shifts during data fetching.
---

# Loading States and Skeletons

## When to use this skill
- Data fetching pages (Tour List, Details).
- Button submittals.

## Techniques
- **Suspense**: Wrap async components in `<Suspense fallback={<Skeleton />} >`.
- **Skeleton Cards**: Match the height and width of the actual Tour Card.
- **Progressive Loading**: Load text first, then images.

## Instructions
- **No Layout Shift**: Ensure skeletons have exact dimensions to prevent jumping content.
- **Visuals**: Use a subtle pulse animation for skeletons.
