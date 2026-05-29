---
name: json-schema
# prettier-ignore
description: Use when working with JSON Schema for validation, OpenAPI schemas, type definitions, and data structure specification
---

# JSON Schema

## Quick Start

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id", "email"],
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "email": { "type": "string", "format": "email" },
    "age": { "type": "integer", "minimum": 0, "maximum": 150 },
    "role": { "enum": ["admin", "user", "guest"] },
    "tags": { "type": "array", "items": { "type": "string" } }
  }
}
```

## Type Keywords

| Type | Validation Keywords |
|------|---------------------|
| `string` | `minLength`, `maxLength`, `pattern`, `format` |
| `number/integer` | `minimum`, `maximum`, `exclusiveMinimum`, `multipleOf` |
| `array` | `items`, `minItems`, `maxItems`, `uniqueItems` |
| `object` | `properties`, `required`, `additionalProperties` |

## Composition

```json
{
  "allOf": [{ "$ref": "#/$defs/Base" }, { "properties": { "extra": {} } }],
  "oneOf": [{ "type": "string" }, { "type": "number" }],
  "anyOf": [{ "minimum": 0 }, { "maximum": 100 }],
  "not": { "type": "null" }
}
```

## References

```json
{
  "$defs": {
    "Address": {
      "type": "object",
      "properties": { "street": { "type": "string" } }
    }
  },
  "properties": {
    "billing": { "$ref": "#/$defs/Address" },
    "shipping": { "$ref": "#/$defs/Address" }
  }
}
```

## Common Formats

`date-time`, `date`, `time`, `email`, `uri`, `uuid`, `ipv4`, `ipv6`, `hostname`

## OpenAPI 3.1 Notes

- OpenAPI 3.1 uses JSON Schema 2020-12
- Use `nullable` via `type: ["string", "null"]`
- `example` for single example, `examples` for multiple
- `$ref` can have siblings in 3.1 (not in 3.0)
