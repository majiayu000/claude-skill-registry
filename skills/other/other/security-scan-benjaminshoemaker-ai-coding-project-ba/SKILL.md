---
name: security-scan
description: Scan for security vulnerabilities in dependencies, code patterns, and secrets. Uses project-documented tooling where available. Use at phase checkpoints or before releases to check for vulnerabilities.
---

# Security Scan Skill

Scan the codebase for security issues across three categories:
1. **Dependency vulnerabilities** — Known CVEs in packages
2. **Static analysis** — Insecure code patterns (per project tooling)
3. **Secrets detection** — API keys, passwords, tokens in code

## When This Skill Runs

- Automatically during `/phase-checkpoint`
- On-demand via `/security-scan`
- Optionally during `/verify-task` for security-critical tasks

## Workflow Overview

Copy this checklist and track progress:

```
Security Scan Progress:
- [ ] Step 1: Discover security tooling from project docs
- [ ] Step 2: Run dependency audit
- [ ] Step 3: Run secrets detection
- [ ] Step 4: Run static analysis
- [ ] Step 5: Aggregate and deduplicate findings
- [ ] Step 6: Present issues with severity
- [ ] Step 7: Offer to apply fixes
```

## Step 1: Discover Project Security Tooling

Read project documentation and task runners to find the correct commands:
- `README.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `Makefile`
- `Taskfile.yml`
- `justfile`
- Any security or build scripts under `scripts/`

Extract any documented commands for:
- Dependency auditing
- Static analysis / security scanning
- Secrets detection (if the project has a preferred tool)

If nothing is documented, ask the human to provide the correct commands.

## Step 2: Dependency Audit

- If a dependency audit command is documented or provided, run it.
- If no command is available, mark this check as SKIPPED and note it in the
  report.

## Step 3: Secrets Detection (Default)

Run a pattern-based secrets scan (stack-agnostic) unless the project documents
its own secrets tool. If a project-specific tool exists, use it instead.

### Patterns to Detect

| Pattern | Regex | Severity |
|---------|-------|----------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | CRITICAL |
| AWS Secret Key | `(?i)aws_secret_access_key\s*=\s*['"][^'"]+['"]` | CRITICAL |
| GitHub Token | `ghp_[a-zA-Z0-9]{36}` | CRITICAL |
| GitHub Token (old) | `github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}` | CRITICAL |
| Generic API Key | `(?i)(api[_-]?key|apikey)\s*[:=]\s*['"][a-zA-Z0-9]{20,}['"]` | HIGH |
| Generic Secret | `(?i)(secret|password|passwd|pwd)\s*[:=]\s*['"][^'"]{8,}['"]` | HIGH |
| Private Key | `-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----` | CRITICAL |
| JWT Token | `eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*` | HIGH |
| Slack Token | `xox[baprs]-[0-9a-zA-Z]{10,48}` | HIGH |
| Stripe Key | `sk_live_[0-9a-zA-Z]{24}` | CRITICAL |

### Directories to Skip

- `node_modules/`
- `.git/`
- `vendor/`
- `venv/`, `.venv/`, `env/`
- `dist/`, `build/`
- `*.min.js`, `*.bundle.js`
- Binary files

## Step 4: Static Analysis

- If a static analysis or security scanning command is documented or provided,
  run it.
- If no command is available, mark this check as SKIPPED and note it in the
  report.

## Step 5: Aggregate Findings

Collect all findings into a unified format:

```
SECURITY SCAN RESULTS
=====================

Scanned: {timestamp}
Checks Run: Dependencies | Secrets | Static Analysis

CRITICAL (N)
------------
[issue details]

HIGH (N)
--------
[issue details]

MEDIUM (N)
----------
[issue details]

LOW (N)
-------
[issue details]

Summary: {N} critical, {N} high, {N} medium, {N} low
```

## Step 6: Present Issues

For CRITICAL and HIGH issues, present interactively with resolution options.
If a fix command is documented, offer it as the primary option.

## Step 7: Propose Fixes

Propose fixes to the user. Do not apply fixes automatically — present each fix for user approval before making changes.

**For each fix, show a preview:**
- Display the proposed change (file, line, before/after)
- Ask for confirmation: "Apply this fix?" (Yes/Skip)
- Only modify files after explicit user confirmation

Apply fixes based on user choices:
- Use project-documented fix commands when available
- Otherwise, propose manual code changes and confirm before editing

## Output Format

### When called from /phase-checkpoint

Return a structured result:

```
Security Scan: PASSED | FAILED | PASSED WITH NOTES

Issues: X critical, Y high, Z medium
Fixed: N issues
Skipped: M checks (documented)

Blocking: Yes/No
```

### When called standalone

Show full report with all findings and options.

## Severity Definitions

| Severity | Meaning | Action |
|----------|---------|--------|
| CRITICAL | Exploitable vulnerability, exposed secrets | BLOCKS checkpoint |
| HIGH | Significant security risk | BLOCKS checkpoint |
| MEDIUM | Should be addressed | Note, doesn't block |
| LOW | Minor issue or informational | Note only |

## Tool Installation Notes

If required tools are missing, instruct the user to install them based on the
project's documentation or security policy.

## Error Handling

**If no project documentation is found:**
- Report: "No security tooling documentation found"
- Ask the user for the correct commands
- Proceed with default secrets detection (always available)

**If a security tool returns a non-zero exit code:**
- If output indicates findings (common for `npm audit`, `pip-audit`, etc.), treat as SUCCESS_WITH_FINDINGS
- Parse and report the findings; do NOT mark the check as FAILED
- If output indicates an execution error (crash, invalid args, config error), treat as FAILED
- Always continue with other checks and include the outcome in the final report

**If tool is not installed:**
- Report: "{tool} not found"
- Provide installation instructions if known
- Mark check as SKIPPED with reason
- Continue with available tools

**If secrets scan finds too many results (>100):**
- Truncate results with: "Showing first 100 of {N} findings"
- Suggest the user may have sensitive data that should be gitignored
- Recommend running on specific directories

**If project has no package manager (dependency scan N/A):**
- Mark dependency scan as NOT APPLICABLE
- Note: "No package.json, requirements.txt, go.mod, or similar found"
- Proceed with other checks

**If scan is interrupted:**
- Report partial results obtained
- Mark interrupted checks clearly
- Suggest re-running the scan

## Example Invocations

```bash
/security-scan              # Full scan
/security-scan --deps       # Dependencies only
/security-scan --secrets    # Secrets detection only
/security-scan --code       # Static analysis only
/security-scan --fix        # Auto-fix where possible
```
