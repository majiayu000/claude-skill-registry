---
name: ci-cd-pipeline
description: Set up and maintain continuous integration and continuous deployment pipelines with GitHub Actions, GitLab CI, Jenkins, or similar tools to automate testing, building, and deployment. Use when configuring automated builds, setting up test automation, implementing deployment automation, creating release workflows, managing environment deployments, configuring build caching, implementing blue-green deployments, setting up rollback strategies, or automating the entire software delivery pipeline.
---

# CI/CD Pipeline - Automating Build, Test, and Deployment

## Package Manager Detection

**IMPORTANT**: Before creating CI/CD configurations, detect the project's package manager by checking for lockfiles and adapt all commands accordingly.

**Detection Order** (first match wins):
1. `bun.lockb` → Use **bun**
2. `pnpm-lock.yaml` → Use **pnpm**
3. `yarn.lock` → Use **yarn**
4. `package-lock.json` → Use **npm**

**Command Mapping** - Adapt examples in this skill to use the detected package manager:

| Action | npm | yarn | pnpm | bun |
|--------|-----|------|------|-----|
| Install (CI) | `npm ci` | `yarn install --frozen-lockfile` | `pnpm install --frozen-lockfile` | `bun install --frozen-lockfile` |
| Run script | `npm run <script>` | `yarn <script>` | `pnpm <script>` | `bun run <script>` |
| Execute bin | `npx <cmd>` | `yarn dlx <cmd>` | `pnpm dlx <cmd>` | `bunx <cmd>` |
| Cache key | `package-lock.json` | `yarn.lock` | `pnpm-lock.yaml` | `bun.lockb` |
| Cache path | `~/.npm` | `~/.yarn/cache` | `~/.pnpm-store` | `~/.bun/install/cache` |

**Note**: The examples below use npm by default. When implementing, replace with the appropriate commands for your detected package manager.

---

## When to use this skill

- Setting up GitHub Actions or GitLab CI workflows
- Automating test execution on every commit
- Implementing automated builds and deployments
- Creating release and versioning workflows
- Managing staging and production deployments
- Configuring build caching for faster pipelines
- Implementing blue-green or canary deployments
- Setting up automatic rollback on failures
- Running linting and type checking in CI
- Automating database migrations in pipelines
- Implementing security scanning in CI
- Creating deployment approval workflows

## When to use this skill

- Setting up continuous integration, automating deployments, configuring build pipelines, or implementing DevOps workflows.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Setting up continuous integration, automating deployments, configuring build pipelines, or implementing DevOps workflows.

## Core Principles

1. **Automate Everything** - Manual steps are error-prone
2. **Fail Fast** - Catch issues early in the pipeline
3. **Test Before Deploy** - Never deploy untested code
4. **Reproducible Builds** - Same inputs = same outputs
5. **Zero-Downtime Deployments** - Users never affected

## GitHub Actions

### 1. **Basic CI Workflow**

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run type check
        run: npm run typecheck
      
      - name: Run tests
        run: npm test -- --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

### 2. **Matrix Testing**

```yaml
# Test across multiple versions
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [18, 20, 21]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - run: npm ci
      - run: npm test
```

### 3. **Deploy Workflow**

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - run: npm ci
      - run: npm run build
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### 4. **Docker Build & Push**

```yaml
name: Docker

on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: myorg/myapp
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=registry,ref=myorg/myapp:buildcache
          cache-to: type=registry,ref=myorg/myapp:buildcache,mode=max
```

### 5. **E2E Testing**

```yaml
name: E2E Tests

on:
  pull_request:

jobs:
  e2e:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - run: npm ci
      
      - name: Install Playwright
        run: npx playwright install --with-deps
      
      - name: Run E2E tests
        run: npm run test:e2e
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

## GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "20"

lint:
  stage: lint
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run lint
    - npm run typecheck

test:
  stage: test
  image: node:${NODE_VERSION}
  services:
    - postgres:15
  variables:
    POSTGRES_DB: test
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
  script:
    - npm ci
    - npm test -- --coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

build:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/

deploy:production:
  stage: deploy
  image: node:${NODE_VERSION}
  script:
    - npm install -g vercel
    - vercel --prod --token=$VERCEL_TOKEN
  only:
    - main
```

## Deployment Strategies

### 1. **Blue-Green Deployment**

```yaml
# Deploy to staging slot first
- name: Deploy to staging
  run: |
    az webapp deployment slot create \
      --name myapp \
      --resource-group mygroup \
      --slot staging
    
    az webapp deployment source config-zip \
      --name myapp \
      --resource-group mygroup \
      --slot staging \
      --src ./dist.zip

# Run smoke tests against staging
- name: Smoke tests
  run: npm run test:smoke -- --url=https://myapp-staging.azurewebsites.net

# Swap staging to production (instant cutover)
- name: Swap to production
  run: |
    az webapp deployment slot swap \
      --name myapp \
      --resource-group mygroup \
      --slot staging \
      --target-slot production
```

### 2. **Canary Deployment**

```yaml
# Deploy to 10% of servers first
- name: Deploy canary
  run: |
    kubectl set image deployment/myapp \
      myapp=myapp:${{ github.sha }} \
      --record
    
    kubectl patch deployment myapp \
      -p '{"spec":{"replicas":1}}'

# Monitor for 10 minutes
- name: Monitor canary
  run: |
    sleep 600
    ERROR_RATE=$(kubectl logs -l app=myapp --tail=1000 | grep ERROR | wc -l)
    if [ $ERROR_RATE -gt 10 ]; then
      echo "High error rate, rolling back"
      kubectl rollout undo deployment/myapp
      exit 1
    fi

# Scale to 100% if healthy
- name: Full deployment
  run: kubectl scale deployment myapp --replicas=5
```

### 3. **Rolling Deployment**

```yaml
# Kubernetes rolling update (zero downtime)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Max 1 extra pod during update
      maxUnavailable: 1  # Max 1 pod down at a time
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Pipeline Best Practices

### 1. **Caching**

```yaml
# Cache dependencies
- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

# Cache build outputs
- name: Cache build
  uses: actions/cache@v3
  with:
    path: .next/cache
    key: ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}
```

### 2. **Secrets Management**

```yaml
# ✅ Store secrets in CI/CD platform
jobs:
  deploy:
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          echo "API_KEY is set: ${API_KEY:+yes}"
          npm run deploy

# ✅ Use vault for sensitive data
- name: Import secrets
  uses: hashicorp/vault-action@v2
  with:
    url: https://vault.example.com
    token: ${{ secrets.VAULT_TOKEN }}
    secrets: |
      secret/data/prod api_key | API_KEY ;
      secret/data/prod db_url | DATABASE_URL
```

### 3. **Quality Gates**

```yaml
jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run tests with coverage
        run: npm test -- --coverage
      
      - name: Check coverage threshold
        run: |
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80%"
            exit 1
          fi
      
      - name: SonarQube Scan
        uses: sonarsource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      
      - name: Check quality gate
        run: |
          STATUS=$(curl -u $SONAR_TOKEN: \
            "https://sonarcloud.io/api/qualitygates/project_status?projectKey=myproject" \
            | jq -r '.projectStatus.status')
          
          if [ "$STATUS" != "OK" ]; then
            echo "Quality gate failed"
            exit 1
          fi
```

### 4. **Notifications**

```yaml
jobs:
  notify:
    runs-on: ubuntu-latest
    if: always()
    needs: [test, build, deploy]
    steps:
      - name: Slack notification
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Deployment ${{ job.status }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
      
      - name: Email notification
        if: failure()
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.MAIL_USERNAME }}
          password: ${{ secrets.MAIL_PASSWORD }}
          subject: 'CI/CD Failed: ${{ github.workflow }}'
          body: 'Build failed on ${{ github.ref }}'
          to: team@example.com
```

## CI/CD Checklist

```
Build Pipeline:
□ Automated on every commit
□ Runs linting and type checking
□ Executes all tests
□ Generates code coverage reports
□ Builds production artifacts
□ Caches dependencies for speed

Quality Gates:
□ Minimum code coverage threshold (e.g., 80%)
□ No critical vulnerabilities (npm audit, Snyk)
□ Code quality checks (SonarQube)
□ No linting errors
□ All tests passing

Deployment:
□ Automated deployment to staging
□ Manual approval for production
□ Health checks before traffic switch
□ Rollback capability
□ Zero-downtime strategy (blue-green, canary, rolling)

Security:
□ Secrets stored securely (not in code)
□ Dependency scanning (Dependabot)
□ Container vulnerability scanning
□ SAST/DAST security scans
□ Signed commits required

Monitoring:
□ Build status notifications (Slack, email)
□ Deployment notifications
□ Error rate monitoring post-deploy
□ Automatic rollback on errors
□ Audit logs maintained
```

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)
- [The DevOps Handbook](https://itrevolution.com/product/the-devops-handbook/)

---

**Remember**: Great CI/CD pipelines are fast, reliable, and give developers confidence to deploy frequently.
