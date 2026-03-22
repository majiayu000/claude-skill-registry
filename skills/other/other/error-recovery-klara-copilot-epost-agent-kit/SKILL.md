---
name: error-recovery
description: (ePost) Use when operations fail transiently — timeouts, network errors, retries, circuit breakers, graceful degradation
metadata:
  agent-affinity: [epost-fullstack-developer, epost-debugger, epost-tester]
  keywords: [error, retry, fallback, circuit-breaker, backoff, resilience, failure, exponential, degradation]
  platforms: [all]
  triggers: [error, exception, timeout, retry, fallback]
  connections:
    enhances: [debug]
---

# Error Recovery Skill

Standardized patterns for robust error handling in agent execution.

## Overview

This skill provides battle-tested strategies for handling failures gracefully: retry with exponential backoff, circuit breaker patterns, and fallback strategies. Use when operations may fail transiently (network, timeouts) or when you need graceful degradation.

## When to Use

- Network requests that may timeout or fail
- External API calls with intermittent issues
- File operations on unreliable storage
- Multi-step workflows where individual steps can fail
- Agent delegation with potential cascade failures

## Core Patterns

### 1. Retry with Exponential Backoff

**When**: Transient errors (network timeout, rate limiting, temporary unavailability)

**Pattern**:
```javascript
async function retryWithBackoff(operation, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      if (!isRetriable(error) || attempt === maxRetries - 1) {
        throw error;
      }
      const delay = Math.pow(2, attempt) * 1000; // 1s, 2s, 4s
      await sleep(delay);
    }
  }
}

function isRetriable(error) {
  const retriableCodes = ['ETIMEDOUT', 'ECONNRESET', 'ENOTFOUND'];
  return retriableCodes.includes(error.code) ||
         (error.status >= 500 && error.status < 600);
}
```

### 2. Circuit Breaker

**When**: Cascading failures (agent A fails → agent B fails → agent C fails)

**Pattern**:
```javascript
class CircuitBreaker {
  constructor(threshold = 3, timeout = 60000) {
    this.failureCount = 0;
    this.threshold = threshold;
    this.timeout = timeout;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.nextAttempt = Date.now();
  }

  async execute(operation) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker OPEN');
      }
      this.state = 'HALF_OPEN';
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}
```

### 3. Fallback Strategy

**When**: Primary approach fails, acceptable alternative exists

**Pattern**:
```javascript
async function withFallback(primary, fallback, condition) {
  try {
    return await primary();
  } catch (error) {
    if (condition(error)) {
      console.warn('Primary failed, using fallback:', error.message);
      return await fallback();
    }
    throw error;
  }
}

// Example usage
const result = await withFallback(
  () => complexAIAnalysis(code),
  () => simplePatternMatching(code),
  (err) => err.code === 'TIMEOUT' || err.code === 'RATE_LIMIT'
);
```

## Decision Matrix

| Scenario | Strategy | Max Retries | Backoff |
|----------|----------|-------------|---------|
| Network request | Retry | 3 | Exponential (1s, 2s, 4s) |
| External API | Retry + Circuit Breaker | 3 | Exponential |
| File read/write | Retry | 2 | Linear (500ms, 1s) |
| Agent delegation | Circuit Breaker + Fallback | 1 | None |
| User input validation | Fail Fast | 0 | None |
| Missing dependency | Fail Fast | 0 | None |

## When to Fail Fast

**Do NOT retry for**:
- Invalid input (schema validation failures)
- Missing required dependencies
- Authentication/authorization errors
- Logical errors in code
- Data corruption

**Pattern**:
```javascript
if (!isValid(input)) {
  throw new Error('Invalid input - fix and retry');
}

if (!fs.existsSync(requiredFile)) {
  throw new Error('Missing required file');
}
```

## Agent-Specific Guidelines

### For Implementer Agents

- Retry file operations (transient disk issues)
- Fail fast on syntax errors
- Fallback: simpler implementation if complex approach fails

### For Tester Agents

- Retry flaky tests (once only)
- Fail fast on compilation errors
- Fallback: skip optional tests if infrastructure unavailable

### For Git Manager

- Retry push (network issues)
- Fail fast on merge conflicts
- Fallback: none (git operations must succeed)

### For Researcher Agents

- Retry API calls (rate limiting, timeouts)
- Circuit breaker for unreliable sources
- Fallback: use cached results if available

## Best Practices

1. **Log retries clearly**: Help debugging
2. **Set reasonable limits**: Avoid infinite loops
3. **Preserve original error**: Include in final throw
4. **Document why retrying**: Comment the reasoning
5. **Monitor failure rates**: Track circuit breaker trips

## Example Integration

```javascript
// In subagent execution
const circuitBreaker = new CircuitBreaker(3, 60000);

try {
  const result = await circuitBreaker.execute(async () => {
    return await retryWithBackoff(
      () => implementFeature(spec),
      3
    );
  });
  return result;
} catch (error) {
  // Fallback to simpler implementation
  console.warn('Complex implementation failed, using simpler approach');
  return await simpleImplementation(spec);
}
```

## References

- [AWS Architecture Blog: Exponential Backoff](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Martin Fowler: Circuit Breaker](https://martinfowler.com/bliki/CircuitBreaker.html)

### Related Skills
- `debug` — Systematic debugging methodology
- `problem-solving` — Root cause analysis techniques
- `knowledge-capture` — Persist error patterns and recovery strategies
