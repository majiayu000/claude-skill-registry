---
name: benefriches-react-best-practices
description: React best practices and performance optimization for Benefriches (Vite + Redux). Reference when writing components, implementing Redux patterns, reviewing code quality, or optimizing performance.
---

# React Best Practices for Benefriches

> **Performance optimization guidelines for React 19+ SPA with Vite + Redux**
>
> **Based on**: [Vercel React Best Practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices)
>
> **Adapted for**: Client-side rendering only

---

## When to Apply This Skill

Use these practices when:

- ✅ Writing new React components
- ✅ Implementing Redux thunks or selectors
- ✅ Reviewing code for performance issues
- ✅ Refactoring existing React code
- ✅ Optimizing bundle size
- ✅ Improving rendering performance
- ✅ Debugging slow interactions or waterfalls

---

## Rule Categories by Priority

| Priority | Category                   | Rules | Impact                          |
| -------- | -------------------------- | ----- | ------------------------------- |
| 🔴       | **Bundle Size**            | 4     | 200-800ms import cost reduction |
| 🟠       | **Async/Waterfall**        | 4     | 2-10× improvement               |
| 🟡       | **Array/Data**             | 2     | Fast-fail + immutability        |
| 🟢       | **Re-render**              | 12    | Prevent unnecessary renders     |
| 🔵       | **Bundle (Continued)**     | 2     | Load on demand                  |
| 🟣       | **Client Data**            | 2     | Scroll + storage optimization   |
| ⚫       | **Rendering Performance**  | 7     | Static hoisting + transitions   |
| ⚪       | **JavaScript Performance** | 11    | Caching + O(1) lookups          |
| 🔘       | **Advanced Patterns**      | 2     | Singletons + stable refs        |

**Total**: 31 applicable practices

---

## Quick Reference by Category

### 🔴 CRITICAL: Bundle Size Optimization

| Rule                             | Impact                 | Relevance                                 |
| -------------------------------- | ---------------------- | ----------------------------------------- |
| Avoid Barrel File Imports        | 200-800ms import cost  | Check `@/features` imports                |
| Dynamic Imports for Heavy Comp.  | Reduce initial bundle  | Lazy-load maps, forms, charts             |
| Promise.all() for Independence   | 2-10× parallel speedup | Redux thunks fetching multiple resources  |
| Dependency-Based Parallelization | Start async ops ASAP   | Complex thunks with multiple dependencies |

### 🟠 HIGH: Async/Waterfall Optimization

| Rule                          | Impact                      | Relevance                             |
| ----------------------------- | --------------------------- | ------------------------------------- |
| Defer Await Until Needed      | Avoid blocking code paths   | Conditional logic in thunks           |
| Strategic Suspense Boundaries | Show wrapper UI immediately | Feature pages with async requirements |
| Conditional Module Loading    | Load heavy libs on demand   | Charts, PDFs, advanced map features   |
| CSS content-visibility        | ~10× faster for long lists  | Site lists, project tables            |

### 🟡 MEDIUM-HIGH: Array/Data Optimization

| Rule                             | Impact                   | Relevance                         |
| -------------------------------- | ------------------------ | --------------------------------- |
| Early Length Check               | Fast-fail expensive ops  | Redux selectors, form validation  |
| Use toSorted() Instead of sort() | Immutability (critical!) | ALL sorting in reducers/selectors |

### 🟢 MEDIUM: Re-render Optimization

| Rule                                   | Impact                          | Relevance                            |
| -------------------------------------- | ------------------------------- | ------------------------------------ |
| Calculate Derived State in Render      | Avoid redundant state           | Redux selectors                      |
| Extract to Memoized Components         | Enable early returns            | Heavy presentational components      |
| Functional setState Updates            | Prevent stale closures          | Already followed via Redux           |
| Lazy State Initialization              | Compute expensive values once   | Local state with complex init        |
| Use Transitions for Non-Urgent Updates | Maintain UI responsiveness      | Search/filter inputs                 |
| Use useRef for Transient Values        | Avoid re-renders                | Animation values, scroll positions   |
| Narrow Effect Dependencies             | Reduce effect re-runs           | Extract specific values from objects |
| Put Logic in Event Handlers            | Avoid state + effect modeling   | Forms, user interactions             |
| Subscribe to Derived State             | Boolean from continuous values  | Redux selectors for UI state         |
| Defer State Reads to Usage Point       | Read dynamic state in callbacks | Event handlers                       |
| Don't Wrap Simple Expressions          | Avoid over-optimization         | Simple calculations                  |
| Extract Default Non-primitive Params   | Preserve memoization            | Memoized component props             |

### 🔵 MEDIUM: Bundle Optimization (Continued)

| Rule                         | Impact                    | Relevance                   |
| ---------------------------- | ------------------------- | --------------------------- |
| Defer Non-Critical Libraries | Load after initialization | Analytics, error tracking   |
| Preload Based on User Intent | Reduce perceived latency  | Heavy modals, project forms |

### 🟣 MEDIUM: Client Data Patterns

| Rule                            | Impact                 | Relevance                      |
| ------------------------------- | ---------------------- | ------------------------------ |
| Passive Event Listeners         | Eliminate scroll delay | Infinite scroll, animations    |
| Version + Minimize localStorage | Prevent breaks, reduce | Redux persistence, preferences |

### ⚫ LOW-MEDIUM: Rendering Performance

| Rule                                  | Impact                 | Relevance                      |
| ------------------------------------- | ---------------------- | ------------------------------ |
| Hoist Static JSX                      | Avoid re-creation      | Empty states, error messages   |
| Use Activity Component for Visibility | Preserve state/DOM     | Toggle forms/maps              |
| Explicit Conditional Rendering        | Prevent rendering 0    | Count displays                 |
| useTransition Over Manual Loading     | Built-in pending state | Replace useState loading flags |
| Optimize SVG Precision                | Reduce file size       | Map icons, illustrations       |
| Animate SVG Wrapper                   | Hardware acceleration  | Spinning icons                 |

### ⚪ LOW-MEDIUM: JavaScript Performance

| Rule                           | Impact                  | Relevance                          |
| ------------------------------ | ----------------------- | ---------------------------------- |
| Cache Repeated Function Calls  | Module-level Maps       | Area calculations, transformations |
| Build Index Maps               | O(1) vs O(n) lookups    | Redux selectors by ID              |
| Use Set/Map for Lookups        | O(1) membership checks  | Selected IDs, uniqueness filtering |
| Avoid Layout Thrashing         | Batch DOM reads/writes  | Animations, dynamic layouts        |
| Cache Property Access in Loops | Hot path optimization   | Array iterations                   |
| Cache Storage API Calls        | Avoid repeated reads    | localStorage access                |
| Combine Array Iterations       | Single loop vs multiple | Chained filter/map operations      |
| Early Return from Functions    | Skip unnecessary work   | Validation functions               |
| Hoist RegExp Creation          | Don't create in render  | Email validation, parsing          |
| Loop for Min/Max vs Sort       | O(n) vs O(n log n)      | Finding extremes                   |

### 🔘 LOW: Advanced Patterns

| Rule                         | Impact               | Relevance                    |
| ---------------------------- | -------------------- | ---------------------------- |
| Initialize App Once          | Module-level guards  | Redux store, analytics setup |
| Store Event Handlers in Refs | Stable subscriptions | Event bus listeners          |

---

## Benefriches-Specific Integration

### Redux Patterns

**Already following these best practices:**

- ✅ Functional updates (reducers use immutable patterns)
- ✅ Derived state in selectors (not duplicated in state)
- ✅ Deferred state reads (useAppSelector in components)

**Apply these explicitly:**

- 🟡 **Use `toSorted()`** instead of `sort()` in all reducers/selectors
- 🟢 **Single ViewData selector** per container (already following)
- 🔴 **Parallel async in thunks** with `Promise.all()`

### Clean Architecture Integration

**Core layer** (business logic):

- ✅ Pure functions - already optimizable with caching/memoization
- ✅ No framework deps - easy to extract heavy computations

**Infrastructure layer** (gateways):

- 🟠 **Conditional module loading** - load heavy services on demand
- 🔵 **Preload on intent** - import services before API calls

**Views layer** (React components):

- 🟢 **React.memo()** for heavy presentational components with lots of potential re-render (DO NOT pre-optimize when it's not necessary)
- ⚫ **Hoist static JSX** - extract constants outside components
- 🟠 **Suspense boundaries** - wrap data-dependent sections

### Path Aliases (`@/`)

When optimizing imports:

- 🔴 **Avoid barrel files** - use direct paths with `@/` alias
- Example: `import { X } from '@/features/create-site/core/createSite.reducer'`

---

## See Also

- **Full detailed guide**: `AGENTS.md` in this skill directory
- **Web app guide**: `apps/web/CLAUDE.md`
- **Monorepo guide**: Root `CLAUDE.md`
- **Original source**: [Vercel React Best Practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices)

---

**END OF QUICK REFERENCE** - For code examples and detailed patterns, see `AGENTS.md`.
