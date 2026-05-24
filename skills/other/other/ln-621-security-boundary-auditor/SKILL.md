---
name: ln-621-security-boundary-auditor
description: "Checks application security boundaries: secrets, injection, XSS, input validation, and sensitive env defaults. Use when auditing exploitable code paths."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__trace_dataflow, mcp__hex-line__read_file, mcp__hex-line__grep_search, mcp__hex-line__outline
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Security Boundary Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing exploitable application security boundaries.

## Purpose & Scope

- Audit codebase for **security boundary vulnerabilities** (Category 1: Critical Priority)
- Scan for hardcoded secrets, SQL injection, XSS, missing input validation, and sensitive env defaults
- Emit `HARDEN_SECURITY_BOUNDARY`, `REMOVE_SECRET`, or `REMOVE_SENSITIVE_DEFAULT`
- Return structured findings with severity, location, effort, actions, and recommendations
- Calculate compliance score (X/10) for Security category

## Inputs

**MANDATORY READ:** Load `references/audit_worker_core_contract.md`.
Tool policy: follow host AGENTS.md MCP preferences; load `references/mcp_tool_preferences.md` and `references/mcp_integration_patterns.md` only when host policy is absent or MCP behavior is unclear.

Receives `contextStore` with: `tech_stack`, `best_practices`, `principles`, `codebase_root`, `output_dir`.

Use `hex-graph` first when dataflow or cross-file reference analysis materially improves confidence. Use `hex-line` first for local code reads when available. If MCP is unavailable, unsupported, or not indexed, continue with built-in `Read/Grep/Glob/Bash` and state the fallback in the report.

## Workflow

Detection policy: use two-layer detection (candidate scan, then context verification); load `references/two_layer_detection.md` only when the verification method is ambiguous.

1) **Parse Context:** Extract tech stack, best practices, codebase root, output_dir from contextStore
2) **Scan Codebase (Layer 1):** Run security checks using Glob/Grep patterns (see Audit Rules below)
3) **Analyze Context (Layer 2):** For each candidate, read surrounding code to classify:
   - Secrets: test fixture / example / template -> FP. Production code -> confirmed
   - SQL injection: ORM parameterization nearby -> FP. Raw string concat with user input -> confirmed
   - XSS: framework auto-escapes (React JSX, Go templates) -> FP. Unsafe context (`innerHTML`, `| safe`) -> confirmed
   - Sensitive defaults: placeholder/example -> skip. Real fallback for secret/token/key -> confirmed
   - Validation: internal service-to-service endpoint -> downgrade. Public API -> confirmed
4) **Collect Findings:** Record confirmed violations with severity, location (file:line), effort estimate (S/M/L), recommendation
5) **Calculate Score:** Count violations by severity, calculate compliance score (X/10)
6) **Write Report:** Build full markdown report in memory per `references/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-621--global.md` in single Write call
7) **Return Summary:** Return minimal summary (see Output Format)

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

### 4. Sensitive Env Defaults
**What:** Secret, token, key, credential, or privileged config values with unsafe code defaults

**Detection:**
- Grep env reads with defaults for sensitive names: `SECRET`, `TOKEN`, `KEY`, `PASSWORD`, `PRIVATE`, `CREDENTIAL`
- Check config/settings classes for hardcoded sensitive fallback values
- Exclude `.env.example`, tests, docs, and obvious placeholders (`changeme`, empty string, `example`)

**Severity:**
- **CRITICAL:** production credential fallback or default signing/encryption secret
- **HIGH:** sensitive default in runtime config reachable in deployed app
- **MEDIUM:** dev/staging sensitive default outside test-only files

**Recommendation:** Remove sensitive default, require explicit config, fail fast at startup

**Effort:** S-M

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

**MANDATORY READ:** Load `references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `references/templates/audit_worker_report_template.md`.

Write JSON summary per `references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-621--global.md` with `category: "Security Boundary"` and checks: hardcoded_secrets, sql_injection, xss_vulnerabilities, sensitive_env_defaults, missing_input_validation.

Return summary per `references/audit_summary_contract.md`.

Standalone mode still writes the same JSON summary to a worker-owned run-scoped artifact path per shared contract.

## Critical Rules

Apply the already-loaded `references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report violations only
- **Tech stack aware:** Use contextStore to apply framework-specific patterns (e.g., React XSS vs PHP XSS)
- **False positive reduction:** Exclude test files, example configs, documentation
- **Effort realism:** S = <1 hour, M = 1-4 hours, L = >4 hours
- **Location precision:** Always include `file:line` for programmatic navigation
- **Unique angle:** Audit exploitable application security boundaries only. Do not audit package health or env synchronization.
- **Action required:** Every finding uses `HARDEN_SECURITY_BOUNDARY`, `REMOVE_SECRET`, or `REMOVE_SENSITIVE_DEFAULT`.

## Definition of Done

Apply the already-loaded `references/audit_worker_core_contract.md`.

- [ ] contextStore parsed successfully (including output_dir)
- [ ] All 5 security checks completed (secrets, SQL injection, XSS, sensitive env defaults, validation)
- [ ] Findings collected with severity, location, effort, recommendation
- [ ] Score calculated using penalty algorithm
- [ ] Report written to `{output_dir}/ln-621--global.md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- **Audit output schema:** `references/audit_output_schema.md`
- Security audit rules: [references/security_rules.md](references/security_rules.md)

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
