---
name: describing-PRs
description: Generate a PR description for the current branch. Writes Markdown to .git/magit/posts/new-pullreq for use with magit-forge.
allowed-tools: Bash(~/.claude/skills/describing-PRs/scripts/find-merge-base.py:*)
---

# PR Description Generator

Generate a well-structured PR description for the current feature branch.

## When to Use This Skill

Use this skill when:

- Preparing to create a pull request
- Needing a PR description for the current branch
- Integrating with magit-forge for PR creation

## Process

1. **Determine the base branch**

   Run the helper script to find the base branch:

   ```bash
   BASE=$(~/.claude/skills/describing-PRs/scripts/find-merge-base.py)
   ```

   The script outputs a branch name (e.g., `origin/main`) that represents
   the base branch for comparison. It handles cases where you branched
   from another feature branch, not just main/master.

   **Options**:
   - `--fetch`: Fetch latest remote refs before determining base branch
   - `--debug`: Show how the base branch is determined

   **Strategy** (implemented in the script):
   - Try `@{upstream}` first (the current branch's configured upstream)
   - Try `origin/HEAD` (the remote's default branch)
   - Fall back to common defaults: `origin/main`, `origin/master`, `origin/develop`
   - If neither works, find the closest remote branch by commit distance

2. **Gather context about the branch**

   Using the base branch found above:

   ```bash
   git branch --show-current
   git log --oneline <base-branch>..HEAD
   git diff --no-ext-diff <base-branch>..HEAD --stat
   git diff --no-ext-diff <base-branch>..HEAD
   ```

3. **Analyze the changes**

   - Identify the purpose of the changes
   - Group related commits by theme
   - Note any breaking changes or important considerations

4. **Generate the PR description**

   Write a Markdown file with:

   - **Title**: A concise summary (will be used as PR title)
   - **Summary**: 2-3 sentences explaining the overall purpose
   - **Changes**: Bullet points of key modifications
   - **Testing**: How the changes were tested (if applicable)
   - **Notes**: Any reviewer notes, breaking changes, or follow-up items

5. **Write to the output file**

   Create the directory and write the description:
   ```bash
   mkdir -p .git/magit/posts
   ```

   Write Markdown content to `.git/magit/posts/new-pullreq`

## Output Format

The generated file should follow this structure:

```markdown
# <PR Title>

## Summary

<Brief explanation of what this PR accomplishes and why>

## Changes

- <Key change 1>
- <Key change 2>
- ...

## Testing

<How changes were tested, or "N/A" if not applicable>

## Notes

<Any additional context for reviewers, breaking changes, or follow-up work>
```

## Formatting Guidelines

- Wrap all symbols, variables, function names, file paths, and code references
  in backticks (e.g., `myFunction`, `CONFIG_VALUE`, `src/utils.ts`)
- Use fenced code blocks for multi-line code snippets
- Keep bullet points concise and scannable

## Important Notes

- The file path `.git/magit/posts/new-pullreq` is used by magit-forge
- Always overwrite the existing file if present
- Keep the description concise but informative
- Focus on the "why" more than the "what" (the diff shows the "what")
