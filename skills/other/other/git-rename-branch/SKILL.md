---
name: git-rename-branch
description: "{{ ƔƔƔ }} Rename branch if needed"
model: sonnet
disable-model-invocation: true
allowed-tools: ["Bash(git:*)"]
argument-hint: ["(optional) desired name"]
---

## Assess and Rename Current Branch

1. If user has specified a new name, apply it; otheriwse, get the current branch name with `git branch --show-current`
2. Get a summary of what's actually been done on this branch:
   - `git log main..HEAD --oneline` to see commits
   - `git diff main..HEAD --name-only` to see changed files
3. Compare the branch name against the actual changes:
   - Does the name still accurately describe the work?
   - Is the scope broader or narrower than the name implies?
   - Does the name follow the `<prefix>/<short-description>` convention?
4. If the name is still accurate, say so and stop
5. If a rename is warranted, suggest a better name and explain why
   - Format: `<prefix>/<short-description>` — all lowercase, hyphens, imperative mood (`add-feature` not `adds-feature` or `adding-feature`)
6. Await approval — if accepted:
   - Rename locally: `git branch -m <new-name>`
   - Rename on remote: `git push origin HEAD:<new-name>` then `git push origin --delete <old-name>`
   - Set upstream: `git branch --set-upstream-to=origin/<new-name>`
