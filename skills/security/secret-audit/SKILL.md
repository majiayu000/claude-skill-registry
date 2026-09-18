---
name: secret-audit
description: Use when the user asks whether secrets were committed, before open-sourcing a repo, or after a leak scare. Scans the working tree and full git history for credentials, reports findings with commit and path, and gives a remediation plan (rotate first, then purge).
---

# secret-audit

## Procedure
1. Tooling: prefer `gitleaks git --report-format json --report-path /tmp/gitleaks.json .` if `command -v gitleaks` succeeds (`detect` is deprecated since gitleaks 8.19; on an older gitleaks use `gitleaks detect --source .`); else `trufflehog git file://. --json`; else fall back to grep over `git log -p --all` with the pattern set below.
2. Fallback pattern set (grep -E): `AKIA[0-9A-Z]{16}`, `sk-(live|test|proj|ant)-[A-Za-z0-9_-]{16,}`, `gh[pousr]_[A-Za-z0-9]{30,}`, `xox[abpr]-`, `-----BEGIN [A-Z ]*PRIVATE KEY-----`, `eyJ[A-Za-z0-9_-]{20,}\.eyJ`, `(?i)(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*["'][^"']{12,}["']`, plus `.env`, `*.pem`, `*.p12`, `id_rsa` filenames in history: `git log --all --diff-filter=A --name-only --format='' | grep -E '(^|/)(\.env|.*\.pem|.*\.p12|id_rsa)$'`.
3. Deduplicate; for each finding record `path | first commit (sha, date, author) | still in HEAD? | type`.
4. Classify: **live in HEAD** (critical), **only in history** (high), **example/test/false positive** (note, no action).
5. Remediation plan, in this order, as a checklist for the user:
   1. Rotate every credential found (it is compromised once committed, even if purged).
   2. Remove from HEAD: move to env/`.env` (gitignored), commit.
   3. Purge history only if the repo is/will be public or shared: `git filter-repo --path <file> --invert-paths` or `--replace-text`, then force-push with `--force-with-lease` and tell collaborators to re-clone. Do not run this without explicit approval.
   4. Add prevention: `.gitignore` entries, pre-commit hook (`gitleaks git --pre-commit --staged .`; `protect --staged` on gitleaks older than 8.19), and this plugin's `secret-scan` hook.
6. Print the findings table and the checklist. Never print full secret values; mask to first 4 + last 2 chars. That includes notes: when a value matches a known placeholder (the AWS docs example key, a vendor's sample token), say so by name and keep the masked form, never the full string.

## Rules
- Never rewrite history or force-push in this skill; propose only.
- Never paste unmasked secrets into the transcript.

## Eval
`evals/secret-audit/`: fixture repo where a `.env` with a fake AWS key was committed then deleted two commits later; expected: finding reported as "only in history" with the introducing sha, value masked, rotate-first plan, no history rewrite executed.
