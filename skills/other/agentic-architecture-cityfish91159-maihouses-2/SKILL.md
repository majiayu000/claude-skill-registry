---
name: agentic_architecture
description: Enforces high-level architectural thinking, separation of concerns, and scalability checks before coding.
allowed-tools: Read, Edit
---

# Agentic Architecture Protocol

## 1. Think Before You Code

Before implementing any feature that spans multiple files:

1.  **Analyze Data Flow**: Where does data come from? Where does it go?
2.  **Define Interfaces**: creating `types/*.ts` is often the best first step.
3.  **Check Boundaries**: Ensure API logic stays in `api/`, UI in `components/`, and business logic in `services/` or `hooks/`.

## 2. Scalability & Performance Checks

- **Database**:
  - Are we fetching 1000 items to filter 10? (Use DB filters instead).
  - Is RLS (Row Level Security) compatible with this query?
- **Frontend**:
  - Are we causing unnecessary re-renders? (Use `React.memo`, `useCallback` appropriately).
  - Is this component becoming a "God Component"? (Break it down).

## 3. The "Three-Tier" Rule

For any non-trivial feature, verify you have these three layers:

1.  **Data Layer**: Types + API/Service (e.g., `user.types.ts`, `userService.ts`)
2.  **State Layer**: Hook or Store (e.g., `useUser.ts`)
3.  **View Layer**: Components (e.g., `UserProfile.tsx`)

## 4. Architecture Checklist

- [ ] Have I defined the types first?
- [ ] Is the business logic separated from the UI?
- [ ] Did I consider how this scales to 10,000 users/items?
- [ ] Is the database schema validated (if changing DB)?
