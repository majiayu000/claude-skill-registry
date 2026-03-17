---
name: jq
description: |
    Use when processing JSON or YAML data from the command line. Covers jq for JSON and yq for YAML — filtering, transforming, and extracting data from structured outputs of APIs, config files, and CLI tools.
    USE FOR: jq, yq, JSON processing, YAML processing, CLI data transformation, filtering JSON, extracting fields, JSON to CSV, JSON arrays, jq expressions, yq expressions
    DO NOT USE FOR: general text processing (use grep/sed/awk via bash), XML processing, full programming (use Python or Node.js for complex transformations)
license: MIT
metadata:
  displayName: "jq & Data Processing"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "jq Documentation"
    url: "https://jqlang.github.io/jq/manual/"
  - title: "jq GitHub Repository"
    url: "https://github.com/jqlang/jq"
  - title: "yq GitHub Repository"
    url: "https://github.com/mikefarah/yq"
---

# jq & Data Processing

## Overview

jq is "sed for JSON" — a lightweight command-line processor for JSON data. Combined with curl, it's the standard way to interact with REST APIs from the terminal. yq extends the same idea to YAML.

## Installation

| Platform | jq | yq |
|----------|----|----|
| Windows | `choco install jq` / `winget install jqlang.jq` | `choco install yq` |
| macOS | `brew install jq` | `brew install yq` |
| Linux | `apt install jq` | `snap install yq` |

## jq Basics

### Identity (pretty-print)

```bash
echo '{"name":"Alice","age":30}' | jq '.'
```

### Field access

```bash
echo '{"name":"Alice","address":{"city":"NYC"}}' | jq '.name'
# "Alice"

echo '{"name":"Alice","address":{"city":"NYC"}}' | jq '.address.city'
# "NYC"
```

### Array indexing

```bash
echo '[10,20,30,40,50]' | jq '.[0]'     # 10
echo '[10,20,30,40,50]' | jq '.[-1]'    # 50
echo '[10,20,30,40,50]' | jq '.[2:5]'   # [30,40,50]
```

### Array iteration

```bash
echo '[{"name":"Alice"},{"name":"Bob"}]' | jq '.[]'
```

### Pipe

```bash
curl -s https://api.example.com/data | jq '.users[] | .name'
```

### Select / filter

```bash
echo '[{"name":"Alice","age":35},{"name":"Bob","age":25}]' | jq '.[] | select(.age > 30)'
```

### Map

```bash
echo '[{"name":"Alice"},{"name":"Bob"}]' | jq '[.[] | .name]'
# ["Alice", "Bob"]
```

### Keys, length, type

```bash
echo '{"a":1,"b":2}' | jq 'keys'       # ["a","b"]
echo '[1,2,3]' | jq 'length'            # 3
echo '"hello"' | jq 'type'              # "string"
```

### Construct objects

```bash
echo '{"first":"Alice","contact":{"email":"a@b.com"}}' | jq '{name: .first, email: .contact.email}'
```

### String interpolation

```bash
echo '{"name":"Alice","email":"a@b.com"}' | jq '"\(.name) - \(.email)"'
# "Alice - a@b.com"
```

## Common jq Recipes

### Extract specific fields

```bash
jq '.[] | {name, email}' users.json
```

### Filter by value

```bash
jq '[.[] | select(.status == "active")]' users.json
```

### Count items

```bash
jq '.users | length' data.json
```

### Sort by field

```bash
jq '.users | sort_by(.age)' data.json
```

### Group by field

```bash
jq '.users | group_by(.department)' data.json
```

### Flatten arrays

```bash
jq '[.[][]]' nested.json
```

### JSON to CSV

```bash
jq -r '.[] | [.name, .email, .age] | @csv' users.json
```

### Unique values

```bash
jq '[.[].category] | unique' items.json
```

### Merge objects

```bash
jq -s '.[0] * .[1]' defaults.json overrides.json
```

### Conditional

```bash
echo '{"age":21}' | jq 'if .age > 18 then "adult" else "minor" end'
```

## yq Basics

### Read a field

```bash
yq '.metadata.name' deployment.yaml
```

### Update a field

```bash
yq '.spec.replicas = 3' -i deployment.yaml
```

### Convert YAML to JSON

```bash
yq -o json deployment.yaml
```

### Convert JSON to YAML

```bash
yq -P data.json
```

### Merge YAML files

```bash
yq eval-all '. as $item ireduce({}; . * $item)' base.yaml override.yaml
```

## Combining with curl

```bash
curl -s https://api.github.com/repos/torvalds/linux | jq '{name: .name, stars: .stargazers_count, language: .language}'
```

Output:
```json
{
  "name": "linux",
  "stars": 178000,
  "language": "C"
}
```

## Best Practices

- Use jq for any JSON manipulation in shell scripts — it is purpose-built and reliable
- Pipe `curl -s` to jq for API work — this is the standard pattern for CLI-based API interaction
- Use yq for editing Kubernetes manifests, Helm values, and CI config files in place
- Prefer jq over grep/awk for JSON — regex on JSON is fragile and error-prone
- Use `-r` for raw string output in scripts to avoid quoted strings in downstream processing
- Learn `select()` and `map()` — they handle the vast majority of filtering and transformation tasks
