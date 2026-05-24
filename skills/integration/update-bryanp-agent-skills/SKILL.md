---
name: github-pr-update
description: Update a pull request in Github
---

Use the `gh pr edit` command to update a pull request.

# Rule: Identity

First use the `identity` skill to assume the identity of the agent.

# Usage

```
Edit a pull request.

Without an argument, the pull request that belongs to the current branch
is selected.

Editing a pull request's projects requires authorization with the `project` scope.
To authorize, run `gh auth refresh -s project`.

The `--add-assignee` and `--remove-assignee` flags both support
the following special values:
- `@me`: assign or unassign yourself
- `@copilot`: assign or unassign Copilot (not supported on GitHub Enterprise Server)

The `--add-reviewer` and `--remove-reviewer` flags support
the following special value:
- `@copilot`: request or remove review from Copilot (not supported on GitHub Enterprise Server)


USAGE
  gh pr edit [<number> | <url> | <branch>] [flags]

FLAGS
      --add-assignee login      Add assigned users by their login. Use "@me" to assign yourself, or "@copilot" to assign Copilot.
      --add-label name          Add labels by name
      --add-project title       Add the pull request to projects by title
      --add-reviewer login      Add reviewers by their login. Use "@copilot" to request review from Copilot.
  -B, --base branch             Change the base branch for this pull request
  -b, --body string             Set the new body.
  -F, --body-file file          Read body text from file (use "-" to read from standard input)
  -m, --milestone name          Edit the milestone the pull request belongs to by name
      --remove-assignee login   Remove assigned users by their login. Use "@me" to unassign yourself, or "@copilot" to unassign Copilot.
      --remove-label name       Remove labels by name
      --remove-milestone        Remove the milestone association from the pull request
      --remove-project title    Remove the pull request from projects by title
      --remove-reviewer login   Remove reviewers by their login. Use "@copilot" to remove review request from Copilot.
  -t, --title string            Set the new title.

INHERITED FLAGS
      --help                     Show help for command
  -R, --repo [HOST/]OWNER/REPO   Select another repository using the [HOST/]OWNER/REPO format

EXAMPLES
  $ gh pr edit 23 --title "I found a bug" --body "Nothing works"
  $ gh pr edit 23 --add-label "bug,help wanted" --remove-label "core"
  $ gh pr edit 23 --add-reviewer monalisa,hubot  --remove-reviewer myorg/team-name
  $ gh pr edit 23 --add-reviewer "@copilot"
  $ gh pr edit 23 --add-assignee "@me" --remove-assignee monalisa,hubot
  $ gh pr edit 23 --add-assignee "@copilot"
  $ gh pr edit 23 --add-project "Roadmap" --remove-project v1,v2
  $ gh pr edit 23 --milestone "Version 1"
  $ gh pr edit 23 --remove-milestone
```
