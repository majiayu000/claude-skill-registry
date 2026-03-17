---
name: linear-issue-create
description: Create an issue in Linear
---

Use the `linear issue create` command to create an issue.

# Rule: Identity

First use the `identity` skill to assume the identity of the agent.

# Usage

```
Usage:   linear issue create
Version: 1.10.0

Description:

  Create a linear issue

Options:

  -h, --help                                - Show this help.
  -w, --workspace            <slug>         - Target workspace (uses credentials)
  --start                                   - Start the issue after creation
  -a, --assignee             <assignee>     - Assign the issue to 'self' or someone (by username or name)
  --due-date                 <dueDate>      - Due date of the issue
  -p, --parent               <parent>       - Parent issue (if any) as a team_number code
  --priority                 <priority>     - Priority of the issue (1-4, descending priority)
  --estimate                 <estimate>     - Points estimate of the issue
  -d, --description          <description>  - Description of the issue
  --description-file         <path>         - Read description from a file (preferred for markdown content)
  -l, --label                <label>        - Issue label associated with the issue. May be repeated.
  --team                     <team>         - Team associated with the issue (if not your default team)
  --project                  <project>      - Name of the project with the issue
  -s, --state                <state>        - Workflow state for the issue (by name or type)
  --no-use-default-template                 - Do not use default template for the issue
  --no-interactive                          - Disable interactive prompts
  -t, --title                <title>        - Title of the issue
```
