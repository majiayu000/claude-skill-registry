---
name: git-pull-request
description: Use when creating a pull request.
---

# Creating Pull Requests

## Process

1. **Analyze changes:** Call the `fetch_feature_branch` tool to get the current branch's changes. If there are no changes, stop.

2. **Check for Linear issue:** Run `./scripts/extract-issue-from-current-branch.sh` to check if the current branch has a Linear issue ID. If it outputs an issue ID, fetch the Linear issue using the Linear MCP.

3. **Create PR title:** Write a clear, descriptive title that explains what the PR accomplishes. Often this will be a slightly reworked version of the Linear issue title. If there's a Linear issue, prepend the title with the issue ID in square brackets.

   Examples:
   - Add user profile management system
   - Update API documentation with examples
   - [IAM-12] Resolve authentication timeout issues
   - [AI-345] Simplify database connection logic

4. **Create PR description:** Write a concise description focused on essential information. Keep it brief and focused.
   - Check for a PR template at `.github/pull_request_template.md`
     - If it exists, use it:
       - If the PR contains a checklist, review each item and determine completion. Ask user if unsure. Remove the checklist section when done.
       - Remove merging instructions or generic template text
       - Keep screenshots/demo sections but leave them empty
     - If no template exists, create a simple description with Summary and Changes sections:
       - **Summary:** Short paragraph explaining what changed and why
       - **Changes:** Bulleted list of key modifications
   - For simple changes, use a single paragraph summary only
   - Focus on what changed and why, not implementation details
   - Use backticks for code terms, file names, and technical references

5. **Present for review:** Show the proposed PR title and body to the user. Display them clearly formatted and ask if they'd like to proceed or make changes.

6. **Create PR:** After user approval:
   - Push commits: `git push`
   - Create PR: `gh pr create --web --title "<title>" --body "<description>"`
