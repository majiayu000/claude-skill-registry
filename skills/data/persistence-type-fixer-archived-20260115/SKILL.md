---
name: persistence-type-fixer
description: SYSTEMATICALLY fix TypeScript generic type system issues in persistence and backup layers. Resolves unknown type assignments, generic constraint failures, and type inference problems that are blocking the application from compiling. CRITICAL: Addresses the root cause of 40% of remaining TypeScript errors in persistence layer.
---

# TypeScript Persistence Type System Fixer

This skill provides comprehensive resolution of generic type system issues in the persistence and backup layers of the Pomo-Flow application.

## Quick Context
- **Complexity**: high
- **Duration**: 20-40 minutes
- **Dependencies**: typescript, vue, pinia, @vue/runtime-core, vite

## Activation Triggers
- **Keywords**: persistence, generic type, unknown type, type constraint, backup, bulletproof, unknown assignable
- **Files**: src/composables/useBulletproofPersistence.ts, src/composables/useAutoBackup.ts, persistence layer files
- **Contexts**: typescript, persistence, generic, type system, database, backup

## 🚨 CRITICAL PERSISTENCE TYPE ISSUES

### **IMMEDIATE Generic Type System Failures**
**CURRENT BLOCKING ISSUES:**
1. **Type 'unknown' is not assignable to type 'T'** - Multiple instances in persistence layer
2. **Generic constraint satisfaction problems** - Firestore adapters and database operations
3. **Type inference failures** - Arbitrary type instantiation issues
4. **Array type mismatches** - Empty object '{}' vs expected array types

### **Why Surface-Level Fixes Don't Work:**
```
// Claude's "fix":
const data: unknown = response.json()
return data as T  // ❌ Unsafe type assertion

// REAL problem:
function useBulletproofPersistence<T>(): T {
  const data = getFromStorage() // returns unknown
  return data  // ❌ Type error: unknown not assignable to T
}
```

## Generic Type System Resolution Process

### Phase 1: Generic Type Analysis (Critical)
```typescript
// Identify generic type failures
interface GenericTypeIssue {
  file: string
  lineNumber: number
  errorType: 'unknown_assignment' | 'constraint_failure' | 'inference_error' | 'array_mismatch'
  genericParameter: string
  actualType: string
  expectedType: string
  context: string
}
```

### Phase 2: Type Guard Implementation (Critical)
```typescript
// Type-safe generic persistence with proper type guards
export function createTypedPersistence<T>(
  typeGuard: (value: unknown) => value is T
): {
  get: () => T | null
  set: (value: T) => Promise<void>
  validate: (value: unknown) => value is T
}

// Example usage:
const taskPersistence = createTypedPersistence<Task>(
  (value): value is Task => {
    return typeof value === 'object' &&
           value !== null &&
           'id' in value &&
           'title' in value
  }
)
```

### Phase 3: Generic Constraint Resolution (Critical)
```typescript
// Fix generic constraints with proper extends clauses
export interface BulletproofPersistence<T extends Record<string, any>> {
  data: Ref<T | null>
  isLoading: Ref<boolean>
  save: (data: T) => Promise<void>
  load: () => Promise<T | null>
  validate: (data: unknown) => data is T
}

// Type-safe database operations
export function useTypedDatabase<
  K extends keyof typeof DB_KEYS
>(
  key: K
): {
  get: () => Promise<(typeof DB_KEYS)[K] | null>
  set: (data: (typeof DB_KEYS)[K]) => Promise<void>
}
```

### Phase 4: Array Type System Fixes (Critical)
```typescript
// Fix empty object vs array type issues
export function useAutoBackup<T extends Record<string, any>>(
  config: {
    interval: number
    maxSize?: number
    validator?: (data: unknown) => data is T[]
  }
): {
  backups: Ref<T[]>
  addBackup: (data: T) => Promise<void>
  loadBackups: () => Promise<T[]>
}

// Type-safe array operations
export const validateTypedArray = <T>(
  data: unknown,
  itemGuard: (item: unknown) => item is T
): data is T[] => {
  return Array.isArray(data) && data.every(itemGuard)
}
```

### Phase 5: Firestore Adapter Type Safety (Critical)
```typescript
// Firestore adapter with proper generic types
export class TypedFirestoreAdapter<T extends { id: string }> {
  constructor(
    private collection: string,
    private typeGuard: (data: unknown) => data is T
  ) {}

  async get(id: string): Promise<T | null> {
    const doc = await this.firestore.collection(this.collection).doc(id).get()
    const data = doc.data()
    return data && this.typeGuard(data) ? data : null
  }

  async set(entity: T): Promise<void> {
    // Type-safe operations
    await this.firestore.collection(this.collection).doc(entity.id).set(entity)
  }
}
```

## Implementation Patterns

### Pattern 1: Type Guard Composable
```typescript
// Reusable type guard system
export function useTypeGuard<T>(
  validator: (value: unknown) => value is T
) {
  const validate = (value: unknown): value is T => {
    return validator(value)
  }

  const assertValid = (value: unknown): T => {
    if (!validator(value)) {
      throw new TypeError(`Invalid type: expected ${typeof validator}, got ${typeof value}`)
    }
    return value
  }

  return {
    validate,
    assertValid
  }
}
```

### Pattern 2: Generic Persistence Hook
```typescript
// Type-safe generic persistence
export function useTypedPersistence<T>(
  key: string,
  validator: (value: unknown) => value is T,
  defaultValue: T
) {
  const data = ref<T>(defaultValue)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const load = async () => {
    isLoading.value = true
    try {
      const stored = localStorage.getItem(key)
      if (stored) {
        const parsed = JSON.parse(stored)
        if (validator(parsed)) {
          data.value = parsed
        }
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load'
    } finally {
      isLoading.value = false
    }
  }

  const save = async (value: T) => {
    isLoading.value = true
    try {
      localStorage.setItem(key, JSON.stringify(value))
      data.value = value
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to save'
    } finally {
      isLoading.value = false
    }
  }

  return {
    data: readonly(data),
    isLoading: readonly(isLoading),
    error: readonly(error),
    load,
    save
  }
}
```

### Pattern 3: Backup System with Type Safety
```typescript
// Type-safe backup system
export function useTypedBackup<T>(
  storageKey: string,
  validator: (value: unknown) => value is T[]
) {
  const backups = ref<T[]>([])
  const isLoading = ref(false)

  const addBackup = async (data: T) => {
    const newBackup = {
      data,
      timestamp: Date.now()
    }
    backups.value.push(newBackup)

    const allBackups = [...backups.value]
    localStorage.setItem(storageKey, JSON.stringify(allBackups))
  }

  const loadBackups = async (): Promise<T[]> => {
    try {
      const stored = localStorage.getItem(storageKey)
      if (stored) {
        const parsed = JSON.parse(stored)
        if (validator(parsed)) {
          backups.value = parsed
        }
      }
    } catch (err) {
      console.error('Failed to load backups:', err)
    }
    return backups.value
  }

  return {
    backups: readonly(backups),
    isLoading: readonly(isLoading),
    addBackup,
    loadBackups
  }
}
```

## Error Resolution Map

### Error Type 1: Unknown Type Assignment
```typescript
// BEFORE (Error):
function useBulletproofPersistence<T>(): T {
  const data = getFromStorage() // returns unknown
  return data  // ❌ Type error

// AFTER (Fixed):
function useBulletproofPersistence<T>(
  validator: (value: unknown) => value is T
): Ref<T | null> {
  const data = ref<T | null>(null)

  const load = async () => {
    const stored = getFromStorage()
    if (validator(stored)) {
      data.value = stored
    }
  }

  return data
}
```

### Error Type 2: Array Type Mismatch
```typescript
// BEFORE (Error):
const backups: any[] = JSON.parse(localStorage.getItem('backups') || '{}')  // ❌ {} not assignable to any[]

// AFTER (Fixed):
const backups: T[] = []
try {
  const stored = localStorage.getItem('backups')
  if (stored) {
    const parsed = JSON.parse(stored)
    if (Array.isArray(parsed)) {
      backups.push(...parsed.filter(validator))
    }
  }
} catch (err) {
  console.warn('Failed to load backups, starting with empty array')
}
```

## Expected Outcomes
After successful execution:
- ✅ **Zero Generic Type Errors**: All `unknown` type assignment issues resolved
- ✅ **Type-Safe Persistence**: All persistence operations use proper type guards
- ✅ **Generic Constraints**: All generic parameters have proper extends constraints
- ✅ **Array Type Safety**: All array operations use proper type validation
- ✅ **Database Operations**: All database operations are type-safe

## Success Criteria
- [ ] Generic type errors reduced by 40%
- [ ] All persistence composables compile without errors
- [ ] Type guards implemented for all critical data structures
- [ ] Firestore adapters work with proper type safety
- [ ] Backup system uses type-safe array operations

## Validation Commands
```bash
# TypeScript compilation check
npx tsc --noEmit --skipLibCheck

# Specific persistence layer tests
npm run test -- --grep "persistence"

# Development server test
npm run dev
```

---
**This skill addresses the most critical TypeScript foundation issues that are preventing the persistence layer from functioning correctly.**

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
