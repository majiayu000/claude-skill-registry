---
name: data-processing
description: "Process JSON with jq and YAML/TOML with yq. Filter, transform, query structured data efficiently. Triggers on: parse JSON, extract from YAML, query config, Docker Compose, K8s manifests, GitHub Actions workflows, package.json, filter data."
compatibility: "Requires jq and yq CLI tools. Install: brew install jq yq (macOS)."
allowed-tools: "Bash Read"
---

# Data Processing

Query, filter, and transform structured data (JSON, YAML, TOML) efficiently from the command line.

## Tools

| Tool | Command | Use For |
|------|---------|---------|
| jq | `jq '.key' file.json` | JSON processing |
| yq | `yq '.key' file.yaml` | YAML/TOML processing |

## jq Essentials

```bash
# Extract single field
jq '.name' package.json

# Extract nested field
jq '.scripts.build' package.json

# Extract from array
jq '.dependencies[0]' package.json

# Extract multiple fields
jq '{name, version}' package.json

# Navigate deeply nested
jq '.data.users[0].profile.email' response.json

# Filter by condition
jq '.users[] | select(.active == true)' data.json

# Transform each element
jq '.users | map({id, name})' data.json

# Count elements
jq '.users | length' data.json

# Raw string output
jq -r '.name' package.json
```

## yq Essentials

```bash
# Extract field
yq '.name' config.yaml

# Extract nested
yq '.services.web.image' docker-compose.yml

# List all keys
yq 'keys' config.yaml

# List all service names (Docker Compose)
yq '.services | keys' docker-compose.yml

# Get container images (K8s)
yq '.spec.template.spec.containers[].image' deployment.yaml

# Update value (in-place)
yq -i '.version = "2.0.0"' config.yaml

# TOML to JSON
yq -p toml -o json '.' config.toml
```

## Quick Reference

| Task | jq | yq |
|------|----|----|
| Get field | `jq '.key'` | `yq '.key'` |
| Array element | `jq '.[0]'` | `yq '.[0]'` |
| Filter array | `jq '.[] \| select(.x)'` | `yq '.[] \| select(.x)'` |
| Transform | `jq 'map(.x)'` | `yq 'map(.x)'` |
| Count | `jq 'length'` | `yq 'length'` |
| Keys | `jq 'keys'` | `yq 'keys'` |
| Pretty print | `jq '.'` | `yq '.'` |
| Compact | `jq -c` | `yq -o json -I0` |
| Raw output | `jq -r` | `yq -r` |
| In-place edit | - | `yq -i` |

## When to Use

- Reading package.json dependencies
- Parsing Docker Compose configurations
- Analyzing Kubernetes manifests
- Processing GitHub Actions workflows
- Extracting data from API responses
- Filtering large JSON datasets
- Config file manipulation
- Data format conversion

## Additional Resources

For complete pattern libraries, load:

- `./references/jq-patterns.md` - Arrays, filtering, transformation, aggregation, output formatting
- `./references/yq-patterns.md` - Docker Compose, K8s, GitHub Actions, TOML, YAML modification
- `./references/config-files.md` - package.json, tsconfig, eslint/prettier patterns
