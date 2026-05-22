---
name: mymind-coding-patterns
description: Coding conventions and patterns for the mymind codebase. Use this skill when writing or modifying any code in this project to ensure consistency with established patterns.
---

# MyMind Coding Patterns

## Stack

- **Runtime**: Bun
- **Framework**: Next.js 15 (App Router)
- **Database**: PGlite (PostgreSQL) with pgvector for embeddings
- **ORM**: Drizzle
- **Validation**: Zod (preferred over type casting)
- **Formatting**: Biome (2 spaces, organize imports)

## Skills (Tools)

Skills are executable tools that Claude can call. They live in `src/skills/`.

### Defining a Skill

```typescript
import { z } from "zod";
import { defineSkill, type SkillResult } from "./types";

const MyParamsSchema = z.object({
  input: z.string().describe("Description for Claude"),
  optional: z.number().optional(),
});

type MyParams = z.infer<typeof MyParamsSchema>;

interface MyResult {
  // typed result
}

export const mySkill = defineSkill({
  name: "my_skill", // snake_case
  description: "What this skill does and when to use it",
  parameters: MyParamsSchema,

  async execute(params: MyParams): Promise<SkillResult<MyResult>> {
    try {
      // do the thing
      return {
        success: true,
        data: { /* result */ },
        message: "Human-readable success message",
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        success: false,
        error: `Failed to do thing: ${message}`,
      };
    }
  },
});

export default mySkill;
```

### Registering Skills

Add new skills to `src/skills/index.ts`:

```typescript
import { mySkill } from "./my-skill";

const skills: Skill[] = [
  // ... existing
  mySkill,
];

export { mySkill } from "./my-skill";
```

## Database Access

Always use `withDb()` wrapper - it handles connection lifecycle:

```typescript
import { withDb } from "@/db/client";
import { items, tags } from "@/db/schema";
import { eq } from "drizzle-orm";

const result = await withDb(async ({ db }) => {
  const rows = await db
    .select()
    .from(items)
    .where(eq(items.type, "bookmark"))
    .limit(10);
  return rows;
});
```

### Schema Types

Use Drizzle's inferred types:

```typescript
import { type Item, type NewItem } from "@/db/schema";

// Item = select type (has id, createdAt, etc.)
// NewItem = insert type (id optional, etc.)
```

## API Routes

### Request Validation

Always use Zod `.parse()` - never type cast:

```typescript
// ✅ Good
const params = MySchema.parse(await request.json());

// ❌ Bad - no runtime validation
const params = (await request.json()) as MyParams;
```

### Response Shape

```typescript
// Success
return NextResponse.json({
  success: true,
  items: result.data,
  total: result.total,
});

// Error
return NextResponse.json(
  { success: false, error: "What went wrong" },
  { status: 400 }
);
```

### Zod Error Handling

```typescript
try {
  const params = Schema.parse(body);
  // ...
} catch (error) {
  if (error instanceof z.ZodError) {
    return NextResponse.json(
      { success: false, error: error.issues },
      { status: 400 }
    );
  }
  throw error;
}
```

## Imports

Use path alias for src:

```typescript
// ✅ Good
import { withDb } from "@/db/client";
import { saveBookmark } from "@/skills";

// ❌ Avoid relative paths across directories
import { withDb } from "../../../db/client";
```

## Naming Conventions

| Thing | Convention | Example |
|-------|-----------|---------|
| Skill names | snake_case | `save_bookmark`, `list_items` |
| Functions | camelCase | `scrapeUrl`, `extractText` |
| Types/Interfaces | PascalCase | `SkillResult`, `ItemMetadata` |
| Files | kebab-case | `save-bookmark.ts`, `list-items.ts` |
| Zod schemas | PascalCase + Schema | `SaveBookmarkSchema` |

## Don't

- Don't use type casting (`as`) for external data - validate with Zod
- Don't create DB connections manually - use `withDb()`
- Don't use `any` - prefer `unknown` with narrowing
- Don't forget to add `.describe()` on Zod fields for tool schemas

