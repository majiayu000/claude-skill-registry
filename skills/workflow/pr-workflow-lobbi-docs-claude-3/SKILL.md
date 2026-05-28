---
name: pr-workflow
description: Comprehensive knowledge for creating, managing, and merging pull requests with Jira integration, following best practices for code review, deployment, and team collaboration
version: 1.0.0
trigger_phrases: [create PR, pull request, merge changes, git workflow, review request]
categories: [git, pr, workflow, deployment, code-review]
author: Claude Orchestration
created: 2025-12-17
updated: 2025-12-17
---

# PR Workflow Skill

Guidance for creating, managing, and merging PRs with Jira integration and deployment best practices.

## Branch Naming

Format: `<type>/<jira-key>-<short-description>`

**Types:** feature, bugfix, hotfix, refactor, docs, test, chore, perf

**Rules:** lowercase, hyphens, max 50 chars, include Jira key

Example: `feature/LOBBI-1234-member-dashboard`

## Commit Messages

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** feat, fix, docs, style, refactor, perf, test, chore, build, ci

**Rules:** lowercase subject, no period, imperative mood, max 50 chars

**Footers:** `Closes PROJ-123`, `BREAKING CHANGE: description`, `Refs PROJ-456`

## PR Title & Description

**Title:** `[JIRA-KEY] Type: Brief description`

**Description checklist items:**
- Jira issue link
- Changes made (bullet points)
- Technical details (architecture, database, API changes)
- Testing: unit, integration, E2E, manual steps
- Screenshots/videos if UI changes
- Risk assessment (Low/Medium/High/Critical)
- Deployment prerequisites & migration steps
- Dependencies (related PRs, blocked by, blocks)
- Checklist: code style, tests, docs, no console.log, no commented code

## Review Process

**Reviewer selection:**
1. Code owner (required, auto-assigned via CODEOWNERS)
2. Subject matter expert (complex/security/performance)
3. Team lead (major architectural changes, breaking changes)

**Review labels:** needs-review, needs-changes, approved, security-review, breaking-change, hotfix, size/small|medium|large, wip

**Merge requirements:**
- All CI/CD checks pass
- Required approvals received
- Branch up-to-date with main
- Documentation complete
- Conversations resolved

## Merge Strategies

| Strategy | Best For | Benefit |
|----------|----------|---------|
| **Squash** | Features, bug fixes, WIP commits | Clean history |
| **Merge Commit** | Long-lived branches, team effort | Preserves history |
| **Rebase** | Clean commits, small focused PRs | Linear history |

**Decision Matrix:**
- Feature + WIP commits → Squash
- Hotfix (single commit) → Rebase
- Large feature (team) → Merge Commit
- Bug fix (2-3 commits) → Squash
- Refactor (logical steps) → Merge Commit

## Jira Integration

**Automatic linking:** Include Jira key in branch name, PR title, or commits

**Status transitions:**
- PR opened → To Do → In Progress
- Ready for review → In Review
- Changes requested → In Progress
- Approved → Ready for Merge
- Merged → Done
- Closed (not merged) → Cancelled

**Automatic Jira comments post:**
- PR opened notification with metadata
- Status updates on approval
- Merge/close notifications

## Deployment

**Risk assessment checklist:**
- Database schema changes
- API breaking changes
- Third-party integration changes
- Auth/authorization changes
- Performance-critical code
- High-traffic endpoints
- Data migration required

**Rollback procedure:**
1. Immediate: alert team, document in incident channel
2. Execute: kubectl rollout undo / helm rollback / vercel rollback
3. Verify: health checks, error rates, user traffic
4. Database: run down migration if needed
5. Post: update Jira, notify stakeholders, schedule post-mortem

**Feature flags:** Use gradual rollout (10%, 50%, 100%) with kill switches

## Common Workflows

**Create Feature PR:**
```bash
git checkout -b feature/PROJ-123-new-dashboard
# Make changes
git add . && git commit -m "feat: add dashboard"
git push -u origin feature/PROJ-123-new-dashboard
# Create PR via Harness Code API
```

**Address Feedback:**
```bash
git add . && git commit -m "fix: address review feedback"
git fetch origin && git rebase origin/main
git push --force-with-lease
# Re-request review
```

**Merge PR (via Harness Code):**
```bash
# Verify all pipeline checks pass via Harness Code API
harness_get_pull_request_checks --pr-number 123
# Merge via Harness Code API
harness_merge_pull_request --pr-number 123 --strategy squash
git checkout main && git pull origin main
# Verify deployment via Harness Pipeline
```

## Troubleshooting

**Merge conflicts:**
- Update main: `git checkout main && git pull origin main`
- Rebase: `git checkout feature && git rebase main`
- Resolve files and `git add . && git rebase --continue`
- Force push: `git push --force-with-lease`

**Failed CI checks:**
- View logs via Harness Pipeline execution logs
- Run locally: `npm test && npm run lint && npm run type-check`
- Fix and push again

**Large PR feedback:**
- Create feature base branch
- Split into logical chunks
- Create sub-PRs against base, then final PR to main

## PR Size Guidelines

- **Small:** < 100 lines (ideal, easy to review)
- **Medium:** 100-500 lines (acceptable)
- **Large:** 500-1000 lines (consider splitting)
- **Too Large:** > 1000 lines (must split)

## Review Turnaround

- Hotfix: < 1 hour
- Bug fix: < 4 hours
- Small feature: < 1 day
- Medium feature: < 2 days
- Large feature: < 3 days

## Best Practices

1. Keep PRs focused on single concern
2. Write descriptive titles and descriptions
3. Link to Jira tickets
4. Include tests and documentation
5. Respond to feedback promptly
6. Use draft PRs for early feedback
7. Clean up commits before merging
8. Delete branches after merge
9. Monitor post-deployment

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Harness Code Repository](https://developer.harness.io/docs/code-repository)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Code Review Best Practices](https://google.github.io/eng-practices/review/)
