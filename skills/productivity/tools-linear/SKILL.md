---
name: tools-linear
description: Issue tracking and project management with Linear MCP. Use when creating issues, managing tasks, updating status, or working with Linear projects. Provides conventions for sizing, status, comments, and labels.
---

# Linear Skill

Conventions and patterns for using the Linear MCP server effectively.

## When to Use This Skill

- Creating or updating Linear issues
- Managing project tasks and priorities
- Adding comments or context to issues
- Querying issues by status, assignee, or project

## MCP Tools

Use the Linear MCP server tools:

| Tool | Purpose |
|------|---------|
| `linear_create_issue` | Create new issues |
| `linear_update_issue` | Update existing issues |
| `linear_search_issues` | Find issues by query |
| `linear_get_issue` | Get issue details |
| `linear_add_comment` | Add comments to issues |
| `linear_get_teams` | List available teams |
| `linear_get_projects` | List projects |

## Field Conventions

### Title

Format: `<type>: <brief description>`

Types:
- `feat` - New feature or enhancement
- `fix` - Bug fix
- `chore` - Maintenance, refactoring, dependencies
- `docs` - Documentation
- `perf` - Performance improvement

Examples:
```
feat: Add user authentication flow
fix: Resolve null pointer in checkout
chore: Upgrade React to v19
docs: Update API documentation
```

### Description

Structure descriptions consistently:

```markdown
## Context
[Why this issue exists - background and motivation]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Notes
[Optional: implementation hints, constraints, dependencies]
```

### Estimate (Sizing)

Use fibonacci-style story points:

| Points | Meaning | Rough Time |
|--------|---------|------------|
| 0 | Trivial | < 30 min |
| 1 | Small | 1-2 hours |
| 2 | Medium-small | Half day |
| 3 | Medium | 1 day |
| 5 | Medium-large | 2-3 days |
| 8 | Large | 1 week |
| 13 | Very large | Consider splitting |

**Default to smaller estimates.** If unsure between 3 and 5, pick 3.

### Priority

| Priority | When to Use |
|----------|-------------|
| Urgent | Production down, security issue, blocking release |
| High | Current sprint commitment, customer-facing bugs |
| Medium | Planned work, improvements (default) |
| Low | Nice-to-have, tech debt, future consideration |

### Status Workflow

Standard workflow states:

```
Backlog → Todo → In Progress → In Review → Done
                     ↓
                  Blocked
```

**Status conventions:**

- **Backlog**: Triaged but not scheduled
- **Todo**: Committed for current cycle
- **In Progress**: Actively being worked on (limit WIP)
- **In Review**: PR submitted, awaiting review
- **Blocked**: Waiting on external dependency
- **Done**: Shipped and verified

### Labels

Use labels sparingly. Recommended categories:

| Category | Examples |
|----------|----------|
| Area | `frontend`, `backend`, `api`, `infra` |
| Type | `bug`, `enhancement`, `tech-debt` |
| Effort | `quick-win`, `spike` |

## Comments

### When to Comment

Add comments for:
- Status updates when blocked
- Technical findings during implementation
- Links to relevant PRs or docs
- Decision rationale

### Comment Format

```markdown
**[Status Update]**
Blocked waiting on API credentials from vendor. ETA tomorrow.

---

**[Technical Note]**
Found that the existing auth middleware can be reused. See `src/middleware/auth.ts`.

---

**[Decision]**
Going with approach A because of X. Considered B but rejected due to Y.
```

### Linking PRs

When a PR is created, add a comment:

```markdown
**[PR Submitted]**
https://github.com/org/repo/pull/123

Ready for review.
```

## Workflow Patterns

### Creating an Issue

```
1. Use linear_get_teams to find team ID
2. Create issue with:
   - Descriptive title (type: description)
   - Structured description with acceptance criteria
   - Appropriate estimate (default to smaller)
   - Priority (default: Medium)
   - Status: Backlog or Todo
```

### Starting Work

```
1. Move issue to "In Progress"
2. Begin implementation
3. Add comments for significant findings
```

### Submitting for Review

```
1. Create PR (see Git conventions)
2. Add comment linking PR to issue
3. Move issue to "In Review"
```

### Completing Work

```
1. Merge PR
2. Move issue to "Done"
3. Add final comment if needed (lessons learned, follow-up items)
```

## Important: No Git Branches

**Do NOT use Linear's git branch integration.** We manage branches manually.

When working on an issue:
1. Create branches using standard git commands
2. Name branches using your team's convention (not Linear's auto-naming)
3. Link work to issues via PR descriptions or comments only

## Query Examples

### Find My Open Issues

```
Search: assignee:me is:open
```

### Find Blocked Issues

```
Search: status:Blocked
```

### Find High Priority Bugs

```
Search: priority:High label:bug
```

### Find Unestimated Issues

```
Search: estimate:none project:"Current Sprint"
```

## Anti-Patterns

### Avoid

- Leaving issues in "In Progress" indefinitely
- Creating issues without acceptance criteria
- Using 13-point estimates (split the issue instead)
- Updating status without context (add a comment)
- Creating issues for work already done

### Prefer

- Small, focused issues (< 8 points)
- Clear acceptance criteria
- Regular status updates via comments
- Closing issues when done (not leaving in review)

## Quick Reference

| Action | Approach |
|--------|----------|
| Create issue | Title with type prefix, structured description |
| Size issue | Fibonacci points, default smaller |
| Update status | Move through workflow, add context comments |
| Link PR | Comment with PR URL when submitted |
| Close issue | Move to Done after PR merged and verified |
