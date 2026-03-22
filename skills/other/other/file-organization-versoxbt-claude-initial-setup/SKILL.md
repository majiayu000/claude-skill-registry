---
name: file-organization
description: >
  Guide file and directory organization for maintainable codebases.
  Use when the user creates new files, asks where to put code, plans project structure,
  or when a file exceeds 400 lines. Apply when scaffolding new projects or refactoring
  large files into smaller modules.
---

# File Organization

Structure codebases with many small, focused files organized by feature or domain. Target 200-400 lines per file, with 800 as a hard maximum.

## When to Use

- Creating a new project or feature module
- A file exceeds 400 lines and needs splitting
- Deciding where to place new code
- Reviewing project structure for maintainability
- Setting up barrel exports or index files

## Core Patterns

### Feature-Based Organization (Preferred)

Group files by feature/domain, not by type. Each feature folder contains everything it needs:

```
src/
  auth/
    components/
      LoginForm.tsx
      SignupForm.tsx
    hooks/
      useAuth.ts
      useSession.ts
    services/
      auth.service.ts
      token.service.ts
    types.ts
    constants.ts
    index.ts              # barrel export

  users/
    components/
      UserProfile.tsx
      UserList.tsx
    hooks/
      useUser.ts
    services/
      user.service.ts
    types.ts
    index.ts

  shared/                 # Cross-cutting concerns only
    components/
      Button.tsx
      Modal.tsx
    hooks/
      useDebounce.ts
    utils/
      format.ts
      validation.ts
```

Compare with the type-based approach (avoid this):

```
# BAD: Type-based organization
src/
  components/             # 50+ files, mixed concerns
    LoginForm.tsx
    UserProfile.tsx
    Button.tsx
    OrderTable.tsx
  hooks/                  # Hard to find related code
    useAuth.ts
    useUser.ts
    useOrders.ts
  services/
    auth.service.ts
    user.service.ts
```

### File Size Guidelines

| Lines     | Action                                       |
|-----------|----------------------------------------------|
| < 100     | Fine, but check if the file is too granular  |
| 100-400   | Ideal range for most files                   |
| 400-600   | Consider splitting if multiple concerns      |
| 600-800   | Split into smaller modules                   |
| > 800     | Must refactor — file is too large            |

Extract when you see:
- Multiple classes or major type groups in one file
- Utility functions unrelated to the file's primary purpose
- Sections separated by comment banners (`// ===== Section =====`)
- More than 5 exported functions from a single file

```typescript
// BEFORE: 600-line user.service.ts
export class UserService {
  // ... 200 lines of CRUD operations
  // ... 150 lines of validation logic
  // ... 100 lines of email notifications
  // ... 150 lines of permission checks
}

// AFTER: Split by responsibility
// user.service.ts (~200 lines) — CRUD operations
// user.validation.ts (~150 lines) — Input validation
// user.notifications.ts (~100 lines) — Email logic
// user.permissions.ts (~150 lines) — Authorization
```

### Barrel Exports (index.ts)

Use barrel exports to simplify imports, but keep them thin:

```typescript
// src/auth/index.ts — barrel export
export { LoginForm } from "./components/LoginForm";
export { SignupForm } from "./components/SignupForm";
export { useAuth } from "./hooks/useAuth";
export { useSession } from "./hooks/useSession";
export { AuthService } from "./services/auth.service";
export type { User, Session, AuthConfig } from "./types";

// Consumer imports cleanly
import { LoginForm, useAuth } from "@/auth";
```

### Colocation Principle

Keep related files close together. Tests, styles, and stories live next to the code they describe:

```
src/auth/components/
  LoginForm.tsx
  LoginForm.test.tsx
  LoginForm.module.css
  LoginForm.stories.tsx

# NOT separated by type
__tests__/
  components/
    LoginForm.test.tsx    # Far from the component
styles/
  LoginForm.module.css    # Far from the component
```

### Backend Project Structure

```
src/
  modules/
    auth/
      auth.controller.ts
      auth.service.ts
      auth.repository.ts
      auth.routes.ts
      auth.middleware.ts
      auth.types.ts
      auth.test.ts
      index.ts

    users/
      users.controller.ts
      users.service.ts
      users.repository.ts
      users.routes.ts
      users.types.ts
      users.test.ts
      index.ts

  common/
    middleware/
      error-handler.ts
      rate-limiter.ts
    utils/
      logger.ts
      config.ts
    types/
      api.ts

  app.ts                  # App setup
  server.ts               # Server entry point
```

## Anti-Patterns

### What NOT to Do

- **God files**: A single `utils.ts` or `helpers.ts` that grows to 1000+ lines with unrelated functions. Split by domain.
- **Deeply nested barrels**: Barrel files re-exporting from other barrel files create circular dependencies and slow builds.
- **Empty wrapper files**: Do not create `index.ts` that just re-exports a single file. Only use barrels when a folder has 3+ exports.
- **Organizing by layer globally**: `controllers/`, `services/`, `models/` at the top level forces developers to jump between distant directories for a single feature.
- **Premature abstraction**: Do not create a `shared/` module for code used by only one feature. Move to shared only when genuinely used by 3+ features.

```
# BAD: God file
src/utils.ts              # 1200 lines, 40 exports

# GOOD: Split by purpose
src/shared/utils/
  format.ts               # Date, currency, string formatting
  validation.ts           # Input validation helpers
  math.ts                 # Numeric utilities
```

## Quick Reference

```
File Size Targets:
  Ideal:     200-400 lines
  Acceptable: 100-600 lines
  Refactor:  600-800 lines
  Must split: > 800 lines

Organization Priority:
  1. Feature-based (preferred)
  2. Domain-driven (for large apps)
  3. Type-based (only for very small projects)

Colocation Rules:
  - Tests next to source files
  - Styles next to components
  - Types in same feature folder
  - Move to shared/ only when used by 3+ features

Barrel Export Rules:
  - One index.ts per feature folder
  - Export only the public API
  - No barrel-of-barrels chains
  - Skip barrel for folders with < 3 exports

Split Signals:
  - Comment banners separating sections
  - Multiple unrelated export groups
  - Scrolling past 400 lines regularly
  - File name is too generic (utils, helpers, misc)
```
