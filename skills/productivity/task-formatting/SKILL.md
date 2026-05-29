---
name: task-formatting
description: Format and structure tasks for ClickUp and Linear including priority calculation, status mapping, and task templates. Use when creating or updating tasks across project management systems.
---

# Task Formatting

Tools for formatting and structuring tasks for ClickUp, Linear, and other project management systems.

## Quick Start

Format ClickUp task:
```bash
python scripts/format_clickup_task.py --title "Add feature" --description desc.md --priority high --output task.json
```

Format Linear issue:
```bash
python scripts/format_linear_issue.py --title "Fix bug" --description "Bug details" --team-id abc123 --output issue.json
```

Calculate priority:
```bash
python scripts/calculate_priority.py --urgency high --impact high --effort low
```

## Task Formatting Patterns

### 1. ClickUp Task Format

**Standard task structure:**
```json
{
  "name": "Task Title",
  "description": "Detailed description with markdown",
  "priority": 2,
  "status": "to do",
  "tags": ["bug", "urgent"],
  "assignees": [123456],
  "due_date": "2026-01-20",
  "time_estimate": 3600000
}
```

**Priority levels:**
- `1` = Urgent (red)
- `2` = High (orange)
- `3` = Normal (yellow)
- `4` = Low (gray)

**Common statuses:**
- `to do`
- `in progress`
- `review`
- `done`

### 2. Linear Issue Format

**Standard issue structure:**
```json
{
  "title": "Issue Title",
  "description": "Detailed description with markdown",
  "priority": 1,
  "teamId": "abc123",
  "assigneeId": "user-id",
  "labelIds": ["label-1", "label-2"],
  "stateId": "state-id",
  "estimate": 3
}
```

**Priority levels:**
- `0` = No priority
- `1` = Urgent
- `2` = High
- `3` = Normal
- `4` = Low

**Common states:**
- `Backlog`
- `Todo`
- `In Progress`
- `In Review`
- `Done`
- `Canceled`

## Priority Calculation

### Formula

Calculate task priority based on multiple factors:

```
Priority Score = (Urgency × 3) + (Impact × 2) + (Effort × -1)

Where:
- Urgency: 1-5 (how soon it needs to be done)
- Impact: 1-5 (how many people/systems affected)
- Effort: 1-5 (how much work required)
```

**Mapping to priority levels:**
- Score ≥ 15: Urgent (Priority 1)
- Score 10-14: High (Priority 2)
- Score 5-9: Normal (Priority 3)
- Score < 5: Low (Priority 4)

### Examples

**Bug affecting production:**
```
Urgency: 5 (needs immediate fix)
Impact: 5 (all users affected)
Effort: 2 (quick fix)

Score = (5 × 3) + (5 × 2) + (2 × -1) = 15 + 10 - 2 = 23
Priority: Urgent (1)
```

**Feature request:**
```
Urgency: 2 (can wait)
Impact: 3 (some users want it)
Effort: 4 (significant work)

Score = (2 × 3) + (3 × 2) + (4 × -1) = 6 + 6 - 4 = 8
Priority: Normal (3)
```

**Technical debt:**
```
Urgency: 1 (no rush)
Impact: 2 (affects developers only)
Effort: 3 (moderate work)

Score = (1 × 3) + (2 × 2) + (3 × -1) = 3 + 4 - 3 = 4
Priority: Low (4)
```

## Status Mapping

### ClickUp ↔ Linear Mapping

```python
STATUS_MAP = {
    # ClickUp → Linear
    "to do": "Todo",
    "in progress": "In Progress",
    "review": "In Review",
    "done": "Done",
    "blocked": "Blocked",

    # Linear → ClickUp
    "Backlog": "to do",
    "Todo": "to do",
    "In Progress": "in progress",
    "In Review": "review",
    "Done": "done",
    "Canceled": "closed"
}
```

### GitHub Issues ↔ ClickUp/Linear

```python
GITHUB_STATUS_MAP = {
    # GitHub → ClickUp/Linear
    "open": "to do",
    "in_progress": "in progress",
    "closed": "done",

    # ClickUp/Linear → GitHub
    "to do": "open",
    "in progress": "open",
    "review": "open",
    "done": "closed"
}
```

## Task Templates

### Bug Report

```markdown
# Bug Report

## Description
[Brief description of the bug]

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- Browser/Device:
- OS:
- Version:

## Screenshots
[If applicable]

## Additional Context
[Any other relevant information]
```

### Feature Request

```markdown
# Feature Request

## Problem Statement
[What problem does this solve?]

## Proposed Solution
[How should we solve it?]

## Alternatives Considered
[What other approaches did you consider?]

## User Stories
- As a [role], I want [feature] so that [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Notes
[Any technical considerations]
```

### Task

```markdown
# Task

## Objective
[What needs to be done?]

## Context
[Why is this important?]

## Steps
1. Step one
2. Step two
3. Step three

## Definition of Done
- [ ] Implementation complete
- [ ] Tests written
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] Merged to main
```

## Scripts

### format_clickup_task.py

Format a task for ClickUp.

**Usage:**
```bash
python scripts/format_clickup_task.py \
    --title "Add user authentication" \
    --description description.md \
    --priority high \
    --tags "feature,auth" \
    --due-date "2026-01-20" \
    --estimate 4h \
    --output task.json
```

**Arguments:**
- `--title`: Task title (required)
- `--description`: Description text or markdown file
- `--priority`: Priority level (urgent, high, normal, low)
- `--tags`: Comma-separated tags
- `--due-date`: Due date (YYYY-MM-DD)
- `--estimate`: Time estimate (e.g., "4h", "2d")
- `--output`: Output JSON file

### format_linear_issue.py

Format an issue for Linear.

**Usage:**
```bash
python scripts/format_linear_issue.py \
    --title "Fix login bug" \
    --description "Users can't login" \
    --team-id "team-abc" \
    --priority urgent \
    --labels "bug,auth" \
    --estimate 3 \
    --output issue.json
```

**Arguments:**
- `--title`: Issue title (required)
- `--description`: Description text
- `--team-id`: Team ID (required)
- `--priority`: Priority level (urgent, high, normal, low)
- `--labels`: Comma-separated labels
- `--estimate`: Story points (1-5)
- `--output`: Output JSON file

### calculate_priority.py

Calculate task priority based on factors.

**Usage:**
```bash
python scripts/calculate_priority.py \
    --urgency 5 \
    --impact 4 \
    --effort 2 \
    --format clickup
```

**Arguments:**
- `--urgency`: Urgency level (1-5)
- `--impact`: Impact level (1-5)
- `--effort`: Effort level (1-5)
- `--format`: Output format (clickup, linear)

**Output:**
```json
{
  "score": 23,
  "priority": 1,
  "priority_label": "Urgent",
  "recommendation": "Address immediately",
  "factors": {
    "urgency": 5,
    "impact": 4,
    "effort": 2
  }
}
```

## Task Metadata

### Labels/Tags

**Bug-related:**
- `bug` - General bug
- `critical-bug` - Severe bug affecting many users
- `minor-bug` - Small issue with workaround

**Feature-related:**
- `feature` - New feature
- `enhancement` - Improvement to existing feature
- `refactor` - Code improvement without new functionality

**Type:**
- `documentation` - Documentation update
- `test` - Test-related
- `ci/cd` - CI/CD pipeline
- `security` - Security-related
- `performance` - Performance improvement

**Priority:**
- `urgent` - Needs immediate attention
- `high-priority` - Important but not urgent
- `low-priority` - Can wait

### Time Estimates

**ClickUp** (milliseconds):
- 1 hour = 3,600,000
- 2 hours = 7,200,000
- 4 hours = 14,400,000
- 1 day = 28,800,000 (8 hours)

**Linear** (story points):
- 1 point = ~2 hours
- 2 points = ~4 hours
- 3 points = ~1 day
- 5 points = ~2 days
- 8 points = ~1 week

**Helper function:**
```python
def parse_time_estimate(estimate_str: str) -> int:
    """
    Parse time estimate string to milliseconds.

    Examples:
        "2h" → 7,200,000
        "1d" → 28,800,000
        "30m" → 1,800,000
    """
```

## Integration with Agents

### Automation Agent

```python
from task_formatting import format_clickup_task, calculate_priority

# Calculate priority
priority_data = calculate_priority(urgency=5, impact=4, effort=2)

# Format task
task = format_clickup_task(
    title="Fix critical bug",
    description="Bug description",
    priority=priority_data['priority'],
    tags=['bug', 'urgent']
)

# Create in ClickUp
clickup_client.create_task(
    list_id='list-123',
    **task
)
```

### Code Agent

```python
from task_formatting import format_linear_issue

# Create issue from GitHub PR
issue = format_linear_issue(
    title=pr['title'],
    description=pr['body'],
    team_id='team-abc',
    priority='normal',
    labels=['pr-review']
)

# Create in Linear
linear_client.create_issue(**issue)
```

## Best Practices

### Task Titles
- Start with verb (Add, Fix, Update, Refactor)
- Be specific and concise
- Include context when needed
- 50-70 characters maximum

**Good:**
- "Add user authentication with OAuth"
- "Fix login redirect bug on mobile"
- "Update payment processing to Stripe API v2"

**Bad:**
- "Auth" (too vague)
- "Fix bug" (not specific)
- "Update the entire payment processing system to use the new Stripe API version 2 with improved error handling" (too long)

### Task Descriptions
- Start with problem statement
- Include context and background
- List acceptance criteria
- Add technical notes if needed
- Link to related tasks/docs

### Priority Assignment
- Don't make everything urgent
- Consider actual impact
- Factor in effort required
- Review priorities regularly
- Use data when available

### Status Updates
- Update status promptly
- Add comments for blockers
- Tag people when needed
- Close completed tasks
- Archive old tasks

## Examples

See `templates/` directory for example tasks:
- `bug_report_template.json`
- `feature_request_template.json`
- `task_template.json`
