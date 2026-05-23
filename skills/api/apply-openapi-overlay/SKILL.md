---
name: apply-openapi-overlay
description: Use when applying an overlay file to a spec
---

# apply-openapi-overlay

## Command

```bash
speakeasy overlay apply -s <spec-path> -o <overlay-path> --out <output-path>
```

## Example

```bash
# Apply overlay and output merged spec
speakeasy overlay apply -s openapi.yaml -o my-overlay.yaml --out openapi-modified.yaml
```

## Using in Workflow

Better approach - add overlay to workflow.yaml:

```yaml
sources:
  my-api:
    inputs:
      - location: ./openapi.yaml
    overlays:
      - location: ./naming-overlay.yaml
      - location: ./grouping-overlay.yaml
```

Overlays are applied in order, so later overlays can override earlier ones.
