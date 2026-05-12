# Consistency Review Reference

## Review Instructions

Identify related files in the project (shared interfaces, similar modules, files importing the same utilities, structurally similar code without shared imports) and read those to detect cross-file patterns. Cross-file issues are the primary focus.

## What to Review

- **Cross-file duplication** — Nearly identical logic in multiple files, copy-pasted functions with slight variation across components, repeated boilerplate that could be extracted into a shared utility, component, or module
- **Architectural inconsistency** — Mixed error handling patterns across modules, inconsistent naming conventions, different approaches to the same concern in different components
- **Abstraction opportunities** — Repeated structural patterns across files that suggest a missing shared abstraction, multiple components manually implementing the same protocol or interface pattern
- **Convention drift** — Divergent logging patterns across modules, inconsistent use of project-defined constants, types, or enums, different approaches to validation, serialization, or resource management

## Determination Criteria

Flag an issue only when ALL of these hold:

1. It spans multiple files or represents an inconsistency across components
2. The issue is discrete and actionable
3. Fixing the inconsistency or extracting the duplication would provide clear maintenance or readability benefit
4. The pattern has at least 2 concrete instances

## Priority Levels

- **P0** — Harmful inconsistency actively causing bugs or maintenance traps (e.g., error handling inconsistency where some paths swallow errors)
- **P1** — Significant duplication or architectural drift that makes changes error-prone
- **P2** — Moderate duplication or convention drift with clear extraction opportunity
- **P3** — Minor inconsistency or duplication with low maintenance impact

## What to Ignore

- Style-only differences unless they indicate a genuine pattern inconsistency
- Intentional variation documented in project guidelines

**Extra metadata:** `**File:** <path 1>, <path 2> (and others)` and `**Category:** <duplication | inconsistency | abstraction | convention-drift>`

**Verdict label:** `Consistency: <consistent | issues found>`
