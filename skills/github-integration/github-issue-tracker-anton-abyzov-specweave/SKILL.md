---
name: github-issue-tracker
description: Task-level GitHub issue tracking for fine-grained progress visibility via comments, checklists, and labels. Use when tracking detailed task progress in GitHub, managing team collaboration on specific tasks, or tracking blocking issues. Enables per-task updates and discussions.
---

# GitHub Issue Tracker - Task-Level Progress Tracking

**Purpose**: Provide fine-grained task-level visibility in GitHub issues for detailed progress tracking and team collaboration.

**When to Use**:
- Detailed progress tracking (per-task updates)
- Team collaboration on specific tasks
- Task assignments via GitHub
- Blocking issue tracking
- Task-level comments and discussions

**Integration**: Works with `github-sync` skill and `/sw:github:*` commands

---

## How Task Tracking Works

### 1. Task Checklist in GitHub Issue

When creating an increment issue, automatically add task checklist:

```markdown
## Tasks

### Week 1: Foundation (12 tasks)

- [ ] T-001: Create plugin type definitions (6h) @developer1
- [ ] T-002: Create plugin manifest schema (4h) @developer1
- [ ] T-003: Implement PluginLoader (6h) @developer2
- [ ] T-004: Implement PluginManager (8h) @developer2
...

### Week 2: GitHub Plugin (10 tasks)

- [ ] T-013: Create GitHub plugin structure (2h)
- [ ] T-014: Implement github-sync skill (8h)
...
```

**Features**:
- Clickable checkboxes (GitHub native)
- Time estimates in parentheses
- Assignees via @mentions
- Organized by phase/week

### 2. Per-Task Comments

After each task completion, post detailed comment:

```markdown
### ✅ Task Completed: T-007

**Title**: Implement Claude plugin installer
**Estimated**: 8h
**Actual**: 7h
**Assignee**: @developer2

**What Changed**:
- Added `compilePlugin()` method to ClaudeAdapter
- Implemented plugin file copying to `.claude/`
- Added unload and status methods
- Updated adapter interface

**Files Modified**:
- `src/adapters/claude/adapter.ts` (+150 lines)
- `src/adapters/adapter-interface.ts` (+35 lines)

**Tests**:
- ✅ Unit tests passing (12 new tests)
- ✅ Integration test: plugin install/uninstall

**Next Task**: T-008 - Implement Cursor plugin compiler

---

**Progress**: 7/48 tasks (15%) | Week 1: 7/12 complete

🤖 Posted by SpecWeave at 2025-10-30 14:30:00
```

**Benefits**:
- Detailed change log per task
- Time tracking (estimated vs actual)
- File change summary
- Test status
- Context for code reviewers

### 3. Task Assignments

Assign tasks to team members via GitHub:

**Method 1: Task checklist with @mentions**
```markdown
- [ ] T-015: Create test suite (8h) @qa-engineer
```

**Method 2: Issue comments**
```
@developer1 Can you take T-003 and T-004 this week?
```

**Method 3: GitHub Projects**
- Drag tasks to columns (To Do, In Progress, Done)
- Auto-sync with increment status

### 4. Blocking Issues

Track dependencies and blockers:

```markdown
### 🚨 Blocked: T-020

**Task**: Implement Kubernetes plugin
**Blocked By**: #127 (Infrastructure setup incomplete)
**Blocking**: T-021, T-022
**Reason**: Need staging cluster before testing K8s plugin

**Resolution**: Wait for #127 to close, then proceed with T-020

---

**ETA**: Blocked since 2025-10-28, expected resolution by 2025-11-01
```

---

## Configuration

Enable task-level tracking in `.specweave/config.yaml`:

```yaml
plugins:
  settings:
    specweave-github:
      # Task-level tracking
      task_tracking:
        enabled: true

        # Post comment after each task
        post_task_comments: true

        # Update checklist after each task
        update_checklist: true

        # Include file changes in comments
        include_file_changes: true

        # Include time tracking
        include_time_tracking: true

        # Auto-assign tasks based on git author
        auto_assign: true

      # Blocking issue detection
      blocking_issues:
        enabled: true

        # Check for blocking keywords in task descriptions
        keywords: ["blocked by", "depends on", "requires"]
```

---

## Commands

### Check Task Status

```bash
/sw:github:status 0004
```

Output:
```
GitHub Issue: #130
Status: Open (In Progress)

Tasks: 7/48 completed (15%)

Week 1: Foundation
✅ T-001: Create plugin types (Done)
✅ T-002: Create manifest schema (Done)
✅ T-003: Implement PluginLoader (Done)
✅ T-004: Implement PluginManager (Done)
✅ T-005: Implement PluginDetector (Done)
✅ T-006: Update adapter interface (Done)
✅ T-007: Implement Claude installer (Done)
⏳ T-008: Implement Cursor compiler (In Progress)
⏸️ T-009: Implement Copilot compiler (Pending)
```

### Sync Task Checklist

```bash
/sw:github:sync 0004 --tasks
```

Updates GitHub issue checklist to match current increment progress.

### Comment on Task

```bash
/sw:github:comment 0004 T-008 "Cursor adapter completed, moving to testing phase"
```

Posts custom comment to GitHub issue for specific task.

---

## GitHub Labels for Tasks

Automatically apply labels based on task status:

| Label | When Applied | Purpose |
|-------|--------------|---------|
| `in-progress` | First task starts | Increment is actively being worked on |
| `testing` | Implementation tasks done | Ready for QA |
| `blocked` | Task marked as blocked | Needs attention |
| `review-requested` | PR created | Code review needed |
| `ready-for-merge` | Review approved | Can be merged |

---

## Team Collaboration Patterns

### Pattern 1: Daily Standups via GitHub

Team members comment on tasks with daily updates:

```markdown
**@developer1** on T-008:
Yesterday: Implemented Cursor adapter skeleton
Today: Adding plugin compilation logic
Blockers: None

**@developer2** on T-014:
Yesterday: Created github-sync skill
Today: Testing sync workflow
Blockers: Waiting for #130 review
```

### Pattern 2: Code Review Integration

Link PRs to tasks:

```markdown
### T-007: Claude plugin installer

**PR**: #45
**Status**: Ready for review
**Reviewers**: @tech-lead, @architect

**Changes**:
- Implemented plugin support in Claude adapter
- Added comprehensive tests
- Updated documentation

**Review Checklist**:
- [ ] Code quality (clean, readable)
- [ ] Test coverage (80%+)
- [ ] Documentation updated
- [ ] No security issues
```

### Pattern 3: Task Handoff

Transfer task ownership:

```markdown
@developer1 → @developer2 (T-015)

**Context**:
- Tests framework configured
- Need to write E2E tests for plugin system
- Reference: T-007 implementation

**Handoff Notes**:
- Use Playwright for E2E tests
- Cover happy path + error scenarios
- See `.specweave/increments/0004/tests.md` for test cases
```

---

## Time Tracking

### Automatic Time Tracking

Track time spent on tasks:

```yaml
# .specweave/increments/0004-plugin-architecture/.metadata.yaml
tasks:
  T-007:
    estimated_hours: 8
    actual_hours: 7
    started_at: 2025-10-30T10:00:00Z
    completed_at: 2025-10-30T17:00:00Z
    assignee: developer2
```

### Time Reports

Generate time reports:

```bash
/sw:github:time-report 0004
```

Output:
```
Time Report: Increment 0004

Estimated: 240 hours (6 weeks)
Actual: 56 hours (1.4 weeks)
Remaining: 184 hours (4.6 weeks)

By Developer:
- developer1: 24h (5 tasks)
- developer2: 32h (2 tasks)

By Phase:
- Week 1 Foundation: 56h / 96h (58%)
- Week 2 GitHub Plugin: 0h / 80h (0%)
- Week 3 Plugins: 0h / 120h (0%)
- Week 4 Docs: 0h / 88h (0%)

Pace: On track (4% ahead of schedule)
```

---

## GitHub Projects Integration

### Automated Kanban Board

Sync increment tasks with GitHub Projects:

**Board Columns**:
1. **Backlog**: Pending tasks
2. **Ready**: Tasks ready to start
3. **In Progress**: Currently being worked on
4. **Review**: PRs open, needs review
5. **Done**: Completed tasks

**Auto-Move Rules**:
- Task starts → Move to "In Progress"
- PR created → Move to "Review"
- PR merged → Move to "Done"

### Milestone Tracking

Link increments to GitHub Milestones:

```yaml
# .specweave/config.yaml
plugins:
  settings:
    specweave-github:
      milestones:
        "v0.4.0":
          increments:
            - 0004-plugin-architecture
            - 0005-user-authentication
          due_date: 2025-11-30
```

GitHub Milestone view shows progress across multiple increments.

---

## Advanced Features

### Task Dependencies

Define task dependencies in `tasks.md`:

```markdown
### T-008: Implement Cursor compiler

**Dependencies**: T-006, T-007
**Blocks**: T-011, T-012

**Description**: ...
```

SpecWeave enforces dependency order and warns if attempting blocked task.

### Subtasks

Break complex tasks into subtasks:

```markdown
### T-014: Implement github-sync skill (8h)

**Subtasks**:
- [ ] T-014.1: Create SKILL.md (1h)
- [ ] T-014.2: Implement export (increment → issue) (3h)
- [ ] T-014.3: Implement import (issue → increment) (2h)
- [ ] T-014.4: Add progress updates (1h)
- [ ] T-014.5: Write tests (1h)
```

Subtasks appear as nested checkboxes in GitHub issue.

### External Issue Links

Reference external blocking issues:

```markdown
### T-020: Kubernetes plugin

**Blocked By**:
- #127 (this repo): Infrastructure setup
- https://github.com/kubernetes/kubernetes/issues/12345: K8s API bug

**Resolution Plan**:
1. Wait for #127 (ETA: 2025-11-01)
2. Work around K8s bug using alternative API
```

---

## Notifications

### Task Assignment Notifications

GitHub automatically notifies assignees:

```
@developer1 you were assigned T-015 in #130
```

### Blocking Notifications

Notify blocked task assignees when blocker resolves:

```
@developer2 Task T-020 is unblocked (#127 was closed)
```

### Deadline Reminders

Warn when tasks are behind schedule:

```
⚠️ T-008 is 2 days overdue (estimated: 2 days, actual: 4 days)
```

---

## Troubleshooting

**Checklist not updating?**
- Verify `update_checklist: true` in config
- Check GitHub API permissions (repo write access)
- Manually sync: `/sw:github:sync 0004 --tasks`

**Comments not posting?**
- Check `post_task_comments: true`
- Verify GitHub CLI authenticated: `gh auth status`
- Check rate limits: `gh api rate_limit`

**Time tracking inaccurate?**
- Verify task timestamps in `.metadata.yaml`
- Check for manual edits to metadata
- Re-sync: `/sw:github:sync 0004 --force`

---

## Best Practices

1. **Keep Tasks Atomic**: Each task should be completable in one work session (2-8 hours)
2. **Update Checklists Daily**: Sync progress at least once per day
3. **Use Assignees**: Assign tasks to specific developers for accountability
4. **Track Blockers**: Immediately flag blocking issues for visibility
5. **Link PRs**: Always reference task ID in PR title (`T-007: Add plugin support`)
6. **Comment Context**: Add context comments when handing off tasks
7. **Review Time Estimates**: Adjust estimates based on actual time tracked

---

## Related

- **github-sync**: High-level increment ↔ issue synchronization
- **github-manager agent**: AI agent for GitHub operations
- **Commands**: All `/sw:github:*` commands

---

**Version**: 1.0.0
**Plugin**: specweave-github
**Last Updated**: 2025-10-30
