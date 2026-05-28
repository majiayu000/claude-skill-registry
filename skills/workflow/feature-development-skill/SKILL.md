---
name: feature-development
category: workflow
version: 2.0.0
description: End-to-end workflow for developing features from spec to PR (Australian-enhanced)
author: Unite Group
priority: 3
triggers:
  - feature
  - new feature
  - implement feature
  - add functionality
requires:
  - verification/verification-first.skill.md
  - verification/error-handling.skill.md
  - design/foundation-first.skill.md
  - australian/australian-context.skill.md
---

# Feature Development Workflow

## Purpose

Guide agents through the complete feature development lifecycle: from specification to production-ready code with Australian context.

## Workflow Phases

### Phase 1: Requirements Analysis

**Objective**: Understand what needs to be built

```markdown
1. Parse User Story/Spec
   - Extract acceptance criteria
   - Identify edge cases
   - Note constraints
   - Apply Australian context (en-AU, regulations)

2. Query Memory
   - Search for similar features
   - Load relevant patterns
   - Check failure patterns to avoid

3. Clarify Ambiguities
   - Ask questions if unclear
   - Confirm assumptions
   - Document decisions
```

**Outputs**:
- Clear understanding of requirements
- List of acceptance criteria
- Known constraints and assumptions
- Australian context requirements (en-AU, dates, currency)

### Phase 2: Design Approach

**Objective**: Plan the implementation

```markdown
1. Architecture Decision
   - Which layer(s) affected? (frontend/backend/database)
   - Existing patterns to follow?
   - New components needed?
   - Design system compliance (2025-2026 aesthetic, NO Lucide icons)

2. File Planning
   - Files to create
   - Files to modify
   - Dependencies to add

3. Test Strategy
   - Unit tests needed
   - Integration tests needed
   - E2E tests needed
   - Test data requirements
   - Australian context testing (dates, currency, phone)

4. Break Into Subtasks
   - Database schema (if needed)
   - Backend API (if needed)
   - Frontend UI (if needed)
   - Tests
   - Documentation
```

**Outputs**:
- Implementation plan
- List of files to touch
- Test strategy
- Dependency changes
- Design system compliance checklist

### Phase 3: Implementation

**Objective**: Build the feature following TDD

```markdown
For each component (database → backend → frontend):

  1. Write Failing Test
     - Define expected behavior
     - Write test that fails
     - Commit test

  2. Implement Feature
     - Minimal code to pass test
     - Follow project patterns
     - Handle errors properly
     - Apply Australian context (en-AU, DD/MM/YYYY, AUD)

  3. Refactor
     - Improve code quality
     - Remove duplication
     - Add documentation
     - Verify design system compliance

  4. Verify
     - Tests pass
     - Type check passes
     - Lint passes
     - Australian context validated

  5. Self-Review
     - Check completeness
     - Verify edge cases
     - Ensure quality
```

**Implementation Order**:
1. **Database**: Create migrations if schema changes needed
2. **Backend**: Implement API endpoints/business logic
3. **Frontend**: Build UI components
4. **Integration**: Wire everything together
5. **Tests**: Ensure comprehensive coverage

### Phase 4: Testing & Verification

**Objective**: Prove the feature works

```markdown
1. Unit Tests
   - All new functions tested
   - Edge cases covered
   - Error cases handled
   - Run: `pnpm test` or `pytest`

2. Integration Tests
   - Components work together
   - API endpoints respond correctly
   - Database operations succeed
   - Run: Integration test suite

3. E2E Tests (if applicable)
   - User flow works end-to-end
   - UI interactions work
   - Run: `pnpm test:e2e`

4. Manual Verification
   - Start dev server
   - Test feature manually
   - Check edge cases
   - Verify UX is good
   - Verify Australian context (dates display as DD/MM/YYYY, currency as AUD)

5. Independent Verification
   - Submit to verification agent
   - Collect evidence
   - Address any failures

6. Design System Verification
   - NO Lucide icons used
   - Design tokens followed
   - 2025-2026 aesthetic applied
   - Bento grid layout (if applicable)
```

**Verification Checklist**:
- [ ] All tests passing
- [ ] Type check passing
- [ ] Lint passing
- [ ] Feature works manually
- [ ] No regressions
- [ ] Performance acceptable
- [ ] Australian context validated (en-AU, DD/MM/YYYY, AUD)
- [ ] Design system compliance (NO Lucide icons)
- [ ] WCAG 2.1 AA compliance

### Phase 5: Documentation

**Objective**: Document the feature

```markdown
1. Code Documentation
   - Docstrings on functions
   - Complex logic has comments
   - Type hints present
   - Australian context noted (e.g., "Date format: DD/MM/YYYY")

2. API Documentation
   - Endpoint descriptions
   - Request/response examples (using Australian data)
   - Error codes documented

3. User Documentation (if needed)
   - README updated
   - Usage examples (Australian context)
   - Migration guide (if breaking)

4. Memory Storage
   - Store successful patterns
   - Document design decisions
   - Record learnings
```

### Phase 6: PR Creation

**Objective**: Create PR for human review

```markdown
1. Create Feature Branch
   - Branch name: `feature/agent-{task-id}`
   - Based on main

2. Commit Changes
   - Descriptive commit message
   - Include co-author line
   - Link to task/issue

3. Run All Checks
   - `pnpm turbo run type-check lint test`
   - All must pass

4. Generate PR Description
   - Summary of changes
   - Test plan
   - Verification evidence
   - Australian context compliance notes
   - Design system compliance notes
   - Agent metadata

5. Create PR
   - Request reviewers
   - Link to task tracker
```

## Example: Adding Invoice Feature (Australian)

### Phase 1: Requirements
```
Feature: Add invoice generation

Acceptance Criteria:
- Generate invoices with ABN
- Display amounts in AUD
- Dates in DD/MM/YYYY format
- Include GST (10%) calculation
- Comply with Australian tax invoice requirements
```

### Phase 2: Design
```
Components Needed:
- Database: invoices table with ABN field
- Backend: /api/invoices endpoint
- Frontend: InvoiceGenerator component (Bento grid, NO Lucide)
- Validation: ABN validation, AUD formatting

Tests:
- Unit: ABN validation function
- Integration: Invoice creation endpoint
- E2E: Full invoice generation flow
```

### Phase 3: Implementation
```
Order:
1. Database: Add invoices table with australian_business_number field
2. Backend: Implement invoice generation with GST calculation
3. Frontend: Create InvoiceGenerator component (2025-2026 aesthetic)
4. Validation: Add ABN validation, date formatting (DD/MM/YYYY)
```

### Phase 4: Testing
```
✅ pytest tests/test_invoices.py - Passed (5/5)
✅ pnpm test --filter=web - Passed (8/8)
✅ pnpm test:e2e - Passed (2/2)
✅ Manual test: Generate invoice with ABN - Works
✅ Date displays as DD/MM/YYYY - Correct
✅ Currency displays as AUD - Correct
✅ GST calculation (10%) - Correct
✅ Independent verification - Passed
```

### Phase 5: Documentation
```
Updated:
- README: Added invoice generation section
- API docs: Documented /api/invoices endpoint
- Code: Added docstrings noting Australian requirements

Stored to Memory:
- Pattern: Australian invoice generation
- Decision: ABN validation using checksum algorithm
```

### Phase 6: PR
```
Created: PR #89 - "feat(invoices): Add Australian invoice generation"
Status: Awaiting human review
Checks: All passing ✅
```

## Key Principles

1. **TDD First**: Write failing tests before implementation
2. **Incremental**: Build in small, testable pieces
3. **Verify Continuously**: Test after each change
4. **Self-Correct**: Iterate if issues found
5. **Document**: Update docs as you go
6. **Learn**: Store patterns for future use
7. **Australian-First**: en-AU defaults everywhere
8. **Design System**: Follow locked tokens (NO Lucide icons)

## Common Pitfalls

❌ **Building everything then testing**
✅ **Test-driven: Test → Code → Refactor**

❌ **Skipping edge cases**
✅ **Cover edge cases in tests**

❌ **Forgetting error handling**
✅ **Handle errors explicitly (en-AU messages)**

❌ **No performance consideration**
✅ **Think about scale and performance**

❌ **Missing documentation**
✅ **Document as you build**

❌ **Using US date formats**
✅ **Always DD/MM/YYYY for Australian market**

❌ **Using Lucide icons**
✅ **AI-generated custom icons only (2025-2026 aesthetic)**

## Integration with Orchestrator

```python
async def develop_feature(orchestrator, spec):
    # Phase 1: Analyze
    requirements = await orchestrator.analyze_requirements(spec)

    # Load Australian context
    australian_context = await orchestrator.load_australian_context()

    # Phase 2: Design
    plan = await orchestrator.design_approach(requirements, australian_context)

    # Phase 3: Implement (parallel if possible)
    if plan.has_database_changes:
        db_agent = await orchestrator.spawn_subagent("database", plan.db_tasks)

    if plan.has_backend_changes:
        backend_agent = await orchestrator.spawn_subagent("backend", plan.backend_tasks)

    if plan.has_frontend_changes:
        frontend_agent = await orchestrator.spawn_subagent("frontend", plan.frontend_tasks)

    # Wait for all agents
    results = await orchestrator.collect_results([db_agent, backend_agent, frontend_agent])

    # Phase 4: Test & Verify
    test_agent = await orchestrator.spawn_subagent("test", results)
    verification = await orchestrator.verify_independently(test_agent.output)

    # Verify Australian context
    au_verification = await orchestrator.verify_australian_context(results)

    # Verify design system compliance
    design_verification = await orchestrator.verify_design_system(results)

    # Phase 5: Document
    await orchestrator.generate_documentation(results, australian_context)

    # Phase 6: Create PR
    pr = await orchestrator.create_pr(results, verification, au_verification, design_verification)

    return pr
```

---

**Goal**: Deliver production-ready features with tests, documentation, Australian context, and design system compliance.
