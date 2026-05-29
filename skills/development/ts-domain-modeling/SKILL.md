---
name: domain-modeling
description: Creates structured domain documentation with anatomy diagrams, entity schemas, and operation specs. Use when designing systems, after brainstorming, or documenting existing architecture.
---

# Domain Modeling

Structured documentation for system design. TypeScript-first schemas.

## Process

1. __Identify entities__ - Nouns in the domain (things with identity/state)
2. __Identify operations__ - Verbs (actions that transform state)
3. __Map relationships__ - How entities connect (1:1, 1:n)
4. __Define schemas__ - TypeScript interfaces for each entity
5. __Specify operations__ - Params interface + step-by-step behavior

## Document Structure

```
## Anatomy
### Diagram              ← Relationship overview (ASCII boxes + cardinality)
### Entities             ← Name | Description table
### Operations           ← Name | Description table
### Other Terms          ← Identifiers, enums, value types (optional)

## Entities
### <EntityName>
#### Schema              ← TypeScript interface
#### Data                ← Known instances (optional)

## Operations
### <operationName>      ← Params interface + numbered steps
```

## Anatomy Section

### Diagram

ASCII boxes with relationship cardinality.

```
┌─────────┐ 1:n  ┌─────────┐
│ <EntityA> │─────▶│ <EntityB> │
└─────────┘      └─────────┘
```

__Conventions:__

* `1:n` = one-to-many
* `1:1` = one-to-one
* Arrow direction = ownership/containment

### Entities Table

| Name           | Description                                 |
| -------------- | ------------------------------------------- |
| __EntityName__ | One-line description of what it represents. |

### Operations Table

| Name            | Description                           |
| --------------- | ------------------------------------- |
| `operationName` | One-line description of what it does. |

### Other Terms (optional)

For identifiers, enums, types that don't warrant full entity treatment:

| Name         | Description       |
| ------------ | ----------------- |
| __TermName__ | Brief definition. |

## Entities Section

One subsection per entity.

### Entity Template

#### Schema

```ts
interface EntityName {
  /** Property description. */
  propertyName: PropertyType
}
```

#### Data (optional)

When entity has known/enumerable instances:

```ts
const instances: EntityName[] = [
  {/* ... */},
]
```

## Operations Section

One subsection per operation. Params interface + numbered behavior steps.

### Operation Template

```ts
interface Params {
  /** Param description. */
  paramName: ParamType
}
```

1. First step
2. Second step
   * Sub-detail if needed
3. Return result

## Discriminated Unions

When an entity has variants:

```ts
type EntityName =
  | EntityNameVariantA
  | EntityNameVariantB

interface EntityNameVariantA {
  kind: 'a'
  /* variant-specific props */
}
```

## Output Location

`docs/design/<domain>-design.md` or `docs/plans/YYYY-MM-DD-<topic>-design.md`
