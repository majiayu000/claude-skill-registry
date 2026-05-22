---
name: api-versioning-strategy
description: Implements API versioning using URL paths, headers, or query parameters with backward compatibility and deprecation strategies. Use when managing multiple API versions, planning breaking changes, or designing migration paths.
---

# API Versioning Strategy

Choose and implement API versioning approaches with proper deprecation timelines.

## Versioning Methods

| Method | Example | Pros | Cons |
|--------|---------|------|------|
| URL Path | `/api/v1/users` | Clear, cache-friendly | URL clutter |
| Header | `API-Version: 1` | Clean URLs | Hidden, harder to test |
| Query | `?version=1` | Easy to use | Not RESTful |

## URL Path Versioning (Recommended)

```javascript
const v1Router = require('./routes/v1');
const v2Router = require('./routes/v2');

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);
```

## Version Adapter Pattern

```javascript
// Transform between versions
const v1ToV2 = (v1Response) => ({
  data: {
    type: 'user',
    id: v1Response.user_id,
    attributes: {
      name: v1Response.user_name,
      email: v1Response.email
    }
  }
});
```

## Deprecation Headers

```javascript
app.use('/api/v1', (req, res, next) => {
  res.setHeader('Deprecation', 'true');
  res.setHeader('Sunset', 'Sat, 01 Jun 2025 00:00:00 GMT');
  res.setHeader('Link', '</api/v2>; rel="successor-version"');
  next();
});
```

## Safe vs Breaking Changes

**Safe Changes** (no version bump):
- Adding optional fields
- Adding new endpoints
- Adding optional parameters

**Breaking Changes** (requires new version):
- Removing fields
- Changing field types
- Restructuring responses
- Removing endpoints

## Deprecation Timeline

| Phase | Duration | Actions |
|-------|----------|---------|
| Deprecated | 3 months | Add headers, docs |
| Sunset Announced | 3 months | Email users |
| Read-Only | 1 month | Disable writes |
| Shutdown | - | Return 410 Gone |

## Best Practices

- Support N-1 versions minimum
- Provide 6+ months migration window
- Include migration guides with code examples
- Monitor version usage to inform deprecation
