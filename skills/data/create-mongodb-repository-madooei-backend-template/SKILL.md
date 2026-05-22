---
name: create-mongodb-repository
description: Create MongoDB repository implementation for production database. Use when implementing repository interface with MongoDB, setting up document mapping, creating indexes, or connecting to real database. Triggers on "mongodb repository", "mongo repository", "production repository", "database repository".
---

# Create MongoDB Repository

Creates a MongoDB repository implementation using the native MongoDB driver (not Mongoose). Includes document mapping, Zod validation, index creation, and proper ObjectId handling.

## Quick Reference

**Location**: `src/repositories/mongodb/{entity-name}.mongodb.repository.ts`
**Naming**: `{entity-name}.mongodb.repository.ts` (e.g., `note.mongodb.repository.ts`)

## Prerequisites

- MongoDB connection configured in `src/config/mongodb.setup.ts`
- Entity schema created in `src/schemas/{entity-name}.schema.ts`
- Repository interface created in `src/repositories/{entity-name}.repository.ts`

## Instructions

### Step 1: Create the Implementation File

Create `src/repositories/mongodb/{entity-name}.mongodb.repository.ts`

### Step 2: Import Dependencies

```typescript
import { Collection, Db, ObjectId } from "mongodb";
import type { WithId, Filter, Sort } from "mongodb";
import type {
  {Entity}Type,
  Create{Entity}Type,
  Update{Entity}Type,
  {Entity}QueryParamsType,
  {Entity}IdType,
} from "@/schemas/{entity-name}.schema";
import { {entity}Schema } from "@/schemas/{entity-name}.schema";
import {
  DEFAULT_LIMIT,
  DEFAULT_PAGE,
  type PaginatedResultType,
} from "@/schemas/shared.schema";
import type { I{Entity}Repository } from "@/repositories/{entity-name}.repository";
import type { UserIdType } from "@/schemas/user.schemas";
import { getDatabase } from "@/config/mongodb.setup";
```

### Step 3: Define MongoDB Document Interface

```typescript
// MongoDB document interface (internal to repository)
// Maps domain model to MongoDB structure
interface Mongo{Entity}Document
  extends Omit<{Entity}Type, "id" | "createdAt" | "updatedAt"> {
  _id?: ObjectId;
  createdAt: Date;
  updatedAt: Date;
}
```

### Step 4: Create the Repository Class

```typescript
export class MongoDb{Entity}Repository implements I{Entity}Repository {
  private collection: Collection<Mongo{Entity}Document> | null = null;

  // Lazy load collection on first use
  private async getCollection(): Promise<Collection<Mongo{Entity}Document>> {
    if (!this.collection) {
      const db: Db = await getDatabase();
      this.collection = db.collection<Mongo{Entity}Document>("{entities}");
      await this.createIndexes(this.collection);
      console.log("📚 {Entities} collection initialized");
    }
    return this.collection;
  }

  // Index creation (idempotent)
  private async createIndexes(
    collection: Collection<Mongo{Entity}Document>,
  ): Promise<void> {
    console.log("Creating indexes for {entities} collection...");

    await Promise.all([
      collection.createIndex({ createdBy: 1 }, { name: "{entities}_createdBy" }),
      collection.createIndex({ createdAt: -1 }, { name: "{entities}_createdAt_desc" }),
      // Add text index for searchable fields
      collection.createIndex({ {searchableField}: "text" }, { name: "{entities}_{searchableField}_text" }),
    ]);

    console.log("✅ {Entities} indexes created successfully");
  }

  // Map MongoDB document to domain entity with Zod validation
  private mapDocumentToEntity(doc: WithId<Mongo{Entity}Document>): {Entity}Type {
    const { _id, ...restOfDoc } = doc;
    return {entity}Schema.parse({
      ...restOfDoc,
      id: _id.toHexString(),
      createdAt: doc.createdAt,
      updatedAt: doc.updatedAt,
    });
  }

  // Map domain data to MongoDB document
  private mapEntityToDocument(
    data: Create{Entity}Type,
    createdByUserId: UserIdType,
  ): Omit<Mongo{Entity}Document, "_id"> {
    const now = new Date();
    return {
      // Map each field from Create{Entity}Type
      ...data,
      createdBy: createdByUserId,
      createdAt: now,
      updatedAt: now,
    };
  }

  // ... implement interface methods (see below)
}
```

### Step 5: Implement Interface Methods

#### findAll

```typescript
async findAll(
  params: {Entity}QueryParamsType,
): Promise<PaginatedResultType<{Entity}Type>> {
  const collection = await this.getCollection();

  // Build MongoDB query filter
  const filter: Filter<Mongo{Entity}Document> = {};

  if (params.createdBy) {
    filter.createdBy = params.createdBy;
  }

  if (params.search?.trim()) {
    filter.$text = { $search: params.search.trim() };
  }

  // Pagination
  const page = params.page ?? DEFAULT_PAGE;
  const limit = params.limit ?? DEFAULT_LIMIT;
  const skip = (page - 1) * limit;

  // Sort criteria
  const sortBy = params.sortBy ?? "createdAt";
  const sortOrder = params.sortOrder === "asc" ? 1 : -1;
  const sort: Sort = { [sortBy]: sortOrder };

  // Execute queries in parallel
  const [documents, total] = await Promise.all([
    collection.find(filter).sort(sort).skip(skip).limit(limit).toArray(),
    collection.countDocuments(filter),
  ]);

  // Map to domain entities
  const entities = documents.map((doc) => this.mapDocumentToEntity(doc));
  const totalPages = Math.ceil(total / limit);

  return {
    data: entities,
    total,
    page,
    limit,
    totalPages,
  };
}
```

#### findById

```typescript
async findById(id: {Entity}IdType): Promise<{Entity}Type | null> {
  // Validate ObjectId format
  if (!ObjectId.isValid(id)) {
    return null;
  }

  const collection = await this.getCollection();
  const document = await collection.findOne({ _id: new ObjectId(id) });

  if (!document) {
    return null;
  }

  return this.mapDocumentToEntity(document);
}
```

#### findAllByIds

```typescript
async findAllByIds(
  ids: {Entity}IdType[],
  params: {Entity}QueryParamsType,
): Promise<PaginatedResultType<{Entity}Type>> {
  const collection = await this.getCollection();

  // Convert to ObjectIds, filter invalid
  const objectIds = ids
    .filter((id) => ObjectId.isValid(id))
    .map((id) => new ObjectId(id));

  const filter: Filter<Mongo{Entity}Document> = { _id: { $in: objectIds } };

  if (params.createdBy) {
    filter.createdBy = params.createdBy;
  }

  if (params.search?.trim()) {
    filter.$text = { $search: params.search.trim() };
  }

  const page = params.page ?? DEFAULT_PAGE;
  const limit = params.limit ?? DEFAULT_LIMIT;
  const skip = (page - 1) * limit;

  const sortBy = params.sortBy === "id" ? "_id" : (params.sortBy ?? "createdAt");
  const sortOrder = params.sortOrder === "asc" ? 1 : -1;
  const sort: Sort = { [sortBy]: sortOrder };

  const [documents, total] = await Promise.all([
    collection.find(filter).sort(sort).skip(skip).limit(limit).toArray(),
    collection.countDocuments(filter),
  ]);

  const entities = documents.map((doc) => this.mapDocumentToEntity(doc));
  const totalPages = Math.ceil(total / limit);

  return {
    data: entities,
    total,
    page,
    limit,
    totalPages,
  };
}
```

#### create

```typescript
async create(
  data: Create{Entity}Type,
  createdByUserId: UserIdType,
): Promise<{Entity}Type> {
  const collection = await this.getCollection();
  const documentToInsert = this.mapEntityToDocument(data, createdByUserId);

  const result = await collection.insertOne(documentToInsert);

  if (!result.insertedId) {
    throw new Error("{Entity} creation failed, no ObjectId generated by database.");
  }

  return {entity}Schema.parse({
    ...documentToInsert,
    id: result.insertedId.toHexString(),
  });
}
```

#### update

```typescript
async update(id: {Entity}IdType, data: Update{Entity}Type): Promise<{Entity}Type | null> {
  if (!ObjectId.isValid(id)) {
    return null;
  }

  const collection = await this.getCollection();

  const updateDoc = {
    $set: {
      ...data,
      updatedAt: new Date(),
    },
  };

  const result = await collection.findOneAndUpdate(
    { _id: new ObjectId(id) },
    updateDoc,
    { returnDocument: "after" },
  );

  if (!result) {
    return null;
  }

  return this.mapDocumentToEntity(result);
}
```

#### remove

```typescript
async remove(id: {Entity}IdType): Promise<boolean> {
  if (!ObjectId.isValid(id)) {
    return false;
  }

  const collection = await this.getCollection();
  const result = await collection.deleteOne({ _id: new ObjectId(id) });
  return result.deletedCount > 0;
}
```

### Step 6: Add Testing Helpers

```typescript
// Helper method for testing: clear all documents
async clear(): Promise<void> {
  const collection = await this.getCollection();
  await collection.deleteMany({});
}

// Helper method for testing: get collection stats
async getStats(): Promise<{ count: number; indexes: string[] }> {
  const collection = await this.getCollection();
  const count = await collection.countDocuments();
  const indexes = await collection.listIndexes().toArray();
  return {
    count,
    indexes: indexes.map((idx) => idx.name),
  };
}
```

## Patterns & Rules

### Document Interface Pattern

Always create a MongoDB-specific document interface:

```typescript
interface Mongo{Entity}Document
  extends Omit<{Entity}Type, "id" | "createdAt" | "updatedAt"> {
  _id?: ObjectId;        // MongoDB's primary key
  createdAt: Date;       // Required in documents
  updatedAt: Date;       // Required in documents
}
```

### ObjectId Handling

- Always validate with `ObjectId.isValid(id)` before using
- Convert string to ObjectId: `new ObjectId(id)`
- Convert ObjectId to string: `_id.toHexString()`
- Return `null` for invalid ObjectIds (don't throw)

### Zod Validation on Read

Always validate documents from MongoDB using Zod:

```typescript
return {entity}Schema.parse({
  ...restOfDoc,
  id: _id.toHexString(),
});
```

### Lazy Collection Loading

Initialize collection on first use, not in constructor:

```typescript
private async getCollection(): Promise<Collection<...>> {
  if (!this.collection) {
    const db = await getDatabase();
    this.collection = db.collection("{entities}");
    await this.createIndexes(this.collection);
  }
  return this.collection;
}
```

### Index Creation

- Indexes are created when collection is first accessed
- `createIndex` is idempotent (safe to call multiple times)
- Always name your indexes: `{ name: "{entities}_fieldName" }`
- Use text indexes for searchable fields

### Parallel Query Execution

Use `Promise.all` for independent queries:

```typescript
const [documents, total] = await Promise.all([
  collection.find(filter).sort(sort).skip(skip).limit(limit).toArray(),
  collection.countDocuments(filter),
]);
```

## Complete Example

See [REFERENCE.md](REFERENCE.md) for a full implementation example including:

- Complete `MongoDbNoteRepository` class
- MongoDB connection setup (`mongodb.setup.ts`)
- Required environment variables

## What NOT to Do

- Do NOT use Mongoose - use native MongoDB driver
- Do NOT expose MongoDB types outside the repository
- Do NOT skip ObjectId validation
- Do NOT skip Zod validation when reading documents
- Do NOT throw errors for not-found cases - return null
- Do NOT forget to handle `sortBy: "id"` → `"_id"` conversion
- Do NOT create indexes in the constructor - use lazy loading
