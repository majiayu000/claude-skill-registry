---
name: github-cli
description: Use this skill when the user asks to work with GitHub from the command line using gh CLI. This includes managing repositories, issues, pull requests, releases, authentication, codespaces, actions, and any other GitHub operations. Use this skill for phrases like "create a PR", "manage issues", "clone a repo", "check gh status", or any GitHub CLI workflow.
version: 1.0.0
license: MIT
---

# GitHub CLI (gh) Comprehensive Skill

Master the GitHub CLI (`gh`) to seamlessly work with GitHub from the command
line. This skill covers all major GitHub operations including repository
management, issues, pull requests, releases, authentication, and more.

## When to Use This Skill

Trigger this skill when the user asks to:

- "Create a PR/issue/release"
- "Manage GitHub repository"
- "Clone/fork/update a repo"
- "Check/authenticate with gh"
- "Work with GitHub Actions"
- "Manage codespaces"
- "Search repos/issues/PRs"
- Any GitHub CLI operation

## Prerequisites

### Installation & Authentication

**Check if gh is installed:**

```bash
gh --version
```

**Install gh (if not installed):**

```bash
# macOS
brew install gh

# Windows (winget)
winget install --id GitHub.cli

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

**Authenticate with GitHub:**

```bash
gh auth login
# Follow prompts:
# - GitHub.com
# - HTTPS protocol
# - Login with web browser OR token
```

**Verify authentication:**

```bash
gh auth status
```

Expected output:

```
github.com
  ✓ Logged in to github.com account <username> (keyring)
  - Active account: true
  - Git operations protocol: https
  - Token: ghp_************************************
```

## Core Command Categories

### 1. Repository Management

#### View Repository Info

```bash
# View current repository
gh repo view

# View specific repository
gh repo view owner/repo

# View with JSON output
gh repo view --json name,description,visibility,owner

# Open repository in browser
gh repo view --web
```

#### Clone Repository

```bash
# Clone current repository (if in directory)
gh repo clone

# Clone specific repository
gh repo clone owner/repo

# Clone to specific directory
gh repo clone owner/repo my-directory

# Clone with SSH
gh repo clone owner/repo -- --ssh
```

#### Create Repository

```bash
# Create new repository (interactive)
gh repo create

# Create with specific settings
gh repo create my-repo \
  --public \
  --description "My awesome repository" \
  --source=. \
  --remote=origin \
  --push

# Create private repository
gh repo create my-private-repo --private

# Create without cloning
gh repo create my-repo --clone=false
```

#### Fork Repository

```bash
# Fork repository
gh repo fork owner/repo

# Fork to specific organization
gh repo fork owner/repo --org my-org

# Fork and clone
gh repo fork owner/repo --clone
```

#### Update Repository Settings

```bash
# Update repository description
gh repo edit --description "New description"

# Change visibility
gh repo edit --visibility private

# Add topics
gh repo edit --add-topic "golang" --add-topic "proxy"

# Set default branch
gh repo edit --default-branch main
```

### 2. Issue Management

#### List Issues

```bash
# List issues in current repository
gh issue list

# List with filters
gh issue list \
  --state open \
  --author masx200 \
  --label bug,enhancement \
  --limit 20

# List closed issues
gh issue list --state closed

# List with JSON output
gh issue list --json number,title,state,labels

# List across repositories
gh issue list --repo owner/repo1 --repo owner/repo2
```

#### View Issue

```bash
# View specific issue
gh issue view 123

# View with comments
gh issue view 123 --comments

# View in browser
gh issue view 123 --web

# View as JSON
gh issue view 123 --json title,body,comments
```

#### Create Issue

```bash
# Create interactively
gh issue create

# Create with title and body
gh issue create \
  --title "Bug in authentication" \
  --body "Detailed description of the bug"

# Create with labels
gh issue create \
  --title "Feature request" \
  --body "Feature description" \
  --label enhancement,good-first-issue

# Create with assignees
gh issue create \
  --title "Fix critical bug" \
  --body "Bug details" \
  --assignee @me

# Create with template
gh issue create --template bug-report.md
```

#### Edit Issue

```bash
# Edit issue interactively
gh issue edit 123

# Add comment
gh issue comment 123 --body "This is a comment"

# Add labels
gh issue edit 123 --add-label "bug,priority"

# Remove labels
gh issue edit 123 --remove-label "wontfix"

# Change state
gh issue close 123
gh issue reopen 123

# Add assignees
gh issue edit 123 --add-assignee username1,username2

# Remove assignees
gh issue edit 123 --remove-assignee username1
```

#### Search Issues

```bash
# Search issues
gh issue search "authentication" --open

# Search across repos
gh search issues --repo owner/repo "label:bug"

# Advanced search
gh search issues \
  --state open \
  --label "good first issue" \
  --language go \
  "stars:>100"
```

### 3. Pull Request Management

#### List Pull Requests

```bash
# List PRs in current repository
gh pr list

# List with filters
gh pr list \
  --state open \
  --author masx200 \
  --base main \
  --limit 20

# List merged PRs
gh pr list --state merged

# List ready for review
gh pr list --state open --review required

# List with JSON output
gh pr list --json number,title,state,author,headRefName
```

#### View Pull Request

```bash
# View specific PR
gh pr view 123

# View with diffs
gh pr view 123 --diff

# View with comments
gh pr view 123 --comments

# View checks/status
gh pr view 123 --json statusCheckRollup

# View in browser
gh pr view 123 --web
```

#### Create Pull Request

```bash
# Create PR interactively
gh pr create

# Create with title and body
gh pr create \
  --title "Add new feature" \
  --body "Description of changes"

# Create from specific branch
gh pr create \
  --base main \
  --head feature-branch \
  --title "Feature implementation"

# Create with reviewers
gh pr create \
  --title "Refactor code" \
  --body "Refactoring details" \
  --reviewer username1,username2

# Create with labels
gh pr create \
  --title "Bug fix" \
  --label bug,priority-high

# Create with draft
gh pr create \
  --title "WIP feature" \
  --body "Work in progress" \
  --draft

# Create from issue
gh pr create \
  --issue 123 \
  --title "Fix issue #123"

# Create with template
gh pr create --template pr-template.md
```

#### Checkout Pull Request

```bash
# Checkout PR (alias: gh pr checkout)
gh pr checkout 123

# Checkout and create branch
gh pr checkout 123 --branchname pr-123
```

#### Edit Pull Request

```bash
# Edit PR interactively
gh pr edit 123

# Add reviewers
gh pr edit 123 --add-reviewer username1,username2

# Add assignees
gh pr edit 123 --add-assignee username1

# Change title
gh pr edit 123 --title "Updated title"

# Add labels
gh pr edit 123 --add-label "needs-review"

# Remove labels
gh pr edit 123 --remove-label "wip"

# Convert to draft
gh pr edit 123 --mark-draft

# Ready for review (remove draft)
gh pr edit 123 --ready-for-review
```

#### Manage Pull Request Reviews

```bash
# Request review
gh pr edit 123 --add-reviewer username

# View reviews
gh pr view 123 --json reviews --jq '.reviews[]'

# Approve PR
gh pr review 123 --approve --body "LGTM!"

# Request changes
gh pr review 123 --request-changes --body "Please fix these issues"

# Comment on PR
gh pr review 123 --comment --body "Just a comment"

# Dismiss reviews
gh pr review 123 --dismiss "No longer relevant"
```

#### Merge Pull Request

```bash
# Merge PR
gh pr merge 123

# Merge with specific method
gh pr merge 123 --merge
gh pr merge 123 --squash
gh pr merge 123 --rebase

# Merge with commit title/body
gh pr merge 123 \
  --merge \
  --subject "Merge PR #123" \
  --body "Detailed message"

# Delete branch after merge
gh pr merge 123 --delete-branch

# Merge without confirmation
gh pr merge 123 --yes
```

#### Close/Reopen Pull Request

```bash
# Close PR
gh pr close 123

# Close with comment
gh pr close 123 --comment "Superseded by PR #456"

# Reopen PR
gh pr reopen 123
```

### 4. Authentication Management

#### Login/Logout

```bash
# Login
gh auth login

# Login to GitHub Enterprise
gh auth login --hostname enterprise.github.com

# Logout
gh auth logout

# Logout from specific hostname
gh auth logout --hostname enterprise.github.com
```

#### Status & Token

```bash
# Check auth status
gh auth status

# Get authentication token
gh auth token

# Get token for specific hostname
gh auth token --hostname enterprise.github.com
```

#### Switch Accounts

```bash
# Switch active account
gh auth switch --username username

# Refresh credentials
gh auth refresh
```

#### Git Integration

```bash
# Setup git with gh credentials
gh auth setup-git

# This configures git to use gh for authentication
# instead of password prompts
```

### 5. Codespaces Management

#### List Codespaces

```bash
# List all codespaces
gh codespace list

# List for specific repository
gh codespace list --repo owner/repo

# List with detailed info
gh codespace list --json name,state,repository,createdAt
```

#### Create Codespace

```bash
# Create codespace
gh codespace create

# Create for specific branch
gh codespace create --branch main

# Create with specific machine
gh codespace create --machine standardLinux32gb

# Create and open in browser
gh codespace create --web
```

#### Connect to Codespace

```bash
# Connect interactively
gh codespace codespace

# SSH into codespace
gh codespace ssh --codespace codespace-name

# Open in VS Code
gh codespace code --codespace codespace-name

# Open in browser
gh codespace view --web --codespace codespace-name
```

#### Delete Codespace

```bash
# Delete codespace
gh codespace delete --codespace codespace-name

# Delete all codespaces
gh codespace delete --all
```

### 6. GitHub Actions Management

#### List Workflow Runs

```bash
# List recent workflow runs
gh run list

# List for specific workflow
gh run list --workflow "ci.yml"

# List with branch filter
gh run list --branch main

# List with limit
gh run list --limit 50

# List with JSON output
gh run list --json databaseId,status,conclusion,event,headBranch
```

#### View Run Details

```bash
# View run details
gh run view 123456789

# View with logs
gh run view 123456789 --log

# View with failed jobs
gh run view 123456789 --log-failed

# View in browser
gh run view 123456789 --web

# Watch run in real-time
gh run watch 123456789
```

#### Rerun Workflows

```bash
# Rerun failed tests
gh run rerun 123456789

# Rerun all failed jobs
gh run rerun 123456789 --failed

# Cancel run
gh run cancel 123456789

# Trigger workflow
gh workflow run ci.yml
```

#### Manage Workflow Files

```bash
# List workflows
gh workflow list

# View workflow
gh workflow view ci.yml

# View workflow YAML
gh workflow view ci.yml --yaml

# Enable workflow
gh workflow enable ci.yml

# Disable workflow
gh workflow disable ci.yml
```

### 7. Release Management

#### List Releases

```bash
# List releases
gh release list

# List with limit
gh release list --limit 20

# List with JSON output
gh release list --json name,tagName,publishedAt
```

#### View Release

```bash
# View specific release
gh release view v1.0.0

# View latest release
gh release view --latest

# View in browser
gh release view v1.0.0 --web

# Download release assets
gh release download v1.0.0

# Download specific assets
gh release download v1.0.0 --pattern "*.tar.gz"
```

#### Create Release

```bash
# Create release
gh release create v1.0.0

# Create with title and notes
gh release create v1.0.0 \
  --title "Version 1.0.0" \
  --notes "Release notes here"

# Create from notes file
gh release create v1.0.0 \
  --notes-file RELEASE_NOTES.md

# Create draft release
gh release create v1.0.0 \
  --notes "Draft notes" \
  --draft

# Create pre-release
gh release create v1.0.0-beta.1 \
  --notes "Beta release" \
  --prerelease

# Create with target commit
gh release create v1.0.0 \
  --target main \
  --notes "Release notes"

# Create with assets
gh release create v1.0.0 \
  --notes "Release" \
  ./dist/binary-linux \
  ./dist/binary-darwin \
  ./dist/binary-windows.exe
```

#### Edit/Delete Release

```bash
# Edit release
gh release edit v1.0.0 --notes "Updated notes"

# Delete release
gh release delete v1.0.0 --yes
```

### 8. Search & Browse

#### Search Repositories

```bash
# Search repositories
gh search repos "http proxy"

# Search with filters
gh search repos \
  --language go \
  --stars ">100" \
  "http proxy"

# Search in specific topic
gh search repos --topic "proxy"

# Search with JSON output
gh search repos "proxy" --json name,description,stargazersCount --limit 10
```

#### Search Issues & PRs

```bash
# Search issues
gh search issues "label:bug state:open"

# Search PRs
gh search prs "state:open author:masx200"

# Search code
gh search code "language:go Proxy()"
```

#### Browse in Browser

```bash
# Open repository in browser
gh browse

# Open specific file
gh browse --branch main --filename README.md

# Open issues
gh browse --issues

# Open PRs
gh browse --pulls

# Open specific PR
gh browse --commit 9a8ebda

# Open settings
gh browse --settings
```

### 9. Organization Management

#### View Organization

```bash
# View organization
gh org view my-org

# View with JSON
gh org view my-org --json name,description,teams

# View in browser
gh org view my-org --web
```

#### List Organization Members

```bash
# List members
gh org list-members my-org

# List with role filter
gh org list-members my-org --role admin

# List with JSON output
gh org list-members my-org --json login,role
```

#### Manage Organization Repositories

```bash
# List organization repos
gh repo list my-org

# Create org repository
gh repo create my-org/new-repo --public
```

### 10. Gist Management

#### List Gists

```bash
# List your gists
gh gist list

# List all gists (including starred)
gh gist list --public

# List with limit
gh gist list --limit 50
```

#### View Gist

```bash
# View gist
gh gist view gist-id

# View in browser
gh gist view gist-id --web

# View with files
gh gist view gist-id --files
```

#### Create/Edit Gist

```bash
# Create gist
gh gist create file.txt

# Create with description
gh gist create file.txt --desc "My gist"

# Create public gist
gh gist create file.txt --public

# Create secret gist
gh gist create file.txt --private

# Edit gist
gh gist edit gist-id --file new-file.txt

# Delete gist
gh gist delete gist-id
```

### 11. Label Management

#### List Labels

```bash
# List labels in current repo
gh label list

# List with colors
gh label list --json name,color,description
```

#### Create Label

```bash
# Create label
gh label create "bug" \
  --color "d73a4a" \
  --description "Something isn't working"

# Create with hex color
gh label create "enhancement" \
  --color "#a2eeef" \
  --description "New feature or request"
```

#### Edit/Delete Label

```bash
# Edit label
gh label edit "bug" --color "ff0000"

# Delete label
gh label delete "wontfix" --yes
```

### 12. Project Management

#### List Projects

```bash
# List projects in current repo
gh project list

# List projects in org
gh project list --org my-org

# List with JSON output
gh project list --json number,title,state
```

#### View Project

```bash
# View project
gh project view 1

# View with items
gh project view 1 --json title,status,items

# View in browser
gh project view 1 --web
```

### 13. Status Command

#### Check Status

```bash
# Check status (issues, PRs, notifications)
gh status

# Check with specific repos
gh status --repo owner/repo1 --repo owner/repo2

# Check with limit
gh status --limit 10
```

### 14. Alias & Extensions

#### Create Aliases

```bash
# Create alias for command
gh alias set prc 'pr create'

# Create complex alias
gh alias set list-prs 'pr list --state open --limit 20'

# List aliases
gh alias list

# Delete alias
gh alias delete prc
```

#### Manage Extensions

```bash
# Install extension
gh extension install owner/extension-repo

# List extensions
gh extension list

# Remove extension
gh extension remove extension-name
```

### 15. API Requests

#### Make API Requests

```bash
# Make authenticated API request
gh api /user

# Make request with query parameters
gh api "/repos/masx200/http-proxy-go-server/issues?state=open"

# Make POST request
gh api \
  --method POST \
  -H "Accept: application/vnd.github.v3+json" \
  /repos/owner/repo/issues \
  -f title="New issue" \
  -f body="Issue description"

# Make request with JSON input
gh api \
  --method PATCH \
  /repos/owner/repo/issues/123 \
  -f state=closed

# Get paginated results
gh api /user/repos --paginate

# Use jq to filter results
gh api /user | jq '.name, .public_repos'
```

### 16. Configuration

#### View Configuration

```bash
# View all config
gh config set

# View specific config
gh config get git_protocol

# Set config
gh config set git_protocol ssh
gh config set editor vim
gh config set prompt enabled
```

#### Configuration Options

```bash
# Set git protocol
gh config set git_protocol ssh   # or https

# Set editor for editing text
gh config set editor code --wait

# Enable/disable prompts
gh config set prompt enabled    # or disabled

# Set pagination
gh config set pager less
```

### 17. SSH & GPG Keys

#### SSH Keys

```bash
# List SSH keys
gh ssh-key list

# Add SSH key
gh ssh-key add ~/.ssh/id_ed25519 --title "My laptop"

# Delete SSH key
gh ssh-key delete 123456789
```

#### GPG Keys

```bash
# List GPG keys
gh gpg-key list

# Add GPG key
gh gpg-key add ~/.ssh/mykey.asc

# Delete GPG key
gh gpg-key delete 123456789
```

### 18. Secrets Management

#### List Secrets

```bash
# List repository secrets
gh secret list

# List organization secrets
gh secret list --org my-org

# List environment secrets
gh secret list --env production
```

#### Set/Delete Secret

```bash
# Set secret (interactive)
gh secret set MY_SECRET

# Set secret from file
gh secret set MY_SECRET < secret.txt

# Set secret for environment
gh secret set MY_SECRET --env production

# Delete secret
gh secret delete MY_SECRET
```

### 19. Variables Management (GitHub Actions)

#### List Variables

```bash
# List variables
gh variable list

# List with JSON output
gh variable list --json name,value
```

#### Set/Delete Variable

```bash
# Set variable
gh variable set VAR_NAME "value"

# Set variable for environment
gh variable set VAR_NAME "value" --env production

# Delete variable
gh variable delete VAR_NAME
```

### 20. Completion Scripts

#### Generate Shell Completion

```bash
# Generate completion for bash
gh completion -s bash > /etc/bash_completion.d/gh

# Generate completion for zsh
gh completion -s zsh > /usr/local/share/zsh/site-functions/_gh

# Generate completion for fish
gh completion -s fish > ~/.config/fish/completions/gh.fish

# Generate completion for powershell
gh completion -s powershell | Out-File gh.ps1
```

## Common Workflows & Examples

### Workflow 1: Complete PR Creation Flow

```bash
# 1. Update main branch
git checkout main
git pull

# 2. Create feature branch
git checkout -b feature/new-feature

# 3. Make changes and commit
git add .
git commit -m "feat: Add new feature"

# 4. Push to remote
git push -u origin feature/new-feature

# 5. Create PR with reviewers
gh pr create \
  --title "Add new feature" \
  --body "Detailed description" \
  --reviewer username1,username2 \
  --label enhancement

# 6. View PR status
gh pr status
```

### Workflow 2: Issue Triage

```bash
# 1. List open issues
gh issue list --state open --limit 50

# 2. View specific issue
gh issue view 123

# 3. Add label and assign
gh issue edit 123 \
  --add-label "bug,priority-high" \
  --add-assignee @me

# 4. Comment on issue
gh issue comment 123 --body "Working on this"

# 5. Create branch and fix
git checkout -b fix/issue-123
# ... make changes ...

# 6. Create PR from issue
gh pr create \
  --issue 123 \
  --title "Fix issue #123" \
  --body "Fixes #123"
```

### Workflow 3: Repository Setup

```bash
# 1. Create repository
gh repo create my-new-repo --public --clone

# 2. Navigate to repository
cd my-new-repo

# 3. Initialize with README
echo "# My New Repo" > README.md
git add README.md
git commit -m "Initial commit"
git push

# 4. Add topics
gh repo edit --add-topic "golang,cli,tool"

# 5. Create labels
gh label create "bug" --color "d73a4a"
gh label create "enhancement" --color "a2eeef"

# 6. Add protect branch (via API)
gh api \
  --method PUT \
  -H "Accept: application/vnd.github.v3+json" \
  /repos/$(gh repo view --json owner,name --jq '.owner.login + "/" + .name')/branches/main/protection \
  -f required_status_checks='{"strict":true,"contexts":[]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"dismiss_stale_reviews":true}'
```

### Workflow 4: Release Management

```bash
# 1. Create release tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 2. Create release
gh release create v1.0.0 \
  --title "Version 1.0.0" \
  --notes-file RELEASE_NOTES.md

# 3. Upload assets
gh release upload v1.0.0 \
  ./dist/binary-linux-amd64 \
  ./dist/binary-darwin-amd64 \
  ./dist/binary-windows-amd64.exe

# 4. View release
gh release view v1.0.0 --web
```

### Workflow 5: Fork & Contribute

```bash
# 1. Fork repository
gh repo fork owner/repo --clone

# 2. Navigate to fork
cd repo

# 3. Create feature branch
git checkout -b feature/contribution

# 4. Make changes
# ... edit files ...
git add .
git commit -m "feat: Add contribution"

# 5. Push to fork
git push -u origin feature/contribution

# 6. Create PR to original repo
gh pr create \
  --repo owner/repo \
  --base main \
  --title "Add contribution" \
  --body "Description of changes"
```

### Workflow 6: Bulk Operations

```bash
# Bulk close issues
gh issue list --label "wontfix" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --comment "Closed as wontfix"

# Bulk add labels
gh issue list --state open --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --add-label "triage"

# Bulk PR merge (careful!)
gh pr list --state open --label "ready-to-merge" --json number --jq '.[].number' | \
  xargs -I {} gh pr merge {} --merge --yes
```

## Tips & Best Practices

### DO ✅

1. **Use aliases** for frequently used commands
   ```bash
   gh alias set prs 'pr list --state open'
   gh alias set issues 'issue list --state open'
   ```

2. **Enable shell completion** for better productivity

3. **Use JSON output** with `jq` for scripting:
   ```bash
   gh pr list --json number,title --jq '.[] | select(.title | contains("fix"))'
   ```

4. **Create templates** for common PR/issue descriptions

5. **Use web flag** to open in browser for complex operations:
   ```bash
   gh pr view --web
   ```

6. **Check auth status** before running sensitive operations

7. **Use `--help`** flag to explore subcommands:
   ```bash
   gh pr create --help
   ```

8. **Leverage search** for complex queries

9. **Use pagination** for large result sets:
   ```bash
   gh issue list --limit 100
   ```

10. **Automate with scripts** using gh in CI/CD pipelines

### DON'T ❌

1. **NEVER hardcode tokens** - let gh handle authentication

2. **DON'T ignore errors** - check exit codes and handle failures

3. **NEVER commit secrets** - use gh secret for sensitive data

4. **DON'T use --yes** in scripts without proper validation

5. **NEVER delete resources** without confirmation (unless intentional)

6. **DON'T forget to push** tags before creating releases

7. **NEVER use --web** in automated scripts

8. **DON'T ignore rate limits** when making API calls

9. **NEVER assume gh is installed** - check and handle missing

10. **DON'T use personal access tokens** when gh auth is available

## Troubleshooting

### Issue: "gh not found"

**Solution:**

```bash
# Check if gh is installed
which gh

# If not, install it
# See Installation section above
```

### Issue: "gh: not logged in"

**Solution:**

```bash
gh auth login
gh auth status  # Verify
```

### Issue: "Permission denied"

**Solution:**

```bash
# Check permissions
gh repo view

# Ensure you have correct access
gh auth refresh
```

### Issue: "Repository not found"

**Solution:**

```bash
# Check current repo
git remote -v

# Set correct remote
git remote set-url origin https://github.com/owner/repo.git
```

### Issue: "gh is slow"

**Solution:**

```bash
# Check git protocol
gh config get git_protocol

# Switch to ssh (faster for authenticated requests)
gh config set git_protocol ssh
```

### Issue: "API rate limit exceeded"

**Solution:**

```bash
# Check rate limit
gh api /rate_limit

# Wait or authenticate to increase limit
gh auth login
```

## Advanced Usage

### JSON Processing with jq

```bash
# Get all open PR titles
gh pr list --json title --jq '.[].title'

# Get PRs with specific label
gh pr list --json number,title,labels --jq '.[] | select(.labels[].name == "bug")'

# Get issues assigned to me
gh issue list --assignee @me --json number,title --jq '.[] | "#\(.number): \(.title)"'

# Count PRs by author
gh pr list --json author --jq 'group_by(.author.login) | map({author: .[0].author.login, count: length})'
```

### Shell Scripting

```bash
#!/bin/bash
# Script to create release with proper checks

# Check authentication
if ! gh auth status &> /dev/null; then
  echo "Not authenticated with gh"
  exit 1
fi

# Check if tag exists
if git rev-parse "$1" &> /dev/null; then
  echo "Tag $1 already exists"
  exit 1
fi

# Create tag
git tag -a "$1" -m "Release $1"
git push origin "$1"

# Create release
gh release create "$1" --notes-file RELEASE_NOTES.md
```

### Git Integration

```bash
# Use gh in git hooks
# .git/hooks/pre-push
#!/bin/bash
BRANCH=$(git branch --show-current)
if [[ $BRANCH == feature/* ]]; then
  echo "Creating PR for $BRANCH"
  gh pr create --base main --head "$BRANCH" --draft
fi
```

## Additional Resources

- [Official GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub Blog - Introducing gh CLI](https://github.blog/2020-09-17-introducing-github-cli/)
- [Awesome gh Extensions](https://github.com/topics/gh-extension)
- [gh Extensions Repository](https://github.com/github/gh-extensions)

## Keyboard Shortcuts & Tips

```bash
# Use gh with fzf for interactive selection
gh pr list | fzf | gh pr view $(awk '{print $1}')

# Quick view latest PR
gh pr view --web $(gh pr list --json number --jq '.[0].number')

# Quick issue creation with template
gh issue create --title "$1" --body "$(cat issue-template.md)"
```

---

**Remember**: The GitHub CLI is a powerful tool - use it wisely to automate your
GitHub workflows and boost your productivity! 🚀
