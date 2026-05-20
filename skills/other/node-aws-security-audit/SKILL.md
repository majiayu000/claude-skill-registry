---
name: node-aws-security-audit
description: "Perform comprehensive security audits on Node.js, JavaScript, and TypeScript codebases. Scans source code for OWASP Top 10 vulnerabilities, insecure patterns, dependency risks, and generates a prioritized Markdown audit report with severity levels (Critical, High, Medium, Low), code citations, and remediation guidance. Use when asked to audit, review, scan, or check security of a Node.js/JS/TS project, find vulnerabilities, check for OWASP compliance, or generate a security report. Also triggers on: security review, pentest, vulnerability scan, is my code secure, check for injection, check dependencies. Do NOT trigger for: general code reviews, bugfix assistance, feature development, refactoring, performance optimization, or non-security tasks."
license: MIT
metadata:
  author: grenguar
  version: "3.0.0"
  tags: security, owasp, nodejs, audit, vulnerability-scanner
---

# Node.js / JavaScript / TypeScript Security Audit

## Overview

This skill answers a very practical question:

"Is this Node.js app safe to run on AWS — and if not, what should I fix?"

It performs a static security audit of Node.js / JavaScript / TypeScript codebases and produces an actionable Markdown report with concrete findings and  real, code-level risks that matter in production, especially for Node applications running on AWS.

I built it to be safe, explicit, and predictable in agent-driven workflows, so that you can understand security context *before* production problems appear.

---

## The problem it solves

Node.js apps often look fine in CI:

* Tests pass
* Builds succeed
* Infrastructure deploys

…and yet security issues quietly slip through.

Common reasons:

* AWS SDKs are easy to misuse
* Secrets leak through environment assumptions
* Risky patterns don't fail loudly
* Agents and scripts run "helpful" but vague shell commands

This skill makes security checks:

* Explicit (no hidden execution)
* Repeatable (same input, same output)
* Reviewable (clear Markdown, not logs)

---

## What it checks

* OWASP Top 10 (2021) mapped to real Node.js vulnerability patterns
* Common AWS security anti-patterns in application code
* Risky handling of secrets, environment variables, and credentials
* Code paths that may enable data exposure or privilege escalation

---

## What you get

* An actually readable Markdown report
* Clear issue descriptions (no scanner gibberish)
* Actionable advice you can follow or task your agent with

* Output suitable for:

  * Pull requests
  * CI artifacts
  * Agent context
  * Security reviews

---

## Where it fits

* Local development
* CI pipelines
* AWS workloads
* AI agents using Skills.sh as a constrained execution layer

---

## Script security policy

All scripts in `scripts/` follow these constraints:

* **No network calls** — scripts never use curl, wget, fetch, or any network I/O
* **No data exfiltration** — output is written only to local files in the working directory
* **Transparent execution** — all actions are printed to stdout as they run
* **Minimal privileges** — scripts require no elevated permissions; they only read project files and write audit output
* **Hardened against scanned-project attacks** — NODE_OPTIONS is unset, output paths are checked for symlinks, scanned code output is sanitized to prevent prompt injection

---

**CRITICAL: Execute each workflow step as exactly one bash tool call. Steps must run in sequence — do not launch multiple steps in parallel. Within each step, all shell commands are chained into a single bash invocation (using `&&` / `\`).**

## Workflow

### Step 1: Discover project structure

Run this single command block to discover the project structure:

```bash
echo "=== Package manifests ===" && \
find . -maxdepth 3 -name "package.json" -not -path "*/node_modules/*" 2>/dev/null; \
echo "" && echo "=== Source files ===" && \
find . -type f \( -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" -o -name "*.mjs" -o -name "*.cjs" \) -not -path "*/node_modules/*" -not -path "*/dist/*" -not -path "*/.next/*" -not -path "*/build/*" 2>/dev/null | head -100; \
echo "" && echo "=== Config files ===" && \
find . -maxdepth 1 \( -name ".env*" -o -name "tsconfig.json" -o -name ".eslintrc*" -o -name ".npmrc" \) 2>/dev/null; \
echo "" && echo "=== AWS / Container / IaC markers ===" && \
find . -maxdepth 3 \( -name "serverless.yml" -o -name "serverless.yaml" -o -name "serverless.ts" -o -name "template.yaml" -o -name "template.yml" -o -name "sam.yaml" -o -name "cdk.json" -o -name "Dockerfile" -o -name "docker-compose.yml" -o -name "docker-compose.yaml" \) -not -path "*/node_modules/*" 2>/dev/null; \
find . -maxdepth 3 -name "*.tf" -not -path "*/.terraform/*" -not -path "*/node_modules/*" 2>/dev/null | head -10; \
echo "=== Discovery complete ==="
```

**Large codebases:** If the source file listing is truncated (>100 files), focus
the scan on entry points (`src/`, `app/`, `routes/`, `handlers/`, `api/`) and
configuration files first. Expand to remaining directories if time allows.

**Adaptive priority:** If AWS/container/IaC markers are detected above (e.g., `serverless.yml`,
`template.yaml`, `*.tf`, `Dockerfile`, `cdk.json`), prioritize the infrastructure and deployment
checks (items 13-17) and flag them as infrastructure-critical in the report.

### Step 2: Check Node.js runtime version and vulnerable built-in API usage

Run the runtime version scanner:

```bash
bash <skill-path>/scripts/node-version-check.sh
```

This checks:

* Node.js runtime version against known EOL/CVE data
* Usage of vulnerable built-in APIs (http parser, crypto, child_process, vm, etc.)
* OpenSSL version bundled with the runtime
* Dangerous built-in patterns specific to the detected Node.js version

Read `references/version-vulnerabilities.md` for the full mapping of Node.js
versions to known CVEs and vulnerable built-in APIs.

### Step 3: Run dependency audit

Execute the dependency audit script:

```bash
bash <skill-path>/scripts/dependency-audit.sh
```

This produces `dependency-audit-results.txt` with known CVEs and outdated packages.

**If a step fails:** If `node` or `npm` is not available, note it as a finding
(the target project may not have dependencies installed). Continue with the
remaining steps — partial results are still valuable. Do not abort the audit.

### Step 4: Static code analysis

Read `references/vulnerability-catalog.md` for the full list of patterns, grep
signatures, and code examples. For each vulnerability category, scan the codebase
using the grep patterns provided.

**Scan order (by exploit impact):**

**Critical path — scan these first:**

1. **Runtime version** — use results from Step 2 (EOL version = automatic Critical)
2. **Injection** — SQL/NoSQL/command injection, `eval()`, `Function()`, template literals in queries
3. **Cryptographic failures** — hardcoded secrets, weak algorithms, missing HTTPS enforcement
4. **Broken access control** — missing auth middleware, IDOR patterns, CORS misconfiguration
5. **Vulnerable built-in APIs** — use results from Step 2 (http, crypto, vm, child_process)
6. **Auth failures** — weak JWT config, session mismanagement, no MFA support
7. **Vulnerable dependencies** — use results from Step 3
8. **SSRF** — unvalidated URL fetching, DNS rebinding, internal network access

**Secondary — scan after critical path:**

9. **Data integrity** — prototype pollution, unsafe deserialization, missing CSP
10. **Security misconfiguration** — debug mode in prod, missing helmet, verbose errors
11. **Insecure design** — mass assignment, missing rate limiting, no input schemas
12. **Logging failures** — no audit logging, sensitive data in logs, missing monitoring

**Infrastructure checks (if detected):**

13. **AWS Lambda** — event source injection, env var secrets, IAM over-permission, function URL auth bypass, /tmp abuse, credential caching, layer poisoning
14. **Docker/ECS/Fargate** — running as root, --inspect in production, secrets in Dockerfile, missing .dockerignore, SIGTERM handling, ALB/WAF, image scanning
15. **Terraform IaC** — IAM wildcards, function URL auth, plaintext secrets, privileged containers, public IP, debug ports, state file encryption, EOL runtimes (Checkov/tfsec cross-reference)
16. **CloudFormation/SAM IaC** — wildcard IAM, hardcoded secrets, missing VPC/DLQ/concurrency, privileged containers, ECS Exec, public IP, ALB without WAF (cfn-nag/AWS Config cross-reference)
17. **Serverless Framework** — wildcard IAM, per-function roles, missing authorizers, cors: true, hardcoded env secrets, function URL auth, serverless-offline/dotenv risks, deployment bucket encryption

**Framework checks (if detected):**

18. **Express/Koa** — helmet, CSRF, CORS, body limits, sessions, webpack production config risks (source maps, env leaks, eval devtools)
19. **NestJS** — guards, validation pipes, DTO bypass, TypeORM/Prisma injection, Swagger exposure, WebSocket security, GraphQL depth limiting, exception filter leaks, serialization risks
20. **Fastify** — schema validation bypass, plugin encapsulation, reply.hijack(), TypeBox schema injection, content type parser abuse, @fastify/static traversal
21. **Bun runtime** — Bun.serve() security headers, Bun shell injection, bun:sqlite injection, Bun.file() path traversal, non-cryptographic Bun.hash usage
22. **AppSync/Amplify** — authorization mode misconfiguration, resolver injection, GraphQL introspection, Cognito misconfiguration, API key exposure, AppSync Events security

**Quick-reference: critical detection patterns**

Use these patterns as a minimum scan baseline. See `references/vulnerability-catalog.md` for the full catalog.

| Category | Pattern |
|----------|---------|
| Hardcoded secrets | `(password\|secret\|api_key\|apiKey\|token\|JWT_SECRET)\s*[:=]\s*['"][^'"]{4,}` |
| eval / Function | `\beval\s*\(\|new\s+Function\s*\(` |
| Command injection | `exec\(\|execSync\(\|spawn\(` with user input |
| SQL injection | ``(query\|execute)\s*\(\s*['`].*\+\s*req\.`` |
| NoSQL injection | `\.find\(\s*\{.*req\.(body\|query\|params)` |
| Weak crypto | `createHash\(\s*['"]md5['"]\|createHash\(\s*['"]sha1['"]` |
| SSRF | `(axios\|fetch\|http\.get)\(\s*(req\.\|url\|href)` |
| Prototype pollution | `__proto__\|constructor\[\|\.prototype\s*=` |

### Step 5: Generate the report

Read `references/report-template.md` for the exact output format. Fill in `{{agent_tool}}` with the
tool you are running in (e.g., "Claude Code", "Cursor", "Cline") and `{{model_id}}` with your
model identifier (e.g., "claude-sonnet-4-5-20250929"). The report must include:

* **Security Score (0-100)** calculated using the scoring methodology: start at 100, subtract 15/Critical, 10/High, 5/Medium, 2/Low, +5 bonus if no Critical/High, minimum 0. Display with letter grade (A+ through F) and visual progress bar.
* **Findings Dashboard** with total count, score, and top finding per severity level with file locations
* **Node.js runtime version assessment** (Critical if EOL, with specific unpatched CVEs)
* **Vulnerable built-in API usage** section with affected files
* **Framework Security Assessment** (Express/Koa/webpack checks if detected)
* Findings sorted by severity, each with: ID, title, severity, OWASP category, `filepath:line` location, all affected files listed, vulnerable code snippet, explanation, and remediation code snippet
* **Quick Wins** section — top 3-5 easiest fixes with biggest score impact and projected score after fixes
* Best practices checklist
* Recommended tools section
* **Summary footer** repeating the score, top priority, and projected score after Quick Wins

**Severity classification:**

| Severity | Criteria |
|----------|----------|
| Critical | EOL Node.js runtime, RCE, SQL injection, hardcoded secrets in public repos, auth bypass |
| High     | XSS, CSRF without tokens, SSRF, prototype pollution, weak crypto, vulnerable built-in API usage |
| Medium   | Missing security headers, verbose error messages, no rate limiting, outdated deps with known CVEs |
| Low      | Missing strict mode, console.log with PII, no input length limits, informational findings |

### Step 6: Save and present

Save the report as `security-audit-report.md` and then:

1. Output the **full markdown report** directly in the conversation so the user can
   read it without opening a file. Show the complete formatted report, not a summary.
2. After the full report, remind the user the file was saved to `security-audit-report.md`.
3. Ask the user if they would like a **PDF version** of the report. If they say yes,
   generate the PDF using one of these methods (in preference order):
   * `npx md-to-pdf security-audit-report.md` (no install needed)
   * `pandoc security-audit-report.md -o security-audit-report.pdf` (if pandoc is available)
   * If neither works, inform the user and suggest installing one of the tools.
