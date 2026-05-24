---
name: pr-summary
description: Generate a pull request summary from the current branch changes
disable-model-invocation: true
---

## Pull request context

- PR diff: !`git diff main...HEAD`
- Changed files: !`git diff main...HEAD --name-only`
- Commit log: !`git log main...HEAD --oneline`

## Your task

Summarize this pull request by:

1. **Title**: Write a concise PR title (under 70 characters)
2. **Summary**: 1-3 bullet points describing what changed and why
3. **Key changes**: Group file changes by area (e.g., API, UI, tests, config)
4. **Testing notes**: Suggest what reviewers should test
5. **Risk assessment**: Low/Medium/High with brief justification

Format the output as a ready-to-use PR description in markdown.
