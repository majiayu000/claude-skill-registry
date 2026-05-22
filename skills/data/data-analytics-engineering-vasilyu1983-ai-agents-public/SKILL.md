---
name: data-analytics-engineering
description: Analytics engineering for reliable metrics and BI readiness. Build transformation layers, dimensional models, semantic metrics, data quality tests, and documentation. Use when you need dbt or SQL transformation strategy, metrics definition, or analytics data modeling.
---

# Data Analytics Engineering

## Scope

- Define metrics, grains, and dimensional models.
- Build transformation layers and semantic models.
- Implement data quality tests and observability.
- Document datasets, lineage, and ownership.
- Align analytics outputs with BI and product needs.

## Ask For Inputs

- Business metrics and decision use cases.
- Source systems, data freshness, and latency needs.
- Existing warehouse, tooling, and orchestration.
- Expected data volumes and change cadence.
- Governance requirements and access controls.

## Workflow

1. Define metric dictionary and grains.
2. Design staging, intermediate, and mart layers.
3. Model dimensions and facts with clear keys.
4. Build semantic layer and metric definitions.
5. Add tests for freshness, nulls, ranges, and duplicates.
6. Document lineage, owners, and SLAs.
7. Plan rollout, backfills, and validation checks.

## Outputs

- Metric dictionary and semantic model.
- Data model with schema and grain definitions.
- Transformation plan and dbt or SQLMesh structure.
- Data quality test suite and alerting plan.
- Documentation and ownership map.

## Quality Checks

- Keep metric definitions stable and versioned.
- Avoid mixed grains in a single model.
- Ensure tests cover critical joins and aggregates.
- Validate against source of truth and historical baselines.

## Templates

- `templates/metric-dictionary.md` for metric definitions and owners.
- `templates/semantic-layer-spec.md` for entities, measures, and dimensions.
- `templates/data-quality-test-plan.md` for test coverage planning.

## Resources

- `resources/modeling-patterns.md` for modeling guidance.

## Related Skills

- Use [data-lake-platform](../data-lake-platform/SKILL.md) for platform architecture.
- Use [data-sql-optimization](../data-sql-optimization/SKILL.md) for query tuning.
- Use [ai-ml-data-science](../ai-ml-data-science/SKILL.md) for modeling and experiments.
