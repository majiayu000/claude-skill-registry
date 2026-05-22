---
name: plugins
description: Use when creating custom Bknd plugins, extending functionality with hooks and events, or building reusable modules that add entities, endpoints, or middleware. Covers plugin architecture, lifecycle hooks, event system integration, and schema extension.
---

# Bknd Plugins

Bknd plugins allow you to extend functionality by hooking into the app lifecycle, adding entities, registering endpoints, and responding to events. Plugins guarantee their data structures are merged into the main schema.

## What You'll Learn

- Plugin structure and lifecycle hooks
- Creating custom plugins with schema extension
- Registering custom API endpoints
- Listening to and handling events
- Using built-in plugins
- Best practices for plugin development

## Plugin Structure

A plugin is a function that receives an `App` instance and returns a plugin configuration:

```typescript
import type { App, AppPlugin } from "bknd";

export const myPlugin: AppPlugin = (app: App) => ({
  name: "my-plugin",
  schema: () => { /* schema definition */ },
  beforeBuild: () => { /* before app builds */ },
  onBuilt: () => { /* after app builds */ },
  onServerInit: (server) => { /* when Hono server initializes */ },
  onBoot: () => { /* on each server boot */ },
  onFirstBoot: () => { /* only on first boot */ },
});
```

## Lifecycle Hooks

| Hook | When Called | Use Case |
|------|-------------|----------|
| `beforeBuild` | Before app builds | Register global configuration |
| `onBuilt` | After app builds | Register routes, event listeners |
| `onServerInit` | When Hono server initializes | Register middleware, CORS |
| `onBoot` | On each server start | Database seeding, cache warmup |
| `onFirstBoot` | Only on first boot ever | Initial data seeding |

## Creating a Simple Plugin

Add a custom entity and API endpoint:

```typescript
/** @jsxImportSource hono/jsx */
import type { App, AppPlugin } from "bknd";
import { em, entity, text } from "bknd";

export const pagesPlugin: AppPlugin = (app) => ({
  name: "pages-plugin",

  // Schema is automatically merged into app schema
  schema: () => em({
    pages: entity("pages", {
      title: text().required(),
      content: text().required(),
    }),
  }),

  onBuilt: () => {
    // Register custom endpoint
    app.server.get("/my-pages", async (c) => {
      const { data: pages } = await app.em.repo("pages").findMany({});
      return c.html(
        <body>
          <h1>Pages: {pages.length}</h1>
          <ul>
            {pages.map((page: any) => (
              <li key={page.id}>{page.title}</li>
            ))}
          </ul>
        </body>,
      );
    });
  },
});
```

Register in `bknd.config.ts`:

```typescript
import type { BkndConfig } from "bknd/adapter";
import { pagesPlugin } from "./pagesPlugin";

export default {
  options: {
    plugins: [pagesPlugin],
  }
} satisfies BkndConfig;
```

## Event System

Bknd provides a powerful event system for hooking into app lifecycle and database operations.

### Listening to Events

```typescript
import { AppEvents, DatabaseEvents } from "bknd";

export const myPlugin: AppPlugin = (app) => ({
  name: "my-plugin",
  onBuilt: () => {
    // Listen to app request events
    app.emgr.onEvent(AppEvents.AppRequest, async (event) => {
      console.log("Request received", event.params.request.url);
    });

    // Listen to database insert events
    app.emgr.onEvent(DatabaseEvents.MutatorInsertBefore, async (event) => {
      console.log("Inserting into", event.params.entity.name);
    });
  },
});
```

### Event Modes

By default, listeners are **async** (non-blocking). Change to **sync** for blocking operations:

```typescript
app.emgr.onEvent(
  DatabaseEvents.MutatorUpdateBefore,
  async (event) => {
    const { data } = event.params;
    // Validate and modify data before update
    return { ...data, updated_at: new Date() };
  },
  { mode: "sync" }, // Block main execution
);
```

### Event Listener ID

Always use a unique ID to prevent duplicate registrations in development (HMR):

```typescript
app.emgr.onEvent(
  DatabaseEvents.MutatorInsertBefore,
  async (event) => {
    // Your logic
  },
  { id: "my-plugin-insert" }, // Required for clean listener management
);
```

### Available Events

**App Events (`AppEvents`):**
- `AppConfigUpdatedEvent` - `{ app }` - Configuration updated
- `AppBuiltEvent` - `{ app }` - App built
- `AppFirstBoot` - `{ app }` - First boot ever
- `AppRequest` - `{ app, request }` - Request received
- `AppBeforeResponse` - `{ app, request, response }` - Before response sent

**Database Events (`DatabaseEvents`):**

*Mutator Events (insert, update, delete):*
- `MutatorInsertBefore` - `{ entity, data }` - Before insert (can modify)
- `MutatorInsertAfter` - `{ entity, data, changed }` - After insert
- `MutatorUpdateBefore` - `{ entity, entityId, data }` - Before update (can modify)
- `MutatorUpdateAfter` - `{ entity, entityId, data, changed }` - After update
- `MutatorDeleteBefore` - `{ entity, entityId }` - Before delete
- `MutatorDeleteAfter` - `{ entity, entityId, data }` - After delete

*Repository Events (find operations):*
- `RepositoryFindOneBefore` - `{ entity, options }` - Before findOne
- `RepositoryFindOneAfter` - `{ entity, options, data }` - After findOne
- `RepositoryFindManyBefore` - `{ entity, options }` - Before findMany
- `RepositoryFindManyAfter` - `{ entity, options, data }` - After findMany

**Media Events (`MediaEvents`):**
- `FileUploadedEvent` - `{ file } & FileUploadPayload` - File uploaded (can modify)
- `FileDeletedEvent` - `{ name }` - File deleted
- `FileAccessEvent` - `{ name }` - File accessed

## Built-in Plugins

### `timestamps` - Auto Timestamps

Adds `created_at` and `updated_at` fields to specified entities:

```typescript
import { timestamps } from "bknd/plugins";

export default {
  options: {
    plugins: [
      timestamps({
        entities: ["posts", "comments"],
        setUpdatedOnCreate: true, // Set updated_at on create (default: true)
      }),
    ],
  },
} satisfies BkndConfig;
```

**Important:** Cannot index `created_at` or `updated_at` fields because the timestamps plugin applies fields after index definitions are processed. Add timestamp fields manually if you need indexes.

### `emailOTP` - Email Authentication

Adds email OTP login/register functionality:

```typescript
import { emailOTP } from "bknd/plugins";
import { resendEmail } from "bknd";

export default {
  drivers: {
    email: resendEmail({ apiKey: process.env.RESEND_API_KEY }),
  },
  options: {
    plugins: [
      emailOTP({
        apiBasePath: "/api/auth/otp", // Default
        ttl: 600, // 10 minutes
        entity: "users_otp", // Default
        generateCode: (user) => Math.floor(100000 + Math.random() * 900000).toString(),
        generateEmail: (otp) => ({
          subject: "OTP Code",
          body: `Your OTP code is: ${otp.code}`,
        }),
        showActualErrors: false, // Hide errors in production
        allowExternalMutations: false, // Only plugin can mutate OTP entity
        sendEmail: true,
      }),
    ],
  },
} satisfies BkndConfig;
```

**Endpoints:**
- `POST /api/auth/otp/login` - Login with OTP
- `POST /api/auth/otp/register` - Register with OTP

**Request body:**
```json
{
  "email": "user@example.com",
  "code": "123456" // Optional - sends email if omitted
}
```

### `syncTypes` - Auto Type Generation

Generates TypeScript types on boot and build:

```typescript
import { syncTypes } from "bknd/plugins";
import { writeFile } from "node:fs/promises";

export default {
  options: {
    plugins: [
      syncTypes({
        enabled: true, // Disable in production
        write: async (et) => {
          await writeFile("bknd-types.d.ts", et.toString(), "utf-8");
        },
      }),
    ],
  },
} satisfies BkndConfig;
```

### `syncConfig` - Auto Config Export

Exports configuration to a file:

```typescript
import { syncConfig } from "bknd/plugins";
import { writeFile } from "node:fs/promises";

export default {
  options: {
    plugins: [
      syncConfig({
        enabled: true,
        write: async (config) => {
          await writeFile("config.json", JSON.stringify(config, null, 2), "utf-8");
        },
      }),
    ],
  },
} satisfies BkndConfig;
```

### `syncSecrets` - Auto Secrets Export

Exports secrets to a file (useful for generating `.env.example`):

```typescript
import { syncSecrets } from "bknd/plugins";
import { writeFile } from "node:fs/promises";

export default {
  options: {
    plugins: [
      syncSecrets({
        enabled: true,
        write: async (secrets) => {
          await writeFile(
            ".env.example",
            Object.entries(secrets)
              .map(([key]) => `${key}=`)
              .join("\n"),
          );
        },
      }),
    ],
  },
} satisfies BkndConfig;
```

### `showRoutes` - Route Logging

Logs all registered routes to console:

```typescript
import { showRoutes } from "bknd/plugins";

export default {
  options: {
    plugins: [
      showRoutes({
        once: true, // Show only once (on first build)
      }),
    ],
  },
} satisfies BkndConfig;
```

### `cloudflareImageOptimization` - Image Optimization

Adds Cloudflare Image Optimization:

```typescript
import { cloudflareImageOptimization } from "bknd/plugins";

export default {
  options: {
    plugins: [
      cloudflareImageOptimization({
        accessUrl: "/api/plugin/image/optimize", // Default
        resolvePath: "/api/media/file", // Default
        defaultOptions: {
          width: 1000,
          quality: 85,
        },
        cacheControl: "public, max-age=31536000, immutable",
      }),
    ],
  },
} satisfies BkndConfig;
```

**Usage:**
```
GET /api/plugin/image/optimize/image.jpg?width=1000&height=1000&format=webp
```

## Advanced Plugin Patterns

### Conditional Schema Registration

```typescript
export const conditionalPlugin: AppPlugin = (app) => ({
  name: "conditional-plugin",
  schema: () => {
    if (process.env.NODE_ENV === "development") {
      return em({
        dev_logs: entity("dev_logs", {
          message: text(),
        }),
      });
    }
  },
});
```

### Protecting Custom Entities

Prevent mutations to plugin entities:

```typescript
import { DatabaseEvents } from "bknd";

export const securePlugin: AppPlugin = (app) => ({
  name: "secure-plugin",
  schema: () => em({
    protected_data: entity("protected_data", {
      value: text(),
    }),
  }),
  onBuilt: () => {
    [DatabaseEvents.MutatorInsertBefore, DatabaseEvents.MutatorUpdateBefore].forEach((event) => {
      app.emgr.onEvent(
        event,
        (e) => {
          if (e.params.entity.name === "protected_data") {
            throw new Error("Direct mutations not allowed");
          }
        },
        { mode: "sync", id: "secure-plugin-guard" },
      );
    });
  },
});
```

### Auto-Seeding Data

```typescript
export const seedPlugin: AppPlugin = (app) => ({
  name: "seed-plugin",
  onFirstBoot: async () => {
    const { data: existing } = await app.em.repo("settings").findOne({ key: "initialized" });
    if (!existing) {
      await app.em.mutator("settings").insertOne({ key: "initialized", value: "true" });
      console.log("Seeded initial data");
    }
  },
});
```

### Registering Middleware

```typescript
export const corsPlugin: AppPlugin = (app) => ({
  name: "cors-plugin",
  onServerInit: (server) => {
    server.use(async (c, next) => {
      c.header("Access-Control-Allow-Origin", "*");
      c.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
      await next();
    });
  },
});
```

## Plugin Configuration Types

Always export TypeScript types for plugin options:

```typescript
import type { AppPlugin } from "bknd";

export type MyPluginOptions = {
  enabled?: boolean;
  apiKey?: string;
  endpoint?: string;
};

export function myPlugin(options: MyPluginOptions = {}): AppPlugin {
  return (app) => ({
    name: "my-plugin",
    // Use options in your plugin
    onBuilt: () => {
      if (options.enabled !== false) {
        console.log("Plugin enabled");
      }
    },
  });
}
```

## Best Practices

**DO:**
- Always provide unique listener IDs for event subscriptions
- Export TypeScript types for plugin configuration options
- Use `onBuilt` for registering routes and event listeners
- Use `onBoot` for database operations and caching
- Return modified data from sync event listeners to change behavior
- Use `sync` mode when you need to block or modify operations
- Use `async` mode (default) for logging and side effects
- Add validation for plugin options
- Document required dependencies (e.g., auth module, email driver)

**DON'T:**
- Register event listeners without IDs in development (memory leaks)
- Use `onFirstBoot` for every startup logic (use `onBoot` instead)
- Mutate data in async event listeners (changes won't apply)
- Forget to register listeners before the app builds
- Create circular dependencies between plugins
- Assume the app is fully initialized in `beforeBuild`
- Modify core Bknd entities in plugins (create your own)
- Skip error handling in custom endpoints

## Common Issues

**"Listener not firing"**
- Ensure you registered the listener in `onBuilt` or earlier
- Check that the event name matches (use `AppEvents` enum)

**"Memory leak in development"**
- Add `{ id: "plugin-name" }` to all `app.emgr.onEvent()` calls
- This prevents duplicate registrations during HMR

**"Event listener not blocking"**
- Set `{ mode: "sync" }` as the third parameter to `onEvent()`
- Default is async, which doesn't block the main flow

**"Schema not merged"**
- Ensure your `schema` function returns an `em()` call
- Check that the plugin is listed in `config.options.plugins`

**"Custom route not accessible"**
- Ensure you're using unique paths (avoid `/api/*` conflicts)
- Register routes in `onBuilt`, not `beforeBuild`

**"Database locked during seeding"**
- Use `app.em.fork()` for separate database contexts
- Handle concurrent access properly with transactions

## Next Steps

- **[Events & Hooks](https://docs.bknd.io/extending/events)** - Full event system reference
- **[Admin UI](https://docs.bknd.io/extending/admin)** - Extending the Admin UI
- **[Data Schema](data-schema)** - Understanding entity definitions
- **[Query](query)** - Query system integration
