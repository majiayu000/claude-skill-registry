---
name: github-project-automation
description: GitHub repository automation (CI/CD, issue templates, Dependabot, CodeQL). Use for project setup, Actions workflows, security scanning, or encountering YAML syntax, workflow configuration, template structure errors.

  Keywords: github actions, github workflow, ci/cd, issue templates, pull request templates,
  dependabot, codeql, security scanning, yaml syntax, github automation, repository setup,
  workflow templates, github actions matrix, secrets management, branch protection, codeowners,
  github projects, continuous integration, continuous deployment, workflow syntax error,
  action version pinning, runner version, github context, yaml indentation error
license: MIT
metadata:
  version: 2.0.0
  last_verified: 2025-12-17
  optimization_date: 2025-12-17
  errors_prevented: 18
  token_savings: ~75%
  complexity: 8/10
---

# GitHub Project Automation

**Status**: Production Ready ✅
**Last Updated**: 2025-12-17
**Version**: 2.0.0 (Optimized with progressive disclosure)
**Dependencies**: None (git and gh CLI recommended)
**Latest Versions**: actions/checkout@v4.2.2, actions/setup-node@v4.1.0, github/codeql-action@v3.27.4

---

## Quick Start (15 Minutes)

### 1. Choose Your Framework

Select the workflow template that matches your project:

```bash
# For React/Vite projects
cp templates/workflows/ci-react.yml .github/workflows/ci.yml

# For Node.js libraries (matrix testing)
cp templates/workflows/ci-node.yml .github/workflows/ci.yml

# For Python projects
cp templates/workflows/ci-python.yml .github/workflows/ci.yml

# For Cloudflare Workers
cp templates/workflows/ci-cloudflare-workers.yml .github/workflows/deploy.yml

# For basic projects (any framework)
cp templates/workflows/ci-basic.yml .github/workflows/ci.yml
```

**Why this matters:**
- Pre-validated YAML prevents syntax errors
- SHA-pinned actions for security
- Explicit runner versions (ubuntu-24.04)
- All 8 GitHub Actions errors prevented

### 2. Add Issue Templates

```bash
# Create directory structure
mkdir -p .github/ISSUE_TEMPLATE

# Copy YAML templates (with validation)
cp templates/issue-templates/bug_report.yml .github/ISSUE_TEMPLATE/
cp templates/issue-templates/feature_request.yml .github/ISSUE_TEMPLATE/
```

**Why YAML over Markdown:**
- Required field validation (Error #12 prevented)
- Consistent data structure
- Better user experience
- No incomplete issues

### 3. Enable Security Scanning

```bash
# CodeQL for code analysis
cp templates/workflows/security-codeql.yml .github/workflows/codeql.yml

# Dependabot for dependency updates
cp templates/security/dependabot.yml .github/dependabot.yml
```

**CRITICAL:**
- CodeQL requires specific permissions (security-events: write)
- Dependabot has 10 PR limit per ecosystem
- Both must run on Dependabot PRs (Error #13 prevention)

---

## The 5-Step Complete Setup Process

### Step 1: Repository Structure

Create the standard GitHub automation directory structure:

```bash
# Create all required directories
mkdir -p .github/{workflows,ISSUE_TEMPLATE}

# Verify structure
tree .github/
# .github/
# ├── workflows/        # GitHub Actions workflows
# ├── ISSUE_TEMPLATE/   # Issue templates
# └── dependabot.yml    # Dependabot config (root of .github/)
```

**Key Points:**
- workflows/ is plural
- ISSUE_TEMPLATE/ is singular (legacy naming)
- dependabot.yml goes in .github/, NOT workflows/

### Step 2: Select Workflow Templates

Choose workflows based on your project needs:

**Continuous Integration (pick ONE):**
1. `ci-basic.yml` - Generic test/lint/build (all frameworks)
2. `ci-node.yml` - Node.js with matrix testing (18, 20, 22)
3. `ci-python.yml` - Python with matrix testing (3.10, 3.11, 3.12)
4. `ci-react.yml` - React/TypeScript with type checking

**Deployment (optional):**
5. `ci-cloudflare-workers.yml` - Deploy to Cloudflare Workers

**Security (recommended):**
6. `security-codeql.yml` - Code scanning
7. `dependabot.yml` - Dependency updates

**Copy selected templates:**
```bash
# Example: React app with security
cp templates/workflows/ci-react.yml .github/workflows/ci.yml
cp templates/workflows/security-codeql.yml .github/workflows/codeql.yml
cp templates/security/dependabot.yml .github/dependabot.yml
```

### Step 3: Configure Secrets (if deploying)

For deployment workflows (Cloudflare, AWS, etc.), add secrets:

```bash
# Using gh CLI
gh secret set CLOUDFLARE_API_TOKEN
# Paste your token when prompted

# Verify
gh secret list
```

**Critical Syntax:**
```yaml
# ✅ CORRECT
env:
  API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}

# ❌ WRONG - Missing double braces
env:
  API_TOKEN: $secrets.CLOUDFLARE_API_TOKEN
```

Prevents Error #6 (secrets syntax).

### Step 4: Add Issue/PR Templates

**Issue templates (YAML format):**
```bash
cp templates/issue-templates/bug_report.yml .github/ISSUE_TEMPLATE/
cp templates/issue-templates/feature_request.yml .github/ISSUE_TEMPLATE/
```

**PR template (Markdown format):**
```bash
cp templates/pr-templates/PULL_REQUEST_TEMPLATE.md .github/
```

**Why separate formats:**
- Issue templates: YAML for validation
- PR template: Markdown (GitHub limitation)

### Step 5: Customize for Your Project

**Required customizations:**

1. **Update usernames/emails:**
   ```yaml
   # In issue templates
   assignees:
     - secondsky  # ← Change to your GitHub username

   # In dependabot.yml
   reviewers:
     - "secondsky"  # ← Change to your username
   ```

2. **Adjust languages (CodeQL):**
   ```yaml
   # In security-codeql.yml
   matrix:
     language: ['javascript-typescript']  # ← Add your languages
     # Options: c-cpp, csharp, go, java-kotlin, python, ruby, swift
   ```

3. **Update package manager (Dependabot):**
   ```yaml
   # In dependabot.yml
   - package-ecosystem: "npm"  # ← Change if using yarn/pnpm/pip/etc
   ```

4. **Set deployment URL (Cloudflare):**
   ```yaml
   # In ci-cloudflare-workers.yml
   echo "Worker URL: https://your-worker.your-subdomain.workers.dev"
   # ← Update with your actual Worker URL
   ```

---

## Critical Rules

### Always Do

✅ **Pin actions to SHA, not @latest**
```yaml
# ✅ CORRECT
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

# ❌ WRONG
- uses: actions/checkout@latest
```

✅ **Use explicit runner versions**
```yaml
# ✅ CORRECT
runs-on: ubuntu-24.04  # Locked to specific LTS

# ❌ RISKY
runs-on: ubuntu-latest  # Changes over time
```

✅ **Include secrets in context syntax**
```yaml
# ✅ CORRECT
${{ secrets.API_TOKEN }}

# ❌ WRONG
$secrets.API_TOKEN
```

✅ **Validate YAML before committing**
```bash
# Use yamllint or GitHub's workflow validator
yamllint .github/workflows/*.yml
```

✅ **Test workflows on feature branch first**
```bash
git checkout -b test/github-actions
# Push and verify CI runs before merging to main
```

### Never Do

❌ **Don't use @latest for action versions**
- Breaks without warning when actions update
- Security risk (unvetted versions auto-adopted)

❌ **Don't hardcode secrets in workflows**
```yaml
# ❌ NEVER DO THIS
env:
  API_TOKEN: "sk_live_abc123..."  # Secret exposed in repo!
```

❌ **Don't skip build steps for compiled languages (CodeQL)**
```yaml
# ❌ WRONG - CodeQL fails for Java without build
- name: Perform CodeQL Analysis  # No .class files to analyze

# ✅ CORRECT - Include build
- name: Build project
  run: ./mvnw clean install
- name: Perform CodeQL Analysis  # Now has .class files
```

❌ **Don't ignore devDependencies in Dependabot**
- DevDependencies run during build, can execute malicious code
- Include both prod and dev dependencies

❌ **Don't use single ISSUE_TEMPLATE.md file**
```
# ❌ OLD WAY
.github/ISSUE_TEMPLATE.md

# ✅ NEW WAY
.github/ISSUE_TEMPLATE/
  bug_report.yml
  feature_request.yml
```

---

## Known Issues Prevention (Top 5)

This skill prevents **18** documented issues. Here are the top 5 most critical:

### Issue #1: YAML Indentation Errors ⚠️ MOST COMMON
**Error**: `workflow file is invalid. mapping values are not allowed in this context`
**Source**: Stack Overflow (most common GitHub Actions error)
**Why It Happens**: Spaces vs tabs, missing spaces after colons, inconsistent indentation
**Prevention**: Use skill templates with validated 2-space indentation
**Impact**: Workflow fails to parse, CI doesn't run

### Issue #2: Action Version Pinning Issues 🔒 SECURITY
**Error**: Workflow breaks unexpectedly after action updates
**Source**: GitHub Security Best Practices 2025
**Why It Happens**: Using `@latest` or `@v4` instead of specific SHA
**Prevention**: All templates pin to SHA with version comment
**Impact**: Unexpected breaking changes, security vulnerabilities

### Issue #3: Secrets Not Available 🔑
**Error**: `Secret not found` or empty variable
**Source**: GitHub Actions Debugging Guides
**Why It Happens**: Wrong syntax (`$secrets.NAME` instead of `${{ secrets.NAME }}`)
**Prevention**: Templates demonstrate correct context syntax
**Impact**: Deployment failures, broken CI/CD pipelines

### Issue #4: CodeQL Not Running on Dependabot PRs 🛡️
**Error**: Security scans skipped on dependency updates
**Source**: GitHub Community Discussion #121836
**Why It Happens**: Default trigger limitations
**Prevention**: Templates include `push: branches: [dependabot/**]`
**Impact**: Vulnerable dependencies merged without scanning

### Issue #5: Missing Required Fields in Issue Templates 📋
**Error**: Incomplete issues, missing critical info
**Source**: Community Feedback
**Why It Happens**: Markdown templates don't validate
**Prevention**: YAML templates with `required: true` validation
**Impact**: Can't reproduce bugs, wasted triage time

**For complete error documentation with all 18 issues**: Load `references/common-errors.md` when debugging GitHub Actions issues or configuring workflows.

---

## When to Load References

Load reference files when working on specific aspects of GitHub automation:

### Common Errors (`references/common-errors.md`)
Load when:
- Encountering workflow syntax errors
- Debugging failed GitHub Actions runs
- Setting up CodeQL or Dependabot for first time
- Resolving "Secret not found" errors
- Understanding why matrix builds fail
- Need detailed solutions for any of the 18 documented errors

### Workflow Patterns (`references/workflow-patterns.md`)
Load when:
- Implementing multi-version testing (Node.js 18/20/22)
- Setting up conditional deployments (main vs PR)
- Sharing build artifacts between jobs
- Integrating GitHub automation with other skills (cloudflare-worker-base, project-planning)
- Optimizing workflow performance
- Need examples of matrix strategies, artifact upload/download

### Configuration Examples (`references/configuration-examples.md`)
Load when:
- Creating dependabot.yml from scratch
- Configuring CodeQL for specific languages
- Setting up GitHub Actions secrets correctly
- Need complete working configuration files
- Understanding branch protection rules
- Creating issue/PR templates with proper validation

### Troubleshooting Guide (`references/troubleshooting-guide.md`)
Load when:
- Workflows not triggering despite pushing code
- CodeQL reports "No code found to analyze"
- Matrix builds all failing with same error
- Dependabot PRs consistently failing CI
- Permissions errors ("Resource not accessible by integration")
- Need step-by-step debugging procedures

### Advanced Configurations (`references/advanced-configurations.md`)
Load when:
- Setting up multi-environment deployments (staging/production)
- Creating reusable workflows or composite actions
- Optimizing CI/CD pipeline performance
- Implementing advanced matrix strategies
- Using OIDC for cloud authentication (no long-lived secrets)
- Need workflow optimization techniques

---

## Integration with Existing Skills

### cloudflare-worker-base → Add CI/CD

When user creates new Worker project:

```bash
# User: "Create Cloudflare Worker with CI/CD"

# This skill runs AFTER cloudflare-worker-base
cp templates/workflows/ci-cloudflare-workers.yml .github/workflows/deploy.yml

# Configure secrets
gh secret set CLOUDFLARE_API_TOKEN
```

**Result**: New Worker with automated deployment on push to main

### project-planning → Generate Automation

When user uses project-planning skill:

```bash
# User: "Plan new React app with GitHub automation"

# project-planning generates IMPLEMENTATION_PHASES.md
# Then this skill sets up GitHub automation
cp templates/workflows/ci-react.yml .github/workflows/ci.yml
cp templates/issue-templates/*.yml .github/ISSUE_TEMPLATE/
```

**Result**: Planned project with complete GitHub automation

### open-source-contributions → Setup Contributor Experience

When preparing project for open source:

```bash
# User: "Prepare repo for open source contributions"

# open-source-contributions skill handles CONTRIBUTING.md
# This skill adds issue templates and CODEOWNERS
cp templates/issue-templates/*.yml .github/ISSUE_TEMPLATE/
cp templates/misc/CODEOWNERS .github/
```

**Result**: Contributor-friendly repository

---

## Dependencies

**Required**:
- **Git** 2.0+ - Version control
- **GitHub CLI (gh)** 2.0+ - Secret management, PR creation (optional but recommended)

**Optional**:
- **yamllint** 1.20+ - YAML validation before commit
- **act** (local GitHub Actions runner) - Test workflows locally

**Install gh CLI**:
```bash
# macOS
brew install gh

# Ubuntu
sudo apt install gh

# Verify
gh --version
```

---

## Official Documentation

- **GitHub Actions**: https://docs.github.com/en/actions
- **Workflow Syntax**: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- **CodeQL**: https://codeql.github.com/docs/
- **Dependabot**: https://docs.github.com/en/code-security/dependabot
- **Issue Templates**: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests

**Context7 Library ID**: Search for `/websites/github` or `/github/` in Context7 MCP

---

## Complete Setup Checklist

Use this checklist to verify your GitHub automation setup:

**Workflows:**
- [ ] Created `.github/workflows/` directory
- [ ] Copied appropriate CI workflow template
- [ ] Updated usernames in workflow files
- [ ] Configured secrets (if deploying)
- [ ] SHA-pinned all actions (not @latest)
- [ ] Explicit runner version (ubuntu-24.04)
- [ ] Workflow triggers match branches (main/master)

**Issue Templates:**
- [ ] Created `.github/ISSUE_TEMPLATE/` directory
- [ ] Copied bug_report.yml
- [ ] Copied feature_request.yml
- [ ] Updated assignees to your GitHub username
- [ ] YAML templates use `required: true` for critical fields

**PR Template:**
- [ ] Copied PULL_REQUEST_TEMPLATE.md to `.github/`
- [ ] Customized checklist for your project needs

**Security:**
- [ ] Copied security-codeql.yml
- [ ] Added correct languages to CodeQL matrix
- [ ] Set `security-events: write` permission
- [ ] Copied dependabot.yml
- [ ] Updated package-ecosystem (npm/pip/etc.)
- [ ] Set reviewers in dependabot.yml

**Testing:**
- [ ] Pushed to feature branch first (not main)
- [ ] Verified CI runs successfully
- [ ] Checked Actions tab for any errors
- [ ] Validated YAML syntax locally
- [ ] Tested secret access (if applicable)

**Documentation:**
- [ ] Added badge to README.md (optional)
- [ ] Documented required secrets in README
- [ ] Updated CONTRIBUTING.md (if open source)

---

**Questions? Issues?**

1. Check `references/common-errors.md` for all 18 errors
2. Verify workflow YAML is valid: `yamllint .github/workflows/*.yml`
3. Check GitHub Actions tab for detailed error messages
4. Review official docs: https://docs.github.com/en/actions
5. Ensure secrets are configured: `gh secret list`

---

**Last Updated**: 2025-12-17
**Version**: 2.0.0 (Optimized with progressive disclosure)
**Status**: Production Ready
