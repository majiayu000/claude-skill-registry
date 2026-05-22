---
name: toon-formatter
description: Token-Oriented Object Notation (TOON) format expert for 30-60% token savings on structured data. Auto-applies to arrays with 5+ items, tables, logs, API responses, database results. Supports tabular, inline, and expanded formats with comma/tab/pipe delimiters. Triggers on large JSON, data optimization, token reduction, structured data, arrays, tables, logs, metrics, TOON.
allowed-tools: Read, Write, Edit, Bash
model: sonnet
license: MIT
metadata:
  author: raintree
  version: "2.0"
  repository: https://github.com/toon-format/spec
---

# TOON v2.0 Format Expert

**TOON (Token-Oriented Object Notation)** saves 30-60% tokens on structured data by eliminating repetitive keys in uniform arrays.

## When to Use

**Automatically apply TOON when:**
- Arrays with 5+ similar objects
- API responses with repeated structure
- Database query results
- Log entries, events, transactions
- Metrics, analytics, benchmarks
- Any tabular data

**Keep as JSON when:**
- Small arrays (<5 items)
- Deeply nested non-uniform data
- Single objects
- Narrative text or instructions

## Format Specification

### Tabular Format (Most Common)

For arrays of uniform objects:

```
[count]{field1,field2,field3}:
  value1,value2,value3
  value1,value2,value3
```

**Example - JSON (120 tokens):**
```json
[
  {"id": 1, "name": "Alice", "role": "admin", "active": true},
  {"id": 2, "name": "Bob", "role": "user", "active": true},
  {"id": 3, "name": "Carol", "role": "user", "active": false}
]
```

**TOON (70 tokens, 42% savings):**
```
[3]{id,name,role,active}:
  1,Alice,admin,true
  2,Bob,user,true
  3,Carol,user,false
```

### Inline Format

For primitive arrays (10 or fewer items):

```
fieldName[count]: value1,value2,value3
```

**Example:**
```
tags[4]: javascript,react,nodejs,api
ids[3]: 101,102,103
```

### Expanded Format

For complex nested values (one per line):

```
items[3]|:
  | {"complex": "object1"}
  | {"complex": "object2"}
  | {"complex": "object3"}
```

### Delimiters

Choose based on data content:

| Delimiter | Syntax | Use When |
|-----------|--------|----------|
| Comma | `[N]` | Default, no commas in values |
| Tab | `[N\t]` | Values contain commas |
| Pipe | `[N\|]` | Values contain commas and tabs |

**Tab-delimited example:**
```
[2\t]{name,description}:
  Product A	A great product, really
  Product B	Another one, even better
```

### Key Folding (Nested Objects)

Flatten nested structures:

```
server.host: localhost
server.port: 8080
server.ssl.enabled: true
database.url: postgres://localhost/db
```

### Special Values

| Value | TOON Representation |
|-------|---------------------|
| null | `~` |
| empty string | `""` |
| true | `true` |
| false | `false` |

## Conversion Patterns

### API Response

**Before (JSON):**
```json
{
  "users": [
    {"id": 1, "email": "a@x.com", "plan": "pro"},
    {"id": 2, "email": "b@x.com", "plan": "free"},
    {"id": 3, "email": "c@x.com", "plan": "pro"}
  ],
  "total": 3
}
```

**After (TOON):**
```
users[3]{id,email,plan}:
  1,a@x.com,pro
  2,b@x.com,free
  3,c@x.com,pro
total: 3
```

### Log Entries

**Before (JSON):**
```json
[
  {"ts": "2024-01-15T10:00:00Z", "level": "INFO", "msg": "Server started"},
  {"ts": "2024-01-15T10:00:01Z", "level": "DEBUG", "msg": "Connection pool ready"},
  {"ts": "2024-01-15T10:00:02Z", "level": "INFO", "msg": "Listening on :8080"}
]
```

**After (TOON):**
```
[3]{ts,level,msg}:
  2024-01-15T10:00:00Z,INFO,Server started
  2024-01-15T10:00:01Z,DEBUG,Connection pool ready
  2024-01-15T10:00:02Z,INFO,Listening on :8080
```

### Database Results

**Before (JSON):**
```json
[
  {"product_id": 101, "name": "Widget", "price": 29.99, "stock": 150},
  {"product_id": 102, "name": "Gadget", "price": 49.99, "stock": 75},
  {"product_id": 103, "name": "Gizmo", "price": 19.99, "stock": 200}
]
```

**After (TOON):**
```
[3]{product_id,name,price,stock}:
  101,Widget,29.99,150
  102,Gadget,49.99,75
  103,Gizmo,19.99,200
```

### Mixed Content

**Combine formats as needed:**
```
config.name: MyApp
config.version: 1.0.0
config.features[3]: auth,logging,metrics

endpoints[4]{method,path,auth}:
  GET,/api/users,required
  POST,/api/users,required
  GET,/api/health,none
  DELETE,/api/users/:id,admin

tags[5]: api,rest,json,http,web
```

## Decision Flowchart

```
Is it an array?
├─ No → Use standard JSON/key-value
└─ Yes → How many items?
    ├─ <5 → Keep as JSON (overhead not worth it)
    └─ ≥5 → Are objects uniform (≥60% same keys)?
        ├─ No → Use expanded format
        └─ Yes → Are values primitives?
            ├─ Yes, ≤10 items → Inline format
            └─ Otherwise → Tabular format
```

## Token Savings Reference

| Data Type | Typical Savings |
|-----------|-----------------|
| User lists | 40-50% |
| Log entries | 35-45% |
| API responses | 30-50% |
| Database rows | 45-55% |
| Event streams | 40-60% |
| Config arrays | 25-35% |

## Binary Encoder

A compiled Zig encoder (20x faster than JS) is available:

```bash
# Encode JSON to TOON
.claude/utils/toon/bin/toon encode data.json

# Decode TOON to JSON  
.claude/utils/toon/bin/toon decode data.toon

# Check if TOON recommended
.claude/utils/toon/bin/toon check data.json

# Analyze token savings
.claude/utils/toon/bin/toon analyze data.json
```

## Commands

| Command | Description |
|---------|-------------|
| `/toon-encode <file>` | Convert JSON to TOON |
| `/toon-decode <file>` | Convert TOON to JSON |
| `/toon-validate <file>` | Validate TOON syntax |
| `/analyze-tokens <file>` | Compare JSON vs TOON size |
| `/convert-to-toon <file>` | Full conversion workflow |

## Best Practices

**DO:**
- Use TOON for data payloads in RAG pipelines
- Apply to tool call responses with arrays
- Convert benchmark results and metrics
- Use tab delimiter when values have commas

**DON'T:**
- Convert small arrays (<5 items)
- Force non-uniform data into tabular format
- Use for deeply nested structures
- Apply to human-readable documentation

## Resources

- **Specification**: https://github.com/toon-format/spec
- **Website**: https://toonformat.dev
- **Local Guide**: `.claude/utils/toon/toon-guide.md`
