# CI Integration Guide

<!-- SCOPE: CI/CD pipeline vulnerability audit integration ONLY. Contains stage recommendations, GitHub Actions/GitLab CI guidance. -->
<!-- DO NOT add here: Audit workflow → ln-625-dependency-reuse-auditor SKILL.md, severity → references/cvss_severity_mapping.md -->

Guidelines for integrating vulnerability audits into CI/CD pipelines.

---

## Integration Points

| Stage | Purpose | Recommended |
|-------|---------|-------------|
| Pre-commit | Block commits with new vulns | Optional (may slow commits) |
| Pull Request | Audit on PR creation/update | **Yes** |
| Main branch | Audit on merge | **Yes** |
| Scheduled | Weekly full audit | **Yes** |
| Release | Audit before deploy | **Yes** |

---

## GitHub Actions Configuration

### Key Considerations

1. **Trigger events:** push, pull_request, schedule
2. **Fail thresholds:** Configure per environment
3. **Caching:** Cache dependencies for faster runs
4. **Parallel jobs:** Audit each ecosystem in parallel
5. **SARIF upload:** Enable GitHub Security tab integration

### Workflow Structure

```
name: Security Audit
on: [push, pull_request, schedule (weekly)]

jobs:
  npm-audit:    (if package.json exists)
  dotnet-audit: (if *.csproj exists)
  pip-audit:    (if requirements.txt exists)
```

---

## Severity Threshold Configuration

| CI Stage | Recommended Threshold | Behavior |
|----------|----------------------|----------|
| PR checks | `--audit-level=high` | Fail on High/Critical |
| Main branch | `--audit-level=critical` | Fail only on Critical |
| Scheduled | `--audit-level=low` | Report all (no fail) |

---

## Handling False Positives

### npm

Use `.nsprc` or `audit-ci` config to ignore specific advisories:
- Document reason for each ignore
- Review ignores quarterly
- Remove when fix available

### .NET

Use `<NoWarn>` in csproj for specific packages:
- Only for packages without fix
- Add comment with CVE ID

### Python

Use `.safety-policy.yml` or `pip-audit` ignore file:
- Specify exact package@version
- Add expiration date for review

---

## SBOM Generation

### Benefits
- Compliance requirement (Executive Order 14028)
- Dependency transparency
- Incident response readiness

### Tools
- `npm sbom` (npm 9+)
- `dotnet CycloneDX`
- `pip-sbom` or `cyclonedx-py`

### Recommended Format
- CycloneDX (OWASP standard)
- SPDX (Linux Foundation standard)

---

## Notification Strategy

| Finding | Notification |
|---------|--------------|
| Critical in main | Slack/Teams alert + email |
| High in main | Daily digest |
| Any in PR | PR comment |
| Scheduled scan | Weekly report |

---

## Metrics to Track

| Metric | Purpose |
|--------|---------|
| Mean Time to Remediate (MTTR) | Security responsiveness |
| Vulnerability density | Per 1000 LOC or per package |
| False positive rate | Audit accuracy |
| Outdated dependency % | Technical debt indicator |

---

**Version:** 1.0.0
**Last Updated:** 2026-02-05
