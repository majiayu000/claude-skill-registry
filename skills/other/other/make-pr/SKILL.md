---
name: make-pr
description: Creates pull requests on GitHub or Azure DevOps by analyzing commits and generating descriptions. Detects platform from git remote and uses gh CLI or az CLI. Use when asked to create PR, open PR, make pull request, submit PR, create pull request, new PR, raise PR, push PR, open pull request, submit changes, PR workflow, or when user mentions PR creation. Generates casual, context-aware PR descriptions that explain WHY not WHAT.
compatibility: Requires git repository, gh CLI for GitHub or az CLI + azure-devops extension for Azure DevOps
allowed-tools: Bash
metadata:
  author: Saturate
  version: "1.3"
---

You are helping the user create a pull request on GitHub or Azure DevOps. Follow these steps:

## Progress Checklist

Copy this checklist to track your progress through the workflow:

```
PR Creation Progress:
- [ ] Step 0: Verified prerequisites (git repo, platform, CLI tools, auth)
- [ ] Step 1: Parsed user arguments
- [ ] Step 2: Got current state (branch, remote, target branch)
- [ ] Step 3: Analyzed commits (found commits to PR)
- [ ] Step 4: Generated PR title and description
- [ ] Step 5: Confirmed PR content with user
- [ ] Step 6: Created PR successfully
- [ ] Step 7: Displayed PR URL and details
```

## Step 0: Prerequisites Check

1. **Verify this is a git repository:**
   ```bash
   git rev-parse --git-dir 2>/dev/null
   ```
   If this fails, exit with: "Not a git repository"

2. **Detect platform from git remote:**
   ```bash
   remote_url=$(git config --get remote.origin.url)
   ```
   - If contains `github.com` → Platform is **GitHub**
   - If contains `dev.azure.com` or `visualstudio.com` → Platform is **Azure DevOps**
   - Otherwise → Exit with: "Unsupported git remote. This skill supports GitHub (github.com) or Azure DevOps (dev.azure.com)"

3. **Check CLI tool is installed:**
   - **GitHub:** `command -v gh >/dev/null 2>&1`
     - If missing → See [references/github-pr.md](references/github-pr.md#installation) for installation instructions
   - **Azure DevOps:** `command -v az >/dev/null 2>&1 && az extension show -n azure-devops >/dev/null 2>&1`
     - If missing → See [references/azure-pr.md](references/azure-pr.md#installation) for installation instructions

4. **Check authentication:**
   - **GitHub:** `gh auth status`
     - If not authenticated → See [references/github-pr.md](references/github-pr.md#authentication)
   - **Azure DevOps:** `az account show >/dev/null 2>&1`
     - If not authenticated → See [references/azure-pr.md](references/azure-pr.md#authentication)

## Step 1: Parse Arguments

**User input format:**

Users invoke this skill with: `/make-pr [arguments]`

Parse any arguments provided after the skill name. Common patterns:
- `/make-pr` - No arguments, auto-generate everything
- `/make-pr --draft` - Boolean flag
- `/make-pr --title "My PR"` - Flag with value
- `/make-pr --draft --reviewers "alice bob"` - Multiple flags

**Supported arguments:**
- `--title "title"` or `-t "title"` - PR title (optional, will be inferred from commits)
- `--description "desc"` or `-d "desc"` - PR description (optional, will be generated)
- `--draft` - Create as draft PR (boolean flag)
- `--base branch` or `-b branch` - Target branch (optional, defaults to repo default branch)
- `--reviewers "user1 user2"` or `-r "user1 user2"` - Space-separated reviewers
- `--labels "label1 label2"` - Space-separated labels (GitHub only)
- `--work-items "123 456"` or `-w "123 456"` - Space-separated work item IDs (Azure only)

**Extract and store values:**

Parse the user's message after `/make-pr` and extract any provided arguments. Store them in variables for use in later steps:

```bash
# Example: Set variables based on parsed arguments
title=""              # Empty if not provided
description=""        # Empty if not provided
draft=""              # Set to "true" if --draft flag present
base_branch=""        # Empty if not provided (will use default)
reviewers=""          # Space-separated list if provided
labels=""             # Space-separated list if provided (GitHub)
work_items=""         # Space-separated list if provided (Azure)
```

## Step 2: Get Current State and Validate

**Get current branch:**
```bash
current_branch=$(git branch --show-current)
```
If empty (detached HEAD) → Exit with: "Cannot create PR from detached HEAD state. Please checkout a branch first."

**Verify branch is pushed to remote:**
```bash
git rev-parse --verify origin/$current_branch 2>/dev/null
```
If fails → Exit with: "Branch '$current_branch' is not pushed to remote. Push it first with:\n  git push -u origin $current_branch"

**Determine target branch:**

If user provided `--base`, use that:
```bash
if [ -n "$base_branch" ]; then
  target_branch="$base_branch"
fi
```

Otherwise, get the default branch from the platform:

**GitHub:**
```bash
if [ -z "$target_branch" ]; then
  target_branch=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null)
fi
```

**Azure DevOps:**
```bash
if [ -z "$target_branch" ]; then
  target_branch=$(az repos show --query defaultBranch -o tsv 2>/dev/null | sed 's|refs/heads/||')
fi
```

**Fallback if platform command fails:**
```bash
if [ -z "$target_branch" ]; then
  # Try common default branches
  if git rev-parse --verify origin/main >/dev/null 2>&1; then
    target_branch="main"
  elif git rev-parse --verify origin/master >/dev/null 2>&1; then
    target_branch="master"
  else
    echo "Cannot determine target branch. Please specify with --base"
    echo "Available branches:"
    git branch -r | grep origin/ | sed 's/origin\///' | grep -v HEAD
    exit 1
  fi
fi
```

**Verify target branch exists:**
```bash
if ! git rev-parse --verify origin/$target_branch >/dev/null 2>&1; then
  echo "Target branch '$target_branch' not found in remote"
  echo "Available branches:"
  git branch -r | grep origin/ | sed 's/origin\///' | grep -v HEAD
  exit 1
fi
```

## Step 3: Analyze Commits

**Get commit range:**
```bash
git log --oneline $target_branch..$current_branch
```
If empty → Exit with: "No commits found between $target_branch and $current_branch. Nothing to create a PR for."

**Get detailed commit information:**
```bash
git log $target_branch..$current_branch --format="%H%n%s%n%b%n---"
```

**Get diff summary:**
```bash
git diff --stat $target_branch...$current_branch
```

## Step 4: Generate PR Title and Description

If the user didn't provide `--title` or `--description`, generate them following the [PR Description Guide](references/pr-description-guide.md).

### Title Generation (if not provided)

- **Single commit:** Use the commit subject line
- **Multiple commits with Conventional Commits:** Use the most significant type/scope (e.g., "feat(auth): Add SSO support")
- **Multiple related commits:** Find common theme by scanning for keywords:
  - Authentication: auth, login, oauth, sso, token
  - Payment: payment, billing, stripe, checkout
  - UI: component, style, css, design, layout
  - Testing: test, spec, coverage
  - Documentation: docs, readme, comment
  - Fix: fix, bug, issue, resolve
  - Refactor: refactor, clean, restructure
- **Fallback:** "Update [area]" where area is the most-changed directory

Keep title under 70 characters.

### Description Generation (if not provided)

Follow these **style principles**:
- **Tone:** Casual, humble engineer explaining to a peer
- **Focus:** Explain WHY decisions were made, not WHAT the code does
- **Avoid:** Robot speak, marketing language, obvious observations
- **Include:** Non-obvious choices, trade-offs, constraints

**Template:**
```
[1-2 sentence intro: what changed and why]

[Optional paragraph: Context on non-obvious decisions, trade-offs, or constraints]

## Changes
- Key change 1 (focus on why, not what)
- Key change 2
- Key change 3

## Testing
- [ ] Tested locally
- [ ] Added/updated tests
- [ ] Verified [relevant scenario]
```

**Analyzing commits for description:**
1. Parse all commit subjects and bodies
2. Identify the main purpose/theme
3. Extract context from commit bodies (especially lines explaining "why")
4. Look at diff summary to understand scope
5. Note any trade-offs mentioned in commits
6. Generate intro sentence: what changed + why it matters
7. List 3-5 key changes (avoid obvious ones)
8. Add testing checklist

See [references/pr-description-guide.md](references/pr-description-guide.md) for detailed guidance and examples.

## Step 5: Confirm PR Content with User

Before creating the PR, display the generated content and ask for confirmation.

**Display the PR details:**

```
Pull Request Preview
====================

Title: [generated or provided title]

Description:
[generated or provided description]

Details:
- Source: [current_branch]
- Target: [target_branch]
- Draft: [yes/no]
- Reviewers: [list if any]
- Labels/Work Items: [list if any]
```

**Ask for confirmation using AskUserQuestion:**

Ask the user: "Ready to create this pull request?"

Options:
1. "Yes, create it" → Proceed to Step 6
2. "Edit title/description" → Allow user to provide revised title and/or description, then show preview again
3. "Cancel" → Exit without creating PR

If user chooses to edit:
- Ask them to provide the updated title and/or description
- Update the variables with their input
- Show the preview again with updated content
- Ask for confirmation again

## Step 6: Create the PR

### GitHub

```bash
gh pr create --title "$title" --body "$description" \
  ${base_branch:+--base "$base_branch"} \
  ${draft:+--draft} \
  ${reviewers:+--reviewer "$reviewers"} \
  ${labels:+--label "$labels"}
```

**Common errors:**
- PR already exists → Show existing PR URL with `gh pr list --head $current_branch`
- Branch not pushed → Show push command
- Authentication failed → Run `gh auth login`

See [references/github-pr.md](references/github-pr.md) for detailed options and troubleshooting.

### Azure DevOps

```bash
az repos pr create --title "$title" --description "$description" \
  ${base_branch:+--target-branch "$base_branch"} \
  ${draft:+--draft true} \
  ${reviewers:+--required-reviewers "$reviewers"} \
  ${work_items:+--work-items $work_items}
```

**Note:** Reviewers must be quoted because they're space-separated. Work items don't need quotes as the variable expansion handles it correctly.

**Common errors:**
- PR already exists → Show existing PR URL with `az repos pr list --source-branch $current_branch`
- Branch not found → Ensure branch is pushed
- Not authenticated → Run `az login`
- No organization/project configured → Run `az devops configure`

See [references/azure-pr.md](references/azure-pr.md) for detailed options and troubleshooting.

## Step 7: Output Result

Display:
- PR URL
- Title
- Source branch → Target branch
- Draft status (if applicable)
- Reviewers (if added)
- Labels/Work items (if added)

## Error Handling Reference

| Error | Message | Resolution |
|-------|---------|------------|
| Not a git repo | "Not a git repository" | Initialize git or cd to repo |
| Unsupported remote | "Unsupported git remote. Supports GitHub or Azure DevOps" | Check `git remote -v` |
| CLI missing | Platform-specific installation message | Install gh or az CLI |
| Not authenticated | Platform-specific auth message | Run auth login command |
| Detached HEAD | "Cannot create PR from detached HEAD" | Checkout a branch |
| Branch not pushed | "Branch not pushed. Run: git push -u origin $branch" | Push the branch |
| Target branch not found | "Target branch '$branch' not found in remote" + list available | Use --base with valid branch |
| Cannot determine target | "Cannot determine target branch" + list available | Specify with --base flag |
| PR exists | "PR already exists: [URL]" | Show existing PR |
| No commits | "No commits between $base and $current" | Nothing to PR |

## Tips

- Use `--draft` for work-in-progress PRs
- The skill auto-generates good descriptions, but you can override with `--description`
- For GitHub, link issues with "Fixes #123" in description
- For Azure, use `--work-items` to link work items
- Generated descriptions are casual and explain why changes were made, not just what changed
