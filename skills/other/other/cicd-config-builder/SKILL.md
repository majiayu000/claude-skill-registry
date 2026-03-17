---
name: building-cicd-configs
description: Generates or updates CI/CD pipeline configurations for GitHub Actions, GitLab CI, or CircleCI. Use when the user asks to set up CI/CD, create workflows, automate deployment, or mentions GitHub Actions, pipelines, or continuous integration.
---

# CI/CD Config Builder

## When to use this skill

- User asks to set up CI/CD for a project
- User wants to create GitHub Actions workflows
- User mentions GitLab CI or CircleCI
- User wants to automate linting, testing, or deployment
- User asks to add a pipeline step or job

## Workflow

- [ ] Detect project type and framework
- [ ] Identify target CI/CD platform
- [ ] Determine required pipeline stages
- [ ] Generate pipeline configuration
- [ ] Validate config syntax locally
- [ ] Present for user approval

## Instructions

### Step 1: Detect Project Type

Check for framework indicators:

| Framework | Indicators                                       |
| --------- | ------------------------------------------------ |
| Next.js   | `next.config.*`, `"next"` in package.json        |
| Nuxt      | `nuxt.config.*`, `"nuxt"` in package.json        |
| Vite      | `vite.config.*`, `"vite"` in package.json        |
| Node.js   | `package.json` without frontend framework        |
| Static    | `index.html` at root, no package.json            |
| Python    | `requirements.txt`, `pyproject.toml`, `setup.py` |

Detect package manager:

```bash
ls package-lock.json yarn.lock pnpm-lock.yaml bun.lockb 2>/dev/null | head -1
```

Check for existing scripts:

```bash
npm pkg get scripts 2>/dev/null
```

### Step 2: Identify CI/CD Platform

Check for existing configs:

```bash
ls -la .github/workflows/ .gitlab-ci.yml .circleci/config.yml 2>/dev/null
```

Platform selection:

- **GitHub Actions**: Default for GitHub repos, `.github/workflows/*.yml`
- **GitLab CI**: For GitLab repos, `.gitlab-ci.yml`
- **CircleCI**: If `.circleci/` exists or user specifies

### Step 3: Determine Pipeline Stages

Standard pipeline flow:

```
install → lint → test → build → deploy
```

Required stages based on project:

- Has ESLint/Prettier → include `lint`
- Has test framework → include `test`
- Has build script → include `build`
- Has deployment target → include `deploy`

### Step 4: Generate Configuration

**GitHub Actions (Node.js/Next.js):**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm test

      - name: Build
        run: npm run build
```

**GitHub Actions (with matrix):**

```yaml
jobs:
  ci:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: "npm"

      - run: npm ci
      - run: npm run lint
      - run: npm test
```

**GitLab CI:**

```yaml
stages:
  - install
  - lint
  - test
  - build

variables:
  npm_config_cache: "$CI_PROJECT_DIR/.npm"

cache:
  paths:
    - .npm/
    - node_modules/

install:
  stage: install
  image: node:20
  script:
    - npm ci

lint:
  stage: lint
  image: node:20
  script:
    - npm run lint

test:
  stage: test
  image: node:20
  script:
    - npm test
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'

build:
  stage: build
  image: node:20
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
```

**CircleCI:**

```yaml
version: 2.1

orbs:
  node: circleci/node@5

jobs:
  build-and-test:
    executor:
      name: node/default
      tag: "20"
    steps:
      - checkout
      - node/install-packages
      - run:
          name: Lint
          command: npm run lint
      - run:
          name: Test
          command: npm test
      - run:
          name: Build
          command: npm run build

workflows:
  ci:
    jobs:
      - build-and-test
```

### Step 5: Add Deployment (Optional)

**Vercel (GitHub Actions):**

```yaml
deploy:
  needs: ci
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main'
  steps:
    - uses: actions/checkout@v4
    - uses: amondnet/vercel-action@v25
      with:
        vercel-token: ${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
        vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
        vercel-args: "--prod"
```

**AWS S3 (GitHub Actions):**

```yaml
deploy:
  needs: ci
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main'
  steps:
    - uses: actions/checkout@v4
    - run: npm ci && npm run build
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    - run: aws s3 sync ./dist s3://${{ secrets.S3_BUCKET }} --delete
```

### Step 6: Validate Configuration

**GitHub Actions:**

```bash
# Install actionlint
brew install actionlint
actionlint .github/workflows/*.yml
```

**GitLab CI:**

```bash
# Use GitLab's CI Lint API or local validation
gitlab-ci-lint .gitlab-ci.yml
```

**CircleCI:**

```bash
circleci config validate .circleci/config.yml
```

**YAML syntax check:**

```bash
npx yaml-lint .github/workflows/*.yml
```

## Common Additions

**Environment variables:**

```yaml
env:
  NODE_ENV: production
  CI: true
```

**Caching (GitHub Actions):**

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

**Conditional jobs:**

```yaml
if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

**Secrets reference:**

```yaml
${{ secrets.SECRET_NAME }}
```

## Validation

Before completing:

- [ ] Config syntax is valid
- [ ] All referenced scripts exist in package.json
- [ ] Secrets are documented (not values, just names needed)
- [ ] Node version matches project requirements
- [ ] Cache configuration is correct for package manager

## Error Handling

- **Workflow not triggering**: Check branch names and `on:` triggers match.
- **Action not found**: Verify action version exists (e.g., `@v4` not `@v5`).
- **Secrets missing**: Document required secrets for user to add in repo settings.
- **Syntax error**: Run `actionlint` or YAML linter locally.
- **Unsure about syntax**: Check platform documentation or run `--help` on CLI tools.

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitLab CI Documentation](https://docs.gitlab.com/ee/ci/)
- [CircleCI Documentation](https://circleci.com/docs/)
- [actionlint](https://github.com/rhysd/actionlint)
