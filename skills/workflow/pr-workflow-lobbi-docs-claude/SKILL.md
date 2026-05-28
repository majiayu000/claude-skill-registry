---
name: pr-workflow
description: Comprehensive knowledge for creating, managing, and merging pull requests with Jira integration, following best practices for code review, deployment, and team collaboration
version: 1.0.0
trigger_phrases:
  - create PR
  - pull request
  - merge changes
  - git workflow
  - open PR
  - submit PR
  - review request
  - merge request
  - code review
  - branch strategy
categories:
  - git
  - pr
  - workflow
  - deployment
  - code-review
  - jira-integration
author: Claude Orchestration
created: 2025-12-17
updated: 2025-12-17
---

# PR Workflow Skill

This skill provides comprehensive guidance for creating, managing, and merging pull requests with Jira integration, following industry best practices for code review, deployment safety, and team collaboration.

## Table of Contents

1. [Branch Naming Conventions](#branch-naming-conventions)
2. [Commit Message Standards](#commit-message-standards)
3. [PR Title and Description](#pr-title-and-description)
4. [PR Templates](#pr-templates)
5. [Review Process](#review-process)
6. [Merge Strategies](#merge-strategies)
7. [Jira Integration](#jira-integration)
8. [Deployment Notes](#deployment-notes)
9. [Common Workflows](#common-workflows)
10. [Troubleshooting](#troubleshooting)

---

## Branch Naming Conventions

### Standard Format

```
<type>/<jira-key>-<short-description>
```

### Branch Types

| Type | Purpose | Example |
|------|---------|---------|
| `feature` | New features | `feature/PROJ-123-user-authentication` |
| `bugfix` | Bug fixes | `bugfix/PROJ-456-login-error` |
| `hotfix` | Urgent production fixes | `hotfix/PROJ-789-payment-failure` |
| `refactor` | Code refactoring | `refactor/PROJ-234-database-queries` |
| `docs` | Documentation only | `docs/PROJ-567-api-documentation` |
| `test` | Adding/updating tests | `test/PROJ-890-integration-tests` |
| `chore` | Maintenance tasks | `chore/PROJ-345-dependency-update` |
| `perf` | Performance improvements | `perf/PROJ-678-query-optimization` |

### Naming Best Practices

- Use lowercase with hyphens
- Include Jira ticket key
- Keep description short but meaningful (max 50 chars)
- Use present tense verbs
- Avoid special characters except `-` and `/`

### Examples

```bash
# Good
feature/LOBBI-1234-member-dashboard
bugfix/LOBBI-5678-email-validation
hotfix/LOBBI-9012-critical-auth-bug

# Bad
feature/add_new_feature
LOBBI-1234
my-branch
fix-bug-in-production
```

---

## Commit Message Standards

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `build`: Build system changes
- `ci`: CI/CD changes
- `revert`: Reverting previous commits

### Subject Line Rules

- Start with lowercase
- No period at the end
- Use imperative mood ("add" not "added")
- Max 50 characters
- Include Jira key if not in branch name

### Body Guidelines

- Wrap at 72 characters
- Explain what and why, not how
- Use bullet points for multiple changes
- Reference related issues

### Footer

- Breaking changes: `BREAKING CHANGE: description`
- Closes issues: `Closes PROJ-123`
- References: `Refs PROJ-456, PROJ-789`

### Examples

```bash
# Simple commit
feat(auth): add OAuth2 login support

# With body
fix(api): resolve race condition in user creation

The user creation endpoint could create duplicate users when
called simultaneously. Added database-level unique constraint
and proper error handling.

Closes LOBBI-5678

# Breaking change
feat(api): update authentication flow

BREAKING CHANGE: Authentication now requires API version header.
Clients must include 'X-API-Version: 2.0' in all requests.

Refs LOBBI-1234

# Multiple changes
refactor(database): optimize query performance

- Add indexes to frequently queried columns
- Use eager loading for related entities
- Implement query result caching
- Remove N+1 query patterns

Performance improved by 60% in testing.

Closes LOBBI-3456
```

---

## PR Title and Description

### Title Format

```
[JIRA-KEY] Type: Brief description
```

### Title Examples

```
[LOBBI-1234] Feature: Add member dashboard with activity feed
[LOBBI-5678] Fix: Resolve email validation error on signup
[LOBBI-9012] Hotfix: Critical authentication bug in production
[LOBBI-3456] Refactor: Optimize database query performance
[LOBBI-7890] Docs: Update API documentation for v2.0
```

### Description Template

Use this template for all PRs:

```markdown
## Summary
[Brief overview of changes - 2-3 sentences]

## Jira Ticket
- **Issue:** [PROJ-123](https://your-jira.atlassian.net/browse/PROJ-123)
- **Type:** Feature | Bug Fix | Hotfix | Refactor | Documentation
- **Priority:** Critical | High | Medium | Low

## Changes Made
- List key changes
- Use bullet points
- Be specific and concise

## Technical Details
### Architecture Changes
- Describe any architectural decisions
- Explain design patterns used

### Database Changes
- Schema migrations
- New tables/columns
- Index additions

### API Changes
- New endpoints
- Modified endpoints
- Breaking changes

## Testing
### Test Coverage
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated
- [ ] Manual testing completed

### Test Instructions
1. Step-by-step instructions for reviewers
2. Include test data or scenarios
3. Expected outcomes

### Test Results
- Coverage: XX%
- All tests passing: Yes/No
- Performance benchmarks: [if applicable]

## Screenshots/Videos
[If UI changes, include before/after screenshots or demo video]

## Deployment Notes
### Risk Assessment
- **Risk Level:** Low | Medium | High | Critical
- **Rollback Plan:** [Describe rollback procedure]

### Prerequisites
- [ ] Database migrations ready
- [ ] Environment variables configured
- [ ] Feature flags set
- [ ] Dependencies updated

### Migration Steps
1. Run migrations: `npm run migrate:up`
2. Deploy application
3. Verify health checks
4. Enable feature flag (if applicable)

### Rollback Procedure
1. Disable feature flag
2. Revert deployment
3. Run down migration: `npm run migrate:down`

## Dependencies
- Related PRs: #123, #456
- Blocked by: #789
- Blocks: #234

## Checklist
- [ ] Code follows project style guide
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.log or debug code
- [ ] No commented-out code
- [ ] Environment variables documented
- [ ] CHANGELOG.md updated
- [ ] Breaking changes documented
- [ ] Jira ticket updated

## Additional Notes
[Any other context, concerns, or discussion points]
```

---

## PR Templates

### Feature PR Template

```markdown
## Feature Summary
[What feature is being added and why]

## Jira Ticket
- **Issue:** [PROJ-123](https://jira.example.com/browse/PROJ-123)
- **Epic:** [PROJ-100](https://jira.example.com/browse/PROJ-100)

## User Story
As a [user type],
I want [goal],
So that [benefit].

## Implementation Details
### New Components
- Component A: Purpose and functionality
- Component B: Purpose and functionality

### Modified Components
- Component C: What changed and why

### New Dependencies
- package-name@version: Why it's needed

## API Changes
### New Endpoints
```
POST /api/v1/resource
GET /api/v1/resource/:id
PUT /api/v1/resource/:id
DELETE /api/v1/resource/:id
```

### Request/Response Examples
```json
// POST /api/v1/resource
{
  "name": "Example",
  "type": "demo"
}

// Response
{
  "id": "123",
  "name": "Example",
  "type": "demo",
  "created_at": "2025-12-17T10:00:00Z"
}
```

## Testing Strategy
- [ ] Unit tests for business logic
- [ ] Integration tests for API endpoints
- [ ] E2E tests for user flows
- [ ] Performance testing completed
- [ ] Security review completed

## Feature Flags
- Flag name: `enable_new_feature`
- Default: `false`
- Rollout plan: Gradual release to 10%, 50%, 100%

## Documentation
- [ ] API documentation updated
- [ ] User guide updated
- [ ] Admin guide updated (if applicable)
- [ ] Technical design document linked

## Deployment
- **Target Environment:** Production
- **Deployment Window:** [Date/Time]
- **Monitoring Plan:** [Metrics to watch]
```

### Bugfix PR Template

```markdown
## Bug Description
[What was broken and how it manifested]

## Jira Ticket
- **Issue:** [PROJ-456](https://jira.example.com/browse/PROJ-456)
- **Severity:** Critical | High | Medium | Low

## Root Cause
[Technical explanation of what caused the bug]

## Solution
[How the bug was fixed]

## Code Changes
### Files Modified
- `src/path/to/file.ts`: Fixed [specific issue]
- `tests/path/to/test.ts`: Added regression test

### Before (Problematic Code)
```javascript
// Code that caused the issue
function buggyFunction() {
  // problematic logic
}
```

### After (Fixed Code)
```javascript
// Fixed code
function fixedFunction() {
  // corrected logic
}
```

## Testing
### Regression Test
```javascript
describe('bugfix PROJ-456', () => {
  it('should handle edge case correctly', () => {
    // Test that prevents regression
  });
});
```

### Manual Testing Steps
1. Navigate to [page/endpoint]
2. Perform [action]
3. Verify [expected behavior]

## Impact Analysis
- **Users Affected:** [Number/Percentage]
- **Environments Affected:** Production | Staging | Development
- **Data Integrity:** No impact | Requires data migration

## Verification
- [ ] Bug reproduced in development
- [ ] Fix verified in development
- [ ] Regression test added
- [ ] No side effects identified
- [ ] Tested in staging
```

### Hotfix PR Template

```markdown
## HOTFIX - URGENT

## Critical Issue
[Clear description of the production issue]

## Jira Ticket
- **Issue:** [PROJ-789](https://jira.example.com/browse/PROJ-789)
- **Severity:** CRITICAL
- **Incident Report:** [Link to incident]

## Impact
- **Users Affected:** [Estimate]
- **Business Impact:** [Revenue, reputation, compliance]
- **Started:** [Timestamp]
- **Duration:** [How long issue has existed]

## Root Cause
[Quick analysis of what went wrong]

## Immediate Fix
[What this PR does to stop the bleeding]

## Long-term Solution
[Follow-up work needed - create Jira tickets]

## Fast-Track Approval
- [ ] Tested in staging replica
- [ ] Rollback plan ready
- [ ] On-call team notified
- [ ] Monitoring alerts configured

## Deployment
- **Deploy ASAP:** YES
- **Requires Downtime:** Yes/No
- **Rollback Time:** [Estimate]

## Post-Deployment
- [ ] Verify fix in production
- [ ] Monitor for 30 minutes
- [ ] Update incident report
- [ ] Schedule post-mortem
```

---

## Review Process

### Requesting Reviews

#### Reviewer Selection

1. **Code Owner (Required)**
   - Automatically assigned via CODEOWNERS
   - Must approve before merge

2. **Subject Matter Expert (Optional)**
   - For complex technical areas
   - Security changes
   - Performance-critical code

3. **Team Lead (For Major Changes)**
   - Architectural decisions
   - Breaking changes
   - Cross-team impact

#### Review Labels

| Label | Purpose | When to Use |
|-------|---------|-------------|
| `needs-review` | Awaiting initial review | When PR is ready |
| `needs-changes` | Changes requested | After review feedback |
| `approved` | Ready to merge | All reviews approved |
| `security-review` | Requires security check | Auth, permissions, data handling |
| `breaking-change` | Contains breaking changes | API changes, deprecations |
| `hotfix` | Urgent production fix | Critical issues |
| `wip` | Work in progress | Not ready for review |
| `size/small` | < 100 lines changed | Auto-applied |
| `size/medium` | 100-500 lines | Auto-applied |
| `size/large` | > 500 lines | Auto-applied, consider splitting |

### Review Checklist

#### For Reviewers

```markdown
## Code Quality
- [ ] Code is readable and maintainable
- [ ] Follows project style guide
- [ ] No code smells or anti-patterns
- [ ] DRY principle followed
- [ ] SOLID principles applied

## Functionality
- [ ] Changes match PR description
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] Input validation present
- [ ] No hardcoded values

## Testing
- [ ] Tests are comprehensive
- [ ] Tests are readable
- [ ] Coverage is adequate
- [ ] Tests actually test the right things
- [ ] No flaky tests

## Security
- [ ] No sensitive data exposed
- [ ] Authentication/authorization correct
- [ ] Input sanitization present
- [ ] SQL injection prevented
- [ ] XSS prevention in place

## Performance
- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] Proper indexing used
- [ ] No N+1 queries
- [ ] Caching considered

## Documentation
- [ ] Code comments where needed
- [ ] API documentation updated
- [ ] README updated if needed
- [ ] CHANGELOG updated
- [ ] Breaking changes documented
```

### Merge Requirements

Before merging, ensure:

1. **Status Checks Pass**
   - All CI/CD pipelines green
   - Tests passing
   - Linting passing
   - Security scans clean

2. **Approvals Met**
   - Required reviewers approved
   - No pending change requests
   - Conversations resolved

3. **Branch Up-to-Date**
   - Rebased on latest main/master
   - Merge conflicts resolved
   - No divergent changes

4. **Documentation Complete**
   - CHANGELOG updated
   - Jira ticket linked
   - Breaking changes noted

---

## Merge Strategies

### Squash and Merge (Recommended for Most PRs)

**When to Use:**
- Feature branches
- Bug fixes
- Multiple WIP commits

**Benefits:**
- Clean, linear history
- Single commit per feature
- Easy to revert

**Process:**
```bash
# GitHub will squash automatically, or manually:
git checkout main
git merge --squash feature/PROJ-123-new-feature
git commit -m "feat: add new feature [PROJ-123]"
git push origin main
```

### Merge Commit (For Complex Features)

**When to Use:**
- Long-lived feature branches
- Multiple contributors
- Want to preserve commit history

**Benefits:**
- Preserves all commits
- Shows collaboration history
- Clear feature boundaries

**Process:**
```bash
git checkout main
git merge --no-ff feature/PROJ-123-new-feature
git push origin main
```

### Rebase and Merge (For Clean History)

**When to Use:**
- Small, focused PRs
- Already clean commit history
- Linear history preference

**Benefits:**
- No merge commits
- Clean linear history
- Each commit is meaningful

**Process:**
```bash
git checkout feature/PROJ-123-new-feature
git rebase main
git push --force-with-lease origin feature/PROJ-123-new-feature
# Then merge via GitHub
```

### Strategy Decision Matrix

| Scenario | Strategy | Reason |
|----------|----------|--------|
| Feature with multiple WIP commits | Squash | Clean up history |
| Hotfix (single commit) | Rebase | Keep linear |
| Large feature (team effort) | Merge Commit | Preserve history |
| Bug fix (2-3 commits) | Squash | Simplify |
| Refactoring (many logical steps) | Merge Commit | Show progression |

---

## Jira Integration

### Linking PRs to Jira Issues

#### Automatic Linking

Include Jira key in:
- Branch name: `feature/PROJ-123-description`
- PR title: `[PROJ-123] Add new feature`
- Commit messages: `feat: add feature (PROJ-123)`

#### Manual Linking

In PR description:
```markdown
## Jira Ticket
- **Issue:** [PROJ-123](https://jira.example.com/browse/PROJ-123)
- **Type:** Feature
- **Priority:** High

Closes PROJ-123
```

### Jira Status Transitions

PRs should trigger automatic status updates:

| PR Event | Jira Status Transition |
|----------|----------------------|
| PR opened | To Do → In Progress |
| PR ready for review | In Progress → In Review |
| Changes requested | In Review → In Progress |
| PR approved | In Review → Ready for Merge |
| PR merged | Ready for Merge → Done |
| PR closed (not merged) | Any → Cancelled |

### Jira Comment Updates

Automatically post to Jira:

```markdown
Pull Request opened: [PR #123](https://github.com/org/repo/pull/123)

**Title:** [PROJ-123] Add new feature
**Author:** @developer
**Status:** Ready for Review
**Files Changed:** 15
**Lines Added:** +250, Removed: -100

[View Pull Request](https://github.com/org/repo/pull/123)
```

---

## Deployment Notes

### Risk Assessment Template

```markdown
## Risk Assessment

### Risk Level: [Low | Medium | High | Critical]

### Risk Factors
- [ ] Database schema changes
- [ ] API breaking changes
- [ ] Third-party integration changes
- [ ] Authentication/authorization changes
- [ ] Performance-critical code modified
- [ ] High-traffic endpoints affected
- [ ] Data migration required

### Impact Analysis
- **User Impact:** [Describe who is affected]
- **System Impact:** [Services/components affected]
- **Data Impact:** [Any data modifications]
- **Downtime Required:** Yes/No - [Duration]

### Mitigation Strategies
1. [Strategy to reduce risk]
2. [Backup plan]
3. [Monitoring approach]
```

### Rollback Procedures

#### Standard Rollback

```markdown
## Rollback Procedure

### Triggers
- Critical bug discovered
- Performance degradation > 20%
- User-reported issues spike
- Health checks failing

### Steps
1. **Immediate Actions** (0-5 minutes)
   - Alert on-call team
   - Document issue in incident channel
   - Prepare rollback command

2. **Execute Rollback** (5-10 minutes)
   ```bash
   # Kubernetes
   kubectl rollout undo deployment/app-name -n namespace

   # Helm
   helm rollback release-name -n namespace

   # Vercel
   vercel rollback [deployment-url]
   ```

3. **Verify Rollback** (10-15 minutes)
   - Check health endpoints
   - Verify user traffic
   - Monitor error rates
   - Test critical flows

4. **Database Rollback** (if needed)
   ```bash
   # Run down migration
   npm run migrate:down
   # or
   npx prisma migrate reset --to-migration [previous-migration]
   ```

5. **Post-Rollback** (15-30 minutes)
   - Update Jira ticket
   - Notify stakeholders
   - Schedule post-mortem
   - Create fix plan
```

### Feature Flags

```markdown
## Feature Flag Strategy

### Flag Configuration
```yaml
feature_flags:
  new_dashboard:
    enabled: false
    rollout:
      - percentage: 10
        start_date: 2025-12-17
      - percentage: 50
        start_date: 2025-12-20
      - percentage: 100
        start_date: 2025-12-24
    kill_switch: true
```

### Implementation
```javascript
// Using LaunchDarkly, Split.io, or custom solution
if (featureFlags.isEnabled('new_dashboard', userId)) {
  return renderNewDashboard();
} else {
  return renderOldDashboard();
}
```

### Rollout Plan
1. **10% - Internal Users** (Day 1-3)
   - Monitor closely
   - Gather feedback
   - Fix critical issues

2. **50% - Beta Users** (Day 4-7)
   - Broader testing
   - Performance validation
   - UX feedback

3. **100% - All Users** (Day 8+)
   - Full rollout
   - Remove old code after 30 days
```

### Migration Steps

```markdown
## Database Migration

### Schema Changes
```sql
-- Migration Up (20251217_add_user_preferences.sql)
CREATE TABLE user_preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  preferences JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);

-- Migration Down
DROP TABLE IF EXISTS user_preferences;
```

### Deployment Steps
1. **Pre-deployment** (30 minutes before)
   ```bash
   # Backup database
   pg_dump -h host -U user -d database > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

2. **Deployment Window**
   ```bash
   # 1. Run migrations
   npm run migrate:up

   # 2. Deploy application
   kubectl set image deployment/app app=org/app:v2.0.0 -n production

   # 3. Wait for rollout
   kubectl rollout status deployment/app -n production
   ```

3. **Post-deployment Verification**
   ```bash
   # Check migration status
   npm run migrate:status

   # Verify data integrity
   psql -c "SELECT COUNT(*) FROM user_preferences;"

   # Test endpoints
   curl https://api.example.com/health
   ```
```

---

## Common Workflows

### Creating a Feature PR

```bash
# 1. Create and checkout feature branch
git checkout -b feature/PROJ-123-new-dashboard

# 2. Make changes and commit
git add .
git commit -m "feat(dashboard): add user activity widget"

# 3. Push branch
git push -u origin feature/PROJ-123-new-dashboard

# 4. Create PR via GitHub CLI
gh pr create \
  --title "[PROJ-123] Feature: Add user activity dashboard" \
  --body "$(cat .github/pull_request_template.md)" \
  --label "feature,needs-review" \
  --reviewer team-lead,code-owner

# 5. Update Jira
# PR link automatically added via GitHub-Jira integration
```

### Updating PR with Review Feedback

```bash
# 1. Make requested changes
git add .
git commit -m "fix: address review feedback"

# 2. Rebase if main has updates
git fetch origin
git rebase origin/main

# 3. Force push (safe because it's your branch)
git push --force-with-lease

# 4. Respond to review comments
gh pr comment 123 --body "Updated per your feedback!"

# 5. Re-request review
gh pr ready 123
```

### Merging a PR

```bash
# 1. Final checks
gh pr checks 123

# 2. Update Jira status
# (Automated via webhook)

# 3. Merge via GitHub
gh pr merge 123 --squash --delete-branch

# 4. Update local main
git checkout main
git pull origin main

# 5. Verify deployment (if auto-deploy enabled)
kubectl get pods -n production

# 6. Close Jira ticket
# (Automated via webhook)
```

---

## Troubleshooting

### Merge Conflicts

```bash
# 1. Update main
git checkout main
git pull origin main

# 2. Rebase feature branch
git checkout feature/PROJ-123-feature
git rebase main

# 3. Resolve conflicts
# Edit conflicted files, then:
git add .
git rebase --continue

# 4. Force push
git push --force-with-lease origin feature/PROJ-123-feature
```

### Failed CI/CD Checks

```bash
# 1. Check failure logs
gh run view [run-id]

# 2. Run tests locally
npm test
npm run lint
npm run type-check

# 3. Fix issues and push
git add .
git commit -m "fix: resolve CI failures"
git push origin feature/PROJ-123-feature
```

### Large PR Feedback

If reviewer says "PR too large":

```bash
# 1. Create feature branch for series
git checkout -b feature/PROJ-123-new-feature-base

# 2. Create sub-branches for logical chunks
git checkout -b feature/PROJ-123-part-1-models
# Make changes, commit, push

# 3. Create first PR against base branch
gh pr create --base feature/PROJ-123-new-feature-base

# 4. Repeat for each logical chunk
git checkout feature/PROJ-123-new-feature-base
git checkout -b feature/PROJ-123-part-2-api
# Continue...

# 5. Final PR merges base into main
gh pr create --base main
```

---

## Advanced Tips

### PR Size Guidelines

- **Small:** < 100 lines - Ideal, easy to review
- **Medium:** 100-500 lines - Acceptable
- **Large:** 500-1000 lines - Consider splitting
- **Too Large:** > 1000 lines - Must split

### Review Turnaround Expectations

- **Hotfix:** < 1 hour
- **Bug fix:** < 4 hours
- **Small feature:** < 1 day
- **Medium feature:** < 2 days
- **Large feature:** < 3 days

### Best Practices Summary

1. Keep PRs focused on single concern
2. Write descriptive titles and descriptions
3. Link to Jira tickets
4. Include tests
5. Update documentation
6. Respond to feedback promptly
7. Use draft PRs for early feedback
8. Clean up commits before merging
9. Delete branches after merge
10. Monitor post-deployment

---

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Code Review Best Practices](https://google.github.io/eng-practices/review/)

---

**Last Updated:** 2025-12-17
**Skill Version:** 1.0.0
**Maintained By:** Claude Orchestration Team
