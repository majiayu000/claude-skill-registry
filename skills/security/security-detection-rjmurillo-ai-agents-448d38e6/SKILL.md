---
name: security-detection
description: Detect infrastructure and security-critical file changes to trigger security agent review recommendations ensuring proper security oversight for sensitive modifications.
license: MIT
metadata:
version: 1.0.0
model: claude-haiku-4-5
---

# Security Detection Utility

## Purpose

Detect infrastructure and security-critical file changes to trigger security agent review recommendations.

## Location

`.claude/skills/security-detection/`

## Available Scripts

| Script | Language | Usage |
|--------|----------|-------|
| `detect-infrastructure.ps1` | PowerShell | Windows/Cross-platform |
| `detect_infrastructure.py` | Python 3 | Cross-platform |

## Usage

### PowerShell

```powershell
# Analyze staged files
.\detect-infrastructure.ps1 -UseGitStaged

# Analyze specific files
.\detect-infrastructure.ps1 -ChangedFiles @(".github/workflows/ci.yml", "src/auth/login.cs")
```

### Python

```bash
# Analyze staged files
python detect_infrastructure.py --git-staged

# Analyze specific files
python detect_infrastructure.py .github/workflows/ci.yml src/auth/login.cs
```

## Output

When security-critical files are detected:

```text
=== Security Review Detection ===

CRITICAL: Security agent review REQUIRED

Matching files:
  [CRITICAL] .github/workflows/deploy.yml
  [HIGH] src/Controllers/AuthController.cs

Run security agent before implementation:
  Task(subagent_type="security", prompt="Review infrastructure changes")
```

When no matches:

```text
No infrastructure/security files detected.
```

## Risk Levels

| Level | Meaning | Action |
|-------|---------|--------|
| CRITICAL | Immediate security implications | Review REQUIRED |
| HIGH | Potential security impact | Review RECOMMENDED |

## Detected Patterns

### Critical (Review Required)

- CI/CD workflows (`.github/workflows/*`)
- Git hooks (`.githooks/*`, `.husky/*`)
- Authentication code (`**/Auth/**`, `**/Security/**`)
- Environment files (`*.env*`)
- Credentials and keys (`*.pem`, `*.key`, `*secret*`)

### High (Review Recommended)

- Build scripts (`build/**/*.ps1`, `scripts/**/*.sh`)
- Container configs (`Dockerfile*`, `docker-compose*`)
- API controllers (`**/Controllers/**`)
- App configuration (`appsettings*.json`)
- Infrastructure as Code (`*.tf`, `*.tfvars`, `*.bicep`)

## Integration

### Pre-commit Hook

Add to `.githooks/pre-commit`:

```bash
# Security detection (non-blocking warning)
if command -v python3 &> /dev/null; then
    python3 .claude/skills/security-detection/detect_infrastructure.py --git-staged
elif command -v pwsh &> /dev/null; then
    pwsh -File .claude/skills/security-detection/detect-infrastructure.ps1 -UseGitStaged
fi
```

### CI Integration

```yaml
- name: Check security-critical files
  run: python .claude/skills/security-detection/detect_infrastructure.py --git-staged
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (warning shown if matches found, non-blocking) |

The scripts are designed to be non-blocking warnings. They always exit 0 to avoid blocking commits or CI. The warning is informational only.

## Customization

Edit the pattern lists in either script to add or modify detection patterns:

- `CRITICAL_PATTERNS` / `$CriticalPatterns` - Review required
- `HIGH_PATTERNS` / `$HighPatterns` - Review recommended

## Related Documents

- [Infrastructure File Patterns](../../security/infrastructure-file-patterns.md)
- [Security Agent Capabilities](../../security/static-analysis-checklist.md)
- [Orchestrator Routing Algorithm](../../../docs/orchestrator-routing-algorithm.md)
