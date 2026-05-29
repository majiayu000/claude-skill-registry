---
name: speckit-08-taskstoissues
description: Convert tasks to GitHub Issues for project tracking
---

# Spec-Kit Tasks to Issues

Convert existing tasks into actionable, dependency-ordered GitHub issues for the feature based on available design artifacts.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Prerequisites Check

1. Run prerequisites check:
   ```bash
   .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
   ```

2. Parse JSON for `FEATURE_DIR` and `AVAILABLE_DOCS`.

3. Extract the path to **tasks.md** from the output.

## GitHub Remote Validation

Get the Git remote:

```bash
git config --get remote.origin.url
```

**CRITICAL**: ONLY PROCEED TO NEXT STEPS IF THE REMOTE IS A GITHUB URL

Valid GitHub URLs:
- `git@github.com:owner/repo.git`
- `https://github.com/owner/repo.git`
- `https://github.com/owner/repo`

If the remote is NOT a GitHub URL:
```
ERROR: Git remote is not a GitHub repository.
Remote URL: [actual remote URL]

This skill only supports GitHub repositories.
```

## Execution Flow

### 1. Parse tasks.md

Read the tasks file and extract:
- Task IDs (T001, T002, etc.)
- Task descriptions
- Phase groupings
- Parallel markers [P]
- User story labels [US1], [US2], etc.
- Dependencies between tasks

### 2. Create GitHub Issues

For each task in the list, create a GitHub issue:

**Issue Title Format**: `[TaskID] [Story] Description`

Example: `[T012] [US1] Create User model in src/models/user.py`

**Issue Body Template**:

```markdown
## Task Details

**Task ID**: T012
**Phase**: Phase 3: User Story 1
**User Story**: US1
**Parallel**: Yes (can be executed in parallel with other [P] tasks)

## Description

Create User model in src/models/user.py

## File Path

`src/models/user.py`

## Dependencies

- Depends on: T011 (if applicable)
- Blocks: T014, T015 (if applicable)

## Acceptance Criteria

- [ ] File created at specified path
- [ ] Model implements required fields from data-model.md
- [ ] Tests pass (if applicable)

---

*Generated from tasks.md by /speckit-05-taskstoissues*
*Feature: [###-feature-name]*
```

**Issue Labels** (create if they don't exist):
- `speckit` - All spec-kit generated issues
- `phase-1`, `phase-2`, etc. - Phase grouping
- `us-1`, `us-2`, etc. - User story grouping
- `parallel` - Tasks that can be parallelized

### 3. Create Issues via gh CLI

Use the GitHub CLI to create issues:

```bash
gh issue create --title "[T012] [US1] Create User model" --body "..." --label "speckit,phase-3,us-1"
```

**CRITICAL SAFETY CHECK**:

UNDER NO CIRCUMSTANCES EVER CREATE ISSUES IN REPOSITORIES THAT DO NOT MATCH THE REMOTE URL

Before each `gh issue create` command, verify:
1. You are in the correct repository
2. The remote URL matches a GitHub repository
3. The issue is being created in the correct repo

### 4. Link Dependencies

After all issues are created, add cross-references:
- Edit issue bodies to include links to blocking/blocked-by issues
- Use GitHub's issue reference syntax: `#123`

## Report

Output:
- Number of issues created
- List of issue numbers and titles
- Any errors encountered
- Link to the GitHub issues list for the repository

## Error Handling

| Condition | Response |
|-----------|----------|
| Not a GitHub remote | STOP with error message |
| gh CLI not installed | STOP with installation instructions |
| gh CLI not authenticated | STOP with auth instructions |
| Issue creation fails | Report error, continue with next task |
| Label creation fails | Continue without label |

## Next Steps

After creating issues:
- Review issues in GitHub
- Assign team members
- Add to project boards
- Begin implementation following the task order
