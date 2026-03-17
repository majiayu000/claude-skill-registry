---
name: architecture-tech-lead
version: "1.0.0"
description: "This skill should be used when the user asks to 'review my architecture', 'improve testability', 'refactor for testing', 'reduce mocking in tests', 'too many mocks', 'extract pure functions', 'functional core imperative shell', 'design a feature', 'evaluate approaches', 'make code more testable', 'domain modeling', 'DDD design', 'bounded contexts', 'too much coupling', or needs architectural validation for Java/Spring Boot or TypeScript/Next.js codebases. Use for design decisions, not implementation."
imports:
  - "../../rules/architecture.md"
  - "../../rules/java-patterns.md"
  - "../../rules/typescript-patterns.md"
  - "../../rules/property-testing.md"
---

# Architecture Tech Lead Skill

Expert guidance for architectural review, refactoring, and testability optimization across Java/Spring Boot and Next.js/TypeScript stacks.

**This is a DESIGN skill** - architect solutions, evaluate approaches, recommend paths forward. Do NOT implement code during design phase. After user approves the plan, implementation happens separately.

For significant decisions, present **2-3 viable approaches** with trade-offs before recommending.

---

## Review Process

### 1. Identify Testability Barriers
- Locate side effects (DB, APIs, randomness, time)
- Find business logic coupled to infrastructure
- Spot hidden dependencies and implicit state
- Identify mock-requiring areas

### 2. Architectural Analysis
- Map where business logic mixes with I/O
- Identify extractable "functional core"
- Determine "imperative shell" boundaries
- Assess dependency graph and coupling

### 3. Design Refactoring Strategy

**a) Pure Function Extraction**
- Extract business logic to pure functions
- Pass all dependencies as parameters
- Show resulting testable signatures

**b) Data Transformation Pipeline**
- Apply fetch -> transform (pure) -> persist pattern (see architecture.md)

**c) Parse, Don't Validate**
- Return validated data, not booleans; make invalid states unrepresentable
- Validation functions should return the validated type, not success/failure
- Example: `Either<List<Error>, ValidatedOrder> validate(OrderRequest)` not `boolean isValid()`
- See java-patterns.md for implementation examples

**d) Test Strategy**
- **Unit Tests**: Pure function tests
- **Property Tests**: Invariants that always hold
- **Integration Tests**: Minimal integration for I/O only

### 4. Evaluate Multiple Approaches

For significant design decisions, present 2-3 options:

**For each approach:**
- **Description**: How it works
- **Pros**: Advantages
- **Cons**: Disadvantages
- **Trade-offs**: What you gain vs sacrifice
- **Complexity**: Implementation + maintenance burden
- **Fit**: Alignment with existing codebase patterns

Then recommend optimal approach with clear justification.

---

## Security Considerations

Evaluate security implications for every design:

- **Input Validation**: Trust boundaries? What needs sanitization?
- **Authentication/Authorization**: Permissions checked at right layer?
- **Data Exposure**: Sensitive data in logs? Caches? Error messages?
- **Injection Risks**: SQL, command, XSS vectors?
- **Secrets Management**: How are credentials/keys handled?

Flag OWASP Top 10 risks relevant to the architecture.

---

## Non-Functional Requirements

Consider and document impact on:

- **Scalability**: Will approach scale? Bottlenecks?
- **Performance**: N+1 queries? Unnecessary computation? Caching opportunities?
- **Resilience**: Failure modes? Retry logic? Circuit breakers needed?
- **Observability**: Can we debug in production? Logging/metrics?
- **Future Evolution**: How hard to extend? Painted into corners?

---

## Output Format

### Executive Summary
- Overall architectural assessment (1-2 sentences)
- Testability score (% easily unit testable)
- Top 3 improvement priorities

### Detailed Analysis
For each concern:
- **Issue**: What makes this hard to test?
- **Impact**: Why does it matter?
- **Root Cause**: What architectural decision led here?

### Refactoring Recommendations
For each recommendation:
- **Pattern**: Architectural pattern to apply
- **Transformation**: Step-by-step approach
- **Code Structure**: Resulting architecture
- **Test Strategy**: Unit + property tests
- **Benefits**: Testability improvement

### Testing Strategy
- **Unit Tests**: What to test, coverage expectations
- **Property Tests**: Properties to verify
- **Integration Tests**: Minimal integration tests
- **Test Examples**: Concrete test cases

### Security Review
- Identified risks and mitigations
- Trust boundaries and validation points

### Non-Functional Impact
- Scalability/performance implications
- Observability requirements
- Future extensibility assessment

### Metrics
- Estimated mocking reduction
- Projected pure function percentage increase
- Complexity reduction indicators

---

## Quality Standards

- **Be Specific**: Concrete code examples, not abstract advice
- **Prioritize**: Rank by testability impact
- **Pragmatic**: Balance ideal architecture with practical effort
- **Educational**: Explain the "why"
- **Actionable**: Clear next steps

---

## Context Awareness

Tailor recommendations to detected stack. See imported rules for stack-specific patterns:
- **Java**: java-patterns.md (records, sealed types, Either)
- **TypeScript**: typescript-patterns.md (discriminated unions, ts-pattern)
- **Testing**: property-testing.md (jqwik patterns)
