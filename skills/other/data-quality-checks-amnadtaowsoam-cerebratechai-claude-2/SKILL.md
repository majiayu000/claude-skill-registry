---
name: Data Quality Checks (Alias)
description: Alias skill path for data quality checks under data engineering; points to the canonical data reliability skill.
---

# Data Quality Checks

## Overview

This is an **alias skill** so docs can reference `53-data-engineering/data-quality-checks`. The canonical skill lives at `43-data-reliability/data-quality-checks`.

## Best Practices

- Validate at ingestion and before serving (two gates).
- Define SLAs/SLOs for data freshness and completeness.
- Fail fast on schema breaks; quarantine bad batches.

## Code Examples

```text
# Canonical reference:
43-data-reliability/data-quality-checks/SKILL.md
```

## Checklist

- [ ] Add schema checks (types, required fields)
- [ ] Add distribution/drift checks for critical features
- [ ] Add alerting + runbook for failures

## References

- Canonical skill: `43-data-reliability/data-quality-checks/SKILL.md`
