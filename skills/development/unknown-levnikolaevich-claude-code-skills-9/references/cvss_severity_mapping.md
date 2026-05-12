# CVSS Severity Mapping Reference

<!-- SCOPE: CVSS severity level mapping ONLY. Contains score ranges, action requirements, blocking rules. -->

CVSS score to severity level mapping for dependency vulnerabilities.

---

## CVSS v3 Score Mapping

| CVSS Score | Severity | Action Required |
|------------|----------|-----------------|
| 9.0 - 10.0 | **Critical** | Immediate fix required, blocks CI |
| 7.0 - 8.9 | **High** | Fix within 48 hours |
| 4.0 - 6.9 | **Medium** | Fix within 1 week |
| 0.1 - 3.9 | **Low** | Fix when convenient |
| 0.0 | **None** | Informational only |

---

## Ecosystem-Specific Mappings

### npm audit

| npm Severity | CVSS Equivalent | Our Severity |
|--------------|-----------------|--------------|
| critical | 9.0+ | Critical |
| high | 7.0-8.9 | High |
| moderate | 4.0-6.9 | Medium |
| low | 0.1-3.9 | Low |

### NuGet

NuGet uses CVSS directly - apply standard mapping.

### pip-audit / safety

| OSV Severity | Our Severity |
|--------------|--------------|
| CRITICAL | Critical |
| HIGH | High |
| MODERATE / MEDIUM | Medium |
| LOW | Low |

---

## Severity Thresholds by Environment

| Environment | Fail Threshold | Warning Threshold |
|-------------|----------------|-------------------|
| Production | Critical | High |
| Staging | High | Medium |
| Development | None (warn all) | Low |

---

## Fix Priority Matrix

| Severity | Exploitability | Network Vector | Fix Priority |
|----------|----------------|----------------|--------------|
| Critical | High | Network | P0 (Immediate) |
| Critical | Low | Local | P1 (24h) |
| High | High | Network | P1 (24h) |
| High | Low | Any | P2 (48h) |
| Medium | Any | Any | P3 (1 week) |
| Low | Any | Any | P4 (Backlog) |

---

## Auto-Fix Guidelines

| Update Type | Auto-Fix Safe? | Notes |
|-------------|----------------|-------|
| Patch (x.x.Y) | Yes | Bug fixes only |
| Minor (x.Y.0) | Usually | May have new features |
| Major (Y.0.0) | No | Breaking changes possible |

**Safe auto-fix rule:** Only auto-fix patch and minor updates with no breaking changes documented.

---

**Version:** 1.0.0
**Last Updated:** 2026-02-05
