---
name: gui-develop-patterns
description: Design patterns, rules, and procedures for developing GUI features in `apps/web`. Covers migration from `optaic-v0` legacy design and new `ApiClient` integration patterns.
---

# GUI Development Patterns

Reference patterns and rules for frontend development in `apps/web`.

## 1. Design Reference Pattern

**Pattern**: "Strict Legacy Replication"
**Context**: When porting features from `optaic-v0`, the design must be preserved exactly while replacing the backend implementation.

**Reference Material**:
- **Legacy Codebase**: `v0-ui/next_app` (Project Relative)
- **Target Aesthetic**: Tailwind CSS classes must match the legacy source to ensure visual consistency.

## 2. Design Philosophy & User Persona

**Target Audience**: Investment Quant Researchers, Data Engineers, Data Scientists, Risk Quants.

**Core Requirements**:
- **Simplism & Modernity**: Clean, distraction-free, professional "FinTech" aesthetic.
- **Density w/ Digestibility**: High information density (grids, charts) but easy to scan.
- **Interactive**: Keyboard shortcuts (Esc, Enter, /) are mandatory for power users.
- **Action-Oriented**: Controls must be intuitive and immediately accessible.

## 3. The Iterative Development Process

GUI development is **iterative, not linear**.

1.  **Develop**: Port/Build using `optaic-v0` reference.
2.  **Verify**: QA using Browser (Agent `ui-ux-tester`).
    - *Check*: Alignment, Responsiveness, Data Binding.
3.  **Report**: Generate QA Report (UX Polish, Missing Backend Features).
4.  **Refine**: Fix issues, improve UX, strictly ignoring backend limitations (report them instead).
5.  **Approve**: Mark as "Production Ready".

## 4. Architecture Patterns

### Data Fetching Pattern

**Rule**: ALL data access must go through the `useApiClient` hook.
**Prohibited**: Direct `fetch()`, `axios`, or SWR fetchers without the SDK.

| Feature | Legacy Pattern (`optaic-v0`) | Modern Pattern (`optaic-trading`) |
|---------|------------------------------|-----------------------------------|
| **Auth** | Implicit Cookie/Session | `ApiClient` (Header integration) |
| **Fetch** | `fetch('/api/resource')` | `api.resource.list()` |
| **State** | Ad-hoc React state | React Query (optional) or `useEffect` + State |
| **Types** | `any` / Missing | `libs/sdk_ts` mapped types |

### Component Structure Pattern

Components should follow this structure separate logic from presentation where possible, but colocation is accepted for simpler ports.

```tsx
export const MyComponent = () => {
    // 1. Hook Initialization
    const api = useApiClient();
    const { tenantId } = useSessionStore();

    // 2. State
    const [data, setData] = useState<DataType | null>(null);

    // 3. Effect (Data Loading)
    useEffect(() => {
        if (!api) return;
        api.domain.operation().then(setData);
    }, [api]);

    // 4. Render
    return <div className="legacy-tailwind-classes">...</div>;
};
```

## 3. Migration Procedure

Use this procedure when porting a component from `optaic-v0` to `apps/web`.

1.  **Selection**: Identify the target component in `optaic-v0/dev_tools/src/ui/next_app`.
2.  **Transplant**: Copy the component file to `apps/web/src/components/...`.
3.  **Sanitization**:
    - Remove Next.js specific imports (`next/link`, `next/router`). Replace with `react-router-dom`.
    - Remove all `fetch` calls.
4.  **Integration**:
    - Inject `useApiClient`.
    - Re-implement data fetching using SDK methods.
    - Map legacy data shapes to SDK `Out` types if necessary.
5.  **Refinement**: Ensure Tailwind classes render correctly in the Vite environment.

## 4. Anti-Patterns (Blocking Rules)

> [!WARNING]
> The following patterns violate platform architecture and must be rejected during code review.

- **Backend Route Copying**: Do NOT copy Next.js API routes (`pages/api/...`). Logic must live in the Python backend (`apps/api`).
- **Raw Fetch**: No `fetch()` calls in UI components.
- **Style Deviation**: Do not "improve" the design unless explicitly requested. Start with strict parity.
