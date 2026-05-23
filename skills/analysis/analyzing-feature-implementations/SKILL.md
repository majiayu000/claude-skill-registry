---
name: analyzing-feature-implementations
description: Analyzes an existing software feature implementation.
```

# Analyzing Feature Implementations
This skill produces a structured, LLM-oriented implementation report for cross-project comparison, tradeoff analysis, and improvement recommendations. 

Use when documenting current feature internals, comparing similar features across repositories, or preparing inputs for LLM-based design review.

## Workflow
1. Resolve feature name -> kebab-case.
2. Discover implementation surface:
   - Identify entrypoints, routes/handlers, core service objects, and integration points.
3. Build "Code map":
   - List primary files and the key identifiers in each.
4. Trace flows:
   - Typical happy path + 2–3 important edge/error paths.
5. Extract interfaces and contracts:
   - API schema, request/response, events, DB schema, config.
6. Identify tradeoffs:
   - What the implementation optimizes for and what it sacrifices.
7. Writes a report to doc/feature-description if folder does not exist create one.
