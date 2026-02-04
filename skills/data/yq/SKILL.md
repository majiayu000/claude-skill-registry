---
name: yq
description: Extract specific fields from YAML files efficiently using qq instead of reading entire files, saving 80-95% context.
---

# yq: YAML Query and Extraction Tool

Use yq to extract specific fields from YAML files without reading entire file contents, saving 80-95% context usage.

## When to Use yq

**Use yq when:**
- Need specific field(s) from structured YAML file
- File is large (>50 lines) and only need subset of data
- Querying nested structures in YAML
- Filtering/transforming YAML data
- Working with docker-compose.yml, GitHub Actions workflows, K8s configs

**Just use Read when:**
- File is small (<50 lines)
- Need to understand overall structure
- Making edits (need full context anyway)

## Tool Selection

**JSON files** → Use `jq`
- Common: package.json, tsconfig.json, lock files, API responses

**YAML files** → Use `yq`
- Common: docker-compose.yml, GitHub Actions, CI/CD configs

Both tools extract exactly what you need in one command - massive context savings.

## Quick Examples

```bash
# Get version from package.json
jq -r .version package.json

# Get service ports from docker-compose
yq '.services.*.ports' docker-compose.yml
```

## Detailed Reference

For comprehensive yq patterns, syntax, and examples, load [yq guide](./reference/yq-guide.md):
- Core patterns (80% of use cases)
- Real-world workflows (Docker Compose, GitHub Actions, Kubernetes)
- Advanced patterns and edge case handling
- Output formats and pipe composition
- Best practices and integration with other tools
