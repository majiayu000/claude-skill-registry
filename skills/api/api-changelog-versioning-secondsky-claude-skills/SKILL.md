---
name: api-changelog-versioning
description: Creates comprehensive API changelogs documenting breaking changes, deprecations, and migration strategies for API consumers. Use when managing API versions, communicating breaking changes, or creating upgrade guides.
---

# API Changelog & Versioning

Document API changes with clear migration paths and deprecation timelines.

## Changelog Structure

```markdown
# API Changelog

## v3.0.0 (2025-01-15) - Breaking Changes

### Breaking Changes
- Response format now follows JSON:API specification
- Authentication switched from API tokens to JWT Bearer

### Migration Steps
1. Update base URL to `/api/v3`
2. Replace `Authorization: Token xxx` with `Authorization: Bearer xxx`
3. Update response parsing for new envelope format

## v2.5.0 (2024-12-01) - Features

### New Features
- Webhook support for order events
- Batch operations endpoint
- Field filtering via `?fields=` parameter

### Improvements
- 56% faster response times on /products
- Enhanced error messages with field-specific suggestions
```

## Deprecation Schedule

| Version | Status | Support Until |
|---------|--------|---------------|
| v3.x | Current | Full support |
| v2.x | Maintenance | 2025-06-01 |
| v1.x | EOL | Unsupported |

## Version Support Policy

- **Current**: Full support, new features
- **Maintenance**: Bug fixes and security only
- **EOL**: No support, remove from docs

## Migration Guide Template

```markdown
## Migrating from v2 to v3

### Before (v2)
```json
{ "user_name": "john" }
```

### After (v3)
```json
{ "data": { "type": "user", "attributes": { "name": "john" } } }
```

### Steps
1. Update SDK to v3.x
2. Modify response handlers
3. Test in staging environment
4. Update production
```

## Best Practices

- Provide 3-6 months deprecation notice
- Include before/after code examples
- Mark breaking changes prominently
- Maintain backward compatibility when feasible
- Version via URL path (`/api/v1/`) for clarity
