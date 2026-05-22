---
name: resilience-patterns
description: Production-grade fault tolerance for distributed systems. Use when implementing circuit breakers, retry with exponential backoff, bulkhead isolation patterns, or building resilience into LLM API integrations.
context: fork
agent: backend-system-architect
version: 1.0.0
author: SkillForge AI Agent Hub
tags: [resilience, circuit-breaker, bulkhead, retry, fault-tolerance]
user-invocable: false
---

# Resilience Patterns Skill

Production-grade resilience patterns for distributed systems and LLM-based workflows. Covers circuit breakers, bulkheads, retry strategies, and LLM-specific resilience techniques.

## When to Use This Skill

- Building fault-tolerant multi-agent systems
- Implementing LLM API integrations with proper error handling
- Designing distributed workflows that need graceful degradation
- Adding observability to failure scenarios
- Protecting systems from cascade failures

## Core Patterns

### 1. Circuit Breaker Pattern (reference: circuit-breaker.md)

Prevents cascade failures by "tripping" when a service exceeds failure thresholds.

```
+-------------------------------------------------------------------+
|                    Circuit Breaker States                         |
+-------------------------------------------------------------------+
|                                                                   |
|    +----------+     failures >= threshold    +----------+         |
|    |  CLOSED  | ----------------------------> |   OPEN   |        |
|    | (normal) |                              | (reject) |         |
|    +----+-----+                              +----+-----+         |
|         |                                         |               |
|         | success                    timeout      |               |
|         |                            expires      |               |
|         |         +------------+                  |               |
|         |         | HALF_OPEN  |<-----------------+               |
|         +---------+  (probe)   |                                  |
|                   +------------+                                  |
|                                                                   |
|   CLOSED:    Allow requests, count failures                       |
|   OPEN:      Reject immediately, return fallback                  |
|   HALF_OPEN: Allow probe request to test recovery                 |
|                                                                   |
+-------------------------------------------------------------------+
```

**Key Configuration:**
- `failure_threshold`: Failures before opening (default: 5)
- `recovery_timeout`: Seconds before attempting recovery (default: 30)
- `half_open_requests`: Probes to allow in half-open (default: 1)

### 2. Bulkhead Pattern (reference: bulkhead-pattern.md)

Isolates failures by partitioning resources into independent pools.

```
+-------------------------------------------------------------------+
|                      Bulkhead Isolation                           |
+-------------------------------------------------------------------+
|                                                                   |
|   +------------------+  +------------------+                      |
|   | TIER 1: Critical |  | TIER 2: Standard |                      |
|   |  (5 workers)     |  |  (3 workers)     |                      |
|   |  +-+ +-+ +-+     |  |  +-+ +-+ +-+     |                      |
|   |  |#| |#| | |     |  |  |#| | | | |     |                      |
|   |  +-+ +-+ +-+     |  |  +-+ +-+ +-+     |                      |
|   |  +-+ +-+         |  |                  |                      |
|   |  | | | |         |  |  Queue: 2        |                      |
|   |  +-+ +-+         |  |                  |                      |
|   |  Queue: 0        |  +------------------+                      |
|   +------------------+                                            |
|                                                                   |
|   +------------------+                                            |
|   | TIER 3: Optional |   # = Active request                       |
|   |  (2 workers)     |     = Available slot                       |
|   |  +-+ +-+         |                                            |
|   |  |#| |#| FULL!   |   Tier 1: synthesis, quality_gate          |
|   |  +-+ +-+         |   Tier 2: analysis agents                  |
|   |  Queue: 5        |   Tier 3: enrichment, optional features    |
|   +------------------+                                            |
|                                                                   |
+-------------------------------------------------------------------+
```

**Tier Configuration (SkillForge):**
| Tier | Workers | Queue | Timeout | Use Case |
|------|---------|-------|---------|----------|
| 1 (Critical) | 5 | 10 | 300s | Synthesis, quality gate |
| 2 (Standard) | 3 | 5 | 120s | Content analysis agents |
| 3 (Optional) | 2 | 3 | 60s | Enrichment, caching |

### 3. Retry Strategies (reference: retry-strategies.md)

Intelligent retry logic with exponential backoff and jitter.

```
+-------------------------------------------------------------------+
|                   Exponential Backoff + Jitter                    |
+-------------------------------------------------------------------+
|                                                                   |
|   Attempt 1:  --> X (fail)                                        |
|               wait: 1s +/- 0.5s                                   |
|                                                                   |
|   Attempt 2:  --> X (fail)                                        |
|               wait: 2s +/- 1s                                     |
|                                                                   |
|   Attempt 3:  --> X (fail)                                        |
|               wait: 4s +/- 2s                                     |
|                                                                   |
|   Attempt 4:  --> OK (success)                                    |
|                                                                   |
|   Formula: delay = min(base * 2^attempt, max_delay) * jitter      |
|   Jitter:  random(0.5, 1.5) to prevent thundering herd            |
|                                                                   |
+-------------------------------------------------------------------+
```

**Error Classification for Retries:**
```python
RETRYABLE_ERRORS = {
    # HTTP/Network
    408, 429, 500, 502, 503, 504,  # HTTP status codes
    ConnectionError, TimeoutError,  # Network errors

    # LLM-specific
    "rate_limit_exceeded",
    "model_overloaded",
    "context_length_exceeded",  # Retry with truncation
}

NON_RETRYABLE_ERRORS = {
    400, 401, 403, 404,  # Client errors
    "invalid_api_key",
    "content_policy_violation",
    "invalid_request_error",
}
```

### 4. LLM-Specific Resilience (reference: llm-resilience.md)

Patterns specific to LLM API integrations.

```
+-------------------------------------------------------------------+
|                    LLM Fallback Chain                             |
+-------------------------------------------------------------------+
|                                                                   |
|   Request --> [Primary Model] --success--> Response               |
|                     |                                             |
|                   fail                                            |
|                     v                                             |
|               [Fallback Model] --success--> Response              |
|                     |                                             |
|                   fail                                            |
|                     v                                             |
|               [Cached Response] --hit--> Response                 |
|                     |                                             |
|                   miss                                            |
|                     v                                             |
|               [Default Response] --> Graceful Degradation         |
|                                                                   |
|   Example Chain:                                                  |
|   1. claude-sonnet-4-20250514 (primary)                           |
|   2. gpt-4o-mini (fallback)                                       |
|   3. Semantic cache lookup                                        |
|   4. "Analysis unavailable" + partial results                     |
|                                                                   |
+-------------------------------------------------------------------+
```

**Token Budget Management:**
```
+-------------------------------------------------------------------+
|                     Token Budget Guard                            |
+-------------------------------------------------------------------+
|                                                                   |
|   Input: 8,000 tokens                                             |
|   +---------------------------------------------+                 |
|   |#################################            |                 |
|   +---------------------------------------------+                 |
|                                          ^                        |
|                                          |                        |
|                                    Context Limit (16K)            |
|                                                                   |
|   Strategy when approaching limit:                                |
|   1. Summarize earlier context (compress 4:1)                     |
|   2. Drop low-priority content (optional fields)                  |
|   3. Split into multiple requests                                 |
|   4. Fail fast with "content too large" error                     |
|                                                                   |
+-------------------------------------------------------------------+
```

## Quick Reference

| Pattern | When to Use | Key Benefit |
|---------|-------------|-------------|
| Circuit Breaker | External service calls | Prevent cascade failures |
| Bulkhead | Multi-tenant/multi-agent | Isolate failures |
| Retry + Backoff | Transient failures | Automatic recovery |
| Fallback Chain | Critical operations | Graceful degradation |
| Token Budget | LLM calls | Cost control, prevent failures |

## SkillForge Integration Points

1. **Workflow Agents**: Each agent wrapped with circuit breaker + bulkhead tier
2. **LLM Calls**: All model invocations use fallback chain + retry logic
3. **External APIs**: Circuit breaker on YouTube, arXiv, GitHub APIs
4. **Database Ops**: Bulkhead isolation for read vs write operations

## Files in This Skill

### References (Conceptual Guides)
- `references/circuit-breaker.md` - Deep dive on circuit breaker pattern
- `references/bulkhead-pattern.md` - Bulkhead isolation strategies
- `references/retry-strategies.md` - Retry algorithms and error classification
- `references/llm-resilience.md` - LLM-specific patterns
- `references/error-classification.md` - How to categorize errors

### Templates (Code Patterns)
- `templates/circuit-breaker.py` - Ready-to-use circuit breaker class
- `templates/bulkhead.py` - Semaphore-based bulkhead implementation
- `templates/retry-handler.py` - Configurable retry decorator
- `templates/llm-fallback-chain.py` - Multi-model fallback pattern
- `templates/token-budget.py` - Token budget guard implementation

### Examples
- `examples/skillforge-workflow-resilience.md` - Full SkillForge integration example

### Checklists
- `checklists/pre-deployment-resilience.md` - Production readiness checklist
- `checklists/circuit-breaker-setup.md` - Circuit breaker configuration guide

## 2025 Best Practices

1. **Adaptive Thresholds**: Use sliding windows, not fixed counters
2. **Observability First**: Every circuit trip = alert + metric + trace
3. **Graceful Degradation**: Always have a fallback, even if partial
4. **Health Endpoints**: Separate health check from circuit state
5. **Chaos Testing**: Regularly test failure scenarios in staging

---

## Related Skills

- `observability-monitoring` - Metrics and alerting for circuit breaker state changes
- `caching-strategies` - Cache as fallback layer in degradation scenarios
- `error-handling-rfc9457` - Structured error responses for resilience failures
- `background-jobs` - Async processing with retry and failure handling

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Circuit breaker recovery | Half-open probe | Gradual recovery, prevents immediate re-failure |
| Retry algorithm | Exponential backoff + jitter | Prevents thundering herd, respects rate limits |
| Bulkhead isolation | Semaphore-based tiers | Simple, efficient, prioritizes critical operations |
| LLM fallback | Model chain with cache | Graceful degradation, cost optimization, availability |

---

## Capability Details

### circuit-breaker
**Keywords:** circuit breaker, failure threshold, cascade failure, trip, half-open
**Solves:**
- Prevent cascade failures when external services fail
- Automatically recover when services come back online
- Fail fast instead of waiting for timeouts

### bulkhead
**Keywords:** bulkhead, isolation, semaphore, thread pool, resource pool, tier
**Solves:**
- Isolate failures to prevent entire system crashes
- Prioritize critical operations over optional ones
- Limit concurrent requests to protect resources

### retry-strategies
**Keywords:** retry, backoff, exponential, jitter, thundering herd
**Solves:**
- Handle transient failures automatically
- Avoid overwhelming recovering services
- Classify errors as retryable vs non-retryable

### llm-resilience
**Keywords:** LLM, fallback, model, token budget, rate limit, context length
**Solves:**
- Handle LLM API rate limits gracefully
- Fall back to alternative models when primary fails
- Manage token budgets to prevent context overflow

### error-classification
**Keywords:** error, retryable, transient, permanent, classification
**Solves:**
- Determine which errors should be retried
- Categorize errors by severity and recoverability
- Map HTTP status codes to resilience actions