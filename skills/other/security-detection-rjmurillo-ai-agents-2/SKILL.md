---
name: security-detection
description: Detect infrastructure and security-critical file changes to trigger security agent review recommendations ensuring proper security oversight for sensitive modifications.
license: MIT
metadata:
version: 1.0.0
model: claude-haiku-4-5
---

# Security Detection Utility

## Triggers

| Trigger Phrase | Operation |
|----------------|-----------|
| `scan for security changes` | detect-infrastructure with staged files |
| `check security-critical files` | detect-infrastructure with file list |
| `run security scan on changes` | detect-infrastructure analysis |
| `do I need a security review` | Risk-level assessment of changed files |
| `check infrastructure changes` | Pattern matching against critical/high lists |

---

## When to Use

Use this skill when:

- Committing changes that may touch infrastructure or security files
- Pre-commit validation for security-sensitive paths
- Determining if a security agent review is needed
- CI pipeline security gate checks

Use the security agent directly instead when:

- You already know security review is needed
- Performing threat modeling or vulnerability assessment
- Reviewing authentication or authorization code in depth

---

## Available Scripts

| Script | Language | Usage |
|--------|----------|-------|
| `detect_infrastructure.py` | Python 3 | Cross-platform |

## Usage

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

## Process

1. Gather the list of changed files (staged or explicit)
2. Run pattern matching against critical and high-risk file patterns
3. Report findings with risk level classification
4. Route to security agent if CRITICAL matches found

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Skipping detection before commits | Security files slip through unreviewed | Run detection on every commit with infrastructure changes |
| Treating warnings as blocking | Scripts exit 0 intentionally | Use output to inform review decisions, not block commits |
| Hardcoding custom patterns inline | Drifts from canonical pattern lists | Edit CRITICAL_PATTERNS/HIGH_PATTERNS in the scripts |
| Ignoring HIGH-level matches | Potential security impact overlooked | Review HIGH matches, escalate to security agent when uncertain |
| Running only one language script | May miss platform-specific detection | Use whichever script matches your environment |

---

## Verification

After running security detection:

- [ ] Script exited with code 0 (non-blocking)
- [ ] All CRITICAL matches reviewed
- [ ] Security agent routed for CRITICAL findings
- [ ] HIGH matches evaluated for review need
- [ ] Output captured in session log if security-relevant

---

## Related Documents

- [Infrastructure File Patterns](../../security/infrastructure-file-patterns.md)
- [Security Agent Capabilities](../../security/static-analysis-checklist.md)
- [Orchestrator Routing Algorithm](../../../docs/orchestrator-routing-algorithm.md)
