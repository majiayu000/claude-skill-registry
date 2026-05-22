---
name: vendure-plugin-writing
description: Create production-ready Vendure plugins with @VendurePlugin decorator, NestJS dependency injection, lifecycle hooks, and configuration patterns. Use when developing new Vendure plugins or extending existing ones.
version: 1.0.0
---

# Vendure Plugin Writing

## Purpose

Guide creation of Vendure plugins following official best practices and production patterns.

## When NOT to Use

- Reviewing existing plugins (use vendure-plugin-reviewing)
- GraphQL-specific work (use vendure-graphql-writing)
- Entity definition only (use vendure-entity-writing)
- Admin UI only (use vendure-admin-ui-writing)

---

## FORBIDDEN Patterns

- Missing @VendurePlugin decorator
- Not importing PluginCommonModule
- Not using @Injectable on services
- Hardcoded values instead of plugin configuration
- Direct database access bypassing services
- Missing async/await on lifecycle hooks
- Constructor injection in strategies (use init() method)
- Skipping default values for optional config

---

## REQUIRED Patterns

- @VendurePlugin() decorator with proper metadata
- PluginCommonModule in imports array
- Configuration interface with sensible defaults
- Static init() method for plugin configuration
- @Injectable() decorator on all services
- Proper DI via constructor injection in services
- Lifecycle hooks when needed (onApplicationBootstrap)

---

## Workflow

### Step 1: Define Plugin Configuration Interface

```typescript
// my-plugin.types.ts
export interface MyPluginOptions {
  enabled?: boolean;
  apiKey?: string;
  maxRetries?: number;
}

// Default configuration
export const defaultMyPluginOptions: Required<MyPluginOptions> = {
  enabled: true,
  apiKey: "",
  maxRetries: 3,
};
```

### Step 2: Create the Plugin Class

```typescript
// my-plugin.plugin.ts
import { PluginCommonModule, VendurePlugin } from "@vendure/core";
import { MyService } from "./my.service";
import { MyEntity } from "./my.entity";
import { MyResolver } from "./my.resolver";
import { MyPluginOptions, defaultMyPluginOptions } from "./my-plugin.types";

@VendurePlugin({
  imports: [PluginCommonModule],
  providers: [MyService],
  entities: [MyEntity],
  adminApiExtensions: {
    schema: graphqlAdminSchema,
    resolvers: [MyResolver],
  },
})
export class MyPlugin {
  static options: Required<MyPluginOptions>;

  static init(options: MyPluginOptions = {}): typeof MyPlugin {
    this.options = {
      ...defaultMyPluginOptions,
      ...options,
    };
    return MyPlugin;
  }
}
```

### Step 3: Create Injectable Service

```typescript
// my.service.ts
import { Injectable } from "@nestjs/common";
import { TransactionalConnection, RequestContext } from "@vendure/core";
import { MyEntity } from "./my.entity";

@Injectable()
export class MyService {
  constructor(private connection: TransactionalConnection) {}

  async findAll(ctx: RequestContext): Promise<MyEntity[]> {
    return this.connection.getRepository(ctx, MyEntity).find();
  }

  async create(ctx: RequestContext, input: CreateInput): Promise<MyEntity> {
    const entity = new MyEntity(input);
    return this.connection.getRepository(ctx, MyEntity).save(entity);
  }
}
```

### Step 4: Add Lifecycle Hooks (If Needed)

```typescript
import { OnApplicationBootstrap, OnApplicationShutdown } from "@nestjs/common";
import { Injector } from "@vendure/core";

@VendurePlugin({
  // ... metadata
})
export class MyPlugin implements OnApplicationBootstrap, OnApplicationShutdown {
  static options: Required<MyPluginOptions>;

  constructor(private injector: Injector) {}

  async onApplicationBootstrap(): Promise<void> {
    // Initialize strategies, start background tasks, etc.
    if (MyPlugin.options.enabled) {
      const service = this.injector.get(MyService);
      await service.initialize();
    }
  }

  async onApplicationShutdown(): Promise<void> {
    // Cleanup resources
  }
}
```

### Step 5: Register Plugin in vendure-config.ts

```typescript
import { MyPlugin } from "./plugins/my-plugin/my-plugin.plugin";

export const config: VendureConfig = {
  plugins: [
    MyPlugin.init({
      enabled: true,
      apiKey: process.env.MY_API_KEY,
      maxRetries: 5,
    }),
  ],
};
```

---

## Plugin Structure Template

```
my-plugin/
├── my-plugin.plugin.ts      # Main plugin file
├── my-plugin.types.ts       # Configuration types
├── my.service.ts            # Business logic
├── my.entity.ts             # Database entity
├── my.resolver.ts           # GraphQL resolver
├── schema.ts                # GraphQL schema extensions
├── strategies/              # Custom strategies
│   └── my.strategy.ts
├── ui/                      # Admin UI extensions
│   └── providers.ts
└── index.ts                 # Public exports
```

---

## Examples

### Example 1: Simple Analytics Plugin

```typescript
import {
  PluginCommonModule,
  VendurePlugin,
  EventBus,
  ProductEvent,
} from "@vendure/core";
import { OnApplicationBootstrap } from "@nestjs/common";

interface AnalyticsOptions {
  trackingId: string;
}

@VendurePlugin({
  imports: [PluginCommonModule],
})
export class AnalyticsPlugin implements OnApplicationBootstrap {
  static options: AnalyticsOptions;

  constructor(private eventBus: EventBus) {}

  static init(options: AnalyticsOptions): typeof AnalyticsPlugin {
    this.options = options;
    return AnalyticsPlugin;
  }

  async onApplicationBootstrap(): Promise<void> {
    this.eventBus.ofType(ProductEvent).subscribe((event) => {
      console.log(`Product ${event.type}: ${event.entity.name}`);
      // Send to analytics service
    });
  }
}
```

### Example 2: Plugin with Custom Strategy

```typescript
import { PluginCommonModule, VendurePlugin, Injector } from "@vendure/core";
import { OnApplicationBootstrap, OnApplicationShutdown } from "@nestjs/common";
import { MyStrategy, DefaultMyStrategy } from "./strategies/my.strategy";

interface PluginOptions {
  strategy?: MyStrategy;
}

@VendurePlugin({
  imports: [PluginCommonModule],
})
export class StrategyPlugin
  implements OnApplicationBootstrap, OnApplicationShutdown
{
  static options: Required<PluginOptions>;

  constructor(private injector: Injector) {}

  static init(options: PluginOptions = {}): typeof StrategyPlugin {
    this.options = {
      strategy: new DefaultMyStrategy(),
      ...options,
    };
    return StrategyPlugin;
  }

  async onApplicationBootstrap(): Promise<void> {
    // Initialize strategy with injector for DI
    if (typeof StrategyPlugin.options.strategy.init === "function") {
      await StrategyPlugin.options.strategy.init(this.injector);
    }
  }

  async onApplicationShutdown(): Promise<void> {
    if (typeof StrategyPlugin.options.strategy.destroy === "function") {
      await StrategyPlugin.options.strategy.destroy();
    }
  }
}
```

### Example 3: Plugin with Admin/Shop API Extensions

```typescript
import { PluginCommonModule, VendurePlugin } from "@vendure/core";
import { gql } from "graphql-tag";
import { MyService } from "./my.service";
import { MyAdminResolver, MyShopResolver } from "./my.resolver";

const graphqlAdminSchema = gql`
  extend type Query {
    myAdminData: [MyType!]!
  }
  extend type Mutation {
    updateMyData(input: UpdateInput!): MyType!
  }
`;

const graphqlShopSchema = gql`
  extend type Query {
    myPublicData: [MyType!]!
  }
`;

@VendurePlugin({
  imports: [PluginCommonModule],
  providers: [MyService],
  adminApiExtensions: {
    schema: graphqlAdminSchema,
    resolvers: [MyAdminResolver],
  },
  shopApiExtensions: {
    schema: graphqlShopSchema,
    resolvers: [MyShopResolver],
  },
})
export class ApiPlugin {}
```

---

## Common Patterns

### Accessing Plugin Options in Service

```typescript
@Injectable()
export class MyService {
  get options() {
    return MyPlugin.options;
  }

  async doSomething() {
    if (this.options.enabled) {
      // Use this.options.apiKey
    }
  }
}
```

### Custom Fields Configuration

```typescript
@VendurePlugin({
  imports: [PluginCommonModule],
  configuration: (config) => {
    config.customFields.Product.push({
      name: "myCustomField",
      type: "string",
      label: [{ languageCode: "en", value: "My Custom Field" }],
    });
    return config;
  },
})
export class CustomFieldsPlugin {}
```

### Plugin Dependencies

```typescript
// If plugin depends on another plugin's services
@VendurePlugin({
  imports: [PluginCommonModule, OtherPlugin],
  providers: [MyService],
})
export class DependentPlugin {}
```

---

## Troubleshooting

| Problem                  | Cause                  | Solution                                  |
| ------------------------ | ---------------------- | ----------------------------------------- |
| Service not found        | Not in providers array | Add to @VendurePlugin({ providers: [] })  |
| Entity not created       | Not in entities array  | Add to @VendurePlugin({ entities: [] })   |
| Options undefined        | init() not called      | Call MyPlugin.init() in vendure-config.ts |
| Circular dependency      | Improper imports       | Use forwardRef() or restructure modules   |
| Strategy not initialized | Missing init() call    | Implement OnApplicationBootstrap          |

---

## Related Skills

- **vendure-plugin-reviewing** - Audit plugin for violations
- **vendure-graphql-writing** - GraphQL schema and resolvers
- **vendure-entity-writing** - Database entities
- **vendure-admin-ui-writing** - Admin UI extensions

---

## External Documentation

### Context7

```
mcp__context7__get-library-docs
context7CompatibleLibraryID: "/vendure-ecommerce/vendure"
topic: "plugins"
```

### Official Docs

- https://docs.vendure.io/guides/developer-guide/plugins/
- https://docs.vendure.io/guides/developer-guide/plugin-lifecycle/
