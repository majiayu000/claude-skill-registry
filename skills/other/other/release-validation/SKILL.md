---
name: release-validation
description: Use when the Production Engineer is validating a branch for production merge, running pre-release checklists, performing regression testing, benchmarking performance, or analyzing the impact of changes before merging to main. Activates for any release readiness assessment.
version: 1.0.0
---

# Release Validation Expertise

## When This Applies

Apply this guidance when:
- Evaluating whether a development branch is ready for production
- Running pre-release checklists
- Performing regression analysis
- Assessing the impact of changes before merging to main

## Pre-Release Checklist

### 1. Code Completeness

- [ ] All tasks for this release are in `done` or `approved` status
- [ ] No tasks are stuck in `in_progress` or `blocked`
- [ ] All change requests included in this release are `completed`
- [ ] CHANGELOG.md is updated with all changes

### 2. Test Validation

- [ ] All unit tests pass (`/run-tests`)
- [ ] All e2e tests pass
- [ ] No test has been skipped or disabled without documented reason
- [ ] Test coverage meets project minimum threshold
- [ ] Performance benchmarks meet requirements (if applicable)

### 3. Code Quality

- [ ] No linting errors or warnings
- [ ] No known security vulnerabilities in dependencies
- [ ] No TODO/FIXME comments without associated task IDs
- [ ] No debug code or temporary workarounds

### 4. Documentation

- [ ] CHANGELOG.md reflects all user-visible changes
- [ ] API documentation is updated for new/changed endpoints
- [ ] ARCHITECTURE.md is current with any structural changes
- [ ] README.md reflects any new setup or usage requirements

### 5. Infrastructure

- [ ] Database migrations are backward-compatible (if applicable)
- [ ] Configuration changes are documented
- [ ] Environment variables are documented
- [ ] Deployment scripts are updated

## Change Impact Analysis

### Categorize Every Changed File

| Category | Risk Level | Examples |
|----------|-----------|---------|
| Data/schema changes | HIGH | Migrations, model changes |
| Auth/security | HIGH | Login, tokens, permissions |
| API contracts | HIGH | Endpoint signatures, response shapes |
| Business logic | MEDIUM | Core feature implementation |
| Configuration | MEDIUM | Environment, feature flags |
| UI/presentation | LOW | Styling, layout, text changes |
| Tests | LOW | New or updated tests |
| Documentation | MINIMAL | Markdown files, comments |

### Risk Calculation

```
Overall Risk = max(individual file risks)
              + bonus if > 20 files changed
              + bonus if > 500 lines changed
              + bonus if database/auth changes present
```

| Score | Level | Action |
|-------|-------|--------|
| LOW | Low risk | Merge after standard validation |
| MEDIUM | Moderate risk | Extra review of changed areas |
| HIGH | Significant risk | Full regression test, prepare rollback plan |
| CRITICAL | Major risk | Stakeholder approval required, staged rollout |

## Regression Testing Strategy

1. **Smoke tests** — Core functionality works (login, main features)
2. **Changed area tests** — Tests covering modified components
3. **Integration points** — Tests for components that interact with changed code
4. **Edge cases** — Known problematic scenarios from past releases

## Validation Report Format

Generate a report at `reports/RELEASE_VALIDATION_<YYYYMMDD>.md`:

```markdown
# Release Validation Report — <date>

## Branch: <source-branch>
## Target: main

## Summary
- Commits: N
- Files changed: N
- Risk level: LOW/MEDIUM/HIGH/CRITICAL
- Tests: PASS/FAIL
- Recommendation: APPROVE/HOLD

## Test Results
[Test output summary]

## Change Impact
[Categorized file changes]

## Risk Factors
[Identified risks]

## Approval
- Status: APPROVED / NOT APPROVED
- Conditions: [any conditions for approval]
```
