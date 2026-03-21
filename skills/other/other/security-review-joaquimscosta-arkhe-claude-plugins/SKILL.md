---
name: security-review
description: >
  Security-focused code review identifying high-confidence exploitable vulnerabilities
  with two-axis severity/confidence scoring, OWASP 2025 alignment, per-finding Haiku
  verification, and false positive filtering. Optional GitHub PR posting.
  Use when user runs /security-review, /review:security-review, requests a "security review",
  "security audit", "vulnerability scan", or mentions "find vulnerabilities", "check for exploits".
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr comment:*), Bash(gh pr list:*)
argument-hint: "[output-directory] [--post-to-pr]"
---

# Security Review

Identify HIGH-CONFIDENCE security vulnerabilities with real exploitation potential. Two-axis scoring (severity + confidence), OWASP 2025 aligned, false positive filtered.

## Parse Arguments

**Output Path Configuration**:
- If `$ARGUMENTS` contains `--post-to-pr`: enable GitHub PR posting (Phase 6)
- Remaining non-flag arguments: use as output directory (default: `./reviews/security/`)

Example usage:
- `/review:security-review` — local report to `./reviews/security/`
- `/review:security-review audits/sec` — local report to `audits/sec/`
- `/review:security-review --post-to-pr` — local report + post to GitHub PR
- `/review:security-review audits/sec --post-to-pr` — both

## Git Analysis

GIT STATUS:

```
!`git status`
```

FILES MODIFIED:

```
!`git diff --name-only origin/HEAD...`
```

COMMITS:

```
!`git log --no-decorate origin/HEAD...`
```

DIFF CONTENT:

```
!`git diff --merge-base origin/HEAD`
```

Review the complete diff above. Focus ONLY on security implications newly added by this PR.

## Objective

- Only flag issues where you have **HIGH confidence** of actual exploitability
- Skip theoretical issues, style concerns, or low-impact findings
- Prioritize vulnerabilities leading to unauthorized access, data breaches, or system compromise
- Use two-axis scoring: severity (impact) and confidence (accuracy) are independent

## Security Categories (OWASP 2025 Aligned)

| Category | Key Checks | OWASP |
|----------|------------|-------|
| Access Control | IDOR, privilege escalation, SSRF, CORS, CSRF, path traversal | A01 |
| Security Misconfiguration | Default credentials, debug endpoints, cloud misconfig, XXE | A02 |
| Supply Chain | Dependency confusion, unpinned actions, vulnerable deps, CI/CD risks | A03 |
| Cryptographic Failures | Hardcoded keys, weak algorithms, insecure randomness, cert validation | A04 |
| Injection | SQLi, command injection, XSS, template injection, NoSQL injection | A05 |
| Auth & Session | Authentication bypass, JWT vulns, session management, missing MFA | A07 |
| Deserialization & Integrity | Unsafe deserialization, prototype pollution, unsigned updates | A08 |
| Error Handling | Fail-open patterns, exception swallowing, verbose error disclosure | A10 |
| API Security | BOLA, mass assignment, shadow APIs, missing rate limiting | API Top 10 |
| LLM/AI Security | Prompt injection, unsafe output handling, excessive agency | LLM Top 10 |

See [WORKFLOW.md](WORKFLOW.md) for detailed subcategories and severity assignment reference.

## Analysis Methodology

**Phase 1 — Repository Context**: Identify existing security frameworks, sanitization patterns, and security model in the codebase.

**Phase 1.5 — Automated Security Scan (Optional)**: Run Trivy (vulnerability/IaC scanning) and Gitleaks (secret detection) if available. Locate the scan script via Glob for `**/review/scripts/security-scan.sh`, then execute: `bash {script_path} --quick --output-dir {output-directory}`. If tools are not installed, skip gracefully — this phase is informational only. See [WORKFLOW.md](WORKFLOW.md) for details.

**Phase 2 — Comparative Analysis**: Compare new code against established secure practices. Flag deviations and new attack surfaces. Cross-reference with automated scan results if available.

**Phase 3 — Vulnerability Assessment**: Trace data flow from user inputs to sensitive operations. Confirm sink reachability and check for sanitizers in the path.

See [WORKFLOW.md](WORKFLOW.md) for detailed methodology and sub-task orchestration.

## Two-Axis Scoring

### Severity (Impact)

| Severity | Criteria | Example |
|----------|----------|---------|
| **CRITICAL** | RCE, auth bypass, mass data exfiltration | Deserialization RCE, SQLi with shell access |
| **HIGH** | Significant data access or privilege escalation | SQLi read, stored XSS, SSRF to cloud metadata |
| **MEDIUM** | Limited impact or requires user interaction | Reflected XSS, CSRF, IDOR on non-sensitive data |
| **LOW** | Defense-in-depth, minimal direct impact | Missing headers, verbose errors |

### Confidence (Accuracy)

| Confidence | Description | Action |
|------------|-------------|--------|
| **HIGH** | Data flow confirmed, clear exploit path | Report — include in findings |
| **MEDIUM** | Pattern match, context needed to confirm | Report only if severity >= HIGH |
| **LOW** | Theoretical or framework likely handles | Do not report |

## Confidence & Signal Quality

Before reporting any finding, assess using both axes:

| Severity \ Confidence | HIGH | MEDIUM | LOW |
|-----------------------|------|--------|-----|
| CRITICAL | **Report** | **Report** | Suppress |
| HIGH | **Report** | **Report** | Suppress |
| MEDIUM | **Report** | Suppress | Suppress |
| LOW | Suppress | Suppress | Suppress |

**Finding caps**: Max **8 meaningful findings** (Blocker + Improvement + Question) and max **2 Nits** per review. Keep the highest-severity, highest-confidence items.

**Self-reflection**: After generating all candidate findings, re-evaluate each in context. Remove redundant, low-signal, or theoretical items. Apply false positive filtering from [WORKFLOW.md](WORKFLOW.md).

## Triage Matrix

Categorize every finding:

- **[Blocker]**: Must fix before merge — CRITICAL/HIGH severity + HIGH confidence. RCE, auth bypass, injection with confirmed data flow (confidence >= HIGH)
- **[Improvement]**: Strong recommendation — HIGH severity + MEDIUM confidence, or MEDIUM + HIGH. Clear vulnerability pattern, may need context verification (confidence >= MEDIUM)
- **[Question]**: Seeks clarification — potential vulnerability depending on context, intent unclear (confidence >= MEDIUM)
- **[Nit]**: Minor hardening suggestion, optional — max 2 per review
- **[Praise]**: Acknowledge good security practice — max 1 per review

## Phase 4 — Per-Finding Haiku Verification

After Phase 3 identifies candidate findings, launch **N parallel Haiku agents** (one per finding) for independent verification.

Each Haiku agent receives:
- The finding description, severity, confidence, category, and CWE
- The relevant diff section around the flagged code
- The framework/sanitizer context discovered in Phase 1

Each agent verifies:
1. **Data flow reachability** — Can user input actually reach the vulnerable sink?
2. **Sanitizer presence** — Are there sanitizers/validators in the path that the main analysis missed?
3. **Framework handling** — Does the framework's security model prevent this exploit?
4. **False positive patterns** — Does this match any hard exclusion or precedent from [WORKFLOW.md](WORKFLOW.md)?

Each agent returns a verdict:
- **KEEP** — Finding confirmed. Data flow verified, no sanitizers found, exploit path is valid.
- **DISMISS** — False positive. Reason: {specific evidence — framework handling, sanitizer found, etc.}
- **DOWNGRADE** — Valid but lower severity or confidence. Reason: {what changed — e.g., only reachable by admins, mitigating control exists.}

Apply verdicts: remove DISMISSED findings, adjust DOWNGRADED findings' severity/confidence. Remaining findings proceed to report.

If a Haiku verification agent fails for a finding, default to KEEP (conservative — finding stays).

See [WORKFLOW.md](WORKFLOW.md) for the Haiku verification prompt template and verdict criteria.

## Output Format

For each vulnerability found:

```markdown
### [Triage] Vuln N: {Category Code}: `{file}:{line}`

* **Severity**: {CRITICAL|HIGH|MEDIUM}
* **Confidence**: {HIGH|MEDIUM}
* **Category**: {OWASP A0X:2025 or API/LLM Top 10}
* **CWE**: CWE-XXX
* **Description**: {What the vulnerability is and how it can be exploited}
* **Exploit Scenario**: {Specific attack path with example payload}
* **Recommendation**: {Concrete fix with code example}
```

## Phase 5 — Report Generation

1. **Create output directory** using Bash: `mkdir -p {output-directory}`
2. **Save the report** to: `{output-directory}/{YYYY-MM-DD}_{HH-MM-SS}_security-review.md`

Include this header:

```markdown
# Security Review Report

**Date**: {ISO 8601 date}
**Branch**: {current branch name}
**Commit**: {short commit hash}
**Reviewer**: Claude Code (security-review)
**Framework**: OWASP Top 10 2025 + API Top 10 + LLM Top 10

## Summary
- **Blocker**: {count} findings
- **Improvement**: {count} findings
- **Question**: {count} findings
- **Total**: {count} actionable findings
- **Automated Scan**: {Passed | X issues found | Skipped — tools not installed}
- **Haiku Verification**: {N} findings verified — {kept} kept, {dismissed} dismissed, {downgraded} downgraded

---
```

3. **Display the full report** to the user in the chat
4. **Confirm the save**: Security report saved to: {output-directory}/{filename}

## Phase 6 — Optional GitHub PR Posting

**Only execute if** `--post-to-pr` flag was passed.

1. Check if an open PR exists for the current branch via `gh pr view`
2. If no PR exists, inform the user: "No open PR found for this branch. Skipping GitHub posting."
3. If a PR exists, check eligibility via a **Haiku agent**:
   - Is the PR closed? → skip
   - Is the PR a draft? → skip
   - Has Claude already commented on this PR? → skip
4. If eligible, format findings as a concise PR comment and post via `gh pr comment`
5. Use the security-specific GitHub comment format from [WORKFLOW.md](WORKFLOW.md)

## Phase 7 — Automatic Verification

After saving the report and confirming the save to the user, invoke the false-positive verifier:

1. Use the Skill tool to invoke `review:verify-findings` with the saved report path as the argument
2. The verifier runs in an isolated forked context and produces a `.verified.md` report
3. After verification completes, inform the user of both report locations

If the Skill tool is not available (e.g., running inside a subagent), inform the user:
> Run verification manually: `/review:verify-findings {report-path}`

## False Positive Filtering

Apply the false positive filtering rules from [WORKFLOW.md](WORKFLOW.md) before finalizing. Each finding must pass the signal quality matrix above.

## Resources

- [WORKFLOW.md](WORKFLOW.md) - Detailed category taxonomy, analysis methodology, false positive filtering, sub-task orchestration
- [EXAMPLES.md](EXAMPLES.md) - Sample security review reports
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and calibration guidance
