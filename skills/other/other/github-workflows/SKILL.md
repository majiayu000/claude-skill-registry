---
name: GitHub Workflows
description: Sets up GitHub Actions workflows for Apex Designer projects. Includes CI/CD with npm publishing.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# GitHub Workflows Setup

Sets up GitHub Actions workflows for Apex Designer projects.

## Usage

Ask Claude to "set up GitHub workflows" or "add CI/CD workflows".

## Installation

Copy workflows from the package to your project:

```bash
mkdir -p .github/workflows
cp node_modules/@apexdesigner/claude-skills/.github/workflows/* .github/workflows/
```

## Available Workflows

### CI/CD (`ci-cd.yml`)
- Runs on push to main/master/release branches
- Publishes to npm on version tags (using trusted publishing/OIDC)
- Slack notifications for build/publish status

## GitHub Configuration

These org-wide secrets/variables are already configured for Apex Designer repos:

| Name | Type | Description |
|------|------|-------------|
| `NPM_READ_ONLY_TOKEN` | Secret | npm token for installing private packages |
| `AD3_SLACK_WEBHOOK_URL` | Secret | Slack webhook for #apex-designer-3 channel |

**For a different Slack channel**, update the secret name in ci-cd.yml:

```yaml
env:
  SLACK_WEBHOOK_URL: ${{ secrets.YOUR_WEBHOOK_SECRET }}
```

For non-Apex Designer repos, configure these secrets/variables in your repository or organization settings.

## Updating Workflows

Workflows are copied during installation and don't auto-update. After updating the npm package, compare and sync:

```bash
diff -r .github/workflows node_modules/@apexdesigner/claude-skills/.github/workflows
```

If there are differences, copy the updated workflows:

```bash
cp node_modules/@apexdesigner/claude-skills/.github/workflows/* .github/workflows/
```
