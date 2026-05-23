---
name: taskstoissues
description: "Convert user stories to GitHub issues. Use when ready to create issues. Triggers on: create github issues, export to github, generate issues."
---

# GitHub Issues Generator

Convert user stories from tasks.md into GitHub issues.

---

## The Job

1. Read tasks.md
2. Parse user stories
3. Generate GitHub issues with `gh` CLI
4. Link dependencies

---

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Git repository with GitHub remote
- tasks.md exists with user stories

---

## Issue Format

For each user story, create issue with:

**Title:** [US-XXX] Story Title

**Body:**
```markdown
## Description
[Story description]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Typecheck passes
- [ ] Tests pass

## Dependencies
#123 (if US-001 already exists as issue #123)

## Phase
Foundation / Stories / Polish

## Priority
High / Medium / Low

---
From: tasks.md
Story ID: US-XXX
```

**Labels:**
- `user-story`
- `priority-high` / `priority-medium` / `priority-low`
- Domain-specific: `database`, `api`, `ui`, `security`, etc.

---

## Execution

```bash
# Dry run first
relentless issues --feature NNN-feature --dry-run

# Create issues
relentless issues --feature NNN-feature

# Create all issues (including completed)
relentless issues --feature NNN-feature --all
```

---

## Mapping

- Extract story ID, title, description, acceptance criteria
- Detect domain from description (api, database, ui, etc.)
- Map priority from tasks.md
- Create dependencies based on US dependencies

---

## Notes

- Dry run first to preview
- Issues created in dependency order
- Issue numbers used for dependency linking
- Only creates issues for incomplete stories (unless --all)
- See relentless CLI for actual implementation
