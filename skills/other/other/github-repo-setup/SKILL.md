---
name: github-repo-setup
description: Configure and initialize GitHub repositories with privacy settings, repository metadata, and feature toggles. Use when preparing repositories for publication on GitHub, including setting up private repositories, adding descriptions to repository about section, and disabling features like releases and environments.
---

# GitHub Repository Setup

Prepare GitHub repositories for publication with proper configuration including privacy settings, metadata, and feature management using GitHub CLI.

⚠️ **Note**: This skill keeps repositories simple and minimal. It does NOT add LICENSE files, CODEOWNERS, CONTRIBUTING.md, SECURITY.md, or issue templates. It focuses only on core GitHub repository configuration.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Repository name defined
- (Optional) Repository description for the about section

## Checking GitHub CLI

Before using this skill, verify that GitHub CLI is installed and authenticated:

```bash
# Check if gh is installed
which gh

# If not installed, install it (macOS):
brew install gh

# For other systems:
# Windows: choco install gh
# Linux: Follow https://github.com/cli/cli/blob/trunk/docs/install_linux.md

# Authenticate with GitHub (if not already authenticated)
gh auth login
```

If `gh` is not installed, you'll see an error. Use the installation command for your operating system above.

## Basic setup

Create and configure a new private GitHub repository (always private):

```bash
# Create a private repository
gh repo create <repo-name> --private --source=. --remote=origin --push

# Configure repository settings (add description)
gh repo edit <owner>/<repo-name> --description="Your repository description"
```

## Complete setup workflow

Use this comprehensive workflow to set up a private repository with all recommended settings:

```bash
#!/bin/bash

# Variables
REPO_NAME="my-repository"
REPO_DESCRIPTION="Brief description of the repository"
OWNER="your-github-username"  # or your organization

# Step 0: Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI is not installed. Install it with:"
    echo "  macOS: brew install gh"
    echo "  Other systems: https://github.com/cli/cli#installation"
    exit 1
fi

# Step 1: Create private repository (always private)
gh repo create "${REPO_NAME}" \
  --private \
  --source=. \
  --remote=origin \
  --push \
  --description="${REPO_DESCRIPTION}"

# Step 2: Add description to about section (if needed)
gh repo edit "${OWNER}/${REPO_NAME}" --description="${REPO_DESCRIPTION}"

# Step 3: Disable wikis and discussions
gh repo edit "${OWNER}/${REPO_NAME}" --enable-wiki=false --enable-discussions=false

# Step 4: Open repository in browser
gh repo view "${OWNER}/${REPO_NAME}" --web
```

## Configuration options

### Repository type

**Always private** (default for this skill):
All repositories created with this skill are automatically set to private for security and control.

If you need to change visibility later:
```bash
gh repo edit <owner>/<repo-name> --visibility private
```

### Repository description

Set the description that appears in the repository's about section:

```bash
gh repo edit <owner>/<repo-name> --description "Your repository description"
```

The description should be concise and clearly communicate the repository's purpose.

### Disable features

**Disable releases**:
Releases are managed via branch protection rules and GitHub Actions workflows. To prevent accidental releases:
- Use branch protection on main/master
- Limit who can create releases via repository permissions

**Disable environments**:
```bash
# Environments are disabled by default for private repositories
# For public repositories, restrict environment access:
gh repo edit <owner>/<repo-name> --enable-discussions=false
```

### Additional settings

**Branch protection** (protect main branch):
```bash
gh api repos/<owner>/<repo-name>/branches/main/protection \
  -X PUT \
  -F enforce_admins=true \
  -F require_code_review_count=1 \
  -F dismiss_stale_reviews=true
```

**Disable wikis and discussions**:
```bash
gh repo edit <owner>/<repo-name> --enable-wiki=false --enable-discussions=false
```

**Add topics** (optional):
```bash
gh repo edit <owner>/<repo-name> --add-topic python --add-topic github
```

## Verifying configuration

Once setup is complete, your repository will open in the browser via `gh repo view --web`. You can also manually verify settings:

```bash
# View repository details
gh repo view <owner>/<repo-name>

# Check specific settings
gh api repos/<owner>/<repo-name> --jq '.{name, private, description, has_releases, has_environments}'
```

## Tips

- Test setup commands on a test repository first
- Use environment variables for repetitive parameters
- Automate setup with the provided script for consistency
- Always verify settings after configuration
- Use `gh repo edit --help` to see all available options