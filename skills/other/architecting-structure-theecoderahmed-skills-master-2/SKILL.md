---
name: architecting-structure
description: Enforces "Feature-First" architecture across standard frameworks. Use to scaffold new projects, refactor messy ones, or enforce clean file organization rules.
---

# Code Structure Architect

## When to use this skill
- When the user asks to "set up the folders" for a new project.
- When the user asks to "clean up" or "refactor" a messy directory.
- When the user asks "where should I put this file?".
- When starting any new Next.js, Flutter, Python, or standard web project.

## Core Philosophy: Feature-First
We strictly follow **Feature-First Architecture (Vertical Slicing)**. Code that changes together stays together.
*   **Bad (Type-First)**: `/components`, `/hooks`, `/services` (Separates logic by file type).
*   **Good (Feature-First)**: `/features/auth`, `/features/dashboard` (Groups explicitly by user value).

## Workflow

### 1. Scaffolding (New Project)
1.  **Identify Framework**: Detect if it's Next.js, Flutter, Python, etc.
2.  **Apply Template**: Use the specific directory map below.
3.  **Create Core**: Generate `core/` (shared logic) and `features/` (business logic) folders immediately.

### 2. Refactoring (Cleanup)
1.  **Audit**: List all files.
2.  **Group**: Identify "features" (e.g., "Login", "Profile", "Feed").
3.  **Move**:
    - Move generic UI (buttons, cards) -> `components/ui/`.
    - Move shared utilities (dates, formatting) -> `utils/`.
    - Move feature logic -> `features/<feature-name>/`.
4.  **Export**: Create barrel files (`index.ts` / `barrier.dart`) only for the public API of a feature.

### 3. Enforcement (Check)
1.  **Review**: Check if a new file is being created in the root or a 'dump' folder.
2.  **Block**: "Stop. This belongs in `features/<name>`. Do not put logic in `pages/`."

## Framework Standards

### A. Next.js (App Router)
*   `app/`: Routing layer **ONLY**. (page.tsx, layout.tsx, route.ts). NO LOGIC.
    *   `app/(auth)/login/page.tsx` -> Imports from `@/features/auth`
*   `features/`: The brain.
    *   `features/auth/components/LoginForm.tsx`
    *   `features/auth/hooks/useLogin.ts`
    *   `features/auth/actions/login.ts` (Server Actions)
*   `components/`: Shared dumb UI.
    *   `components/ui/button.tsx` (Shadcn)
    *   `components/layout/header.tsx`
*   `lib/`: Singletons (Prisma, Stripe, Redis clients).

### B. Flutter (Clean + Riverpod)
*   `lib/main.dart`: Entry point.
*   `lib/core/`: Routing, Themes, Constants, Extensions.
*   `lib/features/`:
    *   `features/auth/presentation/screens/`
    *   `features/auth/presentation/widgets/`
    *   `features/auth/data/repositories/`
    *   `features/auth/domain/models/`
*   `lib/shared/`: Widgets used across multiple features.

### C. Python (FastAPI / General)
*   `app/main.py`: App init.
*   `app/core/`: Config, Security, DB session.
*   `app/routers/`: V1 endpoints.
*   `app/internal/`: Admin routes.
*   `app/services/` (Optional): If logic is heavy.
*   *Note*: Python often prefers flat structures initially. Group by "Domain" (e.g., `app/users/`, `app/items/`) if the app grows.

## Best Practices (Recommended)
1.  **Filenames**:
    - **JS/TS**: `camelCase` for variables/functions, `PascalCase` for Components/Classes, `kebab-case` for folders/routes.
    - **Dart**: always `snake_case` for filenames.
    - **Python**: always `snake_case`.
2.  **Barrel Files**: Avoid them for internal usage (causes circular deps). Use them ONLY to expose a Feature's public API to the rest of the app:
    - *Right*: `import { LoginForm } from '@/features/auth'` (where `features/auth/index.ts` exists).
    - *Wrong*: `import { Button } from '@/components'` (import directly: `@/components/Button`).

## Self-Correction Checklist
Before creating a file, ask:
1.  "Is this file specific to one feature (e.g., 'Delete Task Button')?" -> Put in `features/tasks/components`.
2.  "Is this file generic (e.g., 'Red Delete Button')?" -> Put in `components/ui`.
3.  "Is this file a page?" -> Put in `app/` (Next.js) or `screens/` (Flutter), but keep it empty (logic goes to feature).
