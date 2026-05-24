---
name: gh-workflow
description: GitHub issue workflow management with gh CLI and native dependency tracking. Use for gh commands, finding next issues, viewing issue dependencies, and claiming issues.
---

# gh-workflow Skill

**Activation:** GitHub issues, issue dependencies, next issue, claim issue, blocked issues, priority

## Overview

Manage GitHub issues as the outer-loop planning tool. GitHub's native dependency tracking (`is:blocked`, `is:blocking`) replaces external tools for issue management.

## Key Concepts

### Outer Loop vs Inner Loop

| Loop | Tool | Scope | Duration |
|------|------|-------|----------|
| **Outer** | GitHub Issues | Epic/feature tracking | Days to weeks |
| **Inner** | Ralph Hybrid | Story execution | Single session |

### Issue Processing (Processed vs Unprocessed)

**Critical workflow concept:** Issues created directly in GitHub's browser UI are "unprocessed" - they lack relationship links, parent epics, and haven't been integrated into the roadmap.

| State | Meaning | Has Relationships | Integrated |
|-------|---------|-------------------|------------|
| **Unprocessed** | Created via browser, not yet analyzed | No | No |
| **Processed** | Analyzed by `/plan`, integrated into graph | Yes | Yes |

**Why this matters:**
- Unprocessed issues create "blind spots" in the project roadmap
- Dependencies aren't tracked → work gets blocked unexpectedly
- Duplicates aren't detected → wasted effort
- Context stays stale → planning decisions based on incomplete info

**How issues become processed:**
1. `/plan` ANALYSE phase detects unprocessed issues
2. Each issue is reviewed: close (duplicate/superseded) OR integrate (add relationships)
3. Issue marked as processed via `<!-- processed: YYYY-MM-DD -->` comment in body
4. RECOMPUTE phase updates the full issue graph

**Detecting unprocessed issues:**
```bash
# Issues with NO relationships (likely unprocessed)
# Compare all issues vs issues with any relationship
gh issue list --repo krazyuniks/guitar-tone-shootout --state open \
  --json number,title --limit 100 > /tmp/all-issues.json

gh issue list --repo krazyuniks/guitar-tone-shootout \
  --search "is:open (is:blocked OR is:blocking)" \
  --json number,title > /tmp/related-issues.json

# Difference = likely unprocessed (no dependencies)
```

**Marking as processed:**
```bash
# Add processed marker to issue body
gh issue edit 123 --repo krazyuniks/guitar-tone-shootout \
  --body "$(gh issue view 123 --repo krazyuniks/guitar-tone-shootout --json body --jq '.body')

<!-- processed: $(date +%Y-%m-%d) -->"
```

**Feedback loop:** When ANY issue is updated with new information, the entire plan may need recomputation because context has changed.

### Priority Labels

| Label | Priority | Meaning |
|-------|----------|---------|
| `priority:P0` | 0 | Critical - drop everything |
| `priority:P1` | 1 | High - this sprint |
| `priority:P2` | 2 | Medium - next sprint |
| `priority:P3` | 3 | Low - backlog |
| `priority:P4` | 4 | Wishlist |

## Commands

### /next-issue

Find the highest priority unblocked issue ready to work.

```bash
# Find unblocked P0 issues
gh issue list --repo krazyuniks/guitar-tone-shootout \
  --search "-is:blocked label:priority:P0 is:open" --limit 5

# Find any unblocked issues by priority
gh issue list --repo krazyuniks/guitar-tone-shootout \
  --search "-is:blocked is:open sort:priority" --limit 10
```

### /issue-deps <number>

Show what blocks and is blocked by a specific issue.

```bash
# Find issues that block this one (this issue depends on them)
gh issue list --repo krazyuniks/guitar-tone-shootout \
  --search "is:open blocking:#357"

# Find issues blocked by this one (depend on this issue)
gh issue list --repo krazyuniks/guitar-tone-shootout \
  --search "is:open blocked-by:#357"
```

### /claim-issue <number>

Assign to self, create worktree, initialize Ralph plan.

1. Assign issue: `gh issue edit <n> --add-assignee @me --repo krazyuniks/guitar-tone-shootout`
2. Create worktree: `./worktree.py setup <n>`
3. Run: `/ralph-plan`

## Common Workflows

### Start Work Session

```bash
# 1. Find what to work on
/next-issue

# 2. Review dependencies if needed
/issue-deps 357

# 3. Claim and start
/claim-issue 357
```

### Check Project State

```bash
# View all blocked issues
gh issue list --repo krazyuniks/guitar-tone-shootout \
  --search "is:blocked is:open" --limit 20

# View all issues blocking others
gh issue list --repo krazyuniks/guitar-tone-shootout \
  --search "is:blocking is:open" --limit 20
```

### Managing Dependencies (Native Relationships via REST API)

**IMPORTANT:** Use GitHub's native relationship feature, NOT labels.

**Note:** All endpoints use the issue's internal `id` (not the issue number). Get it with:
```bash
gh issue view 357 --repo krazyuniks/guitar-tone-shootout --json id --jq '.id'
```

#### Add Blocking Relationship
```bash
# Make issue #358 blocked by issue #357
BLOCKING_ID=$(gh issue view 357 --repo krazyuniks/guitar-tone-shootout --json id --jq '.id')

gh api repos/krazyuniks/guitar-tone-shootout/issues/358/dependencies/blocked_by \
  --method POST -f issue_id="$BLOCKING_ID"
```

#### Remove Blocking Relationship
```bash
BLOCKING_ID=$(gh issue view 357 --repo krazyuniks/guitar-tone-shootout --json id --jq '.id')

gh api repos/krazyuniks/guitar-tone-shootout/issues/358/dependencies/blocked_by/$BLOCKING_ID \
  --method DELETE
```

#### List What Blocks an Issue
```bash
gh api repos/krazyuniks/guitar-tone-shootout/issues/358/dependencies/blocked_by
```

#### List What an Issue Blocks
```bash
gh api repos/krazyuniks/guitar-tone-shootout/issues/357/dependencies/blocking
```

#### Add Sub-Issue (Parent-Child Hierarchy)
```bash
# Make issue #358 a sub-issue of epic #350
CHILD_ID=$(gh issue view 358 --repo krazyuniks/guitar-tone-shootout --json id --jq '.id')

gh api repos/krazyuniks/guitar-tone-shootout/issues/350/sub_issues \
  --method POST -f sub_issue_id="$CHILD_ID"
```

#### Remove Sub-Issue
```bash
CHILD_ID=$(gh issue view 358 --repo krazyuniks/guitar-tone-shootout --json id --jq '.id')

gh api repos/krazyuniks/guitar-tone-shootout/issues/350/sub_issues/$CHILD_ID \
  --method DELETE
```

## Planning Integration

The `/plan` command uses these queries during its mandatory phases:

### ANALYSE Phase (Load Full Context)
```bash
# All open issues
gh issue list --repo krazyuniks/guitar-tone-shootout --state open \
  --json number,title,labels,assignees,body --limit 100

# Issues blocking others
gh issue list --repo krazyuniks/guitar-tone-shootout \
  --search "is:blocking is:open" --json number,title

# Blocked issues
gh issue list --repo krazyuniks/guitar-tone-shootout \
  --search "is:blocked is:open" --json number,title
```

### RECOMPUTE Phase (Update Issue Graph)
```bash
# Close superseded issue
gh issue close 123 --repo krazyuniks/guitar-tone-shootout \
  --comment "Superseded by #456"

# Update priority (labels ARE appropriate for priority)
gh issue edit 123 --repo krazyuniks/guitar-tone-shootout \
  --remove-label "priority:P3" --add-label "priority:P2"

# Add dependency - use GraphQL (see "Managing Dependencies" section above)
# Do NOT use labels for dependencies - use native relationships
```

## Notes

- Always use `--repo krazyuniks/guitar-tone-shootout` with `gh` commands
- The `-is:blocked` filter finds issues NOT blocked by anything
- Priority sort requires labels in format `priority:P0` through `priority:P4`
- See `/plan` command for full ANALYSE → RECOMPUTE workflow

### Labels vs Relationships

| Feature | Use | Mechanism |
|---------|-----|-----------|
| **Dependencies** (blocked-by/blocking) | Native relationships | REST API (`/dependencies/blocked_by`) |
| **Sub-issues** (parent-child) | Native relationships | REST API (`/sub_issues`) |
| **Priority** | Labels | `gh issue edit --add-label "priority:P1"` |
| **Type** | Labels | `gh issue edit --add-label "epic"` |

**IMPORTANT:** Never use labels like `blocked-by:#123` for dependencies. Use GitHub's native relationship feature via REST API.

### Official Documentation

- [REST API - Issue Dependencies](https://docs.github.com/rest/issues/issue-dependencies)
- [REST API - Sub-Issues](https://docs.github.com/rest/issues/sub-issues)
- [Webhooks - issue_dependencies events](https://docs.github.com/webhooks/webhook-events-and-payloads#issue_dependencies)
- [Dependencies changelog](https://github.blog/changelog/2025-08-21-dependencies-on-issues/)
- [Sub-issues changelog](https://github.blog/changelog/2024-12-12-github-issues-projects-close-issue-as-a-duplicate-rest-api-for-sub-issues-and-more/)
