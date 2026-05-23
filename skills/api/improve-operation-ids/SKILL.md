---
name: improve-operation-ids
description: Use when SDK methods have auto-generated names like GetApiV1Users, or wanting `sdk.users.list()` style naming
---

# improve-operation-ids

## Prerequisites

For non-interactive environments (CI/CD, AI agents), set:
```bash
export SPEAKEASY_API_KEY="<your-api-key>"
```
See `configure-authentication` skill for details.

## Check Current State

```bash
speakeasy suggest operation-ids -s openapi.yaml
```

## SDK Method Naming

Speakeasy generates grouped SDK methods using `x-speakeasy-group`:

| HTTP Method | SDK Usage | Operation ID |
|-------------|-----------|--------------|
| GET (list) | `sdk.users.list()` | `users_list` |
| GET (single) | `sdk.users.get()` | `users_get` |
| POST | `sdk.users.create()` | `users_create` |
| PUT | `sdk.users.update()` | `users_update` |
| PATCH | `sdk.users.patch()` | `users_patch` |
| DELETE | `sdk.users.delete()` | `users_delete` |

Use `x-speakeasy-group: users` and `x-speakeasy-name-override: list` to achieve this grouping.

## Apply Suggestions

```bash
# Generate overlay
speakeasy suggest operation-ids -s openapi.yaml -o operation-ids.yaml

# Add to workflow and regenerate
speakeasy run
```

## Manual Override

```yaml
overlay: 1.0.0
info:
  title: Custom operation names
  version: 1.0.0
actions:
  - target: "$.paths['/api/v1/users'].get"
    update:
      x-speakeasy-group: users
      x-speakeasy-name-override: listAll
```

This produces: `sdk.users.listAll()`
