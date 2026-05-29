---
name: rn-observability
description: Logging, error messages, and debugging patterns for React Native. Use when adding logging, designing error messages, debugging production issues, or improving code observability.
---

# React Native Observability

## Problem Statement

Silent failures are debugging nightmares. Code that returns early without logging, error messages that lack context, and missing observability make production issues impossible to diagnose. Write code as if you'll debug it at 3am with only logs.

---

## Pattern: No Silent Early Returns

**Problem:** Early returns without logging create invisible failure paths.

**Example (from retake bug):**

```typescript
// WRONG - silent death
const saveAnswer = (questionId: string, value: number) => {
  if (!retakeAreas.has(skillArea)) {
    return;  // ❌ Why did we return? No one knows.
  }
  // ... save logic
};

// CORRECT - observable
const saveAnswer = (questionId: string, value: number) => {
  if (!retakeAreas.has(skillArea)) {
    logger.warn('[saveAnswer] Dropping answer - skill area not in retake set', {
      questionId,
      skillArea,
      retakeAreas: Array.from(retakeAreas),
    });
    return;
  }
  // ... save logic
};
```

**Rule:** Every early return should log why it's returning, with enough context to diagnose.

---

## Pattern: Error Message Design

**Problem:** Error messages that don't help diagnose the issue.

```typescript
// BAD - no context
throw new Error('No answers found');

// BAD - slightly better but still useless at 3am
throw new Error('No answers found. Please complete at least one question.');

// GOOD - diagnostic context included
throw new Error(
  `No answers found. Completed: ${Object.keys(completedAnswers).length}, ` +
  `New: ${Object.keys(userAnswers).length}, ` +
  `Assessment ID: ${assessmentId}. This may indicate a timing issue.`
);
```

**Error message template:**

```typescript
throw new Error(
  `[${functionName}] ${whatFailed}. ` +
  `Context: ${relevantState}. ` +
  `Possible cause: ${hypothesis}.`
);
```

**What to include:**

| Element | Why |
|---------|-----|
| Function/location | Where the error occurred |
| What failed | The specific condition that wasn't met |
| Relevant state | Values that help diagnose |
| Possible cause | Your best guess for the fix |

---

## Pattern: Structured Logging

**Problem:** Console.log statements that are hard to parse and search.

```typescript
// BAD - unstructured
console.log('saving answer', questionId, value);
console.log('current state', answers);

// GOOD - structured with context object
logger.info('[saveAnswer] Saving answer', {
  questionId,
  value,
  skillArea,
  existingAnswerCount: Object.keys(answers).length,
});
```

**Logging levels:**

| Level | Use for |
|-------|---------|
| `error` | Exceptions, failures that need immediate attention |
| `warn` | Unexpected conditions that didn't fail but might indicate problems |
| `info` | Important business events (user actions, flow milestones) |
| `debug` | Detailed diagnostic info (state dumps, timing) |

**Wrapper for consistent logging:**

```typescript
// utils/logger.ts
const LOG_LEVELS = ['debug', 'info', 'warn', 'error'] as const;
type LogLevel = typeof LOG_LEVELS[number];

const currentLevel: LogLevel = __DEV__ ? 'debug' : 'warn';

function shouldLog(level: LogLevel): boolean {
  return LOG_LEVELS.indexOf(level) >= LOG_LEVELS.indexOf(currentLevel);
}

export const logger = {
  debug: (message: string, context?: object) => {
    if (shouldLog('debug')) {
      console.log(`[DEBUG] ${message}`, context ?? '');
    }
  },
  info: (message: string, context?: object) => {
    if (shouldLog('info')) {
      console.log(`[INFO] ${message}`, context ?? '');
    }
  },
  warn: (message: string, context?: object) => {
    if (shouldLog('warn')) {
      console.warn(`[WARN] ${message}`, context ?? '');
    }
  },
  error: (message: string, context?: object) => {
    if (shouldLog('error')) {
      console.error(`[ERROR] ${message}`, context ?? '');
    }
  },
};
```

---

## Pattern: Sensitive Data Handling

**Problem:** Logging sensitive data to console or crash reporting.

```typescript
// utils/secureLogger.ts
const SENSITIVE_KEYS = ['password', 'token', 'ssn', 'creditCard', 'apiKey'];

function redactSensitive(obj: object): object {
  const redacted = { ...obj };
  for (const key of Object.keys(redacted)) {
    if (SENSITIVE_KEYS.some(s => key.toLowerCase().includes(s))) {
      redacted[key] = '[REDACTED]';
    } else if (typeof redacted[key] === 'object' && redacted[key] !== null) {
      redacted[key] = redactSensitive(redacted[key]);
    }
  }
  return redacted;
}

export const secureLogger = {
  info: (message: string, context?: object) => {
    const safeContext = context ? redactSensitive(context) : undefined;
    logger.info(message, safeContext);
  },
  // ... other levels
};
```

---

## Pattern: Flow Tracing

**Problem:** Multi-step operations where it's unclear how far execution got.

```typescript
async function retakeFlow(assessmentId: string, skillArea: string) {
  const flowId = `retake-${Date.now()}`;
  
  logger.info(`[retakeFlow:${flowId}] Starting`, { assessmentId, skillArea });
  
  try {
    logger.debug(`[retakeFlow:${flowId}] Step 1: Loading completed answers`);
    await loadCompletedAssessmentAnswers(assessmentId);
    
    logger.debug(`[retakeFlow:${flowId}] Step 2: Enabling retake`);
    await enableSkillAreaRetake(skillArea);
    
    logger.debug(`[retakeFlow:${flowId}] Step 3: Clearing answers`);
    await clearSkillAreaAnswers(skillArea);
    
    logger.info(`[retakeFlow:${flowId}] Completed successfully`);
  } catch (error) {
    logger.error(`[retakeFlow:${flowId}] Failed`, {
      error: error.message,
      stack: error.stack,
      assessmentId,
      skillArea,
    });
    throw error;
  }
}
```

**Benefits:**
- Can search logs by flowId to see entire flow
- Know exactly which step failed
- Timing visible via timestamps

---

## Pattern: State Snapshots for Debugging

**Problem:** Need to understand state at specific points in complex flows.

```typescript
function snapshotState(label: string) {
  const state = useStore.getState();
  logger.debug(`[StateSnapshot] ${label}`, {
    answers: Object.keys(state.answers).length,
    retakeAreas: Array.from(state.retakeAreas),
    completedAnswers: Object.keys(state.completedAssessmentAnswers).length,
    loading: state.loading,
  });
}

// Usage in flow
async function retakeFlow() {
  snapshotState('Before load');
  await loadCompletedAnswers(id);
  snapshotState('After load');
  await enableRetake(area);
  snapshotState('After enable');
}
```

---

## Pattern: Assertion Helpers

**Problem:** Conditions that "should never happen" but need visibility when they do.

```typescript
// utils/assertions.ts
export function assertDefined<T>(
  value: T | null | undefined,
  context: string
): asserts value is T {
  if (value === null || value === undefined) {
    const message = `[Assertion Failed] Expected defined value: ${context}`;
    logger.error(message, { value });
    throw new Error(message);
  }
}

export function assertCondition(
  condition: boolean,
  context: string,
  debugInfo?: object
): asserts condition {
  if (!condition) {
    const message = `[Assertion Failed] ${context}`;
    logger.error(message, debugInfo);
    throw new Error(message);
  }
}

// Usage
assertDefined(assessment, `Assessment not found: ${assessmentId}`);
assertCondition(
  retakeAreas.has(skillArea),
  `Skill area not in retake set`,
  { skillArea, retakeAreas: Array.from(retakeAreas) }
);
```

---

## Pattern: Production Error Reporting

**Problem:** Errors in production with no visibility.

```typescript
// Integration with error reporting service
import * as Sentry from '@sentry/react-native';

export function captureError(
  error: Error,
  context?: Record<string, unknown>
) {
  logger.error(error.message, { ...context, stack: error.stack });
  
  if (!__DEV__) {
    Sentry.captureException(error, {
      extra: context,
    });
  }
}

// Usage
try {
  await riskyOperation();
} catch (error) {
  captureError(error, {
    assessmentId,
    skillArea,
    userAnswers: Object.keys(userAnswers),
  });
  throw error;
}
```

---

## Checklist: Adding Observability

When writing new code:

- [ ] All early returns have logging with context
- [ ] Error messages include diagnostic information
- [ ] Multi-step operations have flow tracing
- [ ] Sensitive data is redacted before logging
- [ ] State snapshots available for debugging complex flows
- [ ] Production errors are captured with context

When debugging existing code:

- [ ] Add logging to suspect early returns
- [ ] Add state snapshots before and after async operations
- [ ] Check for silent catches that swallow errors
- [ ] Verify error messages have enough context

---

## Quick Debugging Template

Add this temporarily when debugging async/state issues:

```typescript
const DEBUG = true;

function debugLog(label: string, data?: object) {
  if (DEBUG) {
    console.log(`[DEBUG ${Date.now()}] ${label}`, data ?? '');
  }
}

// In your flow
debugLog('Flow start', { inputs });
debugLog('After step 1', { state: getState() });
debugLog('After step 2', { state: getState() });
debugLog('Flow end', { result });
```

Remove before committing, or gate behind a flag.
