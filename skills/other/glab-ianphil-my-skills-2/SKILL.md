---
name: glab
description: GitLab CLI (glab) for merge requests, issues, and CI/CD pipelines. Use when working with GitLab repositories for MR creation/review, issue management, pipeline debugging, or any GitLab API operations. Triggers on GitLab URLs, mentions of "merge request" or "MR" (not "PR"), gitlab.com, or glab commands.
---

# glab - GitLab CLI

## Quick Reference

```bash
# Authentication
glab auth login                    # Interactive login
glab auth status                   # Check auth status

# Merge Requests
glab mr create                     # Create MR interactively
glab mr list                       # List open MRs
glab mr view <id>                  # View MR details
glab mr merge <id>                 # Merge an MR
glab mr checkout <id>              # Checkout MR branch locally

# Issues
glab issue create                  # Create issue interactively
glab issue list                    # List open issues
glab issue view <id>               # View issue details
glab issue close <id>              # Close an issue

# Pipelines
glab ci status                     # Current branch pipeline status
glab ci view                       # View pipeline in browser
glab ci list                       # List recent pipelines
glab ci trace                      # Stream job logs live
```

## MR Creation Flow

```bash
# Create MR with options
glab mr create \
  --title "feat: add user authentication" \
  --description "Implements OAuth2 login flow" \
  --assignee @me \
  --reviewer @teammate \
  --label "feature,needs-review" \
  --milestone "v1.0"

# Create draft MR
glab mr create --draft --title "WIP: refactoring auth"

# Create MR targeting specific branch
glab mr create --target-branch develop

# Push and create MR in one step
glab mr create --push
```

### MR Review Workflow

```bash
# List MRs needing review
glab mr list --reviewer=@me

# Checkout MR for local testing
glab mr checkout 42
# ... test locally ...

# Approve MR
glab mr approve 42

# Merge when ready
glab mr merge 42 --squash --remove-source-branch
```

## Issue Management

### Creating Issues with Descriptions

**Simple inline description:**
```bash
glab issue create --title "Fix login bug" --description "Users cannot log in"
```

**Multiline descriptions - use `$'...'` syntax for newlines:**
```bash
glab issue create \
  --title "Bug: login fails on mobile" \
  --description $'## Summary\nLogin fails on iOS devices.\n\n## Steps to Reproduce\n1. Open app\n2. Tap login\n3. Enter credentials\n\n## Expected\nUser logs in successfully'
```

**Complex descriptions - use a temp file (most reliable):**
```bash
cat << 'EOF' > /tmp/issue-body.md
## Summary
Login fails on iOS devices when using OAuth.

## Steps to Reproduce
1. Open the app on iOS 17+
2. Tap "Login with Google"
3. Complete OAuth flow
4. App crashes on redirect

## Expected Behavior
User should be logged in and see dashboard.

## Environment
- iOS 17.2
- App version 2.3.1
EOF

glab issue create \
  --title "Bug: OAuth login crashes on iOS" \
  --label "bug,priority::high" \
  --assignee @me \
  < /tmp/issue-body.md
```

**Interactive mode (opens editor):**
```bash
glab issue create  # Opens $EDITOR for description
```

### Updating Issues

```bash
# Update description (use -d flag)
glab issue update 123 -d "New description here"

# Multiline description update
glab issue update 123 -d $'## Updated\n\nNew multiline description'

# Open editor for description (-d "-" opens $EDITOR)
glab issue update 123 -d -

# Update from file
glab issue update 123 -d "$(cat /tmp/new-description.md)"

# Other updates
glab issue update 123 --title "New title"
glab issue update 123 -l "in-progress"
glab issue update 123 --unlabel "needs-triage"
glab issue update 123 --assignee @teammate
glab issue update 123 --milestone "v1.0"
```

**Note:** For very complex updates, the API gives more control:
```bash
glab api --method PUT projects/:fullpath/issues/123 \
  -f description="$(cat /tmp/description.md)"
```

### Issue Search and Filtering

```bash
glab issue list --search "authentication"
glab issue list --label "bug"
glab issue list --label "bug" --label "priority::high"  # AND logic
glab issue list --assignee @me
glab issue list --author @me
glab issue list --closed
glab issue list --milestone "v1.0"
```

### Linking Issues to MRs

In MR descriptions, use keywords to auto-close issues on merge:
- `Closes #123`
- `Fixes #123`
- `Resolves #123`

```bash
glab issue close 123
glab issue reopen 123
```

## Pipeline Debugging

```bash
# Check current pipeline status
glab ci status

# List recent pipelines
glab ci list
glab ci list --status=failed

# View pipeline interactively (shows jobs, allows actions)
glab ci view

# View specific branch pipeline
glab ci view main
```

### Job Operations

```bash
# Stream live logs (interactive job selection)
glab ci trace

# Stream logs from specific job (by name or ID)
glab ci trace build
glab ci trace 224356863

# Retry a failed job
glab ci retry deploy
glab ci retry 224356863

# Trigger a manual job
glab ci trigger deploy-production

# Cancel running pipeline or job
glab ci cancel pipeline
glab ci cancel job 224356863
```

### Artifacts

```bash
# Download artifacts (use glab job artifact)
glab job artifact main build
glab job artifact main build --path="./artifacts/"
```

## Project Operations

```bash
# Clone with glab
glab repo clone owner/repo

# Fork a project
glab repo fork owner/repo

# View project in browser
glab repo view --web

# List project members
glab api projects/:id/members
```

## Tips

- Use `--web` or `-w` flag to open result in browser
- Use `glab alias set` to create shortcuts
- Environment variable `GITLAB_TOKEN` for CI/CD auth
- Use `glab api` for any GitLab API endpoint not covered by commands
