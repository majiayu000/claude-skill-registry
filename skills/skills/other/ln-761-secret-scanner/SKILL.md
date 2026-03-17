---
name: ln-761-secret-scanner
description: Scans codebase for hardcoded secrets. Returns normalized findings with severity and remediation guidance. Pre-commit hook integration.
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Secret Scanner

Scans codebase for hardcoded secrets and credentials, returning structured findings for remediation.

## Purpose & Scope

- Detect hardcoded secrets using available tools (gitleaks, trufflehog) or manual patterns
- Classify findings by severity (Critical/High/Medium/Low)
- Filter false positives via baseline and allowlists
- Provide remediation guidance per finding type
- Return normalized report to parent orchestrator (ln-760)

## When to Use

- During project bootstrap (via ln-760-security-setup)
- Pre-commit hook validation
- CI/CD security pipeline
- Manual security audit

---

## Workflow

### Phase 1: Tool Detection

**Step 1: Check Available Scanners**
- Check if gitleaks is installed (preferred)
- Check if trufflehog is installed (alternative)
- If neither available: use manual pattern matching as fallback

**Step 2: Load Configuration**
- Load project `.gitleaks.toml` if exists (custom rules)
- Load `.gitleaksbaseline` if exists (known false positives)
- If no config: use default patterns from `references/detection_patterns.md`

### Phase 2: Scan Execution

**Step 1: Run Available Scanner**
- Execute scanner against project root
- Capture output in structured format (JSON/SARIF preferred)
- If tool unavailable: run manual grep patterns for high-confidence secrets

**Step 2: Parse Results**
- Normalize output to common format: file, line, pattern, raw_match
- Preserve original severity if provided by tool

### Phase 3: Report Generation

**Step 1: Severity Classification**
- Map findings to severity levels per `references/detection_patterns.md`
- Critical: AWS keys, private keys, JWT secrets
- High: Generic passwords, connection strings
- Medium: API keys (may be test data)
- Low: Potential secrets requiring manual review

**Step 2: False Positive Filtering**
- Apply baseline exclusions
- Apply allowlist patterns (placeholders, test data, docs)
- Mark filtered items as "excluded" with reason

**Step 3: Build Report**
- Group findings by severity
- Include file path, line number, pattern matched
- Do NOT include actual secret values in report

### Phase 4: Remediation Guidance

**Step 1: Attach Remediation Actions**
- For each finding, attach remediation steps from `references/remediation_guide.md`
- For Critical findings: emphasize immediate rotation requirement

**Step 2: Return Results**
- Return structured findings list to orchestrator
- Include summary: total scanned, total found, by severity

---

## Critical Rules

1. **Never log actual secret values** - redact in all outputs
2. **Treat any found secret as compromised** - rotation required for Critical
3. **Preserve baseline** - do not remove existing baseline entries
4. **Pre-commit priority** - recommend pre-commit hook if not configured
5. **Git history awareness** - warn if secret may exist in history (requires git-filter-repo)

---

## Definition of Done

- [ ] Scan completed using available tool or manual patterns
- [ ] Findings classified by severity
- [ ] False positives filtered via baseline/allowlist
- [ ] Remediation guidance attached to each finding
- [ ] Report returned in normalized format (no raw secret values)
- [ ] Critical findings flagged with rotation requirement

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/detection_patterns.md` | Secret patterns by confidence level |
| `references/gitleaks_config_template.toml` | Template for project gitleaks config |
| `references/remediation_guide.md` | Rotation procedures by secret type |

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
