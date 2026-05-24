---
description: Review pull requests including bot suggestions and CI checks
triggers:
  - review pr
  - check pr
  - review pull request
  - checkout pr
  - check pull request
  - review github pr
---

# Pull Request Review Workflow

Complete workflow for reviewing pull requests, including checking out the code, reviewing bot suggestions, and verifying builds.

## Quick PR Checkout

```bash
# Checkout a PR by number
gh pr checkout <PR_NUMBER>

# View PR details
gh pr view <PR_NUMBER>

# Check CI/build status
gh pr checks <PR_NUMBER>
```

## Full Review Process

### 1. Fetch PR Information

```bash
# View PR description and metadata
gh pr view <PR_NUMBER>

# View PR diff
gh pr diff <PR_NUMBER>

# List all PR comments
gh pr view <PR_NUMBER> --comments
```

### 2. Checkout PR Code

```bash
# Checkout the PR branch
gh pr checkout <PR_NUMBER>

# Verify you're on the correct branch
git branch --show-current
```

### 3. Review Bot Comments **CAREFULLY**

**CRITICAL:** Bot suggestions require careful human evaluation.

When reviewing bot comments (from GitHub bots, linters, or AI assistants):

#### DO:
- ✅ Read each suggestion carefully and understand what it's proposing
- ✅ Evaluate whether the suggestion improves code quality
- ✅ Check if the suggestion aligns with project coding standards
- ✅ Verify the suggestion doesn't break functionality
- ✅ Test changes if accepting bot suggestions
- ✅ Consider context the bot might not understand

#### DON'T:
- ❌ Accept all bot suggestions blindly
- ❌ Assume the bot understands project-specific conventions
- ❌ Let the bot override your engineering judgment
- ❌ Accept suggestions that reduce code clarity
- ❌ Apply suggestions without understanding them

#### Common Bot Suggestion Categories:

1. **Code Style/Formatting**
   - Usually safe to accept if consistent with project style
   - Verify it doesn't conflict with existing patterns

2. **Performance Optimizations**
   - Evaluate whether the optimization is meaningful
   - Check for potential side effects or edge cases

3. **Security/Bug Fixes**
   - These are high-priority but verify the fix is correct
   - Ensure the fix doesn't introduce new issues

4. **Refactoring Suggestions**
   - Consider whether the refactoring improves readability
   - Check if it aligns with project architecture

5. **Dependency Updates**
   - Verify compatibility with existing code
   - Check for breaking changes in changelogs

### 4. Check Build Status

```bash
# Check all CI checks
gh pr checks <PR_NUMBER>

# List recent workflow runs
gh run list --limit 5

# View specific workflow run
gh run view <RUN_ID>
```

### 5. Test Locally

**For firmware changes:**
```bash
cd inav
./build.sh SITL  # or specific target
```

**For configurator changes:**
```bash
cd inav-configurator
NODE_ENV=development npm start
```

### 6. Review Checklist

Use this checklist when reviewing PRs:

- [ ] Code follows project conventions and style
- [ ] Changes are well-documented (comments, commit messages)
- [ ] No unnecessary or debug code left in
- [ ] All CI checks passing
- [ ] Bot suggestions reviewed and valid ones addressed
- [ ] Invalid bot suggestions documented/dismissed
- [ ] Changes tested locally if significant
- [ ] No breaking changes (or properly documented if unavoidable)
- [ ] Related issues/PRs referenced

## Viewing PR Comments

```bash
# View all comments including bot suggestions
gh api repos/iNavFlight/inav/pulls/<PR_NUMBER>/comments

# For configurator repo
gh api repos/iNavFlight/inav-configurator/pulls/<PR_NUMBER>/comments
```

## Adding Review Comments

```bash
# Leave a review comment
gh pr review <PR_NUMBER> --comment -b "Your comment here"

# Approve PR
gh pr review <PR_NUMBER> --approve -b "LGTM! Changes look good."

# Request changes
gh pr review <PR_NUMBER> --request-changes -b "Please address..."
```

## Common Review Scenarios

### Bot Suggested Too Many Changes

If a bot has suggested many changes:
1. Group suggestions by category (style, performance, bugs)
2. Evaluate each category separately
3. Accept valid categories as a group
4. Document why certain suggestions were rejected
5. Provide clear feedback to PR author

### Build Failures

If CI checks are failing:
1. Check `gh pr checks <PR_NUMBER>` for specific failures
2. View workflow logs: `gh run view <RUN_ID> --log`
3. Reproduce locally if needed
4. Provide specific guidance on fixes

### Merge Conflicts

If PR has conflicts:
1. PR author should resolve conflicts
2. Verify conflict resolution doesn't break functionality
3. Re-test after conflicts are resolved

## After Review

```bash
# Return to your working branch
git checkout <YOUR_BRANCH>

# Or return to master
git checkout master
```

## Example Review Workflow

```bash
# 1. Check out PR #2433
gh pr checkout 2433

# 2. View PR and comments
gh pr view 2433 --comments

# 3. Review bot suggestions carefully
# (Read through comments, evaluate each suggestion)

# 4. Check builds
gh pr checks 2433

# 5. Test locally
cd inav-configurator
NODE_ENV=development npm start

# 6. Leave review
gh pr review 2433 --approve -b "Reviewed bot suggestions. Accepted valid ones, documented rejected ones. Code looks good!"

# 7. Return to your branch
git checkout master
```

## Resources

- **GitHub CLI docs:** `gh pr --help`
- **Project review guidelines:** Check `claude/COMMUNICATION.md` for standards
- **Recent PR reviews:** See `claude/projects/review-pr*/` for examples

---

## Related Skills

- **git-workflow** - Checkout PR branches and manage git operations
- **create-pr** - Create your own pull requests
- **check-builds** - Check CI build status for PRs under review
- **run-configurator** - Test configurator PRs locally
- **build-sitl** - Build and test firmware PRs
