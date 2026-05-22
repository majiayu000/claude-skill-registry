---
name: act-local-testing
description: Use when testing GitHub Actions workflows locally with act. Covers act CLI usage, Docker configuration, debugging workflows, and troubleshooting common issues when running workflows on your local machine.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Act - Local Workflow Testing

Use this skill when testing GitHub Actions workflows locally with act. This covers act CLI commands, Docker setup, debugging, and best practices for fast local iteration on CI/CD workflows.

## Installation

### macOS

```bash
brew install act
```

### Linux

```bash
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

### Windows

```bash
choco install act-cli
# or
scoop install act
```

### From Source

```bash
go install github.com/nektos/act@latest
```

## Basic Usage

### Run All Workflows

```bash
# Run workflows triggered by push event
act

# Equivalent to
act push
```

### Run Specific Events

```bash
# Pull request event
act pull_request

# Workflow dispatch
act workflow_dispatch

# Custom event
act repository_dispatch -e event.json
```

### Run Specific Workflows

```bash
# Run specific workflow file
act -W .github/workflows/ci.yml

# Run specific job
act -j build

# Run specific workflow and job
act -W .github/workflows/deploy.yml -j production
```

### List Available Workflows

```bash
# List all workflows and jobs
act -l

# List for specific event
act pull_request -l
```

## Validation and Dry Runs

### Dry Run

```bash
# Validate without executing
act --dryrun

# Show what would run
act -n

# Validate specific workflow
act --dryrun -W .github/workflows/ci.yml
```

### Graph Visualization

```bash
# Show workflow graph
act -g

# Show graph for specific event
act pull_request -g
```

## Docker Configuration

### Default Runners

Act uses Docker images to simulate GitHub's runners:

```bash
# Use default images (micro - minimal)
act

# Use medium images (more tools)
act -P ubuntu-latest=catthehacker/ubuntu:act-latest

# Use large images (most compatible)
act -P ubuntu-latest=catthehacker/ubuntu:full-latest
```

### Custom Platform Images

Create `.actrc` file in project root:

```
-P ubuntu-latest=catthehacker/ubuntu:act-latest
-P ubuntu-22.04=catthehacker/ubuntu:act-22.04
-P ubuntu-20.04=catthehacker/ubuntu:act-20.04
```

Or use command line:

```bash
act -P ubuntu-latest=node:18 \
    -P ubuntu-22.04=catthehacker/ubuntu:act-22.04
```

### Reusing Docker Containers

```bash
# Reuse containers between runs (faster)
act --reuse

# Clean up after run
act --rm
```

## Secrets Management

### Using .secrets File

Create `.secrets` in project root:

```
GITHUB_TOKEN=ghp_your_token_here
NPM_TOKEN=npm_your_token_here
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

Add to `.gitignore`:

```
.secrets
```

Run with secrets:

```bash
act --secret-file .secrets
```

### Inline Secrets

```bash
# Single secret
act -s GITHUB_TOKEN=ghp_token

# Multiple secrets
act -s GITHUB_TOKEN=ghp_token \
    -s NPM_TOKEN=npm_token
```

### Environment-Specific Secrets

```bash
# Development secrets
act --secret-file .secrets.dev

# Production secrets
act --secret-file .secrets.prod
```

## Environment Variables

### Setting Variables

```bash
# Single variable
act --env NODE_ENV=development

# Multiple variables
act --env NODE_ENV=development \
    --env DEBUG=true
```

### Using .env File

Create `.env` file:

```
NODE_ENV=development
DEBUG=true
LOG_LEVEL=debug
```

Run with env file:

```bash
act --env-file .env
```

### GitHub Context Variables

Act automatically sets these:

```
GITHUB_ACTOR=nektos/act
GITHUB_REPOSITORY=owner/repo
GITHUB_EVENT_NAME=push
GITHUB_SHA=abc123...
GITHUB_REF=refs/heads/main
ACT=true
```

## Debugging

### Verbose Output

```bash
# Verbose mode
act -v

# Very verbose (debug)
act -vv
```

### Step-by-Step Execution

```bash
# Interactive mode - pause before each step
act --watch
```

### Inspect Containers

```bash
# Keep container running after workflow
act --reuse

# Then in another terminal
docker ps
docker exec -it <container-id> /bin/bash
```

### Bind Mount Local Files

```bash
# Mount current directory
act --bind

# Mount specific directory
act -b /host/path:/container/path
```

## Common Workflows

### Test Before Push

```bash
# Validate workflow syntax
act --dryrun

# Run tests
act -j test

# Run full CI
act
```

### Iterative Development

```bash
# Edit workflow
vim .github/workflows/ci.yml

# Test immediately
act --reuse -j build

# Iterate quickly
act --reuse -j build
```

### Matrix Testing

```bash
# Run specific matrix combination
act --matrix os:ubuntu-latest --matrix node:20

# Run all combinations
act
```

## Troubleshooting

### Docker Issues

```bash
# Check Docker is running
docker ps

# Pull required images manually
docker pull catthehacker/ubuntu:act-latest

# Clean up Docker resources
docker system prune -a
```

### Permission Issues

```bash
# Run with sudo (Linux)
sudo act

# Fix Docker permissions (Linux)
sudo usermod -aG docker $USER
newgrp docker
```

### Missing Tools

```bash
# Use fuller image
act -P ubuntu-latest=catthehacker/ubuntu:full-latest

# Or install in workflow
- run: |
    apt-get update
    apt-get install -y some-tool
```

### Workflow Not Found

```bash
# Check workflow files exist
ls -la .github/workflows/

# Validate YAML syntax
yamllint .github/workflows/*.yml

# List detected workflows
act -l
```

### Action Compatibility

Some actions don't work with act:

```yaml
# Skip action in act
- name: GitHub-only action
  if: ${{ !env.ACT }}
  uses: github/some-action@v1

# Use alternative in act
- name: Local alternative
  if: env.ACT == 'true'
  run: echo "Running local version"
```

## Best Practices

### DO

✅ Use `act --dryrun` before running full workflows
✅ Create `.actrc` for consistent configuration
✅ Use `.secrets` file and add it to `.gitignore`
✅ Use `--reuse` for faster iteration
✅ Test workflows locally before pushing
✅ Use appropriate image sizes for your needs
✅ Document act usage in README

### DON'T

❌ Commit `.secrets` or `.env` files
❌ Use `latest` Docker tags in production
❌ Skip validation with `--dryrun`
❌ Run act without understanding what it will do
❌ Ignore Docker disk space usage
❌ Assume all actions work perfectly with act

## Configuration Files

### .actrc

```
# Platform mappings
-P ubuntu-latest=catthehacker/ubuntu:act-latest

# Default options
--reuse
--secret-file .secrets
--env-file .env

# Container options
--container-architecture linux/amd64
```

### .github/workflows/.actrc

Project-specific overrides in workflows directory.

## CI/CD Integration

### Pre-Push Hook

`.git/hooks/pre-push`:

```bash
#!/bin/bash
echo "Validating workflows..."
act --dryrun
if [ $? -ne 0 ]; then
  echo "Workflow validation failed"
  exit 1
fi
```

### Make Target

```makefile
.PHONY: test-workflows
test-workflows:
 act --dryrun
 act -j test

.PHONY: ci-local
ci-local:
 act --reuse
```

## Performance Tips

### Faster Iteration

```bash
# Use reuse flag
act --reuse

# Skip checkout if not needed
act --reuse -j test --no-recurse

# Use smaller images for simple tests
act -P ubuntu-latest=node:20-alpine
```

### Caching

Act respects GitHub Actions caching:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

Cache location on host: `~/.cache/act/`

## Related Skills

- **act-workflow-syntax**: Creating and structuring workflow files
- **act-docker-setup**: Configuring Docker for act
- **act-advanced-features**: Advanced act usage patterns
