---
name: styled-jsx-resolve
description: Use styled-jsx/css resolve to style nested child components from a parent while preserving encapsulation. Use when you need to target a child component’s className from a parent.
argument-hint: "[ParentComponent] [Child selector/intent]"
---

# styled-jsx resolve Skill

When a parent must style nested child components without leaking global CSS, use styled-jsx/css "resolve".

## Rules

1. Prefer passing props/variants to the child first.
2. If the child is third-party or cannot be changed, prefer :global(...) in a narrow way.
3. Use resolve only when it materially improves scoping and maintainability.

## Output expectations

- Show the parent code using resolve tags from styled-jsx/css.
- Clearly indicate the scope class returned by resolve and where it is applied.
- Add a brief test or story demonstrating the styling effect (as feasible).
