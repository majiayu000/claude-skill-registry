---
name: jq-yq
description: JSON and YAML manipulation with jq and yq command-line tools. Use when user asks to "parse JSON", "transform YAML", "extract from JSON", "filter JSON array", "convert YAML to JSON", "query JSON", or manipulate structured data from command line.
---

# jq & yq

Command-line JSON and YAML processing.

## jq Basics

### Extract Values

```bash
# Get field
echo '{"name":"John","age":30}' | jq '.name'
# "John"

# Nested field
echo '{"user":{"name":"John"}}' | jq '.user.name'

# Array element
echo '[1,2,3]' | jq '.[0]'
# 1

# Multiple fields
echo '{"a":1,"b":2,"c":3}' | jq '{a,b}'
# {"a":1,"b":2}
```

### Array Operations

```bash
# All elements
echo '[1,2,3]' | jq '.[]'

# Filter array
echo '[1,2,3,4,5]' | jq '[.[] | select(. > 2)]'
# [3,4,5]

# Map
echo '[1,2,3]' | jq '[.[] * 2]'
# [2,4,6]

# Length
echo '[1,2,3]' | jq 'length'
# 3

# First/last
echo '[1,2,3]' | jq 'first'
echo '[1,2,3]' | jq 'last'
```

### Object Arrays

```bash
# Extract field from each
echo '[{"name":"a"},{"name":"b"}]' | jq '.[].name'

# Filter objects
echo '[{"age":20},{"age":30}]' | jq '[.[] | select(.age > 25)]'

# Sort
echo '[{"a":2},{"a":1}]' | jq 'sort_by(.a)'

# Group
echo '[{"type":"a"},{"type":"b"},{"type":"a"}]' | jq 'group_by(.type)'
```

### Transform

```bash
# Build new object
echo '{"first":"John","last":"Doe"}' | jq '{fullName: "\(.first) \(.last)"}'

# Add field
echo '{"a":1}' | jq '. + {b:2}'

# Delete field
echo '{"a":1,"b":2}' | jq 'del(.b)'

# Rename key
echo '{"old":1}' | jq '{new: .old}'
```

### Conditionals

```bash
# If-then-else
echo '{"age":20}' | jq 'if .age >= 18 then "adult" else "minor" end'

# Null handling
echo '{"a":null}' | jq '.a // "default"'
```

### Raw Output

```bash
# No quotes
echo '{"name":"John"}' | jq -r '.name'
# John

# Compact output
echo '{"a":1}' | jq -c '.'
# {"a":1}
```

## yq Basics

### YAML Operations

```bash
# Read value
yq '.name' file.yaml

# Update value
yq -i '.version = "2.0"' file.yaml

# Add field
yq -i '.new_field = "value"' file.yaml

# Delete field
yq -i 'del(.unwanted)' file.yaml
```

### Convert Formats

```bash
# YAML to JSON
yq -o=json file.yaml

# JSON to YAML
yq -P file.json

# YAML to XML
yq -o=xml file.yaml
```

### Multiple Documents

```bash
# Select document
yq 'select(documentIndex == 0)' multi.yaml

# Evaluate all docs
yq ea '. as $item ireduce ([]; . + [$item])' multi.yaml
```

## Common Patterns

### API Response Processing

```bash
# Get specific fields from API
curl -s api.example.com/users | jq '.data[] | {id, name, email}'

# Count results
curl -s api.example.com/items | jq '.results | length'

# Filter and format
curl -s api.example.com/posts | jq -r '.[] | "\(.id): \(.title)"'
```

### Config File Manipulation

```bash
# Update version in package.json
jq '.version = "1.2.3"' package.json > tmp && mv tmp package.json

# Add script
jq '.scripts.test = "jest"' package.json | sponge package.json

# Merge configs
jq -s '.[0] * .[1]' base.json override.json
```

### Kubernetes/Helm

```bash
# Get pod names
kubectl get pods -o json | jq -r '.items[].metadata.name'

# Filter by status
kubectl get pods -o json | jq '.items[] | select(.status.phase=="Running")'

# Update YAML manifest
yq -i '.spec.replicas = 3' deployment.yaml
```

## Reference

For advanced jq filters and recipes: `references/recipes.md`
