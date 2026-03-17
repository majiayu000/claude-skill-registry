---
name: nestjs-graphql
description: Comprehensive guide for NestJS GraphQL development using Apollo and code-first approach. This skill should be used when writing GraphQL resolvers, mutations, queries, types, subscriptions, or implementing advanced features like field middleware, complexity limits, and custom scalars. Also covers project-specific patterns including zero-trust auth decorators and DataLoader integration.
---

# NestJS GraphQL Development Guide

## Overview

This skill provides comprehensive guidance for building GraphQL APIs with NestJS using Apollo Server and the code-first approach. It covers official NestJS GraphQL patterns plus project-specific implementations for authentication, authorization, and data loading.

## When to Use This Skill

- Writing new GraphQL resolvers, queries, or mutations
- Creating GraphQL object types, input types, or enums
- Implementing field resolvers or computed fields
- Adding subscriptions for real-time updates
- Configuring query complexity limits
- Creating custom scalars or field middleware
- Implementing authentication/authorization on GraphQL operations
- Setting up DataLoader for N+1 prevention

## Quick Reference

### Core Decorators

| Decorator | Purpose | Import |
|-----------|---------|--------|
| `@Resolver()` | Define resolver class | `@nestjs/graphql` |
| `@Query()` | Define query operation | `@nestjs/graphql` |
| `@Mutation()` | Define mutation operation | `@nestjs/graphql` |
| `@Args()` | Extract arguments | `@nestjs/graphql` |
| `@Context()` | Access GraphQL context | `@nestjs/graphql` |
| `@Parent()` | Access parent in field resolver | `@nestjs/graphql` |
| `@ResolveField()` | Define field resolver | `@nestjs/graphql` |
| `@ObjectType()` | Define GraphQL object type | `@nestjs/graphql` |
| `@InputType()` | Define GraphQL input type | `@nestjs/graphql` |
| `@Field()` | Define field on type | `@nestjs/graphql` |
| `@Extensions()` | Attach metadata to fields | `@nestjs/graphql` |

### Type Decorators

| Decorator | GraphQL Type | TypeScript Type |
|-----------|-------------|-----------------|
| `@Field(() => String)` | "String!" | `string` |
| `@Field(() => Int)` | "Int!" | `number` |
| `@Field(() => Float)` | "Float!" | `number` |
| `@Field(() => Boolean)` | "Boolean!" | `boolean` |
| `@Field(() => ID)` | "ID!" | `string` |
| `@Field(() => [String])` | "[String!]!" | `string[]` |
| `@Field({ nullable: true })` | `String` | `string \| null` |

## Code-First Patterns

### Basic Resolver Structure

```typescript
import { Args, Context, Mutation, Query, Resolver } from "@nestjs/graphql";
import { Public, Authed } from "../auth";

@Resolver(() => Entity)
export class EntityResolver {
  constructor(private readonly entityService: EntityService) {}

  @Query(() => Entity, { description: "Retrieve entity by ID" })
  @Authed()
  async entity(@Args("id", { type: () => ID }) id: string): Promise<Entity> {
    return this.entityService.findById(id);
  }

  @Mutation(() => Entity, { description: "Create new entity" })
  @Authed()
  async createEntity(
    @Args("input") input: CreateEntityInput,
    @Context() { req }: GraphQLContext
  ): Promise<Entity> {
    return this.entityService.create(input, req.user.id);
  }
}
```

### Object Type Definition

```typescript
import { Field, ID, ObjectType } from "@nestjs/graphql";

@ObjectType({ description: "Represents a user in the system" })
export class User {
  @Field(() => ID, { description: "Unique identifier" })
  id: string;

  @Field(() => String, { description: "User's email address" })
  email: string;

  @Field(() => String, { nullable: true, description: "Display name" })
  displayName?: string;

  @Field(() => Date, { description: "Account creation timestamp" })
  createdAt: Date;
}
```

### Input Type Definition

```typescript
import { Field, InputType } from "@nestjs/graphql";

@InputType({ description: "Input for creating a new user" })
export class CreateUserInput {
  @Field(() => String, { description: "User's email address" })
  email: string;

  @Field(() => String, { description: "User's password" })
  password: string;

  @Field(() => String, { nullable: true, description: "Optional display name" })
  displayName?: string;
}
```

## References

This skill includes detailed reference files for specific topics:

### references/quick-start.md
Setup and configuration for NestJS GraphQL with Apollo driver, module configuration, and code-first vs schema-first approaches.

### references/resolvers-mutations.md
Comprehensive guide to writing resolvers, queries, mutations, field resolvers, and using decorators like @Args, @Context, @Parent.

### references/types-scalars.md
Creating object types, input types, enums, interfaces, unions, and custom scalars. Includes mapped types (PartialType, PickType, etc.).

### references/advanced-features.md
Field middleware, query complexity, plugins, subscriptions, and extensions.

### references/project-patterns.md
Project-specific patterns including zero-trust auth decorators (@Public, @Authed, @Owner, @Groups), DataLoader integration, and GraphQL documentation standards.

## Common Tasks

### Adding a New Query

1. Add method to resolver with `@Query()` decorator
2. Add auth decorator (`@Public()`, `@Authed()`, or `@Groups()`)
3. Define return type in decorator: `@Query(() => ReturnType)`
4. Add description: `@Query(() => ReturnType, { description: "..." })`
5. Use `@Args()` for parameters with descriptions

### Adding a New Mutation

1. Add method to resolver with `@Mutation()` decorator
2. Add auth decorator (mutations typically use `@Authed()`)
3. Create InputType for complex inputs
4. Access user context via `@Context() { req }: GraphQLContext`

### Adding Field Resolver

```typescript
@ResolveField(() => [Comment], { description: "Entity's comments" })
async comments(
  @Parent() entity: Entity,
  @Context() { loaders }: GraphQLContext
): Promise<Comment[]> {
  return loaders.commentsLoader.load(entity.id);
}
```

### Adding DataLoader for New Entity

1. Add batch method to service: `getByIds(ids: string[]): Promise<Entity[]>`
2. Add loader type to `IDataLoaders` interface
3. Create loader in `DataLoaderService.getLoaders()`
4. Use in resolver: `loaders.entityLoader.load(id)`

See `references/project-patterns.md` for detailed DataLoader patterns.
