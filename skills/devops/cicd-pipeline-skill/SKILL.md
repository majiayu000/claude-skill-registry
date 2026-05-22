---
document_name: "cicd-pipeline.skill.md"
location: ".claude/skills/cicd-pipeline.skill.md"
codebook_id: "CB-SKILL-CICD-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for CI/CD pipeline configuration and maintenance"
skill_metadata:
  category: "devops"
  complexity: "advanced"
  estimated_time: "varies"
  prerequisites:
    - "GitHub repository access"
    - "Understanding of build process"
category: "skills"
status: "active"
tags:
  - "skill"
  - "cicd"
  - "devops"
  - "github-actions"
ai_parser_instructions: |
  This skill defines procedures for CI/CD pipeline management.
  Section markers: === SECTION ===
  Procedure markers: === PROCEDURE: NAME ===
---

# CI/CD Pipeline Skill

=== PURPOSE ===

This skill provides procedures for configuring and maintaining CI/CD pipelines. Used by the DevOps Engineer for all pipeline-related work.

---

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(devops-engineer) @ref(CB-AGENT-DEVOPS-001) | Primary skill for pipelines |

---

=== PREREQUISITES ===

Before using this skill:
- [ ] Repository access with Actions enabled
- [ ] Understanding of project build process
- [ ] Test suite available

---

=== PROCEDURE: Create CI Workflow ===

**Location:** `.github/workflows/ci.yml`

**Purpose:** Run tests and checks on every PR

**Template:**
```yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
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
      - run: npm ci
      - run: npm test
      - run: npm run lint
      - run: npm run typecheck

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
```

---

=== PROCEDURE: Create CD Workflow ===

**Location:** `.github/workflows/deploy.yml`

**Purpose:** Deploy on release

**Template:**
```yaml
name: Deploy

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: |
          # Deployment commands here
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

---

=== PROCEDURE: Pipeline Stages ===

**Standard Stages:**
1. **Checkout** - Get code
2. **Setup** - Install dependencies
3. **Lint** - Code style checks
4. **Test** - Run test suite
5. **Build** - Create artifacts
6. **Deploy** - Ship to environment

**Stage Dependencies:**
```
checkout → setup → lint
                 → test  → build → deploy
```

---

=== PROCEDURE: Caching ===

**Purpose:** Speed up builds

**Common Caches:**
```yaml
# Node.js
- uses: actions/setup-node@v4
  with:
    cache: 'npm'

# Python
- uses: actions/setup-python@v5
  with:
    cache: 'pip'

# Custom cache
- uses: actions/cache@v4
  with:
    path: ~/.cache/custom
    key: ${{ runner.os }}-custom-${{ hashFiles('**/lockfile') }}
```

---

=== PROCEDURE: Secret Management ===

**Purpose:** Handle sensitive data

**Steps:**
1. Go to Settings > Secrets and variables > Actions
2. Add repository secret
3. Reference in workflow: `${{ secrets.SECRET_NAME }}`

**Best Practices:**
- Never log secrets
- Use environment-specific secrets
- Rotate secrets regularly
- Use OIDC for cloud providers

---

=== PROCEDURE: Branch Protection ===

**Purpose:** Enforce CI before merge

**Settings:**
- Require status checks to pass
- Require branches to be up to date
- Select required checks (test, lint, build)

---

=== ANTI-PATTERNS ===

### No Caching
**Problem:** Slow builds from fresh installs
**Solution:** Cache dependencies and build artifacts

### Secrets in Code
**Problem:** Sensitive data in workflow files
**Solution:** Use GitHub Secrets

### No Failure Notifications
**Problem:** Silent failures
**Solution:** Add failure notifications

### Sequential When Parallel Possible
**Problem:** Slow pipelines
**Solution:** Parallelize independent jobs

---

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(deployment) | CI triggers deployment |
| @skill(infrastructure) | Infrastructure supports CI |
