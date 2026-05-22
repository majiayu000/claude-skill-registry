---
name: development-workflow
version: 1.0
last_updated: 2025-11-16
description: MECE development workflow with 5-phase todo template for API development, type safety, and code quality enforcement. Auto-loads for all development tasks.
license: MIT
triggers:
  - ALL development tasks (API, features, refactoring)
  - User mentions "개발", "API", "코드 작성", "구현"
  - Before starting implementation work
  - After requirements clarification
priority: highest
dependencies:
  - testing-checklist-SKILL.md: Phase 4 validation
  - git-workflow: Phase 5 commit
  - secure-coding-SKILL.md: Phase 4 security review
  - CLAUDE.md: Lines 429-455 (Code conventions)
compatibility:
  - claude-code: ">=1.0"
  - CLAUDE.md: ">=2.3"
changelog:
  - version: 1.0
    date: 2025-11-16
    changes:
      - Initial creation of development-workflow SKILL
      - MECE Phase 1-5 template for API development
      - Type safety enforcement (any 금지)
      - Integration with testing-checklist and git-workflow
---

# 🔄 Development Workflow SKILL

## Purpose

Provide MECE (Mutually Exclusive, Collectively Exhaustive) todo template for all development tasks. Ensures code quality, type safety, and comprehensive validation before commit.

---

## Auto-Trigger Conditions

**Activate when:**

1. **Development tasks:**
   - API development
   - New features
   - Refactoring
   - Bug fixes

2. **User mentions keywords:**
   - "개발", "API", "코드 작성"
   - "구현", "만들어줘"
   - "요구사항", "schema"

3. **Before implementation:**
   - After user clarifies requirements
   - Before writing first line of code
   - When starting new branch

---

## 📋 MECE Todo Template (5 Phases)

### Phase 1: Requirements Analysis

**Goal:** Clearly define what to build

- [ ] **Clarify User Story**
  - Who: User persona
  - What: Feature description
  - Why: Business value

- [ ] **Define Edge Cases**
  - Empty value handling (null, undefined, empty string)
  - Error scenarios (network failure, timeout)
  - Boundary values (min/max, 0, negative numbers)

- [ ] **Set Success Criteria**
  - How to verify functionality
  - Performance goals (response time, throughput)
  - Compatibility requirements (browsers, devices)

---

### Phase 2: Design

**Goal:** Design the structure for implementation

- [ ] **Schema Analysis**
  - Reference: `@docs/claude/test.guide.md` (test guide)
  - Verify database schema
  - Define API request/response formats
  - State management structure (Zustand, Redux)

- [ ] **Type Definitions (TypeScript strict mode)**
  - ❌ **NEVER use `any`** (Rule: Type safety is top priority)
  - ✅ **ALWAYS use:**
    - Utility types (Partial, Pick, Omit, Record)
    - Generic types (`<T>`, `<K extends keyof T>`)
    - Duck typing (structural typing)
    - Union types (`string | number`)
    - Discriminated unions (type guards)

  **Example:**
  ```typescript
  // ❌ BAD
  function process(data: any) { ... }

  // ✅ GOOD
  function process<T extends { id: string }>(data: T): Result<T> { ... }
  ```

- [ ] **API Interface Design**
  - Define REST endpoints (GET, POST, PUT, DELETE)
  - Request/Response types
  - Error handling structure
  - Validation rules

---

### Phase 3: Implementation

**Goal:** Convert design into code

- [ ] **Code Structuring (logically coherent)**
  - Single Responsibility Principle (SRP): One role per function
  - DRY: Eliminate duplicate code
  - Function length: Maximum 50 lines (reduce complexity)
  - Readability: Clear variable names, minimal comments (code explains itself)

  **Folder structure:**
  ```
  app/api/[endpoint]/
    route.ts           # API handler
    schema.ts          # Zod validation
    service.ts         # Business logic
    types.ts           # TypeScript types
  ```

- [ ] **Follow Conventions (CLAUDE.md Lines 429-455)**
  - PascalCase: Components, Types
  - camelCase: Functions, variables
  - UPPER_SNAKE_CASE: Constants
  - kebab-case: File names (URL slugs)
  - Tailwind: Utility-first CSS
  - Server-first: Next.js RSC pattern

- [ ] **Write E2E Tests (testing-checklist-SKILL.md)**
  - Reference: `@docs/claude/test.guide.md`
  - Happy path: Normal operation scenarios
  - Sad path: Error handling scenarios
  - Edge cases: Boundary values, empty values

  **E2E Test Template:**
  ```typescript
  // tests/e2e/api-endpoint.spec.ts
  test('should create item successfully', async ({ request }) => {
    const response = await request.post('/api/items', {
      data: { name: 'Test Item' }
    });
    expect(response.status()).toBe(201);
    const data = await response.json();
    expect(data).toHaveProperty('id');
  });

  test('should handle validation errors', async ({ request }) => {
    const response = await request.post('/api/items', {
      data: { name: '' } // Invalid: empty name
    });
    expect(response.status()).toBe(400);
  });
  ```

---

### Phase 4: Validation

**Goal:** Ensure code quality + performance

- [ ] **Run E2E Logic and Fix Errors**
  ```bash
  npx playwright test                    # Run all E2E tests
  npx playwright test --headed           # Visual debugging
  npx playwright test -g "API endpoint"  # Specific test
  ```

  **Pass criteria:**
  - All tests green ✅
  - Coverage: 80%+ for core logic
  - No flaky tests (remove unstable tests)

- [ ] **Check and Fix `any` Types**
  ```bash
  # Search for 'any' type usage
  grep -r "any" app/ components/ lib/ --include="*.ts" --include="*.tsx"

  # Or use ESLint rule
  # "@typescript-eslint/no-explicit-any": "error"
  ```

  **Fix methods:**
  ```typescript
  // Before: using any
  function handleData(data: any) { ... }

  // After 1: Generic type
  function handleData<T extends Record<string, unknown>>(data: T) { ... }

  // After 2: Union type
  function handleData(data: string | number | boolean) { ... }

  // After 3: Interface definition
  interface DataStructure { id: string; value: number; }
  function handleData(data: DataStructure) { ... }
  ```

- [ ] **Pessimistic Code Review (performance + quality)**

  **Checklist:**

  1. **Performance Optimization**
     - [ ] No N+1 queries (database)
     - [ ] No unnecessary re-renders (React)
     - [ ] Apply memoization (useMemo, useCallback)
     - [ ] Image optimization (Next.js Image)
     - [ ] Check bundle size (`npm run build` → .next/analyze)

  2. **Security (secure-coding-SKILL.md)**
     - [ ] Prevent XSS (sanitize inputs)
     - [ ] Prevent SQL Injection (Prepared statements)
     - [ ] CSRF token verification
     - [ ] No sensitive info logging (passwords, API keys)

  3. **Error Handling**
     - [ ] Try-catch implementation
     - [ ] User-friendly error messages
     - [ ] Structured logging (Sentry, Winston)
     - [ ] Fallback UI (error boundaries)

  4. **Accessibility (a11y)**
     - [ ] Semantic HTML (header, nav, main)
     - [ ] ARIA labels (button, input)
     - [ ] Keyboard navigation (Tab, Enter)
     - [ ] Color contrast (WCAG AA standard)

- [ ] **Run npm run lint**
  ```bash
  npm run lint        # ESLint + Prettier
  npm run type-check  # TypeScript errors
  ```

  **Pass criteria:**
  - 0 errors, 0 warnings
  - Auto-fix: `npm run lint -- --fix`

---

### Phase 5: Deployment Preparation

**Goal:** Prepare for production environment

- [ ] **Add Controller Exception Headers**
  ```typescript
  // app/api/[endpoint]/route.ts
  export async function POST(request: Request) {
    try {
      // ... business logic
    } catch (error) {
      console.error('[API Error]', error);
      return NextResponse.json(
        { error: 'Internal Server Error' },
        {
          status: 500,
          headers: {
            'X-Error-Type': error instanceof Error ? error.name : 'Unknown',
            'X-Request-ID': crypto.randomUUID(), // For debugging
          }
        }
      );
    }
  }
  ```

- [ ] **Pass Type-check**
  ```bash
  npm run type-check  # Must pass before commit
  ```

- [ ] **Build Verification (when modifying Protected Files)**
  ```bash
  npm run build       # Production build
  # Check: No errors, bundle size acceptable
  ```

  **Conditional Build (Rule 21):**
  - Simple (1-2 files): `type-check` only
  - Important (Protected/3+files/core): `type-check` + `build`

- [ ] **Commit (git-workflow)**
  - Reference: `.skills/git-workflow/commit-reminder-SKILL.md`
  - Format: `<Type>_<AI>_<Purpose>_<FileCount>-Files`
  - Pre-commit hook: automatic type-check
  - **NEVER auto-commit** (Rule 2)

---

## 🔗 Integration with Other SKILLs

### Workflow Integration

```
development-workflow (Phase 1-2)
   ↓
[User approves design]
   ↓
development-workflow (Phase 3: Implementation)
   ↓
testing-checklist-SKILL.md (E2E tests)
   ↓
development-workflow (Phase 4: Validation)
   ↓
secure-coding-SKILL.md (Security review)
   ↓
development-workflow (Phase 5: Deployment prep)
   ↓
git-workflow (Commit + Push)
```

### File Relationships

| Phase | Related SKILL | Purpose |
|-------|---------------|---------|
| Phase 1-2 | CLAUDE.md Project Overview | Context understanding |
| Phase 3 | testing-checklist-SKILL.md | E2E test writing |
| Phase 4 | secure-coding-SKILL.md | Security validation |
| Phase 4 | testing-checklist-SKILL.md | Test execution |
| Phase 5 | git-workflow | Commit protocol |

---

## 📊 Quality Metrics

### Phase Completion Criteria

| Phase | Metric | Target |
|-------|--------|--------|
| **Phase 1** | Requirements clarity | 100% (no ambiguity) |
| **Phase 2** | Type coverage | 100% (0 `any` types) |
| **Phase 3** | Convention compliance | 100% (ESLint pass) |
| **Phase 4** | Test coverage | 80%+ (core logic) |
| **Phase 5** | Build success | 100% (0 errors) |

### Code Quality Checklist

- [ ] Cyclomatic Complexity < 10 (per function)
- [ ] Function length < 50 lines
- [ ] File length < 300 lines (split if larger)
- [ ] No commented-out code
- [ ] No console.log in production code
- [ ] No hardcoded values (use constants/env vars)

---

## 💡 Best Practices

### Type Safety Patterns

**1. Utility Types**
```typescript
// Pick specific properties
type UserProfile = Pick<User, 'name' | 'email'>;

// Make all properties optional
type PartialUser = Partial<User>;

// Omit sensitive fields
type PublicUser = Omit<User, 'password' | 'apiKey'>;

// Create key-value map
type StatusMap = Record<string, boolean>;
```

**2. Generics**
```typescript
// Generic function
function findById<T extends { id: string }>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}

// Generic component
interface TableProps<T> {
  data: T[];
  columns: Array<keyof T>;
}
function Table<T>({ data, columns }: TableProps<T>) { ... }
```

**3. Type Guards**
```typescript
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function processValue(value: string | number) {
  if (isString(value)) {
    return value.toUpperCase(); // TypeScript knows value is string
  }
  return value.toFixed(2); // TypeScript knows value is number
}
```

### E2E Test Patterns

**1. API Testing**
```typescript
test.describe('POST /api/users', () => {
  test('should create user with valid data', async ({ request }) => {
    const response = await request.post('/api/users', {
      data: { name: 'John', email: 'john@example.com' }
    });
    expect(response.ok()).toBeTruthy();
    const user = await response.json();
    expect(user).toMatchObject({ name: 'John', email: 'john@example.com' });
  });

  test('should reject invalid email', async ({ request }) => {
    const response = await request.post('/api/users', {
      data: { name: 'John', email: 'invalid-email' }
    });
    expect(response.status()).toBe(400);
  });
});
```

**2. UI Interaction Testing**
```typescript
test('should complete form submission', async ({ page }) => {
  await page.goto('/register');

  // Fill form
  await page.fill('input[name="name"]', 'John Doe');
  await page.fill('input[name="email"]', 'john@example.com');

  // Submit
  await page.click('button[type="submit"]');

  // Verify success
  await expect(page.locator('.success-message')).toBeVisible();
  await expect(page).toHaveURL('/dashboard');
});
```

---

## ⚠️ Common Pitfalls

### 1. Skipping Phase 1 (Requirements)
**Problem:** Unclear requirements → Rework later
**Solution:** Always clarify edge cases upfront

### 2. Using `any` for convenience
**Problem:** Type safety lost → Runtime errors
**Solution:** Invest time in proper types (saves debugging time)

### 3. No E2E tests
**Problem:** Manual testing unreliable → Bugs in production
**Solution:** Write tests DURING implementation (not after)

### 4. Skipping code review
**Problem:** Performance/security issues missed
**Solution:** ALWAYS run Phase 4 checklist

### 5. Direct commit to main
**Problem:** No review, risky deployment
**Solution:** Use feature branches (Rule 20)

---

## 🎯 Example: Complete API Development Flow

### Scenario: Create "Add to Favorites" API

**Phase 1: Requirements**
```
User Story: As a user, I want to save jobs to favorites so I can review them later

Edge Cases:
- What if job already favorited? → Return 200 (idempotent)
- What if job doesn't exist? → Return 404
- What if user not authenticated? → Return 401

Success Criteria:
- API responds < 200ms
- Works on mobile + desktop
- Persists across sessions
```

**Phase 2: Design**
```typescript
// Schema (Zod)
const addFavoriteSchema = z.object({
  jobId: z.string().uuid(),
  userId: z.string().uuid(),
});

// Types
interface Favorite {
  id: string;
  userId: string;
  jobId: string;
  createdAt: Date;
}

// API Interface
POST /api/favorites
Request: { jobId: string }
Response: { favorite: Favorite }
Errors: 401, 404, 500
```

**Phase 3: Implementation**
```typescript
// app/api/favorites/route.ts
export async function POST(request: Request) {
  const session = await getServerSession();
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

  const body = await request.json();
  const { jobId } = addFavoriteSchema.parse(body);

  const favorite = await prisma.favorite.upsert({
    where: { userId_jobId: { userId: session.user.id, jobId } },
    create: { userId: session.user.id, jobId },
    update: {},
  });

  return NextResponse.json({ favorite }, { status: 200 });
}
```

**Phase 4: Validation**
```bash
# E2E tests
npx playwright test -g "Favorites API"
✓ should add favorite (201)
✓ should return existing favorite (200 idempotent)
✓ should reject unauthenticated (401)
✓ should reject invalid jobId (400)

# Type check
npm run type-check
✓ 0 errors

# Lint
npm run lint
✓ 0 errors, 0 warnings
```

**Phase 5: Deployment**
```bash
# Build
npm run build
✓ Build succeeded

# Commit
git add app/api/favorites/
git commit -m "feat: Add favorites API with idempotent upsert"
```

---

**Last Updated:** 2025-11-16
**Version:** 1.0
**Maintainer:** WHRESUME Team
