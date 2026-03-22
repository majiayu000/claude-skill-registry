---
name: vcp-audit
description: >
  Run a comprehensive audit against all applicable VCP standards.
  Supports full audit, compliance-specific audit, and quick release readiness check.
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, WebFetch, Task, TeamCreate, TaskCreate, TaskUpdate, TaskList, SendMessage, TeamDelete
argument-hint: "[path] | compliance [gdpr|pci-dss|hipaa] | quick"
---

# VCP Audit

Comprehensive codebase audit against VCP standards. Uses team mode to parallelize scanning, then validates findings to eliminate false positives before reporting.

## Modes

- `/vcp-audit` or `/vcp-audit [path]` — **Full audit** against all applicable standards
- `/vcp-audit compliance [gdpr|pci-dss|hipaa]` — **Compliance audit** with regulation citations
- `/vcp-audit quick` — **Release readiness** check (critical + high rules, no team mode, READY/NOT READY verdict)

## Step 1: Resolve Config

1. Read `.vcp/config.json` from the project root. Extract the `pluginRoot` field.
2. **If `.vcp/config.json` does not exist or `pluginRoot` is missing:** Stop and tell the user: "No VCP configuration found. Run `/vcp-init` to configure VCP for this project."
3. **Validate `pluginRoot`:** The path must be absolute, contain `/.claude/` (or `\.claude\` on Windows) as a path segment, and contain only safe path characters (letters, digits, `/`, `\`, `-`, `_`, `.`, `:`, and spaces). Reject any path with shell metacharacters (`;`, `&`, `|`, `$`, `` ` ``, `(`, `)`, `{`, `}`, `<`, `>`, `!`, `~`, `#`, `*`, `?`, `[`, `]`, `'`, `"`). If validation fails, stop and tell the user: "Invalid pluginRoot — must be within ~/.claude/ and contain no shell metacharacters. Run `/vcp-init` to fix." Also verify the file `<pluginRoot>/lib/vcp-context-core.ts` exists using Glob. If it does not exist, stop and tell the user: "pluginRoot points to an invalid VCP installation. Run `/vcp-init` to fix."
4. Run the config resolution script via Bash:
   ```bash
   bun "<pluginRoot>/lib/resolve-config.ts" "<project-root>"
   ```
5. Parse the JSON output. It contains: `applicableStandards`, `ignoredRules`, `severity`, `exclude`.

## Step 2: Fetch Applicable Standards

**Determine mode from `$ARGUMENTS`:**

- If `$ARGUMENTS` starts with `compliance` → **Compliance mode**. Extract the framework name after `compliance` (e.g., `gdpr`, `pci-dss`, `hipaa`). If no framework specified, ask the user which compliance framework to audit.
- If `$ARGUMENTS` is `quick` → **Quick mode**
- Otherwise → **Full mode** (`$ARGUMENTS` is treated as an optional path)

### Full Mode

**No tag filter** — load ALL entries from `applicableStandards`.

### Compliance Mode

Map the framework argument to standard id:
- `gdpr` → `compliance-gdpr`
- `pci-dss` → `compliance-pci-dss`
- `hipaa` → `compliance-hipaa`

Keep entries where:
- `id` matches the mapped compliance standard, OR
- `tags` array includes `"security"` (security standards are cross-referenced with compliance)

If the mapped compliance standard is not in `applicableStandards`, stop and tell the user: "Compliance framework '[name]' is not configured in .vcp/config.json. Run `/vcp-init` to add it."

### Quick Mode

**No tag filter** — load ALL entries from `applicableStandards`.

---

For each selected standard, use WebFetch to fetch its content from:
```
{entry.url}
```

Extract the **Rules** section from each fetched standard.

## Step 3: Scan Target Code

### Quick Mode (No Team)

Quick mode scans directly without team mode for speed.

1. Use Glob to find code files in the project (exclude patterns from `exclude`).
2. For each standard, check rules with **critical and high** severity implications. Skip medium-severity rules for speed. Focus on:
   - Security vulnerabilities (injection, hardcoded secrets, missing auth)
   - Critical architecture violations (missing input validation at boundaries)
   - Critical compliance gaps (unencrypted PII, missing audit logging)
3. For each violation found, note: standard id, rule number, file:line, and brief description.
4. **Skip to Step 5 (Report)** — no validation pass in quick mode.

### Full Mode & Compliance Mode (Team Mode)

**Target path:** `$ARGUMENTS` if provided and not a mode keyword. Default: project root.

#### Create Team

Create a team named `vcp-audit` using TeamCreate.

#### Partition Standards into Scanning Domains

Group applicable standards into domains. Only create domains where standards exist:

| Domain | Standards |
|--------|-----------|
| `backend` | core-security, core-secure-defaults, core-api-design-security, core-data-flow-security, core-attack-surface, web-backend-security, web-backend-structure, web-backend-data-access, web-backend-api-design, web-backend-realtime, web-backend-caching |
| `frontend` | web-frontend-security, web-frontend-structure, web-frontend-performance, web-frontend-accessibility |
| `architecture` | core-architecture, core-code-quality, core-error-handling, core-testing, core-root-cause-analysis, core-concurrency-security |
| `database` | database-encryption, database-schema-security, core-dependency-management |
| `compliance` | compliance-gdpr, compliance-pci-dss, compliance-hipaa (whichever are in applicableStandards) |
| `mobile` | mobile-security, mobile-platform-configuration |
| `desktop` | desktop-security |
| `cli` | cli-security-and-quality |
| `devops` | devops-container-security, devops-cicd-security, devops-iac-security, devops-kubernetes-security |
| `agentic-ai` | agentic-ai-agent-security, agentic-ai-tool-security, agentic-ai-permissions, agentic-ai-supply-chain, agentic-ai-communication |

**Every standard in `applicableStandards` must be assigned to exactly one domain.** If a future standard does not fit any domain above, add it to the most relevant domain or create a new one. Never silently drop a standard.

#### Create Tasks and Spawn Scanner Agents

For each domain:

1. Create a task via TaskCreate describing the scanning scope.
2. Spawn a scanner agent via Task with `subagent_type="Explore"` and `team_name="vcp-audit"`.

**Each scanner agent prompt must include:**
- The extracted rules for its domain (rule number, title, and description for each)
- The project root path and target path
- Exclude patterns from config
- Instruction to return findings in this **exact format** (one per finding):

```
FINDING: {standard-id}/rule-{N} ({severity})
FILE: {path}:{line}
EVIDENCE: {exact code snippet read from the file, 3-5 relevant lines}
ISSUE: {specific problem description}
FIX: {suggested fix}
```

**Critical:** Instruct agents to include the literal code they read as EVIDENCE. Findings without evidence cannot be validated.

#### Collect Results

Wait for all scanner agents to report back. Messages are delivered automatically.

**Failure handling:** If an agent fails, stalls, or returns no findings after a reasonable wait:
- Do NOT block the entire audit. Proceed with findings from agents that completed.
- Note the failed domain in the report: `**WARNING: [domain] scan did not complete. Results may be incomplete.**`
- The orchestrator may scan the failed domain's standards directly as a fallback.

Once all available results are collected, aggregate all findings.

### Existing-File Secrets Scan

In addition to standard-based scanning, the `backend` domain scanner must also check for secrets already committed to the repository:

1. **Scan `.env*` files** (`.env`, `.env.local`, `.env.production`, etc.) for actual secret values. Skip placeholders like `YOUR_API_KEY_HERE`, `changeme`, `xxx`, `TODO`, or empty values.
2. **Scan config files** (`config.json`, `config.yaml`, `settings.py`, `application.properties`, etc.) for embedded credentials — API keys, passwords, connection strings with credentials, bearer tokens.
3. **Check for files that should not be committed:** `.env`, `credentials.json`, `*.pem`, `*.key`, `*.p12`, `service-account.json`, `.htpasswd`.

**False positive controls:**
- Respect the `exclude` patterns from config. Skip files matching exclusion globs.
- Skip files in `test/`, `tests/`, `__tests__/`, `fixtures/`, `examples/`, `sample/` directories — test fixtures often contain dummy secrets.
- Map all secrets findings to **CWE-798** so that `"ignore": ["CWE-798"]` in `.vcp/config.json` suppresses them consistently with security-gate behavior.
- Only flag values that look like real secrets (high entropy strings, known API key prefixes like `sk_live_`, `AKIA`, `ghp_`, `glpat-`).

## Step 4: Validate Findings

**This step applies to Full and Compliance modes only. Skip for Quick mode.**

After collecting findings from all scanner agents, validate each one. This eliminates false positives before the user sees the report.

For EACH finding, perform these checks **in order**. Stop at the first check that produces a verdict.

### Check 1: Verify Evidence

Re-read the flagged file at the reported line (±30 lines context). Does the code match the reported evidence?
- If the file/line doesn't exist or the code doesn't match → **FALSE-POSITIVE**

### Check 2: Trace Data Flow (for injection, redirect, and XSS findings)

Where does the flagged input actually come from? Trace backwards through assignments and function calls:
- **User-controlled** (query params, form data, URL path, URL hash, `window.location.*`, headers, external API responses, database values from user input) → proceed to next check
- **Internally constructed** (hardcoded constants, derived from server-only state like process uptime or config files, from a function that returns a fixed value) → **FALSE-POSITIVE**

**Caution:** Browser URL properties (`window.location.pathname`, `window.location.hash`, `document.referrer`) are attacker-controlled — an attacker chooses which URL the victim visits. Do NOT treat these as trusted.

### Check 3: Verify Rule Scope

Re-read the specific rule that was violated. Does the flagged code match what the rule actually targets?

Examples of scope mismatches:
- Rule targets auth tokens in localStorage → code stores user-generated content → **FALSE-POSITIVE**
- Rule targets logging sensitive data → code logs a public identifier (OAuth client_id, request IDs) → **FALSE-POSITIVE**
- Rule targets user input concatenation → code concatenates a constant string → **FALSE-POSITIVE**

### Check 4: Check Mitigating Factors

Search the codebase for factors that reduce or eliminate the risk:
- **Lockfile committed** → loose version ranges downgraded to medium (not a supply chain risk)
- **Security headers set at proxy/CDN layer** → missing application-level headers may be covered
- **Framework defaults** handle the concern (e.g., React auto-escapes JSX, Next.js escapes output)
- **Rate limiting / CAPTCHA** in front of the endpoint → timing attacks downgraded
- **Single-tenant deployment** → multi-tenant controls (RLS) are defense-in-depth, not critical

If a mitigating factor fully addresses the concern → **FALSE-POSITIVE**
If a mitigating factor partially addresses the concern → **downgrade severity one level**

### Check 5: Check Technology Context

Consider the specific technology stack's behavior:
- PostgreSQL 11+: adding nullable columns is a non-locking operation (not a zero-downtime concern)
- Go `bcrypt.DefaultCost`: verify the actual value for the specific library version
- ORM-specific: check if the ORM handles parameterization automatically
- Framework migration tools: check if they handle rollback automatically

If the technology already handles the concern → **FALSE-POSITIVE**

### Check 6: Exposure Context

Determine how the flagged code is reachable. Entry points include HTTP routes, WebSocket handlers, CLI argument parsers, message queue consumers, cron jobs, file import handlers, and gRPC/GraphQL resolvers — not just HTTP.

- Is it called from a public entry point (no authentication required)?
- Is it called from an authenticated entry point?
- Is it behind an admin route with role checks?
- Is it an internal utility not reachable from any entry point (HTTP, CLI, MQ, cron, etc.)?

Adjust severity based on exposure:
- Public entry point → keep original severity
- Authenticated entry point → keep original severity (compromised credentials or insider threat)
- Admin-only behind authentication + role check → downgrade one level
- Internal code not reachable from any entry point → **FALSE-POSITIVE** (unless it could become reachable in the future, in which case mark as UNLIKELY)

**How to check:** Trace backwards from the flagged function. Find all callers using Grep. Follow the call chain to an entry point (route handler, CLI parser, MQ consumer, cron handler). Check what middleware, decorators, or access controls protect that entry point.

### Check 7: Exploit Path Viability

Can this finding be exploited end-to-end? Trace the full exploit path:
1. **Entry point:** How does the attacker reach the vulnerable code? (specific HTTP endpoint, WebSocket message, CLI argument)
2. **Preconditions:** What must be true for exploitation? (authentication bypassed, specific user role, race condition timing)
3. **Vulnerability:** What happens when the vulnerable code executes with attacker input?
4. **Impact:** What does the attacker gain? (data exfiltration, privilege escalation, code execution, denial of service)

Check for mitigating factors in the path:
- WAF (Web Application Firewall) rules that filter the attack payload
- CSP (Content Security Policy) headers that prevent script execution
- Framework protections (e.g., Django ORM auto-parameterization, React auto-escaping)
- Rate limiting that prevents brute-force exploitation
- Network segmentation that limits blast radius

If no viable exploit path exists (e.g., all paths to the sink go through adequate defenses) → mark as **UNLIKELY**
If the exploit path exists but mitigating factors significantly reduce risk → downgrade severity

### Assign Verdict

After all checks, assign one of:
- **CONFIRMED** — Finding verified. Evidence matches, rule applies, no mitigating factors.
- **LIKELY** — Finding plausible but partial mitigation exists or context is ambiguous. Include in report, flag for manual review.
- **FALSE-POSITIVE** — Remove from report entirely.

### Severity Adjustment

For CONFIRMED and LIKELY findings, adjust severity if warranted:
- Mitigating factor partially addresses the concern → downgrade one level
- Concern is defense-in-depth (recommended but not a direct vulnerability) → cap at medium

## Step 4.5: Cleanup Team

**Always run this step**, whether validation succeeded, partially completed, or failed:
1. Send shutdown requests to all scanner agents via SendMessage.
2. Delete the team via TeamDelete.

If cleanup itself fails, warn the user: `**Note: Team cleanup incomplete. Run TeamDelete manually if needed.**`

## Step 5: Report Findings

Before outputting findings, remove any that match an entry in the `ignoredRules` array from the resolved config. If `"standard-id/rule-N"` is in the list, suppress that specific rule's findings. (Standard-level ignores are already applied by the config resolution script.) After filtering, if any findings were suppressed, append a line: `**Suppressed:** X finding(s) by ignore config.` If any suppressed findings came from security-scoped standards (tag `"security"`) or compliance standards, also add: `**WARNING: Critical security findings suppressed by ignore config. Review .vcp/config.json ignore list.**`

### Full Mode Output

```
### VCP Audit

**Scopes:** core, web-backend, ...
**Standards loaded:** N standards, M rules checked
**Target:** [path or "project root"]
**Validation:** X findings scanned → Y confirmed, Z likely, W false positives removed

#### Standards Summary

| Standard | Status | Critical | High | Medium |
|----------|--------|----------|------|--------|
| core-security | FAIL | 2 | 1 | 0 |
| core-architecture | PASS | 0 | 0 | 0 |
| web-backend-security | WARN | 0 | 3 | 1 |
| ... | ... | ... | ... | ... |

**Overall: X critical, Y high, Z medium findings across N standards.**

#### Findings by Standard

##### core-security

- **Rule 3** (critical) — SQL string concatenation
  - **File:** src/db/queries.py:42
  - **Issue:** User input concatenated into SQL query
  - **Fix:** Use parameterized queries

- **Rule 5** ⚠ LIKELY (high) — JWT secret length
  - **File:** src/auth/config.py:12
  - **Issue:** No minimum length check for HMAC-SHA256 key
  - **Fix:** Enforce minimum 32-byte secret length
  - **Note:** Verify actual secret length in deployment config

...
```

Status per standard: **FAIL** = has critical findings, **WARN** = has high findings but no critical, **PASS** = no findings at or above the severity threshold.

LIKELY findings are marked with ⚠ and include a **Note** explaining what the user should verify.

### Compliance Mode Output

```
### VCP Compliance Audit — GDPR

**Standards loaded:** compliance-gdpr + N security standards
**Rules checked:** M rules
**Validation:** X findings scanned → Y confirmed, Z likely, W false positives removed

| Rule | Status | Regulation Ref | Finding |
|------|--------|----------------|---------|
| Rule 1 | FAIL | GDPR Art. 5(1)(f) | PII stored without encryption in users table |
| Rule 2 | PASS | GDPR Art. 17 | Data deletion endpoint exists |
| Rule 3 | WARN | GDPR Art. 32 | Encryption at rest configured but key rotation not found |
| ... | ... | ... | ... |

**Summary:** X FAIL, Y WARN, Z PASS out of M rules.
```

### Quick Mode Output

```
### VCP Release Readiness

**Standards loaded:** N standards
**Rules checked:** M critical/high rules (medium skipped)
**Note:** Quick mode does not validate findings. Run `/vcp-audit` for validated results.

| Standard | Verdict | Blocking Issues |
|----------|---------|-----------------|
| core-security | FAIL | 2 critical findings |
| core-architecture | PASS | — |
| web-backend-security | WARN | 1 high finding |
| ... | ... | ... |

---

**Verdict: NOT READY — 2 critical issues must be resolved before release.**
```

Verdict logic:
- **FAIL** = critical findings exist in that standard
- **WARN** = high findings exist but no critical
- **PASS** = no findings at or above the severity threshold
- Overall **READY** = no FAIL standards. Overall **NOT READY** = one or more FAIL standards.

If no findings across all standards: **"READY — No critical or high issues found across N standards."**
