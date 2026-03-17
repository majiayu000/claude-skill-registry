---
name: staging-ui-first
description: UI-first implementation and staging workflow for Zeus. Use when building routes, components, or forms before backend integration, or when creating UI scaffolds with mock data and later wiring to real APIs.
---

# Staging UI First

> **Skill Purpose:** Build UI scaffolds early with mock data, validate layout and interactions, then integrate with real data sources.

---

## Core Skill Pattern

**Objective:** Deliver working UI flows fast by staging UI using mocks/placeholders, then replace with real data and auth.

**Universal Pattern:**
1. Define route/component scope from INTERFACE_CONTRACT and PRODUCT_SPEC.
2. Build UI with mock data and placeholder states.
3. Validate layout, accessibility, and responsive behavior.
4. Add loading/empty/error states.
5. Integrate real API/data once endpoints and schema are ready.

**Key Decisions (Project-Specific):**
- Mock data strategy (inline fixtures vs shared mock utilities)
- Loading/error state design
- When to switch from mock to live data
- Auth gating requirements for staged UI

---

## Project-Specific Implementation Notes (Zeus)

**Default stack:** Next.js App Router + shadcn/ui + Tailwind CSS.

**Staging rules:**
- Use mocks for UI-first build until API and schema are available.
- Clearly label mock data blocks and TODOs for integration.
- Preserve component contracts (props, types) to ease later wiring.

---

## Example Staging Flow (Next.js App Router)

1. Create route skeleton and layout.
2. Render with mock data arrays and placeholder UI.
3. Add empty/error states.
4. Replace mock data with real fetch when API is ready.

```tsx
// app/(dashboard)/users/page.tsx
import { UsersTable } from '@/components/users/users-table';

const mockUsers = [
  { id: '1', name: 'Jane Doe', email: 'jane@example.com' },
  { id: '2', name: 'John Smith', email: 'john@example.com' },
];

export default function UsersPage() {
  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold">Users</h1>
      <UsersTable users={mockUsers} isLoading={false} />
    </section>
  );
}
```

---

## Checklist (Staging UI First)

- [ ] Route/component skeleton created
- [ ] Mock data wired for primary views
- [ ] Loading/empty/error states included
- [ ] Responsive behavior validated
- [ ] Accessibility basics checked (labels, focus, contrast)
- [ ] Integration TODOs noted for API wiring

---

## Best Practices

1. Keep mock data realistic (shape and size).
2. Use consistent loading and empty state patterns.
3. Avoid hard-coding auth assumptions; gate later via auth layer.
4. Keep component props stable to minimize refactors.
5. Document mock-to-real integration steps in handoff.

---

## Stop Conditions

STOP and escalate if:
- Required route contracts are missing or ambiguous.
- Mock data conflicts with known schema constraints.
- UI scope changes without updated Product Spec.

---

*Skill Version: 1.0.0*
