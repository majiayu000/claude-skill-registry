---
name: ci-cd
description: Continuous Integration and Continuous Deployment best practices. Use when setting up automated build pipelines, test automation, deployment workflows, or improving release processes.
---

# CI/CD Skill

## Core Principle

**Automate everything from commit to production.**

CI/CD eliminates manual steps, catches issues early, and enables rapid, reliable releases. Every commit should automatically:
- Build
- Test
- Deploy (to appropriate environment)

---

## Continuous Integration (CI)

### What is CI?

**CI = Automatically build and test every commit**

When code is pushed:
1. Automated build runs
2. All tests execute
3. Code quality checks run
4. Team sees results immediately

### CI Pipeline Stages

```
┌─────────────────────────────────────────────────────┐
│              CI PIPELINE                            │
└─────────────────────────────────────────────────────┘

  Commit → Build → Test → Lint → Security → Report
    │        │       │      │        │          │
    │        ├──✅    ├──✅   ├──✅     ├──✅       ├──✅ PASS
    │        └──❌    └──❌   └──❌     └──❌       └──❌ FAIL
    │
    └──────► Block merge if any stage fails
```

### Essential CI Steps

1. **Checkout Code**
   ```yaml
   - uses: actions/checkout@v3
   ```

2. **Setup Environment**
   ```yaml
   - uses: actions/setup-node@v3
     with:
       node-version: '18'
   ```

3. **Install Dependencies**
   ```yaml
   - run: npm ci  # Use 'ci' not 'install' for reproducibility
   ```

4. **Build**
   ```yaml
   - run: npm run build
   ```

5. **Test**
   ```yaml
   - run: npm test -- --coverage
   ```

6. **Lint & Format Check**
   ```yaml
   - run: npm run lint
   - run: npm run format:check
   ```

7. **Security Scan**
   ```yaml
   - run: npm audit
   ```

---

## Continuous Deployment (CD)

### What is CD?

**CD = Automatically deploy passing builds to environments**

Deployment progression:
```
Development → Staging → Production
    ↑            ↑           ↑
  Auto        Auto      Manual approval
               or Auto
```

### Deployment Strategies

#### 1. Blue-Green Deployment

Two identical environments (Blue = current, Green = new):

```
┌────────────┐     ┌────────────┐
│   BLUE     │     │   GREEN    │
│ (Current)  │     │   (New)    │
└─────┬──────┘     └─────┬──────┘
      │                  │
      └────────┬─────────┘
               │
          ┌────▼────┐
          │  Router │ ← Switch traffic instantly
          └─────────┘
```

**Benefits:**
- Zero downtime
- Instant rollback (switch back to Blue)
- Test Green before switching

---

#### 2. Canary Deployment

Gradual rollout to subset of users:

```
Version A (old): 90% of traffic
Version B (new): 10% of traffic

  → Monitor metrics
  → If good: increase B to 50%
  → If good: increase B to 100%
  → If bad: rollback to 100% A
```

**Benefits:**
- Limit blast radius of bugs
- Real-world testing
- Data-driven rollout decisions

---

#### 3. Rolling Deployment

Update instances one at a time:

```
Instance 1: v1.0 → v1.1 ✅
Instance 2: v1.0 → v1.1 ✅  (after 1 is healthy)
Instance 3: v1.0 → v1.1 ✅  (after 2 is healthy)
```

**Benefits:**
- No downtime
- Automatic rollback if health checks fail
- Resource efficient

---

## CI/CD Pipeline Examples

### GitHub Actions (Node.js)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test -- --coverage

      - name: Build
        run: npm run build

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  deploy-staging:
    needs: build-and-test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to staging
        run: |
          echo "Deploying to staging..."
          # Your deployment script here

  deploy-production:
    needs: build-and-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # Your deployment script here
```

---

### GitLab CI (Python)

```yaml
stages:
  - test
  - build
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

test:
  stage: test
  image: python:3.11
  before_script:
    - python -m venv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
  script:
    - pytest --cov=src --cov-report=xml
    - pylint src/
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy-staging:
  stage: deploy
  only:
    - develop
  script:
    - echo "Deploy to staging"
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy-production:
  stage: deploy
  only:
    - main
  when: manual  # Requires approval
  script:
    - echo "Deploy to production"
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

---

## Best Practices

### 1. Fast Feedback

**Keep CI pipeline fast (<10 minutes):**

✅ **Do:**
- Parallel test execution
- Test only changed code (when possible)
- Cache dependencies
- Use faster test runners

❌ **Don't:**
- Run slow integration tests on every commit
- Rebuild everything from scratch
- Run tests sequentially

---

### 2. Fail Fast

**Stop pipeline at first failure:**

```yaml
# Good: Fail fast
- run: npm run lint
- run: npm test  # Only runs if lint passes
```

**Why:** Saves CI resources and developer time

---

### 3. Reproducible Builds

**Same input = same output:**

✅ **Do:**
- Lock dependency versions (`package-lock.json`, `Pipfile.lock`)
- Use specific tool versions (`node-version: '18.0.0'`)
- Use `npm ci` not `npm install`
- Tag Docker images with commit SHA

❌ **Don't:**
- Use `latest` tags
- Use version ranges without locks
- Rely on global installations

---

### 4. Separate Build from Deploy

**Build once, deploy many times:**

```
Build artifact → Test → Deploy to dev
                        Deploy to staging
                        Deploy to production
                     (Same artifact everywhere)
```

**Benefits:**
- Consistent deployments
- Faster deployments (no rebuild)
- Test the actual artifact that goes to production

---

### 5. Environment Parity

**Keep environments similar:**

```
Development ≈ Staging ≈ Production
```

**Same:**
- Operating system
- Runtime versions
- Configuration structure
- Database schema

**Different:**
- Scale (production has more resources)
- Data (production has real data)
- Secrets (different credentials)

---

### 6. Infrastructure as Code

**Define infrastructure in version control:**

```yaml
# terraform/main.tf
resource "aws_instance" "app" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"

  tags = {
    Name = "app-server"
  }
}
```

**Benefits:**
- Version controlled
- Reviewable
- Reproducible
- Self-documenting

---

## Security in CI/CD

### 1. Secrets Management

❌ **Never commit secrets:**
```yaml
# BAD - Secrets in code
- run: deploy.sh --api-key=abc123
```

✅ **Use secret management:**
```yaml
# GOOD - Secrets from vault
- run: deploy.sh --api-key=${{ secrets.API_KEY }}
```

---

### 2. Dependency Scanning

**Scan for vulnerabilities:**

```yaml
- name: Security audit
  run: |
    npm audit --audit-level=moderate
    # Or use Snyk, Dependabot, etc.
```

---

### 3. Container Scanning

**Scan Docker images:**

```yaml
- name: Scan image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'myapp:${{ github.sha }}'
    severity: 'CRITICAL,HIGH'
```

---

### 4. Least Privilege

**CI/CD should have minimal permissions:**

- Read-only access to repos
- Deploy-only access to environments
- No admin permissions
- Scoped tokens with expiration

---

## Monitoring CI/CD

### Key Metrics

1. **Build Success Rate**
   - Target: >95%
   - Track: Percentage of passing builds

2. **Build Time**
   - Target: <10 minutes
   - Track: P50, P95, P99 build durations

3. **Deployment Frequency**
   - Target: Multiple per day (for high-performing teams)
   - Track: Deployments per day/week

4. **Mean Time to Recovery (MTTR)**
   - Target: <1 hour
   - Track: Time from incident to fix deployed

5. **Change Failure Rate**
   - Target: <15%
   - Track: Percentage of deployments causing issues

---

## Troubleshooting

### Build Failures

**Debug steps:**

1. **Reproduce locally**
   ```bash
   # Use same versions as CI
   nvm use 18.0.0
   npm ci
   npm test
   ```

2. **Check CI logs**
   - Look for error messages
   - Check environment variables
   - Verify dependencies installed correctly

3. **Common issues:**
   - Flaky tests (non-deterministic)
   - Network timeouts
   - Resource limits (memory, disk)
   - Race conditions (parallel tests)

---

### Deployment Failures

**Rollback strategy:**

```bash
# Manual rollback
kubectl rollout undo deployment/app

# Or use previous Docker tag
docker pull myapp:$PREVIOUS_COMMIT_SHA
```

**Debug checklist:**
- [ ] Health checks passing?
- [ ] Database migrations applied?
- [ ] Configuration correct?
- [ ] Network connectivity?
- [ ] Resource limits sufficient?

---

## Integration with Other Skills

### With Git Hygiene

- CI runs on every commit
- Commit messages reference issues
- CI status visible in PRs

### With Testing Strategy

- CI runs all test levels
- Coverage tracked over time
- Failed tests block merge

### With Code Review

- CI results visible in PR
- Reviewers see test results
- Automated checks complement human review

---

## Quick Reference

### CI Pipeline Checklist

- [ ] Build on every commit
- [ ] Run all tests automatically
- [ ] Lint and format checks
- [ ] Security scans
- [ ] Fast feedback (<10 min)
- [ ] Block merge on failure

### CD Pipeline Checklist

- [ ] Automated deployment to dev/staging
- [ ] Manual approval for production (or automated with safeguards)
- [ ] Rollback strategy defined
- [ ] Health checks after deployment
- [ ] Monitoring and alerts configured

---

**Remember:** CI/CD is about automation, speed, and reliability. Build once, test thoroughly, deploy confidently. Fast feedback loops catch issues early. Automate the boring stuff, focus on building features.
