---
name: git-sensitive-scan
description: Run sensitive information scanning before commit. Use to check staged files for secrets, credentials, private keys, and local-only endpoints.
---

# Git Sensitive Scan

Use this skill before git commit to avoid leaking secrets or local/private environment information.

Run commands from repository root:
`E:\coding\TermLink`

## Workflow

1. Scan staged files:
```powershell
powershell -ExecutionPolicy Bypass -File ./scripts/git-sensitive-scan.ps1 -Staged
```

2. Scan specific files (optional):
```powershell
powershell -ExecutionPolicy Bypass -File ./scripts/git-sensitive-scan.ps1 -Files ./.claude/skills/android-local-build-debug/local-config.ps1
```

3. If a finding is intentional and safe, add marker `sensitive-scan:allow` on that line.

4. Commit only after scanner passes.

## Notes

1. Pre-commit hook calls this scanner automatically once `core.hooksPath=.githooks` is enabled.
2. `local-config.ps1` files should remain local and not be tracked by git.
