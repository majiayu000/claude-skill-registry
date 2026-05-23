---
name: unify
description: Validate spec-implementation-test alignment and convergence. Checks spec completeness, implementation conformance, test coverage, and contract consistency. Use after implementation and tests are complete.
allowed-tools: Read, Glob, Grep, Bash, Task
---

# Unify Skill

## Purpose
Validate that implementation and tests conform to the spec. Ensure convergence before approval and merge.

## Convergence Criteria

A task is **converged** when:
1. **Spec is complete** - All required sections present, open questions resolved
2. **Implementation aligns** - Code matches spec requirements exactly
3. **Tests pass** - All tests passing, coverage adequate
4. **Contracts valid** - (For MasterSpec) Contracts consistent across workstreams

If any criterion fails → Task is **not converged** → Iteration needed.

## Validation Process

### Step 1: Load Spec
```bash
cat .claude/specs/active/<slug>.md
```

Read:
- Acceptance criteria
- Requirements (EARS format)
- Task list
- Test plan
- Decision & Work Log

### Step 2: Spec Completeness Check

#### For TaskSpec
Verify:
- [ ] Context and Goal present
- [ ] Requirements in EARS format
- [ ] Acceptance criteria are testable
- [ ] Design notes (if non-trivial)
- [ ] Task list with clear outcomes
- [ ] Test plan maps ACs to tests
- [ ] Decision & Work Log has approval entry
- [ ] No unresolved blocking open questions

#### For WorkstreamSpec
Verify all sections from template:
- [ ] Context, Goals/Non-goals
- [ ] Atomic testable requirements
- [ ] Core flows documented
- [ ] At least one sequence diagram
- [ ] Edge cases identified
- [ ] Interfaces & data model defined
- [ ] Security considerations addressed
- [ ] Task list with dependencies
- [ ] Testing strategy defined
- [ ] Open questions resolved or deferred
- [ ] Decision & Work Log complete

#### For MasterSpec
Verify:
- [ ] All workstream specs linked
- [ ] Contract registry complete
- [ ] Dependency graph is acyclic
- [ ] No cross-workstream conflicts
- [ ] All gates passed

**Output**: Spec completeness report

```markdown
## Spec Completeness: ✅ Pass

- All required sections present
- 4 acceptance criteria defined (all testable)
- 6 tasks in task list (all completed)
- No blocking open questions
- Approval recorded: 2026-01-02
```

### Step 3: Implementation Alignment Check

Verify implementation matches spec requirements.

#### Approach
For each requirement/AC:
1. Identify implementation location (from task list evidence)
2. Read implementation code
3. Verify behavior matches spec
4. Check error handling matches spec edge cases

```bash
# Find implemented files
grep -r "logout" src/ --include="*.ts" -l

# Read implementation
cat src/services/auth-service.ts
```

#### Alignment Checklist
- [ ] All requirements have corresponding implementation
- [ ] Interfaces match spec definitions
- [ ] Error handling matches spec edge cases
- [ ] No undocumented functionality (features not in spec)
- [ ] Data models match spec
- [ ] API contracts match spec

**Output**: Implementation alignment report

```markdown
## Implementation Alignment: ✅ Pass

- AC1.1: ✅ Token cleared in AuthService.logout():42
- AC1.2: ✅ Redirect to /login in Router.onAuthChange():58
- AC1.3: ✅ Toast shown in UserMenu.handleLogout():31
- AC2.1: ✅ Error handling in AuthService.logout():47

**No undocumented features detected**
```

#### Common Misalignments

**Extra features**:
```markdown
❌ Found feature not in spec:
  - File: src/services/auth-service.ts:65
  - Feature: Auto-retry on network failure
  - **Action**: Remove or add to spec and get approval
```

**Missing requirements**:
```markdown
❌ Requirement AC2.3 not implemented:
  - AC2.3: Retry button appears on error
  - **Action**: Implement missing requirement
```

**Behavioral deviation**:
```markdown
❌ Behavior differs from spec:
  - Spec: "redirect to /login"
  - Implementation: "redirect to /login?error=logged_out"
  - **Action**: Match spec exactly or propose amendment
```

### Step 4: Test Coverage Check

Verify tests cover all acceptance criteria and pass.

```bash
# Run tests
npm test

# Check coverage
npm test -- --coverage
```

#### Coverage Checklist
- [ ] Every acceptance criterion has at least one test
- [ ] Tests verify spec requirements (not implementation details)
- [ ] All tests passing
- [ ] No flaky tests (run 3x to confirm)
- [ ] Coverage meets standards (typically 80%+)

**Output**: Test coverage report

```markdown
## Test Coverage: ✅ Pass

| AC | Test | Status |
|----|------|--------|
| AC1.1 | auth-service.test.ts:12 | ✅ Pass |
| AC1.2 | auth-router.test.ts:24 | ✅ Pass |
| AC1.3 | user-menu.test.ts:35 | ✅ Pass |
| AC2.1 | auth-service.test.ts:28 | ✅ Pass |

**Coverage**: 12 tests total, 100% AC coverage, 94% line coverage
```

#### Common Coverage Issues

**Missing test**:
```markdown
❌ AC2.3 has no test:
  - AC2.3: Retry button appears on error
  - **Action**: Add test in user-menu.test.ts
```

**Failing test**:
```markdown
❌ Test failing:
  - Test: auth-service.test.ts:28
  - Error: Expected null, got "test-token"
  - **Action**: Fix implementation or fix test
```

**Low coverage**:
```markdown
⚠️  Coverage below standard:
  - Current: 72% line coverage
  - Required: 80%
  - **Action**: Add tests for uncovered branches
```

### Step 5: Contract Validation (MasterSpec Only)

For multi-workstream efforts, validate contracts.

```bash
# Load MasterSpec
cat .claude/specs/active/<slug>/master.md

# Check contract registry
grep -A 5 "^## Contract Registry" .claude/specs/active/<slug>/master.md
```

#### Contract Checklist
- [ ] All contracts registered in registry
- [ ] No duplicate contract IDs
- [ ] Contract owners match workstreams
- [ ] Contract versions consistent
- [ ] Implementations match contract interfaces

**Output**: Contract validation report

```markdown
## Contract Validation: ✅ Pass

| Contract ID | Owner | Implementation | Status |
|-------------|-------|----------------|--------|
| contract-websocket-api | ws-1 | src/websocket/server.ts | ✅ Match |
| contract-notification-api | ws-3 | src/services/notifications.ts | ✅ Match |

**No conflicts detected**
```

#### Common Contract Issues

**Interface mismatch**:
```markdown
❌ Contract implementation mismatch:
  - Contract: contract-websocket-api (ws-1)
  - Expected: `connect(userId: string): Promise<WebSocket>`
  - Found: `connect(userId: number): Promise<WebSocket>`
  - **Action**: Fix implementation to match contract or update contract
```

**Dependency cycle**:
```markdown
❌ Dependency cycle detected:
  - ws-1 depends on ws-2
  - ws-2 depends on ws-3
  - ws-3 depends on ws-1
  - **Action**: Restructure to break cycle
```

### Step 6: Generate Convergence Report

Aggregate all checks into single convergence report.

```markdown
# Convergence Report: <Task Name>

**Date**: 2026-01-02 16:30
**Spec**: .claude/specs/active/logout-button.md

## Summary: ✅ CONVERGED

All validation checks passed. Ready for approval and merge.

---

## Validation Results

### Spec Completeness: ✅ Pass
- All required sections present
- 4 acceptance criteria (all testable)
- 6 tasks completed
- No blocking open questions
- Approval: 2026-01-02

### Implementation Alignment: ✅ Pass
- All 4 ACs implemented correctly
- No undocumented features
- Error handling matches spec
- Interfaces match spec definitions

### Test Coverage: ✅ Pass
- 12 tests total
- 100% AC coverage
- All tests passing
- 94% line coverage

### Overall Status: CONVERGED ✅

**Next Steps**:
1. Run security review (if applicable)
2. Run browser tests (if UI changes)
3. Propose commit

---

## Evidence

**Implementation files**:
- src/services/auth-service.ts (logout method)
- src/components/UserMenu.tsx (logout button)
- src/router/auth-router.ts (redirect logic)

**Test files**:
- src/services/__tests__/auth-service.test.ts (4 tests)
- src/components/__tests__/user-menu.test.ts (3 tests)
- src/router/__tests__/auth-router.test.ts (2 tests)
- tests/integration/logout-flow.test.ts (3 tests)

**Test run**:
```
PASS  src/services/__tests__/auth-service.test.ts
PASS  src/components/__tests__/user-menu.test.ts
PASS  src/router/__tests__/auth-router.test.ts
PASS  tests/integration/logout-flow.test.ts

Tests: 12 passed, 12 total
Coverage: 94% statements, 92% branches, 96% functions, 95% lines
```
```

### Step 7: Handle Non-Convergence

If validation fails, identify specific gaps and recommend iterations.

```markdown
# Convergence Report: <Task Name>

## Summary: ❌ NOT CONVERGED

Issues found in implementation alignment and test coverage.

---

## Issues

### Issue 1: Missing Implementation (Priority: High)
- **AC2.3**: Retry button appears on error
- **Status**: Not implemented
- **Action**: Implement retry button in UserMenu component

### Issue 2: Test Failing (Priority: High)
- **Test**: auth-service.test.ts:28
- **Error**: Expected null, got "test-token"
- **Action**: Fix token clearing logic in AuthService.logout()

### Issue 3: Low Coverage (Priority: Medium)
- **Current**: 72% line coverage
- **Required**: 80%
- **Action**: Add tests for error paths

---

## Recommendations

1. **Iteration 1**: Implement AC2.3 retry button
2. **Iteration 2**: Fix token clearing bug
3. **Iteration 3**: Add error path tests

**Estimated effort**: 1-2 hours

After fixes, re-run unifier to validate convergence.
```

### Step 8: Iteration Loop

If not converged, route to appropriate fix:

```javascript
// Spec gap → Update spec
if (issue.type === "spec_gap") {
  useSkill("/spec"); // Amend spec with user approval
}

// Implementation bug → Fix implementation
if (issue.type === "impl_bug") {
  useSkill("/implement"); // Fix and re-test
}

// Missing test → Add test
if (issue.type === "missing_test") {
  useSkill("/test"); // Write missing test
}

// Re-validate
useSkill("/unify"); // Run convergence check again
```

**Iteration cap**: Maximum 3 iterations before escalating to user.

## Convergence Gates

### TaskSpec Gates
- [ ] Spec complete and approved
- [ ] All ACs implemented
- [ ] All tests passing
- [ ] Coverage ≥ 80%
- [ ] No undocumented features

### WorkstreamSpec Gates
All TaskSpec gates plus:
- [ ] Sequence diagrams match implementation
- [ ] Interfaces defined and implemented
- [ ] Security considerations addressed
- [ ] Workstream reflection complete

### MasterSpec Gates
All WorkstreamSpec gates plus:
- [ ] All workstream specs converged
- [ ] Contract registry validated
- [ ] No cross-workstream conflicts
- [ ] Dependency graph acyclic
- [ ] Integration tests passing

## Integration with Other Skills

After convergence, the review chain is:
1. `/code-review` - Code quality review (always)
2. `/security` - Security review (always)
3. `/browser-test` - UI validation (if UI changes)
4. `/docs` - Documentation generation (if public API)
5. Commit

**Next step after unify passes**: Dispatch `/code-review`

If not converged:
- Use `/spec`, `/implement`, or `/test` to address gaps
- Re-run `/unify` after fixes

## Examples

### Example 1: Converged TaskSpec

**Input**: TaskSpec for logout button (all ACs implemented, tests passing)

**Unifier Process**:
1. Spec completeness: ✅ All sections present
2. Implementation alignment: ✅ All 4 ACs implemented
3. Test coverage: ✅ 12 tests, all passing, 94% coverage

**Output**: CONVERGED ✅ - Ready for security review

### Example 2: Non-Converged WorkstreamSpec

**Input**: WorkstreamSpec for WebSocket server (missing edge case test)

**Unifier Process**:
1. Spec completeness: ✅ Pass
2. Implementation alignment: ✅ Pass
3. Test coverage: ❌ Fail - No test for connection timeout edge case

**Output**:
```markdown
❌ NOT CONVERGED

**Issue**: Missing test for connection timeout (Edge Case #3)
**Action**: Add test in websocket-server.test.ts
**Iteration 1**: Write timeout test
```

After test added → Re-run unifier → CONVERGED ✅

### Example 3: MasterSpec Contract Conflict

**Input**: MasterSpec with 3 workstreams

**Unifier Process**:
1. Spec completeness: ✅ Pass
2. Implementation alignment: ✅ Pass (per-workstream)
3. Test coverage: ✅ Pass
4. Contract validation: ❌ Fail - Interface mismatch between ws-1 and ws-2

**Output**:
```markdown
❌ NOT CONVERGED

**Issue**: Contract interface mismatch
  - ws-1 implements: `send(data: Buffer)`
  - ws-2 expects: `send(data: string)`

**Action**: Update ws-1 to match contract or amend contract
**Iteration 1**: Fix interface to accept string
```

After fix → Re-run unifier → CONVERGED ✅
