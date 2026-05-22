---
name: sonarqube-best-practices
description: SonarLint best practices for Next.js 16 applications. Covers pre-merge quality checks, issue severity prioritization, common fixes for TypeScript/Next.js, and when to defer minor issues. Use when performing code quality analysis, fixing SonarLint warnings, or setting up quality gates.
---

# SonarLint Best Practices for Next.js 16

Best practices for using SonarLint to maintain code quality in The Simpsons API (Next.js 16 + TypeScript).

## When to Use This Skill

Use this skill when:

- Creating a new PR and need pre-merge quality check
- Fixing code quality issues flagged by SonarLint
- Setting up quality gates for CI/CD
- Understanding which SonarLint issues to fix vs defer

## Pre-Merge SonarLint Workflow

### 1. Analyze Modified Files

```bash
# Get all TypeScript files modified in PR
git diff --name-only main...your-branch | grep -E "\.(ts|tsx)$"

# Analyze each file (use VS Code SonarLint extension)
# Or use available tools in your environment
```

### 2. Categorize Issues by Severity

| Severity    | Action         | Timeline           |
| ----------- | -------------- | ------------------ |
| 🔴 BLOCKER  | **Must fix**   | Before merge       |
| 🟠 CRITICAL | **Must fix**   | Before merge       |
| 🟡 MAJOR    | **Should fix** | Before merge       |
| 🔵 MINOR    | **Can defer**  | With justification |
| ⚪ INFO     | **Optional**   | Per team standards |

### 3. Common Issues and Fixes

#### Issue: "Replace Error with TypeError"

**When:** Type validation errors
**Fix:**

```typescript
// ❌ Before
if (typeof input !== "number") {
  throw new Error("Expected number");
}

// ✅ After
if (typeof input !== "number") {
  throw new TypeError("Expected number, got " + typeof input);
}
```

**Exception:** Domain validation should use domain exceptions

```typescript
// ✅ Correct for business rules
if (rating < 1 || rating > 5) {
  throw new ValidationException("Rating must be 1-5");
}
```

#### Issue: "Avoid using 'any' type"

**Production Code:**

```typescript
// ❌ Wrong
function process(data: any): any {
  return data;
}

// ✅ Correct - Use generics
function process<T>(data: T): T {
  return data;
}

// ✅ Correct - Use unknown when type is truly unknown
function process(data: unknown): ProcessedData {
  if (typeof data !== "object") {
    throw new TypeError("Expected object");
  }
  // ... narrow type and process
}
```

**Test Mocks:**

```typescript
// ✅ Acceptable with comment
// @ts-expect-error - Test mock intentionally incomplete for flexibility
const mockRepo: any = { findById: vi.fn() };

// ✅ Better - Use Partial<T>
const mockRepo: Partial<EpisodeRepository> = {
  findById: vi.fn().mockResolvedValue(mockEpisode),
};
```

#### Issue: "Preserve Exception Types"

**Critical Pattern from PR #14:**

```typescript
// ❌ Wrong - Loses type information
catch (error) {
  if (error instanceof ValidationException) {
    throw new Error(error.message); // Lost field, code, metadata
  }
}

// ✅ Correct - Preserves exception type
catch (error) {
  if (error instanceof ValidationException || error instanceof DomainException) {
    throw error; // Full type info preserved for client
  }
  if (error instanceof Error) {
    throw error; // Preserve stack trace
  }
  throw new Error("Unexpected error");
}
```

**Why This Matters:**

- Client code can catch specific exception types
- Domain exception metadata (field, code) is preserved
- Better debugging with full stack traces
- Type-safe error handling throughout the stack

---

## Project-Specific Guidelines

### When to Defer Minor Issues

**Acceptable deferrals:**

1. **Test mock `any` types** - If mock needs flexibility
2. **Generic Error in infrastructure** - If wrapping external libraries
3. **Console.log in dev utilities** - If for debugging only

**Document deferrals:**

```typescript
// @ts-expect-error - SonarLint: Using 'any' for test flexibility
// Justification: Mock needs to work with multiple use case types
const mockFactory: any = { create: vi.fn() };
```

### Quality Gates

**Before PR Creation:**

```bash
pnpm test           # All tests pass
pnpm build          # Build succeeds
pnpm tsc --noEmit   # Type check clean
# SonarLint analysis # Zero blockers/critical
```

**During Code Review:**

- All blockers fixed
- All critical fixed
- Major issues addressed or justified
- Deferrals documented

---

## Error Handling Standards (Validated)

### Preserve Domain Exception Types

**Pattern from PR #14 SonarLint fixes:**

```typescript
// app/_actions/episodes.ts
export async function trackEpisode(episodeId: number, rating: number) {
  return withAuthenticatedRLS(prisma, async (tx, user) => {
    try {
      const useCase = UseCaseFactory.createTrackEpisodeUseCase();
      await useCase.execute({ episodeId, rating }, user.id);

      revalidatePath(`/episodes/${episodeId}`);
      return { success: true };
    } catch (error) {
      // ✅ Preserve all domain exceptions
      if (error instanceof ValidationException) {
        throw error; // Preserves: field, message, code
      }
      if (error instanceof NotFoundException) {
        throw error; // Preserves: entityType, entityId
      }
      if (error instanceof DomainException) {
        throw error; // Base class for all domain exceptions
      }
      if (error instanceof Error) {
        throw error; // Preserve stack trace
      }
      throw new Error("Failed to track episode");
    }
  });
}
```

**Client can now handle specific types:**

```typescript
// app/_components/EpisodeTracker.tsx
try {
  await trackEpisode(episodeId, rating);
  toast.success("Episode tracked!");
} catch (error) {
  if (error instanceof ValidationException) {
    // Show field-specific error
    toast.error(`${error.field}: ${error.message}`);
  } else if (error instanceof NotFoundException) {
    toast.error(`${error.entityType} not found`);
  } else {
    toast.error("Something went wrong");
  }
}
```

---

## Type Safety Rules

### Production Code

- ✅ Zero `any` types allowed
- ✅ Use `unknown` for truly dynamic data, then narrow
- ✅ Use `Partial<T>` for optional fields
- ✅ Use generics for flexible types
- ❌ No implicit `any` from missing types

### Test Code

- ✅ Prefer `Partial<Interface>` for mocks
- ✅ Use `@ts-expect-error` only when necessary
- ✅ Document WHY `any` is used
- ❌ Don't use `any` without comment

**Examples:**

```typescript
// ✅ Production - Use Partial<T>
function updateUser(id: string, updates: Partial<User>) {
  // ...
}

// ✅ Production - Use unknown
function parseJson(input: unknown): ParsedData {
  if (typeof input !== "string") {
    throw new TypeError("Expected string");
  }
  return JSON.parse(input);
}

// ✅ Test - Document any usage
// @ts-expect-error - Test mock intentionally uses any for flexibility
const mockUseCase: any = {
  execute: vi.fn().mockResolvedValue({ success: true }),
};

// ✅ Test - Better with Partial
const mockUseCase: Partial<TrackEpisodeUseCase> = {
  execute: vi.fn().mockResolvedValue({ success: true }),
};
```

---

## Integration with CI/CD

### GitHub Actions (Future)

```yaml
# .github/workflows/quality-check.yml
name: Code Quality

on:
  pull_request:
    branches: [main]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: SonarQube Analysis
        uses: sonarsource/sonarqube-scan-action@master
        with:
          args: >
            -Dsonar.projectKey=thesimpsonsapi
            -Dsonar.qualitygate.wait=true
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### Local Pre-Push Hook

```bash
# .git/hooks/pre-push
#!/bin/bash
echo "Running SonarLint analysis..."
# Add SonarLint CLI check here
# Exit 1 if blockers/critical found
```

---

## Common Patterns from PR #14

### Files Fixed

1. [app/\_actions/collections.ts](../../../app/_actions/collections.ts) - 2 fixes
2. [app/\_actions/episodes.ts](../../../app/_actions/episodes.ts) - 1 fix
3. [app/\_actions/diary.ts](../../../app/_actions/diary.ts) - 2 fixes
4. [app/\_actions/social.ts](../../../app/_actions/social.ts) - 1 fix
5. [vitest.setup.ts](../../../vitest.setup.ts) - 1 fix

### Pattern: Server Action Error Handling

**Before (loses type):**

```typescript
catch (error) {
  if (error instanceof ValidationException) {
    throw new Error(error.message);
  }
  throw new Error("Failed");
}
```

**After (preserves type):**

```typescript
catch (error) {
  if (error instanceof ValidationException || error instanceof DomainException) {
    throw error;
  }
  if (error instanceof Error) {
    throw error;
  }
  throw new Error("Failed");
}
```

### Pattern: Test Mock Flexibility

**Vitest Setup:**

```typescript
// vitest.setup.ts
vi.mock("next/image", () => ({
  // ❌ Before: any type
  default: (props: any) => props,

  // ✅ After: explicit type
  default: (props: Record<string, unknown>) => props,
}));
```

---

## Resources

- [SonarLint for VS Code](https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarlint-vscode)
- [SonarQube Rules](https://rules.sonarsource.com/typescript)
- [TypeScript Best Practices](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
- [Project Lessons: .traces/05-sonarlint-pr14-cleanup.md](../../../.traces/05-sonarlint-pr14-cleanup.md)
