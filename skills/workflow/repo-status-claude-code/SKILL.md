---
name: repo-status
description: Checks the status of the repository
user-invokable: true
disable-model-invocation: true
---

# Instructions for getting the context
- Commits in the last week: !`git log --oneline --since="last week"`
- Last week top contributors: !`git shortlog -sn --since="last week"`

# Output
If there are more than 5 commits and at least 2 contributors, respond that the repository is in good shape; otherwise, that it’s in bad shape.
