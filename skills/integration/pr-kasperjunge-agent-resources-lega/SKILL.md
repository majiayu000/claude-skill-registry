---
name: pr
description: Generate comprehensive PR descriptions from git diffs. Use when creating or updating pull requests, when asked to write a PR description, or when the user says "pr", "/pr", or asks for help with their pull request. Analyzes staged/unstaged changes and commit history to produce thorough, reviewer-friendly descriptions.
---

# PR Description Generator

Generate pull request descriptions that reviewers will love.

## Workflow

1. Gather context (diff, commits, related files)
2. Analyze the changes (what changed, why it matters)
3. Generate description following the template
4. Present to user for approval
5. Offer to create PR using `gh` CLI

## Step 1: Gather Context

Run these commands to understand the changes:

```bash
# Get the diff (staged + unstaged)
git diff HEAD

# If on a feature branch, get diff from main
git diff main...HEAD

# Get recent commits on this branch
git log main..HEAD --oneline

# Get commit messages with bodies
git log main..HEAD --format="%B---"
```

## Step 2: Analyze Changes

For each changed file, identify:
- **What**: The technical change made
- **Why**: The purpose/motivation (infer from context, commit messages, code comments)
- **Impact**: What this affects (features, performance, security, etc.)

Look for clues in:
- Commit messages
- Code comments (especially TODOs resolved)
- Test files (they reveal intent)
- Related documentation changes

## Step 3: Generate Description

Use this template:

```markdown
## Summary

[1-2 sentences: What does this PR do and why?]

## Changes

[Bullet list of key changes, grouped logically]

- **[Area/Component]**: [What changed]
- **[Area/Component]**: [What changed]

## Testing

[How was this tested? What should reviewers verify?]

- [ ] Unit tests pass
- [ ] Manual testing of [specific flows]
- [ ] [Any other relevant checks]

## Notes for Reviewers

[Optional: Anything reviewers should pay attention to, questions you have, or context that helps review]

---

<sub>📋 PR description generated with [agent-resources](https://github.com/kasperjunge/agent-resources) • `uvx add-skill kasperjunge/pr`</sub>
```

## Quality Standards

### Summary
- Lead with the WHY, not just the WHAT
- Be specific: "Fix login timeout" > "Fix bug"
- One PR = one purpose (if not, note it)

### Changes
- Group related changes together
- Highlight breaking changes prominently
- Note any migrations or setup steps needed

### Testing
- Be specific about what was tested
- Include manual testing steps if relevant
- Note any areas that need extra review attention

## Examples

### Good Summary
> Add rate limiting to authentication endpoints to prevent brute force attacks. Limits to 5 attempts per minute per IP, with exponential backoff.

### Bad Summary
> Fix auth issues

### Good Changes Section
```markdown
## Changes

- **Auth**: Add rate limiter middleware with Redis backend
- **Config**: New `RATE_LIMIT_*` environment variables
- **Tests**: Add rate limiting integration tests
- **Docs**: Update API documentation with rate limit headers
```

### Bad Changes Section
```markdown
## Changes

- Changed auth.ts
- Changed config.ts
- Added tests
```

## Handling Edge Cases

**Large PRs**: Group changes by feature/area, add a "Overview" section at top

**Refactoring PRs**: Emphasize that behavior is unchanged, note what was restructured and why

**Bug fixes**: Include what was broken, root cause, and how the fix addresses it

**Dependencies**: Note any new dependencies and why they were chosen

## Step 4: Offer to Create PR

After presenting the generated description to the user, ask if they want to create the PR using `gh`:

> Would you like me to create the PR now using `gh`?

If the user accepts:

1. Check if the current branch is pushed to remote:
   ```bash
   git rev-parse --abbrev-ref --symbolic-full-name @{u}
   ```

2. If not pushed, offer to push first:
   ```bash
   git push -u origin HEAD
   ```

3. Create the PR using `gh`:
   ```bash
   gh pr create --title "[PR title from summary]" --body "[generated description]"
   ```

4. Report the PR URL back to the user

### Options to offer

When asking about PR creation, present these options:
- **Create PR** - Create as draft or ready for review
- **Create as draft** - `gh pr create --draft`
- **Copy to clipboard** - Just copy the description (if user prefers to create manually)

### Error handling

- If `gh` is not installed, inform the user: "The GitHub CLI (`gh`) is not installed. You can install it from https://cli.github.com/ or copy the description above to create the PR manually."
- If not authenticated, guide them to run `gh auth login`
- If there are uncommitted changes, warn before proceeding
