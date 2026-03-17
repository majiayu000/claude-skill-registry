---
name: multi-ai-implementation
description: Production-ready code generation and incremental development using Explore-Plan-Code-Commit workflow. TDD-driven with <200 line changes, automatic rollback, and multi-agent coordination. Use when implementing features, refactoring code, migrating systems, or integrating components requiring rigorous testing and quality assurance.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Multi-AI Implementation

## Overview

multi-ai-implementation provides systematic code generation and incremental development using the proven Explore-Plan-Code-Commit workflow with built-in TDD, quality gates, and multi-agent coordination.

**Purpose**: Transform specifications into production-ready code through incremental, test-driven development

**Pattern**: Workflow-based (6-step sequential process)

**Key Principles** (validated by tri-AI research):
1. **Explore Before Coding** - Gather context first, never jump straight to implementation
2. **Plan Architecture** - Use multi-ai-planning before writing code
3. **Incremental Development** - Small changes (<200 lines), continuous testing
4. **Test-Driven** - Write/generate tests first, then implement
5. **Quality Gates** - Multi-layer validation before commit
6. **Safe Rollback** - Automatic revert on test failures

**Quality Guarantee**: Code generated through this workflow achieves ≥85/100 quality score with ≥80% test coverage

---

## When to Use

Use multi-ai-implementation when:

- Implementing new features (>200 lines, multiple components)
- Refactoring existing code (maintaining backward compatibility)
- Migrating systems (database, framework, architecture changes)
- Integrating components (API, services, third-party libraries)
- Building complex functionality requiring testing and verification
- Multi-agent coordination needed for parallel development

**When NOT to Use**:
- Simple changes (<50 lines, single file, obvious implementation)
- Documentation-only changes
- Configuration tweaks (use fast-track workflow instead)

---

## Prerequisites

### Required
- Clear implementation specification or plan
- Test framework available (Jest, Vitest, pytest, etc.)
- Time allocated (2-8 hours depending on complexity)

### Recommended
- **multi-ai-planning** - Create plan before implementation
- **multi-ai-testing** - Generate and execute tests
- **multi-ai-verification** - Quality validation before commit

### Understanding
- Basic TDD concepts (test-first development)
- Git workflow (commits, branches, rollback)
- Testing frameworks for your language

---

## Implementation Workflow

### Step 1: Explore & Gather Context

Gather comprehensive context through progressive disclosure before writing any code.

**Purpose**: Understand existing system, patterns, and constraints

**Inputs**:
- Implementation objective or specification
- Existing codebase (if applicable)
- Design mockups (for UI features)
- API documentation (for integrations)

**Process**:

1. **Progressive File Discovery**:

   Use 3-level approach (never load everything):

   **Level 1: Structure (Glob)**
   ```bash
   # Map relevant files
   glob "**/*.{ts,js,py}" # Source files
   glob "**/test*.{ts,js,py}" # Test files
   glob "**/*auth*" # Domain-specific
   ```

   **Level 2: Patterns (Grep)**
   ```bash
   # Find specific patterns
   grep "export.*class.*Auth" --glob "**/*.ts"
   grep "describe\|it\(" --glob "**/*.test.ts"
   grep "TODO|FIXME" --glob "src/**"
   ```

   **Level 3: Targeted Reading**
   ```bash
   # Read only critical files
   read "src/auth/login.ts"
   read "src/auth/tokens.ts"
   read "tests/auth/login.test.ts"
   ```

2. **Analyze Visual Mockups** (for UI features):
   - Read design files/screenshots
   - Understand layout requirements
   - Note component hierarchy
   - Identify styling needs

3. **Map Dependencies & Integration Points**:
   ```markdown
   # Integration Analysis

   **Components This Touches**:
   - src/auth/* (authentication logic)
   - src/api/routes.ts (API endpoints)
   - src/middleware/auth.ts (authorization)

   **External Dependencies**:
   - jsonwebtoken (JWT generation)
   - bcrypt (password hashing)

   **Integration Points**:
   - Database (users, tokens tables)
   - API (POST /login, POST /register)
   - Frontend (auth forms, protected routes)
   ```

4. **Research Domain Patterns** (optional - for unfamiliar domains):

   **If using multi-ai-research**:
   ```
   Use multi-ai-research for "Research [domain] implementation best practices and patterns"
   ```

   **Manual research**:
   - Search: "[domain] best practices 2024-2025"
   - Review: Official documentation
   - Find: 3-5 example implementations

5. **Document Context Synthesis**:
   ```markdown
   # Context Synthesis

   ## Current State
   - [What exists now]
   - [Current patterns used]
   - [Existing tests]

   ## Desired State
   - [What should exist]
   - [New functionality needed]

   ## Constraints
   - Backward compatibility required
   - Must maintain existing API
   - Performance: <200ms response time

   ## Key Insights
   - [Pattern 1 found in codebase]
   - [Best practice from research]
   - [Integration consideration]
   ```

**Outputs**:
- Context synthesis document
- File inventory (relevant files identified)
- Pattern analysis
- Integration map
- Constraint documentation

**Validation**:
- [ ] Relevant files identified via progressive disclosure
- [ ] Existing patterns understood
- [ ] Integration points mapped
- [ ] Constraints documented
- [ ] Research conducted (if needed)
- [ ] Context comprehensive

**Time Estimate**: 30-60 minutes

**Next**: Proceed to Step 2

---

### Step 2: Plan Architecture

Create detailed implementation plan using multi-ai-planning before writing any code.

**Purpose**: Think through architecture and approach before implementation

**Inputs**:
- Context synthesis (from Step 1)
- Implementation objective
- Success criteria

**Process**:

1. **Invoke Multi-AI Planning**:
   ```
   Use multi-ai-planning to create implementation plan for [objective]
   ```

   This will guide you through:
   - Objective analysis
   - Hierarchical task decomposition
   - Dependency mapping
   - Verification planning
   - Quality validation (≥90/100)

2. **Review Generated Plan**:
   ```markdown
   Plan Review Checklist:
   - [ ] All requirements covered by tasks
   - [ ] Tasks decomposed to atomic level
   - [ ] Dependencies mapped correctly
   - [ ] Each task has success criteria
   - [ ] Verification methods defined
   - [ ] Quality score ≥90/100
   ```

3. **Extract Implementation Sequence**:
   ```markdown
   # Implementation Sequence (from plan)

   Phase 1: Foundation (Tasks 1-2)
   - Task 1: Database schema
   - Task 2: Core models

   Phase 2: Business Logic (Tasks 3-4)
   - Task 3: Token management
   - Task 4: Authentication logic

   Phase 3: API Layer (Task 5)
   - Task 5: API endpoints

   Phase 4: Integration (Task 6)
   - Task 6: End-to-end integration
   ```

4. **Identify Test Strategy** (from plan verification):
   ```markdown
   # Test Strategy

   **Test-First Approach**:
   - Generate tests before implementation
   - Confirm tests fail
   - Implement until tests pass

   **Coverage Targets**:
   - Gate (must pass): ≥80% line coverage
   - Target (desired): ≥95% line coverage

   **Test Types**:
   - Unit: Functions, classes
   - Integration: Components together
   - E2E: Complete workflows
   ```

5. **Optional: Use Extended Thinking for Complex Decisions**:
   - Press Tab for extended thinking mode
   - Evaluate multiple architectural approaches
   - Reason through trade-offs
   - Document decision with rationale

**Outputs**:
- Complete implementation plan (from multi-ai-planning)
- plan.json (machine-readable)
- PLAN.md (human-readable)
- Implementation sequence
- Test strategy

**Validation**:
- [ ] Plan created using multi-ai-planning
- [ ] Plan quality score ≥90/100
- [ ] All tasks have verification defined
- [ ] Implementation sequence clear
- [ ] Test strategy documented

**Time Estimate**: 30-90 minutes (most time in multi-ai-planning)

**Next**: Proceed to Step 3

---

### Step 3: Incremental Implementation (TDD)

Implement features incrementally using test-driven development with continuous validation.

**Purpose**: Build quality code through small, tested increments

**Inputs**:
- Implementation plan (from Step 2)
- Context synthesis (from Step 1)
- Test strategy

**Process**:

1. **For Each Task in Plan, Follow TDD Cycle**:

   **3.1. Generate Tests First** (use multi-ai-testing):
   ```
   Use multi-ai-testing TDD workflow for Task [X]

   Specification:
   - [What this task should do]
   - Success criteria: [from plan]
   - Edge cases: [boundary conditions]
   ```

   This generates tests and confirms they FAIL.

   **3.2. Implement to Pass Tests** (incremental):
   ```typescript
   // Implement feature incrementally
   // Target: <200 lines per commit
   // Keep tests running continuously

   // Example: Implement token generation
   export function generateToken(user: User): string {
     // 1. Basic implementation (30 lines)
     const payload = { userId: user.id };
     const token = jwt.sign(payload, process.env.JWT_SECRET);
     return token;
   }

   // Run tests → Some pass, some fail
   // 2. Add expiry (10 lines)
   // Run tests → More pass
   // 3. Add error handling (15 lines)
   // Run tests → All pass ✅
   ```

   **3.3. Verify Tests Pass**:
   ```bash
   # Run test suite
   npm test -- src/auth/tokens.test.ts

   # Check coverage
   npm run coverage -- --file=src/auth/tokens.ts

   # Verify ≥80% coverage
   ```

   **3.4. If Tests Fail: Iterate**:
   ```markdown
   ## Iteration Loop (Max 3 Attempts)

   Attempt 1: Implement feature → Tests fail
      ↓ Analyze failure, adjust code
   Attempt 2: Fix implementation → Tests fail (different error)
      ↓ Analyze, adjust again
   Attempt 3: Final fix → Tests pass ✅

   If still failing after 3 attempts:
      ↓ HALT and request human review
      ❌ Doom Loop Prevention
   ```

   **Doom Loop Breaker** (Gemini recommendation):
   - Max 3 implementation attempts per task
   - If same error 3x: Escalate to human
   - If oscillating errors (A→B→A): Escalate
   - Prevents infinite refactoring loops

2. **Maintain Incremental Commits**:

   **Small Change Pattern**:
   ```bash
   # After each logical increment:
   git add <changed-files>
   git commit -m "Add [specific feature]: [what changed]"

   # Target: <200 lines per commit
   # Benefit: Clear intent, easy rollback
   ```

   **Automatic Rollback** on Test Failures:
   ```bash
   # If tests fail after commit:
   npm test || git reset --hard HEAD~1

   # TCR Pattern (Test-Commit-Revert):
   # - Tests pass → Commit
   # - Tests fail → Automatic revert
   ```

3. **Handle Backward Compatibility** (for changes to existing code):

   **Expand-Migrate-Contract Pattern**:
   ```markdown
   ### Example: Add OAuth to Existing Auth

   **Phase 1: Expand**
   - Add new OAuth tables/functions
   - Keep existing password auth
   - Both work in parallel

   **Phase 2: Migrate**
   - Dual-write (password + OAuth)
   - Gradual user transition
   - Validate both paths work

   **Phase 3: Contract**
   - Deprecate password auth
   - Remove old code
   - OAuth only

   **Benefit**: Zero downtime, safe rollback at each phase
   ```

4. **Error Handling Pattern**:
   ```typescript
   // Every function needs error handling

   export function generateToken(user: User): string {
     // Validate input
     if (!user || !user.id) {
       throw new Error('Invalid user: missing id');
     }

     // Validate environment
     if (!process.env.JWT_SECRET) {
       throw new Error('JWT_SECRET not configured');
     }

     try {
       // Implementation
       const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET);
       return token;
     } catch (error) {
       // Graceful handling
       console.error('Token generation failed:', error);
       throw new Error(`Failed to generate token: ${error.message}`);
     }
   }
   ```

**Outputs**:
- Working code (incremental commits)
- All tests passing
- Coverage ≥80% (gate), target ≥95%
- Error handling complete
- Backward compatible (if applicable)

**Validation**:
- [ ] All tests pass
- [ ] Coverage meets gate (≥80%)
- [ ] Changes <200 lines per commit (mostly)
- [ ] Error handling present
- [ ] Backward compatible verified
- [ ] No doom loops encountered

**Time Estimate**: 2-8 hours (varies by complexity)

**Next**: Proceed to Step 4 (if multi-agent needed) or Step 5

---

### Step 4: Multi-Agent Coordination (Optional)

For complex features requiring parallel development, coordinate multiple implementation agents.

**Purpose**: Parallelize independent work to save time

**When to Use**:
- Feature has multiple independent components
- Different agents can work on different modules
- Clear separation of concerns possible
- Time optimization important

**When to Skip**:
- Simple linear implementation
- Strong coupling between components
- Single developer workflow

**Inputs**:
- Implementation plan with parallel groups identified
- Clear boundaries between components

**Process**:

1. **Identify Parallel Opportunities** (from plan):
   ```markdown
   ## Parallel Groups (from multi-ai-planning)

   **Parallel Group 1** (after Task 1):
   - Task 2.1: Frontend authentication component
   - Task 2.2: Backend API endpoints
   - Task 2.3: Database migrations

   These can run simultaneously (independent).
   ```

2. **Spawn Parallel Implementation Agents** (Task tool):
   ```typescript
   // Coordinate multiple agents via Task tool

   const implementations = await Promise.all([
     task({
       description: "Implement frontend auth component",
       prompt: `Create React authentication component.

       Specifications:
       - Login form with email/password
       - Form validation
       - API integration hooks
       - Error handling

       Write to: src/components/Auth/LoginForm.tsx
       Write tests to: src/components/Auth/LoginForm.test.tsx

       Success criteria:
       - Component renders correctly
       - Validation works
       - Tests pass
       - Coverage ≥80%`
     }),

     task({
       description: "Implement backend API endpoints",
       prompt: `Create authentication API endpoints.

       Endpoints:
       - POST /api/auth/login
       - POST /api/auth/register
       - POST /api/auth/refresh

       Write to: src/api/auth.ts
       Write tests to: src/api/auth.test.ts

       Success criteria:
       - All endpoints functional
       - Tests pass
       - Coverage ≥80%`
     }),

     task({
       description: "Create database migrations",
       prompt: `Create database schema for authentication.

       Tables:
       - users (id, email, password_hash, created_at)
       - sessions (id, user_id, token, expires_at)

       Write migrations to: migrations/001_auth_schema.sql
       Write tests to: migrations/001_auth_schema.test.ts`
     })
   ]);

   // All three execute in parallel
   // Each has isolated context
   // Results returned when all complete
   ```

3. **Integrate Results**:
   ```markdown
   # Integration After Parallel Execution

   **Check Each Component**:
   - [ ] Frontend component complete and tested
   - [ ] Backend API complete and tested
   - [ ] Database migrations complete and tested

   **Integration Steps**:
   1. Verify all components built correctly
   2. Connect frontend → API
   3. Connect API → database
   4. Run integration tests
   5. Verify end-to-end workflow
   ```

4. **Handle Coordination Issues**:
   ```markdown
   ## Common Coordination Challenges

   **Issue**: Components don't integrate
   - **Cause**: Mismatched interfaces
   - **Fix**: Review specifications, align interfaces, re-implement

   **Issue**: Duplicate work
   - **Cause**: Overlapping agent responsibilities
   - **Fix**: Clearer task boundaries in plan

   **Issue**: Conflicting changes
   - **Cause**: Agents modifying same files
   - **Fix**: Use git worktrees for isolation
   ```

**Outputs**:
- Multiple components implemented in parallel
- All components tested independently
- Integration verified
- Time saved (20-40% faster than sequential)

**Validation**:
- [ ] All parallel tasks completed
- [ ] Each component tested independently
- [ ] Integration successful
- [ ] No conflicts or duplicate work
- [ ] Time savings achieved

**Time Estimate**: 2-6 hours (potentially 20-40% faster than sequential)

**Next**: Proceed to Step 5

---

### Step 5: Integration & End-to-End Testing

Integrate all components and verify complete workflows function correctly.

**Purpose**: Ensure components work together, catch integration issues

**Inputs**:
- Implemented code (from Step 3-4)
- Integration test strategy (from plan)

**Process**:

1. **Integration Testing**:

   **Generate Integration Tests** (use multi-ai-testing):
   ```
   Use multi-ai-testing test generation workflow for integration tests

   Components:
   - [List all components to integrate]

   Workflows to Test:
   - User registration → database → email confirmation
   - User login → token generation → API access
   - Token refresh → validation → new token

   Write tests to: tests/integration/auth-workflows.test.ts
   ```

2. **Execute Integration Tests**:
   ```bash
   # Run integration test suite
   npm test -- tests/integration/

   # Verify all workflows work
   # Fix any integration issues found
   ```

3. **End-to-End Testing**:
   ```markdown
   # E2E Test Scenarios

   **Scenario 1: Complete Registration Flow**
   1. User submits registration form
   2. API validates and creates user
   3. Database stores user record
   4. Email confirmation sent
   5. User confirms email
   6. User can log in

   **Scenario 2: Complete Login Flow**
   [Similar detailed steps]
   ```

   **Execute E2E Tests**:
   ```bash
   # Run E2E test suite
   npm run test:e2e

   # Or use multi-ai-testing
   Use multi-ai-testing for E2E testing of [workflows]
   ```

4. **Performance Validation**:
   ```bash
   # Run performance tests
   npm run test:performance

   # Check response times
   # Verify: <200ms for critical paths
   # Identify bottlenecks if any
   ```

5. **Backward Compatibility Check** (for changes to existing code):
   ```bash
   # Run full test suite (old + new tests)
   npm test

   # Verify: All existing tests still pass
   # Verify: No breaking changes
   # Verify: APIs backward compatible
   ```

**Outputs**:
- Integration tests passing
- E2E tests passing
- Performance validated
- Backward compatibility verified
- Integration issues resolved

**Validation**:
- [ ] Integration tests generated and passing
- [ ] E2E workflows verified
- [ ] Performance acceptable (<200ms or spec)
- [ ] No backward compatibility breaks
- [ ] All existing tests still pass

**Time Estimate**: 1-3 hours

**Next**: Proceed to Step 6

---

### Step 6: Quality Verification & Commit

Run final verification before committing, ensuring all quality gates pass.

**Purpose**: Multi-layer quality assurance before production

**Inputs**:
- Complete implementation (from Steps 3-5)
- All tests passing
- Plan verification criteria

**Process**:

1. **Run Multi-Layer Verification** (use multi-ai-verification):
   ```
   Use multi-ai-verification for complete quality check of [implementation]
   ```

   This runs all 5 verification layers:
   - Layer 1: Rules-based (linting, types, schema) - 95% automated
   - Layer 2: Functional (tests, coverage) - 60-80% automated
   - Layer 3: Visual (if UI) - 30-50% automated
   - Layer 4: Integration (E2E, system) - 20-30% automated
   - Layer 5: Quality scoring (0-100) - LLM-as-judge

2. **Review Verification Report**:
   ```markdown
   # Verification Results

   ## Layer 1: Rules ✅
   - Linting: PASS
   - Type checking: PASS
   - Schema validation: PASS

   ## Layer 2: Functional ✅
   - Tests: 95/95 passing
   - Coverage: 87% (≥80% gate)
   - Examples: All working

   ## Layer 3: Visual ✅ (if applicable)
   - Screenshots match mockups
   - Responsive design works

   ## Layer 4: Integration ✅
   - E2E tests pass
   - API integration verified

   ## Layer 5: Quality Score
   - **Total**: 92/100 ✅ (≥90 gate)
   - Correctness: 19/20
   - Functionality: 19/20
   - Quality: 18/20
   - Integration: 18/20
   - Security: 18/20

   **Status**: ALL GATES PASS ✅
   ```

3. **If Quality <90: Iterate**:
   ```markdown
   ## Gap Analysis (if score <90)

   **Issues Found**:
   1. [Issue 1] - Priority: High
      - Fix: [Specific action]
   2. [Issue 2] - Priority: Medium
      - Fix: [Action]

   **Action**: Apply fixes, re-verify
   **Target**: Reach ≥90/100
   ```

4. **Create Git Commit** (only if all gates pass):
   ```bash
   # Stage changes
   git add <files>

   # Commit with clear message
   git commit -m "feat: Add user authentication with OAuth

   - Implemented JWT token generation and validation
   - Added login/register API endpoints
   - Created database schema and migrations
   - Tests: 95/95 passing, coverage 87%
   - Quality score: 92/100

   Closes #123"
   ```

5. **Create Pull Request** (for team workflows):
   ```bash
   # Push branch
   git push -u origin feature/auth

   # Create PR
   gh pr create --title "Add user authentication" --body "$(cat <<EOF
   ## Summary
   Implements user authentication with OAuth support.

   ## Changes
   - Database schema for users and tokens
   - JWT token generation and validation
   - Login/register API endpoints
   - Frontend auth components

   ## Testing
   - Unit tests: 95/95 passing
   - Integration tests: 12/12 passing
   - Coverage: 87% (gate: ≥80%)
   - Quality score: 92/100

   ## Verification
   - ✅ All 5 verification layers pass
   - ✅ Security scan: No vulnerabilities
   - ✅ Backward compatible
   - ✅ Performance: <150ms avg response

   Ready for review.
   EOF
   )"
   ```

6. **Document Implementation**:
   ```markdown
   # Implementation Complete

   **What Was Built**:
   - [List of components]

   **Tests Added**:
   - [Test files and coverage]

   **Quality Metrics**:
   - Quality score: 92/100
   - Test coverage: 87%
   - Performance: <150ms

   **Next Steps**:
   - Code review by team
   - Deployment to staging
   - Production release
   ```

**Outputs**:
- Production-ready code
- All tests passing
- Coverage ≥80% (gate), ideally ≥95%
- Quality score ≥90/100
- Git commit(s) created
- PR created (if team workflow)
- Documentation updated

**Validation**:
- [ ] All 5 verification layers pass
- [ ] Quality score ≥90/100
- [ ] Test coverage ≥80%
- [ ] Git commit created
- [ ] PR created (if applicable)
- [ ] Documentation complete

**Time Estimate**: 30-90 minutes

**Result**: Production-ready, tested, verified implementation

---

## Integration with Other Skills

### With multi-ai-planning (Step 2)

**Usage**: Create implementation plan before coding

**Benefits**:
- Structured approach (not ad-hoc)
- Quality ≥90 plans
- Clear task breakdown
- Verification built-in

---

### With multi-ai-testing (Steps 3, 5)

**Usage**: TDD workflow, test generation, coverage validation

**Benefits**:
- Test-first development
- Independent verification prevents gaming
- 95% coverage achievable
- Self-healing tests

---

### With multi-ai-verification (Step 6)

**Usage**: Multi-layer quality assurance before commit

**Benefits**:
- 5-layer verification (automated → LLM-as-judge)
- Quality scoring (0-100)
- All gates must pass
- Actionable feedback

---

## Workflow Modes

### Standard Mode (Full Quality)

**Use For**: Features, refactorings, security changes, integrations

**Process**: All 6 steps with all 5 verification layers
**Time**: 5-15 hours
**Quality**: Maximum (all gates, score ≥90)

---

### Fast-Track Mode (Gemini Recommendation)

**Use For**: Typos, documentation, minor config tweaks

**Process**: Steps 1-3 + Layer 1-2 verification only
**Time**: 30-90 minutes
**Quality**: Essential checks only

**Usage**: Explicitly request "fast-track" or skip verification step

---

## Best Practices

### 1. Always Explore First (Step 1)
Never jump straight to coding. Context prevents errors.

### 2. Always Plan (Step 2)
Use multi-ai-planning for quality ≥90 plans.

### 3. Test-Driven Development (Step 3)
Tests first, then implementation. Prevents overfitting.

### 4. Small Increments (<200 Lines)
Prevents LLM degradation, enables easy rollback.

### 5. Continuous Testing
Run tests after each change, not just at end.

### 6. Independent Verification (Step 6)
Use multi-ai-verification for unbiased quality check.

---

## Common Mistakes

### Mistake 1: Skipping Exploration
**Problem**: Coding without understanding existing patterns
**Fix**: Always complete Step 1

### Mistake 2: No Plan
**Problem**: Ad-hoc implementation, rework needed
**Fix**: Always use multi-ai-planning (Step 2)

### Mistake 3: Large Monolithic Changes
**Problem**: >500 lines, hard to review, LLM quality degrades
**Fix**: Incremental commits (<200 lines)

### Mistake 4: Implementation-First (Not Test-First)
**Problem**: Tests fit to code (gaming)
**Fix**: Generate tests first in Step 3

### Mistake 5: Skipping Verification
**Problem**: Low-quality code reaches production
**Fix**: Always run multi-ai-verification (Step 6)

---

## Appendix A: Task Tool Coordination Patterns

### Pattern 1: Sequential Verification Agent

```typescript
// Implementation complete
const implResult = await task({
  description: "Implement authentication",
  prompt: `Implement user authentication.
  Write code to: src/auth/
  Write tests to: tests/auth/
  Write summary to: implementation-summary.json`
});

// Independent verification (separate agent)
const verification = await task({
  description: "Verify implementation independently",
  prompt: `Review implementation in src/auth/.

  Do NOT read previous conversation.
  Verify against success-criteria.json ONLY.

  Check:
  - All success criteria met
  - Tests pass
  - Code quality
  - Security

  Write report to: verification-report.md`
});

// Read verification results
const report = readFile('verification-report.md');
if (report.score >= 90) {
  // Approved for commit
} else {
  // Apply fixes from feedback
}
```

---

### Pattern 2: Parallel Component Implementation

```typescript
// Build multiple components in parallel

const [frontend, backend, database] = await Promise.all([
  task({
    description: "Build frontend component",
    prompt: "Create React auth component. Write to: src/components/Auth/"
  }),

  task({
    description: "Build backend API",
    prompt: "Create auth API endpoints. Write to: src/api/auth.ts"
  }),

  task({
    description: "Create database schema",
    prompt: "Create auth schema. Write to: migrations/"
  })
]);

// Integrate results after all complete
```

---

### Pattern 3: Shared State via Files

```typescript
// Agent 1: Research
await task({
  description: "Research OAuth patterns",
  prompt: "Research OAuth 2.0 implementation. Write findings to: research.md"
});

// Agent 2: Plan based on research
await task({
  description: "Create implementation plan",
  prompt: "Read research.md. Create detailed plan. Write to: plan.json"
});

// Agent 3: Implement based on plan
await task({
  description: "Implement OAuth",
  prompt: "Read plan.json. Implement OAuth. Write code to: src/oauth/"
});

// Pattern: Agent A → file → Agent B reads → next file
```

---

## Appendix B: Doom Loop Prevention

### Detection Patterns

**Oscillating Errors**:
```
Attempt 1: Fix error A → Test B fails
Attempt 2: Fix error B → Test A fails
Attempt 3: Fix error A → Test B fails again
↓
DOOM LOOP DETECTED → Escalate to human
```

**Same Error Repeatedly**:
```
Attempt 1: Error: "undefined userId"
Attempt 2: Error: "undefined userId" (same fix tried)
Attempt 3: Error: "undefined userId" (stuck)
↓
ESCALATE → Human needed
```

### Breaker Implementation

```python
MAX_RETRIES = 3
error_history = []

for attempt in range(MAX_RETRIES):
    result = implement_and_test()

    if result.success:
        break

    error_history.append(result.error)

    # Detect doom loop
    if attempt >= 2:
        # Same error 3 times?
        if error_history[0] == error_history[1] == error_history[2]:
            escalate_to_human("Same error 3x:", error_history[0])
            break

        # Oscillating?
        if error_history[0] == error_history[2] and error_history[1] != error_history[0]:
            escalate_to_human("Oscillating errors:", error_history)
            break

    # Continue trying
```

---

## Appendix C: Technical Foundation

### Orchestration Runtime
- **Development**: Claude Code Task tool
- **CI/CD**: GitHub Actions
- **Data Contracts**: JSON schemas (in schemas/)
- **Artifact Storage**: File system (.implementations/)

### Tooling Per Language

**JavaScript/TypeScript**:
- Linter: ESLint
- Type checker: TypeScript compiler (tsc)
- Test framework: Jest or Vitest
- Coverage: c8 or nyc
- SAST: Semgrep or eslint-plugin-security

**Python**:
- Linter: Pylint/Ruff
- Type checker: mypy
- Test framework: pytest
- Coverage: pytest-cov
- SAST: Bandit

### Rollback Strategy
- **Code**: Git tags + git worktree (NOT git reset)
- **Database**: Migration down scripts
- **Feature flags**: Gradual rollout with kill switch

### Cost/Latency Controls
- **Budget**: $50/month cap for LLM-as-judge
- **Caching**: Cache verification results for 24h
- **Fast-path**: Skip Layer 5 for changes <50 lines

---

## Quick Reference

### The 6-Step Workflow

| Step | Purpose | Time | Tools Used |
|------|---------|------|------------|
| 1 | Explore & Context | 30-60m | Glob, Grep, Read, Research |
| 2 | Plan Architecture | 30-90m | multi-ai-planning |
| 3 | Implement (TDD) | 2-8h | multi-ai-testing, Write, Edit |
| 4 | Coordinate (optional) | 2-6h | Task tool (parallel) |
| 5 | Integrate & E2E | 1-3h | multi-ai-testing (integration) |
| 6 | Verify & Commit | 30-90m | multi-ai-verification, Git |

**Total**: 5-15 hours (standard mode) or 30-90 min (fast-track)

### Quality Metrics

- **Test Coverage**: ≥80% gate, ≥95% target
- **Quality Score**: ≥90/100 required
- **Change Size**: <200 lines per commit ideal
- **Verification Layers**: All 5 must pass
- **Performance**: Meets specification

---

**multi-ai-implementation delivers production-ready code through systematic Explore-Plan-Code-Commit workflow with TDD, multi-agent coordination, and rigorous quality gates - validated by Claude + Gemini + Codex research.**

For examples, see examples/. For coordination patterns, see Appendix A.
