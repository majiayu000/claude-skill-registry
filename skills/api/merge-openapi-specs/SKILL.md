---
name: merge-openapi-specs
description: Use when combining multiple OpenAPI specs, or have microservices with separate spec files
---

# merge-openapi-specs

Use `speakeasy merge` to combine multiple specs into one.

## Command

```bash
speakeasy merge -o <output-path> <spec1> <spec2> [spec3...]
```

## Example

```bash
# Merge two specs
speakeasy merge -o combined.yaml ./api/users.yaml ./api/orders.yaml

# Merge multiple specs
speakeasy merge -o combined.yaml ./specs/*.yaml
```

## Use Cases

- Microservices with separate specs per service
- API versioning with multiple spec files
- Combining public and internal API specs

## Conflict Resolution

When specs have conflicts:
- Later specs override earlier ones for duplicate paths
- Schema conflicts may require manual resolution
- Review merged output for correctness
