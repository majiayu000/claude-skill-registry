---
name: multi-ai-testing
description: Test-driven development with independent verification to prevent test gaming. TDD workflows, test generation, coverage validation (≥80% gate, ≥95% target), property-based testing, edge case discovery. Use when implementing TDD workflows, generating comprehensive test suites, validating test coverage, or preventing test gaming through independent multi-agent verification.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Multi-AI Testing

## Overview

multi-ai-testing provides test-driven development workflows with independent verification to prevent test gaming and ensure comprehensive test coverage.

**Purpose**: Generate high-quality tests through TDD, achieve ≥80% coverage (gate) / ≥95% (target), prevent agents from gaming their own tests

**Pattern**: Workflow-based (4 core workflows)

**Key Innovation**: **Independent verification** through separate test/implementation agents prevents overfitting and test gaming

**Core Principles** (validated by tri-AI research):
1. **Test-First Development** - Write tests BEFORE implementation
2. **Independent Verification** - Separate agents for testing vs. implementation
3. **Comprehensive Coverage** - ≥80% gate, ≥95% achievable with AI edge case discovery
4. **Non-Deterministic Evaluation** - Scoring systems, not binary pass/fail
5. **Self-Healing Tests** - Tests adapt to code changes (80% maintenance reduction)

---

## When to Use

Use multi-ai-testing when:

- Implementing test-driven development (TDD)
- Generating comprehensive test suites (unit, integration, E2E)
- Validating test coverage (≥80% minimum)
- Preventing test gaming (independent verification)
- Discovering edge cases (AI-powered exploration)
- Maintaining and evolving tests (self-healing adaptation)

---

## Prerequisites

### Required
- Test framework installed (Jest, Vitest, pytest, etc.)
- Code or specifications to test
- Coverage tool available

### Recommended
- **multi-ai-implementation** - For implementing code after tests written
- **multi-ai-verification** - For test quality verification

### Understanding
- TDD concepts (test-first development)
- Coverage metrics (line, branch, function)
- Testing frameworks for your language

---

## Testing Workflows

### Workflow 1: TDD (Test-Driven Development)

The core test-first development workflow that prevents mock implementations and test gaming.

**Purpose**: Ensure tests drive implementation, not the reverse

**Pattern**: Test → Fail → Implement → Pass → Verify (Independent)

**Process**:

1. **Define Specifications**:
   ```markdown
   # Feature Specification

   **Function**: generateToken(user: User): string

   **Requirements**:
   - Accepts user object with id
   - Returns JWT string (format: xxx.yyy.zzz)
   - Token includes userId claim
   - Token expires in 24 hours
   - Throws error for invalid user

   **Edge Cases**:
   - user is null/undefined
   - user.id is missing
   - JWT_SECRET not configured
   ```

2. **Generate Tests First** (Test Agent):

   **Spawn Independent Test Agent** (Task tool):
   ```typescript
   const testGeneration = await task({
     description: "Generate tests for token generation",
     prompt: `Generate comprehensive tests for token generation function.

     Specifications (read from spec.md):
     - Function: generateToken(user)
     - Requirements: [paste from spec]
     - Edge cases: [list all]

     Generate tests covering:
     1. Happy path (valid user)
     2. All edge cases
     3. Error scenarios
     4. Security considerations

     Use Jest/Vitest framework.
     Write to: tests/auth/generateToken.test.ts

     DO NOT implement the function.
     Tests should FAIL initially (function doesn't exist yet).`
   });
   ```

3. **Confirm Tests Fail**:
   ```bash
   # Run generated tests
   npm test -- tests/auth/generateToken.test.ts

   # Expected output:
   # ❌ FAIL tests/auth/generateToken.test.ts
   #    ● generateToken is not defined
   #    ● [All tests fail as expected]

   # If tests pass: ⚠️ Problem! Tests should fail without implementation.
   ```

4. **Implement to Pass Tests** (Implementation Agent):

   **Spawn Separate Implementation Agent** (Task tool):
   ```typescript
   const implementation = await task({
     description: "Implement generateToken function",
     prompt: `Implement the generateToken function to pass existing tests.

     Tests are in: tests/auth/generateToken.test.ts
     Implement in: src/auth/tokens.ts

     Requirements:
     - Make all tests pass
     - Do NOT modify tests
     - Follow patterns from tests

     Success: All tests in generateToken.test.ts pass`
   });
   ```

   **Key**: Separate agent can't see test generation reasoning, only tests themselves

5. **Verify Tests Pass**:
   ```bash
   # Run tests again
   npm test -- tests/auth/generateToken.test.ts

   # Expected:
   # ✅ PASS tests/auth/generateToken.test.ts
   #    ● generateToken › returns valid JWT ✓
   #    ● generateToken › includes userId ✓
   #    ● generateToken › expires in 24h ✓
   #    ● generateToken › throws on invalid user ✓
   #    [All tests pass]
   ```

6. **Independent Verification** (Verification Agent):

   **Spawn Independent Verifier** (Task tool):
   ```typescript
   const verification = await task({
     description: "Verify tests and implementation quality",
     prompt: `Review tests (tests/auth/generateToken.test.ts) and implementation (src/auth/tokens.ts).

     Do NOT read implementation conversation.

     Verify:
     1. Tests actually test requirements (not overfitted)
     2. Edge cases adequately covered
     3. Implementation is quality code (not test gaming)
     4. Security considerations addressed

     Score quality (0-100).
     Write report to: tdd-verification.md`
   });

   // Read verification
   const report = readFile('tdd-verification.md');
   if (report.score >= 90) {
     // ✅ Approved: Tests and implementation are quality
   } else {
     // ⚠️ Issues found: Address before commit
   }
   ```

**Outputs**:
- Tests written first (before implementation)
- Tests confirm initial failure
- Implementation passes all tests
- Independent verification score ≥90/100
- No test gaming (verified)

**Validation**:
- [ ] Tests generated before implementation
- [ ] Tests confirmed to fail initially
- [ ] Separate agent implemented code
- [ ] Implementation agent didn't modify tests
- [ ] All tests now pass
- [ ] Independent verification score ≥90
- [ ] No overfitting detected

**Time Estimate**: 1-3 hours

---

### Workflow 2: Test Generation

Generate comprehensive test suites covering unit, integration, E2E, property-based, and edge cases.

**Purpose**: Achieve ≥95% coverage through automated test generation

**Pattern**: Analyze → Generate (multiple types) → Execute → Validate

**Process**:

1. **Analyze Target** (code or specifications):
   ```bash
   # For existing code
   grep "export.*function\|export.*class" --glob "src/**/*.ts"

   # Identify all testable units
   # Map function signatures
   # Note current coverage gaps
   ```

2. **Generate Unit Tests** (function/class level):
   ```typescript
   const unitTests = await task({
     description: "Generate unit tests",
     prompt: `Generate comprehensive unit tests for src/auth/tokens.ts.

     For each exported function/class:
     - Happy path tests
     - Edge case tests
     - Error scenario tests

     Use Jest framework.
     Write to: tests/auth/tokens.test.ts

     Target: ≥80% coverage of tokens.ts`
   });
   ```

3. **Generate Integration Tests** (component level):
   ```typescript
   const integrationTests = await task({
     description: "Generate integration tests",
     prompt: `Generate integration tests for authentication flow.

     Components to integrate:
     - src/auth/tokens.ts (token generation)
     - src/auth/validate.ts (token validation)
     - src/api/auth.ts (API endpoints)

     Test workflows:
     - Token generation → validation (round-trip)
     - API login → token return → validation
     - Token expiry → validation failure

     Write to: tests/integration/auth-flow.test.ts`
   });
   ```

4. **Generate E2E Tests** (complete workflows):
   ```typescript
   const e2eTests = await task({
     description: "Generate E2E tests",
     prompt: `Generate end-to-end tests for complete auth workflow.

     User journeys:
     1. Register → Email confirm → Login → Access protected resource
     2. Login → Get token → Refresh token → Continue session
     3. Failed login → Rate limiting → Account lockout

     Use Playwright or Cypress.
     Write to: tests/e2e/auth-workflows.test.ts`
   });
   ```

5. **Generate Property-Based Tests** (invariants):
   ```typescript
   const propertyTests = await task({
     description: "Generate property-based tests",
     prompt: `Generate property-based tests for token generation.

     Invariants to test:
     - All generated tokens are valid JWTs (xxx.yyy.zzz format)
     - All tokens contain userId claim
     - All tokens expire (have exp claim)
     - Token validation is inverse of generation (roundtrip)

     Use fast-check (JS) or Hypothesis (Python).
     Write to: tests/properties/tokens.property.test.ts`
   });
   ```

6. **Generate Edge Case Tests**:
   ```typescript
   const edgeCaseTests = await task({
     description: "Generate edge case tests",
     prompt: `Generate edge case tests for authentication.

     Edge cases (AI-discovered):
     - Empty/null inputs
     - Maximum input sizes
     - Boundary conditions (exactly 24h expiry)
     - Invalid formats
     - Unicode/special characters
     - Concurrent requests
     - Leap year date edge cases
     - Timezone edge cases

     Write to: tests/edge-cases/auth-edge-cases.test.ts`
   });
   ```

**Can Parallelize**:
```typescript
// All test generation in parallel
const [unit, integration, e2e, properties, edges] = await Promise.all([
  task({description: "Unit tests", prompt: "..."}),
  task({description: "Integration tests", prompt: "..."}),
  task({description: "E2E tests", prompt: "..."}),
  task({description: "Property tests", prompt: "..."}),
  task({description: "Edge case tests", prompt: "..."})
]);
```

**Outputs**:
- Comprehensive test suite (5 test types)
- ≥95% coverage (AI finds cases humans miss)
- All test types generated
- Edge cases discovered

**Validation**:
- [ ] Unit tests generated
- [ ] Integration tests generated
- [ ] E2E tests generated
- [ ] Property tests generated
- [ ] Edge case tests generated
- [ ] All tests executable
- [ ] Coverage estimated ≥95%

**Time Estimate**: 30-90 minutes

---

### Workflow 3: Coverage Validation

Measure test coverage, identify gaps, generate missing tests until ≥80% (gate) or ≥95% (target) achieved.

**Purpose**: Ensure comprehensive test coverage

**Pattern**: Measure → Identify Gaps → Generate Tests → Re-Measure → Report

**Process**:

1. **Execute Test Suite**:
   ```bash
   # Run all tests with coverage
   npm test -- --coverage

   # Or for Python
   pytest --cov=src --cov-report=html
   ```

2. **Measure Coverage** (multiple dimensions):
   ```markdown
   # Coverage Report

   **Line Coverage**: 78% (target: ≥80%)
   **Branch Coverage**: 72% (target: ≥80%)
   **Function Coverage**: 85% (target: ≥90%)
   **Path Coverage**: 65% (target: ≥70%)

   **Status**: Below gate (need ≥80% line coverage)
   ```

3. **Identify Uncovered Code**:
   ```bash
   # Find uncovered lines/functions
   npm run coverage:uncovered

   # Or use coverage report
   open coverage/index.html

   # Note which functions/branches not covered
   ```

   **Example Output**:
   ```markdown
   # Uncovered Code

   **src/auth/tokens.ts**:
   - Lines 45-52: Error handling branch (not tested)
   - Lines 78-82: Token refresh logic (no tests)
   - Function: validateExpiry() - 0% coverage

   **src/auth/validate.ts**:
   - Lines 23-28: Edge case (expired token by 1 second)
   ```

4. **Generate Missing Tests** (for gaps):
   ```typescript
   const gapTests = await task({
     description: "Generate tests for coverage gaps",
     prompt: `Generate tests to cover identified gaps.

     Uncovered code:
     - src/auth/tokens.ts lines 45-52 (error handling)
     - src/auth/tokens.ts lines 78-82 (refresh logic)
     - validateExpiry() function (0% coverage)

     Generate tests that exercise:
     - Error handling branches
     - Token refresh scenarios
     - validateExpiry function with various expiry times

     Write to: tests/auth/coverage-gaps.test.ts`
   });
   ```

5. **Re-Measure Coverage**:
   ```bash
   # Run tests again with new tests
   npm test -- --coverage

   # Check improvement
   # Before: 78% → After: 87% ✅ (≥80% gate passed)
   ```

6. **Generate Coverage Report**:
   ```markdown
   # Final Coverage Report

   **Line Coverage**: 87% ✅ (gate: ≥80%)
   **Branch Coverage**: 82% ✅
   **Function Coverage**: 92% ✅
   **Path Coverage**: 74% ✅

   **Status**: GATE PASSED ✅

   **Gaps Remaining** (if targeting 95%):
   - src/auth/admin.ts: 45% (low priority admin functions)
   - Edge cases in error recovery (rare scenarios)

   **Recommendation**: Current coverage sufficient for gate.
   Target 95% in future iteration if needed.
   ```

**Outputs**:
- Coverage measurements (all dimensions)
- Gap analysis (uncovered code identified)
- Additional tests generated for gaps
- Final coverage report
- Gate status (≥80% pass/fail)

**Validation**:
- [ ] Coverage measured across all dimensions
- [ ] Gaps identified specifically
- [ ] Tests generated for critical gaps
- [ ] Re-measurement shows improvement
- [ ] Gate threshold achieved (≥80%)

**Time Estimate**: 30-60 minutes

---

### Workflow 4: Independent Verification

Prevent test gaming through multi-agent ensemble verification.

**Purpose**: Verify tests actually test requirements (not overfitted to implementation)

**Pattern**: Spawn Independent Verifier → Ensemble Evaluation → Score → Report

**Process**:

1. **Spawn Independent Verification Agent** (Task tool):

   **Critical**: Separate agent that hasn't seen implementation process

   ```typescript
   const verification = await task({
     description: "Independently verify test quality",
     prompt: `Verify test quality for authentication tests.

     Tests: tests/auth/*.test.ts
     Code: src/auth/*.ts
     Specifications: specs/auth-requirements.md

     DO NOT read previous implementation conversation.

     Verify:
     1. Tests match original specifications (not just what code does)
     2. Edge cases adequately covered (not just happy path)
     3. Tests would catch real bugs (not superficial)
     4. No overfitting to specific implementation details
     5. Property-based tests present (invariants)

     Score each dimension (0-20):
     - Specification alignment: /20
     - Edge case coverage: /20
     - Bug detection capability: /20
     - Implementation independence: /20
     - Property coverage: /20

     Total: /100

     Write detailed report to: independent-verification.md`
   });
   ```

2. **Multi-Agent Ensemble** (for critical features):

   **Spawn 3 Independent Verifiers** (voting ensemble):
   ```typescript
   // 3 separate agents, no shared context
   const [verify1, verify2, verify3] = await Promise.all([
     task({description: "Verifier 1", prompt: verificationPrompt}),
     task({description: "Verifier 2", prompt: verificationPrompt}),
     task({description: "Verifier 3", prompt: verificationPrompt})
   ]);

   // Aggregate scores (median to prevent outliers)
   const scores = [
     verify1.score, // e.g., 92
     verify2.score, // e.g., 88
     verify3.score  // e.g., 90
   ];

   const medianScore = median(scores); // 90
   const variance = max(scores) - min(scores); // 92-88 = 4

   if (variance > 15) {
     // High disagreement → spawn 2 more verifiers
     // Use 5-agent ensemble for final score
   }

   if (medianScore >= 90) {
     // ✅ Tests are high quality, independent
   } else {
     // ⚠️ Tests may be overfitted or incomplete
   }
   ```

3. **Cross-Verify Against Specifications**:
   ```markdown
   # Specification Verification

   For each requirement in specs/auth-requirements.md:
   ✅ Req 1: "Tokens expire in 24h" → Test: validateExpiry.test.ts:15-20 ✓
   ✅ Req 2: "Invalid user throws error" → Test: generateToken.test.ts:45-50 ✓
   ❌ Req 3: "Token refresh supported" → NO TEST FOUND

   **Finding**: Missing test for Requirement 3
   **Action**: Generate test for token refresh
   ```

4. **Score Test Quality**:
   ```markdown
   # Test Quality Score (0-100)

   ## Specification Alignment (/20)
   - All requirements have tests: 18/20 (1 missing)

   ## Edge Case Coverage (/20)
   - Boundary conditions tested: 17/20 (good)

   ## Bug Detection Capability (/20)
   - Would catch real bugs: 18/20 (strong)

   ## Implementation Independence (/20)
   - Tests don't assume implementation details: 19/20 (excellent)

   ## Property Coverage (/20)
   - Invariants tested: 15/20 (basic property tests present)

   **Total**: 87/100

   **Status**: ⚠️ PASS (≥80) but below ideal (≥90)
   **Recommendation**: Add test for Req 3, improve property coverage
   ```

5. **Provide Actionable Feedback**:
   ```markdown
   # Verification Feedback

   ## Critical Issues (Must Fix)
   None

   ## High Priority (Should Fix)
   1. **Missing test for token refresh**
      - **What**: Requirement 3 has no test coverage
      - **Where**: tests/auth/generateToken.test.ts
      - **Why**: Core functionality untested
      - **How**: Add test suite for refresh logic
      - **Priority**: High

   ## Medium Priority
   1. **Property test coverage low**
      - **What**: Only 2 invariants tested
      - **How**: Add tests for: roundtrip (generate→validate), expiry monotonicity

   **Estimated Effort**: 30-45 min to reach ≥90 score
   ```

**Outputs**:
- Independent verification report
- Quality score (0-100)
- Specification cross-check
- Actionable feedback (What/Where/Why/How/Priority)
- Ensemble score (if used)

**Validation**:
- [ ] Independent agent verified (no implementation context)
- [ ] Specification alignment checked
- [ ] Quality scored (0-100)
- [ ] Actionable feedback provided
- [ ] Ensemble used for critical features (optional)

**Time Estimate**: 45-90 minutes (ensemble adds 30 min)

---

## Integration with Other Skills

### With multi-ai-implementation

**Called During**: Step 3 (Incremental Implementation)

**Process**:
1. Implementation invokes TDD workflow
2. Tests generated first
3. Implementation makes tests pass
4. Continuous integration

**Benefit**: Test-driven development enforced

---

### With multi-ai-verification

**Called For**: Test quality verification

**Process**:
1. Tests generated
2. Verification checks test quality
3. Independent scoring
4. Feedback for improvement

**Benefit**: Ensures tests are high quality, not gaming

---

## Quality Standards

### Coverage Targets
- **Gate (must pass)**: ≥80% line coverage
- **Target (desired)**: ≥95% line coverage
- **Stretch**: 100% with mutation testing

### Test Quality Score
- **Gate**: ≥80/100 for basic quality
- **Target**: ≥90/100 for production
- **Dimensions**: Specification alignment, edge cases, bug detection, independence, property coverage

### Independence Verification
- **Always**: Use separate test/implementation agents
- **Critical features**: Use 3-5 agent ensemble
- **Scoring**: Median of ensemble (prevent outliers)

---

## Appendix A: Independence Protocol

### How Test Independence is Maintained

**Technical Isolation**:
1. Test generation agent spawned via Task tool
2. Prompt does NOT reference implementation approach
3. Agent sees: Specifications ONLY (no code yet)

**During TDD**:
```typescript
// Step 1: Test agent sees specifications only
await task({
  prompt: "Generate tests from specs/auth.md. No code exists yet."
});

// Step 2: Implementation agent sees tests only
await task({
  prompt: "Implement code to pass tests in tests/auth/. Do NOT modify tests."
});

// Step 3: Verification agent sees both, but fresh context
await task({
  prompt: "Verify tests in tests/auth/ match specs/auth.md independently."
});
```

**Bias Prevention**:
- Specifications written BEFORE test generation
- Test agent cannot see implementation decisions
- Implementation agent cannot modify tests
- Verification agent evaluates independence

**Enforcement**:
- Prompt engineering (explicit independence)
- Verification checklist (independence maintained?)
- Post-verification audit (manual check)

**Validation of Independence**:
- If verifier finds 0 issues: ⚠️ Suspicious (expected some feedback)
- If verifier finds 1-3 issues: ✅ Healthy skepticism
- If verifier finds >5 issues: ⚠️ Tests may be low quality

---

## Appendix B: Technical Foundation

### Test Frameworks Supported

**JavaScript/TypeScript**:
- Jest, Vitest (unit/integration)
- Playwright, Cypress (E2E)
- fast-check (property-based)

**Python**:
- pytest (unit/integration/E2E)
- Hypothesis (property-based)

**Coverage Tools**:
- JS/TS: c8, nyc, istanbul
- Python: pytest-cov, coverage.py

### CI/CD Integration
```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm test -- --coverage
      - run: npx c8 check-coverage --lines 80
```

### Cost Controls
- **Test generation**: Use Sonnet (faster, cheaper than Opus)
- **Verification**: Use ensemble (3 agents) only for critical features
- **Budget cap**: $30/month for test generation

---

## Quick Reference

### The 4 Workflows

| Workflow | Purpose | Time | Output |
|----------|---------|------|--------|
| **TDD** | Test-first development | 1-3h | Tests + implementation (verified) |
| **Generation** | Comprehensive test creation | 30-90m | 5 test types, ≥95% coverage |
| **Coverage** | Validate and improve coverage | 30-60m | Coverage report (≥80% gate) |
| **Verification** | Independent quality check | 45-90m | Quality score (0-100) |

### Coverage Gates

- **Gate (must pass)**: ≥80% line coverage
- **Target (desired)**: ≥95% line coverage
- **Stretch**: 100% with mutation tests

### Quality Scores

- **≥90**: Excellent (production-ready)
- **80-89**: Good (acceptable)
- **70-79**: Needs work (improve before production)
- **<70**: Poor (regenerate tests)

---

**multi-ai-testing ensures comprehensive, independently-verified test coverage through TDD workflows, preventing test gaming and achieving ≥95% coverage with AI-powered edge case discovery.**

For TDD examples, see examples/. For independence protocol, see Appendix A.
