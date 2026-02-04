---
name: ts-foundation-restorer
emoji: "⭐"
description: "Systematically restore TypeScript foundation by fixing missing interface properties, recreating store methods, and resolving type definition issues"
keywords: typescript, compilation, error, missing property, type definition, tsc, no emit, build failure
category: specialized
triggers: typescript compilation errors, missing types, foundation issues
---

# TypeScript Foundation Restoration

## Purpose
This skill provides systematic TypeScript foundation restoration for the Pomo-Flow application when compilation fails due to missing interface properties, store methods, or type definitions.

## Quick Context
- **Complexity**: high
- **Duration**: 45-90 minutes
- **Dependencies**: typescript, vue, pinia, @vue/runtime-core

## Activation Triggers
- **Keywords**: typescript, compilation, error, missing property, task interface, store method, type definition, tsc, no emit
- **Files**: src/stores/tasks.ts, src/**/*.ts, src/**/*.vue, tsconfig.json, package.json
- **Contexts**: typescript, compilation, type-system, interface, store, pinia, vue, foundation

## 🚨 CRITICAL TESTING REQUIREMENTS

### **MANDATORY Testing Protocol**
**ZERO TOLERANCE POLICY**: NEVER claim TypeScript fixes work without comprehensive testing. All foundation fixes MUST be validated through:

1. **Playwright Visual Testing**: Verify application loads and functions correctly
2. **DevTools Type Checking**: Ensure no type errors in browser console
3. **Compilation Verification**: Run `npx tsc --noEmit` to confirm zero errors
4. **Runtime Testing**: Test all affected functionality in browser

## Implementation Strategy

### Phase 1: Error Analysis
```typescript
// Step 1: Categorize TypeScript errors systematically
interface ErrorCategory {
  missingProperties: Array<{file: string, property: string, line: number}>
  missingMethods: Array<{file: string, method: string, expectedType: string}>
  typeDefinitionIssues: Array<{file: string, type: string, issue: string}>
  importProblems: Array<{file: string, import: string, problem: string}>
  returnTypeMismatches: Array<{file: string, function: string, expected: string, actual: string}>
}

// Command: npx tsc --noEmit --skipLibCheck 2>&1 | head -100
```

### Phase 2: Task Interface Restoration
**Current Missing Properties Identified:**
- `scheduledDate: string` - Legacy field for calendar scheduling
- `scheduledTime?: string` - Time component for scheduled tasks
- `isUncategorized?: boolean` - Task classification flag
- `estimatedPomodoros?: number` - Planning field for task estimation
- `instances?: TaskInstance[]` - Calendar instances (NEW)
- Complete TaskInstance interface definition

### Phase 3: Store Method Restoration
**Missing Methods to Implement:**
```typescript
const getTask = (taskId: string): Task | undefined => {
  return tasks.value.find(task => task.id === taskId)
}

const getUncategorizedTaskCount = computed(() => {
  return tasks.value.filter(task =>
    task.projectId === 'uncategorized' ||
    task.isUncategorized ||
    !task.projectId
  ).length
})
```

### Phase 4: Import/Export Resolution
**Fix RecurrencePattern Import Issue:**
```typescript
// WRONG (used as value):
import { RecurrencePattern } from '@/types/recurrence'

// CORRECT (used as type):
import type { RecurrencePattern } from '@/types/recurrence'
```

### Phase 5: Validation Pipeline
**Automated Validation Steps:**
```typescript
interface ValidationStep {
  name: string
  command: string
  successCriteria: string
  failureAction: string
}

const validationPipeline: ValidationStep[] = [
  {
    name: 'TypeScript Compilation Check',
    command: 'npx tsc --noEmit --skipLibCheck',
    successCriteria: 'Compilation completed without errors',
    failureAction: 'Fix compilation errors before proceeding'
  },
  {
    name: 'Development Server Start',
    command: 'npm run dev',
    successCriteria: 'VITE server running successfully',
    failureAction: 'Fix runtime configuration issues'
  },
  {
    name: 'Browser Validation (Playwright)',
    command: 'npx playwright test --config playwright.config.ts',
    successCriteria: 'All tests pass',
    failureAction: 'Fix runtime functionality issues'
  }
]
```

## Common Error Patterns & Solutions

### Pattern 1: Property Access Errors
```typescript
// ERROR: Property 'scheduledDate' does not exist on type 'Task'
// SOLUTION: Add property to Task interface with backward compatibility
```

### Pattern 2: Method Not Found Errors
```typescript
// ERROR: Property 'getTask' does not exist on type 'UnwrapRef...'
// SOLUTION: Implement missing store methods with proper TypeScript types
```

### Pattern 3: Type Import vs Value Import
```typescript
// ERROR: 'RecurrencePattern' refers to a value but is being used as a type
// SOLUTION: Use 'import type' for type-only imports
```

### Pattern 4: Return Type Mismatch
```typescript
// ERROR: Type 'Promise<boolean>' is not assignable to type 'Promise<void>'
// SOLUTION: Fix method signatures to return correct types
```

## Quick Validation Commands
```bash
# Quick TypeScript check (10 seconds)
npx tsc --noEmit --skipLibCheck --incremental false

# Development server health check (15 seconds)
timeout 15s npm run dev -- --host 0.0.0.0 --port 5546

# Build process test (30 seconds)
npm run build

# Playwright smoke test (2 minutes)
npx playwright test --config playwright.config.ts --grep "smoke"
```

## Expected Outcomes
After successful execution:
- ✅ **Zero TypeScript Errors**: `npx tsc --noEmit` passes cleanly
- ✅ **Fast Compilation**: Development server starts in <15 seconds
- ✅ **Complete Task Interface**: All expected properties including scheduledDate, TaskInstance available
- ✅ **Functional Store Methods**: getTask, getUncategorizedTaskCount work correctly
- ✅ **Working Application**: All features compile and run properly
- ✅ **Surface Fixes Work**: Claude's previous fixes actually function
- ✅ **Performance Restored**: No more slow compilation or runtime type errors

## Success Criteria
- [ ] TypeScript compilation succeeds with 0 errors (`npx tsc --noEmit`)
- [ ] Development server starts quickly without errors (<15 seconds)
- [ ] All Task properties are accessible (scheduledDate, scheduledTime, isUncategorized, etc.)
- [ ] All store methods work correctly (getTask, getUncategorizedTaskCount)
- [ ] Application loads and functions properly in browser
- [ ] Previously broken features now work
- [ ] Playwright validation passes (if available)

## 🚨 CRITICAL REMINDER

**EVERY TypeScript fix MUST be tested before claiming success:**
1. **Visual Verification**: Use Playwright MCP to see the application working
2. **Type Error Check**: Verify no console errors in DevTools
3. **Compilation Test**: Ensure `npx tsc --noEmit` passes completely
4. **Functionality Test**: Test the specific features that were broken

**NEVER claim TypeScript foundation is restored without comprehensive testing evidence.**

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
