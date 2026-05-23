---
name: summarize-epic
description: Summarize GitHub Epic issue with sub-issues and related PRs. Use when reviewing epic progress or getting implementation overview.
disable-model-invocation: true
---

# Summarize Epic

Aggregate and summarize a GitHub Epic issue with its sub-issues and related PRs.

## Arguments

`<epic-issue-url>`: GitHub Epic issue URL (e.g., https://github.com/owner/repo/issues/123)

$ARGUMENTS

## Steps

### 1. Fetch Epic Issue

- Extract repository name and issue number from URL
- Get Epic details (title, body, state, comments)

### 2. Fetch Sub-issues

```bash
gh api repos/<owner>/<repo>/issues/<epic-number>/sub_issues --paginate --jq '.[].number'
```

- On failure: Report error as-is
- On success: Aggregate sub-issue states (completed/in-progress)

### 3. Fetch Related PRs

- Use GraphQL API to get PRs from issue timeline
- Search PR bodies for issue references
- Extract PR numbers from Epic body
- Get PR details (title, state, mergedAt, additions, deletions, files)

### 4. Output Format

```markdown
# Epic Summary

## Basic Info
- **Epic**: <url>
- **State**: <state>
- **Assignees**: <assignee-list>

## Overview
<Epic body summary>

## Key Comments
<Important decisions and changes from Epic comments>

## Sub-issue Progress
- **Completed**: <completed>/<total> issues
- **Progress**: <percentage>%

## Implementation Highlights

### Merged Changes
- <pr-url>: <summary of main changes>

### In Progress
- <pr-url>: <change overview>

## Overall Progress
- **Completed**: <completed>/<total> issues
- **Progress**: <percentage>%
- **Remaining**: <pending or in-progress tasks>

## Issues & Gaps
<Discrepancies between Epic spec and implementation, blockers, concerns>

## Next Steps
<Upcoming milestones>
```

## Commands

```bash
# Epic issue
gh issue view <number> --repo <owner>/<repo> --json title,body,state,comments

# Sub-issues
gh api repos/<owner>/<repo>/issues/<epic-number>/sub_issues --paginate --jq '.[].number'

# Related PRs (GraphQL)
gh api graphql -f query='
  {
    repository(owner: "<owner>", name: "<repo>") {
      issue(number: <issue-number>) {
        timelineItems(first: 100, itemTypes: [CROSS_REFERENCED_EVENT]) {
          nodes {
            ... on CrossReferencedEvent {
              source {
                ... on PullRequest { number title state merged mergedAt }
              }
            }
          }
        }
      }
    }
  }
'

# PR details
gh pr view <pr-number> --repo <owner>/<repo> --json title,body,state,mergedAt,additions,deletions,changedFiles
```
