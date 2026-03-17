---
name: locu
description: Manage tasks and projects via Locu's Public API.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎯",
        "requires": { "env": ["LOCU_API_TOKEN"] },
        "primaryEnv": "LOCU_API_TOKEN",
      },
  }
---

# Locu Skill

Use the Locu Public API to interact with your workspace.

## Authentication
- `LOCU_API_TOKEN`: Your Personal Access Token (PAT).

## Commands

### User Info
- Get my info: `curl -X GET "https://api.locu.app/api/v1/me" -H "Authorization: Bearer $LOCU_API_TOKEN"`

### Tasks
- List tasks: `curl -X GET "https://api.locu.app/api/v1/tasks" -H "Authorization: Bearer $LOCU_API_TOKEN"`

### Projects
- List projects: `curl -X GET "https://api.locu.app/api/v1/projects" -H "Authorization: Bearer $LOCU_API_TOKEN"`

## Usage Notes
Always parse the JSON output to extract details about tasks (id, name, done status, type). Locu tasks can be native or integrated from Linear/Jira.
