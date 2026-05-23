---
name: gh-setting-milestones
description: Associates an issue with a milestone. Use for release planning.
---

# Setting Issue Milestones

## Purpose

Updates the milestone of an issue using the `gh issue edit` command.

## 1. Safety & Verification

- **Milestone Title**: Requires the title or number of the milestone.

## 2. Common Workflows

### Workflow: Assign Milestone

Links an issue to a specific release target.

**Command**:

```bash
gh issue edit <issue-number> --milestone "v1.0"
```
