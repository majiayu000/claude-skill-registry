---
name: sea-dsl-authoring
description: Author SEA-DSL specifications with proper CQRS annotations and validation.
tags: [semantic-core, authoring, sea-dsl]
inputs:
  files:
    - docs/specs/semantic-core/reference/001-sbvr-ubm-dsl-specification.md
    - docs/reference/sea_dsl_language_reference.yml
  concepts: [sea-dsl, policies, flows, entities]
  tools: [toolset:write]
---

# SEA-DSL Authoring Skill

Guides users through authoring semantically valid SEA-DSL files.

## Prerequisites

Before authoring SEA-DSL, understand:
- SEA-DSL grammar from `sea_dsl_language_reference.yml`
- CQRS annotation requirements from `flow_lint.py`
- Namespace conventions and bounded context boundaries

## Workflow

1. **Draft**: Create `.sea` file with proper namespacing
2. **Annotate**: Add required annotations to all Flows
3. **Validate**: Run `just sea-validate <file>`
4. **Parse**: Run `just sea-parse <file>` to generate AST
5. **Lint**: Run `just flow-lint` to verify annotations

## Required Annotations

Every Flow MUST have:
```sea
@cqrs { "kind": "command" | "query" | "event" }
```

Commands MUST have:
```sea
@tx { "transactional": true | false }
```

Events MUST have:
```sea
@outbox { "mode": "required" | "optional" }
```

## Rules

- Use nested JSON only (no dotted keys like `@cqrs.kind`)
- All JSON must be valid
- Never claim success without validation passing
- Follow namespace conventions: `system.<context>.<name>`

## Example

```sea
@namespace "system.orders"
@version "1.0.0"

Entity "Order" in system.orders

Flow "CreateOrder" from "Customer" to "OrderAggregate"
  @cqrs { "kind": "command" }
  @tx { "transactional": true }
  @idempotency { "enabled": true, "key": "orderId" }
```

## Related Skills

- [sea-flow-annotations](../sea-flow-annotations/SKILL.md)
- [spec-authoring](../spec-authoring/SKILL.md)
