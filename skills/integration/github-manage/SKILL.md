---
name: github-manage
description: Manage operations concerning GitHub on behalf of user
allowed-tools: Read, Grep, Glob, Bash
---

# Manage GitHub operations

## When to use this skill

This skill provides specific instructions to manage github on behalf of the user, for:

- Authorization
- 


# Create GitHub Milestone

Create a milestone on GitHub with title, description, and optional due date.

## Usage

```bash
/gh-milestone-create                    # Interactive mode
/gh-milestone-create "Sprint 3"         # With title
/gh-milestone-create "Sprint 3" 2025-11-15  # With title and due date
```

## What it does

1. Checks if GitHub CLI is authenticated
2. Gets repository information
3. Creates milestone with specified details
4. Optionally sets due date
5. Returns milestone URL and number

## Execution

!echo "📋 Creating GitHub milestone..."
!gh auth status
!gh repo view --json nameWithOwner,url | grep -E 'nameWithOwner|url'
!gh milestone create "New Milestone" --description "Milestone description" --due-date 2025-12-31

## Interactive Example

For interactive milestone creation with prompts:

!gh api repos/:owner/:repo/milestones -f title="Sprint 3" -f description="Sprint 3 objectives" -f due_on="2025-11-15T23:59:59Z" -f state="open"

## Parameters

- **title** (required): Milestone title
- **description** (optional): Detailed description of milestone goals
- **due-date** (optional): Due date in YYYY-MM-DD format
- **state** (optional): open or closed (default: open)

## Examples

### Basic milestone
```bash
/gh-milestone-create "v1.0 Release"
```

### Milestone with due date
```bash
/gh-milestone-create "Q4 Goals" 2025-12-31
```

### Using GitHub API directly
```bash
gh api repos/owner/repo/milestones \
  -f title="Sprint 4" \
  -f description="Complete core features" \
  -f due_on="2025-11-30T23:59:59Z"
```

## Listing Existing Milestones

```bash
gh milestone list
gh api repos/:owner/:repo/milestones
```

## Requirements

- GitHub CLI (`gh`) installed and authenticated
- Write access to the repository
- Valid repository context

## Tips

- Use clear, action-oriented milestone titles
- Set realistic due dates
- Include objectives in description
- Link issues to milestones for tracking
- Use milestones for sprint planning
- Close milestones when complete

## Related Commands

- `/pr-creation` - Create pull requests
- `gh issue create --milestone "Sprint 3"` - Create issue with milestone
- `gh milestone list` - List all milestones
