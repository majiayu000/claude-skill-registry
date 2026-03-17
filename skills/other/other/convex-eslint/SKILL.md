---
name: convex-eslint
description: Write Convex code that passes @convex-dev/eslint-plugin rules by default
version: 1.0.0
author: Convex
tags: [convex, eslint, linting, code-quality, validation]
---

# Convex ESLint Compliance

Write all Convex functions to pass @convex-dev/eslint-plugin. These rules prevent common bugs, security issues, and ensure code quality.

## Documentation Sources

- https://docs.convex.dev/eslint
- https://www.npmjs.com/package/@convex-dev/eslint-plugin

## Setup

Install the plugin:

```bash
npm i @convex-dev/eslint-plugin --save-dev
```

Configure `eslint.config.js`:

```javascript
import { defineConfig } from "eslint/config";
import convexPlugin from "@convex-dev/eslint-plugin";

export default defineConfig([...convexPlugin.configs.recommended]);
```

## Rules

### 1. no-old-registered-function-syntax

Always use object syntax with a `handler` property.

```typescript
// Correct
export const list = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("messages").collect();
  },
});

// Wrong - bare function syntax
export const list = query(async (ctx) => {
  return await ctx.db.query("messages").collect();
});
```

### 2. require-argument-validators

Always include `args` object, even when empty.

```typescript
// Correct - with arguments
export const get = query({
  args: { id: v.id("messages") },
  handler: async (ctx, { id }) => {
    return await ctx.db.get("messages", id);
  },
});

// Correct - no arguments
export const listAll = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("messages").collect();
  },
});

// Wrong - missing args
export const get = query({
  handler: async (ctx, { id }: { id: Id<"messages"> }) => {
    return await ctx.db.get("messages", id);
  },
});
```

### 3. explicit-table-ids

Use explicit table names in all database operations (Convex 1.31.0+).

```typescript
// Correct
const message = await ctx.db.get("messages", messageId);
await ctx.db.patch("messages", messageId, { text: "updated" });
await ctx.db.replace("messages", messageId, {
  text: "replaced",
  author: "Alice",
});
await ctx.db.delete("messages", messageId);

// Wrong - implicit table from ID type
const message = await ctx.db.get(messageId);
await ctx.db.patch(messageId, { text: "updated" });
await ctx.db.replace(messageId, { text: "replaced", author: "Alice" });
await ctx.db.delete(messageId);
```

Migration codemod available:

```bash
npx @convex-dev/codemod@latest explicit-ids
```

### 4. import-wrong-runtime

Never import Node.js runtime files into Convex runtime files.

```typescript
// convex/queries.ts (no "use node" directive)

// Correct - importing from Convex runtime file
import { helper } from "./utils"; // utils.ts has no "use node"

// Wrong - importing from Node runtime file
import { nodeHelper } from "./nodeUtils"; // nodeUtils.ts has "use node"
```

## Best Practices

1. Run ESLint before committing: `npx eslint convex/`
2. Use auto-fix for quick migrations: `npx eslint convex/ --fix`
3. Add to CI pipeline to catch violations early
4. Configure your editor for real-time feedback

## Quick Reference

| Rule                                | What it enforces                  |
| ----------------------------------- | --------------------------------- |
| `no-old-registered-function-syntax` | Object syntax with `handler`      |
| `require-argument-validators`       | `args: {}` on all functions       |
| `explicit-table-ids`                | Table name in db operations       |
| `import-wrong-runtime`              | No Node imports in Convex runtime |

## References

- [ESLint Plugin Docs](https://docs.convex.dev/eslint)
- [Explicit IDs Announcement](https://news.convex.dev/db-table-name/)
