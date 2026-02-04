---
name: gh-updating-issues
description: Updates existing GitHub issues (title, body, labels, assignees, milestones, and projects). Use to refine issue details or synchronize with project boards.
---

# Updating GitHub Issues

## Purpose

Enables the modification of existing issues using the `gh issue edit` command. This skill is critical for keeping issues accurate and properly tracked within GitHub Projects.

## 1. Safety & Verification

- **Mandatory Context**: Ensure `gh-verifying-context` has been run and confirmed by the user.
- **Human-in-the-Loop**: You MUST present all proposed changes (Title, Body, Labels, Assignees, Projects) and the target issue to the user before execution.
- **Verify Issue Exists**: Use `gh-viewing-issue-details` to confirm the issue state before editing.
- **Sensitivity Check**: Do not introduce internal credentials or proprietary data into the issue metadata or body.

## 2. Common Workflows

### Workflow: Update Title and Body

Refines the core description of the issue.

**Command**:

```bash
gh issue edit <issue-number> --title "Updated Title" --body "Updated Body"
```

### Workflow: Update Project Associations

Adds or removes issues from GitHub Project boards.

**Command**:

```bash
# Add to a project
gh issue edit <issue-number> --add-project "Project Title"

# Remove from a project
gh issue edit <issue-number> --remove-project "Project Title"
```

### Workflow: Manage Metadata (Labels, Assignees, Milestones)

Efficiently updates multiple fields in a single call.

**Command**:

```bash
# Add labels and assign yourself
gh issue edit <issue-number> --add-label "bug,high-priority" --add-assignee "@me"

# Set a milestone
gh issue edit <issue-number> --milestone "v1.0-release"
```

### Workflow: Update Parent Issue

Changes or removes the parent relationship for an issue. Use this to move sub-issues between parents or promote them to top-level issues.

**Command**:

```bash
# 1. Get the numeric ID of the child issue
CHILD_ID=$(gh issue view <child-number> --json id -q .id)

# 2. To change or set a parent:
gh api --method POST /repos/{owner}/{repo}/issues/{new-parent-number}/sub_issues \
  -F sub_issue_id=$CHILD_ID

# 3. To remove from current parent (promote to top-level):
gh api --method DELETE /repos/{owner}/{repo}/issues/{current-parent-number}/sub_issue \
  -F sub_issue_id=$CHILD_ID
```

## 3. Combined Updates

You can perform multiple updates simultaneously for efficiency.

**Command**:

```bash
gh issue edit <issue-number> \
  --title "Refined Bug Report" \
  --add-label "bug" \
  --add-project "Maintenance" \
  --add-assignee "@me"
```

## 4. Error Handling

- **Invalid Flag**: If a flag is rejected, run `gh issue edit --help` to check for syntax changes in the CLI version.
- **Resource Not Found**: If the issue or project title doesn't exist, verify the names using listing skills.
