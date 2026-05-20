---
name: convex-component-authoring
displayName: Convex Component Authoring
description: How to create, structure, and publish self-contained Convex components with proper isolation, exports, and dependency management
version: 1.0.0
author: Convex
tags: [convex, components, reusable, packages, npm]
---

# Convex Component Authoring

Create self-contained, reusable Convex components with proper isolation, exports, and dependency management for sharing across projects.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: https://docs.convex.dev/components
- Component Authoring: https://docs.convex.dev/components/authoring
- For broader context: https://docs.convex.dev/llms.txt

## Instructions

### What Are Convex Components?

Convex components are self-contained packages that include:
- Database tables (isolated from the main app)
- Functions (queries, mutations, actions)
- TypeScript types and validators
- Optional frontend hooks

### Component Structure

```
my-convex-component/
├── package.json
├── tsconfig.json
├── README.md
├── src/
│   ├── index.ts           # Main exports
│   ├── component.ts       # Component definition
│   ├── schema.ts          # Component schema
│   └── functions/
│       ├── queries.ts
│       ├── mutations.ts
│       └── actions.ts
└── convex.config.ts       # Component configuration
```

### Creating a Component

#### 1. Component Configuration

```typescript
// convex.config.ts
import { defineComponent } from "convex/server";

export default defineComponent("myComponent");
```

#### 2. Component Schema

```typescript
// src/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // Tables are isolated to this component
  items: defineTable({
    name: v.string(),
    data: v.any(),
    createdAt: v.number(),
  }).index("by_name", ["name"]),
  
  config: defineTable({
    key: v.string(),
    value: v.any(),
  }).index("by_key", ["key"]),
});
```

#### 3. Component Definition

```typescript
// src/component.ts
import { defineComponent, ComponentDefinition } from "convex/server";
import schema from "./schema";
import * as queries from "./functions/queries";
import * as mutations from "./functions/mutations";

const component = defineComponent("myComponent", {
  schema,
  functions: {
    ...queries,
    ...mutations,
  },
});

export default component;
```

#### 4. Component Functions

```typescript
// src/functions/queries.ts
import { query } from "../_generated/server";
import { v } from "convex/values";

export const list = query({
  args: {
    limit: v.optional(v.number()),
  },
  returns: v.array(v.object({
    _id: v.id("items"),
    name: v.string(),
    data: v.any(),
    createdAt: v.number(),
  })),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("items")
      .order("desc")
      .take(args.limit ?? 10);
  },
});

export const get = query({
  args: { name: v.string() },
  returns: v.union(v.object({
    _id: v.id("items"),
    name: v.string(),
    data: v.any(),
  }), v.null()),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("items")
      .withIndex("by_name", (q) => q.eq("name", args.name))
      .unique();
  },
});
```

```typescript
// src/functions/mutations.ts
import { mutation } from "../_generated/server";
import { v } from "convex/values";

export const create = mutation({
  args: {
    name: v.string(),
    data: v.any(),
  },
  returns: v.id("items"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("items", {
      name: args.name,
      data: args.data,
      createdAt: Date.now(),
    });
  },
});

export const update = mutation({
  args: {
    id: v.id("items"),
    data: v.any(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, { data: args.data });
    return null;
  },
});

export const remove = mutation({
  args: { id: v.id("items") },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.delete(args.id);
    return null;
  },
});
```

#### 5. Main Exports

```typescript
// src/index.ts
export { default as component } from "./component";
export * from "./functions/queries";
export * from "./functions/mutations";

// Export types for consumers
export type { Id } from "./_generated/dataModel";
```

### Using a Component

```typescript
// In the consuming app's convex/convex.config.ts
import { defineApp } from "convex/server";
import myComponent from "my-convex-component";

const app = defineApp();

app.use(myComponent, { name: "myComponent" });

export default app;
```

```typescript
// In the consuming app's code
import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

function MyApp() {
  // Access component functions through the app's API
  const items = useQuery(api.myComponent.list, { limit: 10 });
  const createItem = useMutation(api.myComponent.create);
  
  return (
    <div>
      {items?.map((item) => (
        <div key={item._id}>{item.name}</div>
      ))}
      <button onClick={() => createItem({ name: "New", data: {} })}>
        Add Item
      </button>
    </div>
  );
}
```

### Component Configuration Options

```typescript
// convex/convex.config.ts
import { defineApp } from "convex/server";
import myComponent from "my-convex-component";

const app = defineApp();

// Basic usage
app.use(myComponent);

// With custom name
app.use(myComponent, { name: "customName" });

// Multiple instances
app.use(myComponent, { name: "instance1" });
app.use(myComponent, { name: "instance2" });

export default app;
```

### Providing Component Hooks

```typescript
// src/hooks.ts
import { useQuery, useMutation } from "convex/react";
import { FunctionReference } from "convex/server";

// Type-safe hooks for component consumers
export function useMyComponent(api: {
  list: FunctionReference<"query">;
  create: FunctionReference<"mutation">;
}) {
  const items = useQuery(api.list, {});
  const createItem = useMutation(api.create);
  
  return {
    items,
    createItem,
    isLoading: items === undefined,
  };
}
```

### Publishing a Component

#### package.json

```json
{
  "name": "my-convex-component",
  "version": "1.0.0",
  "description": "A reusable Convex component",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": [
    "dist",
    "convex.config.ts"
  ],
  "scripts": {
    "build": "tsc",
    "prepublishOnly": "npm run build"
  },
  "peerDependencies": {
    "convex": "^1.0.0"
  },
  "devDependencies": {
    "convex": "^1.17.0",
    "typescript": "^5.0.0"
  },
  "keywords": [
    "convex",
    "component"
  ]
}
```

#### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "declaration": true,
    "outDir": "dist",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Examples

### Rate Limiter Component

```typescript
// rate-limiter/src/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  requests: defineTable({
    key: v.string(),
    timestamp: v.number(),
  })
    .index("by_key", ["key"])
    .index("by_key_and_time", ["key", "timestamp"]),
});
```

```typescript
// rate-limiter/src/functions/mutations.ts
import { mutation } from "../_generated/server";
import { v } from "convex/values";

export const checkLimit = mutation({
  args: {
    key: v.string(),
    limit: v.number(),
    windowMs: v.number(),
  },
  returns: v.object({
    allowed: v.boolean(),
    remaining: v.number(),
    resetAt: v.number(),
  }),
  handler: async (ctx, args) => {
    const now = Date.now();
    const windowStart = now - args.windowMs;
    
    // Clean old entries
    const oldEntries = await ctx.db
      .query("requests")
      .withIndex("by_key_and_time", (q) => 
        q.eq("key", args.key).lt("timestamp", windowStart)
      )
      .collect();
    
    for (const entry of oldEntries) {
      await ctx.db.delete(entry._id);
    }
    
    // Count current window
    const currentRequests = await ctx.db
      .query("requests")
      .withIndex("by_key", (q) => q.eq("key", args.key))
      .collect();
    
    const remaining = Math.max(0, args.limit - currentRequests.length);
    const allowed = remaining > 0;
    
    if (allowed) {
      await ctx.db.insert("requests", {
        key: args.key,
        timestamp: now,
      });
    }
    
    const oldestRequest = currentRequests[0];
    const resetAt = oldestRequest 
      ? oldestRequest.timestamp + args.windowMs 
      : now + args.windowMs;
    
    return { allowed, remaining: remaining - (allowed ? 1 : 0), resetAt };
  },
});
```

```typescript
// Usage in consuming app
import { useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

function useRateLimitedAction() {
  const checkLimit = useMutation(api.rateLimiter.checkLimit);
  
  return async (action: () => Promise<void>) => {
    const result = await checkLimit({
      key: "user-action",
      limit: 10,
      windowMs: 60000,
    });
    
    if (!result.allowed) {
      throw new Error(`Rate limited. Try again at ${new Date(result.resetAt)}`);
    }
    
    await action();
  };
}
```

## Best Practices

- Never run `npx convex deploy` unless explicitly instructed
- Never run any git commands unless explicitly instructed
- Keep component tables isolated (don't reference main app tables)
- Export clear TypeScript types for consumers
- Document all public functions and their arguments
- Use semantic versioning for component releases
- Include comprehensive README with examples
- Test components in isolation before publishing

## Common Pitfalls

1. **Cross-referencing tables** - Component tables should be self-contained
2. **Missing type exports** - Export all necessary types
3. **Hardcoded configuration** - Use component options for customization
4. **No versioning** - Follow semantic versioning
5. **Poor documentation** - Document all public APIs

## References

- Convex Documentation: https://docs.convex.dev/
- Convex LLMs.txt: https://docs.convex.dev/llms.txt
- Components: https://docs.convex.dev/components
- Component Authoring: https://docs.convex.dev/components/authoring
