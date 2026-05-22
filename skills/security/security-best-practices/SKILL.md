---
name: security-best-practices
description: >-
  Analyze codebases for security vulnerabilities across Python, JavaScript,
  TypeScript, and Go. Operates in three modes: secure-by-default code
  generation, passive critical-vulnerability flagging during development, and
  full security audit with structured findings report. Covers authentication,
  injection prevention, XSS, CSRF, secrets management, file uploads, and
  framework-specific hardening for FastAPI, Django, Flask, Express, Next.js,
  React, Vue, and Go net/http. Trigger when the user requests a security
  review, security report, secure coding guidance, or vulnerability analysis.
  Do not trigger for general code review, debugging, or non-security tasks.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
  - WebSearch
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - analyzer
    - security
    - vulnerability
    - audit
    - owasp
  provenance:
    upstream_source: "security-best-practices"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T15:55:03+00:00"
    generator_version: "1.0.0"
    intent_confidence: 0.62
---

# Security Best Practices Analyzer

Analyze codebases for security vulnerabilities and generate structured findings reports covering authentication, injection, XSS, CSRF, secrets, and framework-specific hardening across Python, JavaScript/TypeScript, and Go.

## Overview

This skill operates in three modes depending on context:

**Mode 1 -- Secure generation (default):** When writing new code, apply every security rule from the reference checklist. Enforce parameterized queries, proper auth middleware, secure cookie flags, and secrets-from-environment patterns without being asked.

**Mode 2 -- Passive review (always on):** While editing or reading code for other tasks, flag critical vulnerabilities found in touched or nearby files. Focus on high-impact issues: hardcoded secrets, SQL injection, command injection, disabled auth, permissive CORS. Do not overwhelm the user with low-severity findings during unrelated work.

**Mode 3 -- Active audit (on request):** When the user asks for a security review or report, perform a systematic scan of the codebase and produce a structured findings report ordered by severity.

**What it analyzes:**
- Authentication and authorization enforcement
- Injection vectors (SQL, command, template, path traversal, deserialization)
- Cross-site scripting (XSS) and cross-site request forgery (CSRF)
- Secrets management and credential exposure
- File upload handling
- Security headers and TLS configuration
- Framework-specific misconfigurations

**What it produces:**
- Structured findings with severity, file path, line number, evidence, and remediation
- Executive summary with critical/high/medium/low counts
- Prioritized fix recommendations

## Analysis Checklist

### Authentication and Authorization

- [ ] Auth enforced via middleware or dependency injection, not per-handler opt-in
- [ ] Password hashing uses bcrypt, argon2, or scrypt with appropriate cost factor
- [ ] JWT validation checks signature, expiry, issuer, and audience
- [ ] Resource ownership verified on every state-changing request
- [ ] Session tokens regenerated after privilege changes
- [ ] Rate limiting applied to authentication endpoints

### Injection Prevention

- [ ] SQL uses parameterized queries or ORM exclusively (no string concatenation)
- [ ] No use of `eval()`, `exec()`, `os.system()`, `child_process.exec()` with user input
- [ ] Template rendering uses auto-escaping (no user input as template source)
- [ ] File paths validated and canonicalized (reject `..` sequences)
- [ ] No deserialization of untrusted data (`pickle.load`, `yaml.load` without SafeLoader)

### XSS Prevention

- [ ] Framework auto-escaping enabled (React JSX, Vue templates, Jinja2 `|e`)
- [ ] No use of `dangerouslySetInnerHTML`, `v-html`, or `innerHTML` with user data
- [ ] Rich content sanitized through DOMPurify or bleach
- [ ] Content-Security-Policy header configured

### CSRF Protection

- [ ] Token-based CSRF protection when cookies carry authentication
- [ ] Django: `{% csrf_token %}` and middleware enabled
- [ ] Express: `csurf` or `csrf-csrf` middleware configured
- [ ] Next.js: Origin header verification on server actions

### Secrets Management

- [ ] All secrets loaded from environment variables or secret managers
- [ ] No hardcoded credentials in source, config files, or Docker images
- [ ] `.gitignore` excludes `.env`, key files, and credential stores
- [ ] No secrets in log output or error messages

### File Upload Security

- [ ] MIME type and magic bytes validated (not just file extension)
- [ ] Files stored outside web root with generated random filenames
- [ ] Size limits enforced server-side
- [ ] Upload directory not executable

### Framework Hardening

- [ ] FastAPI: `docs_url=None` and `redoc_url=None` in production
- [ ] Django: `DEBUG=False`, `ALLOWED_HOSTS` set, `SECRET_KEY` from environment
- [ ] Flask: `app.secret_key` from environment, `debug=False` in production
- [ ] Express: `helmet()` middleware for security headers
- [ ] Next.js: Server Actions validate input server-side
- [ ] Go: Server and client timeouts set, `crypto/rand` used (not `math/rand`)

## Metrics

### Severity Classification

| Severity | Description | Response Time |
|----------|-------------|---------------|
| CRITICAL | Exploitable with no authentication, data breach risk | Immediate fix |
| HIGH | Exploitable with low complexity, significant impact | Fix within sprint |
| MEDIUM | Requires specific conditions, moderate impact | Plan within quarter |
| LOW | Minimal impact, defense-in-depth improvement | Track in backlog |

### Vulnerability Categories

| Category | Scan Target | Detection Method |
|----------|-------------|------------------|
| Injection | SQL, command, template, path | Pattern search for unsafe APIs |
| Auth bypass | Missing middleware, weak tokens | Route analysis, config review |
| XSS | Unescaped output, raw HTML insertion | Grep for dangerous sinks |
| Secrets exposure | Hardcoded keys, logged tokens | Pattern search, entropy analysis |
| Misconfiguration | Debug mode, permissive CORS | Config file review |

## Scanning Heuristics

Search for these patterns to detect vulnerabilities:

```bash
# Command injection
grep -rn 'eval(' --include='*.py' --include='*.js' --include='*.ts'
grep -rn 'os\.system(' --include='*.py'
grep -rn 'subprocess.*shell=True' --include='*.py'
grep -rn 'child_process\.exec(' --include='*.js' --include='*.ts'

# SQL injection
grep -rn 'execute.*format\|execute.*f"' --include='*.py'
grep -rn 'fmt\.Sprintf.*SELECT' --include='*.go'

# XSS sinks
grep -rn 'dangerouslySetInnerHTML' --include='*.jsx' --include='*.tsx'
grep -rn 'v-html' --include='*.vue'
grep -rn 'innerHTML' --include='*.js' --include='*.ts'

# Unsafe deserialization
grep -rn 'pickle\.load' --include='*.py'
grep -rn 'yaml\.load(' --include='*.py'

# Secrets and misconfigurations
grep -rn 'DEBUG\s*=\s*True' --include='*.py'
```

## Report Format

### Finding Structure

```
[SEC-NNN] Severity: CRITICAL|HIGH|MEDIUM|LOW
Category: Injection|Auth|XSS|CSRF|Secrets|Config|Upload
File: path/to/file.py:42
Finding: One-sentence vulnerability description
Evidence: `code_snippet()`
Impact: What an attacker could achieve
Fix: Remediation steps
```

### Full Report Structure

```markdown
# Security Best Practices Report

**Repository:** /path/to/repo
**Date:** 2026-02-04
**Scope:** Python (FastAPI), JavaScript (React)

## Executive Summary

- Critical: 2 findings
- High: 3 findings
- Medium: 5 findings
- Low: 4 findings

## Critical Findings

[SEC-001] ...

## High Findings

[SEC-002] ...

## Recommendations

1. Fix SQL injection in auth handler (SEC-001)
2. Remove hardcoded API key (SEC-003)
```

## Workflow

### Step 1: Detect languages and frameworks

Inspect the repository for `package.json` (Node.js), `requirements.txt` or `pyproject.toml` (Python), `go.mod` (Go), and framework indicators in imports and configs.

### Step 2: Load security reference

Read `references/cross-language-security.md` and apply rules relevant to the detected stack.

### Step 3: Choose operating mode

- Writing new code: Mode 1 (secure generation), apply rules silently
- Editing existing code: Mode 2 (passive review), flag critical issues only
- User requests review: Mode 3 (active audit), full structured report

### Step 4: Scan for vulnerabilities (Mode 3)

Run scanning heuristics using Grep and Bash. Organize findings by severity with file paths and line numbers.

### Step 5: Generate report (Mode 3)

Write to `security_best_practices_report.md` or user-specified location. Structure by severity. Summarize to user and offer to begin fixes.

### Step 6: Apply fixes

Fix one finding at a time. Write comments explaining security rationale. Verify fixes do not break functionality. Follow project commit and testing conventions.

## Overrides and Exceptions

Projects may bypass specific rules for legitimate reasons. When documented in project config or CLAUDE.md, respect the override. When undocumented, inform the user once and suggest adding documentation.

## Safety Constraints

- MUST NOT output, log, or commit secrets (API keys, passwords, tokens, signing keys)
- MUST NOT weaken protections as a "fix" (disabling auth, permissive CORS, skipping validation)
- MUST provide evidence for every finding (file path, line number, code snippet)
- MUST treat uncertainty honestly: note "verify at runtime" when infrastructure protections may exist
- CORS is not an authentication mechanism; CSRF applies only when browsers auto-attach cookies

## TLS and HSTS Guidance

Do not flag missing TLS in development contexts. Do not set `Secure` cookie flags unless the application runs over HTTPS. Do not recommend HSTS without discussing long-term implications. Provide environment-based toggles for production-only security headers.

## Examples

### Example 1: Full security audit

```
User: Run a security review on this Python FastAPI project.
Assistant: I'll analyze the codebase for security vulnerabilities.

Detected: Python 3.11, FastAPI 0.104, SQLAlchemy 2.0, React 18

Scanning authentication, injection, XSS, CSRF, secrets...

Security Best Practices Report
==============================
Critical: 1 | High: 2 | Medium: 3 | Low: 2

[SEC-001] CRITICAL - SQL Injection
File: app/db/queries.py:87
Finding: Raw string interpolation in SQL query
Evidence: `cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")`
Fix: Use parameterized query: `cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))`

[SEC-002] HIGH - Hardcoded Secret
File: app/config.py:12
Finding: JWT secret hardcoded in source
Evidence: `JWT_SECRET = "my-secret-key-123"`
Fix: Load from environment: `JWT_SECRET = os.environ["JWT_SECRET"]`

Full report written to security_best_practices_report.md.
Want me to start fixing these findings?
```

### Example 2: Passive detection during development

```
User: Add a new endpoint to fetch user profile by ID.
Assistant: I'll add the endpoint. While working on this file, I noticed
a critical issue in a nearby function:

[SEC-003] CRITICAL - Command Injection
File: app/utils/export.py:23
Finding: os.system() called with user-controlled input
Evidence: `os.system(f"pdf-convert {filename}")`
Fix: Use subprocess.run(["pdf-convert", filename], shell=False)

Want me to fix this while I'm here?

[Proceeds to add the requested endpoint with parameterized queries
and proper auth middleware applied by default]
```

## Interpretation Guide

| Finding Count | Risk Assessment | Recommended Action |
|---------------|-----------------|-------------------|
| 0 critical, 0 high | Low risk | Maintain current practices |
| 0 critical, 1-3 high | Moderate risk | Schedule fixes within sprint |
| 1+ critical | High risk | Stop feature work, fix immediately |
| 5+ high | Elevated risk | Dedicated security sprint needed |
