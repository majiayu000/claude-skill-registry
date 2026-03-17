---
name: workflow-feature
description: Complete feature development workflow from design to deployment. Use when implementing new features or functionality.
---

# Feature Development Workflow

Complete workflow for developing new features from design to deployment.

## Phases

### 1. Architecture Design
**Define:**
- Component structure
- Data models
- API contracts
- Integration points
- Dependencies

**Output:** Architecture diagram, component list, API specs

**Agent:** `architect-review` for complex features

### 2. Implementation Planning
**Break down into:**
- Discrete tasks (< 2 hours each)
- Dependencies between tasks
- Parallel workstreams

**Output:** Task list with estimates

### 3. Implementation
**Guidelines:**
- Write tests alongside code (TDD optional but helpful)
- Commit frequently (atomic commits)
- Follow existing patterns in codebase
- Document as you go

**Run parallel workstreams:**
- Core implementation
- Tests
- Documentation

### 4. Code Review
**Checklist:**
- [ ] Code follows project conventions
- [ ] No obvious bugs or edge cases missed
- [ ] Performance acceptable
- [ ] Error handling complete
- [ ] Tests meaningful (not just coverage)

**Agent:** `code-reviewer`

### 5. Security Review
**Check:**
- Input validation
- Auth/authz on new endpoints
- Sensitive data handling
- No secrets in code

**Agent:** `security-auditor` (if auth-related)

### 6. Testing
**Required:**
- Unit tests (80%+ coverage on new code)
- Integration tests for API endpoints
- E2E tests for critical paths

**Agent:** `test-automator` or `debugger`

### 7. Performance Check
**Verify:**
- Response times acceptable
- No memory leaks
- Bundle size impact (frontend)

**Agent:** `performance-engineer` (if perf-sensitive)

### 8. Documentation
**Update:**
- API docs (OpenAPI/Swagger)
- User guide (if user-facing)
- Changelog entry
- README if needed

### 9. Deployment Prep
**Checklist:**
- [ ] Version bumped
- [ ] Changelog updated
- [ ] Migration scripts (if DB changes)
- [ ] Rollback plan documented
- [ ] Feature flags (if gradual rollout)

## Success Criteria
- [ ] All tests pass
- [ ] Security review clean
- [ ] Performance within limits
- [ ] Documentation complete
- [ ] Code reviewed and approved

## Review Gate
```bash
# Run before marking complete
cortex review -c feature
```

## Quick Start Template

```markdown
## Feature: [Name]

### Requirements
- [ ] Requirement 1
- [ ] Requirement 2

### Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Tests
- [ ] Docs

### API Changes
- `POST /api/v1/resource` - Create resource
- `GET /api/v1/resource/:id` - Get resource

### Rollback Plan
1. Revert commit
2. Run down migration
3. Clear cache
```
