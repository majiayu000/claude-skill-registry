---
name: complete-idea
description: 'Mark an idea as completed when all its derived tasks are done. Note:
  Ideas are automatically closed when converted to tasks via /feed-backlog. Use this
  skill only for edge cases (manually created task'
---

---
name: complete-idea
description: Mark an idea as completed when all its derived tasks are done. Note: Ideas are automatically closed when converted to tasks via /feed-backlog. Use this skill only for edge cases (manually created tasks, legacy ideas, etc.).
---

# Complete Idea

Mark an accepted idea as completed after all its derived tasks are done.

**Note**: Since `/feed-backlog` automatically closes ideas when converting them to tasks, this skill is primarily for edge cases:

- Ideas that were manually converted to tasks (not via `/feed-backlog`)
- Legacy ideas that predate the auto-close feature
- Cases where an idea needs to be closed but wasn't automatically closed

## Instructions

When completing idea #N:

### Step 1 - Fetch the Idea

```bash
gh issue view N --repo jmlweb/tooling --json number,title,body,labels,state
```

Verify:

- Has `idea:accepted` label
- Is still open

### Step 2 - Find Related Tasks

```bash
gh issue list --repo jmlweb/tooling --search "idea #N in:body" --state all --json number,title,state
```

Also check the idea's body for task references.

### Step 3 - Verify Task Completion

Check if all related tasks are closed. If any are still open, inform user.

### Step 4 - Mark as Completed

```bash
gh issue edit N --repo jmlweb/tooling \
  --remove-label "idea:accepted" \
  --add-label "idea:completed"

gh issue comment N --repo jmlweb/tooling --body "## Idea Completed

All tasks derived from this idea have been implemented.

**Completed on:** $(date +%Y-%m-%d)"

gh issue close N --repo jmlweb/tooling
```

## Idea Lifecycle

```text
/add-idea       -> Creates idea (idea:pending)
/validate-ideas -> Accepts or rejects (idea:accepted | idea:rejected)
/feed-backlog   -> Creates tasks from accepted ideas AND closes the idea automatically
/next-task      -> Implements tasks
complete-idea   -> Manual closure for edge cases (normally not needed)
```

**Normal Flow**: Ideas are automatically closed when converted to tasks via `/feed-backlog`. This skill is only needed for edge cases.
