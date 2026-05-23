---
name: create-openapi-overlay
description: Use when you need to customize SDK generation without editing the source spec, or can't modify the original OpenAPI file
---

# create-openapi-overlay

Overlays let you customize an OpenAPI spec for SDK generation without modifying the source.

## Create Overlay Template

```bash
speakeasy overlay create -s <spec-path> -o <output-path>
```

## When to Use Overlays

**Overlays are great for:**
- Renaming operations (x-speakeasy-name-override)
- Adding descriptions/summaries
- Grouping operations (x-speakeasy-group)
- Adding retry configuration
- Marking endpoints as deprecated
- Adding SDK-specific extensions
- Fixing spec issues without modifying the source
- Adding new endpoints or schemas
- Making portable patches that work across spec versions

**Overlays cannot easily handle:**
- Deduplication of schemas (requires structural analysis)

## Example Overlay

```yaml
overlay: 1.0.0
info:
  title: SDK Customizations
  version: 1.0.0
actions:
  - target: "$.paths['/users'].get"
    update:
      x-speakeasy-group: users
      x-speakeasy-name-override: list
  - target: "$.paths['/users'].post"
    update:
      x-speakeasy-group: users
      x-speakeasy-name-override: create
  - target: "$.paths['/users/{id}'].get"
    update:
      x-speakeasy-group: users
      x-speakeasy-name-override: get
  - target: "$.paths['/users/{id}'].delete"
    update:
      x-speakeasy-group: users
      x-speakeasy-name-override: delete
      deprecated: true
```

This produces: `sdk.users.list()`, `sdk.users.create()`, `sdk.users.get()`, `sdk.users.delete()`

## JSONPath Targeting

| Target | Selects |
|--------|---------|
| `$.paths['/users'].get` | GET /users operation |
| `$.paths['/users/{id}'].*` | All operations on /users/{id} |
| `$.components.schemas.User` | User schema |
| `$.info` | API info object |
