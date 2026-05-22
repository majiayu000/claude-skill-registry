---
name: audit-security
description: Run a single-session security audit on the codebase
---

# Single-Session Security Audit

## Pre-Audit Validation

**Step 1: Check Thresholds**

Run `npm run review:check` and report results. Check for security-sensitive file
changes.

- Display count of security-sensitive files changed
- If none: "⚠️ No security-sensitive changes detected. Proceed anyway?"
- Continue with audit regardless (user invoked intentionally)

**Step 2: Gather Current Baselines**

Collect these metrics by running commands:

```bash
# Dependency vulnerabilities (extract summary without truncating JSON)
npm audit --json 2>/dev/null | node -e '
try {
  const d = JSON.parse(require("fs").readFileSync(0,"utf8"));
  console.log(JSON.stringify(d.metadata?.vulnerabilities ?? d.vulnerabilities ?? {}, null, 2));
} catch (e) {
  console.log("{\"error\": \"Invalid JSON from npm audit\"}");
}
'

# Security lint warnings
npm run lint 2>&1 | grep -i "security" | head -10

# Pattern compliance (security patterns)
npm run patterns:check 2>&1

# Check for .env files (existence only - no permission/owner metadata needed)
ls .env* 2>/dev/null || echo "No .env files found"
```

**Step 2b: Query SonarCloud Security (if MCP available)**

If `mcp__sonarcloud__get_security_hotspots` is available:

- Query with `status: "TO_REVIEW"` to get unresolved security hotspots
- Note hotspot count and severity distribution

If `mcp__sonarcloud__get_issues` is available:

- Query with `types: "VULNERABILITY"` to get security-specific issues
- Cross-reference with npm audit findings for comprehensive coverage

This provides real-time security issue data from static analysis.

**Step 3: Load False Positives Database**

Read `docs/audits/FALSE_POSITIVES.jsonl` and filter findings matching:

- Category: `security`
- Expired entries (skip if `expires` date passed)

Note patterns to exclude from final findings.

**Step 4: Check Template Currency**

Read `docs/templates/MULTI_AI_SECURITY_AUDIT_PLAN_TEMPLATE.md` and verify:

- [ ] FIREBASE_CHANGE_POLICY.md reference is valid
- [ ] Security-sensitive file list is current
- [ ] OWASP categories are complete
- [ ] Firestore rules path is correct

If outdated, note discrepancies but proceed with current values.

---

## Audit Execution

**Focus Areas (12 Categories):**

1. Authentication & Authorization (auth checks, role validation, IDOR, privilege
   escalation)
2. Input Validation & Injection Prevention:
   - SQL/NoSQL injection, command injection
   - Template injection, eval/Function(), new Function()
   - Unsafe deserialization, prototype pollution
3. Data Protection (encryption, PII handling, secrets, overly verbose errors)
4. Firebase/Firestore Security (rules, Cloud Functions, rate limiting, replay
   protection)
5. Dependency Security & Supply Chain:
   - npm audit, outdated packages
   - Unpinned versions, risky postinstall scripts
   - Unused dependencies with known vulnerabilities
6. OWASP Top 10 Coverage
7. Hosting & Headers Security:
   - CSP, HSTS, X-Frame-Options, X-Content-Type-Options
   - COOP, COEP, Referrer-Policy, Permissions-Policy
8. Next.js/Framework-Specific:
   - Server/client boundary leaks (secrets in client bundles)
   - API route / middleware auth gates
   - Static export vs server rendering assumptions
9. File Handling Security:
   - Insecure file upload, path traversal
   - MIME type validation, file size limits
10. Crypto & Randomness:
    - Weak randomness (Math.random for security), broken hashing
    - Unsafe JWT/session handling, homegrown crypto
11. Product/UX Security Risks:
    - Misleading "security UI" (toggles without server enforcement)
    - Dangerous defaults not clearly communicated
    - Admin-only flows accessible via client routes without backend checks
12. AI-Generated Code & Agent Security:
    - Prompt-injection surfaces in scripts/configs
    - Agent config files with unsafe patterns
    - Suspicious strings/comments that could manipulate AI agents

**For each category:**

1. Search relevant files using Grep/Glob
2. Identify specific vulnerabilities with file:line references
3. Classify severity: S0 (Critical) | S1 (High) | S2 (Medium) | S3 (Low)
4. Classify OWASP category if applicable
5. Estimate effort: E0 (trivial) | E1 (hours) | E2 (day) | E3 (major)
6. **Assign confidence level** (see Evidence Requirements below)

**Security-Sensitive Files to Check:**

- `firestore.rules`, `storage.rules`
- `functions/src/**/*.ts`
- `lib/firebase*.ts`, `lib/auth*.ts`
- `middleware.ts`, `next.config.mjs`
- `firebase.json` (hosting headers, rewrites)
- `.env*` files (environment variables)
- `package.json`, `package-lock.json` (supply chain)
- `.claude/` configs (agent security)
- Any file with "security", "auth", "token", "secret", "credential" in name

**Additional Checks for Vibe-Coded Apps:**

- Search for `eval(`, `new Function(`, `Function(` - dynamic code execution
- Search for `dangerouslySetInnerHTML` - XSS vectors
- Search for `NEXT_PUBLIC_` env vars - ensure no secrets leaked
- Search for `process.env` in client components - boundary leaks
- Search for `postinstall`, `preinstall` in package.json - supply chain
- Search for suspicious patterns in `.claude/` that could be prompt injection

**Scope:**

- Include: `app/`, `components/`, `lib/`, `functions/`, `firestore.rules`,
  `firebase.json`, `.claude/`
- Exclude: `node_modules/`, `.next/`, `docs/`, `tests/`

---

## Evidence Requirements (MANDATORY)

**All findings MUST include:**

1. **File:Line Reference** - Exact location (e.g., `lib/auth.ts:45`)
2. **Code Snippet** - The actual vulnerable code (3-5 lines of context)
3. **Verification Method** - How you confirmed this is an issue (grep output,
   tool output)
4. **Standard Reference** - CWE number, OWASP category, or security best
   practice citation

**Confidence Levels:**

- **HIGH (90%+)**: Confirmed by external tool (npm audit, ESLint security),
  verified file exists, code snippet matches
- **MEDIUM (70-89%)**: Found via pattern search, file verified, but no tool
  confirmation
- **LOW (<70%)**: Pattern match only, needs manual verification

**S0/S1 findings require:**

- HIGH or MEDIUM confidence (LOW confidence S0/S1 must be escalated)
- Dual-pass verification (re-read the code after initial finding)
- Cross-reference with npm audit, ESLint, or patterns:check output

---

## Cross-Reference Validation

Before finalizing findings, cross-reference with:

1. **npm audit output** - Mark dependency findings as "TOOL_VALIDATED" if npm
   audit agrees
2. **ESLint security warnings** - Mark code findings as "TOOL_VALIDATED" if
   ESLint flagged same issue
3. **patterns:check output** - Mark pattern violations as "TOOL_VALIDATED" if
   patterns:check flagged
4. **Prior audits** - Check `docs/audits/single-session/security/` for duplicate
   findings

Findings without tool validation should note: `"cross_ref": "MANUAL_ONLY"`

---

## Dual-Pass Verification (S0/S1 Only)

For all S0 (Critical) and S1 (High) findings:

1. **First Pass**: Identify the issue, note file:line and initial evidence
2. **Second Pass**: Re-read the actual code in context
   - Verify the vulnerability is exploitable
   - Check for existing mitigations (validation, sanitization, auth checks)
   - Confirm file and line still exist
3. **Decision**: Mark as CONFIRMED or DOWNGRADE (with reason)

Document dual-pass result in finding: `"verified": "DUAL_PASS_CONFIRMED"` or
`"verified": "DOWNGRADED_TO_S2"`

---

## Output Requirements

**1. Markdown Summary (display to user):**

```markdown
## Security Audit - [DATE]

### Baselines

- npm audit: X vulnerabilities (Y critical, Z high)
- Security patterns: X violations
- Security-sensitive files: X changed since last audit

### Findings Summary

| Severity | Count | OWASP Category | Confidence  |
| -------- | ----- | -------------- | ----------- |
| S0       | X     | ...            | HIGH/MEDIUM |
| S1       | X     | ...            | HIGH/MEDIUM |
| S2       | X     | ...            | ...         |
| S3       | X     | ...            | ...         |

### Critical/High Findings (Immediate Action)

1. [file:line] - Description (S0/OWASP-A01) - DUAL_PASS_CONFIRMED
2. ...

### False Positives Filtered

- X findings excluded (matched FALSE_POSITIVES.jsonl patterns)

### Dependency Vulnerabilities

- ...

### Recommendations

- ...
```

**2. JSONL Findings (save to file):**

Create file: `docs/audits/single-session/security/audit-[YYYY-MM-DD].jsonl`

Each line (UPDATED SCHEMA with confidence and verification):

```json
{
  "id": "SEC-001",
  "category": "Auth|Input|Data|Firebase|Deps|OWASP|Headers|Framework|FileHandling|Crypto|ProductUXRisk|AgentSecurity",
  "severity": "S0|S1|S2|S3",
  "effort": "E0|E1|E2|E3",
  "confidence": "HIGH|MEDIUM|LOW",
  "verified": "DUAL_PASS_CONFIRMED|TOOL_VALIDATED|MANUAL_ONLY",
  "owasp": ["A01", "A03"],
  "file": "path/to/file.ts",
  "line": 123,
  "title": "Short description",
  "description": "Detailed vulnerability",
  "recommendation": "How to fix",
  "cwe": "CWE-XXX",
  "evidence": ["code snippet", "grep output", "tool output"],
  "cross_ref": "npm_audit|eslint|patterns_check|MANUAL_ONLY"
}
```

**3. Markdown Report (save to file):**

Create file: `docs/audits/single-session/security/audit-[YYYY-MM-DD].md`

Full markdown report with all findings, baselines, and remediation plan.

---

## Post-Audit Validation

**Before finalizing the audit:**

1. **Run Validation Script:**

   ```bash
   node scripts/validate-audit.js docs/audits/single-session/security/audit-[YYYY-MM-DD].jsonl
   ```

2. **Validation Checks:**
   - All findings have required fields
   - No matches in FALSE_POSITIVES.jsonl (or documented override)
   - No duplicate findings
   - All S0/S1 have HIGH or MEDIUM confidence
   - All S0/S1 have DUAL_PASS_CONFIRMED or TOOL_VALIDATED

3. **If validation fails:**
   - Review flagged findings
   - Fix or document exceptions
   - Re-run validation

---

## Post-Audit

1. Display summary to user
2. Confirm files saved to `docs/audits/single-session/security/`
3. Run `node scripts/validate-audit.js` on the JSONL file
4. **Validate CANON schema** (if audit updates CANON files):
   ```bash
   npm run validate:canon
   ```
   Ensure all CANON files pass validation before committing.
5. **Update AUDIT_TRACKER.md** - Add entry to "Security Audits" table:
   - Date: Today's date
   - Session: Current session number from SESSION_CONTEXT.md
   - Commits Covered: Number of commits since last security audit
   - Files Covered: Number of security-sensitive files analyzed
   - Findings: Total count (e.g., "1 S0, 2 S1, 3 S2")
   - Reset Threshold: YES (single-session audits reset that category's
     threshold)
6. **Update Technical Debt Backlog** - Re-aggregate all findings:
   ```bash
   npm run aggregate:audit-findings
   ```
   This updates `docs/aggregation/MASTER_ISSUE_LIST.md` and the Technical Debt
   Backlog section in `ROADMAP.md`. Review the updated counts and ensure new
   findings are properly categorized.
7. If S0/S1 findings: "⚠️ Critical security issues found. Recommend immediate
   remediation."
8. Ask: "Would you like me to fix any of these issues now?"

---

## Threshold System

### Category-Specific Thresholds

This audit **resets the security category threshold** in `docs/AUDIT_TRACKER.md`
(single-session audits reset their own category; multi-AI audits reset all
thresholds). Reset means the commit counter for this category starts counting
from zero after this audit.

**Security audit triggers (check AUDIT_TRACKER.md):**

- ANY security-sensitive file modified, OR
- 20+ commits since last security audit

### Multi-AI Escalation

After 3 single-session security audits, a full multi-AI Security Audit is
recommended. Track this in AUDIT_TRACKER.md "Single audits completed" counter.

---

## Adding New False Positives

If you encounter a pattern that should be excluded from future audits:

```bash
node scripts/add-false-positive.js \
  --pattern "regex-pattern" \
  --category "security" \
  --reason "Explanation of why this is not a security issue" \
  --source "AI_REVIEW_LEARNINGS_LOG.md#review-XXX"
```
