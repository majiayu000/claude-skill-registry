---
name: vendure-developing
description: Develop Vendure e-commerce plugins, extend GraphQL APIs, create Admin UI components, and define database entities. Use vendure-expert agent for comprehensive guidance across all Vendure development domains.
version: 1.0.0
---

# Vendure Development

## Purpose

Entry point for all Vendure development tasks. Provides quick reference and guides to the vendure-expert agent for coordinated multi-domain guidance.

## When NOT to Use

- Non-Vendure e-commerce platforms (Shopify, Magento, etc.)
- Basic TypeScript/NestJS without Vendure context
- Frontend-only React without Vendure Admin UI

## Quick Start: Use the Agent

For comprehensive Vendure guidance, use the **`vendure-expert`** agent:

```
Task(subagent_type: "vendure-expert", prompt: "Your Vendure task here")
```

The agent coordinates 9 specialized skills:

- Plugin development (writing + reviewing)
- GraphQL API (writing + reviewing)
- Entity/Database (writing + reviewing)
- Admin UI (writing + reviewing)
- Delivery/shipping features (specialized)

---

## Vendure Architecture Quick Reference

### 6 Core Domains

| Domain         | Key Concepts                                         |
| -------------- | ---------------------------------------------------- |
| **Plugins**    | @VendurePlugin, NestJS DI, lifecycle hooks           |
| **GraphQL**    | Dual APIs (Shop/Admin), RequestContext, gql template |
| **Entities**   | VendureEntity, TypeORM, migrations, custom fields    |
| **Admin UI**   | React/Angular, UI DevKit, lazy loading               |
| **Strategies** | InjectableStrategy, custom logic                     |
| **Events**     | EventBus, transaction-safe subscriptions             |

### Plugin Scaffold

```typescript
import { PluginCommonModule, VendurePlugin } from "@vendure/core";

@VendurePlugin({
  imports: [PluginCommonModule],
  providers: [MyService],
  entities: [MyEntity],
  adminApiExtensions: {
    schema: gql`...`,
    resolvers: [MyResolver],
  },
})
export class MyPlugin {
  static init(options: MyPluginOptions) {
    this.options = options;
    return MyPlugin;
  }
}
```

### GraphQL Resolver Pattern

```typescript
import { Ctx, RequestContext, Query, Resolver } from "@vendure/core";
import { Allow, Permission } from "@vendure/core";

@Resolver()
export class MyResolver {
  constructor(private myService: MyService) {}

  @Query()
  @Allow(Permission.ReadSettings)
  async myQuery(@Ctx() ctx: RequestContext): Promise<MyType[]> {
    return this.myService.findAll(ctx);
  }
}
```

### Entity Pattern

```typescript
import { VendureEntity, DeepPartial } from "@vendure/core";
import { Entity, Column, ManyToOne } from "typeorm";

@Entity()
export class MyEntity extends VendureEntity {
  constructor(input?: DeepPartial<MyEntity>) {
    super(input);
  }

  @Column()
  name: string;

  @ManyToOne(() => OtherEntity)
  relation: OtherEntity;
}
```

### Admin UI Extension

```typescript
// providers.ts
import { addNavMenuSection } from "@vendure/admin-ui/react";

export default [
  addNavMenuSection(
    {
      id: "my-section",
      label: "My Feature",
      items: [
        {
          id: "my-page",
          label: "My Page",
          routerLink: ["/extensions/my-feature"],
          icon: "cog",
        },
      ],
    },
    "settings",
  ),
];
```

---

## FORBIDDEN Patterns

### Plugin Development

- Missing @VendurePlugin decorator
- Not using NestJS DI (@Injectable)
- Hardcoded values instead of plugin config
- Direct database access bypassing services

### GraphQL

- Missing @Ctx() RequestContext parameter
- Bypassing @Allow() permission decorator
- Mixing Shop/Admin schema types
- Not using gql template literal

### Entities

- Not extending VendureEntity
- Missing @Entity() decorator
- No migration file created
- Using `any` type

### Admin UI

- Not lazy loading routes
- Hardcoded strings (not using i18n)
- Missing loading/error states
- Not handling permissions

---

## REQUIRED Patterns

### RequestContext Threading

```typescript
// ALWAYS pass ctx through service calls
async myResolver(@Ctx() ctx: RequestContext) {
  return this.service.findAll(ctx);  // Pass ctx!
}
```

### Permission Decorators

```typescript
@Query()
@Allow(Permission.ReadCatalog)  // ALWAYS specify permissions
async products(@Ctx() ctx: RequestContext) { }
```

### Entity Input Types

```typescript
// Use DeepPartial for constructor input
constructor(input?: DeepPartial<MyEntity>) {
  super(input);
}
```

### InputMaybe Handling

```typescript
// Check BOTH undefined AND null for GraphQL inputs
if (input.field !== undefined && input.field !== null) {
  entity.field = input.field;
}
```

---

## Domain Skill Decision Tree

```
Task Type
    │
    ├─> Creating/modifying plugin structure
    │   └─> vendure-plugin-writing
    │
    ├─> Reviewing plugin code
    │   └─> vendure-plugin-reviewing
    │
    ├─> Extending GraphQL schema or resolvers
    │   └─> vendure-graphql-writing
    │
    ├─> Reviewing GraphQL code
    │   └─> vendure-graphql-reviewing
    │
    ├─> Creating/modifying entities
    │   └─> vendure-entity-writing
    │
    ├─> Reviewing entity definitions
    │   └─> vendure-entity-reviewing
    │
    ├─> Building Admin UI components
    │   └─> vendure-admin-ui-writing
    │
    ├─> Reviewing Admin UI code
    │   └─> vendure-admin-ui-reviewing
    │
    └─> Delivery/shipping features
        └─> vendure-delivery-plugin
```

---

## Common Patterns

### Dual API Separation

```typescript
// Admin API - full access
export const graphqlAdminSchema = gql`
  extend type Query {
    myAdminQuery: [MyType!]!
  }
  extend type Mutation {
    updateMyType(input: UpdateInput!): MyType!
  }
`;

// Shop API - customer-facing, read-only or limited
export const graphqlShopSchema = gql`
  extend type Query {
    myPublicQuery: [MyType!]!
  }
`;
```

### Service Pattern with RequestContext

```typescript
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

### Transaction Decorator

```typescript
@Mutation()
@Transaction()  // Wrap in database transaction
@Allow(Permission.UpdateSettings)
async updateMyEntity(
  @Ctx() ctx: RequestContext,
  @Args() { input }: { input: UpdateInput }
): Promise<MyEntity> {
  return this.service.update(ctx, input);
}
```

---

## Examples

### Example 1: Create a Simple Plugin

**Task:** Create a plugin that tracks product views.

**Approach:**

1. Use vendure-plugin-writing for plugin scaffold
2. Use vendure-entity-writing for ProductView entity
3. Use vendure-graphql-writing for query extension

**Result:**

```typescript
@VendurePlugin({
  imports: [PluginCommonModule],
  entities: [ProductViewEntity],
  providers: [ProductViewService],
  shopApiExtensions: {
    schema: gql`
      extend type Query {
        productViews(productId: ID!): Int!
      }
    `,
    resolvers: [ProductViewResolver],
  },
})
export class ProductViewsPlugin {}
```

### Example 2: Add Admin UI Page

**Task:** Add a settings page to manage plugin configuration.

**Approach:**

1. Use vendure-admin-ui-writing for React components
2. Register route and navigation item
3. Use DataService for API calls

**Result:**

```tsx
// pages/SettingsPage.tsx
export function SettingsPage() {
  const dataService = useInjector(DataService);
  const [settings, setSettings] = useState<Settings>();

  useEffect(() => {
    dataService
      .query(GetSettingsDocument)
      .stream$.subscribe((result) => setSettings(result.mySettings));
  }, []);

  return <SettingsForm settings={settings} />;
}
```

### Example 3: Review Plugin Code

**Task:** Audit a plugin for security and best practices.

**Approach:**

1. Use vendure-plugin-reviewing for plugin structure
2. Use vendure-graphql-reviewing for resolver patterns
3. Use vendure-entity-reviewing for database patterns

**Checks:**

- RequestContext passed through all service calls
- Permissions declared on all resolvers
- No direct database queries (use TransactionalConnection)
- Proper error handling

---

## Troubleshooting

| Problem              | Cause                        | Solution                                |
| -------------------- | ---------------------------- | --------------------------------------- |
| Entity not found     | Not in plugin entities array | Add to @VendurePlugin({ entities: [] }) |
| Resolver not called  | Not in resolvers array       | Add to apiExtensions.resolvers          |
| Permission denied    | Missing @Allow decorator     | Add @Allow(Permission.X)                |
| TypeScript errors    | Wrong import path            | Import from @vendure/core               |
| Admin UI not loading | Not lazy loaded              | Use React.lazy() for routes             |

---

## External Documentation

### Context7 (Recommended)

```
mcp__context7__get-library-docs
context7CompatibleLibraryID: "/vendure-ecommerce/vendure"
topic: "plugins" or "entities" or "graphql" etc.
```

### Official Docs

- https://docs.vendure.io/guides/developer-guide/
- https://docs.vendure.io/reference/typescript-api/

---

## Related Agent

For comprehensive multi-domain Vendure guidance, use the **`vendure-expert`** agent.

The agent coordinates all 9 Vendure skills and provides:

- Full plugin lifecycle guidance
- Security and quality audits
- Best practices enforcement
- Domain-specific patterns
