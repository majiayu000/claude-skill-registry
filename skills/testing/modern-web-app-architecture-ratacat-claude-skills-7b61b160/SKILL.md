---
name: modern-web-app-architecture
description: 'Use when designing or building modern web applications in JavaScript/TypeScript
  (SPA/SSR/SSG/ISR/RSC): architecture trade-offs, state/data patterns, performance,
  testing, delivery, and team scaling.'
---

---
name: modern-web-app-architecture
description: Use when designing or building modern web applications in JavaScript/TypeScript (SPA/SSR/SSG/ISR/RSC): architecture trade-offs, state/data patterns, performance, testing, delivery, and team scaling.
---

# Modern Web App Architecture (SPA/SSR/SSG/RSC)

## Overview

Comprehensive guidance for designing and building modern web applications (including SPAs and hybrid rendering apps). This skill emphasizes trade-offs, explicit boundaries, and production-ready practices (performance, accessibility, security, testing, delivery).

**Core principle:** Everything in architecture is a trade-off. There are no "right" answers, only least-worst combinations for your specific context.

## Operating Mode (How to Use This Skill)

When activated, work in this order:

1. **Clarify context (5–10 questions max)** → users, routes, SEO, interactivity, data, auth, team, constraints.
2. **Choose a rendering strategy per route** (not “one strategy for the whole app”).
3. **Define boundaries** → feature/domain modules, shared libraries, ownership, and stable interfaces.
4. **Plan state + data** → local/shared/global/server/URL state, cache strategy, invalidation, optimistic updates.
5. **Plan non-functionals** → performance budgets + measurement, accessibility plan, security posture, observability.
6. **Produce artifacts** → short recommendations with explicit trade-offs, plus concrete next steps (folder structure, ADRs, checklists).

If the user can’t answer a question, state reasonable assumptions and continue (don’t block).

## When to Use

- Starting a new SPA or web application
- Choosing rendering strategies (CSR, SSR, SSG, ISR, RSC)
- Implementing state management
- Optimizing Core Web Vitals (LCP/INP/CLS)
- Scaling for multiple frontend teams
- Making architecture trade-off decisions
- Migrating from legacy to modern frontend

## Quick Discovery Questions (Ask First)

- What are the top 3 user journeys and their target latency (e.g., “search → product → checkout”)?
- Is **SEO** required for any routes? Which are public vs behind auth?
- What’s the **data shape**: mostly CRUD, real-time, offline-first, heavy forms, large tables/charts?
- What are the constraints: **browser support**, bundle limits, time-to-market, compliance (SOC2/HIPAA/PCI)?
- What’s the **team topology**: how many devs/teams, release cadence, ownership boundaries?
- What’s your preferred stack (React/Vue/Angular/vanilla), and are you open to TypeScript?

## Reference Files

| Topic | When to Load |
|-------|--------------|
| @references/design-patterns.md | Implementing JS patterns (Module, Observer, Factory, etc.) |
| @references/react-patterns.md | React components, hooks, state, composition |
| @references/spa-fundamentals.md | SPA architecture, routing, module organization |
| @references/micro-frontends.md | Scaling teams, independent deployments |
| @references/performance.md | Bundle size, loading, Core Web Vitals |
| @references/architecture-decisions.md | Trade-offs, coupling, fitness functions |
| @references/rendering-strategies.md | CSR vs SSR vs SSG vs ISR vs RSC |
| @references/state-management.md | Local, global, server state patterns |
| @references/security-and-auth.md | Auth choices, token storage, XSS/CSRF, CSP, API boundaries |
| @references/accessibility-and-i18n.md | WCAG basics, SPA focus mgmt, inclusive components, i18n pitfalls |
| @references/testing-and-quality.md | Testing strategy, CI quality gates, a11y checks, contract tests |
| @references/tooling-and-delivery.md | Bundling, environments, deployment, observability, feature flags |

## Quick Architecture Decision Tree

```
Project Requirements?
├─ SEO critical + dynamic content → SSR (or SSR+streaming)
├─ SEO critical + mostly static → SSG/ISR (or hybrid)
├─ Mostly behind auth + app-like UX → CSR SPA (or hybrid with pre-rendered shell)
├─ Mixed (marketing + app) → Hybrid/Islands (route-level strategy)
│
Team Size?
├─ <5 developers → Modular monolith SPA
├─ 5-15 developers → Well-structured SPA or Service-based
├─ >15 developers, multiple teams → Consider micro-frontends
│
Domain Complexity?
├─ Simple CRUD → Layered architecture
├─ Complex workflows → Domain-partitioned (DDD)
├─ Multiple bounded contexts → Micro-frontends
```

## Default Outputs (What You Should Produce)

Depending on the user request, aim to output:
- **Route strategy map**: a small table of routes → CSR/SSR/SSG/ISR/RSC + why
- **Module boundary sketch**: feature folders, shared libs, interface contracts
- **State map**: local/shared/global/server/URL, plus the chosen tooling pattern
- **Data plan**: caching/invalidation, error states, optimistic updates, pagination
- **Quality plan**: testing layers + CI gates + accessibility checks
- **Performance plan**: budgets + measurement + concrete loading strategy (split points)
- **Risk register**: top 5 risks + mitigations (e.g., hydration cost, auth posture, team coupling)

## Essential Patterns Quick Reference

### Component Patterns
| Pattern | Use When |
|---------|----------|
| Container/Presentational | Separating data from UI |
| Compound Components | Building composable APIs (Select, Menu) |
| Hooks | Sharing stateful logic without HOCs |
| Provider | Avoiding prop drilling for global data |

### State Management
| Approach | Use When |
|----------|----------|
| useState/useReducer | Local component state |
| Context | Theme, auth, low-frequency global state |
| Zustand/Jotai | Simple global state, minimal boilerplate |
| Redux Toolkit | Complex state, time-travel debugging |
| React Query/SWR | Server state, caching, background refresh |
| XState | Complex flows with explicit state machines |

### Performance Essentials
| Technique | Impact |
|-----------|--------|
| Code splitting | Reduce initial bundle |
| Lazy loading | Defer non-critical |
| React.memo | Prevent unnecessary re-renders |
| useMemo/useCallback | Stable references |
| Virtual lists | Handle large datasets |

## Architecture Characteristics (Pick 3-7)

| Characteristic | Questions to Ask |
|----------------|------------------|
| **Scalability** | How many concurrent users? Growth rate? |
| **Performance** | What's acceptable TTI? LCP target? |
| **Deployability** | How often do you ship? Independent deploys? |
| **Testability** | How easy to verify changes? |
| **Maintainability** | What's the expected lifespan? |
| **Modularity** | How often do requirements change? |

## Anti-patterns to Avoid

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| Prop drilling | Tight coupling | Context or state management |
| God components | Too many responsibilities | Split by concern |
| Premature optimization | Complexity without evidence | Profile first |
| Shared mutable state | Race conditions, bugs | Immutable patterns |
| Monolithic bundle | Slow initial load | Code splitting |
| Over-fetching | Wasted bandwidth | GraphQL or BFF |
| LocalStorage tokens by default | XSS turns into account takeover | Prefer httpOnly cookies + CSP (see security refs) |
| Global store for server data | Cache invalidation pain | Use React Query/SWR for server state |

## Performance Budgets

Budgets must be **calibrated to your users/devices**, but these are good starting points for a “fast by default” app:

| Metric | Target | Needs Work |
|--------|--------|------------|
| LCP | <2.5s | 2.5–4s |
| INP | <200ms | 200–500ms |
| CLS | <0.1 | 0.1–0.25 |
| TTFB | <800ms | 800ms–1.8s |
| Route JS (initial) | <170KB gzip | <300KB gzip |

## Sources

Synthesized from:
- Learning JavaScript Design Patterns (Osmani, 2023)
- React in Depth (Barklund, 2024)
- SPA Design and Architecture (Scott)
- Single Page Web Applications (Mikowski & Powell)
- Building Micro-Frontends (Mezzalira)
- Micro Frontends in Action (Geers)
- Responsible JavaScript (Wagner)
- High Performance Browser Networking (Grigorik)
- Web Performance in Action (Wagner)
- Frontend Architecture for Design Systems (Godbolt)
- Fundamentals of Software Architecture (Richards & Ford)
- Software Architecture: The Hard Parts (Ford et al.)
- Patterns.dev
