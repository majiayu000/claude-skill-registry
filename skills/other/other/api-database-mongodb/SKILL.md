---
name: api-database-mongodb
description: MongoDB with Mongoose ODM - schemas, models, queries, aggregation, indexes, TypeScript typing, connection management
---

# MongoDB / Mongoose Patterns

> **Quick Guide:** Use Mongoose as the ODM for MongoDB. Define schemas with automatic TypeScript inference, use `lean()` for read-only queries, prefer embedding over referencing for co-accessed data, place `$match` early in aggregation pipelines, and always define indexes to match your query patterns.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define Mongoose middleware (pre/post hooks) BEFORE calling `model()` -- hooks registered after model compilation are silently ignored)**

**(You MUST pass `{ session }` to EVERY operation inside a transaction -- missing session causes operations to run outside the transaction)**

**(You MUST use `.lean()` for read-only queries that send results directly to API responses -- skipping lean wastes 3x memory on hydration overhead)**

**(You MUST use `127.0.0.1` instead of `localhost` in connection strings -- Node.js 18+ prefers IPv6 and `localhost` can cause connection timeouts)**

**(You MUST NOT use `findOneAndUpdate` / `updateOne` and expect `save` middleware to fire -- only `save()` and `create()` trigger document middleware)**

</critical_requirements>

---

**Auto-detection:** MongoDB, Mongoose, mongoose.connect, Schema, model, ObjectId, populate, aggregate, $match, $group, $lookup, lean, HydratedDocument, InferSchemaType, MongoClient, Atlas

**When to use:**

- Defining MongoDB schemas and models with Mongoose
- Building CRUD operations and complex queries
- Designing aggregation pipelines for analytics and reporting
- Managing indexes for query performance
- Connecting to MongoDB Atlas or local instances
- Modeling document relationships (embedding vs referencing)

**Key patterns covered:**

- Connection setup (Atlas URI, pooling, error handling)
- Schema definition (types, validation, defaults, enums)
- Models with TypeScript (automatic inference, methods, statics, virtuals)
- CRUD operations (create, find, update, delete, lean)
- Query building (filters, projection, sort, limit, populate)

**When NOT to use:**

- Relational data with complex joins and foreign key constraints (use a relational database)
- ACID transactions across many collections as a core pattern (use a relational database)
- Simple key-value storage (use a dedicated key-value store)

**Detailed Resources:**

- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Core Patterns:**

- [examples/core.md](examples/core.md) - Connection, schema definition, model creation, TypeScript typing

**Query Patterns:**

- [examples/queries.md](examples/queries.md) - Complex queries, populate, lean, cursor, pagination

**Aggregation:**

- [examples/aggregation.md](examples/aggregation.md) - Aggregation pipeline, $match, $group, $lookup, $project

**Advanced Patterns:**

- [examples/patterns.md](examples/patterns.md) - Schema design (embedding vs referencing), transactions, middleware hooks, virtuals

**Indexing:**

- [examples/indexes.md](examples/indexes.md) - Index types, compound indexes, text search, geospatial, TTL, performance

---

<philosophy>

## Philosophy

MongoDB is a document database. Mongoose provides schema-based modeling on top of it. The core principle: **data that is accessed together should be stored together.**

**Core principles:**

1. **Schema-first design** -- Define schemas before models. Schemas enforce structure, validation, and defaults at the application layer.
2. **Embed by default** -- Co-accessed data belongs in the same document. Only reference when data is shared across many documents, grows unbounded, or is frequently updated independently.
3. **Lean for reads** -- Use `.lean()` for read-only queries. It returns plain objects (3x less memory) instead of full Mongoose documents.
4. **Index your queries** -- Every query pattern needs a supporting index. Compound indexes follow the Equality-Sort-Range (ESR) rule.
5. **Aggregation over application logic** -- Push data transformation to the database with aggregation pipelines instead of processing in application code.
6. **TypeScript inference** -- Let Mongoose infer types from schema definitions. Avoid manually duplicating interfaces unless you need methods/statics/virtuals.

**When to use MongoDB / Mongoose:**

- Document-oriented data (user profiles, product catalogs, content)
- Flexible schemas that evolve over time
- Hierarchical or nested data structures
- High read throughput with embedding
- Geospatial queries and full-text search

**When NOT to use:**

- Highly relational data with complex joins (use a relational database)
- Strong ACID guarantees across many collections as a primary pattern
- Fixed schemas where relational constraints are critical
- Time-series data at scale (use a dedicated time-series database)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Connection Setup

Establish a single connection at application startup. Use environment variables for credentials.

```typescript
import mongoose from "mongoose";

const POOL_SIZE_MAX = 10;
const POOL_SIZE_MIN = 2;
const SERVER_SELECTION_TIMEOUT_MS = 5000;
const SOCKET_TIMEOUT_MS = 45000;

async function connectDatabase(): Promise<typeof mongoose> {
  const uri = process.env.MONGODB_URI;
  if (!uri) {
    throw new Error("MONGODB_URI environment variable is required");
  }

  const connection = await mongoose.connect(uri, {
    maxPoolSize: POOL_SIZE_MAX,
    minPoolSize: POOL_SIZE_MIN,
    serverSelectionTimeoutMS: SERVER_SELECTION_TIMEOUT_MS,
    socketTimeoutMS: SOCKET_TIMEOUT_MS,
    retryWrites: true,
    retryReads: true,
  });

  return connection;
}

export { connectDatabase };
```

**Why good:** Named constants for all numeric values, environment variable for URI, typed return, error on missing URI

```typescript
// BAD: Hardcoded URI, no options, no error handling
mongoose.connect("mongodb://localhost:27017/mydb");
```

**Why bad:** Hardcoded connection string leaks credentials, `localhost` fails on Node.js 18+ (IPv6), no pool or timeout configuration, no error handling

#### Connection Events

```typescript
mongoose.connection.on("connected", () => {
  console.log("MongoDB connected");
});

mongoose.connection.on("error", (err) => {
  console.error("MongoDB connection error:", err);
});

mongoose.connection.on("disconnected", () => {
  console.log("MongoDB disconnected");
});
```

---

### Pattern 2: Schema Definition with TypeScript

Let Mongoose infer types from the schema definition. Use explicit interfaces only when adding methods, statics, or virtuals.

#### Automatic Type Inference (Preferred)

```typescript
import { Schema, model } from "mongoose";

const userSchema = new Schema(
  {
    name: { type: String, required: true, trim: true },
    email: { type: String, required: true, unique: true, lowercase: true },
    role: {
      type: String,
      enum: ["admin", "user", "moderator"] as const,
      default: "user",
    },
    age: { type: Number, min: 0, max: 150 },
    isActive: { type: Boolean, default: true },
    tags: [{ type: String }],
    metadata: { type: Schema.Types.Mixed },
  },
  { timestamps: true },
);

const User = model("User", userSchema);
export { User, userSchema };
```

**Why good:** TypeScript infers document types from schema, `as const` preserves enum literal types, timestamps added via schema option, named exports

#### Explicit Interface (For Methods/Statics/Virtuals)

```typescript
import {
  Schema,
  model,
  type HydratedDocument,
  type Model,
  type Types,
} from "mongoose";

interface IUser {
  name: string;
  email: string;
  role: "admin" | "user" | "moderator";
  organizationId: Types.ObjectId;
}

interface IUserMethods {
  isAdmin(): boolean;
}

interface IUserVirtuals {
  displayName: string;
}

type UserModel = Model<IUser, {}, IUserMethods, IUserVirtuals>;

const userSchema = new Schema<
  IUser,
  UserModel,
  IUserMethods,
  {},
  IUserVirtuals
>({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  role: { type: String, enum: ["admin", "user", "moderator"], default: "user" },
  organizationId: {
    type: Schema.Types.ObjectId,
    ref: "Organization",
    required: true,
  },
});

userSchema.methods.isAdmin = function () {
  return this.role === "admin";
};

userSchema.virtual("displayName").get(function () {
  return `${this.name} (${this.role})`;
});

const User = model<IUser, UserModel>("User", userSchema);
export { User, userSchema };
export type { IUser, IUserMethods };
export type UserDocument = HydratedDocument<
  IUser,
  IUserMethods & IUserVirtuals
>;
```

**Why good:** Separate interfaces for document shape, methods, and virtuals; generic parameters correctly ordered; `HydratedDocument` type exported for consumers

```typescript
// BAD: Duplicate interface and schema definition without inference
interface IUser {
  name: string;
  email: string;
}
const userSchema = new Schema({ name: String, email: String });
// Types are disconnected -- schema changes don't update the interface
```

**Why bad:** Manual interface duplicates schema definition, interface and schema can drift out of sync, no validation constraints in schema

---

### Pattern 3: CRUD Operations

#### Create

```typescript
// Single document
const user = await User.create({
  name: "Alice",
  email: "alice@example.com",
  role: "admin",
});

// Bulk insert
const BATCH_SIZE = 1000;
const users = generateUsers(BATCH_SIZE);
await User.insertMany(users, { ordered: false });
```

#### Read with Lean

```typescript
// Single document (read-only response)
const user = await User.findById(id).lean();

// Multiple with filters
const PAGE_SIZE = 20;
const activeAdmins = await User.find({ role: "admin", isActive: true })
  .select("name email role")
  .sort({ name: 1 })
  .limit(PAGE_SIZE)
  .lean();
```

**Why good:** `.lean()` for read-only responses, `.select()` for projection, named constant for page size

#### Update

```typescript
// Update with save() -- triggers middleware
const user = await User.findById(id);
if (!user) {
  throw new Error(`User not found: ${id}`);
}
user.name = "Updated Name";
await user.save();

// Direct update -- does NOT trigger save middleware
await User.findByIdAndUpdate(
  id,
  { $set: { name: "Updated" } },
  { new: true, runValidators: true },
);

// Bulk update
await User.updateMany(
  { isActive: false },
  { $set: { archivedAt: new Date() } },
);
```

**Why good:** `save()` triggers middleware, `findByIdAndUpdate` with `runValidators: true` enforces schema validation, `{ new: true }` returns updated document

#### Delete

```typescript
await User.findByIdAndDelete(id);
await User.deleteMany({ isActive: false, archivedAt: { $lt: cutoffDate } });
```

```typescript
// BAD: No null check before calling method on potentially null result
const user = await User.findById(id);
user.deleteOne(); // TypeError if user is null
```

**Why bad:** No null check before calling method on potentially null result, crashes at runtime if document not found

---

### Pattern 4: Query Building

#### Filters and Operators

```typescript
const MIN_AGE = 18;
const MAX_AGE = 65;

// Comparison operators
const users = await User.find({
  age: { $gte: MIN_AGE, $lte: MAX_AGE },
  role: { $in: ["admin", "moderator"] },
  email: { $regex: /@company\.com$/i },
}).lean();

// Logical operators
const results = await User.find({
  $or: [{ role: "admin" }, { isActive: true, age: { $gte: MIN_AGE } }],
}).lean();
```

#### Populate (Reference Resolution)

```typescript
const post = await Post.findById(id)
  .populate("author", "name email") // select specific fields
  .populate({
    path: "comments",
    populate: { path: "author", select: "name" }, // nested populate
    options: { sort: { createdAt: -1 }, limit: 10 },
  })
  .lean();
```

**Why good:** Field selection on populate reduces data transfer, nested populate for deep references, sort and limit on populated array

```typescript
// BAD: Populating everything without field selection
const post = await Post.findById(id)
  .populate("author") // returns ALL author fields
  .populate("comments"); // returns ALL comments, unbounded
```

**Why bad:** No field selection wastes bandwidth and memory, unbounded populate can return thousands of documents, each populate is a separate database query

---

### Pattern 5: Schema Validation

```typescript
const productSchema = new Schema({
  name: {
    type: String,
    required: [true, "Product name is required"],
    minlength: [2, "Name must be at least 2 characters"],
    maxlength: [100, "Name must be at most 100 characters"],
  },
  price: {
    type: Number,
    required: true,
    min: [0, "Price cannot be negative"],
    validate: {
      validator: (v: number) => Number.isFinite(v),
      message: "Price must be a finite number",
    },
  },
  sku: {
    type: String,
    required: true,
    unique: true,
    match: [/^[A-Z]{2}-\d{6}$/, "SKU must match format XX-000000"],
  },
  status: {
    type: String,
    enum: {
      values: ["draft", "active", "archived"] as const,
      message: "{VALUE} is not a valid status",
    },
    default: "draft",
  },
  variants: {
    type: [
      {
        size: { type: String, required: true },
        color: { type: String, required: true },
        stock: { type: Number, min: 0, default: 0 },
      },
    ],
    validate: {
      validator: (v: unknown[]) => v.length > 0,
      message: "At least one variant is required",
    },
  },
});

export { productSchema };
```

**Why good:** Custom error messages for every validator, regex validation with descriptive message, array-level validation, enum with `as const` for TypeScript inference, subdocument schema inline

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Mutating a document fetched with `.lean()` and expecting `.save()` to work -- lean returns plain objects without Mongoose methods
- Registering middleware after `model()` call -- hooks are silently ignored
- Running operations in parallel inside a transaction (`Promise.all()`) -- MongoDB does not support parallel operations within a single transaction
- Using `localhost` in connection strings on Node.js 18+ -- IPv6 preference causes connection timeouts, use `127.0.0.1`
- Missing `{ session }` on any operation inside a transaction -- that operation runs outside the transaction

**Medium Priority Issues:**

- Using `findOneAndUpdate` / `updateOne` and expecting `pre('save')` hooks to fire -- only `save()` and `create()` trigger document middleware
- Unbounded `.populate()` without `limit` or field selection -- can return thousands of documents per query
- Not calling `runValidators: true` on `findOneAndUpdate` -- schema validation is skipped by default on updates
- Creating indexes in production code instead of migration scripts -- index builds lock the collection
- Using `$where` or JavaScript expressions in queries -- disables indexes and enables injection

**Common Mistakes:**

- Forgetting `{ new: true }` on `findOneAndUpdate` -- returns the old document by default
- Using `Schema.Types.ObjectId` in TypeScript interfaces instead of `Types.ObjectId` -- `Schema.Types.ObjectId` is for schema definitions, `Types.ObjectId` is for interfaces
- Not handling duplicate key errors (code 11000) from unique indexes
- Calling `.lean()` on write operations -- lean is for reads only
- Checking `doc.isNew` in `post('save')` hooks -- always `false` after save, use `this.$locals.wasNew` set in a `pre('save')` hook

**Gotchas & Edge Cases:**

- MongoDB has a 16 MB document size limit -- deeply embedded arrays can hit this
- Mongoose buffers operations before connection is established -- queries queue silently if connection fails
- `deleteOne` / `deleteMany` do not trigger `pre('remove')` middleware -- use `findOneAndDelete` or document `.deleteOne()` if you need middleware
- Virtual properties are excluded from `toJSON()` / `toObject()` by default -- set `{ toJSON: { virtuals: true } }` in schema options
- `remove()` was completely removed in Mongoose 7+ -- use `deleteOne()` or `deleteMany()` instead
- Mongoose 9 dropped callback-based `next()` in pre hooks -- use async/await instead
- Mongoose 9 renamed `FilterQuery` to `QueryFilter` -- update TypeScript imports if upgrading
- Mongoose 9 requires `updatePipeline: true` for pipeline-style updates -- they throw by default
- Mongoose 9 removed the `background` index option -- MongoDB 4.2+ builds all indexes in the background by default

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define Mongoose middleware (pre/post hooks) BEFORE calling `model()` -- hooks registered after model compilation are silently ignored)**

**(You MUST pass `{ session }` to EVERY operation inside a transaction -- missing session causes operations to run outside the transaction)**

**(You MUST use `.lean()` for read-only queries that send results directly to API responses -- skipping lean wastes 3x memory on hydration overhead)**

**(You MUST use `127.0.0.1` instead of `localhost` in connection strings -- Node.js 18+ prefers IPv6 and `localhost` can cause connection timeouts)**

**(You MUST NOT use `findOneAndUpdate` / `updateOne` and expect `save` middleware to fire -- only `save()` and `create()` trigger document middleware)**

**Failure to follow these rules will cause silent data corruption, middleware bypass, or transaction isolation failures.**

</critical_reminders>
