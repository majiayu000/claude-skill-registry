---
name: sql-on-fhir
description: Expert guidance for implementing SQL on FHIR v2 ViewDefinitions and operations to create portable, tabular projections of FHIR data. Use this skill when the user asks to create ViewDefinitions, flatten FHIR resources into tables, write FHIRPath expressions for data extraction, implement forEach/forEachOrNull/repeat patterns for unnesting, create where clauses for filtering, use constants in view definitions, combine data with unionAll, execute ViewDefinitions with $run or $export operations, or implement SQL on FHIR server capabilities. Trigger keywords include "ViewDefinition", "SQL on FHIR", "flatten FHIR", "tabular FHIR", "FHIR to SQL", "FHIR analytics", "FHIRPath columns", "unnest FHIR", "$viewdefinition-run", "$export", "view runner", "repeat", "recursive", "QuestionnaireResponse".
---

# SQL on FHIR

SQL on FHIR v2 defines portable, tabular projections of FHIR resources using FHIRPath expressions. ViewDefinitions transform hierarchical FHIR data into flat tables for analytics.

## Core Concepts

A **ViewDefinition** projects exactly one FHIR resource type into rows and columns. It contains:

- `resource`: The FHIR resource type (Patient, Observation, etc.)
- `select`: Column definitions and row iteration logic
- `where`: Optional filtering criteria
- `constant`: Reusable values for expressions

## ViewDefinition Structure

Basic structure:

```json
{
    "resourceType": "ViewDefinition",
    "resource": "Patient",
    "status": "active",
    "select": [
        {
            "column": [
                { "name": "id", "path": "id" },
                { "name": "gender", "path": "gender" },
                { "name": "birth_date", "path": "birthDate" }
            ]
        }
    ]
}
```

For complete element reference, see [references/view-definition-structure.md](references/view-definition-structure.md).

## Column Definitions

Each column has:

- `name`: Database-friendly identifier (pattern: `^[A-Za-z][A-Za-z0-9_]*$`)
- `path`: FHIRPath expression extracting the value
- `type` (optional): FHIR primitive type URI
- `collection` (optional): Set true if column may contain arrays
- `description` (optional): Human-readable explanation

```json
{
    "column": [
        {
            "name": "family_name",
            "path": "name.first().family",
            "type": "string",
            "description": "Patient's primary family name"
        }
    ]
}
```

## Row Iteration with forEach

Use `forEach` to create one row per element in a collection. Without `forEach`, one row per resource is created.

**Example: One row per patient name:**

```json
{
    "resource": "Patient",
    "select": [
        { "column": [{ "name": "id", "path": "id" }] },
        {
            "forEach": "name",
            "column": [
                { "name": "family", "path": "family" },
                { "name": "given", "path": "given.first()" }
            ]
        }
    ]
}
```

**forEachOrNull**: Same as forEach but keeps a row with nulls when the collection is empty.

**Nested forEach**: Create cross-products by nesting:

```json
{
    "forEach": "contact",
    "select": [
        {
            "column": [
                {
                    "name": "contact_phone",
                    "path": "telecom.where(system='phone').value"
                }
            ]
        },
        {
            "forEach": "name.given",
            "column": [{ "name": "given_name", "path": "$this" }]
        }
    ]
}
```

## Recursive Traversal with repeat

Use `repeat` to recursively traverse nested structures to any depth. This is essential for resources with arbitrary nesting like QuestionnaireResponse items.

**Constraint**: Only one of `forEach`, `forEachOrNull`, or `repeat` may be specified per select.

```json
{
    "resource": "QuestionnaireResponse",
    "select": [
        { "column": [{ "name": "response_id", "path": "id" }] },
        {
            "repeat": ["item", "answer.item"],
            "column": [
                { "name": "link_id", "path": "linkId" },
                {
                    "name": "answer_text",
                    "path": "answer.value.ofType(string).first()"
                }
            ]
        }
    ]
}
```

The view runner:

1. Starts at the resource root
2. Evaluates each path in the `repeat` array
3. For each result, recursively applies the same paths
4. Continues until no more matches exist
5. Unions all results from all levels

This produces a flat table with all items regardless of nesting depth.

## Filtering with where

Filter resources using FHIRPath expressions that must evaluate to true:

```json
{
  "resource": "Patient",
  "where": [
    {"path": "active = true"},
    {"path": "name.exists()"}
  ],
  "select": [...]
}
```

Multiple where clauses are ANDed together.

## Constants

Define reusable values referenced via `%name` syntax:

```json
{
    "constant": [{ "name": "use_type", "valueString": "official" }],
    "select": [
        {
            "forEach": "name.where(use = %use_type)",
            "column": [{ "name": "official_name", "path": "family" }]
        }
    ]
}
```

Supported constant types: `valueString`, `valueInteger`, `valueBoolean`, `valueDecimal`, `valueDate`, `valueDateTime`, `valueCode`.

## Combining Data with unionAll

Combine multiple selection paths with matching column schemas:

```json
{
    "select": [
        { "column": [{ "name": "id", "path": "id" }] },
        {
            "unionAll": [
                {
                    "forEach": "telecom",
                    "column": [
                        { "name": "contact", "path": "value" },
                        { "name": "system", "path": "system" }
                    ]
                },
                {
                    "forEach": "contact.telecom",
                    "column": [
                        { "name": "contact", "path": "value" },
                        { "name": "system", "path": "system" }
                    ]
                }
            ]
        }
    ]
}
```

## FHIRPath Subset

ViewDefinitions use a minimal FHIRPath subset. Key functions:

| Function                 | Description                     |
| ------------------------ | ------------------------------- |
| `first()`                | First element of collection     |
| `exists()`               | True if collection has elements |
| `empty()`                | True if collection is empty     |
| `where(expr)`            | Filter collection by condition  |
| `ofType(type)`           | Filter to specific FHIR type    |
| `extension(url)`         | Get extension by URL            |
| `join(sep)`              | Join collection into string     |
| `getResourceKey()`       | Resource ID (indirect access)   |
| `getReferenceKey(type?)` | Extract ID from reference       |

**Path navigation:**

- Dot notation: `name.family`
- Indexing: `name[0].family`
- `$this`: Current context element

For complete FHIRPath reference, see [references/fhirpath-subset.md](references/fhirpath-subset.md).

## Working with Extensions

Extract extension values using the `extension()` function:

```json
{
    "column": [
        {
            "name": "birth_sex",
            "path": "extension('http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex').value.ofType(code).first()"
        }
    ]
}
```

Nested extensions:

```json
{
    "path": "extension('http://hl7.org/fhir/us/core/StructureDefinition/us-core-race').extension('ombCategory').value.ofType(Coding).code.first()"
}
```

## Profiles

**ShareableViewDefinition**: For portable definitions. Requires:

- `url`: Canonical identifier
- `name`: Database-safe identifier
- `fhirVersion`: Target FHIR version(s)
- Column `type`: Explicit types on all columns

**TabularViewDefinition**: For scalar/CSV output. Enforces:

- No `collection: true` columns
- Primitive types only (string, boolean, integer, etc.)

## Design Constraints

ViewDefinitions intentionally exclude:

- Cross-resource joins (use SQL after flattening)
- Sorting, aggregation, limits (apply in analytics layer)
- Output format specification (runner determines format)

## Operations

SQL on FHIR defines two operations for executing ViewDefinitions:

### $viewdefinition-run

Synchronous execution returning results immediately.

```
GET  [base]/ViewDefinition/[id]/$run?_format=csv
POST [base]/ViewDefinition/$run
```

Key parameters:

- `viewReference` or `viewResource`: The ViewDefinition to execute
- `_format`: Output format (`json`, `ndjson`, `csv`, `parquet`)
- `patient`, `group`: Filter by patient/group
- `_limit`: Maximum rows

### $export

Asynchronous bulk export for large datasets.

```
POST [base]/ViewDefinition/$export
```

Uses async pattern:

1. POST with `Prefer: respond-async` → 202 Accepted + status URL
2. Poll status URL until complete
3. Download results from output URLs

Key parameters:

- `view`: One or more ViewDefinitions to export
- `_format`: Output format
- `patient`, `group`, `_since`: Filtering options

For complete operation details, parameters, and examples, see [references/operations.md](references/operations.md).

## Examples

For comprehensive examples including Patient demographics, Condition flattening, blood pressure extraction, and complex unnesting patterns, see [references/examples.md](references/examples.md).
