# Release Readiness Reporting

## Purpose

Release readiness reporting gives maintainers a short, reproducible summary of
the generated main artifact after core and data have been published together.
It is not a publish gate.

## Report-Only Checks

Run:

```bash
python scripts/build_publish_readiness_report.py \
  --main-dir ../claude-skill-registry \
  --output-json /tmp/publish-readiness.json
```

The report reads:

- `docs/stats.json`
- `docs/categories/other/manifest.json`
- `registry-manifest.json`
- `provenance/merge-source.json`
- `provenance/publish-status.json`

It summarizes the current `other` count, raw archive counts, deduped registry
count, provenance tuple, publish-status checks, and manifest consistency.

## Residual Governance

Run:

```bash
python scripts/build_other_residual_governance_report.py \
  --skills-dir ../claude-skill-registry/skills \
  --output-json /tmp/other-residual-governance.json
```

The residual report groups current `other` skills into:

- `security_failed`
- `structure_review`
- `semantic_review_candidate`
- `low_context`
- `manual_taxonomy_review`

These buckets are review queues. They are not automatic migrations and do not
block publish.

## Deferred Gate Discussion

An `other` count or growth threshold may be useful later, but it should remain
an issue-level discussion until maintainers explicitly choose to make it a
publish blocker.
