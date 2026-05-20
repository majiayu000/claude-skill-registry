---
name: declaration-contract-design
description: "Use when declaration contracts need design or refactoring decisions across signatures, type shapes, schemas, or generic parameters. Goal: declaration contracts are explicit, coherent, and stable at use sites."
---

# Declaration Contract Design

Design or refactor declaration contracts using a Name plus Shape view so meaning stays explicit and the shape remains stable at use sites.

## Response Contract

- Deliverable: apply the requested changes to the target artifact.
- Chat output: no additional output beyond the deliverable.

## Skill Model

Definitions used to reason about declaration shape decisions.

### Grouping

Grouping is how a declaration organizes elements into conceptual blocks. A shape reflects the grouping decisions that were made.

### Addressing Modes

A declaration’s shape is addressed in one of two modes.

- **Named shape**
  Elements are addressed by name.

- **Positional shape**
  Elements are addressed by position.

## Standards

Each standard is defined once here and referenced elsewhere by its ID.

- **name.meaning — Name states meaning**
  Choose names that communicate domain meaning rather than implementation detail.

- **contract.core.explicit — Core meaning is explicit**
  Keep meaning-defining elements explicit in the declaration shape. Do not hide them inside unmodeled containers or convenience wrappers.

### Grouping

- **grouping.modeled_only — Grouping is a modeled concept**
  Introduce a group only when the group itself is a nameable concept with a stable semantic boundary.

- **grouping.no_catch_all — No catch-all groups**
  Do not use groups whose purpose is only to absorb leftovers or unrelated concerns.

### Positional shape

- **positional.role.anchor — Anchor role**
  Identifies the primary subject, such as a target, id, path, key.

- **positional.role.core — Core role**
  Required information that defines the primary semantic variation.

- **positional.role.policy — Policy role**
  Optional strategy and tuning that changes behavior without changing the subject.

- **positional.role.observability — Observability role**
  Diagnostics and tracing concerns.

- **positional.order.gradient — Order follows stability gradient**
  In positional shape, order elements by role: Anchor, Core, Policy, Observability.

- **positional.prefix.stable — Stable prefix discipline**
  Treat Anchor and Core as a stable prefix. After publication, do not reorder the stable prefix. Only append new positional elements at the tail.

### Callable declarations

- **callable.split — Split by role**
  When a callable uses both modes and the language supports named arguments, keep Anchor and Core in the positional segment and express Policy and Observability through named mechanisms.

- **callable.options.modeled — Options are modeled**
  If a callable introduces an options or config argument, it must be a modeled concept under `grouping.modeled_only` and must not become a catch-all under `grouping.no_catch_all`.

### Parameterized declarations

- **generics.semantic_order — Order by semantic progression**
  Order generic or type parameters by semantic progression: meaning-defining parameters first, constrained parameters later, and defaulted parameters at the end.

## Workflow

1. Identify the declaration kind and the meaning the contract must communicate. Apply `name.meaning` and `contract.core.explicit`.
2. Decide grouping boundaries if any. Apply `grouping.modeled_only` and `grouping.no_catch_all`.
3. Choose addressing mode for the shape or for shape segments.
4. If any segment is positional, assign roles and order by the stability gradient. Apply `positional.role.*`, `positional.order.gradient`, `positional.prefix.stable`.
5. Apply kind-specific standards.

   - Data-shape: no additional family beyond the base standards already applied.
   - Callable: apply `callable.*`.
   - Parameterized: apply `generics.*`.
6. Run acceptance checks.

## Acceptance Criteria

A revision is complete only if all checks pass.

- **Response**: Output satisfies the Response Contract.
- **Standards satisfied**:

  - Data-shape: `name.meaning`, `contract.core.explicit`, plus `grouping.*` when grouping is introduced, and `positional.*` when positional shape is used.
  - Callable: `name.meaning`, `contract.core.explicit`, `callable.*`, plus `grouping.*` when grouping is introduced, and `positional.*` when positional shape is used.
  - Parameterized: `contract.core.explicit`, `generics.*`, plus `positional.*` when positional shape is used.
