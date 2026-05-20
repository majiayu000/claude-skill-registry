---
name: security-scan
description: Security scan workflow — dependency audit, OWASP checklist, secrets scan, vulnerability report. Applies software-engineer role with security focus. Use standalone or as part of code review.
context: fork
allowed-tools: Read, Grep, Glob, Bash
---

# Security Scan

Automated security audit for the project. Checks dependencies for known vulnerabilities, scans for hardcoded secrets, and reviews code against OWASP guidelines.

## 1. Detect Project Stack

Read `CLAUDE.md` and project config to determine:

- **Language(s)** and dependency managers
- **Infrastructure** (Docker, Kubernetes, Terraform)
- **Existing security tools** (Snyk, Trivy, OWASP dependency-check, etc.)

## 2. Dependency Audit

Run the project's dependency vulnerability scanner:

| Stack | Command |
|---|---|
| Node.js (npm) | `npm audit` |
| Node.js (pnpm) | `pnpm audit` |
| Node.js (yarn) | `yarn audit` |
| Python (pip) | `pip-audit` or `safety check` |
| Python (poetry) | `poetry audit` or `pip-audit` |
| Java (Maven) | `mvn org.owasp:dependency-check-maven:check` |
| Java (Gradle) | `gradle dependencyCheckAnalyze` |
| Go | `govulncheck ./...` |
| .NET | `dotnet list package --vulnerable` |
| Docker | `trivy image <image-name>` or `docker scout cves` |

Classify findings by severity:

| Severity | Action |
|---|---|
| **Critical / High** | Must fix before merge. Upgrade dependency or apply workaround |
| **Medium** | Should fix. Schedule if no immediate upgrade available |
| **Low** | Track. Fix in next maintenance cycle |

## 3. Secrets Scan

Scan the codebase for hardcoded secrets:

```
// turbo
git log --diff-filter=A --name-only --pretty=format: | sort -u
```

Check for common secret patterns in source files:
- API keys (AWS, GCP, GitHub, Slack)
- Private keys (RSA, EC, SSH)
- Connection strings with credentials
- JWT tokens and bearer tokens
- Passwords in config files

**Tools** (if available):
- `gitleaks detect --source .`
- `trufflehog filesystem .`
- `detect-secrets scan`

## 4. OWASP Top 10 Review

Manual code review against OWASP Top 10 (2021):

| # | Risk | What to Check |
|---|---|---|
| A01 | Broken Access Control | Authorization checks on every endpoint, CORS policy, directory traversal |
| A02 | Cryptographic Failures | TLS enforcement, password hashing, data encryption, no weak algorithms |
| A03 | Injection | SQL/NoSQL/OS command injection, parameterized queries, input validation |
| A04 | Insecure Design | Threat model, rate limiting, business logic flaws |
| A05 | Security Misconfiguration | Default credentials, debug mode, unnecessary features, error messages |
| A06 | Vulnerable Components | Dependency audit results (Step 2) |
| A07 | Auth Failures | Brute force protection, session management, MFA |
| A08 | Data Integrity Failures | CI/CD pipeline security, deserialization, update verification |
| A09 | Logging Failures | Security event logging, no PII in logs, monitoring |
| A10 | SSRF | Server-side request validation, allowlists for external calls |

Use `code-review` skill's `security-checklist.md` for detailed checks.

## 5. Infrastructure Security (if applicable)

### Docker
- Base images from trusted registries
- No `latest` tag — pinned versions
- Non-root user in container
- No secrets in Dockerfile or image layers
- Minimal base image (distroless/alpine)

### Kubernetes
- Pods run as non-root with read-only filesystem
- Network policies restrict traffic
- Secrets in Kubernetes Secrets or external vault
- Resource limits set on all containers
- RBAC follows least-privilege

### Terraform
- No hardcoded credentials in `.tf` files
- State file encrypted and access-controlled
- Security groups follow least-privilege
- Encryption enabled for storage and databases

## 6. Report

```
## Security Scan Report

### Summary
- **Risk level**: LOW / MEDIUM / HIGH / CRITICAL
- **Scan date**: [date]
- **Scope**: [what was scanned]

### Dependency Vulnerabilities
| Package | Current | Fixed In | Severity | CVE |
|---------|---------|----------|----------|-----|
| [pkg]   | [ver]   | [ver]    | [sev]    | [id]|

### Secrets Found
- [ ] [file:line] — [type of secret] — **ACTION: Remove and rotate**

### OWASP Findings
| Risk | Status | Details |
|------|--------|---------|
| A01 Access Control | ✅/❌ | [details] |
| A02 Crypto | ✅/❌ | [details] |
| ... | ... | ... |

### Infrastructure
- Docker: [pass/fail/N/A]
- Kubernetes: [pass/fail/N/A]
- Terraform: [pass/fail/N/A]

### Recommended Actions
1. **Critical**: [action] — [deadline]
2. **High**: [action] — [deadline]
3. **Medium**: [action] — [schedule]
```

## Integration

- **Called by**: `/code-review` (security layer), `/pre-commit` (optional)
- **Roles**: `Agent(software-engineer)` (security focus), `Agent(devops-engineer)` (infra scan), `Agent(devops-architect)` (supply chain security, GHAS, SBOM/SLSA)
- **Skills**: `code-review` skill (security checklist)
