---
name: json-validator
description: Validate, format, and fix JSON data. Use this skill when working with JSON files, API responses, or configuration files that need validation or formatting.
---

# JSON Validator

Validate, format, and fix JSON data with helpful error messages and suggestions.

## When to Use This Skill

Use this skill when you need to:
- Validate JSON syntax and structure
- Format/prettify JSON data
- Fix common JSON errors
- Convert between JSON and other formats
- Analyze JSON structure

## Validation

When validating JSON:

1. **Check syntax**: Identify syntax errors with line numbers
2. **Provide context**: Show the problematic section
3. **Suggest fixes**: Offer specific corrections
4. **Explain issues**: Describe what's wrong and why

### Common JSON Errors to Check

- Missing or extra commas
- Unclosed brackets/braces
- Unquoted keys
- Trailing commas (invalid in strict JSON)
- Single quotes instead of double quotes
- Comments (not allowed in JSON)
- Undefined/NaN/Infinity values

### Example Validation Output

```
❌ JSON Validation Failed

Line 5: Trailing comma after last object property
  "name": "example",
  "value": 123,  ← Remove this comma
}

✅ Suggested fix:
{
  "name": "example",
  "value": 123
}
```

## Formatting

When formatting JSON:

1. **Use 2-space indentation** (standard)
2. **Sort keys alphabetically** (optional, ask user)
3. **Remove unnecessary whitespace**
4. **Ensure consistent structure**

### Example

**Input (minified):**
```json
{"name":"test","items":[1,2,3],"active":true}
```

**Output (formatted):**
```json
{
  "name": "test",
  "items": [
    1,
    2,
    3
  ],
  "active": true
}
```

## Fixing Common Issues

### Trailing Commas
```json
// ❌ Invalid
{
  "key": "value",
}

// ✅ Fixed
{
  "key": "value"
}
```

### Single Quotes
```json
// ❌ Invalid
{'key': 'value'}

// ✅ Fixed
{"key": "value"}
```

### Unquoted Keys
```json
// ❌ Invalid
{key: "value"}

// ✅ Fixed
{"key": "value"}
```

### Comments
```json
// ❌ Invalid
{
  // This is a comment
  "key": "value"
}

// ✅ Fixed
{
  "key": "value"
}
```

## Conversion

When converting to/from JSON:

### From JSON to other formats
- **YAML**: Preserve structure, use proper indentation
- **TOML**: Handle nested objects appropriately
- **CSV**: Flatten structure if needed, handle arrays
- **XML**: Choose appropriate tag names

### To JSON from other formats
- Ensure proper escaping
- Validate the result
- Maintain data types (strings, numbers, booleans, null)

## Analysis

When analyzing JSON structure:

1. **Report schema**:
   - Top-level type (object/array)
   - Key names and types
   - Nesting depth
   - Array sizes

2. **Identify patterns**:
   - Repeated structures
   - Optional fields
   - Data types used

3. **Suggest improvements**:
   - Inconsistent naming
   - Deep nesting issues
   - Large array optimization

### Example Analysis

```
JSON Structure Analysis:

Type: Object
Keys: 3 (name, items, metadata)

Schema:
{
  "name": string,
  "items": array[3] of numbers,
  "metadata": {
    "created": string,
    "updated": string
  }
}

Depth: 2 levels
Total size: ~150 bytes
```

## Best Practices

1. **Always validate before formatting** - Don't format invalid JSON
2. **Show clear error messages** - Include line numbers and context
3. **Preserve data types** - Don't convert numbers to strings unnecessarily
4. **Handle edge cases** - Empty objects, null values, Unicode characters
5. **Ask before major changes** - e.g., sorting keys, removing comments

## Examples

### Example 1: Validate and Fix

**User request:**
"Validate this JSON and fix any errors"

**Response:**
```
Found 2 issues:

1. Line 3: Trailing comma after "name"
2. Line 5: Single quotes instead of double quotes

Here's the corrected JSON:
{
  "name": "example",
  "data": {
    "value": 42
  }
}
```

### Example 2: Format

**User request:**
"Format this JSON nicely"

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "name": "Alice"
    },
    {
      "id": 2,
      "name": "Bob"
    }
  ],
  "total": 2
}
```

### Example 3: Convert to YAML

**User request:**
"Convert this JSON to YAML"

**Response:**
```yaml
users:
  - id: 1
    name: Alice
  - id: 2
    name: Bob
total: 2
```
