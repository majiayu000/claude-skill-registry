---
name: skogai-jq
description: Use when performing JSON transformations, manipulating nested JSON structures, filtering arrays, extracting values, validating JSON schemas, or composing multi-step JSON operations. This skill provides 60+ schema-driven jq transformations optimized for AI agent discoverability.
---

# jq-transforms

## Overview

jq-transforms is a schema-driven JSON transformation library built specifically for AI agents. It provides 60+ composable transformations for JSON manipulation, each with clear input/output contracts, comprehensive tests, and minimal implementations. The library emphasizes discoverability through schemas and composability through Unix pipes.

## When to Use This Skill

Use this skill when:

- Transforming JSON data structures (CRUD operations, nested paths)
- Filtering or mapping arrays within JSON objects
- Extracting specific fields or patterns from JSON
- Validating JSON schemas or field types
- Converting between JSON types
- Composing multi-step JSON transformations
- Processing API responses or configuration files

## Core Transformation Categories

### CRUD Operations (crud-\*)

Path-based object manipulation for getting, setting, deleting, checking existence, merging, and querying nested JSON structures.

**Common examples:**

- `crud-get`: Retrieve value at nested path with optional default
- `crud-set`: Set value at path, creating intermediate objects
- `crud-delete`: Remove field at path
- `crud-has`: Check if path exists
- `crud-merge`: Recursively merge two objects

### Array Operations (array-\*)

Array transformations including filtering, mapping, reducing, flattening, chunking, and deduplication.

**Common examples:**

- `array-filter`: Filter array by field value
- `array-map`: Extract field from each array element
- `array-reduce`: Aggregate array (sum, avg, min, max, count)
- `array-unique`: Remove duplicate values
- `array-flatten`: Flatten nested arrays to specified depth

### String Operations (string-\*)

String manipulation within JSON objects.

**Common examples:**

- `string-split`: Split string into array by separator
- `string-join`: Join array into string with separator
- `string-replace`: Replace pattern in string
- `string-trim`: Remove whitespace from string

### Extraction (extract-\*)

Pattern-based extraction from text fields.

**Common examples:**

- `extract-urls`: Extract URLs from text
- `extract-code-blocks`: Extract code blocks from markdown
- `extract-mentions`: Extract @mentions from text

### Validation (validate-_, is-_, has-\*)

Field validation and type checking.

**Common examples:**

- `validate-required`: Check required fields exist
- `validate-types`: Validate field types
- `is-timestamp`: Check if value is valid timestamp
- `has-field`: Check if nested path exists

### Type Conversions (to-\*)

Convert between JSON types safely.

**Common examples:**

- `to-string`, `to-number`, `to-boolean`, `to-array`, `to-object`

## Usage Pattern

All transformations follow a consistent invocation pattern:

```bash
jq -f <transform-dir>/transform.jq [--arg key val] [--argjson key json] input.json
```

**Example - Get nested value:**

```bash
echo '{"user":{"name":"skogix"}}' | \
  jq -f crud-get/transform.jq --arg path "user.name"
# Output: "skogix"
```

**Example - Filter array:**

```bash
echo '{"items":[{"status":"active"},{"status":"inactive"}]}' | \
  jq -f array-filter/transform.jq \
    --arg array_field "items" \
    --arg field "status" \
    --arg value "active"
# Output: {"items":[{"status":"active"}]}
```

**Example - Compose multiple transforms:**

```bash
cat data.json | \
  jq -f array-filter/transform.jq --arg array_field "users" --arg field "active" --arg value "true" | \
  jq -f array-map/transform.jq --arg array_field "users" --arg field "email"
```

## Transform Discovery

To find the right transform for a task:

1. **By category**: Refer to the categories above to narrow down the domain (CRUD, array, string, etc.)
2. **By cheat sheet**: Consult `references/CHEAT_SHEET.md` for complete transform index with arguments and examples
3. **By schema**: Read `<transform-dir>/schema.json` for detailed input/output contracts

Each transform directory contains:

- `transform.jq` - The jq implementation (5-40 lines)
- `schema.json` - Input/output contract with examples
- `test.sh` - Comprehensive test suite
- `test-input-*.json` - Test fixtures

## Key Design Principles

1. **Schema-first**: Every transform has explicit input/output/args contract
2. **Argument-based**: All parameters via `--arg`/`--argjson` (no hardcoding)
3. **Composable**: Chain transforms via Unix pipes
4. **Type-safe**: Graceful handling of missing paths and wrong types
5. **Self-contained**: Each transform is isolated, no dependencies
6. **Minimal**: Fewer lines = fewer bugs, easier to understand

## Common Patterns

**Get value with default:**

```bash
jq -f crud-get/transform.jq --arg path "config.timeout" --arg default "30"
```

**Set nested value:**

```bash
jq -f crud-set/transform.jq --arg path "user.profile.age" --arg value "30"
```

**Filter and extract:**

```bash
jq -f array-filter/transform.jq --arg array_field "users" --arg field "active" --arg value "true" | \
jq -f array-map/transform.jq --arg array_field "users" --arg field "email"
```

**Validate required fields:**

```bash
jq -f validate-required/transform.jq --arg fields "name,email,age"
```

## Critical Implementation Notes

When creating new transforms or debugging issues:

**Avoid common jq pitfalls:**

- Use `try-catch` instead of `// fallback` for falsy value handling
- Use `has()` instead of `!= null` for existence checks
- Check array types before using `map()` operations

Refer to `references/IMPLEMENTATION_SPEC.md` for complete implementation patterns, test coverage requirements, and detailed pitfall documentation.

## References

This skill bundles comprehensive reference documentation (loaded only when needed):

- **CHEAT_SHEET.md** - Quick reference of all 60+ transforms with arguments and examples
- **IMPLEMENTATION_SPEC.md** - Complete implementation guide with patterns and pitfalls
- **README.md** - User-facing documentation and design principles
- **USAGE_EXAMPLES.md** - Real-world usage scenarios

## Testing

Test transforms before use:

```bash
# Test specific transform
./crud-get/test.sh

# Test all transforms
./test-all.sh
```

Each transform has 8-17 test cases covering happy paths, falsy values, type safety, boundary conditions, and error cases.
