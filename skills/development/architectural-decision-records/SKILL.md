---
name: architectural-decision-records
version: "1.0"
description: >
  Architecture Decision Records (ADRs) format, templates, and best practices for documenting technical decisions.
  PROACTIVELY activate for: (1) documenting significant technical decisions, (2) recording design trade-offs, (3) creating technology selection rationales.
  Triggers: "ADR", "decision record", "architecture"
group: foundation
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Architectural Decision Records (ADRs)

## What is an ADR?

An ADR documents **why** a significant technical decision was made, not just **what** was decided.

## When to Create an ADR

Create an ADR for:
- Technology selection (Next.js vs Remix, Zustand vs Redux)
- Architectural patterns (Server Components default, API design approach)
- Data modeling decisions (SQL vs NoSQL, schema design)
- Security patterns (authentication approach, authorization model)
- Performance trade-offs (caching strategy, bundling approach)

Don't create ADRs for:
- Routine code changes
- Bug fixes
- Refactoring without architectural impact

## ADR Template

```markdown
# ADR-[NUMBER]: [Title in Present Tense]

**Date**: YYYY-MM-DD
**Status**: [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]
**Deciders**: [Names]

## Context

[What problem are we solving? What forces are at play? What constraints exist?]

## Decision

[What are we doing? Be specific and concrete.]

## Consequences

### Positive Consequences
- [Benefit 1]
- [Benefit 2]

### Negative Consequences
- [Cost/Risk 1]
- [Cost/Risk 2]

### Mitigation Strategies
- [How to address negative consequence 1]
- [How to address negative consequence 2]

## Alternatives Considered

### Alternative 1: [Name]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why Rejected**: [Specific reason]

### Alternative 2: [Name]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why Rejected**: [Specific reason]

## References

- [Documentation links]
- [Related ADRs]
```

## Example ADR

```markdown
# ADR-001: Adopt React Server Components as Default

**Date**: 2025-10-23
**Status**: Accepted
**Deciders**: Engineering Team

## Context

Next.js 14+ offers two component types: Server Components (default) and Client
Components. We must decide which to use as our default pattern.

Our goals:
- Minimize client-side JavaScript bundle size
- Improve page load performance
- Maintain developer productivity

Constraints:
- Team has React experience but limited RSC knowledge
- Some features require client-side interactivity

## Decision

We will use **React Server Components** as the default for all new components.
Client Components (marked with 'use client') will be used only for:
- Interactive UI (forms with local state, buttons with onClick)
- Browser API usage (localStorage, window)
- React hooks (useState, useEffect)

## Consequences

### Positive Consequences
- **50% smaller bundles**: Less JavaScript sent to client
- **Faster page loads**: Server-rendered HTML loads immediately
- **Better SEO**: Pre-rendered content is indexable
- **Direct database access**: No need for API layer in many cases

### Negative Consequences
- **Learning curve**: Team must understand Server vs Client boundaries
- **Debugging complexity**: Errors can occur in different environments
- **Third-party library compatibility**: Not all libraries work with RSC

### Mitigation Strategies
- Provide team training on Server Component patterns
- Create reusable templates for common scenarios
- Document compatible libraries in project wiki
- Use TypeScript strict mode to catch boundary violations early

## Alternatives Considered

### Alternative 1: Client Components Default (Traditional React)
- **Pros**: Team familiar with this approach, no learning curve
- **Cons**: Larger bundles, slower performance, more boilerplate
- **Why Rejected**: Doesn't leverage Next.js 14+ performance benefits

### Alternative 2: Mix without clear default
- **Pros**: Flexibility to choose per component
- **Cons**: Inconsistent codebase, harder to review/maintain
- **Why Rejected**: Need clear patterns for team consistency

## References

- [React Server Components](https://react.dev/reference/rsc/server-components)
- [Next.js App Router](https://nextjs.org/docs/app)
```

## ADR Lifecycle

1. **Proposed** - Decision under discussion
2. **Accepted** - Decision approved and being implemented
3. **Deprecated** - Decision no longer valid but kept for history
4. **Superseded by ADR-XXX** - Decision replaced by newer ADR

Store ADRs in `docs/adr/` directory with sequential numbering.

For full examples and governance, use `/generate-adr` command.
