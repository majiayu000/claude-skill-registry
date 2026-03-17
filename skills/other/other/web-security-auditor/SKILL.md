---
name: web-security-auditor
description: Aggregate SAST, SCA, DAST, secrets, API, frontend, and backend security checks into one report.
compatibility: codex, claude-code, claude-ai, agent-skills
license: Apache-2.0
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
  - web_search
metadata:
  category: web-builder
  stage: 9-security
  pipeline: web-builder
---

# Web Security Auditor

## Objective

Perform a comprehensive web application security review aligned to OWASP Top 10
and practical production hardening controls.

## Required Workflow

### A. Static Analysis (SAST)

- Run Semgrep for injection, secrets, crypto misuse, and prototype pollution.
- Run ESLint security plugins (`eslint-plugin-security`, `eslint-plugin-no-unsanitized`).
- Run Bandit for Python codebases.

### B. Dependency Scanning (SCA)

- Run `npm audit`, `pip-audit`, or `cargo audit` by stack.
- Include Aikido Security or Snyk where available.
- Include Vulert for no-install open-source dependency checks.

### C. Dynamic Analysis (DAST)

- Run OWASP ZAP automation/headless scans.
- Optionally run StackHawk.
- Optionally run Nuclei templates for quick vulnerability sweeps.

### D. Secret Detection

- Run Gitleaks across repository and history.
- Run TruffleHog scan.

### E. Frontend Security Checks

- Verify CSP (no unsafe inline/eval in production policy).
- Verify clickjacking protection (`X-Frame-Options` or `frame-ancestors`).
- Verify HSTS.
- Verify `X-Content-Type-Options: nosniff`.
- Verify no sensitive data in `localStorage` and no exposed production source maps.
- Check for XSS hazards (`dangerouslySetInnerHTML`, `innerHTML`, `eval`).

### F. Backend Security Checks

- Verify parameterized DB access / ORM usage.
- Verify strong JWT secret management and token expiry.
- Verify rate limiting on auth/sensitive routes.
- Verify strict CORS origins.
- Verify input validation on all endpoints.
- Verify secure password hashing (bcrypt/argon2).
- Check IDOR controls on user-owned resources.

### G. API Security

- Include Akto or Escape.tech checks for business-logic and GraphQL/REST API risks.

## Output

- `security-report.json` with findings grouped by `Critical`, `High`, `Medium`, `Low`

## Execution

```bash
python skills/web-security-auditor/scripts/security_auditor.py --input <workspace> --output <out.json> --format json
```

## References

- `references/tools.md`
