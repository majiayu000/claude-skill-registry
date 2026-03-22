---
name: security
description: "Use when scanning for security vulnerabilities: SAST, dependency audit, secret detection, and SBOM generation with OWASP mapping and CWE references."
effort: max
argument-hint: "all|static|deps|secrets|sbom|--fix"
tags: [security, sast, dependencies, sbom, owasp, enterprise]
requires:
  bins:
  - gitleaks
  - semgrep
---



# Security Scanning

Unified security assessment for regulated industries. Modes: `static` (SAST with semgrep), `deps` (pip-audit/npm audit), `secrets` (gitleaks), `sbom` (CycloneDX). Zero tolerance for medium+ findings. Each finding includes severity, location, fix suggestion, and CWE reference.

## When to Use

- Security review, pre-release gate, dependency audit, compliance reporting.
- NOT for code quality metrics -- use `/ai-quality`.
- NOT for governance compliance -- use `/ai-governance`.

## Modes

### static -- SAST

1. **Detect stacks** -- read project files for active languages.
2. **Secret detection** -- `gitleaks detect --source . --no-git`. Any finding is critical.
3. **Semgrep** -- `semgrep scan --config auto --json`. Parse for rule IDs, severity, CWE.
4. **Manual analysis** -- review what tools miss:
   - Authentication on every endpoint (A01)
   - Parameterized queries only (A03)
   - Secrets from env/vault, never hardcoded (A02)
   - HTTP security headers (A05)
   - No user-controlled URLs in HTTP clients (A10)
5. **Classify** -- severity + OWASP category per finding.

### deps -- Dependency Audit

1. **Detect lock files** -- `uv.lock`, `package-lock.json`, `Cargo.lock`, `*.csproj`.
2. **Run audit** -- Python: `pip-audit --strict --desc`. Node: `npm audit --json`. Rust: `cargo audit --json`.
3. **Assess exploitability** -- mark unreachable paths as reduced severity with justification.
4. **Report** with upgrade paths.

### secrets -- Secret Detection

1. **Full scan** -- `gitleaks detect --source . --no-git --report-format json`.
2. **Staged scan** -- `gitleaks protect --staged --no-banner`.
3. **For each finding**: file, line, rule, remediation (rotate credential, store in vault).

### sbom -- Software Bill of Materials

1. **Generate** -- `cdxgen -o sbom.json --spec-version 1.5` (CycloneDX JSON).
2. **Validate** -- all direct deps with versions, license info, package URLs.
3. **Flag license risks** -- copyleft (GPL, AGPL) conflicting with project license.

### `--fix` -- Auto-fix

When `--fix` is passed, attempt automatic remediation:
- Secrets: remove from source, add to `.gitignore`, warn to rotate.
- Dependencies: `pip install --upgrade <pkg>` for fixable vulns.
- Lint findings: `semgrep --autofix` where rules support it.
- Report what was fixed and what requires manual intervention.

## Severity Classification

| Severity | Definition | Gate Impact |
|----------|-----------|-------------|
| Blocker | Actively exploitable, breach imminent | Blocks release |
| Critical | High-impact, exploit feasible | Blocks release |
| Major | Significant risk, requires conditions | Resolve before next release |
| Minor | Low risk, defense-in-depth | Resolve during maintenance |

## Output Contract

```markdown
# Security Report: [mode]

## Score: N/100
## Verdict: PASS (>=80) | WARN (60-79) | FAIL (<60)

## Findings
| # | Severity | OWASP | CWE | Description | Location | Fix |
|---|----------|-------|-----|-------------|----------|-----|

## Tool Outputs
- gitleaks: [N findings / clean]
- semgrep: [N findings / clean]
- pip-audit: [N findings / clean]
```

## Quick Reference

```
/ai-security              # run all modes
/ai-security static       # SAST only
/ai-security deps         # dependency audit only
/ai-security secrets      # secret detection only
/ai-security sbom         # generate SBOM
/ai-security deps --fix   # audit + auto-fix
```

## Common Mistakes

- Suppressing findings with `# nosec` -- fix the root cause or use risk acceptance.
- Ignoring transitive dependency vulns -- they are still exploitable.
- Running `gitleaks detect` on the full repo for pre-commit -- use `gitleaks protect --staged`.

## Integration

- Pre-commit hook runs `gitleaks protect --staged` automatically.
- Pre-push hook runs `semgrep` and `pip-audit`.
- Release gate (`/ai-release`) aggregates security results.
- Risk acceptances go to `state/decision-store.json` via `/ai-governance risk`.

## References

- `.ai-engineering/contexts/frameworks/` -- security and OWASP control mapping.
- `.ai-engineering/manifest.yml` -- non-negotiables and gate thresholds.
$ARGUMENTS
