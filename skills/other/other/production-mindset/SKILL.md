---
name: vibe-production-mindset
description: Sets quality expectations for implementation — "imagine this serves 1 million users." Checks for observability, error handling, input validation, graceful degradation.
user-invocable: true
---

# vibe-production-mindset

The gap between "works on my machine" and "works in production" is where incidents live.

## When to Use This Skill

- Starting any implementation that will run in production
- When implementing API endpoints, data processing, or user-facing features
- Before declaring a feature "done"
- When the user cares about production quality

## When NOT to Use This Skill

- Prototypes or spikes explicitly marked as throwaway
- Internal scripts that run once
- Test code (different quality criteria)
- When the user says "just get it working"

## The Checklist

Imagine this code serves 1 million users. Check:

### 1. Observability
- [ ] Structured logging at key decision points (not just errors)
- [ ] Tracing/correlation ID propagated through the request
- [ ] Metrics for key operations (latency, success/failure counts)
- [ ] Alerts defined for anomalies

### 2. Error Handling at System Boundaries
- [ ] External API calls have timeouts
- [ ] External API calls have retries with backoff
- [ ] File I/O handles "file not found" and "permission denied"
- [ ] Network errors are handled (connection refused, timeout, DNS failure)
- [ ] Database errors are handled (connection lost, constraint violation)

### 3. Input Validation
- [ ] All external input validated before processing
- [ ] Size limits on string/array inputs
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] Authentication checked before authorization

### 4. Graceful Degradation
- [ ] Circuit breakers for external dependencies
- [ ] Fallback behavior when dependencies are unavailable
- [ ] Graceful shutdown (drain connections, finish in-flight)
- [ ] Health check endpoint

### 5. Resource Management
- [ ] Connections closed/returned to pool
- [ ] Goroutines/threads have lifecycle management
- [ ] Memory bounded (no unbounded growth)
- [ ] File handles closed

## Steps

1. **Read the implementation**
2. **Run through the checklist** — not every item applies to every feature
3. **Flag gaps** — only for items that DO apply
4. **Recommend fixes** — specific, not generic

## Output Format

### Production Readiness: [Feature Name]

**Overall**: READY / NEEDS_WORK / NOT_READY

| Category | Status | Gaps |
|----------|--------|------|
| Observability | ✓/◐/✗ | [count] |
| Error Handling | ✓/◐/✗ | [count] |
| Input Validation | ✓/◐/✗ | [count] |
| Graceful Degradation | ✓/◐/✗ | [count] |
| Resource Management | ✓/◐/✗ | [count] |

### Critical Gaps
1. [Gap with specific file:line and fix suggestion]

### Note
This is NOT about over-engineering. It's about not under-engineering the critical paths. A simple feature should have simple production hardening — logging, error handling, and input validation. Not every feature needs circuit breakers.
