---
name: update-changelog
description: Update the changelog based on commits in the current git branch
allowed-tools: Bash(git *)
---

# Update Changelog

Update the project's changelog based on the commits in the current branch.

## Instructions

1. **Identify the changelog file**
   - Look for `CHANGELOG.md`, `HISTORY.md`, or similar
   - Note the existing format and style

2. **Analyze the current branch**
   - Get the branch name: `git branch --show-current`
   - Get commits since branching from main: `git log main..HEAD --oneline`
   - Read the full commit messages for context: `git log main..HEAD`

3. **Categorize changes**
   - Group commits by type:
     - Added (new features)
     - Changed (modifications to existing features)
     - Fixed (bug fixes)
     - Removed (removed features)
     - Security (security fixes)
     - Deprecated (soon-to-be removed features)

4. **Update the changelog**
   - Add a new "Unreleased" section if needed
   - Write clear, user-facing descriptions (not just commit messages)
   - Follow the existing format and style of the changelog
   - Link to relevant issues/PRs if the project does that

## Examples

- "Update the changelog with my changes"
- "Add my branch changes to CHANGELOG.md"
- "What should I add to the changelog?"
