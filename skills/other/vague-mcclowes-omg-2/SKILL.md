---
name: vague
# prettier-ignore
description: Use when writing Vague (.vague) files - a declarative language for generating realistic test data with superposition, constraints, and cross-references
---

# Vague Language

## Quick Start

```vague
schema Invoice {
  id: unique int in 1000..9999,
  status: "draft" | "sent" | "paid",
  total: decimal in 100.00..5000.00,
  line_items: 1..5 of LineItem,
  tax: round(total * 0.2, 2),
  assume total > 0
}

dataset TestData {
  invoices: 100 of Invoice
}
```

## Core Syntax

- **Types**: `string`, `int`, `decimal`, `boolean`, `date`
- **Superposition**: `"a" | "b"` or weighted `0.7: "a" | 0.3: "b"`
- **Ranges**: `int in 1..100`, `date in 2020..2024`
- **Collections**: `1..5 of Item` or `100 of Item`
- **Computed**: `total: sum(items.amount)`, `median()`, `first()`, `last()`, `product()`
- **Constraints**: `assume due_date >= issued_date`
- **Refine**: `} refine { if type == "A" { field: int in 1..10 } }`
- **References**: `any of companies where .active == true`
- **Parent ref**: `= ^parent_field`
- **Nullable**: `string?` or `string | null`
- **Unique**: `id: unique int in 1..1000`
- **Private**: `age: private int` (generated but excluded from output)
- **Ordered**: `[48, 52, 55, 60]` (cycles through values)

## Reference Files

- [references/syntax.md](references/syntax.md) - Complete syntax
- [references/functions.md](references/functions.md) - Built-in functions
- [references/plugins.md](references/plugins.md) - Faker, Issuer, Regex plugins
- [references/cli.md](references/cli.md) - CLI usage
