---
name: jira:pr
description: Create pull request linked to Jira issue. Use when the user wants to "create PR", "open pull request", "submit for review", or "jira pr".
version: 4.0.0
---

# Jira Pull Request Creation

Create a pull request linked to a Jira issue with proper formatting and linking.

## Usage

```
/jira:pr <issue-key>
```

## Features

- Creates GitHub PR
- Links PR to Jira issue
- Adds Jira issue key to title
- Generates comprehensive description
- Requests reviewers
- Transitions issue to "In Review"

## Related Commands

- `/jira:commit` - Create smart commit first
- `/jira:review` - Request code review
