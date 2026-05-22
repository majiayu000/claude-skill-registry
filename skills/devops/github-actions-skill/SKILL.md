---
name: github-actions-skill
description: Expert guidance on GitHub Actions CI/CD workflows. Use when creating or modifying: (1) GitHub Actions workflow files, (2) CI/CD pipelines for testing and deployment, (3) Matrix strategies for multi-version testing, (4) Secrets and environment variable configuration, (5) Docker build and push workflows, (6) Deployment automation to cloud providers. Invoke when setting up automation, configuring pipelines, or troubleshooting workflow issues.
---

# GitHub Actions

Expert guidance for building CI/CD pipelines with GitHub Actions.

## Quick Start Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run tests
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
```

## Common Triggers

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 0 * * *"  # Daily at midnight
  workflow_dispatch:      # Manual trigger
  release:
    types: [published]
```

## Matrix Testing

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pytest
```

## Using Secrets

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: ./deploy.sh
```

## Workflow Structure

```
.github/
└── workflows/
    ├── ci.yml           # Test on every push/PR
    ├── cd.yml           # Deploy on release
    ├── docker.yml       # Build and push images
    └── scheduled.yml    # Cron jobs
```

## Reference Guides

For detailed patterns, see:

- **Workflow Syntax**: See [references/workflow-syntax.md](references/workflow-syntax.md) for triggers, jobs, steps, and expressions
- **CI Pipelines**: See [references/ci-pipelines.md](references/ci-pipelines.md) for testing, linting, and coverage
- **Matrix Strategies**: See [references/matrix-strategies.md](references/matrix-strategies.md) for multi-version and multi-platform testing
- **Secrets & Env**: See [references/secrets-env.md](references/secrets-env.md) for secure configuration
- **Docker Workflows**: See [references/docker-workflows.md](references/docker-workflows.md) for building and pushing images
- **Deployment**: See [references/deployment-automation.md](references/deployment-automation.md) for cloud deployments
