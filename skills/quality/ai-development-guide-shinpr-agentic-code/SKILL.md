---
name: ai-development-guide
description: "Detects code smells, anti-patterns, and debugging issues. Use when: fixing bugs, reviewing code quality, or refactoring."
---

# AI Developer Guide

## Technical Anti-patterns (Red Flag Patterns)

Immediately stop and reconsider design when detecting the following patterns:

### Code Quality Anti-patterns
1. **Writing similar code 3 or more times**
2. **Multiple responsibilities mixed in a single file**
3. **Defining same content in multiple files**
4. **Making changes without checking dependencies**
5. **Disabling code with comments**
6. **Error suppression**

### Design Anti-patterns
- **"Make it work for now" thinking**
- **Patchwork implementation**
- **Optimistic implementation of uncertain technology**
- **Symptomatic fixes**
- **Unplanned large-scale changes**

## Fail-Fast Fallback Design Principles

### Core Principle
Prioritize primary code reliability over fallback implementations. In distributed systems, excessive fallback mechanisms can mask errors and make debugging difficult.

### Implementation Guidelines

#### Default Approach
- **Explicit failure over silent defaults**: Errors must be visible and traceable, not masked by automatic default values
- **Preserve error context**: Include original error information when re-throwing

#### When Fallbacks Are Acceptable
- **Only with explicit Design Doc approval**: Document why fallback is necessary
- **Business-critical continuity**: When partial functionality is better than none
- **Graceful degradation paths**: Clearly defined degraded service levels

#### Layer Responsibilities
- **Infrastructure Layer**:
  - Always throw errors upward
  - No business logic decisions
  - Provide detailed error context

- **Application Layer**:
  - Make business-driven error handling decisions
  - Implement fallbacks only when specified in requirements
  - Log all fallback activations for monitoring

### Error Masking Detection

**Review Triggers** (require design review):
- Writing 3rd error handling block in the same feature
- Multiple error handling structures in single function
- Nested error handling structures
- Error handlers that return default values without propagating

**Before Implementing Any Fallback**:
1. Verify Design Doc explicitly defines this fallback
2. Document the business justification
3. Ensure error is logged with full context
4. Add monitoring/alerting for fallback activation

### Implementation Patterns

Note: Use your language's standard error handling mechanism (exceptions, Result types, error values, etc.)

```
❌ AVOID: Silent fallback that hides errors
    [handle error]:
        return DEFAULT_USER  // Error is hidden, debugging becomes difficult

✅ PREFERRED: Explicit failure with context
    [handle error]:
        logError('Failed to fetch user data', userId, error)
        propagate ServiceError('User data unavailable', error)

✅ ACCEPTABLE: Documented fallback with monitoring (when justified in Design Doc)
    [handle error]:
        // Fallback defined in Design Doc section 3.2.1
        logWarning('Primary data source failed, using cache', error)
        incrementMetric('data.fallback.cache_used')

        cachedData = fetchFromCache()
        if not cachedData:
            propagate ServiceError('Both primary and cache failed', error)
        return cachedData
```

## Rule of Three - Criteria for Code Duplication

| Duplication Count | Action | Reason |
|-------------------|--------|--------|
| 1st time | Inline implementation | Cannot predict future changes |
| 2nd time | Consider future consolidation | Pattern beginning to emerge |
| 3rd time | Implement commonalization | Pattern established |

### Criteria for Commonalization

**Cases for Commonalization**
- Business logic duplication
- Complex processing algorithms
- Areas likely requiring bulk changes
- Validation rules

**Cases to Avoid Commonalization**
- Accidental matches (coincidentally same code)
- Possibility of evolving in different directions
- Significant readability decrease from commonalization
- Simple helpers in test code

### Implementation Example
```
// ❌ Bad: Immediate commonalization on 1st duplication
function validateUserEmail(email) { /* ... */ }
function validateContactEmail(email) { /* ... */ }
// → Premature abstraction

// ✅ Good: Commonalize on 3rd occurrence
// 1st time: inline implementation
// 2nd time: Copy but consider future
// 3rd time: Extract to common validator
function validateEmail(email, context) { /* ... */ }
```

## Common Failure Patterns and Avoidance Methods

### Pattern 1: Error Fix Chain
**Symptom**: Fixing one error causes new errors
**Cause**: Surface-level fixes without understanding root cause
**Avoidance**: Identify root cause with 5 Whys before fixing

### Pattern 2: Implementation Without Sufficient Testing
**Symptom**: Many bugs after implementation
**Cause**: Ignoring Red-Green-Refactor process
**Avoidance**: Always start with failing tests

### Pattern 4: Ignoring Technical Uncertainty
**Symptom**: Frequent unexpected errors when introducing new technology
**Cause**: Assuming "it should work according to official documentation" without prior investigation
**Avoidance**:
- Record certainty evaluation at the beginning of task files
  ```
  Certainty: low (Reason: no examples of MCP connection found)
  Exploratory implementation: true
  Fallback: use conventional API
  ```
- For low certainty cases, create minimal verification code first

### Pattern 5: Insufficient Existing Code Investigation
**Symptom**: Duplicate implementations, architecture inconsistency, integration failures
**Cause**: Insufficient understanding of existing code before implementation
**Avoidance Methods**:
- Before implementation, always search for similar functionality (using domain, responsibility, configuration patterns as keywords)
- Similar functionality found → Use that implementation (do not create new implementation)
- Similar functionality is technical debt → Create ADR improvement proposal before implementation
- No similar functionality exists → Implement new functionality following existing design philosophy
- Record all decisions and rationale in "Existing Codebase Analysis" section of Design Doc

## Debugging Techniques

### 1. Error Analysis Procedure
```bash
# How to read stack traces
1. Read error message (first line) accurately
2. Focus on first and last of stack trace
3. Identify first line where your code appears
```

### 2. 5 Whys - Root Cause Analysis
```
Symptom: Application crash on startup
Why1: Configuration loading failed → Why2: Config file format changed
Why3: Dependency update → Why4: Library breaking change
Why5: Unconstrained dependency version specification
Root cause: Inappropriate version management strategy
```

### 3. Minimal Reproduction Code
To isolate problems, attempt reproduction with minimal code:
- Remove unrelated parts
- Replace external dependencies with mocks
- Create minimal configuration that reproduces problem

### 4. Debug Log Output
```
// Track problems with structured logs
log('DEBUG:', {
  context: 'user-creation',
  input: { email, name },
  state: currentState,
  timestamp: currentTimestamp()
})
```

## Situations Requiring Technical Decisions

### Timing of Abstraction
- Extract patterns after writing concrete implementation 3 times
- Be conscious of YAGNI, implement only currently needed features
- Prioritize current simplicity over future extensibility

### Performance vs Readability
- Prioritize readability unless clear bottleneck exists
- Measure before optimizing (don't guess, measure)
- Document reason with comments when optimizing

## Continuous Improvement Mindset

- **Humility**: Perfect code doesn't exist, welcome feedback
- **Courage**: Execute necessary refactoring boldly
- **Transparency**: Clearly document technical decision reasoning

## Implementation Completeness Assurance

### Impact Analysis: Mandatory 3-Stage Process

Complete these stages sequentially before any implementation:

**1. Discovery** - Identify all affected code:
- Implementation references (imports, calls, instantiations)
- Interface dependencies (contracts, types, data structures)
- Test coverage
- Configuration (build configs, env settings, feature flags)
- Documentation (comments, docs, diagrams)

**2. Understanding** - Analyze each discovered location:
- Role and purpose in the system
- Dependency direction (consumer or provider)
- Data flow (origin → transformations → destination)
- Coupling strength

**3. Identification** - Produce structured report:
```
## Impact Analysis
### Direct Impact
- [Unit]: [Reason and modification needed]

### Indirect Impact
- [System]: [Integration path → reason]

### Data Flow
[Source] → [Transformation] → [Consumer]

### Risk Assessment
- High: [Complex dependencies, fragile areas]
- Medium: [Moderate coupling, test gaps]
- Low: [Isolated, well-tested areas]

### Implementation Order
1. [Start with lowest risk or deepest dependency]
2. [...]
```

**Critical**: Do not implement until all 3 stages are documented

**Relationship to Pattern 5**: This process provides the structured methodology to avoid "Insufficient Existing Code Investigation"

### Unused Code Deletion

When unused code is detected:
- Will it be used in this work? Yes → Implement now | No → Delete now (Git preserves)
- Applies to: Code, tests, docs, configs, assets

### Existing Code Modification

```
In use? No → Delete
       Yes → Working? No → Delete + Reimplement
                     Yes → Fix/Extend
```

**Principle**: Prefer clean implementation over patching broken code
