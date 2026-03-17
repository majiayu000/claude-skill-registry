---
name: publish
description: Commit and publish Quarto project to GitHub Pages. Use when the user wants to publish changes to a Quarto book or website.
user-invocable: true
---

# Publish Quarto Project

When the user invokes `/publish`, commit and publish the Quarto project to GitHub Pages.

## Steps

### 1. Check for Changes

```bash
git status
```

If no changes, inform the user and stop.

### 2. Show What Will Be Committed

List the changed files and ask the user for a commit message, or suggest one based on recent work.

### 3. Commit and Push

```bash
git add .
git commit -m "USER_MESSAGE

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

### 4. Publish to GitHub Pages

```bash
quarto publish gh-pages --no-prompt
```

If quarto is not in PATH, try `/usr/local/bin/quarto`.

### 5. Confirm

Tell the user:
- Commit was created
- Site will be live in 1-3 minutes at the GitHub Pages URL
- Provide the URL if known (check `_quarto.yml` or git remote)

## Notes

- This skill assumes the project is already set up for GitHub Pages (has `gh-pages` branch)
- If `quarto publish` fails, show the error and suggest troubleshooting steps
- The GitHub Pages URL follows the pattern: `https://ORG.github.io/REPO/`