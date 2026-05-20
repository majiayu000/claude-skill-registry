---
name: security-review
description: Use when asked for a security audit/review or vulnerability hunt (injection, XSS, authn/authz, crypto, SSRF, secrets) and report only high-confidence exploitable findings.
allowed-tools: Read, Grep, Glob, Bash, Task
license: LICENSE
---

<!--
Reference material based on OWASP Cheat Sheet Series (CC BY-SA 4.0)
https://cheatsheetseries.owasp.org/
-->

# Security Review Skill

Goal: find exploitable vulnerabilities. Report only findings with **high confidence**.

## Scope: Research vs Reporting (Mandatory)

- **Report scope**: only user-requested files/diff/component.
- **Research scope**: whole codebase as needed to confirm exploitability.

Before reporting, verify:
- true input source (attacker-controlled vs server-controlled)
- upstream validation/sanitization
- framework default protections
- relevant config/middleware/infra behavior

Pattern matching alone is insufficient.

## Confidence Policy

| Level | Criteria | Action |
|---|---|---|
| High | vulnerable sink + attacker-controlled path confirmed | Report |
| Medium | suspicious pattern, source/control unclear | Mark "Needs verification" |
| Low | theoretical or defense-in-depth only | Do not report |

## Do Not Flag

- tests (unless security of tests requested)
- dead/commented code
- constants and server-controlled configuration values
- paths requiring prior auth without bypass risk (state auth requirement)

### Server-controlled examples (usually safe)

| Source | Example |
|---|---|
| framework settings | `settings.API_URL` |
| env vars | `os.environ.get(...)` |
| server config files | `config.yaml` |
| hardcoded constants | `BASE_URL = ...` |

SSRF contrast:

```python
# Vulnerable: attacker-controlled URL
requests.get(request.GET.get('url'))

# Usually safe: server-controlled URL
requests.get(f"{settings.SEER_AUTOFIX_URL}{path}")
```

## Framework-Mitigation Awareness

Do not flag auto-escaped/parameterized-safe patterns unless mitigations are bypassed.

| Pattern | Usually safe because |
|---|---|
| Django `{{ x }}` | auto-escaped |
| React `{x}` | escaped by default |
| Vue `{{ x }}` | escaped by default |
| ORM filters | parameterized queries |
| parameterized SQL APIs | bound parameters |

Flag only when bypass exists:
- Django: `|safe`, `autoescape off`, `mark_safe(user_input)`
- React: `dangerouslySetInnerHTML` with user input
- Vue: `v-html` with user input
- ORM raw SQL interpolation

## Review Process

### 1) Detect code context

| Context | Load refs |
|---|---|
| API/routes | `authorization.md`, `authentication.md`, `injection.md` |
| Frontend/templates | `xss.md`, `csrf.md` |
| Files/uploads | `file-security.md` |
| Crypto/secrets | `cryptography.md`, `data-protection.md` |
| Serialization | `deserialization.md` |
| Outbound requests | `ssrf.md` |
| Business flows | `business-logic.md` |
| API design | `api-security.md` |
| Config/CORS/headers | `misconfiguration.md` |
| CI/deps | `supply-chain.md` |
| Errors/logging | `error-handling.md`, `logging.md` |

### 2) Load language guide

| Indicators | Guide |
|---|---|
| `.py`, Django/Flask/FastAPI | `languages/python.md` |
| `.js/.ts`, Express/React/Vue/Next | `languages/javascript.md` |
| `.go` | `languages/go.md` |
| `.rs` | `languages/rust.md` |
| Java/Spring | `languages/java.md` |

### 3) Load infra guide if needed

| Artifact | Guide |
|---|---|
| Docker | `infrastructure/docker.md` |
| Kubernetes/Helm | `infrastructure/kubernetes.md` |
| Terraform | `infrastructure/terraform.md` |
| CI workflow | `infrastructure/ci-cd.md` |
| Cloud/IAM | `infrastructure/cloud.md` |

### 4) Validate exploitability before reporting

For each candidate:
1. Trace data flow to input origin
2. Confirm attacker control
3. Check mitigations and allowlists
4. Confirm reachable attack path

### 5) Report high-confidence findings only

Skip speculative findings.

## Severity Guide

| Severity | Typical impact |
|---|---|
| Critical | direct severe exploit, often no-auth (RCE/auth bypass/secrets exposure) |
| High | significant exploit with conditions (stored XSS, SSRF to metadata, sensitive IDOR) |
| Medium | constrained exploitability (reflected XSS, CSRF state change, path traversal) |
| Low | defense-in-depth gaps |

## Pattern Reference

### Always flag (critical)

```text
eval(user_input)
exec(user_input)
pickle.loads(user_data)
yaml.load(user_data)   # unsafe loader
unserialize(user_data)
deserialize(user_data)
shell=True + user_input
child_process.exec(user)
```

### Always flag (high)

```text
innerHTML = userInput
dangerouslySetInnerHTML={user}
v-html="userInput"
string-interpolated SQL with user input
os.system(f"cmd {user_input}")
```

### Always flag (secrets)

```text
hardcoded passwords/api keys/private keys/cloud secrets
```

### Must investigate context first

```text
requests.get(user_url)          # SSRF candidate
open(user_path)                 # path traversal candidate
redirect(user_next)             # open redirect candidate
md5/random for security purpose # weak crypto/randomness candidate
```

Use-case matters (e.g., `md5` for checksums may be acceptable).

## Output Format

```markdown
## Security Review: [File/Component]

### Summary
- Findings: X (Critical Y, High Z, ...)
- Risk Level: Critical/High/Medium/Low
- Confidence: High/Mixed

### Findings
#### [VULN-001] [Type] (Severity)
- Location: `file.py:123`
- Confidence: High
- Issue: ...
- Impact: ...
- Evidence:
  ```python
  ...
  ```
- Fix: ...

### Needs Verification
#### [VERIFY-001] [Potential issue]
- Location: `file.py:456`
- Question: ...
```

If none: `No high-confidence vulnerabilities identified.`

## Reference Index

### Core (`references/`)
- `injection.md`, `xss.md`, `authorization.md`, `authentication.md`, `cryptography.md`
- `deserialization.md`, `file-security.md`, `ssrf.md`, `csrf.md`, `data-protection.md`
- `api-security.md`, `business-logic.md`, `modern-threats.md`, `misconfiguration.md`
- `error-handling.md`, `supply-chain.md`, `logging.md`

### Language (`languages/`)
- `python.md`, `javascript.md`, `go.md`, `rust.md`, `java.md`

### Infrastructure (`infrastructure/`)
- `docker.md`, `kubernetes.md`, `terraform.md`, `ci-cd.md`, `cloud.md`
