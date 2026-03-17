---
name: linear-issue-view
description: View an issue in Linear
---

Use the `linear issue view` command to view an issue.

# Rule: Identity

First use the `identity` skill to assume the identity of the agent.

# Usage

```
Usage:   linear issue view [issueId]
Version: 1.10.0

Description:

  View issue details (default) or open in browser/app

Options:

  -h, --help               - Show this help.
  -w, --workspace  <slug>  - Target workspace (uses credentials)
  -w, --web                - Open in web browser
  -a, --app                - Open in Linear.app
  --no-comments            - Exclude comments from the output
  --no-pager               - Disable automatic paging for long output
  -j, --json               - Output issue data as JSON
  --no-download            - Keep remote URLs instead of downloading files
```
