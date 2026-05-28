---
name: feature-workflow-orchestrator
description: End-to-end feature development orchestration from planning through deployment with quality gates
license: MIT
metadata:
  adapted-by: ai-skills
  category: development-workflow
---

# Feature Workflow Orchestrator

Complete workflow for feature development from concept to production.

## Feature Development Lifecycle

```
┌──────────────────────────────────────────────────┐
│                                                  │
│  PLAN → DESIGN → IMPLEMENT → TEST → REVIEW      │
│    ↓       ↓         ↓         ↓       ↓        │
│  Scope  Arch     Code+Tests  QA    PR+Deploy    │
│                                                  │
└──────────────────────────────────────────────────┘
```

## Phase 1: Planning

### Feature Specification

```markdown
# Feature: [Name]

## Problem Statement
What problem does this solve?

## User Stories
- As a [role], I want to [action], so that [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Considerations
- Dependencies
- Performance requirements
- Security concerns

## Success Metrics
- Metric 1: Target value
- Metric 2: Target value
```

## Phase 2: Design

### Architecture Decision

```markdown
## Architecture Decision: [Title]

**Context**: What necessitates this decision
**Options**:
1. Option A - Pros/Cons
2. Option B - Pros/Cons

**Decision**: Chosen approach
**Consequences**: Impact on codebase
```

## Phase 3: Implementation

### TDD Cycle

1. Write failing tests
2. Implement minimal code
3. Refactor while green
4. Document as you go

### Branch Strategy

```bash
# Create feature branch
git checkout -b feature/user-authentication

# Regular commits
git commit -m "feat(auth): add login endpoint"
git commit -m "test(auth): add login tests"
git commit -m "docs(auth): update API docs"
```

## Phase 4: Testing

### Quality Gates

- [ ] All tests pass (80%+ coverage)
- [ ] No type errors
- [ ] No lint warnings
- [ ] Security scan clean
- [ ] Performance benchmarks met

### Verification

```bash
# Run verification loop
npm run build
npm run type-check
npm run lint
npm test -- --coverage
npm run security-scan
```

## Phase 5: Review & Deploy

### Pull Request Checklist

- [ ] Description explains what and why
- [ ] Tests included
- [ ] Documentation updated
- [ ] Breaking changes noted
- [ ] Screenshots/demo for UI changes

### Deployment

```bash
# Merge to main after approval
git checkout main
git merge --no-ff feature/user-authentication

# Tag release
git tag -a v1.2.0 -m "Release v1.2.0: Add user authentication"
git push origin v1.2.0
```

## Integration Points

Complements:
- **tdd-workflow**: For test-first development
- **verification-loop**: For quality gates
- **project-orchestration**: For project management
- **deployment-cicd**: For automated deployment
