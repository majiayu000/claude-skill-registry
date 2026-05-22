---
name: api-version
description: Manage API versioning strategy for Hono routes in apps/api/src/v1. Use when creating new API versions or migrating endpoints between versions.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# API Versioning Skill

This skill helps you manage API versions in `apps/api/src/v1/` and prepare for future versions.

## When to Use This Skill

- Creating a new API version (v2, v3, etc.)
- Deprecating old API endpoints
- Migrating endpoints between versions
- Planning breaking changes
- Maintaining backward compatibility

## Current API Structure

```
apps/api/src/
├── v1/                  # Current API version
│   ├── routes/
│   │   ├── cars.ts      # Car registration endpoints
│   │   ├── coe.ts       # COE bidding endpoints
│   │   ├── pqp.ts       # PQP data endpoints
│   │   └── health.ts    # Health check
│   └── index.ts         # v1 router assembly
└── index.ts             # Main Hono app with versioned routes
```

## Versioning Strategy

### URL-Based Versioning

The project uses URL path versioning:
- `https://api.sgcarstrends.com/v1/cars`
- `https://api.sgcarstrends.com/v1/coe`
- Future: `https://api.sgcarstrends.com/v2/cars`

### Benefits
- Clear, explicit versioning visible in URLs
- Easy to cache and monitor per version
- Clients can migrate at their own pace
- Multiple versions can coexist

## Creating a New API Version

### Step 1: Create Version Directory

```bash
mkdir -p apps/api/src/v2/routes
```

### Step 2: Copy Existing Routes

Start with current v1 routes as a base:

```bash
cp -r apps/api/src/v1/routes/* apps/api/src/v2/routes/
```

### Step 3: Create Version Router

Create `apps/api/src/v2/index.ts`:

```typescript
import { Hono } from "hono";
import { carsRouter } from "./routes/cars";
import { coeRouter } from "./routes/coe";
import { pqpRouter } from "./routes/pqp";

const v2 = new Hono();

// Mount routes
v2.route("/cars", carsRouter);
v2.route("/coe", coeRouter);
v2.route("/pqp", pqpRouter);

export default v2;
```

### Step 4: Mount in Main App

Update `apps/api/src/index.ts`:

```typescript
import { Hono } from "hono";
import v1 from "./v1";
import v2 from "./v2";

const app = new Hono();

// Mount API versions
app.route("/v1", v1);
app.route("/v2", v2);  // Add new version

// Default to latest stable version
app.route("/", v1);  // Keep v1 as default or change to v2 when stable

export default app;
```

### Step 5: Implement Breaking Changes

Make necessary changes in v2 routes:

```typescript
// v1 response format
{
  "success": true,
  "data": [...],
  "count": 10
}

// v2 response format (breaking change)
{
  "data": [...],
  "meta": {
    "total": 10,
    "page": 1,
    "pageSize": 10
  }
}
```

## Migration Patterns

### 1. Gradual Migration

Keep both versions running:

```typescript
// v1/routes/cars.ts - deprecated but maintained
export const carsRouter = new Hono();

carsRouter.get("/", async (c) => {
  // Old logic
  return c.json({
    success: true,
    data: await getCars(),
  });
});

// v2/routes/cars.ts - new implementation
export const carsRouter = new Hono();

carsRouter.get("/", async (c) => {
  // New logic with pagination
  const { page = 1, limit = 10 } = c.req.query();
  const result = await getCars({ page, limit });

  return c.json({
    data: result.items,
    meta: {
      total: result.total,
      page,
      pageSize: limit,
    },
  });
});
```

### 2. Feature Flag Pattern

Use feature flags to test changes:

```typescript
import { Hono } from "hono";

export const carsRouter = new Hono();

carsRouter.get("/", async (c) => {
  const useV2Format = c.req.header("X-API-Version") === "2";

  const data = await getCars();

  if (useV2Format) {
    return c.json({ data, meta: { ... } });
  }

  // v1 format
  return c.json({ success: true, data });
});
```

### 3. Deprecation Warnings

Add deprecation headers to v1:

```typescript
import { Hono } from "hono";

export const carsRouter = new Hono();

// Add deprecation middleware
carsRouter.use("*", async (c, next) => {
  await next();
  c.header("X-API-Deprecation", "true");
  c.header("X-API-Sunset", "2025-12-31");
  c.header("Link", '<https://api.sgcarstrends.com/v2/cars>; rel="successor-version"');
});

carsRouter.get("/", async (c) => {
  // Existing logic
});
```

## Breaking Changes Checklist

When introducing breaking changes, consider:

- [ ] Response structure changes
- [ ] Required parameter additions
- [ ] Authentication method changes
- [ ] URL structure modifications
- [ ] HTTP method changes
- [ ] Header requirement changes
- [ ] Error format modifications
- [ ] Data type changes

## Version Documentation

Document versions in OpenAPI/Swagger:

```typescript
// apps/api/src/v2/openapi.ts
import { OpenAPIHono } from "@hono/zod-openapi";

const app = new OpenAPIHono();

app.openapi(
  {
    method: "get",
    path: "/cars",
    summary: "Get car registrations (v2)",
    deprecated: false,
    tags: ["Cars"],
    responses: {
      200: {
        description: "Success",
        content: {
          "application/json": {
            schema: carResponseSchema,
          },
        },
      },
    },
  },
  async (c) => {
    // Handler
  }
);
```

## Version Sunset Process

### 1. Announce Deprecation

- Update documentation
- Add deprecation headers
- Notify API consumers
- Set sunset date

### 2. Monitor Usage

Track v1 usage metrics:

```typescript
import { middleware } from "hono/middleware";

v1.use("*", async (c, next) => {
  // Log usage for monitoring
  console.log("v1 API usage:", {
    path: c.req.path,
    user: c.get("user")?.id,
    timestamp: new Date(),
  });

  await next();
});
```

### 3. Provide Migration Guide

Create migration documentation:

```markdown
# Migrating from v1 to v2

## Breaking Changes

### Response Format
**v1:**
\`\`\`json
{ "success": true, "data": [...] }
\`\`\`

**v2:**
\`\`\`json
{ "data": [...], "meta": { ... } }
\`\`\`

### Pagination
v2 includes built-in pagination:
- Query params: `?page=1&limit=10`
- Response includes `meta` with pagination info

## Migration Steps
1. Update base URL from `/v1` to `/v2`
2. Update response parsing to handle new format
3. Add pagination parameters if needed
4. Update error handling for new error format
```

### 4. Remove Old Version

After sunset date:

```bash
# Remove v1 directory
rm -rf apps/api/src/v1

# Update main app
# Remove v1 mounting from apps/api/src/index.ts
```

## Testing Multiple Versions

Test all active versions:

```bash
# Test v1
curl https://api.sgcarstrends.com/v1/cars

# Test v2
curl https://api.sgcarstrends.com/v2/cars

# Run version-specific tests
pnpm -F @sgcarstrends/api test -- src/v1
pnpm -F @sgcarstrends/api test -- src/v2
```

## Deployment Considerations

### Zero-Downtime Deployment

1. Deploy v2 alongside v1
2. Test v2 in production
3. Gradually route traffic to v2
4. Monitor error rates
5. Rollback if issues occur

### Environment Variables

Version-specific config:

```env
# v1 settings
V1_RATE_LIMIT=100
V1_CACHE_TTL=300

# v2 settings
V2_RATE_LIMIT=200
V2_CACHE_TTL=600
```

## Common Scenarios

### Scenario 1: Add Required Parameter

**v1:** Optional parameter
```typescript
carsRouter.get("/", async (c) => {
  const make = c.req.query("make"); // optional
  return c.json(await getCars({ make }));
});
```

**v2:** Required parameter (breaking change)
```typescript
carsRouter.get("/", async (c) => {
  const make = c.req.query("make");
  if (!make) {
    return c.json({ error: "make parameter required" }, 400);
  }
  return c.json(await getCars({ make }));
});
```

### Scenario 2: Change Data Format

**v1:** Flat structure
```typescript
{ id: 1, make: "Toyota", model: "Camry" }
```

**v2:** Nested structure (breaking change)
```typescript
{
  id: 1,
  vehicle: {
    make: "Toyota",
    model: "Camry"
  }
}
```

### Scenario 3: Rename Endpoint

**v1:** `/cars/list`
**v2:** `/cars` (breaking change - URL structure)

Solution: Redirect in v1
```typescript
v1.get("/cars/list", async (c) => {
  c.header("X-API-Deprecated", "true");
  c.header("Location", "/v2/cars");
  return c.redirect("/v2/cars", 301);
});
```

## References

- Hono documentation: Use Context7 for latest docs
- Related files:
  - `apps/api/src/v1/` - Current API version
  - `apps/api/src/index.ts` - Main app with version mounting
  - `apps/api/CLAUDE.md` - API service documentation

## Best Practices

1. **Semantic Versioning**: Use v1, v2, v3 (not v1.1, v1.2)
2. **Backward Compatibility**: Maintain old versions during migration period
3. **Documentation**: Document all breaking changes clearly
4. **Communication**: Announce deprecations well in advance
5. **Monitoring**: Track usage of deprecated endpoints
6. **Testing**: Maintain tests for all active versions
7. **Graceful Sunset**: Provide sufficient migration time (6-12 months)
8. **Error Messages**: Help users migrate with clear error messages
