---
name: nextjs-ddd-architect
description: Domain-Driven Design architecture for Next.js 16 App Router projects. Provides domain-driven folder structures, layered architecture patterns, bounded context design, and separation of concerns. Use when refactoring to DDD, designing modular architecture, organizing domains, or scaling applications with clean architecture principles.
---

# Next.js DDD Architect

Expert guidance for implementing Domain-Driven Design (DDD) architecture in Next.js 16 App Router projects with clean architecture principles, domain-driven folders, and modular design patterns.

---

## ⚠️ PRAGMATIC DDD: Avoid Over-Engineering

> **YAGNI Principle:** Apply DDD patterns ONLY where they add demonstrable value. Simple CRUD doesn't need full DDD.

### The Simpsons API: Real-World Example

This project demonstrates PRAGMATIC DDD with three pattern levels:

#### 🟢 Simple Domains (Direct Repository)

| Domain            | Pattern               | Why Simple?                       |
| ----------------- | --------------------- | --------------------------------- |
| Characters (read) | `findAllCharacters()` | Public catalog, no business rules |
| Episodes (read)   | `findAllEpisodes()`   | Public catalog, no business rules |
| Locations         | `findAllLocations()`  | Static reference data             |

```typescript
// app/_lib/repositories.ts - Direct Prisma queries
export async function findAllCharacters(limit = 50) {
  return prisma.character.findMany({ take: limit });
}
```

#### 🟡 Hybrid Domains (Read Simple, Write DDD)

| Domain     | Simple Operations | DDD Operations       |
| ---------- | ----------------- | -------------------- |
| Episodes   | List, Details     | Track progress, Rate |
| Characters | View profile      | Follow, Comment      |
| Trivia     | View facts        | Submit new facts     |

#### 🔴 Complex Domains (Full DDD)

| Domain        | Why Full DDD?                       |
| ------------- | ----------------------------------- |
| Diary         | User ownership, business rules, RLS |
| Collections   | Ownership, validation, quotas       |
| User Progress | State management, history           |

```typescript
// app/_actions/diary.ts - Full DDD pattern
export async function createDiaryEntry(...) {
  return withAuthenticatedRLS(prisma, async (tx, user) => {
    const useCase = UseCaseFactory.createCreateDiaryEntryUseCase();
    await useCase.execute(input, user.id);
  });
}
```

### Decision Flowchart

```
New Feature → Is it read-only?
                   ↓ Yes: Use Simple Repository
                   ↓ No: Has business rules?
                            ↓ No: Simple Server Action + Zod
                            ↓ Yes: Full DDD with UseCase
                                    ↓ Requires auth?
                                        ↓ Yes: Add RLS wrapper
```

### Reference

See [docs/ARCHITECTURE_DECISION_MATRIX.md](../../../docs/ARCHITECTURE_DECISION_MATRIX.md) for the complete decision guide.

---

## When to Use This Skill

✅ **Primary Use Cases**

- "Refactor to DDD architecture"
- "Organize domains in Next.js"
- "Create domain-driven folders"
- "Design bounded context"
- "Separate business logic from framework"
- "Scale application architecture"

✅ **Secondary Use Cases**

- "Where should I put server actions?"
- "How to organize services and repositories?"
- "Design domain stores (Zustand/Jotai)"
- "Create domain-specific components"
- "Implement layered architecture"
- "Decouple framework from domain"

❌ **Do NOT use when**

- Simple UI components without business logic
- Quick prototypes or MVPs
- Single-feature applications
- Pure API routes without domain logic

---

## Architectural Principles

### 1. Domain-Driven Folders (Not Feature Folders)

Organize by **business domain**, not by technical concern.

```
❌ WRONG - Feature folders
app/
  users/
  products/
  orders/
components/
  UserCard.tsx
  ProductCard.tsx
services/
  userService.ts
  productService.ts

✅ CORRECT - Domain-driven folders
domains/
  users/
    components/
    services/
    actions/
    store/
    types.ts
    index.ts
  products/
    components/
    services/
    actions/
    store/
    types.ts
    index.ts
app/
  users/
    page.tsx  # delivery layer only
  products/
    page.tsx
```

### 2. Layered Architecture

#### Delivery Layer (`/app`)

- Next.js App Router routes, layouts, pages
- Server components for data fetching orchestration
- Minimal logic - just composition and orchestration
- Import from domains via public API (`index.ts`)

#### Domain Layer (`/domains`)

- Business logic, entities, value objects
- Services, repositories, stores
- Domain-specific components
- Validations (Zod schemas)
- Server actions within domain
- **Framework-agnostic** (can be ported to other frameworks)

#### Infrastructure Layer (`/app/_lib`)

- Database clients (Prisma, Drizzle)
- External API integrations
- Authentication utilities
- Shared infrastructure concerns

#### Shared Kernel (`/shared`)

- Truly cross-domain utilities
- UI primitives (`/components/ui`)
- Global types and constants
- **Keep minimal** - most code belongs in domains

---

## Domain Structure Template

### Canonical Domain Structure

```typescript
domains/
  {domain-name}/
    components/           # Domain-specific UI components
      DomainList.tsx
      DomainCard.tsx
      DomainForm.tsx
    services/             # Business logic & data fetching
      getDomain.ts
      createDomain.ts
      updateDomain.ts
    actions/              # Server actions (Next.js specific)
      createDomainAction.ts
      updateDomainAction.ts
    store/                # Client state management
      useDomainStore.ts   # Zustand/Jotai stores
    hooks/                # Domain-specific hooks
      useDomainLogic.ts
    types.ts              # Domain types & interfaces
    schemas.ts            # Zod validation schemas
    constants.ts          # Domain constants
    index.ts              # Public API exports
```

### Exports Strategy (`index.ts`)

```typescript
// domains/users/index.ts
// Public API - controlled exports only

// Services (server-side)
export { getUsers } from "./services/getUsers";
export { getUserById } from "./services/getUserById";

// Components (client + server)
export { UserList } from "./components/UserList";
export { UserCard } from "./components/UserCard";

// Actions (server actions)
export { createUserAction } from "./actions/createUserAction";
export { updateUserAction } from "./actions/updateUserAction";

// Types (shared)
export type { User, CreateUserInput, UpdateUserInput } from "./types";

// ❌ Do NOT export:
// - Internal helpers
// - Store internals (export hooks only)
// - Private utilities
```

---

## Server Actions Within Domain

### Pattern: Actions + Services Separation

```typescript
// domains/users/services/createUser.ts
"use server"; // Optional if called only from actions

import { prisma } from "@/app/_lib/prisma";
import { CreateUserSchema, type CreateUserInput } from "../schemas";

export async function createUser(input: CreateUserInput) {
  const validated = CreateUserSchema.parse(input);

  return await prisma.user.create({
    data: {
      name: validated.name,
      email: validated.email,
    },
  });
}

// domains/users/actions/createUserAction.ts
"use server";

import { revalidatePath } from "next/cache";
import { createUser } from "../services/createUser";
import type { CreateUserInput } from "../types";

export async function createUserAction(input: CreateUserInput) {
  const user = await createUser(input);
  revalidatePath("/users");
  return { success: true, user };
}

// app/users/page.tsx (delivery layer)
import { createUserAction, UserList, getUsers } from "@/domains/users";

export default async function UsersPage() {
  const users = await getUsers();
  return (
    <div>
      <UserList users={users} />
      <form action={createUserAction}>
        {/* form fields */}
      </form>
    </div>
  );
}
```

**Why this pattern?**

- **Services**: Pure business logic, reusable, testable
- **Actions**: Next.js-specific (revalidation, redirects, cookies)
- **Separation**: Services can be used in API routes, cron jobs, tests

---

## Domain Stores (Client State)

### Zustand Store Pattern

```typescript
// domains/users/store/useUsersStore.ts
"use client";

import { create } from "zustand";
import type { User } from "../types";

interface UsersState {
  selectedUser: User | null;
  filters: {
    search: string;
    status: "active" | "inactive" | "all";
  };
  setSelectedUser: (user: User | null) => void;
  setFilters: (filters: Partial<UsersState["filters"]>) => void;
  resetFilters: () => void;
}

export const useUsersStore = create<UsersState>((set) => ({
  selectedUser: null,
  filters: {
    search: "",
    status: "all",
  },
  setSelectedUser: (user) => set({ selectedUser: user }),
  setFilters: (filters) =>
    set((state) => ({ filters: { ...state.filters, ...filters } })),
  resetFilters: () =>
    set({ filters: { search: "", status: "all" } }),
}));

// domains/users/index.ts
export { useUsersStore } from "./store/useUsersStore";

// app/users/page.tsx
"use client";
import { useUsersStore } from "@/domains/users";

function UsersFilter() {
  const { filters, setFilters } = useUsersStore();
  return <input onChange={(e) => setFilters({ search: e.target.value })} />;
}
```

---

## Bounded Contexts & Domain Dependencies

### Rule: Domains Should Be Independent

```typescript
❌ WRONG - Direct domain imports
// domains/orders/services/createOrder.ts
import { getUserById } from "@/domains/users/services/getUserById"; // ❌ Tight coupling

✅ CORRECT - Dependency injection
// domains/orders/services/createOrder.ts
import type { User } from "@/domains/users";

export async function createOrder(
  userId: string,
  getUserFn: (id: string) => Promise<User> // Injected dependency
) {
  const user = await getUserFn(userId);
  // ... create order logic
}

// app/orders/actions.ts
import { createOrder } from "@/domains/orders";
import { getUserById } from "@/domains/users";

export async function createOrderAction(userId: string) {
  return createOrder(userId, getUserById); // Inject at boundary
}
```

### Shared Types Across Domains

```typescript
// domains/_shared/types.ts (or /shared/types.ts)
export interface PaginationParams {
  page: number;
  limit: number;
}

export interface ApiResponse<T> {
  data: T;
  meta: { total: number; page: number };
}

// domains/users/services/getUsers.ts
import type { PaginationParams } from "@/domains/_shared/types";

export async function getUsers(params: PaginationParams) {
  // ...
}
```

---

## Testing Strategy by Domain

### Unit Tests (Services)

```typescript
// domains/users/services/createUser.test.ts
import { describe, it, expect, vi } from "vitest";
import { createUser } from "./createUser";
import { prisma } from "@/app/_lib/prisma";

vi.mock("@/app/_lib/prisma", () => ({
  prisma: {
    user: {
      create: vi.fn(),
    },
  },
}));

describe("createUser", () => {
  it("creates user with valid input", async () => {
    const input = { name: "John", email: "john@example.com" };
    vi.mocked(prisma.user.create).mockResolvedValue({
      id: "1",
      ...input,
      createdAt: new Date(),
    });

    const result = await createUser(input);
    expect(result.name).toBe("John");
    expect(prisma.user.create).toHaveBeenCalledWith({
      data: input,
    });
  });
});
```

### Integration Tests (Actions)

```typescript
// domains/users/actions/createUserAction.test.ts
import { describe, it, expect } from "vitest";
import { createUserAction } from "./createUserAction";

describe("createUserAction", () => {
  it("creates user and revalidates path", async () => {
    const result = await createUserAction({
      name: "Jane",
      email: "jane@example.com",
    });

    expect(result.success).toBe(true);
    expect(result.user.name).toBe("Jane");
  });
});
```

---

## Migration Strategy: Existing Project → DDD

### Phase 1: Create Domain Structure

```bash
mkdir -p domains/users/{components,services,actions,store}
touch domains/users/index.ts
touch domains/users/types.ts
touch domains/users/schemas.ts
```

### Phase 2: Move Business Logic

```typescript
// Before: app/_lib/repositories.ts (mixed concerns)
export async function getUserById(id: string) {
  /* ... */
}
export async function getEpisodeById(id: number) {
  /* ... */
}

// After: Separate by domain
// domains/users/services/getUserById.ts
export async function getUserById(id: string) {
  /* ... */
}

// domains/episodes/services/getEpisodeById.ts
export async function getEpisodeById(id: number) {
  /* ... */
}
```

### Phase 3: Move Components

```typescript
// Before: app/_components/UserCard.tsx (generic)

// After: domains/users/components/UserCard.tsx (domain-specific)
// and update imports in app/users/page.tsx
import { UserCard } from "@/domains/users";
```

### Phase 4: Move Actions

```typescript
// Before: app/_actions/users.ts (all actions in one folder)

// After: domains/users/actions/createUserAction.ts
// domains/users/actions/updateUserAction.ts
```

### Phase 5: Update Imports

```typescript
// Before: app/users/page.tsx
import { getUserById } from "@/app/_lib/repositories";
import { UserCard } from "@/app/_components/UserCard";

// After: app/users/page.tsx
import { getUserById, UserCard } from "@/domains/users";
```

---

## Real-World Example: The Simpsons API

### Current Structure (Mixed)

```
app/
  _actions/
    episodes.ts
    diary.ts
    social.ts
  _components/
    EpisodeTracker.tsx
    CommentSection.tsx
  _lib/
    repositories.ts (mixed domain queries)
```

### Proposed DDD Structure

```
domains/
  episodes/
    components/
      EpisodeCard.tsx
      EpisodeTracker.tsx
      EpisodeList.tsx
    services/
      getEpisodes.ts
      getEpisodeById.ts
      trackEpisode.ts
    actions/
      trackEpisodeAction.ts
      rateEpisodeAction.ts
    store/
      useEpisodesStore.ts
    types.ts
    schemas.ts
    index.ts

  diary/
    components/
      DiaryForm.tsx
      DiaryEntryCard.tsx
    services/
      getDiaryEntries.ts
      createDiaryEntry.ts
    actions/
      createDiaryEntryAction.ts
      deleteDiaryEntryAction.ts
    types.ts
    schemas.ts
    index.ts

  social/
    components/
      CommentSection.tsx
      FollowButton.tsx
    services/
      getComments.ts
      followUser.ts
    actions/
      addCommentAction.ts
      toggleFollowAction.ts
    types.ts
    schemas.ts
    index.ts

app/
  episodes/
    page.tsx          # Delivery layer
    [id]/page.tsx
  diary/
    page.tsx
  _lib/
    prisma.ts         # Infrastructure
    auth.ts
```

---

## Decision Framework

### When to Create a New Domain?

✅ **Create separate domain when:**

- Clear bounded context (e.g., "users", "episodes", "payments")
- Independent business rules and validation
- Can be developed/tested in isolation
- Has its own data models and entities

❌ **Keep in existing domain when:**

- Tightly coupled to parent domain
- Shared lifecycle with parent
- Just a UI variant (use components folder)
- Pure utility function (use shared)

### When to Use Shared vs Domain?

**Shared:**

- UI primitives (Button, Card, Input)
- Framework utilities (cn, formatDate)
- Global constants (API_URL, MAX_RETRIES)

**Domain:**

- Business logic (calculateDiscount, validateOrder)
- Domain-specific components (UserCard, EpisodeTracker)
- Domain types and schemas

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Mixing Delivery and Domain

```typescript
// app/users/page.tsx
export default async function UsersPage() {
  // ❌ Business logic in route
  const users = await prisma.user.findMany({
    where: { isActive: true },
    orderBy: { createdAt: "desc" },
  });

  return <div>{users.map(/* ... */)}</div>;
}
```

✅ **Solution:** Extract to domain service

```typescript
// domains/users/services/getUsers.ts
export async function getActiveUsers() {
  return await prisma.user.findMany({
    where: { isActive: true },
    orderBy: { createdAt: "desc" },
  });
}

// app/users/page.tsx
import { getActiveUsers, UserList } from "@/domains/users";

export default async function UsersPage() {
  const users = await getActiveUsers();
  return <UserList users={users} />;
}
```

### ❌ Anti-Pattern 2: Domain Coupling

```typescript
// domains/orders/services/createOrder.ts
import { sendEmail } from "@/domains/notifications"; // ❌ Direct dependency
```

✅ **Solution:** Use events or dependency injection

```typescript
// domains/orders/services/createOrder.ts
import { EventBus } from "@/shared/events";

export async function createOrder(input: CreateOrderInput) {
  const order = await prisma.order.create({ data: input });

  // Emit event instead of direct call
  EventBus.emit("order.created", { orderId: order.id });

  return order;
}
```

### ❌ Anti-Pattern 3: Anemic Domain Model

```typescript
// domains/users/types.ts
export interface User {
  id: string;
  name: string;
  email: string;
}

// services/userService.ts (separate from domain)
export function isUserActive(user: User) {
  /* ... */
}
```

✅ **Solution:** Enrich domain with behavior

```typescript
// domains/users/types.ts
export class User {
  constructor(
    public id: string,
    public name: string,
    public email: string,
    public lastLoginAt: Date | null,
  ) {}

  isActive(): boolean {
    if (!this.lastLoginAt) return false;
    const daysSinceLogin =
      (Date.now() - this.lastLoginAt.getTime()) / (1000 * 60 * 60 * 24);
    return daysSinceLogin < 30;
  }
}
```

---

## Quick Reference

### Domain Checklist

- [ ] `components/` - Domain-specific UI components
- [ ] `services/` - Business logic and data fetching
- [ ] `actions/` - Server actions with revalidation
- [ ] `store/` - Client state (Zustand/Jotai)
- [ ] `types.ts` - Domain types and interfaces
- [ ] `schemas.ts` - Zod validation schemas
- [ ] `index.ts` - Public API exports

### File Naming Conventions

- **Services**: `{verb}{Entity}.ts` (e.g., `getUserById.ts`, `createUser.ts`)
- **Actions**: `{verb}{Entity}Action.ts` (e.g., `createUserAction.ts`)
- **Components**: `{Entity}{Component}.tsx` (e.g., `UserCard.tsx`, `UserList.tsx`)
- **Stores**: `use{Entity}Store.ts` (e.g., `useUsersStore.ts`)

### Import Patterns

```typescript
// ✅ Import from domain public API
import { getUsers, UserList, createUserAction } from "@/domains/users";

// ❌ Never import internals
import { UserList } from "@/domains/users/components/UserList"; // ❌
```

---

## Resources

- [Domain-Driven Design by Eric Evans](https://www.domainlanguage.com/ddd/)
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Modular Monolith Architecture](https://www.kamilgrzybek.com/design/modular-monolith-primer/)
