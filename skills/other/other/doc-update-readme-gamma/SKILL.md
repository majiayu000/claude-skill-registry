---
name: doc-update-readme-gamma
description: "{{ ƔƔƔ }} Update a README to reflect recent changes"
model: sonnet
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Bash(git:*)"]
argument-hint: [path/to/directory (optional, defaults to ./)]
---

Update the README.md in the specified directory (or the project root if none given).

Target directory:

```
$ARGUMENTS
```

If no argument was provided, default to `./README.md`.

## Steps

1. Resolve the target: if an argument was given, look for `README.md` in that directory; otherwise use `./README.md`
2. If the README doesn't exist, stop and suggest using `/doc:create:readme:for` instead
3. Read the existing README to understand its structure and style
4. Review recent changes in the target directory:
   - `git log -15 --oneline -- <directory>`
   - `git diff HEAD~15 -- <directory>` (or fewer commits if the directory has less history)
   - Check for new, renamed, or deleted files
5. Identify what needs updating:
   - Outdated descriptions or references
   - New features, files, or modules not yet documented
   - Removed content that should be cleaned up
   - Structural changes (renamed sections, reorganised files)
6. Generate targeted updates preserving the existing structure and style; show a diff
7. Apply on approval

## Notes

- Match the existing README's tone and formatting
- Don't remove content unless it's genuinely obsolete
- Prefer surgical updates over full rewrites
- If changes are minor, say so — don't invent updates for the sake of it
