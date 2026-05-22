---
name: convex-backend
description: Build real-time, reactive backend applications with Convex using TypeScript queries, mutations, and actions with automatic reactivity and optimistic updates. Use when building real-time collaborative applications, implementing reactive data synchronization, writing serverless backend functions, creating queries that auto-update, implementing mutations with transactional guarantees, handling file uploads with Convex storage, implementing authentication with Convex Auth, designing reactive database schemas, or building applications requiring instant data synchronization.
---

# Convex Backend - Realtime Database & Functions

## When to use this skill

- Building real-time collaborative applications
- Implementing reactive data that auto-updates
- Writing Convex queries, mutations, and actions
- Creating serverless backend functions with TypeScript
- Implementing optimistic UI updates
- Handling file uploads with Convex storage
- Implementing authentication with Convex Auth
- Designing Convex database schemas
- Building chat applications or live dashboards
- Creating applications with instant data sync
- Implementing scheduled functions (crons)
- Building backends without managing infrastructure

## When to use this skill

- Building realtime apps with Convex, implementing reactive queries, or managing backend logic with type-safe functions.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Building realtime apps with Convex, implementing reactive queries, or managing backend logic with type-safe functions.

## Core Concepts

### Queries (Read Data)
\`\`\`typescript
import { query } from './_generated/server';
import { v } from 'convex/values';

export const list = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query('users').collect();
  }
});

export const get = query({
  args: { id: v.id('users') },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.id);
  }
});
\`\`\`

### Mutations (Write Data)
\`\`\`typescript
import { mutation } from './_generated/server';

export const create = mutation({
  args: { name: v.string(), email: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db.insert('users', args);
  }
});
\`\`\`

## Resources
- [Convex Docs](https://docs.convex.dev/)
