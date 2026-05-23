---
name: schema-to-openapi
description: |
  Convert Synnovator data schema to OpenAPI 3.0 specification. Use when:
  (1) Need to generate REST API spec from Synnovator's content types and relations
  (2) Preparing input for api-builder skill to scaffold backend code
  (3) Want standardized, RESTful API design from the Synnovator data model

  Triggers: "generate openapi", "create api spec", "convert schema to openapi",
  "prepare for api-builder", "generate REST API from synnovator"
---

# Schema to OpenAPI

Generate OpenAPI 3.0 specification from Synnovator's data schema.

## Quick Start

```bash
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py
```

Output: `.synnovator/openapi.yaml`

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--output`, `-o` | `.synnovator/openapi.yaml` | Output file path |
| `--title` | `Synnovator API` | API title |
| `--version` | `1.0.0` | API version |
| `--format` | `yaml` | Output format (`yaml` or `json`) |

## What Gets Generated

### Content Type Endpoints (7 resources)
- `/categories` - Activity/competition management
- `/posts` - User posts and submissions
- `/resources` - File attachments
- `/rules` - Category rules and scoring criteria
- `/users` - User management
- `/groups` - Teams and groups
- `/users/me` - Current user profile

### Nested Relation Endpoints
- `/categories/{id}/rules` - Category rules
- `/categories/{id}/posts` - Category submissions
- `/categories/{id}/groups` - Registered teams
- `/groups/{id}/members` - Group membership
- `/posts/{id}/resources` - Post attachments
- `/posts/{id}/related` - Related posts

### Interaction Endpoints (RESTful style)
- `POST/DELETE /posts/{id}/like` - Like/unlike
- `GET/POST /posts/{id}/comments` - Comments
- `GET/POST /posts/{id}/ratings` - Ratings

### Admin Batch Operations
- `DELETE /admin/posts` - Batch delete
- `PATCH /admin/posts/status` - Batch status update
- `PATCH /admin/users/role` - Batch role update

## Schema Normalization

| Original (engine.py) | OpenAPI Spec |
|---------------------|--------------|
| `_body` internal field | `content` field |
| `deleted_at` exposed | Hidden, use `?include_deleted=true` |
| Cache fields | Marked `readOnly: true` |
| Scattered enums | Centralized in `components/schemas` |

## Integration with api-builder

After generating the spec:

```bash
# Generate OpenAPI spec
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py

# Use api-builder to scaffold backend
/api-builder .synnovator/openapi.yaml
```

## Authentication

The generated spec uses OAuth2 with three scopes:
- `read` - Read access to resources
- `write` - Write access to resources
- `admin` - Admin batch operations