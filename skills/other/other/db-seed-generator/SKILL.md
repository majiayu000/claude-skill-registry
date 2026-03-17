---
name: db-seed-generator
description: Generate realistic database seed data from a Prisma schema. Use when asked to generate seed data, create test data, populate the database, seed the DB, or create fixtures.
---

# DB Seed Generator

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Process

1. Read `schema.prisma` and extract all models, fields, types, constraints, relations, and enums.
2. Determine dependency order: models with no required relations first, then models that depend on them.
3. Generate a `prisma/seed.ts` file with realistic fake data that respects all constraints.
4. Output a ready-to-run seed file.

## Dependency Ordering

Build a directed graph of model dependencies from `@relation` fields. Topologically sort so parent records are created before children.

```
User (no deps)           → create first
Organization (no deps)   → create first
Post (depends on User)   → create second
Comment (depends on User, Post) → create third
```

If circular dependencies exist, use a two-pass approach: create records with required fields first, then update with optional relation fields.

## Data Generation Rules

### Field Name Conventions

Generate realistic values based on field names:

| Pattern | Generated value |
|---|---|
| `firstName` | `"Elena"`, `"Marcus"`, `"Priya"` |
| `lastName` | `"Rodriguez"`, `"Chen"`, `"Okafor"` |
| `name` (on User) | `"Elena Rodriguez"` |
| `email` | `"elena.rodriguez@example.com"` |
| `phone` | `"555-0101"`, `"555-0102"` |
| `avatarUrl`, `imageUrl` | `"https://example.com/avatars/1.jpg"` |
| `url`, `website` | `"https://example.com"` |
| `title` (on Post/Article) | Realistic short sentences |
| `content`, `body`, `description` | 1-3 realistic sentences |
| `slug` | Derived from title: `"realistic-short-sentence"` |
| `price`, `amount` | Realistic numbers like `29.99`, `149.00` |
| `quantity`, `count` | Small integers: `1`-`100` |
| `createdAt`, `updatedAt` | Dates spread over the last 90 days |
| `publishedAt` | Either `null` or a date after `createdAt` |
| `isActive`, `isPublished` | Mix of `true`/`false` |
| `role` (enum) | Distribute across valid enum values |
| `password` | Pre-hashed placeholder: `"$2b$10$..."` — never plaintext |

### Constraints

- **`@unique`**: Ensure every value is unique. Use index suffixes: `"user1@example.com"`, `"user2@example.com"`.
- **`@id @default(cuid())`**: Omit from create calls — let the database generate them.
- **`@default(now())`**: Omit or set explicit dates for predictable ordering.
- **`@default(value)`**: Omit to use the default, or set explicitly for variety.
- **Enums**: Only use values defined in the enum.
- **`Int`, `Float`**: Respect `@db.SmallInt`, `@db.Decimal(10,2)` etc.

### Relations

- **One-to-many**: Create the "one" side first, reference its ID on the "many" side.
- **Many-to-many** (implicit): Use `connect` syntax after both sides exist.
- **Self-referencing**: Create root records first (no parent), then children pointing to them.
- **Required relations**: Always satisfy — never leave a required FK null.
- **Optional relations**: Mix of connected and null.

## Output Template

```typescript
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  // Clear existing data (reverse dependency order)
  await prisma.comment.deleteMany();
  await prisma.post.deleteMany();
  await prisma.user.deleteMany();

  // Seed in dependency order
  const users = await Promise.all([
    prisma.user.upsert({
      where: { email: "elena.rodriguez@example.com" },
      update: {},
      create: {
        email: "elena.rodriguez@example.com",
        name: "Elena Rodriguez",
        // ... fields
      },
    }),
    // ... more users
  ]);

  // Use createMany for bulk inserts where relations allow
  await prisma.post.createMany({
    data: [
      { title: "...", authorId: users[0].id },
      // ...
    ],
  });

  console.log("Seeded: X users, Y posts, Z comments");
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
```

## Scale Parameter

When the user specifies a count (e.g., "seed 50 users"), generate that many records. Default to 5-10 records per model. Use `createMany` for bulk inserts where possible. Wrap large seeds in a `prisma.$transaction()`.

## Upsert Pattern

Use `upsert` on a unique field to make the seed idempotent — safe to run multiple times.

## Reference

See [references/seed-patterns.md](references/seed-patterns.md) for dependency ordering details, realistic data patterns, and performance tips.
