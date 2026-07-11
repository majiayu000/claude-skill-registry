---
name: 055-design-parallel-change
description: Use when a database schema or data-meaning change needs Parallel Change, including expand, migrate, and contract sequencing for column renames, type or data reinterpretation, large-table backfills, relationship-table changes, enum/status transitions, timezone/default changes, and index or uniqueness changes. This should trigger before framework-specific Flyway implementation guidance when deciding whether a migration needs a compatibility window or whether a simpler migration is sufficient. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.17.0
---
# Parallel Change Design

Guide Java Enterprise developers through Parallel Change for database migration scenarios. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Deciding whether a database migration needs a compatibility window
- Sequencing database changes as expand, migrate, and contract deployable steps
- Preserving old and new application versions during rollout and rollback windows
- Handling column renames, type or data reinterpretation, large backfills, relationship-table changes, and index or uniqueness changes
- Explaining tradeoffs such as temporary dual paths, extra migrations, verification effort, and delayed cleanup
- Routing framework-specific implementation to Spring Boot, Quarkus, or Micronaut Flyway skills after the design approach is clear

## Constraints

Use Parallel Change as a database migration design pattern, then hand off implementation details to the framework-specific migration skill when needed.

- **MUST** read `references/055-design-parallel-change.md` before applying Parallel Change guidance
- **MUST** explain expand, migrate, and contract as separate deployable steps when recommending Parallel Change
- **MUST** decide whether Parallel Change is needed before recommending framework-specific Flyway implementation details
- **MUST** recommend a simpler single migration when the change is additive, immediately safe, and does not require old and new application versions to coexist
- **MUST** describe the compatibility, data-preservation, verification, and cleanup tradeoffs of the chosen approach
- **MUST** use framework-specific Flyway skills for Spring Boot, Quarkus, or Micronaut implementation details after the migration strategy is selected

## When to use this skill

- Apply Parallel Change to this database migration
- Use expand migrate contract for this schema change
- Plan a safe column rename migration
- Plan a zero-downtime database migration
- Should this Flyway migration use Parallel Change?
- Design a safe backfill and contract migration
- Decide if this schema change needs a compatibility window

## Workflow

1. **Classify the Migration Risk**

Read `references/055-design-parallel-change.md`, then identify the schema shape, data meaning, application read/write path, rollout window, rollback expectation, and production-data risk affected by the migration.

2. **Choose Parallel Change or Simpler Migration**

Recommend Parallel Change when old and new application versions or data interpretations must coexist. Recommend a simpler forward-only migration when the change is additive, small, immediately safe, and does not require a compatibility window.

3. **Design Expand, Migrate, Contract**

For Parallel Change, separate expand, migrate, and contract into independently deployable steps. Keep the old shape valid during expand and migrate; contract only after all deployed code and data have moved to the new shape.

4. **Plan Verification and Operations**

Define previous-release fixture checks, row-count expectations, duplicate detection, backfill monitoring, rollback behavior, and cleanup ownership. Prefer production-dialect migration tests and production-like data samples where feasible.

5. **Route Framework Implementation**

After the strategy is clear, use `313-frameworks-spring-db-migrations-flyway`, `413-frameworks-quarkus-db-migrations-flyway`, or `513-frameworks-micronaut-db-migrations-flyway` for framework-specific Flyway dependencies, configuration, migration locations, and tests.

6. **Report the Migration Plan**

Report the chosen approach, rejected alternative, expand/migrate/contract sequence or simpler migration, verification evidence, cleanup trigger, tradeoffs, skipped checks, and remaining risks.

## Reference

For detailed guidance, examples, and constraints, see [references/055-design-parallel-change.md](references/055-design-parallel-change.md).
