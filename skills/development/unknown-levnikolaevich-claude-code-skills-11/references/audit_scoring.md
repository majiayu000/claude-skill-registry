<!-- SOURCE-OF-TRUTH: shared/references/audit_scoring.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Audit Scoring Algorithm

Mandatory scoring contract for audit workers.

## Formula

```text
penalty = (critical x 2.0) + (high x 1.0) + (medium x 0.5) + (low x 0.2)
score = max(0, 10 - penalty)
```

## Weights

| Severity | Weight | Use for |
|----------|--------|---------|
| CRITICAL | 2.0 | Security vulnerabilities, data loss, RFC/standard violations |
| HIGH | 1.0 | Architecture violations, CVE dependencies, blocking bugs |
| MEDIUM | 0.5 | Best-practice violations, code smells, minor performance issues |
| LOW | 0.2 | Style issues, minor inconsistencies, cosmetic problems |

## Score Bands

| Score | Action |
|-------|--------|
| 10 | No action |
| 8-9 | Low-priority fixes |
| 6-7 | Next-sprint fixes |
| 4-5 | Prioritized fixes |
| 1-3 | Immediate action |

Optional diagnostic sub-scores (`compliance`, `completeness`, `quality`, `implementation`) are informational only; the primary `score` always uses the formula above.

---
**Version:** 2.0.0
**Last Updated:** 2026-03-01
