---
name: vendure-graphql-writing
description: Extend Vendure GraphQL schema with custom types, queries, mutations, and resolvers. Handles RequestContext threading, permissions, and dual Shop/Admin API separation. Use when adding GraphQL endpoints to Vendure.
version: 1.0.0
---

# Vendure GraphQL Writing

## Purpose

Guide creation of GraphQL schema extensions and resolvers in Vendure following official patterns.

## When NOT to Use

- Plugin structure only (use vendure-plugin-writing)
- Entity definition only (use vendure-entity-writing)
- Reviewing existing code (use vendure-graphql-reviewing)

---

## FORBIDDEN Patterns

- Missing @Ctx() RequestContext parameter
- Not using @Resolver() decorator
- Bypassing @Allow() permission decorator
- Returning raw entities without proper types
- Mixing Shop and Admin schema types
- Using hardcoded strings in gql schema
- Missing error handling in resolvers

---

## REQUIRED Patterns

- @Resolver() decorator on resolver classes
- @Ctx() ctx: RequestContext as first parameter
- @Allow() decorator specifying permissions
- gql template literal for schema definition
- Separate Admin and Shop schema files
- Proper input types for mutations
- Service injection via constructor

---

## Workflow

### Step 1: Define GraphQL Schema

```typescript
// schema.ts
import { gql } from "graphql-tag";

// Admin API schema - full access
export const graphqlAdminSchema = gql`
  type MyCustomType {
    id: ID!
    name: String!
    createdAt: DateTime!
    internalNotes: String # Admin-only field
  }

  input CreateMyTypeInput {
    name: String!
  }

  input UpdateMyTypeInput {
    name: String
  }

  extend type Query {
    myCustomTypes: [MyCustomType!]!
    myCustomType(id: ID!): MyCustomType
  }

  extend type Mutation {
    createMyCustomType(input: CreateMyTypeInput!): MyCustomType!
    updateMyCustomType(id: ID!, input: UpdateMyTypeInput!): MyCustomType!
    deleteMyCustomType(id: ID!): Boolean!
  }
`;

// Shop API schema - customer-facing
export const graphqlShopSchema = gql`
  type MyCustomType {
    id: ID!
    name: String!
    # internalNotes excluded for customers
  }

  extend type Query {
    myCustomTypes: [MyCustomType!]! # Read-only
  }
`;
```

### Step 2: Create Admin Resolver

```typescript
// admin.resolver.ts
import { Args, Mutation, Query, Resolver } from "@nestjs/graphql";
import {
  Allow,
  Ctx,
  Permission,
  RequestContext,
  Transaction,
} from "@vendure/core";
import { MyService } from "./my.service";
import { MyEntity } from "./my.entity";

@Resolver()
export class MyAdminResolver {
  constructor(private myService: MyService) {}

  @Query()
  @Allow(Permission.ReadSettings)
  async myCustomTypes(@Ctx() ctx: RequestContext): Promise<MyEntity[]> {
    return this.myService.findAll(ctx);
  }

  @Query()
  @Allow(Permission.ReadSettings)
  async myCustomType(
    @Ctx() ctx: RequestContext,
    @Args() args: { id: string },
  ): Promise<MyEntity | null> {
    return this.myService.findOne(ctx, args.id);
  }

  @Mutation()
  @Transaction()
  @Allow(Permission.UpdateSettings)
  async createMyCustomType(
    @Ctx() ctx: RequestContext,
    @Args() args: { input: CreateMyTypeInput },
  ): Promise<MyEntity> {
    return this.myService.create(ctx, args.input);
  }

  @Mutation()
  @Transaction()
  @Allow(Permission.UpdateSettings)
  async updateMyCustomType(
    @Ctx() ctx: RequestContext,
    @Args() args: { id: string; input: UpdateMyTypeInput },
  ): Promise<MyEntity> {
    return this.myService.update(ctx, args.id, args.input);
  }

  @Mutation()
  @Transaction()
  @Allow(Permission.DeleteSettings)
  async deleteMyCustomType(
    @Ctx() ctx: RequestContext,
    @Args() args: { id: string },
  ): Promise<boolean> {
    return this.myService.delete(ctx, args.id);
  }
}
```

### Step 3: Create Shop Resolver

```typescript
// shop.resolver.ts
import { Args, Query, Resolver } from "@nestjs/graphql";
import { Allow, Ctx, Permission, RequestContext } from "@vendure/core";
import { MyService } from "./my.service";

@Resolver()
export class MyShopResolver {
  constructor(private myService: MyService) {}

  @Query()
  @Allow(Permission.Public) // Available to all customers
  async myCustomTypes(@Ctx() ctx: RequestContext): Promise<MyEntity[]> {
    return this.myService.findAllPublic(ctx);
  }
}
```

### Step 4: Register in Plugin

```typescript
// my-plugin.plugin.ts
import { PluginCommonModule, VendurePlugin } from "@vendure/core";
import { graphqlAdminSchema, graphqlShopSchema } from "./schema";
import { MyAdminResolver } from "./admin.resolver";
import { MyShopResolver } from "./shop.resolver";
import { MyService } from "./my.service";

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
export class MyPlugin {}
```

---

## Common Patterns

### Field Resolver

```typescript
@Resolver("MyCustomType")
export class MyFieldResolver {
  constructor(private relatedService: RelatedService) {}

  @ResolveField()
  async relatedItems(
    @Ctx() ctx: RequestContext,
    @Parent() parent: MyEntity,
  ): Promise<RelatedEntity[]> {
    return this.relatedService.findByParentId(ctx, parent.id);
  }
}
```

### InputMaybe Handling (Critical)

```typescript
// GraphQL generates InputMaybe<T> for optional fields
// MUST check both undefined AND null

async update(ctx: RequestContext, id: ID, input: UpdateInput): Promise<MyEntity> {
  const entity = await this.findOne(ctx, id);

  // WRONG: Only checks undefined
  if (input.name !== undefined) {
    entity.name = input.name;  // Bug: null passes through!
  }

  // CORRECT: Check both
  if (input.name !== undefined && input.name !== null) {
    entity.name = input.name;
  }

  return this.connection.getRepository(ctx, MyEntity).save(entity);
}
```

### Permission Combinations

```typescript
// Public access
@Allow(Permission.Public)

// Authenticated customer
@Allow(Permission.Authenticated)

// Admin with specific permission
@Allow(Permission.ReadCatalog)
@Allow(Permission.UpdateCatalog)

// Multiple permissions (any of these)
@Allow(Permission.ReadOrder, Permission.Owner)

// Owner permission for customer's own resources
@Allow(Permission.Owner)
async myOrders(@Ctx() ctx: RequestContext): Promise<Order[]> {
  // ctx.activeUserId available for filtering
}
```

### Error Handling

```typescript
import { UserInputError, ForbiddenError } from '@vendure/core';

@Mutation()
@Transaction()
@Allow(Permission.UpdateSettings)
async updateMyType(
  @Ctx() ctx: RequestContext,
  @Args() args: { id: string; input: UpdateInput },
): Promise<MyEntity> {
  const entity = await this.myService.findOne(ctx, args.id);

  if (!entity) {
    throw new UserInputError(`Entity with id ${args.id} not found`);
  }

  if (!this.canUpdate(ctx, entity)) {
    throw new ForbiddenError();
  }

  return this.myService.update(ctx, args.id, args.input);
}
```

### Pagination

```typescript
// Schema
gql`
  type MyTypeList implements PaginatedList {
    items: [MyType!]!
    totalItems: Int!
  }

  extend type Query {
    myTypes(options: MyTypeListOptions): MyTypeList!
  }

  input MyTypeListOptions {
    skip: Int
    take: Int
    sort: MyTypeSortParameter
    filter: MyTypeFilterParameter
  }
`;

// Resolver
@Query()
@Allow(Permission.ReadSettings)
async myTypes(
  @Ctx() ctx: RequestContext,
  @Args() args: { options?: ListQueryOptions<MyEntity> },
): Promise<PaginatedList<MyEntity>> {
  return this.myService.findAll(ctx, args.options);
}
```

---

## Examples

### Example 1: Extending Product Type

```typescript
// Add custom field resolver to existing Product type
const schema = gql`
  extend type Product {
    customScore: Int!
  }
`;

@Resolver("Product")
export class ProductScoreResolver {
  constructor(private scoreService: ScoreService) {}

  @ResolveField()
  async customScore(
    @Ctx() ctx: RequestContext,
    @Parent() product: Product,
  ): Promise<number> {
    return this.scoreService.calculateScore(ctx, product.id);
  }
}
```

### Example 2: Shop API with Customer Verification

```typescript
// Verify customer owns the resource
@Resolver()
export class CustomerOrderResolver {
  constructor(
    private orderService: OrderService,
    private activeOrderService: ActiveOrderService,
  ) {}

  @Mutation()
  @Allow(Permission.Owner)
  async updateDeliveryDate(
    @Ctx() ctx: RequestContext,
    @Args() args: { orderId: string; date: string },
  ): Promise<Order> {
    // Verify ownership
    const activeOrder = await this.activeOrderService.getActiveOrder(ctx, {});
    if (!activeOrder || activeOrder.id !== args.orderId) {
      throw new ForbiddenError("Cannot modify this order");
    }

    return this.orderService.updateDeliveryDate(ctx, args.orderId, args.date);
  }
}
```

---

## Troubleshooting

| Problem             | Cause                      | Solution                            |
| ------------------- | -------------------------- | ----------------------------------- |
| Resolver not called | Not in resolvers array     | Add to adminApiExtensions.resolvers |
| Permission denied   | Missing @Allow             | Add @Allow(Permission.X) decorator  |
| Type error          | Schema/TypeScript mismatch | Regenerate types with codegen       |
| ctx undefined       | Missing @Ctx() decorator   | Add @Ctx() ctx: RequestContext      |
| Mutation not saving | Missing @Transaction()     | Add @Transaction() decorator        |

---

## Related Skills

- **vendure-graphql-reviewing** - Review GraphQL code
- **vendure-plugin-writing** - Plugin structure
- **vendure-entity-writing** - Entity definitions
