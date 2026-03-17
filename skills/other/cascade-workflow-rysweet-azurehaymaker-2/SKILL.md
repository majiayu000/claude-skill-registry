---
name: cascade-workflow
version: 1.0.0
description: Graceful degradation through cascading fallback strategies - ensures system always completes while maintaining acceptable functionality
auto_activates:
  - "external API"
  - "external service"
  - "timeout handling"
  - "high availability"
  - "fallback strategy"
  - "resilient operation"
explicit_triggers:
  - /amplihack:cascade
confirmation_required: false
token_budget: 3500
---

# Cascade Workflow with Graceful Degradation Skill

## Purpose

Implement graceful degradation through cascading fallback strategies. When optimal approaches fail or timeout, the system automatically falls back to simpler, more reliable alternatives while maintaining acceptable functionality.

## When to Use This Skill

**USE FOR:**
- External service dependencies (APIs, databases)
- Time-sensitive operations with acceptable degraded modes
- Operations where partial results are better than no results
- High-availability requirements (system must always respond)
- Scenarios where waiting for perfect solution is worse than good-enough solution

**AVOID FOR:**
- Operations requiring exact correctness (no acceptable degradation)
- Security-critical operations (authentication, authorization)
- Financial transactions (no room for "approximate")
- When failures must surface to user (diagnostic operations)
- Simple operations with no meaningful fallback

## Configuration

### Core Parameters

**Timeout Strategy:**
- `aggressive` - Fast failures, quick degradation (5s / 2s / 1s)
- `balanced` - Reasonable attempts (30s / 10s / 5s) - **DEFAULT**
- `patient` - Thorough attempts before fallback (120s / 30s / 10s)
- `custom` - Define your own timeouts

**Fallback Types:**
- `service` - External API → Cached data → Static defaults
- `quality` - Comprehensive → Standard → Minimal analysis
- `freshness` - Real-time → Recent → Historical data
- `completeness` - Full dataset → Sample → Summary
- `accuracy` - Precise → Approximate → Estimate

**Degradation Notification:**
- `silent` - Log only, no user notification
- `warning` - Inform user of degradation
- `explicit` - Detailed explanation of what degraded and why

## Cascade Level Requirements

**PRIMARY (Optimal):**
- Best possible outcome
- May depend on external services
- May be slow or resource-intensive
- Can fail or timeout

**SECONDARY (Acceptable):**
- Reduced quality but functional
- More reliable than primary
- Faster or fewer dependencies
- Acceptable for users

**TERTIARY (Guaranteed):**
- Always succeeds, never fails
- No external dependencies
- Fast and reliable
- Minimal but functional
- **CRITICAL: Must be designed to never fail**

## Execution Process

### Step 1: Define Cascade Levels

- **Use architect agent** to identify cascade levels
- Define PRIMARY approach (optimal solution)
- Define SECONDARY approach (acceptable degradation)
- Define TERTIARY approach (guaranteed completion)
- Set timeout for each level
- Document what degrades at each level
- **CRITICAL: Ensure tertiary ALWAYS succeeds**

**Example Cascade Definitions:**

**Code Analysis with AI:**
- PRIMARY: GPT-4 comprehensive analysis (timeout: 30s)
- SECONDARY: GPT-3.5 standard analysis (timeout: 10s)
- TERTIARY: Static analysis with regex (timeout: 5s)

**External API Data Fetch:**
- PRIMARY: Live API call (timeout: 10s)
- SECONDARY: Cached data (timeout: 2s)
- TERTIARY: Default values (timeout: 0s)

**Test Execution:**
- PRIMARY: Full test suite (timeout: 120s)
- SECONDARY: Critical tests only (timeout: 30s)
- TERTIARY: Smoke tests (timeout: 10s)

### Step 2: Attempt Primary Approach

- Execute optimal solution
- Set timeout based on strategy configuration
- Monitor execution progress
- If completes successfully: DONE (best outcome)
- If fails or times out: Continue to Step 3
- Log attempt and reason for failure

```python
# Pseudocode for primary attempt
try:
    result = execute_primary_approach(timeout=PRIMARY_TIMEOUT)
    log_success(level="PRIMARY", result=result)
    return result  # DONE - best outcome achieved
except TimeoutError:
    log_failure(level="PRIMARY", reason="timeout")
    # Continue to Step 3
except ExternalServiceError as e:
    log_failure(level="PRIMARY", reason=f"service_error: {e}")
    # Continue to Step 3
```

### Step 3: Attempt Secondary Approach

- Log degradation to secondary level
- Execute acceptable fallback solution
- Set shorter timeout (typically 1/3 of primary)
- Monitor execution progress
- If completes successfully: DONE (acceptable outcome)
- If fails or times out: Continue to Step 4
- Log attempt and reason for failure

```python
# Pseudocode for secondary attempt
log_degradation(from_level="PRIMARY", to_level="SECONDARY")
try:
    result = execute_secondary_approach(timeout=SECONDARY_TIMEOUT)
    log_success(level="SECONDARY", result=result, degraded=True)
    return result  # DONE - acceptable outcome
except TimeoutError:
    log_failure(level="SECONDARY", reason="timeout")
    # Continue to Step 4
```

### Step 4: Attempt Tertiary Approach

- Log degradation to tertiary level
- Execute guaranteed completion approach
- Set minimal timeout (typically 1s)
- **MUST succeed - no failures allowed**
- Return minimal but functional result
- Log success (degraded but functional)
- DONE (guaranteed completion)

```python
# Pseudocode for tertiary attempt
log_degradation(from_level="SECONDARY", to_level="TERTIARY")
try:
    result = execute_tertiary_approach(timeout=TERTIARY_TIMEOUT)
    log_success(level="TERTIARY", result=result, heavily_degraded=True)
    return result  # DONE - minimal but functional
except Exception as e:
    # THIS SHOULD NEVER HAPPEN
    log_critical_failure("TERTIARY approach failed - this is a bug!")
    raise SystemError("Cascade safety violation: tertiary failed")
```

### Step 5: Report Degradation

- Determine notification level from configuration
- **Silent:** Log only, no user message
- **Warning:** Brief notification to user
- **Explicit:** Detailed degradation explanation
- Document which level succeeded
- Explain impact of degradation
- Log cascade path taken for analysis

**Degradation Reporting Templates:**

**Silent Mode:**
```
[LOG] CASCADE: PRIMARY timeout (30s) → SECONDARY success (6s)
Result: standard_analysis (degraded from comprehensive)
```

**Warning Mode:**
```
⚠️  Using cached data (less than 1 hour old)
Current real-time data unavailable.
```

**Explicit Mode:**
```
ℹ️  Analysis Quality Notice

We attempted to provide comprehensive code analysis using GPT-4,
but encountered slow response times (>30s timeout).

Fallback Applied:
- Used: GPT-3.5 standard analysis (completed in 6s)
- Quality: Standard (vs. Comprehensive)
- Impact: Advanced semantic insights not included

What You're Getting:
✓ Basic pattern detection
✓ Standard recommendations
✓ Code quality assessment

What's Missing:
✗ Complex architectural insights
✗ Deep semantic analysis
✗ Advanced refactoring suggestions
```

### Step 6: Log Cascade Metrics

- Record cascade path taken
- Document level reached (primary/secondary/tertiary)
- Log timing for each level attempted
- Track degradation frequency
- Identify patterns in failures
- Update cascade strategy if needed

**Metrics to Track:**
- Success rate by level
- Average response times
- Degradation frequency
- User impact assessment

### Step 7: Continuous Optimization

- **Use analyzer agent** to review cascade metrics
- Identify optimization opportunities
- Adjust timeouts based on success rates
- Improve secondary approaches if frequently used
- Update tertiary if inadequate
- Document learnings in `.claude/context/DISCOVERIES.md`

**Optimization Criteria:**
- **If PRIMARY succeeds < 50%:** Timeout too aggressive → Increase timeout
- **If SECONDARY used > 40%:** Secondary is really the "normal" case → Swap primary and secondary
- **If TERTIARY used > 10%:** Secondary not reliable enough → Improve secondary

## Trade-Offs

**Benefit:** System always completes, never fully fails
**Cost:** Users may receive degraded responses
**Best For:** User-facing features where responsiveness matters

## Examples

### Example 1: Weather API Integration

**Configuration:**
- Strategy: Balanced (30s / 10s / 5s)
- Type: Service fallback
- Notification: Warning

**Implementation:**
```python
async def get_weather(location: str) -> WeatherData:
    """Get weather data with cascade fallback"""

    # PRIMARY: Live weather API
    try:
        return await fetch_weather_api(location, timeout=30)
    except (TimeoutError, APIError):
        log.warning("PRIMARY weather API failed, trying cache")

    # SECONDARY: Cached weather data
    try:
        cached = await get_cached_weather(location, max_age=3600)
        if cached:
            notify_user("Using weather data from cache (< 1 hour old)")
            return cached
    except CacheError:
        log.warning("SECONDARY cache failed, using defaults")

    # TERTIARY: Default weather data
    return get_default_weather(location)  # Never fails
```

**Outcome:** System always returns weather data, quality degrades gracefully

### Example 2: Code Review with AI

**Configuration:**
- Strategy: Patient (120s / 30s / 10s)
- Type: Quality fallback
- Notification: Explicit

**Cascade Path:**
1. PRIMARY: GPT-4 comprehensive review - TIMEOUT after 120s
2. SECONDARY: GPT-3.5 standard review - SUCCESS in 18s
3. TERTIARY: Not attempted

### Example 3: Search Results Ranking

**Configuration:**
- Strategy: Aggressive (5s / 2s / 1s)
- Type: Accuracy fallback
- Notification: Silent

**Implementation:**
```python
def search_and_rank(query: str) -> List[Result]:
    """Search with ML ranking, fallback to simple ranking"""

    results = fetch_results(query)

    # PRIMARY: ML-based ranking (sophisticated)
    try:
        return ml_rank(results, timeout=5)
    except TimeoutError:
        pass  # Silent fallback

    # SECONDARY: Heuristic ranking (good enough)
    try:
        return heuristic_rank(results, timeout=2)
    except TimeoutError:
        pass

    # TERTIARY: Simple text match ranking (basic)
    return simple_rank(results)  # Always fast
```

## Philosophy Alignment

This workflow enforces:
- **Resilience:** System always completes, never completely fails
- **User Experience:** Better degraded service than error message
- **Transparency:** Users understand what they're getting (if explicit mode)
- **Progressive Enhancement:** Optimal by default, degrade when necessary
- **Measurable Quality:** Clear definition of what degrades at each level
- **Continuous Improvement:** Metrics drive timeout optimization
- **Guaranteed Completion:** Tertiary level must never fail

## Key Principle

**Better to deliver degraded service than no service**
