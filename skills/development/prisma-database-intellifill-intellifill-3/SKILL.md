---
name: prisma-database
description: Prisma schema design and database operations for IntelliFill. Use when modifying database schema, writing queries, or managing migrations.
---

# Prisma Database Development Skill

This skill provides comprehensive guidance for working with Prisma ORM and PostgreSQL in IntelliFill.

## Table of Contents

1. [Schema Design](#schema-design)
2. [Naming Conventions](#naming-conventions)
3. [Relations](#relations)
4. [Migrations](#migrations)
5. [Query Patterns](#query-patterns)
6. [Advanced Features](#advanced-features)
7. [Performance Optimization](#performance-optimization)
8. [Testing with Prisma](#testing-with-prisma)

## Schema Design

IntelliFill uses PostgreSQL with Prisma ORM for type-safe database access.

### Schema Location

```
quikadmin/prisma/
├── schema.prisma           # Main schema definition
├── migrations/             # Migration history
│   └── YYYYMMDDHHMMSS_description/
│       └── migration.sql
└── seed.ts                 # Seed data script
```

### Base Schema Template

```prisma
// quikadmin/prisma/schema.prisma

generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["postgresqlExtensions"]
}

datasource db {
  provider   = "postgresql"
  url        = env("DATABASE_URL")
  directUrl  = env("DIRECT_URL")
  extensions = [pgvector(map: "vector")]
}

// Base model template with common fields
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?

  // Timestamps (always include)
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  // Soft delete support
  deletedAt DateTime? @map("deleted_at")

  // Relations
  documents Document[]

  @@map("users") // Plural table name
}

model Document {
  id          String   @id @default(uuid())
  name        String
  description String?

  // Foreign keys
  userId      String   @map("user_id")
  user        User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  // Metadata
  status      DocumentStatus @default(PENDING)

  // Timestamps
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")
  deletedAt   DateTime? @map("deleted_at")

  // Indexes
  @@index([userId])
  @@index([status])
  @@index([createdAt])
  @@map("documents")
}

enum DocumentStatus {
  PENDING
  PROCESSING
  COMPLETED
  FAILED
}
```

## Naming Conventions

IntelliFill follows strict naming conventions for consistency.

### Model Naming

```prisma
// Models: PascalCase, singular
model User { }
model Document { }
model TemplateMapping { }

// Table names: snake_case, plural (use @@map)
@@map("users")
@@map("documents")
@@map("template_mappings")
```

### Field Naming

```prisma
model Document {
  // Fields: camelCase in Prisma
  id String
  userId String
  createdAt DateTime

  // Column names: snake_case in database (use @map)
  userId String @map("user_id")
  createdAt DateTime @map("created_at")

  // Relations: camelCase, descriptive
  user User
  templateMappings TemplateMapping[]
}
```

### Enum Naming

```prisma
// Enums: PascalCase
enum DocumentStatus {
  PENDING      // Values: SCREAMING_SNAKE_CASE
  PROCESSING
  COMPLETED
  FAILED
}
```

## Relations

### One-to-Many Relationship

```prisma
// User has many Documents
model User {
  id        String   @id @default(uuid())
  documents Document[]

  @@map("users")
}

model Document {
  id     String @id @default(uuid())
  userId String @map("user_id")

  // Relation field
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)

  // Index on foreign key
  @@index([userId])
  @@map("documents")
}
```

### Many-to-Many Relationship

```prisma
// Explicit join table (recommended)
model Document {
  id   String @id @default(uuid())
  tags DocumentTag[]

  @@map("documents")
}

model Tag {
  id        String @id @default(uuid())
  name      String @unique
  documents DocumentTag[]

  @@map("tags")
}

// Join table with additional fields
model DocumentTag {
  documentId String   @map("document_id")
  tagId      String   @map("tag_id")
  addedAt    DateTime @default(now()) @map("added_at")

  document   Document @relation(fields: [documentId], references: [id], onDelete: Cascade)
  tag        Tag      @relation(fields: [tagId], references: [id], onDelete: Cascade)

  @@id([documentId, tagId])
  @@index([tagId])
  @@map("document_tags")
}
```

### Self-Referencing Relationship

```prisma
model Category {
  id       String     @id @default(uuid())
  name     String

  // Self-reference for hierarchy
  parentId String?    @map("parent_id")
  parent   Category?  @relation("CategoryHierarchy", fields: [parentId], references: [id])
  children Category[] @relation("CategoryHierarchy")

  @@index([parentId])
  @@map("categories")
}
```

### One-to-One Relationship

```prisma
model User {
  id      String   @id @default(uuid())
  profile Profile?

  @@map("users")
}

model Profile {
  id     String @id @default(uuid())
  bio    String?
  avatar String?

  userId String @unique @map("user_id")
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@map("profiles")
}
```

## Migrations

### Creating Migrations

```bash
# Create migration from schema changes
cd quikadmin
npx prisma migrate dev --name description_of_change

# Examples
npx prisma migrate dev --name add_document_status
npx prisma migrate dev --name add_user_profile
npx prisma migrate dev --name create_knowledge_base_tables
```

### Migration Best Practices

1. **Descriptive names** - Use clear, concise descriptions
2. **Small migrations** - One logical change per migration
3. **Review SQL** - Always check generated SQL before applying
4. **Backup data** - Backup production data before migrations
5. **Test rollback** - Ensure migrations can be rolled back

### Manual Migration Editing

```sql
-- quikadmin/prisma/migrations/20240101000000_add_indexes/migration.sql

-- Add indexes for query performance
CREATE INDEX CONCURRENTLY IF NOT EXISTS "documents_user_id_status_idx"
  ON "documents" ("user_id", "status");

-- Add full-text search index
CREATE INDEX IF NOT EXISTS "documents_name_search_idx"
  ON "documents" USING gin(to_tsvector('english', name));

-- Add check constraint
ALTER TABLE "documents"
  ADD CONSTRAINT "documents_name_length_check"
  CHECK (length(name) >= 1 AND length(name) <= 255);
```

### Migration Workflow

```bash
# 1. Modify schema.prisma
# 2. Create migration
npx prisma migrate dev --name my_change

# 3. Review generated SQL in migrations/*/migration.sql
# 4. Edit migration SQL if needed
# 5. Apply migration
npx prisma migrate deploy

# 6. Regenerate Prisma Client
npx prisma generate
```

## Query Patterns

### Basic CRUD Operations

```typescript
import prisma from '@/utils/prisma';

// CREATE
const document = await prisma.document.create({
  data: {
    name: 'My Document',
    userId: 'user-123',
    status: 'PENDING',
  },
});

// READ - Single
const document = await prisma.document.findUnique({
  where: { id: 'doc-123' },
  include: { user: true }, // Include relations
});

// READ - Multiple
const documents = await prisma.document.findMany({
  where: {
    userId: 'user-123',
    status: 'COMPLETED',
  },
  orderBy: { createdAt: 'desc' },
  take: 20,
  skip: 0,
});

// UPDATE
const updated = await prisma.document.update({
  where: { id: 'doc-123' },
  data: { name: 'New Name' },
});

// DELETE
await prisma.document.delete({
  where: { id: 'doc-123' },
});
```

### Filtering and Search

```typescript
// Multiple conditions (AND)
const documents = await prisma.document.findMany({
  where: {
    userId: 'user-123',
    status: 'COMPLETED',
    deletedAt: null,
  },
});

// OR conditions
const documents = await prisma.document.findMany({
  where: {
    OR: [
      { status: 'COMPLETED' },
      { status: 'PROCESSING' },
    ],
  },
});

// Complex nested conditions
const documents = await prisma.document.findMany({
  where: {
    AND: [
      { userId: 'user-123' },
      {
        OR: [
          { name: { contains: 'invoice', mode: 'insensitive' } },
          { description: { contains: 'invoice', mode: 'insensitive' } },
        ],
      },
    ],
  },
});

// String filters
const documents = await prisma.document.findMany({
  where: {
    name: {
      contains: 'search',      // LIKE '%search%'
      startsWith: 'prefix',    // LIKE 'prefix%'
      endsWith: 'suffix',      // LIKE '%suffix'
      mode: 'insensitive',     // Case-insensitive
    },
  },
});

// Date filters
const documents = await prisma.document.findMany({
  where: {
    createdAt: {
      gte: new Date('2024-01-01'), // Greater than or equal
      lte: new Date('2024-12-31'), // Less than or equal
    },
  },
});

// Array filters
const documents = await prisma.document.findMany({
  where: {
    tags: {
      hasSome: ['urgent', 'important'],  // Has any of these tags
      hasEvery: ['approved', 'final'],   // Has all of these tags
    },
  },
});
```

### Pagination

```typescript
// Offset-based pagination
async function getDocuments(page: number, limit: number) {
  const skip = (page - 1) * limit;

  const [documents, total] = await Promise.all([
    prisma.document.findMany({
      where: { userId: 'user-123' },
      skip,
      take: limit,
      orderBy: { createdAt: 'desc' },
    }),
    prisma.document.count({
      where: { userId: 'user-123' },
    }),
  ]);

  return {
    documents,
    total,
    page,
    totalPages: Math.ceil(total / limit),
  };
}

// Cursor-based pagination (better for large datasets)
async function getDocumentsCursor(cursor?: string, limit: number = 20) {
  const documents = await prisma.document.findMany({
    take: limit,
    ...(cursor && {
      skip: 1, // Skip the cursor
      cursor: { id: cursor },
    }),
    orderBy: { createdAt: 'desc' },
  });

  return {
    documents,
    nextCursor: documents[documents.length - 1]?.id,
  };
}
```

### Aggregations

```typescript
// Count
const count = await prisma.document.count({
  where: { status: 'COMPLETED' },
});

// Aggregate functions
const stats = await prisma.document.aggregate({
  where: { userId: 'user-123' },
  _count: { id: true },
  _avg: { processingTime: true },
  _sum: { pageCount: true },
  _min: { createdAt: true },
  _max: { createdAt: true },
});

// Group by
const statusCounts = await prisma.document.groupBy({
  by: ['status'],
  _count: { id: true },
  where: { userId: 'user-123' },
});
```

### Transactions

```typescript
// Sequential operations in transaction
const result = await prisma.$transaction(async (tx) => {
  // Create document
  const document = await tx.document.create({
    data: { name: 'New Doc', userId: 'user-123' },
  });

  // Create mapping
  const mapping = await tx.templateMapping.create({
    data: {
      documentId: document.id,
      templateId: 'template-123',
    },
  });

  // Update user stats
  await tx.user.update({
    where: { id: 'user-123' },
    data: { documentCount: { increment: 1 } },
  });

  return { document, mapping };
});

// Batch operations
await prisma.$transaction([
  prisma.document.create({ data: {...} }),
  prisma.document.update({ where: {...}, data: {...} }),
  prisma.document.delete({ where: {...} }),
]);
```

### Soft Delete Pattern

```typescript
// Add deletedAt field to models
model Document {
  deletedAt DateTime? @map("deleted_at")
}

// Soft delete
async function softDelete(id: string) {
  return prisma.document.update({
    where: { id },
    data: { deletedAt: new Date() },
  });
}

// Exclude soft-deleted in queries
const documents = await prisma.document.findMany({
  where: {
    userId: 'user-123',
    deletedAt: null, // Only non-deleted
  },
});

// Include soft-deleted
const allDocuments = await prisma.document.findMany({
  where: { userId: 'user-123' },
  // No deletedAt filter
});

// Restore soft-deleted
async function restore(id: string) {
  return prisma.document.update({
    where: { id },
    data: { deletedAt: null },
  });
}
```

## Advanced Features

### JSON Fields

```prisma
model Document {
  id       String @id @default(uuid())
  metadata Json?  // JSON field

  @@map("documents")
}
```

```typescript
// Create with JSON
await prisma.document.create({
  data: {
    name: 'Doc',
    metadata: {
      category: 'invoice',
      tags: ['urgent'],
      customFields: { field1: 'value1' },
    },
  },
});

// Query JSON fields (PostgreSQL-specific)
const documents = await prisma.document.findMany({
  where: {
    metadata: {
      path: ['category'],
      equals: 'invoice',
    },
  },
});
```

### Full-Text Search

```prisma
model Document {
  id          String @id @default(uuid())
  name        String
  description String?

  // Add GIN index for full-text search in migration
  @@map("documents")
}
```

```sql
-- In migration SQL
CREATE INDEX "documents_search_idx"
  ON "documents"
  USING gin(to_tsvector('english', name || ' ' || COALESCE(description, '')));
```

```typescript
// Use raw SQL for full-text search
const documents = await prisma.$queryRaw`
  SELECT * FROM documents
  WHERE to_tsvector('english', name || ' ' || COALESCE(description, ''))
    @@ plainto_tsquery('english', ${searchQuery})
  ORDER BY ts_rank(
    to_tsvector('english', name || ' ' || COALESCE(description, '')),
    plainto_tsquery('english', ${searchQuery})
  ) DESC
  LIMIT 20;
`;
```

### pgvector for Embeddings

```prisma
// Enable pgvector extension
datasource db {
  provider   = "postgresql"
  url        = env("DATABASE_URL")
  extensions = [pgvector(map: "vector")]
}

model KnowledgeChunk {
  id        String                 @id @default(uuid())
  content   String
  embedding Unsupported("vector(1536)")? // OpenAI embedding dimension

  @@map("knowledge_chunks")
}
```

```typescript
// Store embedding
await prisma.$executeRaw`
  INSERT INTO knowledge_chunks (id, content, embedding)
  VALUES (${id}, ${content}, ${embedding}::vector)
`;

// Similarity search
const results = await prisma.$queryRaw`
  SELECT id, content, embedding <=> ${queryEmbedding}::vector AS distance
  FROM knowledge_chunks
  ORDER BY distance
  LIMIT 10;
`;
```

## Performance Optimization

### Indexes

```prisma
model Document {
  id     String @id @default(uuid())
  userId String @map("user_id")
  status DocumentStatus
  name   String

  // Single-column indexes
  @@index([userId])
  @@index([status])
  @@index([createdAt])

  // Composite indexes
  @@index([userId, status])
  @@index([userId, createdAt])

  // Unique constraint
  @@unique([userId, name])

  @@map("documents")
}
```

### Select Specific Fields

```typescript
// BAD: Fetches all fields
const documents = await prisma.document.findMany();

// GOOD: Select only needed fields
const documents = await prisma.document.findMany({
  select: {
    id: true,
    name: true,
    status: true,
  },
});
```

### Batch Operations

```typescript
// BAD: N+1 queries
for (const id of documentIds) {
  await prisma.document.update({
    where: { id },
    data: { status: 'COMPLETED' },
  });
}

// GOOD: Single batch update
await prisma.document.updateMany({
  where: { id: { in: documentIds } },
  data: { status: 'COMPLETED' },
});
```

### Connection Pooling

```typescript
// quikadmin/src/utils/prisma.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
  // Connection pool settings
  log: process.env.NODE_ENV === 'development' ? ['query', 'error'] : ['error'],
});

// Graceful shutdown
async function shutdown() {
  await prisma.$disconnect();
  process.exit(0);
}

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);

export default prisma;
```

## Testing with Prisma

### Mock Prisma Client

```typescript
import { PrismaClient } from '@prisma/client';
import { mockDeep, mockReset, DeepMockProxy } from 'jest-mock-extended';

export const prismaMock = mockDeep<PrismaClient>() as unknown as DeepMockProxy<PrismaClient>;

beforeEach(() => {
  mockReset(prismaMock);
});

// In tests
prismaMock.document.findUnique.mockResolvedValue({
  id: 'doc-1',
  name: 'Test Doc',
});
```

### Test Database Setup

```typescript
// quikadmin/src/test/setup.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.TEST_DATABASE_URL,
    },
  },
});

beforeAll(async () => {
  // Run migrations
  await prisma.$executeRaw`
    CREATE SCHEMA IF NOT EXISTS test;
  `;
});

afterAll(async () => {
  await prisma.$disconnect();
});

export default prisma;
```

## Best Practices

1. **Use transactions** - For multi-step operations
2. **Index foreign keys** - Always add @@index on foreign keys
3. **Soft delete** - Add deletedAt for audit trails
4. **Timestamps** - Always include createdAt and updatedAt
5. **Cascade deletes** - Use onDelete: Cascade for dependent data
6. **Select specific fields** - Avoid fetching unnecessary data
7. **Batch operations** - Use updateMany/createMany when possible
8. **Connection pooling** - Configure appropriate pool size
9. **Migration naming** - Use descriptive migration names
10. **Review generated SQL** - Always check migration SQL

## References

- [Prisma Documentation](https://www.prisma.io/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgvector Extension](https://github.com/pgvector/pgvector)
- [Prisma Best Practices](https://www.prisma.io/docs/guides/performance-and-optimization)
