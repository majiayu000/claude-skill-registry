---
name: pr-summary
description: Generate a PR summary and write to .ai/ pr_summary.md
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Create PR Summary

Generate a pull request summary based on branch changes.

## Instructions

1. **Gather Context**
   - Get current branch name
   - Find the corresponding `.ai/` workflow folder for this branch:
     - For issue branches (e.g., `feature/59-no-verify`): look for `.ai/issue-59-*`
     - For named branches (e.g., `feature/worktree-support`): look for `.ai/feature-worktree-support/` or `.ai/worktree-support/`
     - Use `ls .ai/` and match based on branch name patterns
   - Read these files if they exist (use them to understand the feature goals and implementation approach):
     - `concept.md` - Feature concept and design rationale
     - `analysis.md` - Issue analysis and requirements
     - `plan.md` - Implementation plan with specific changes
   - Get associated issue number from branch name, commits, or analysis.md

2. **Analyze Changes**
   ```bash
   # All commits on this branch
   git log main...HEAD --oneline

   # Full diff
   git diff main...HEAD --stat

   # Changed files
   git diff main...HEAD --name-only
   ```

3. **Generate Summary**

   Read `.github/PULL_REQUEST_TEMPLATE.md` for the format specification and example.

   Use context from the `.ai/` folder files to write a better summary:
   - **concept.md**: Understand the design goals and rationale
   - **analysis.md**: Reference the original issue requirements
   - **plan.md**: Verify all planned changes were implemented

   Write the summary to `.ai/<folder>/pr_summary.md`.

4. **Create PR Command**

   Output the `gh pr create` command:

   ```bash
   gh pr create --title "<title>" --body "$(cat .ai/<folder>/pr_summary.md)"
   ```

5. **Report Completion**
   - Show path to pr_summary.md
   - Show the PR creation command
   - Remind to push branch first if not already pushed

## PR Title Guidelines

- Use imperative mood: "Add feature" not "Added feature"
- Be specific but concise
- Do NOT include the issue number in the title (it will be linked in the PR body)
