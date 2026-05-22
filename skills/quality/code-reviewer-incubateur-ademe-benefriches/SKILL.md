---
name: code-reviewer
description: Reviews code for bugs, security vulnerabilities, and quality issues. MUST be invoked automatically after completing a coding task (feature, bug fix, or refactor) - do not wait for user to request it.
user-invocable: true
---

# Code Review

Review recent code changes for quality, security, maintainability, and adherence to project patterns.

## Instructions

### 1. Get Recent Changes

Run `git diff` to see uncommitted changes. If no uncommitted changes, run `git diff HEAD~1` to review the last commit.

Focus on modified files and analyze them thoroughly.

### 2. Review Checklist

Apply this checklist to all changed code:

#### Security (CRITICAL)

- Hardcoded credentials (API keys, passwords, tokens)
- SQL injection risks (string concatenation in queries - should use Knex parameterized queries)
- XSS vulnerabilities (unescaped user input in responses)
- Missing input validation (DTOs should use Zod schemas)
- Authentication bypasses (missing `@UseGuards(JwtAuthGuard)`)
- Path traversal risks (user-controlled file paths)
- CSRF vulnerabilities
- Insecure dependencies (outdated, vulnerable)

#### Clean Architecture (CRITICAL)

**Clean Architecture - API** (API only):

**Dependency Rule Violations**:
- ❌ `core/` MUST NEVER import from `adapters/` - Check all imports in core files
- ❌ UseCases depending on concrete implementations (e.g., `SqlRepository`) instead of interfaces
- ❌ Domain models importing infrastructure code
- ✅ Core should only import from `core/`, `shared-kernel/`, or `"shared"` package

**Layer Violations**:
- Controllers containing business logic (should only handle HTTP → UseCase → HTTP)
- Business logic in repositories/queries (should be in UseCases)
- Direct database access in controllers (should go through UseCases)

**Clean Architecture - Web** (Web only):

**Dependency Rule Violations**:
- ❌ `core/` importing from `infrastructure/` or `views/` directories
- ❌ Presentational components with business logic
- ✅ Core should only import from `core/` or `"shared"` package

Example violation:
```typescript
// BAD - core importing from infrastructure
// File: src/features/create-site/core/createSite.reducer.ts
import { HttpSiteService } from "../../infrastructure/site-service/HttpSiteService";

// GOOD - core depending on interface only
// File: src/features/create-site/core/createSite.reducer.ts
import type { SiteService } from "./gateways/SiteService";
```

#### Redux Architecture (CRITICAL - Web only)

**ESTABLISHED Pattern**:
- ❌ Refactoring Redux to other state management (Zustand, Jotai, MobX)
- ❌ Using `createSlice` for new code (legacy - maintenance only)
- ❌ Actions using imperative tense (`completeStep`, `fetchData`)
- ✅ Use event-based Redux with `createReducer`
- ✅ Actions in passive tense (`stepCompleted`, `dataFetched`)

Example violations:
```typescript
// BAD - createSlice in new code
export const newFeatureSlice = createSlice({
  name: 'newFeature',
  initialState,
  reducers: { /* ... */ }
});

// GOOD - createReducer for new code
export const newFeatureReducer = createReducer(initialState, (builder) => {
  builder.addCase(featureDataFetched, (state, action) => { /* ... */ });
});

// BAD - imperative action names
export const fetchSiteData = createAction("site/fetch");
export const completeSiteCreation = createAction("site/complete");

// GOOD - passive/event-based action names
export const siteDataFetched = createAction("site/dataFetched");
export const siteCreationCompleted = createAction("site/creationCompleted");
```

#### UseCase Pattern (CRITICAL - API only)

**Result Pattern**:
- ❌ UseCases not implementing `UseCase<Request, TResult<Response, Error>>`
- ❌ UseCases not returning `TResult<Data, Error>`
- ❌ Using `throw` for domain errors instead of `fail("ErrorType")`
- ❌ Error types that are action-based ("CreateFailed") instead of state-based ("AlreadyExists", "NotFound")
- ✅ All UseCases should use `success(data)` or `fail("ErrorType")`

**Dependency Injection**:
- ❌ UseCases depending on concrete classes (e.g., `SqlSiteRepository`) instead of interfaces
- ❌ Missing gateway interfaces in `core/gateways/`
- ✅ Constructor parameters should be typed as interfaces, not concrete classes

#### Controller Pattern (CRITICAL - API only)

**DTOs**:
- ❌ DTOs defined in controller files (should be in `/packages/shared/src/api-dtos/`)
- ❌ Missing Zod schema validation with `ZodValidationPipe`
- ❌ Business logic validation in DTOs (should be in UseCases)
- ✅ All request/response DTOs should be in shared package with both schema + type export

**Authentication**:
- ❌ Routes missing `@UseGuards(JwtAuthGuard)` (unless explicitly public)
- ❌ Unprotected routes without clear justification

**Result Mapping**:
- ❌ Not handling Result errors (missing `if (result.isFailure())` check)
- ❌ Inconsistent HTTP status mapping (e.g., `*NotFound` should throw `NotFoundException`)
- ❌ Returning domain entities instead of ViewModels

#### Container/Presentational Pattern (HIGH - Web only)

**ViewData Pattern**:
- ❌ Multiple `useAppSelector` calls in container
- ❌ Selectors not following `select{Feature}ViewData` naming
- ❌ Presentational components using Redux hooks
- ✅ Single ViewData selector per container
- ✅ Presentational components receive all data via props

Example violations:
```typescript
// BAD - multiple selectors in container
const Container = () => {
  const sites = useAppSelector(selectSites);
  const loading = useAppSelector(selectLoading);
  const error = useAppSelector(selectError);
  // ...
};

// GOOD - single ViewData selector
const Container = () => {
  const viewData = useAppSelector(selectSitesViewData);
  return <SitesPage viewData={viewData} />;
};

// BAD - presentational component with Redux
const SitesPage = () => {
  const sites = useAppSelector(selectSites); // ❌ NO REDUX IN PRESENTATIONAL
  return <div>{sites.map(...)}</div>;
};

// GOOD - presentational component with props only
const SitesPage = ({ viewData }: { viewData: SitesViewData }) => {
  return <div>{viewData.sites.map(...)}</div>;
};
```

#### Redux Hooks (HIGH - Web only)

- ❌ Using untyped `useSelector` or `useDispatch` from react-redux
- ✅ Always use `useAppSelector` and `useAppDispatch` from `@/shared/views/hooks/store.hooks`

Example violation:
```typescript
// BAD - untyped hooks
import { useSelector, useDispatch } from 'react-redux';
const data = useSelector(state => state.feature); // No type safety
const dispatch = useDispatch();

// GOOD - typed hooks
import { useAppSelector, useAppDispatch } from '@/shared/views/hooks/store.hooks';
const data = useAppSelector(selectFeatureData); // Fully typed
const dispatch = useAppDispatch();
```

#### CQS (Command-Query Separation) (HIGH - API only)

**Repository vs Query**:
- ❌ Repository interfaces mixing reads and writes
- ❌ Query interfaces with write methods
- ❌ Write UseCases using Query interfaces for data modification
- ✅ Write operations should use Repository, read-only operations should use Query

#### Database Patterns (CRITICAL - API only)

**Migrations**:
- ❌ Direct database schema changes without migration
- ❌ Missing `down()` function in migrations
- ❌ Missing indexes on foreign keys or frequently queried columns

**Table Types**:
- ❌ New tables without corresponding `Sql*` type in `tableTypes.d.ts`
- ❌ Using `any` type for SQL operations
- ❌ Optional properties (`?:`) instead of nullable (`| null`) in table types
- ❌ Using `string` for timestamp columns (should be `Date` - Knex auto-converts)
- ✅ All SQL table types should use `snake_case` column names

**Naming Convention**:
- ❌ Database columns using `camelCase` (should be `snake_case`)
- ❌ Application properties using `snake_case` (should be `camelCase`)
- ✅ Repository code should map between `snake_case` (DB) and `camelCase` (app)

**Transactions**:
- ❌ Multi-table operations without transactions
- ✅ Operations spanning multiple tables should use `sqlConnection.transaction()`

#### Testing Pattern (CRITICAL)

**Testing - API** (API only):

**InMemory Implementations**:
- ❌ New Repository/Query interfaces without InMemory implementation
- ❌ Missing test helper methods (prefixed with `_`) in InMemory classes
- ❌ Unit tests accessing real database (should use InMemory)

**Unit Tests**:
- ❌ UseCase instantiation in `beforeEach()` (should be in each `it()`)
- ❌ Using `toMatchObject()` when `toEqual()` is appropriate (less exhaustive)
- ❌ Missing failure path tests (only testing happy path)
- ❌ Not verifying side effects (e.g., data saved, not saved on failure)
- ❌ Using real services (random IDs, current dates) instead of deterministic ones

**Event Testing**:
- ❌ Success paths not asserting published events
- ❌ Error paths not asserting NO events published
- ❌ Event assertions without complete type (should use `expect().toEqual<EventType>(...)`)
- ✅ Use `InMemoryEventPublisher` and assert `eventPublisher.events` length and content

**Integration Tests**:
- ❌ SQL Repository/Query without integration test file (`*.integration-spec.ts`)
- ❌ Controller without integration test
- ✅ Integration tests should test against real database (testcontainers)

**Testing - Web** (Web only):

- ❌ Unit tests using HTTP services (should use InMemory)
- ❌ Not using builder pattern for test state
- ❌ Hardcoded test data instead of builders
- ✅ Use `StoreBuilder` pattern for test setup
- ✅ InMemory services for all external dependencies

Reference: `src/features/create-project/core/urban-project/__tests__/_testStoreHelpers.ts`

Example violation:
```typescript
// BAD - hardcoded test state
it("should display sites", () => {
  const store = configureStore({
    preloadedState: {
      sites: {
        list: [{ id: "1", name: "Site 1" }],
        loading: false
      }
    }
  });
  // ...
});

// GOOD - builder pattern
it("should display sites", () => {
  const store = new StoreBuilder()
    .withSiteData({ id: "1", name: "Site 1" })
    .build();
  // ...
});
```

#### Dependency Injection (HIGH - API only)

**NestJS Modules**:
- ❌ Not using factory pattern (`useFactory`) for providers
- ❌ Missing `inject` array in factory providers
- ❌ Not importing required modules (SqlConnectionModule, EventPublisherModule)
- ❌ Using injection tokens for UseCases (should use direct injection of `RealEventPublisher`)
- ✅ UseCases should inject `RealEventPublisher` directly, not via token

#### Gateway Pattern (HIGH)

**Gateway Pattern - API** (API only):

See Controller Pattern section for API gateway checks.

**Gateway Pattern - Web** (Web only):

- ❌ HTTP services without InMemory mock implementation
- ❌ HTTP services not validating DTOs with Zod `safeParse()`
- ❌ Services not registered in store's `extraArgument`
- ❌ Thunks not accessing services via `extra` parameter
- ✅ HTTP implementation + InMemory mock required
- ✅ Validate request/response with shared Zod schemas

Reference: `src/features/onboarding/infrastructure/create-user-service/HttpCreateUserService.ts`

Example violation:
```typescript
// BAD - no DTO validation
async createUser(data: CreateUserDto) {
  const response = await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify(data) // ❌ No validation
  });
  return response.json(); // ❌ No validation
}

// GOOD - Zod validation
import { createUserDtoSchema, createUserResponseSchema } from "shared";

async createUser(data: CreateUserDto) {
  const validated = createUserDtoSchema.safeParse(data);
  if (!validated.success) throw new Error("Invalid request");

  const response = await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify(validated.data)
  });

  const json = await response.json();
  const result = createUserResponseSchema.safeParse(json);
  if (!result.success) throw new Error("Invalid response");
  return result.data;
}
```

#### Naming Conventions (HIGH)

**Naming Conventions - API** (API only):

**File Naming**:
- ❌ UseCase files not following `[verb][Noun].usecase.ts` pattern
- ❌ Repository files not following `Sql[Name]Repository.ts` pattern
- ❌ Query files not following `Sql[Name]Query.ts` pattern
- ❌ Test files not matching source file name with `.spec.ts` or `.integration-spec.ts`

**Import Aliases**:
- ❌ Using relative imports (`../../../`) for cross-module (should use `@/`)
- ❌ Using `@/` for shared package (should use `"shared"`)
- ❌ Long import chains when path alias would be clearer

**Naming Conventions - Web** (Web only):

**Actions**:
- ❌ Actions using imperative tense (`completeStep`, `fetchData`)
- ✅ Actions in passive tense (`stepCompleted`, `dataFetched`)

**Selectors**:
- ❌ Selectors not following `select{Feature}ViewData` pattern
- ✅ One ViewData selector per container component

**Reducers**:
- ❌ Using `createSlice` in new code (legacy - maintenance only)
- ✅ Use `createReducer` for new reducers

**Import Aliases**:
- ❌ Using relative imports (`../../../`) for cross-feature imports (should use `@/`)
- ❌ Using `@/` for shared package (should use `"shared"`)
- ✅ Use `@/` for imports within web app
- ✅ Use `"shared"` for shared package imports
- ✅ Use relative `./` or `../` only within same feature folder

Example violations:
```typescript
// BAD - relative import for cross-feature
import { selectUserData } from "../../../user/core/user.selectors";

// GOOD - use @/ alias
import { selectUserData } from "@/features/user/core/user.selectors";

// BAD - using @/ for shared package
import type { Site } from "@/shared";

// GOOD - use "shared" for package imports
import type { Site } from "shared";
```

#### TypeScript & Node.js Compatibility (CRITICAL)

**Erasable Types**:
- ❌ TypeScript `enum` usage (use Zod `z.enum()` or const object instead)
- ❌ Namespace declarations
- ⚠️ Class parameter properties in new code (legacy allowed, but avoid in new code)
- ✅ Use `type` over `interface` unless extending
- ✅ Use Zod schemas for enum-like types

**Type Safety**:
- ❌ Using `any` type (use `unknown` when type is truly unknown)
- ❌ Missing explicit return types on public functions/methods
- ❌ Not using `import type { }` for type-only imports
- ✅ `strict: true` compliance

#### Code Quality (HIGH)

**Function/File Size**:
- Large functions (>50 lines) - consider breaking down
- Large files (>800 lines) - consider splitting by responsibility
- Deep nesting (>4 levels) - refactor for readability

**Error Handling**:
- Missing error handling in async operations
- `console.log` statements left in production code (use proper logging)
- Swallowing errors without logging

**State Management**:
- Mutation of shared state
- Missing immutability in domain models

#### Performance (MEDIUM)

- Inefficient algorithms (O(n²) when O(n log n) possible)
- N+1 query patterns (should use joins or batch queries)
- Missing database indexes on frequently queried columns
- Unnecessary re-renders in React
- Missing memoization opportunities in React
- Large bundle size additions

#### Best Practices (MEDIUM)

- TODO/FIXME without tickets or context
- Missing JSDoc for complex public APIs
- Poor variable naming (x, tmp, data, result without context)
- Magic numbers without explanation
- Inconsistent formatting (should run `pnpm format`)

### 3. Confidence-Based Filtering

**Only report issues you are highly confident about**:

- ✅ **HIGH Confidence** - Clear violations visible in the diff:
  - Missing `@UseGuards(JwtAuthGuard)` on route
  - `core/` importing from `adapters/`
  - UseCase not returning `TResult<>`
  - TypeScript `enum` usage
  - Missing table type after migration

- ⚠️ **MEDIUM Confidence** - Probable but needs context:
  - Report with caveat: "Possible issue (verify context)..."
  - Large functions/files (may be justified)
  - Missing tests (may exist elsewhere)

- ❌ **LOW Confidence** - Skip reporting:
  - Require deep codebase knowledge
  - May have valid reasons not visible in diff
  - Speculative or style-only concerns

**When in doubt, skip the issue** - focus on clear, actionable problems.

### 4. Output Format

For each issue found, use this format:

```
[SEVERITY] Issue Title
File: path/to/file.ts:line
Issue: Description of the problem
Fix: How to resolve it

// Bad
<code snippet showing the problem>

// Good
<code snippet showing the fix>
```

**Severity Levels**:
- **CRITICAL**: Security, architecture violations, type safety issues
- **HIGH**: Missing tests, pattern violations, significant bugs
- **MEDIUM**: Performance, maintainability, code quality
- **LOW**: Style, minor improvements

### 5. Summary

End with a summary:

```
## Review Summary

- Critical: X issues
- High: X issues
- Medium: X issues
- Low: X issues

## Verdict

- ✅ APPROVE: No Critical or High issues
- ⚠️ CAUTION: Medium issues only (can proceed with awareness)
- ❌ BLOCK: Critical or High issues must be fixed
```

## Scope

$ARGUMENTS

If no scope provided, review all uncommitted changes.

## Important Notes

- Focus on **high-confidence** issues only - don't report speculative concerns
- Prioritize **architecture violations**:
  - **API**: Clean Architecture, Result pattern, CQS
  - **Web**: Clean Architecture, Redux patterns, Container/Presentational separation
- Check **security** (authentication, SQL injection, input validation)
- Verify **testing**:
  - **API**: InMemory implementations, unit + integration tests
  - **Web**: Builder pattern, InMemory services
- Validate **naming**:
  - **API**: Files, database columns, imports
  - **Web**: Actions (passive tense), selectors (ViewData), imports
- Ensure **type safety** (no enums, no `any`, proper Result usage for API)
- Check **established patterns**:
  - **Web**: Redux is ESTABLISHED - no refactoring to Zustand/Jotai/MobX
  - **Web**: Use `createReducer` for new code, not `createSlice`
- Be concise but actionable - provide clear fixes with code examples
