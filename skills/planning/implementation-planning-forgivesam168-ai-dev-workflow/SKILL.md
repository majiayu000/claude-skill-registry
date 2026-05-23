---
name: implementation-planning
description: 'Break down specifications into executable implementation plans with TDD integration. Use when asked to "create plan", "break down tasks", "implementation roadmap", "規劃實作", "拆解任務", "執行計畫", or need step-by-step implementation guidance with test strategies and impact analysis.'
license: See LICENSE.txt in repository root
---

# Implementation Planning

> 💡 **Recommended Agent**: `plan-agent` (Strategic Planner)
> - **CLI**: Input `/agent` and select `plan-agent`
> - **VS Code**: Use `@workspace #plan-agent` in Chat
>
> **⚠️ CLI Note**: In CLI, use natural language like "規劃實作計畫". VS Code users can use `/create-plan` shortcut.

## When to Use This Skill

Use this skill when:
- Spec is complete and ready for implementation breakdown
- Need to divide feature into manageable tasks
- Want TDD-integrated task planning
- Need impact analysis for brownfield changes
- 規格文件完成,要開始拆解實作任務
- 需要評估變更對現有系統的影響

## Prerequisites

**Required**:
- `03-spec.md` with clear requirements and acceptance criteria

**Recommended**:
- `01-brainstorm.md` for context and chosen approach
- `02-decision-log.md` for architectural decisions

## Step-by-Step Workflow

### Step 1: Requirements Review

Review the spec and confirm:
1. **Goals** are clear
2. **User stories** have acceptance criteria
3. **Technical requirements** are defined
4. **Dependencies** are identified

### Step 2: Task Breakdown

Break down implementation into phases:

#### Phase Structure
Each phase should:
- Be independently testable
- Take 2-4 hours max (break larger tasks)
- Include clear entry/exit criteria
- Specify test strategy

#### Example Breakdown
```
Phase 1: Data Model & Database
Phase 2: Core Business Logic
Phase 3: API Layer
Phase 4: Frontend Integration
Phase 5: E2E Testing & Polish
```

### Step 3: TDD Integration

For each task, specify:
1. **Test First**: What tests to write
2. **Implementation**: Minimal code to pass
3. **Refactor**: Cleanup and optimization
4. **Verification**: How to confirm completion

### Step 4: Impact Analysis (Brownfield)

If modifying existing system:
1. **Affected Components**: Which files/modules change
2. **Breaking Changes**: API/schema changes
3. **Migration Requirements**: Data migration needs
4. **Rollback Strategy**: How to revert if needed

### Step 5: Generate Plan Document

Create `changes/<YYYY-MM-DD>-<slug>/04-plan.md`:

---

**Template**:

```markdown
# Implementation Plan: {Feature Name}

## Overview
{Brief summary of what will be implemented}

**Spec Reference**: `03-spec.md`

## Implementation Strategy

### Approach
{High-level approach: e.g., "Bottom-up: DB → Logic → API → UI"}

### Phases
{Number of phases: e.g., "5 phases, estimated 16-20 hours total"}

---

## Phase 1: {Phase Name}

### Objective
{What this phase accomplishes}

### Tasks

#### Task 1.1: {Task Name}
**Test Strategy** (RED):
- Write test: `{test file path}`
- Test case: {What the test validates}
- Expected failure: {Why it should fail initially}

**Implementation** (GREEN):
- File: `{implementation file path}`
- Changes: {Brief description}
- Minimal code to pass test

**Refactor** (REFACTOR):
- Extract common logic
- Improve naming
- Remove duplication

**Acceptance Criteria**:
- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] Test coverage ≥80%

**Estimated Time**: {X hours}

---

#### Task 1.2: {Task Name}
{Repeat structure}

---

### Phase 1 Exit Criteria
- [ ] All Phase 1 tests passing
- [ ] Code reviewed and refactored
- [ ] Coverage ≥80%
- [ ] No blocking issues

---

## Phase 2: {Phase Name}
{Repeat phase structure}

---

## Dependencies

### External
- {Dependency 1: e.g., "Redis for job queue"}
- {Dependency 2: e.g., "SendGrid API key for email"}

### Internal
- {Dependency 1: e.g., "User authentication must be complete"}
- {Dependency 2: e.g., "Database migration #123 deployed"}

### Sequencing
- Phase 1 must complete before Phase 2
- Phase 3 and Phase 4 can run in parallel

---

## Impact Analysis (Brownfield Changes)

### Affected Components
| Component | Type | Impact Level | Action Required |
|-----------|------|--------------|-----------------|
| `lib/users.ts` | Modified | Medium | Update user model |
| `api/v1/users` | Modified | High | Breaking change (version bump) |
| `components/UserProfile` | Modified | Low | Update props |
| `tests/users.test.ts` | Modified | Medium | Add new test cases |

### Breaking Changes
- ⚠️ API: `/api/v1/users` response schema adds `notificationPreferences` field
  - **Impact**: External clients may break if they validate strict schemas
  - **Migration**: Announce 2 weeks before, provide migration guide
  - **Rollback**: Deploy v1 and v2 endpoints in parallel during transition

### Data Migration
**Required**: Yes
- **Script**: `migrations/2024-01-30-add-notification-prefs.sql`
- **Rollback**: `migrations/2024-01-30-add-notification-prefs-down.sql`
- **Test**: Run on staging first
- **Estimated time**: 30 seconds (10k rows)

### Rollback Strategy
1. Database: Run down migration
2. Code: Deploy previous git commit
3. Feature flag: Disable `notifications_enabled` flag
4. Verify: Check health endpoints and logs

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Email deliverability issues | Medium | High | Configure SPF/DKIM, use reputable service |
| Performance degradation | Low | High | Load test with 10x expected traffic |
| Notification spam | Medium | Medium | Rate limiting, user preferences |

---

## Testing Strategy

### Unit Tests
- All business logic functions
- Target: 80%+ coverage
- Tools: Jest/Vitest

### Integration Tests
- API endpoints
- Database operations
- External service mocks

### E2E Tests
- Critical user flows only
- Tools: Playwright
- Run on: Staging environment

### Performance Tests (if needed)
- Load: {X requests/second}
- Duration: {Y minutes}
- Tool: k6/Artillery

---

## Estimated Timeline

| Phase | Tasks | Estimated Time | Dependencies |
|-------|-------|---------------|--------------|
| Phase 1 | 3 tasks | 4-6 hours | None |
| Phase 2 | 4 tasks | 5-7 hours | Phase 1 complete |
| Phase 3 | 2 tasks | 3-4 hours | Phase 2 complete |
| Phase 4 | 3 tasks | 4-5 hours | Phase 3 complete |
| **Total** | **12 tasks** | **16-22 hours** | Sequential |

---

## Approval & Next Steps

**Plan Status**: ⏳ Awaiting Approval

**Approval Checklist**:
- [ ] All phases reviewed
- [ ] Risks acceptable
- [ ] Timeline reasonable
- [ ] Dependencies available
- [ ] Impact analysis complete (if brownfield)

**Next Step After Approval**:
→ Start Phase 1 with TDD: "開始 TDD 實作"
→ Or use workflow orchestrator: "what's next?"
```

---

## Quality Criteria

**Must Have**:
- ✅ Each task has TDD strategy (Red-Green-Refactor)
- ✅ Acceptance criteria are testable
- ✅ Dependencies identified
- ✅ Estimated timeline provided
- ✅ Impact analysis (if brownfield)

**Financial Systems Must Have**:
- ✅ Money handling tasks specify precision (no floats)
- ✅ Transaction tasks include idempotency plan
- ✅ Audit logging tasks defined

**Nice to Have**:
- Sequence diagrams for complex flows
- Risk matrix visualization
- Automated dependency checks

## Next Step

After plan approval:

**CLI**:
```
Input: "開始 TDD 實作"
[System loads tdd-workflow skill]
→ /agent → Select coder-agent
→ Follow Red-Green-Refactor cycle
```

**VS Code**:
```
Input: /tdd
Or: "start TDD implementation"
```

Or use workflow orchestrator:
```
Input: "what's next?"
[System detects plan complete, recommends TDD stage]
```

## Troubleshooting

### "The tasks are too large"
**Solution**: Break down further. Each task should take 2-4 hours max. Use sub-tasks if needed.

### "I don't know the estimate"
**Solution**: Use t-shirt sizing (S/M/L/XL) or Fibonacci (1/2/3/5/8). Refine after Phase 1.

### "Should I include ALL edge cases?"
**Solution**: Include critical edge cases in initial plan. Document "known limitations" for non-critical ones to address later.

### "How detailed should test strategy be?"
**Solution**: 
- Specify **what** to test (behavior, not implementation)
- Name the test file
- List key test cases
- Don't write full test code yet (that's in TDD phase)

## Financial Systems Best Practices

### Task Breakdown Example
```
Task 3.2: Implement Transaction Creation Endpoint
Test Strategy:
- Test happy path: valid transaction with idempotency key
- Test duplicate idempotency key returns 409 Conflict
- Test invalid amount (negative, zero) returns 422
- Test money precision: decimal with 4 places

Implementation:
- Use decimal for amount (NOT float)
- Store currency as string (ISO 4217)
- Implement idempotency-key check
- Log all transaction events for audit

Refactor:
- Extract amount validation to shared utility
- Use money value object pattern
```

## Related Documentation

- [Specification Skill](../specification/SKILL.md) - Previous stage
- [TDD Workflow Skill](../tdd-workflow/SKILL.md) - Next stage
- [WORKFLOW.md](../../WORKFLOW.md) - Overall workflow
- [TDD Guide](../../instructions/playbooks/tdd-guide.md) - TDD methodology

---

💡 **Tip**: A good plan is detailed enough to start implementation without confusion, but flexible enough to adapt when reality diverges from expectations.
