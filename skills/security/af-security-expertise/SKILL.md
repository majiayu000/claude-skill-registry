---
name: af-security-expertise
description: Use when configuring security tooling, running security audits, or adding vulnerability scanning to projects. Covers Dependabot, npm audit, GitHub secret scanning, and CI security workflows.

title: Security Expertise
created: 2026-01-06
updated: 2026-01-06
last_checked: 2026-01-06
tags: [skill, expertise, security, dependabot, audit, secrets]
parent: ../README.md
---

# Security Expertise

Directive knowledge for configuring and using security tooling in AgentFlow projects.

## When to Use This Skill

Load this skill when you need to:
- Configure Dependabot for dependency updates
- Add security scanning to CI workflows
- Audit a project's security posture
- Set up secret detection
- Understand security best practices

## Quick Reference

| Tool | Purpose | Setup Location |
|------|---------|----------------|
| **Dependabot** | Auto-PRs for vulnerable deps | `.github/dependabot.yml` |
| **npm audit** | Check for known vulnerabilities | CI workflow step |
| **GitHub Secret Scanning** | Detect leaked secrets | Repo settings (manual) |
| **gitleaks** | Pre-commit secret detection | Optional hook |

---

## Rules

### Security Configuration Rules (MUST)

1. **MUST add Dependabot** to all new projects - it's zero-maintenance security.

2. **MUST add npm audit** to CI workflows - fail builds on high/critical vulnerabilities.

3. **MUST NOT commit secrets** - use Doppler for all credentials.

4. **MUST document manual steps** - GitHub secret scanning requires UI enablement.

### Security Configuration Rules (SHOULD)

5. **SHOULD enable GitHub secret scanning** on all repositories.

6. **SHOULD review Dependabot PRs weekly** - don't let them pile up.

7. **SHOULD use `npm audit --audit-level=high`** - moderate issues can wait.

---

## Workflows

### Workflow: Add Security to New Project

**When:** Setting up greenfield or brownfield project.

**Steps:**

1. **Create Dependabot config:**
   ```bash
   cp .claude/templates/github/dependabot.yml .github/dependabot.yml
   ```

2. **Add npm audit to CI** (if GitHub Actions exist):
   ```yaml
   - name: Security audit
     run: npm audit --audit-level=high
   ```

3. **Enable secret scanning** (manual):
   - Go to repo Settings → Security → Secret scanning
   - Enable "Secret scanning"
   - Enable "Push protection" (blocks commits with secrets)

4. **Verify setup:**
   ```bash
   # Check Dependabot config exists
   test -f .github/dependabot.yml && echo "✅ Dependabot configured"

   # Check for npm audit in CI
   grep -r "npm audit" .github/workflows/ && echo "✅ npm audit in CI"
   ```

### Workflow: Security Audit

**When:** Running `/security:audit` command or checking project security posture.

**Checks to perform:**

| Check | How | Pass Criteria |
|-------|-----|---------------|
| Dependabot config | `test -f .github/dependabot.yml` | File exists |
| npm audit in CI | `grep "npm audit" .github/workflows/*.yml` | Found in workflow |
| No high vulnerabilities | `npm audit --audit-level=high` | Exit code 0 |
| No secrets in code | `grep -rE "(password\|secret\|api_key)\s*=\s*['\"][^'\"]+['\"]" src/` | No matches |

**Output format:**
```
Security Audit Results:

✅ Dependabot configured (.github/dependabot.yml)
✅ npm audit in CI workflow
⚠️  GitHub secret scanning - check manually: [repo settings link]
❌ npm audit found 2 high vulnerabilities

Run `npm audit fix` to resolve vulnerabilities.
```

### Workflow: Fix Vulnerabilities

**When:** npm audit reports issues.

**Steps:**

1. **Try automatic fix:**
   ```bash
   npm audit fix
   ```

2. **If breaking changes required:**
   ```bash
   npm audit fix --force  # Use with caution
   ```

3. **If fix unavailable:**
   - Check if vulnerability is exploitable in your context
   - Consider alternative packages
   - Document accepted risk if proceeding

---

## Templates

### Dependabot Configuration

**Location:** `.claude/templates/github/dependabot.yml`

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "security"
```

### CI Security Step

**Add to GitHub Actions workflow:**

```yaml
- name: Security audit
  run: npm audit --audit-level=high
```

**For GainInsight Standard projects, add after install step in workflow.**

---

## Integration Points

### With Setup Process

- **Greenfield:** Creates `.github/dependabot.yml` during initial setup
- **Brownfield:** Adds security phase to setup process

### With GainInsight Standard

- **Layer 4 (CI/CD):** npm audit step in GitHub Actions workflows
- **Templates:** Security workflow snippet in templates

### With af:sync

- Checks for missing security configs
- Offers to create if missing

### With Hook

- `git-commit-reminder` includes security awareness prompt

---

## Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| Dependabot PRs piling up | Not reviewing weekly | Schedule weekly review |
| npm audit false positives | Dev dependencies flagged | Use `--omit=dev` for production |
| CI failing on moderate issues | audit-level too strict | Use `--audit-level=high` |
| Secret scanning not working | Not enabled in settings | Manual UI enablement required |

---

## Future Expansion

This skill can be extended to cover:

- **SonarQube** - Code quality and security analysis
- **Snyk** - Advanced vulnerability scanning
- **OWASP ZAP** - Dynamic application security testing
- **License compliance** - Dependency license checking
- **Container scanning** - Docker image vulnerabilities

---

## Related Documentation

- [GainInsight Layer 4: CI/CD](../../docs/guides/gaininsight-standard/layer-4-cicd.md)
- [Setup Process](../af-setup-process/SKILL.md)
- [Dependabot Template](../../templates/github/dependabot.yml)
