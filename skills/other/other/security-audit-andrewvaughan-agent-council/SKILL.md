---
name: security-audit
description: Run a comprehensive security audit combining automated SAST scanning, STRIDE threat modeling, and attack tree analysis. Use before major releases, after security-sensitive changes, or on a regular cadence. Can audit the full codebase or specific directories.
user-invokable: true
---

# Security Audit Workflow

Run a comprehensive security audit that combines automated static analysis, threat modeling, and multi-perspective council review. This skill produces a prioritized audit report with actionable remediation steps.

## Scope Exclusions

> [!IMPORTANT]
> This audit covers **application-level security only**. Production infrastructure (TLS termination, reverse proxy, network segmentation, firewall rules, DNS) is managed by a separate project and is out of scope. Do not flag missing TLS, reverse proxy configuration, network-level MITM risks, or production deployment topology as findings.

## Step 1: Define Audit Scope

Ask the user:

- **Scope**: Full codebase or specific area? (e.g., `apps/api/src/auth/`, `apps/web/src/`)
- **Trigger**: What prompted this audit? (routine, pre-release, security incident, new feature, dependency update)
- **Focus areas**: Authentication, API security, data protection, frontend security, or all?

### CHECKPOINT: Confirm the audit scope and focus areas with the user before proceeding.

## Step 2: Automated SAST Scanning

Invoke `/security-scanning:security-sast` on the defined scope.

Scan for:

- **Injection**: SQL injection, NoSQL injection, command injection, LDAP injection
- **XSS**: Reflected, stored, and DOM-based cross-site scripting
- **CSRF**: Missing CSRF protections on state-changing endpoints
- **Authentication**: Weak password policies, broken auth flows, session fixation
- **Secrets**: Hardcoded API keys, passwords, tokens, connection strings
- **Dependencies**: Known vulnerabilities in npm packages (CVEs)
- **Deserialization**: Insecure deserialization patterns
- **Prototype pollution**: JavaScript-specific object manipulation attacks

Collect every finding with:

- **Severity**: Critical / High / Medium / Low / Info
- **Category**: OWASP Top 10 mapping
- **Location**: File path and line number
- **Description**: What the vulnerability is
- **Evidence**: The specific code pattern that triggered the finding
- **Remediation**: How to fix it

## Step 3: Security Hardening Review

Invoke `/security-scanning:security-hardening` for a comprehensive hardening review:

### HTTP Security

- Security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options)
- CORS configuration (allowed origins, methods, headers)
- Cookie security flags (HttpOnly, Secure, SameSite)

### API Security

- Rate limiting on all public endpoints
- Input validation completeness (every user input validated)
- Output encoding to prevent injection
- API key and token management
- Request size limits

### Authentication and Authorization

- Password hashing algorithm (bcrypt, argon2)
- JWT configuration (algorithm, expiration, refresh)
- Session management (timeout, invalidation, rotation)
- Role-based access control enforcement
- OAuth/OIDC configuration (if applicable)

### Data Protection

- PII encrypted at rest
- Sensitive data encrypted in transit (TLS 1.2+)
- Logging does not include sensitive data
- Error messages do not leak internal details
- Database connection uses SSL

### Environment Variables

- No secrets hardcoded in code or logs
- Startup validation rejects weak/default secrets in production

## Step 4: STRIDE Threat Modeling

Invoke `/security-scanning:stride-analysis-patterns` to systematically model threats:

### Spoofing

- Can user identities be faked? (auth bypass, token theft)
- Can service identities be spoofed? (service-to-service auth)

### Tampering

- Can request data be modified in transit?
- Can database records be altered without authorization?
- Can client-side data (localStorage, cookies) be tampered?

### Repudiation

- Are all security-relevant actions logged?
- Can a user deny performing an action?
- Is there an audit trail for data changes?

### Information Disclosure

- Can sensitive data leak through error messages?
- Can unauthorized users access other users' data?
- Are there timing attacks or side-channel leaks?

### Denial of Service

- Can the system be overwhelmed by excessive requests?
- Are there resource-intensive endpoints without rate limiting?
- Can large payloads cause memory exhaustion?

### Elevation of Privilege

- Can a regular user access admin functionality?
- Can horizontal privilege escalation occur (access another user's resources)?
- Are there IDOR (Insecure Direct Object Reference) vulnerabilities?

Document each threat with:

- **Likelihood**: High / Medium / Low
- **Impact**: Critical / High / Medium / Low
- **Risk Score**: Likelihood x Impact
- **Existing Mitigations**: What's already in place
- **Gaps**: What's missing

## Step 5: Attack Tree Analysis

For the top 3 highest-risk threats identified in STRIDE:

Invoke `/security-scanning:attack-tree-construction` to build attack trees showing:

- **Attack goal**: What the attacker wants to achieve
- **Attack paths**: Different ways to reach the goal
- **Sub-goals**: Intermediate steps required
- **Required resources**: Attacker skill level, tools, access needed
- **Existing defenses**: Current mitigations along each path
- **Weakest links**: Where defenses are thinnest

## Step 6: Architecture Council Security Review

Activate a subset of the Architecture Council (defined in `.claude/councils/architecture-council.md`) for security review:

> **Model Selection**: See the [Model Selection](../../README.md#model-selection) section in README.md for mapping agent model specs to Task tool parameters.

### Security Engineer (Lead) — consult: security-scanning

- Validate automated findings (identify false positives)
- Prioritize remediation based on actual risk
- Assess overall security posture
- **Assessment**: Strong / Adequate / Needs Improvement / Critical Risk

### Principal Engineer — consult: full-stack-orchestration

- Assess architectural implications of required remediations
- Identify systemic patterns that create vulnerabilities
- Recommend architectural changes for defense-in-depth
- **Assessment**: Architecturally sound / Needs refactoring / Fundamental issues

### Backend Specialist — consult: backend-development

- Evaluate backend-specific security patterns
- Assess API security implementation quality
- Review database access patterns for injection risks
- **Assessment**: Well-secured / Some gaps / Significant concerns

## Step 7: Present Audit Report

Generate a structured security audit report:

### Executive Summary

- **Overall Security Posture**: Strong / Adequate / Needs Improvement / Critical
- **Total Findings**: Count by severity (Critical, High, Medium, Low)
- **Top 3 Risks**: The most important issues to address
- **STRIDE Coverage**: Summary of threat categories with risk levels

### Critical and High Findings (must-fix)

For each finding:

- Severity, category, and OWASP mapping
- File and line number
- Description with evidence
- Step-by-step remediation
- Effort estimate (quick fix / moderate / significant)

### Medium Findings (should-fix)

Same format as above, prioritized by risk.

### Low and Info Findings (track)

Summary list for tracking as technical debt.

### Threat Model Summary

- STRIDE analysis results table
- Top 3 attack trees (visual or structured text)
- Defense gap analysis

### Recommended Actions (prioritized)

1. **Immediate** (Critical): Must fix before next deployment
2. **This Sprint** (High): Fix within current work cycle
3. **Next Sprint** (Medium): Schedule for upcoming work
4. **Backlog** (Low): Track as technical debt

### CHECKPOINT: Present the full audit report to the user. Ask which findings they want to remediate now, and which to track for later.

## Step 8: Remediation (Optional)

If the user chooses to remediate findings now:

1. Address findings in priority order (Critical first, then High)
2. For each fix:
   - Apply the remediation
   - Re-run the relevant SAST scan to verify the fix
   - Run tests to ensure no regressions
3. Commit each fix with:
   ```
   fix(security): remediate <finding-description>
   ```

After remediation, suggest the next step (see below).

## Step 9: Create Issues for Tracked Findings

For any findings that the user chooses to track for later (not remediated immediately in Step 8), create GitHub issues so they are not lost.

### CHECKPOINT: Present a summary table of findings to be created as issues before proceeding.

| #   | Finding         | Severity | Est. Size | Label `build-ready`? |
| --- | --------------- | -------- | --------- | -------------------- |
| 1   | \<description\> | Medium   | S         | Yes                  |

Ask the user to confirm which findings should become issues. Wait for approval before creating.

> [!NOTE]
> Add the `build-ready` label to findings with a clear, scoped remediation (the fix is known and does not require architectural decisions). Omit `build-ready` for findings that need further planning via `/plan-feature` — for example, findings that require schema changes, new infrastructure, or cross-cutting architectural decisions.

1. For each approved finding, create a GitHub issue:

   ```bash
   ISSUE_URL=$(gh issue create \
     --title "security: <finding-description>" \
     --body "<body>" \
     --label "enhancement" \
     --label "security-audit" \
     --label "build-ready")

   ISSUE_NUM=$(echo "$ISSUE_URL" | grep -o '[0-9]*$')
   ```

   Omit `--label "build-ready"` for findings that need further planning (see NOTE above).

   The issue body should include:
   - **Context**: Which audit identified this finding and the audit date
   - **Problem**: Description with file path and line number
   - **Recommended Fix**: Step-by-step remediation from the audit report
   - **Priority**: Severity rating and recommended timeline
   - **Files**: Affected file paths

2. Add each created issue to the project board and set fields:

   ```bash
   ITEM_ID=$(gh project item-add {PROJECT_NUMBER} --owner {OWNER} --url "$ISSUE_URL" --format json | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
   gh project item-edit --project-id {PROJECT_ID} --id "$ITEM_ID" --field-id {PHASE_FIELD_ID} --single-select-option-id <phase-option-id>
   gh project item-edit --project-id {PROJECT_ID} --id "$ITEM_ID" --field-id {SIZE_FIELD_ID} --single-select-option-id <size-option-id>
   gh project item-edit --project-id {PROJECT_ID} --id "$ITEM_ID" --field-id {START_FIELD_ID} --date <start-date>
   gh project item-edit --project-id {PROJECT_ID} --id "$ITEM_ID" --field-id {TARGET_FIELD_ID} --date <target-date>
   ```

   Set phase, size, and dates appropriate to the finding's priority and the current milestone:

   | Severity      | Typical Size             | Schedule Priority                                     |
   | ------------- | ------------------------ | ----------------------------------------------------- |
   | Critical/High | M (3 days) or L (5 days) | Current active milestone, near the front of the queue |
   | Medium        | S (2 days)               | Current milestone, after existing scheduled items     |
   | Low/Info      | XS (1 day)               | Current milestone or next, at the end of the queue    |

3. Report all created issue numbers (`$ISSUE_NUM`) and URLs to the user.

> [!IMPORTANT]
> Every tracked finding must have both a GitHub issue **and** a project board entry. Creating an issue without adding it to the project board is what causes orphaned work items that `/build-feature` cannot discover via auto-pick.

## Step 10: Close Tracking Issue (Conditional)

If the user provided a GitHub issue number as an argument (e.g., `/security-audit #137`):

1. Check off any audit checklist items in the issue body using `gh issue edit`
2. **CHECKPOINT**: Ask the user whether to close the issue now that the audit is complete. Present the issue number and title for confirmation.
3. If approved, close the issue:
   ```bash
   gh issue close <number> --reason completed
   ```

If no issue number was provided, skip this step.

## Step 11: Hand Off

Present the next step to the user:

- **If code was changed** (remediation applied): Run `/review-code` to verify fixes in context of other changes
- **If no code was changed** (audit-only): No further action needed — track findings as issues or technical debt
- **If starting a new feature**: Run `/plan-feature` to begin the next feature with audit findings in mind

**Pipeline**: `/plan-feature` → `/build-feature` or `/build-api` → `/review-code` → `/submit-pr`

**Standalone**: `/security-audit` can be run at any point in the pipeline or independently.
