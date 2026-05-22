---
name: frontend-core
description: Build React components, pages, forms, and state management with TypeScript and TanStack Query. Use for frontend development, component creation, routing, and data fetching.
---

# Frontend Core Skill

## When to Use

- Creating React components or pages
- Implementing forms with validation
- Setting up data fetching or state management
- Working with routing (/c, /o, /t)
- Working with files under `frontend/`

---

## CRITICAL: Irreversible Action Confirmation (MANDATORY)

### Redeem Flow

Customer screen shows "사용 처리" button → Trigger 2-step modal:

**Modal Content:**
- Title: "되돌릴 수 없는 작업입니다"
- Body: "매장 직원이 확인 후 눌러주세요"
- Buttons: [취소] (easy to hit) / [확인]

**TTL Enforcement:**
- If modal not confirmed within 30-60s → auto-expire
- Show "요청이 만료되었습니다" → retry CTA

**Why This Matters:**
- Prevents accidental customer-only redemption
- Forces store-side confirmation
- Abuse mitigation (no auto-click scripts)

---

## Stack

**Default (popular) stack:**
- React + TypeScript + Vite
- Tailwind CSS
- React Router
- TanStack Query
- Axios
- React Hook Form + Zod

### Libraries Policy
- Use the existing stack first
- Adding a new library requires:
  - clear benefit
  - small footprint
  - at least one example usage

---

## Architecture

### User Types & Viewports
- **Customer Wallet:** mobile-first
- **Owner Backoffice:** desktop-first
- **Store Terminal:** always-on approval screen

### Component Composition Pattern
```
Page (route-level)
  └─ Container (data fetch + state)
       └─ View (presentational)
```

### File Organization
- `src/components/` - Common UI elements
- `src/features/<feature>/components/` - Feature-specific UI

---

## Code Style

**Base:** Airbnb JavaScript Style Guide, with these overrides:
- Indentation: 4 spaces
- Max line length: 120 characters
- Semicolons: false

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components/Files | PascalCase | `UserProfile.tsx` |
| Variables/Functions/Hooks | camelCase | `const isOpen = useState()` |
| Constants | SCREAMING_SNAKE_CASE | `const MAX_RETRY_COUNT = 3` |

**No Abbreviations:**
```typescript
// bad
const idx = 0

// good
const index = 0
```

**Boolean Naming:**
- Use prefixes: `is`, `has`, `can`, `should`
- Event handlers: `handle*` for functions, `on*` for props

```tsx
// good
const handleOpen = () => {}
<Button onClick={handleOpen} />
```

### Component Internal Order
1. State declarations (`useState`)
2. Memoization (`useMemo`, `useCallback`)
3. Side effects (`useEffect`)
4. Event handlers
5. JSX Rendering

### TypeScript Rules
- **Never** use `any` (use `unknown` if uncertain)
- `interface` for objects (Props, API responses)
- `type` for unions/aliases
- Use `as const` instead of enums:

```typescript
const ROLES = {
  ADMIN: "ADMIN",
  USER: "USER",
} as const

type Role = (typeof ROLES)[keyof typeof ROLES]
```

### Prettier Config
```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 4,
  "trailingComma": "es5",
  "printWidth": 120,
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

---

## State Branching (REQUIRED)

Every page **MUST** handle:
- **Loading** state
- **Empty** state
- **Error** state (with retry CTA)

### Error Handling
- Show user-friendly message
- Provide a recovery action (retry / back)

---

## State & Data Fetching

### TanStack Query Patterns
- `useQuery` for reads
- `useMutation` for writes
- Invalidate queries on mutation success

### Polling (MVP REQUIRED)

Issuance approval status and terminal lists must support polling:
- **Default interval:** 2-3 seconds
- **Stop when:** status is final OR TTL expires

---

## Routing & Navigation

Use React Router.

### Route Grouping
- `/c/*` - customer
- `/o/*` - owner/backoffice
- `/t/*` - store terminal

### Navigation Rules
- Keep route params explicit (e.g., `storeId`, `stampCardId`)
- Avoid deep nesting unless it improves clarity

---

## Forms & Validation

- Use `react-hook-form` for forms
- Use `zod` schemas for validation

### UX Requirements
- Display field errors near the field
- Disable submit while loading
- Prevent double submits

---

## Import Rules

### Use Absolute Paths
Use `@/` prefix for major directories (`components/`, `hooks/`, etc.)

### Import Sorting Order
1. React core libraries
2. Third-party libraries
3. Global/Common components
4. Domain-specific components
5. Hooks, Utils, Types
6. Assets (images, css)

---

## Control Flow & Depth

- **Braces Required:** Do not omit `{}` even for single-line `if`
- **Depth Limit:** Maintain depth of 1 or less (max 2)
- Actively use **early returns**

---

## Linting & Formatting

**Tools:**
- **ESLint:** Code quality, accessibility (a11y), import sorting
- **Prettier:** Code formatting and Tailwind class sorting
- **Husky & lint-staged:** Automated verification before `git commit`

---

## PR Checklist

- [ ] Loading/Empty/Error states exist
- [ ] Keyboard navigation works
- [ ] Mobile-first layout checked
- [ ] No unnecessary re-renders / infinite loops
- [ ] API errors are handled
