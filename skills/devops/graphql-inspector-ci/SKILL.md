---
name: graphql-inspector-ci
description: Use when setting up GraphQL Inspector in CI/CD pipelines, GitHub Actions, or GitLab CI for automated schema validation.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# GraphQL Inspector - CI/CD Integration

Expert knowledge of integrating GraphQL Inspector into continuous integration and deployment pipelines for automated schema and operation validation.

## Overview

GraphQL Inspector provides multiple integration options for CI/CD, from simple CLI commands to dedicated GitHub Apps and Actions. This skill covers all integration patterns for automated GraphQL quality enforcement.

## GitHub App

The official GitHub App provides the richest integration:

### Features

- Automatic schema diff on pull requests
- Comment with breaking changes summary
- Block merges on breaking changes
- Compare against base branch automatically

### Installation

1. Install from [GitHub Marketplace](https://github.com/marketplace/graphql-inspector)
2. Configure `.github/graphql-inspector.yaml`:

```yaml
schema: 'schema.graphql'
branch: 'main'
endpoint: 'https://api.example.com/graphql'
diff: true
notifications:
  slack: ${{ secrets.SLACK_WEBHOOK }}
```

## GitHub Actions

### Basic Schema Diff

```yaml
name: GraphQL Schema Check
on:
  pull_request:
    paths:
      - 'schema.graphql'
      - '**/*.graphql'

jobs:
  schema-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install GraphQL Inspector
        run: npm install -g @graphql-inspector/cli

      - name: Check for breaking changes
        run: |
          graphql-inspector diff \
            'git:origin/main:schema.graphql' \
            'schema.graphql'
```

### Complete Validation Pipeline

```yaml
name: GraphQL Validation
on:
  pull_request:
    paths:
      - '**/*.graphql'
      - 'src/**/*.tsx'
      - 'schema.graphql'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm install -g @graphql-inspector/cli

      - name: Schema Diff
        id: diff
        run: |
          graphql-inspector diff \
            'git:origin/main:schema.graphql' \
            'schema.graphql' \
            --onlyBreaking
        continue-on-error: true

      - name: Validate Operations
        run: |
          graphql-inspector validate \
            'src/**/*.graphql' \
            'schema.graphql' \
            --maxDepth 10

      - name: Audit Operations
        run: |
          graphql-inspector audit \
            'src/**/*.graphql'

      - name: Comment on PR
        if: steps.diff.outcome == 'failure'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '⚠️ Breaking GraphQL schema changes detected!'
            })
```

### Matrix Strategy for Multiple Schemas

```yaml
name: Multi-Schema Validation
on: pull_request

jobs:
  validate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service:
          - { name: 'users', schema: 'services/users/schema.graphql' }
          - { name: 'orders', schema: 'services/orders/schema.graphql' }
          - { name: 'products', schema: 'services/products/schema.graphql' }

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install GraphQL Inspector
        run: npm install -g @graphql-inspector/cli

      - name: Diff ${{ matrix.service.name }}
        run: |
          graphql-inspector diff \
            'git:origin/main:${{ matrix.service.schema }}' \
            '${{ matrix.service.schema }}'
```

## GitLab CI

### Basic Configuration

```yaml
stages:
  - validate

graphql-diff:
  stage: validate
  image: node:20
  before_script:
    - npm install -g @graphql-inspector/cli
  script:
    - graphql-inspector diff "git:origin/main:schema.graphql" schema.graphql
  rules:
    - changes:
        - "**/*.graphql"

graphql-validate:
  stage: validate
  image: node:20
  before_script:
    - npm install -g @graphql-inspector/cli
  script:
    - graphql-inspector validate 'src/**/*.graphql' schema.graphql
  rules:
    - changes:
        - "**/*.graphql"
        - "src/**/*.tsx"
```

### Merge Request Comments

```yaml
graphql-diff:
  stage: validate
  image: node:20
  script:
    - npm install -g @graphql-inspector/cli
    - |
      OUTPUT=$(graphql-inspector diff "git:origin/main:schema.graphql" schema.graphql 2>&1 || true)
      if [[ "$OUTPUT" == *"Breaking"* ]]; then
        curl --request POST \
          --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
          --data "body=⚠️ Breaking GraphQL changes detected" \
          "$CI_API_V4_URL/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID/notes"
      fi
```

## CircleCI

```yaml
version: 2.1

jobs:
  graphql-check:
    docker:
      - image: cimg/node:20.0
    steps:
      - checkout
      - run:
          name: Install GraphQL Inspector
          command: npm install -g @graphql-inspector/cli
      - run:
          name: Schema Diff
          command: |
            graphql-inspector diff \
              'git:origin/main:schema.graphql' \
              'schema.graphql'
      - run:
          name: Validate Operations
          command: |
            graphql-inspector validate \
              'src/**/*.graphql' \
              'schema.graphql'

workflows:
  validate:
    jobs:
      - graphql-check
```

## Configuration File

Create `.graphql-inspector.yaml` for all commands:

```yaml
# Schema configuration
schema:
  path: './schema.graphql'
  # Or for federation
  # federation: true

# Diff configuration
diff:
  rules:
    - suppressRemovalOfDeprecatedField
  failOnBreaking: true
  failOnDangerous: false
  notifications:
    slack: ${SLACK_WEBHOOK_URL}

# Validate configuration
validate:
  documents: './src/**/*.graphql'
  maxDepth: 10
  maxAliasCount: 5
  maxComplexityScore: 100

# Audit configuration
audit:
  documents: './src/**/*.graphql'
```

## Advanced Patterns

### Caching Dependencies

```yaml
# GitHub Actions with caching
- name: Cache npm
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-graphql-inspector

- name: Install GraphQL Inspector
  run: npm install -g @graphql-inspector/cli
```

### Slack Notifications

```yaml
- name: Notify Slack on breaking changes
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "⚠️ Breaking GraphQL changes in ${{ github.repository }}",
        "attachments": [{
          "color": "danger",
          "title": "Pull Request #${{ github.event.pull_request.number }}",
          "title_link": "${{ github.event.pull_request.html_url }}"
        }]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Required Status Checks

Configure repository settings:

1. Go to Settings → Branches → Branch protection rules
2. Enable "Require status checks to pass"
3. Add "GraphQL Schema Check" job as required

### Remote Schema Comparison

```yaml
- name: Diff against production
  run: |
    graphql-inspector diff \
      'https://api.production.example.com/graphql' \
      'schema.graphql'
  env:
    GRAPHQL_INSPECTOR_HEADERS: |
      Authorization: Bearer ${{ secrets.PROD_API_TOKEN }}
```

## Best Practices

1. **Fail fast** - Use `--onlyBreaking` to focus on critical issues
2. **Cache installation** - Speed up CI with npm caching
3. **Required checks** - Make schema validation a required check
4. **Branch protection** - Block merges with breaking changes
5. **Notifications** - Alert team on breaking changes
6. **Documentation** - Link to migration guides in comments
7. **Multiple environments** - Validate against staging and production
8. **Parallel jobs** - Run diff, validate, and audit in parallel

## Troubleshooting

### "Permission denied" for git refs

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Fetch full history
```

### "Schema not found" in CI

- Verify file path is correct in repository
- Check that schema is committed (not gitignored)
- Use absolute paths if relative paths fail

### Different results local vs CI

- Ensure same GraphQL Inspector version
- Check Node.js version matches
- Verify git refs are accessible

## When to Use This Skill

- Setting up automated schema validation
- Configuring breaking change detection in CI
- Building GraphQL quality gates
- Integrating with GitHub/GitLab workflows
- Creating PR comments for schema changes
- Blocking deployments with breaking changes
