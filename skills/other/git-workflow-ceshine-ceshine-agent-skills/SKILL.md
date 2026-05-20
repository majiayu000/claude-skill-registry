---
name: git-workflow
description: "Always invoke this skill for any git-related request (commit messages, staging review, history, PR descriptions, etc.) so git workflows are handled consistently."
---

# Git Workflow

Generate comprehensive pull request descriptions by analyzing git state: staged changes, commit history, and diffs between commits or branches.

## Tool Selection

Try tools with these stems in their names first. Fall back to bash if unavailable (see Error Handling section for procedure):

**MCP tools (preferred):**
- `git-diff(ancestor)` - Get diff from ancestor commit/branch to HEAD
- `git-cached-diff()` - Get staged (cached) changes
- `git-commit-messages(ancestor)` - Get commit messages from ancestor to HEAD
> **IMPORTANT:** Tool names may have prefixes (e.g., `git-tools_git-diff`) depending on the runtime environment. Always check available tools first.

**Bash fallbacks:**
```bash
git diff <ancestor>..HEAD              # Diff between ancestor and HEAD
git diff --cached                      # Staged changes only
git log --oneline <ancestor>..HEAD     # Commit messages from ancestor to HEAD
```

## Operations

### 1. Review Staged Changes

Perform a code review of staged modifications:

1. Get cached changes: `git-cached-diff()` or `git diff --cached`
2. Analyze the diff for:
   - **Syntax errors**: Missing semicolons, brackets, or typos
   - **Logic issues**: Broken conditions, off-by-one errors, null reference risks
   - **Security concerns**: Hardcoded secrets, SQL injection vectors, XSS patterns
   - **Code quality**: Deeply nested blocks, duplicated code, overly complex functions
   - **Missing pieces**: Unhandled edge cases, incomplete error handling
   - **Style inconsistencies**: Deviation from project's coding conventions
3. Summarize findings:
   - Critical issues: Issues that should block the commit
   - Suggestions: Suggestions for improvement
   - Questions: Questions for the author

Present findings clearly, distinguishing between blocking issues and optional suggestions.

### 2. Generate Commit Message Summary

Extract commit messages to understand the history:

**MCP:** `git-commit-messages(ancestor="<commit-or-branch>")`
**Bash:** `git log --oneline <commit-or-branch>..HEAD`

Returns commit hashes and messages, useful for:

- Understanding changes across multiple commits
- Identifying key features/bug fixes
- Creating a changelog-style summary

### 3. Generate Commit Message for Cached/Staged Changes

Create a descriptive commit message based on staged changes through an iterative review process:

1. **Review staged changes** - Perform code review using the process described in the "1. Review Staged Changes" section.
2. **Present findings and wait for feedback** - Show issues and suggestions to user. User may:
  - Edit the staged changes
  - Acknowledge issues if any but proceed
  - Ask for clarification
  - Or simply confirm they have reviewed the findings and approve moving on
  **Only move on to the the next step after an explicit approval from the user**.
3. **Load history** - Load the two most recent commit messages (e.g., `git-commit-messages(ancestor="HEAD~2")`) to ensure historical context.
4. **Draft the commit message** - write it to `./cache/commit_message.txt` in the conventional commit format (remove the file if it already exists before attempting to write to it):
   ```
   <type>(<scope>): <subject>

   <body>

   <footer>
   ```
  - Type: feat, fix, docs, style, refactor, test, chore
  - Scope: (optional) the area of code affected
  - Description: brief explanation of changes
  - Body: detailed description if needed
  - Footer: breaking changes or issue references
5. **Display the commit message** - User may:
  - Request revision
  - Approve the commit message

### 4. Create Pull Request Description

Use the diff and recent commits to compose a structured PR body:

1. Collect the diff for the target branch, preferably against the base (e.g., `origin/main`).
2. Gather its commit messages to capture intent and progression.
3. Extract:
   - **Summary**: A concise paragraph (1-2 sentences) describing the overall intent of the branch.
   - **Key Changes**: Bullet list that highlights the most important file edits or feature additions.
   - **Commit History**: Chronological list of commits (hash + message) so reviewers can trace the work.

Format suggestions:
```markdown
## Summary
[Commit-driven overview]

## Key Changes
- `[File]`: [Primary modification]
- ...
```

#### Workflow Notes

- Identify the merge base (usually `origin/main` or `main`).
- Run `git-diff(ancestor="origin/main")` and `git-commit-messages(ancestor="origin/main")` to gather the data.
- Parse and organize the collected information into the sections above before sharing with the user.

## Error Handling

If git MCP tools are unavailable:

1. Inform the user: "Git MCP tools not detected. These tools provide git diff, cached diff, and commit message functionality."
2. Ask: "Would you like to proceed using bash commands instead?"
3. If user confirms, use the bash fallbacks documented above
4. If user declines, stop the workflow

If git commands fail:

- Verify git repository
- Check ancestor exists (commit hash or branch name)
- Ensure working directory is clean or handle uncommitted changes
