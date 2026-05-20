---
name: jira:commit
description: Create smart commit linked to Jira issue. Use when the user wants to "commit", "smart commit", "jira commit", or "commit changes".
version: 4.0.0
---

# Jira Smart Commit

Create a git commit linked to a Jira issue with smart commit syntax.

## Usage

```
/jira:commit [issue-key] [message]
```

## Features

- Formats commit with issue key
- Adds work log via smart commit
- Comments on issue
- Can transition issue status
- Links commit to issue

## Smart Commit Syntax

```
[ISSUE-KEY] message #comment text #time 2h #transition "In Progress"
```

## Related Commands

- `/jira:pr` - Create pull request
- `/jira:branch` - Create linked branch
