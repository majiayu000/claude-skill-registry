---
name: layer-frontend
description: Use when creating or modifying code in frontend/. Covers React components, hooks, API clients, and TypeScript code. All frontend changes require lint, typecheck, and build verification before completion.
---

# Frontend Layer

**Location:** `frontend/` (separate from Python backend)

**Stack:** React 19 · TypeScript · Vite · MUI

---

## Terminal Commands

Use `Push-Location`/`Pop-Location` to run npm commands without changing the working directory:

```powershell
Push-Location frontend; npm run lint; Pop-Location
Push-Location frontend; npm run build; Pop-Location
```

**Never use `cd frontend`** - it changes the terminal's working directory permanently.

---

## Required Verification

After ANY frontend change, run:

```powershell
Push-Location frontend; npm run lint; npm run build; Pop-Location
```

The `build` script runs `tsc -b` (type-check) then Vite build.

**Do not complete frontend work until both pass.**

---

## Structure

```
frontend/src/
├── main.tsx           # Entry point
├── App.tsx            # Root component
├── theme.ts           # MUI theme
├── components/        # Shared UI (layout, widgets)
├── features/          # Feature modules (auth, library, analytics, ...)
├── hooks/             # Custom React hooks
├── router/            # Route definitions
└── shared/            # API client, types, utilities
    ├── api.ts         # Typed backend client
    ├── types.ts       # TypeScript interfaces
    └── auth.ts        # Session utilities
```

---

## Rules

### TypeScript

- Strict mode - no `any`
- Explicit return types on exports
- Interface for object shapes, type for unions

### React

- Functional components only
- Feature-based folders (not type-based)
- Hooks for state management

### MUI

- Use MUI components, not raw HTML
- Use `sx` prop, not inline styles
- Reference theme tokens, don't hardcode colors

---

## API Client

All backend calls use `shared/api.ts`:

```typescript
import { api } from '../shared/api';

const stats = await api.library.getStats();
```

Adding endpoints:
1. Add interface to `shared/types.ts`
2. Add method to `shared/api.ts`

---

## Completion Checklist

1. ☐ `npm run lint` passes
2. ☐ `npm run build` passes
3. ☐ No `console.log` in committed code
4. ☐ No hardcoded URLs

---

## Layer Scripts

This skill includes validation scripts in `.github/skills/layer-frontend/scripts/`:

### `lint.py`

Runs ESLint and TypeScript type checking:

```powershell
python .github/skills/layer-frontend/scripts/lint.py
```

Runs `npm run lint` from the frontend directory.

### `build.py`

Runs the full build (typecheck + Vite):

```powershell
python .github/skills/layer-frontend/scripts/build.py
```

Runs `npm run build` from the frontend directory.
