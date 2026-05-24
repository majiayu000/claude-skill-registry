---
name: github
description: "GitHub CLI - manage repositories, issues, pull requests, actions, releases, and more from the command line."
---

# GitHub CLI Skill

Use the `gh` CLI to interact with GitHub repositories and services.

## Authentication

Check auth status:
```bash
gh auth status
```

Login:
```bash
gh auth login
```

Refresh token:
```bash
gh auth refresh
```

## Repositories

Clone repository:
```bash
gh repo clone owner/repo
```

Create new repo:
```bash
gh repo create my-repo --public --source=. --push
```

Fork repository:
```bash
gh repo fork owner/repo --clone
```

View repo in browser:
```bash
gh repo view --web
```

List your repos:
```bash
gh repo list
```

## Issues

List issues:
```bash
gh issue list
```

Create issue:
```bash
gh issue create --title "Bug: Login fails" --body "Description here"
```

Create issue interactively:
```bash
gh issue create
```

View issue:
```bash
gh issue view 123
```

Close issue:
```bash
gh issue close 123
```

Reopen issue:
```bash
gh issue reopen 123
```

Comment on issue:
```bash
gh issue comment 123 --body "Working on this"
```

Assign issue:
```bash
gh issue edit 123 --add-assignee @me
```

Add labels:
```bash
gh issue edit 123 --add-label "bug,priority:high"
```

## Pull Requests

List PRs:
```bash
gh pr list
```

Create PR:
```bash
gh pr create --title "Add feature" --body "Description"
```

Create PR from current branch:
```bash
gh pr create --fill
```

View PR:
```bash
gh pr view 45
```

View PR in browser:
```bash
gh pr view 45 --web
```

Checkout PR locally:
```bash
gh pr checkout 45
```

Review PR:
```bash
gh pr review 45 --approve
gh pr review 45 --request-changes --body "Please fix X"
gh pr review 45 --comment --body "Looks good but..."
```

Merge PR:
```bash
gh pr merge 45 --squash
gh pr merge 45 --merge
gh pr merge 45 --rebase
```

Close PR:
```bash
gh pr close 45
```

List PR checks:
```bash
gh pr checks 45
```

View PR diff:
```bash
gh pr diff 45
```

## Actions (CI/CD)

List workflow runs:
```bash
gh run list
```

View run details:
```bash
gh run view 12345
```

Watch run in progress:
```bash
gh run watch 12345
```

View run logs:
```bash
gh run view 12345 --log
```

Rerun failed jobs:
```bash
gh run rerun 12345 --failed
```

List workflows:
```bash
gh workflow list
```

Run workflow manually:
```bash
gh workflow run deploy.yml
```

Run with inputs:
```bash
gh workflow run deploy.yml -f environment=production
```

Disable/enable workflow:
```bash
gh workflow disable deploy.yml
gh workflow enable deploy.yml
```

## Releases

List releases:
```bash
gh release list
```

Create release:
```bash
gh release create v1.0.0 --title "Version 1.0" --notes "Release notes"
```

Create from tag:
```bash
gh release create v1.0.0 --generate-notes
```

Upload assets:
```bash
gh release upload v1.0.0 ./dist/app.zip
```

Download assets:
```bash
gh release download v1.0.0
```

Delete release:
```bash
gh release delete v1.0.0
```

## Gists

Create gist:
```bash
gh gist create file.txt --public
```

Create from stdin:
```bash
echo "Hello" | gh gist create -
```

List gists:
```bash
gh gist list
```

View gist:
```bash
gh gist view GIST_ID
```

Edit gist:
```bash
gh gist edit GIST_ID
```

## Search

Search repos:
```bash
gh search repos "react hooks" --limit 10
```

Search issues:
```bash
gh search issues "bug authentication" --repo owner/repo
```

Search PRs:
```bash
gh search prs "fix memory leak" --state open
```

Search code:
```bash
gh search code "function handleAuth" --repo owner/repo
```

## API

Make API request:
```bash
gh api repos/owner/repo
```

POST request:
```bash
gh api repos/owner/repo/issues -f title="New issue" -f body="Description"
```

GraphQL query:
```bash
gh api graphql -f query='{ viewer { login } }'
```

Paginate results:
```bash
gh api repos/owner/repo/issues --paginate
```

## Labels

List labels:
```bash
gh label list
```

Create label:
```bash
gh label create "priority:high" --color FF0000 --description "High priority"
```

## Projects

List projects:
```bash
gh project list
```

View project:
```bash
gh project view 1
```

## SSH Keys

List SSH keys:
```bash
gh ssh-key list
```

Add SSH key:
```bash
gh ssh-key add ~/.ssh/id_ed25519.pub --title "My laptop"
```

## GPG Keys

List GPG keys:
```bash
gh gpg-key list
```

Add GPG key:
```bash
gh gpg-key add key.gpg
```

## Secrets (for Actions)

List secrets:
```bash
gh secret list
```

Set secret:
```bash
gh secret set MY_SECRET
```

Set from file:
```bash
gh secret set MY_SECRET < secret.txt
```

Delete secret:
```bash
gh secret delete MY_SECRET
```

## Variables (for Actions)

List variables:
```bash
gh variable list
```

Set variable:
```bash
gh variable set MY_VAR --body "value"
```

## Extensions

List installed extensions:
```bash
gh extension list
```

Install extension:
```bash
gh extension install owner/gh-extension
```

Browse extensions:
```bash
gh extension browse
```

## Aliases

Create alias:
```bash
gh alias set pv 'pr view'
```

List aliases:
```bash
gh alias list
```

## Configuration

View config:
```bash
gh config list
```

Set default editor:
```bash
gh config set editor vim
```

Set default browser:
```bash
gh config set browser "open"
```

## Common Workflows

### Quick PR workflow:
```bash
# Create branch, commit, push, create PR
git checkout -b feature/my-feature
# ... make changes ...
git add . && git commit -m "Add feature"
git push -u origin feature/my-feature
gh pr create --fill
```

### Review and merge:
```bash
gh pr checkout 45
# ... review code ...
gh pr review --approve
gh pr merge --squash --delete-branch
```

### Check CI status:
```bash
gh pr checks
gh run watch
```
