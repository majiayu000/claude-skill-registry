---
name: convex-mutations
description: This skill should be used when implementing Convex mutation functions. It provides comprehensive guidelines for defining, registering, calling, and scheduling mutations, including database operations, transactions, and scheduled job patterns.
---

# Convex Mutations Skill

This skill provides specialized guidance for implementing Convex mutation functions, including best practices for function definition, registration, database operations, and scheduling patterns.

## When to Use This Skill

Use this skill when:
- Defining new mutation functions to write or modify data in the Convex database
- Performing database operations (`insert`, `patch`, `replace`, `delete`)
- Calling mutations from other Convex functions
- Scheduling future mutations with `ctx.scheduler.runAfter`
- Handling transactional operations
- Coordinating mutations with actions for background processing

## Skill Resources

This skill includes comprehensive reference documentation in `references/mutation-guidelines.md` that covers:

### Core Mutation Development
- Function definition syntax using the new function syntax
- Mutation registration (`mutation` and `internalMutation`)
- Argument validators and their usage
- Function calling patterns (`ctx.runQuery` and `ctx.runMutation`)
- Function references (`api` and `internal` objects)
- File-based routing for mutation paths

### Database Operations
- `ctx.db.insert()` - Create new documents
- `ctx.db.patch()` - Shallow merge updates into existing documents
- `ctx.db.replace()` - Fully replace existing documents
- Error handling for missing documents
- Transaction semantics and consistency guarantees

### Advanced Mutation Features
- **Scheduling**: Using `ctx.scheduler.runAfter()` to queue background jobs
  - Scheduling mutations and actions for future execution
  - Understanding that auth state does NOT propagate to scheduled jobs
  - Using internal functions for scheduled jobs that need privileges
  - Avoiding tight loops and respecting 10-second minimum intervals
- **Transactional Behavior**: Understanding mutation transactions
  - Enqueuing scheduler jobs is transactional within mutations
  - Race condition prevention through transaction boundaries

### Function Composition
- Calling queries within mutations for validation
- Calling mutations from mutations
- Using return type annotations for same-file mutation calls

## How to Use This Skill

1. **Read the reference documentation** at `references/mutation-guidelines.md` to understand the complete mutation patterns
2. **Follow the syntax examples** for defining mutation functions with proper validators
3. **Use appropriate database operations** (`insert`, `patch`, `replace`) based on your needs
4. **Schedule background work** using `ctx.scheduler.runAfter` for long-running operations
5. **Remember auth state does NOT propagate** to scheduled jobs; use internal functions for privileged operations
6. **Leverage transactions** for consistency across multiple operations

## Key Mutation Guidelines

- ALWAYS include argument validators for all mutation functions
- Use `ctx.db.patch()` for partial updates and `ctx.db.replace()` for full replacements
- Use `ctx.scheduler.runAfter()` to schedule actions (e.g., AI responses, notifications)
- Remember that scheduled jobs have `null` auth state; use internal functions instead
- Mutations execute for at most 1 second and can write up to 8192 documents
- Return `null` implicitly if your mutation doesn't have an explicit return value
- Use return type annotations when calling mutations in the same file (TypeScript circularity workaround)

## Example: Mutation with Database Operation and Scheduling

```ts
import { mutation, internalAction } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

export const sendMessage = mutation({
  args: {
    channelId: v.id("channels"),
    authorId: v.id("users"),
    content: v.string(),
  },
  handler: async (ctx, args) => {
    // Validate channel and user exist
    const channel = await ctx.db.get(args.channelId);
    if (!channel) {
      throw new Error("Channel not found");
    }

    // Insert message into database
    await ctx.db.insert("messages", {
      channelId: args.channelId,
      authorId: args.authorId,
      content: args.content,
    });

    // Schedule AI response generation (transactional)
    await ctx.scheduler.runAfter(0, internal.functions.generateResponse, {
      channelId: args.channelId,
    });

    return null;
  },
});

export const updateUserStatus = mutation({
  args: {
    userId: v.id("users"),
    status: v.string(),
  },
  handler: async (ctx, args) => {
    // Patch updates an existing document with shallow merge
    await ctx.db.patch(args.userId, {
      status: args.status,
      lastUpdated: Date.now(),
    });
    return null;
  },
});
```

For more detailed information and additional patterns, refer to the complete reference documentation.
