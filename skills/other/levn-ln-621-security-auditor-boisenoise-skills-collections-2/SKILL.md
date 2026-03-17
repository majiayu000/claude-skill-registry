---
name: ln-621-security-auditor
description: Security audit worker (L3). Scans codebase for hardcoded secrets, SQL injection, XSS, insecure dependencies, missing input validation. Returns findings with severity (Critical/High/Medium/Low), location, effort, and recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

# Security Auditor (L3 Worker)

Specialized worker auditing security vulnerabilities in codebase.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline** - invoked by ln-620-codebase-auditor
- Audit codebase for **security vulnerabilities** (Category 1: Critical Priority)
- Scan for hardcoded secrets, SQL injection, XSS, insecure dependencies, missing input validation
- Return structured findings to coordinator with severity, location, effort, recommendations
- Calculate compliance score (X/10) for Security category

## Inputs (from Coordinator)

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md#audit-coordinator--worker-contract` for contextStore structure.

Receives `contextStore` with: `tech_stack`, `best_practices`, `principles`, `codebase_root`.

## Workflow

1) **Parse Context:** Extract tech stack, best practices, codebase root from contextStore
2) **Scan Codebase:** Run security checks using Glob/Grep patterns (see Audit Rules below)
3) **Collect Findings:** Record each violation with severity, location (file:line), effort estimate (S/M/L), recommendation
4) **Calculate Score:** Count violations by severity, calculate compliance score (X/10)
5) **Return Results:** Return JSON with category, score, findings to coordinator

## Audit Rules (Priority: CRITICAL)

### 1. Hardcoded Secrets
**What:** API keys, passwords, tokens, private keys in source code

**Detection:**
- Search patterns: `API_KEY = "..."`, `password = "..."`, `token = "..."`, `SECRET = "..."`
- File extensions: `.ts`, `.js`, `.py`, `.go`, `.java`, `.cs`
- Exclude: `.env.example`, `README.md`, test files with mock data

**Severity:**
- **CRITICAL:** Production credentials (AWS keys, database passwords, API tokens)
- **HIGH:** Development/staging credentials
- **MEDIUM:** Test credentials in non-test files

**Recommendation:** Move to environment variables (.env), use secret management (Vault, AWS Secrets Manager)

**Effort:** S (replace hardcoded value with `process.env.VAR_NAME`)

### 2. SQL Injection Patterns
**What:** String concatenation in SQL queries instead of parameterized queries

**Detection:**
- Patterns: `query = "SELECT * FROM users WHERE id=" + userId`, `db.execute(f"SELECT * FROM {table}")`, `` `SELECT * FROM ${table}` ``
- Languages: JavaScript, Python, PHP, Java

**Severity:**
- **CRITICAL:** User input directly concatenated without sanitization
- **HIGH:** Variable concatenation in production code
- **MEDIUM:** Concatenation with internal variables only

**Recommendation:** Use parameterized queries (prepared statements), ORM query builders

**Effort:** M (refactor query to use placeholders)

### 3. XSS Vulnerabilities
**What:** Unsanitized user input rendered in HTML/templates

**Detection:**
- Patterns: `innerHTML = userInput`, `dangerouslySetInnerHTML={{__html: data}}`, `echo $userInput;`
- Template engines: Check for unescaped output (`{{ var | safe }}`, `<%- var %>`)

**Severity:**
- **CRITICAL:** User input directly inserted into DOM without sanitization
- **HIGH:** User input with partial sanitization (insufficient escaping)
- **MEDIUM:** Internal data with potential XSS if compromised

**Recommendation:** Use framework escaping (React auto-escapes, use `textContent`), sanitize with DOMPurify

**Effort:** S-M (replace `innerHTML` with `textContent` or sanitize)

### 4. Insecure Dependencies
**What:** Dependencies with known CVEs (Common Vulnerabilities and Exposures)

**Detection:**
- Run `npm audit` (Node.js), `pip-audit` (Python), `cargo audit` (Rust), `dotnet list package --vulnerable` (.NET)
- Check for outdated critical dependencies

**Severity:**
- **CRITICAL:** CVE with exploitable vulnerability in production dependencies
- **HIGH:** CVE in dev dependencies or lower severity production CVEs
- **MEDIUM:** Outdated packages without known CVEs but security risk

**Recommendation:** Update to patched versions, replace unmaintained packages

**Effort:** S-M (update package.json, test), L (if breaking changes)

### 5. Missing Input Validation
**What:** Missing validation at system boundaries (API endpoints, user forms, file uploads)

**Detection:**
- API routes without validation middleware
- Form handlers without input sanitization
- File uploads without type/size checks
- Missing CORS configuration

**Severity:**
- **CRITICAL:** File upload without validation, authentication bypass potential
- **HIGH:** Missing validation on sensitive endpoints (payment, auth, user data)
- **MEDIUM:** Missing validation on read-only or internal endpoints

**Recommendation:** Add validation middleware (Joi, Yup, express-validator), implement input sanitization

**Effort:** M (add validation schema and middleware)

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_output_schema.md` for JSON structure.

Return JSON with `category: "Security"` and checks: hardcoded_secrets, sql_injection, xss_vulnerabilities, insecure_dependencies, missing_input_validation.

## Critical Rules

- **Do not auto-fix:** Report violations only; coordinator creates task for user to fix
- **Tech stack aware:** Use contextStore to apply framework-specific patterns (e.g., React XSS vs PHP XSS)
- **False positive reduction:** Exclude test files, example configs, documentation
- **Effort realism:** S = <1 hour, M = 1-4 hours, L = >4 hours
- **Location precision:** Always include `file:line` for programmatic navigation

## Definition of Done

- contextStore parsed successfully
- All 5 security checks completed (secrets, SQL injection, XSS, deps, validation)
- Findings collected with severity, location, effort, recommendation
- Score calculated using penalty algorithm
- JSON result returned to coordinator

## Reference Files

- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`
- Security audit rules: [references/security_rules.md](references/security_rules.md)

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
