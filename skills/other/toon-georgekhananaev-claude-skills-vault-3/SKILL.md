---
name: toon
description: Token-Oriented Object Notation (TOON) format for LLM-optimized data encoding. Converts JSON to compact, human-readable format that minimizes tokens (~40% reduction) while improving LLM comprehension accuracy.
license: MIT
reference: https://github.com/toon-format/toon
author: George Khananaev
---

# TOON Format Guide

## Overview

TOON (Token-Oriented Object Notation) is a compact encoding of JSON designed for LLM input. Combines YAML-style indentation w/ CSV-style tables for uniform arrays.

**Key benefits:**
- ~40% fewer tokens vs JSON
- 73.9% accuracy vs 69.7% for JSON in retrieval tasks
- Explicit length declarations for validation
- Lossless JSON round-trips

## Syntax

### Objects (YAML-style indentation)
```toon
user:
  name: John
  age: 30
  address:
    city: NYC
    zip: 10001
```

### Uniform Arrays (Tabular)
```toon
users[3]{id,name,email}:
  1,John,john@ex.com
  2,Jane,jane@ex.com
  3,Bob,bob@ex.com
```
- `[N]` = array length (req for validation)
- `{fields}` = column schema (declared once)

### Scalar Arrays
```toon
tags[4]: api,rest,json,toon
```

### Non-uniform Arrays (Nested)
```toon
items:
  - id: 1
    type: book
    meta:
      pages: 200
  - id: 2
    type: video
    meta:
      duration: 3600
```

## Conversion Rules

### JSON to TOON

1. **Objects** => indented key-value pairs
2. **Uniform arrays** => tabular `[N]{fields}:` format
3. **Mixed/nested arrays** => `-` list notation
4. **Scalars** => quote only when containing `,` or special chars

### Examples

**JSON:**
```json
{"orders":[{"id":1,"item":"Book","qty":2,"price":29.99},{"id":2,"item":"Pen","qty":10,"price":1.99}]}
```

**TOON:**
```toon
orders[2]{id,item,qty,price}:
  1,Book,2,29.99
  2,Pen,10,1.99
```

**Nested JSON:**
```json
{"config":{"db":{"host":"localhost","port":5432},"cache":{"enabled":true,"ttl":300}}}
```

**TOON:**
```toon
config:
  db:
    host: localhost
    port: 5432
  cache:
    enabled: true
    ttl: 300
```

## When to Use TOON

TOON replaces **data serialization formats** when sending to LLMs.

### Formats to convert → TOON:
| Format | Convert? | Notes |
|--------|----------|-------|
| JSON | Yes | Primary use case |
| JSON compact | Yes | Same as JSON |
| YAML | Yes | Structured data |
| XML | Yes | Verbose, big savings |

### Do NOT convert to TOON:
| Format | Convert? | Reason |
|--------|----------|--------|
| Markdown | No | Keep as markdown |
| Plain text | No | Keep as text |
| Code files | No | Keep original syntax |
| CSV | No | Already compact for flat tables |

### TOON sweet spot:
Uniform arrays of objects (same fields per item) from JSON/YAML/XML.

### Key insight:
TOON replaces **data serialization formats** when the consumer is an LLM.

## Quick Reference

| Data Type | TOON Syntax | Example |
|-----------|-------------|---------|
| Object | indent | `user:\n  name: John` |
| Uniform array | `[N]{fields}:` | `items[2]{a,b}:\n  1,x\n  2,y` |
| Scalar array | `[N]:` | `ids[3]: 1,2,3` |
| Nested array | `- item` | `- name: x\n- name: y` |
| Quoted str | `"val"` | `name: "a,b,c"` |
| Null | `null` | `val: null` |
| Bool | `true`/`false` | `active: true` |

## File Format

- Extension: `.toon`
- Media type: `text/toon`
- Encoding: UTF-8

## Implementations

Official npm: `@toon-format/toon`, `@toon-format/cli`

### Node.js/TypeScript Example
```typescript
// npm install @toon-format/toon
import { encode, decode } from '@toon-format/toon';

// JSON to TOON
const data = { users: [{ id: 1, name: 'John' }] };
const toonStr = encode(data);

// TOON to JSON
const parsed = decode(toonStr);
```

### CLI Example
```bash
# npm install -g @toon-format/cli
toon encode input.json > output.toon
toon decode input.toon > output.json
```

## Validation

TOON's `[N]` notation enables:
- Array truncation detection
- Field count validation
- Schema consistency checks

```toon
# This declares exactly 3 items w/ 2 fields each
products[3]{name,price}:
  Widget,9.99
  Gadget,19.99
  Tool,14.99
```

If LLM receives incomplete data, length mismatch signals corruption.

## Scripts

### Validator (`scripts/validate.py`)

Validates TOON syntax and structure before use.

```bash
# Validate TOON file
python .claude/skills/document-skills/toon/scripts/validate.py input.toon

# Check JSON compatibility for TOON conversion
python .claude/skills/document-skills/toon/scripts/validate.py --json input.json

# Quiet mode (errors only)
python .claude/skills/document-skills/toon/scripts/validate.py -q input.toon
```

**Checks:**
- Array length `[N]` matches actual row count
- Field count `{a,b,c}` matches values per row
- Quote balance
- Consistent indentation
- Empty value warnings

### Converter - Node.js (`scripts/convert.js`) - Recommended

Uses official `@toon-format/toon` library for full spec compliance.

```bash
# Install official library
npm install @toon-format/toon

# JSON to TOON
node .claude/skills/document-skills/toon/scripts/convert.js input.json

# JSON to TOON with output file
node .claude/skills/document-skills/toon/scripts/convert.js input.json -o output.toon

# TOON to JSON
node .claude/skills/document-skills/toon/scripts/convert.js --to-json input.toon

# Verify round-trip
node .claude/skills/document-skills/toon/scripts/convert.js --verify input.json
```

### Converter - Python (`scripts/convert.py`) - Fallback

Basic implementation when Node.js is not available.

```bash
# JSON to TOON
python .claude/skills/document-skills/toon/scripts/convert.py input.json

# TOON to JSON
python .claude/skills/document-skills/toon/scripts/convert.py --to-json input.toon

# Verify round-trip
python .claude/skills/document-skills/toon/scripts/convert.py --verify input.json
```

## Compression Tips

1. Use tabular format for uniform arrays (max savings)
2. Declare lengths `[N]` for validation
3. Quote strings only when necessary
4. Flatten when possible, nest when required
5. Combine related arrays into single table