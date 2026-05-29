---
name: esper:backlog
description: Show the current backlog of pending and active plans, sorted by priority.
---

Display the current esperkit backlog for this project.

## Steps

1. Run `esperkit config check`. If it exits non-zero, tell the user to run `/esper:init` first and stop.

2. Run the backlog display subcommand:
   ```bash
   esperkit backlog
   ```
   Print the output verbatim. Shows ACTIVE, PENDING, and DONE (last 3) sections.

3. Run `esperkit config get backlog_mode`. If the output is `github`, also run:
   ```bash
   gh issue list --state open --json number,title,labels
   ```
   Cross-reference open issues with: the current phase file's `gh_issue` field (parent issue), and all plan files' `gh_issue` fields (sub-issues of the phase). Flag any open GitHub issues that have no matching phase or plan.

4. Print at the bottom:
   - Current phase: run `esperkit config get current_phase` and display as `Phase: <output>`
   - Tips: `/esper:apply` to start the top item · `/esper:plan` to add a feature · `/esper:fix` to log a bug
