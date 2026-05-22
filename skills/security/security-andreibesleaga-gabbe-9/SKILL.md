---
name: safety-scan
description: Active Security Enforcement. Scans code for vulnerabilities (SAST), secrets (Gitleaks), and insecure dependencies (SCA) before commit/deployment.
triggers: [scan security, check vulnerabilities, audit code, gitleaks, semgrep, finding secrets]
context_cost: medium
---

# Safety Scan Skill

## Goal
Prevent "Insecure Code" from entering the codebase by strictly enforcing security checks.

## Flow

### 1. Credentials Check (Gitleaks)
**Command**: `gitleaks detect --source . -v` (or regex fallback)
**Check**: Are there API Keys, Tokens, or Passwords in the diff?
*   *If Found*: **BLOCK COMMIT**. Auto-delete or `.gitignore` the secret. Alert Human.

### 2. Static Analysis (SAST)
**Command**: `semgrep scan --config=p/security-audit` (if installed) OR `npm audit` / `pip-audit`.
**Check**: High-Severity vulnerabilities (RCE, SQLi, XSS).
*   *If Found*: **BLOCK COMMIT**. Invoke `ci-autofix` to patch.

### 3. Logic & PII Check
**Action**: LLM Review of the diff.
*   "Does this code log User PII?"
*   "Does this code execute arbitrary system commands (`exec`, `eval`)?"
*   *If Risky*: Add `# TODO: SECURITY REVIEW` comment and flag in `project/tasks.md`.

## Output
*   **PASS**: "No critical issues found."
*   **FAIL**: "Blocking Commit. Found [N] Issues."
