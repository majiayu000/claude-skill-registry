---
name: devops
description: DevOps skills for CI/CD, GitHub workflows, and infrastructure automation
icon: 🚀
category: automation
tools:
  - git
  - gh
  - docker
  - nix
  - github-actions
---

# DevOps Skills

## Overview

This skill provides expertise in DevOps practices including CI/CD pipelines, GitHub workflows, and infrastructure automation.

## Git Operations

### Basic Workflow
```bash
gs                                    # git status
ga                                    # git add
gc                                    # git commit
gp                                    # git push
gl                                    # git pull
```

### Branching
```bash
gco <branch>                          # git checkout
gb                                    # git branch
git checkout -b feature/name          # Create and switch to branch
git merge <branch>                    # Merge branch
```

### History
```bash
glog                                  # git log --oneline --graph
gd                                    # git diff
git log --oneline -10                 # Last 10 commits
git blame <file>                      # Line-by-line history
```

## GitHub CLI (gh)

### Pull Requests
```bash
gh pr create                          # Create PR interactively
gh pr create --title "Title" --body "Body"
gh pr list                            # List open PRs
gh pr view <number>                   # View PR details
gh pr checkout <number>               # Checkout PR locally
gh pr merge <number>                  # Merge PR
```

### Issues
```bash
gh issue create                       # Create issue
gh issue list                         # List issues
gh issue view <number>                # View issue
gh issue close <number>               # Close issue
```

### Workflows
```bash
gh run list                           # List workflow runs
gh run view <run-id>                  # View run details
gh run watch <run-id>                 # Watch run in real-time
gh workflow run <workflow>            # Trigger workflow
```

### Releases
```bash
gh release create v1.0.0              # Create release
gh release list                       # List releases
gh release download                   # Download release assets
```

## GitHub Actions

### Workflow Structure
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: DeterminateSystems/nix-installer-action@main
      - run: nix develop --command echo "Ready"
```

### Common Actions
- `actions/checkout@v4` - Checkout repository
- `DeterminateSystems/nix-installer-action@main` - Install Nix
- `DeterminateSystems/magic-nix-cache-action@main` - Nix cache
- `actions/upload-artifact@v4` - Upload artifacts

### Self-Hosted Runners
```bash
# Labels for WSL2 runner
runs-on: [self-hosted, Windows, WSL2]
```

See: `.github/docs/self-hosted-runner-setup.md`

## Container Operations

### Docker
```bash
docker build -t image:tag .           # Build image
docker run -it image:tag              # Run container
docker push registry/image:tag        # Push to registry
docker compose up -d                  # Start services
```

### Multi-Stage Builds
```dockerfile
FROM nixos/nix AS builder
RUN nix build .#package

FROM alpine
COPY --from=builder /result /app
```

## Infrastructure as Code

### Nix-based Deployments
```bash
nix build .#nixosConfigurations.host.config.system.build.toplevel
nixos-rebuild switch --flake .#host
```

### Home Manager
```bash
home-manager switch --flake .#user
```

## Secrets Management

### GitHub Secrets
- Set via: Settings → Secrets and variables → Actions
- Access in workflow: `${{ secrets.SECRET_NAME }}`
- Never log secrets in workflow output

### Local Development
- Use `.env` files (gitignored)
- Use `pass` or `1password-cli` for credential storage
- Use `sops` for encrypted secrets in git

## Monitoring

### Workflow Status
```bash
gh run list --limit 5                 # Recent runs
gh run view --log                     # View logs
gh api repos/{owner}/{repo}/actions/runs
```

### Health Checks
- Add status badges to README
- Set up branch protection rules
- Configure required status checks

## Best Practices

1. **Pin action versions** - Use SHA or version tags
2. **Cache dependencies** - Use Nix cache actions
3. **Fail fast** - Use `continue-on-error: false`
4. **Matrix builds** - Test multiple platforms
5. **Reusable workflows** - Extract common patterns

## Troubleshooting

### Workflow Failures
- Check `gh run view --log` for details
- Verify secrets are set correctly
- Check runner availability for self-hosted

### Permission Issues
- Verify `GITHUB_TOKEN` permissions
- Check repository settings for actions

## Related Skills

- [ROS2 Development](../ros2-development/SKILL.md) - CI for ROS packages
- [Nix Environment](../nix-environment/SKILL.md) - Reproducible builds
