---
name: push
description: Pushes the current branch to the remote repository.
unsandboxed: true
---

When asked to push code, follow these steps:

1. Run `git status` to verify there are commits to push.

2. Push to the remote repository:

   - Run `git push` to push the commits
   - If the branch has no upstream, use `git push -u origin <branch-name>`

3. Report the results including:
   - The branch name
   - The push status
