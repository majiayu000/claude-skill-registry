---
name: _workflow-data-pipeline
description: Lifecycle for building data pipelines, analytics engineering, and data quality checks. Follow the phases sequentially.
---

# Workflow Data Pipeline

Lifecycle for building data pipelines, analytics engineering, and data quality checks.

This is a **Workflow** skill. When executing this lifecycle, you should progress through the phases sequentially. For each phase, invoke or refer to the specific sub-skills that are contextually relevant to the project's language or framework.

## Lifecycle Phases

### 1. Storage & Ingestion
- [postgresql](../postgresql/SKILL.md)
- [api-design-principles](../api-design-principles/SKILL.md)
- [async-python-patterns](../async-python-patterns/SKILL.md)

### 2. Analytics Engineering & Transformation
- [dbt-transformation-patterns](../dbt-transformation-patterns/SKILL.md)
- [pandas-specialist](../pandas-specialist/SKILL.md)
- [numpy-specialist](../numpy-specialist/SKILL.md)

### 3. Quality & Contracts
- [data-quality-frameworks](../data-quality-frameworks/SKILL.md)
- [test-driven-development](../test-driven-development/SKILL.md)

### 4. Visualization & Storytelling
- [data-storytelling](../data-storytelling/SKILL.md)
- [grafana-dashboards](../grafana-dashboards/SKILL.md)
