---
name: specstory-guard
description: Install a pre-commit hook that scans .specstory/history for secrets before commits. Run when user says "set up secret scanning", "install specstory guard", "protect my history", or "check for secrets".
license: Apache-2.0
metadata:
  author: SpecStory, Inc.
  version: "1.0.0"
  argument-hint: "[install|scan|check|uninstall] [--root PATH]"
allowed-tools: Bash, Read, Write
---

# SpecStory Guard

A pre-commit guardrail that scans `.specstory/history` for potential secrets and blocks commits until they are removed or redacted.

## How It Works

1. **Installs** a git pre-commit hook in your repository
2. **Scans** `.specstory/history` files on every commit
3. **Detects** common secret patterns (API keys, tokens, private keys)
4. **Blocks** the commit if secrets are found
5. **Reports** findings with redacted previews for safe review

## Why Use Guard?

AI coding sessions may inadvertently capture sensitive data:
- API keys you pasted into chat
- Environment variables in command output
- Private keys or tokens in error messages
- Credentials in configuration examples

Guard prevents accidental commits of these secrets.

## Usage

### Slash Command

| User says | Action |
|-----------|--------|
| `/specstory-guard` | Install the pre-commit hook |
| `/specstory-guard install` | Install the pre-commit hook |
| `/specstory-guard scan` | Run a manual scan without installing |
| `/specstory-guard check` | Alias for scan |
| `/specstory-guard uninstall` | Remove the pre-commit hook |

### Direct Script Usage

```bash
# Install the pre-commit hook
python skills/specstory-guard/scripts/guard.py install

# Run a manual scan
python skills/specstory-guard/scripts/guard.py scan --root .

# Uninstall the hook
python skills/specstory-guard/scripts/guard.py uninstall

# Scan with custom allowlist
SPECSTORY_GUARD_ALLOWLIST='example-key,PLACEHOLDER_.*' \
  python skills/specstory-guard/scripts/guard.py scan --root .
```

## Output

### Scan with findings:

```
SpecStory Guard - Security Scan
===============================

Scanning .specstory/history/...

ALERT: Potential secrets found!

File: .specstory/history/2026-01-22_19-20-56Z-api-setup.md
  Line 142: AWS_SECRET_ACCESS_KEY=AKIA...redacted...XYZ
  Line 289: private_key: "-----BEGIN RSA PRIVATE KEY-----..."

File: .specstory/history/2026-01-20_10-15-33Z-debug-auth.md
  Line 56: Authorization: Bearer eyJhbG...redacted...

Total: 3 potential secrets in 2 files

Commit blocked. Please redact or remove these secrets before committing.
```

### Clean scan:

```
SpecStory Guard - Security Scan
===============================

Scanning .specstory/history/...

All clear! No secrets detected in 47 files.
```

### Installation success:

```
SpecStory Guard - Setup
=======================

Pre-commit hook installed at .git/hooks/pre-commit

The hook will now scan .specstory/history/ before each commit.
To test: python skills/specstory-guard/scripts/guard.py scan --root .
```

## Detected Patterns

Guard scans for these common secret patterns:

| Pattern | Example |
|---------|---------|
| AWS Keys | `AKIA...`, `aws_secret_access_key` |
| API Tokens | `Bearer ...`, `token: ...` |
| Private Keys | `-----BEGIN RSA PRIVATE KEY-----` |
| GitHub Tokens | `ghp_...`, `github_pat_...` |
| Generic Secrets | `password=`, `secret=`, `api_key=` |

## Tuning with Allowlist

If you have false positives (example keys, placeholders), use the allowlist:

```bash
# Environment variable (comma-separated regex patterns)
SPECSTORY_GUARD_ALLOWLIST='example-key,PLACEHOLDER_.*,test-token' \
  python skills/specstory-guard/scripts/guard.py scan --root .
```

## Remediation

When secrets are found:

1. **Open the file** - Find the line number from the report
2. **Redact the secret** - Replace with `[REDACTED]` or remove the line
3. **Re-run scan** - Verify the fix with another scan
4. **Commit** - The pre-commit hook will pass

## Present Results to User

After running guard commands:

1. **For install** - Confirm the hook is installed and explain what it does
2. **For scan with findings** - List the findings and offer to help redact them
3. **For clean scan** - Confirm no secrets were found

### Example Response (findings)

```
I found 3 potential secrets in your SpecStory history:

1. **AWS credentials** in `2026-01-22_19-20-56Z-api-setup.md` (line 142)
2. **Private key** in the same file (line 289)
3. **Bearer token** in `2026-01-20_10-15-33Z-debug-auth.md` (line 56)

Would you like me to help redact these? I can replace them with `[REDACTED]`
while preserving the rest of the conversation context.
```

## Notes

- Uses no external dependencies (pure Python)
- Hook runs automatically on `git commit`
- Scan is fast - typically under 1 second for hundreds of files
- Allowlist patterns are regular expressions
