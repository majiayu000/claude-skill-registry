---
name: api-database-mongoose
description: MongoDB ODM with schemas, validation, middleware, and TypeScript support
---

# Mongoose ODM Patterns

> **Quick Guide:** Use Mongoose as the ODM layer for MongoDB. Let TypeScript infer types from schema definitions instead of duplicating interfaces. Register all middleware before calling `model()` -- hooks added after compilation are silently ignored. Use `.lean()` for any read-only query. Pass `{ session }` to every operation inside a transaction or enable `transactionAsyncLocalStorage`. Prefer `session.withTransaction()` over manual commit/abort. Use `127.0.0.1` instead of `localhost` in connection strings (Node.js 18+ IPv6 preference causes timeouts).

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define all middleware (pre/post hooks) BEFORE calling `model()` -- hooks registered after model compilation are silently ignored with no error)**

**(You MUST pass `{ session }` to EVERY operation inside a transaction -- missing session causes that operation to run outside the transaction silently)**

**(You MUST use `.lean()` for read-only queries returning API responses -- skipping lean wastes 3x memory on hydration overhead)**

**(You MUST use `127.0.0.1` instead of `localhost` in connection strings -- Node.js 18+ prefers IPv6 and `localhost` causes connection timeouts)**

**(You MUST NOT use `findOneAndUpdate`/`updateOne` and expect `pre('save')` to fire -- only `save()` and `create()` trigger document middleware)**

**(You MUST NOT use `next()` callbacks in pre hooks on Mongoose 9 -- use async/await instead; `next()` was removed in v9)**

</critical_requirements>

---

**Auto-detection:** Mongoose, mongoose, mongoose.connect, Schema, model, ObjectId, populate, HydratedDocument, InferSchemaType, InferRawDocType, pre('save'), post('save'), lean, mongoose.startSession, withTransaction, discriminator, virtual, Schema.Types.ObjectId, Types.ObjectId

**When to use:**

- Defining MongoDB schemas and models with Mongoose
- TypeScript integration with schema type inference
- Middleware hooks (pre/post save, validate, find, delete)
- Population (resolving references between collections)
- Transactions with session management
- Virtuals and instance/static methods
- Discriminators (single collection inheritance)
- Connection management (single and multi-database)

**Key patterns covered:**

- Schema definition with automatic TypeScript inference
- TypeScript typing (HydratedDocument, InferSchemaType, methods/statics/virtuals generics)
- CRUD operations (create, find, update, delete, lean vs hydrated)
- Middleware hooks and their execution rules
- Population with field selection and limits
- Transactions (withTransaction, transactionAsyncLocalStorage)
- Validation (built-in validators, custom validators, error messages)
- Virtuals (computed, populate virtuals)
- Discriminators (inheritance pattern)
- Connection setup and multi-database

**When NOT to use:**

- Raw MongoDB driver queries without schema enforcement (use the native driver)
- Relational data with complex joins and foreign key constraints (use a relational database)
- Simple key-value storage (use a dedicated key-value store)

**Detailed Resources:**

- For decision frameworks, quick reference tables, and migration notes, see [reference.md](reference.md)

**Core Patterns:**

- [examples/core.md](examples/core.md) -- Connection, schema definition, TypeScript typing, model creation, CRUD, validation

**Middleware & Lifecycle:**

- [examples/middleware.md](examples/middleware.md) -- Pre/post hooks, error handling middleware, query middleware, soft delete

**Relationships & Population:**

- [examples/population.md](examples/population.md) -- Populate, virtual populate, discriminators, embedding vs referencing

**Transactions & Advanced:**

- [examples/transactions.md](examples/transactions.md) -- Sessions, withTransaction, transactionAsyncLocalStorage, connection management

---

<philosophy>

## Philosophy

Mongoose provides schema-based modeling for MongoDB. Its value is the **application-layer enforcement** of structure, validation, middleware, and type safety on top of MongoDB's flexible document model.

**Core principles:**

1. **Schema-first** -- Define schemas before models. Schemas enforce structure, validation, defaults, and middleware at the application layer.
2. **Infer, don't duplicate** -- Let Mongoose infer TypeScript types from schema definitions. Only define explicit interfaces when adding methods, statics, or virtuals.
3. **Middleware before model** -- All pre/post hooks must be registered before `model()`. This is the single most common Mongoose bug -- hooks added after compilation are silently ignored.
4. **Lean for reads** -- `.lean()` returns plain JavaScript objects (3x less memory). Use it for every read-only query. Only skip lean when you need Mongoose document methods.
5. **Session discipline** -- Every operation inside a transaction must receive `{ session }`. One missed session means that operation runs outside the transaction with no error.
6. **Validate at the schema** -- Push validation into schema definitions (required, min, max, enum, custom validators with error messages). Don't validate in application code what the schema can enforce.

**When to use Mongoose:**

- You want schema enforcement and validation on MongoDB documents
- You need middleware hooks (pre/post save, validate, find)
- You want automatic TypeScript type inference from schemas
- You need population (reference resolution between collections)
- You want computed properties (virtuals) and instance methods

**When NOT to use Mongoose:**

- Performance-critical bulk operations where the ODM overhead matters (use native driver)
- You only need raw MongoDB queries without schema enforcement
- You're doing heavy aggregation-only workloads (aggregation pipelines bypass most Mongoose features)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Connection Setup

Establish a single connection at application startup. Use environment variables for credentials. Never hardcode connection strings.

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

  return mongoose.connect(uri, {
    maxPoolSize: POOL_SIZE_MAX,
    minPoolSize: POOL_SIZE_MIN,
    serverSelectionTimeoutMS: SERVER_SELECTION_TIMEOUT_MS,
    socketTimeoutMS: SOCKET_TIMEOUT_MS,
    retryWrites: true,
    retryReads: true,
  });
}

export { connectDatabase };
```

**Why good:** Named constants for all numeric values, environment variable for URI, typed return, error on missing URI

```typescript
// BAD: Hardcoded URI, localhost, no options
mongoose.connect("mongodb://localhost:27017/mydb");
```

**Why bad:** Hardcoded connection string leaks credentials, `localhost` fails on Node.js 18+ (IPv6 preference), no pool or timeout configuration

---

### Pattern 2: Schema Definition with TypeScript Inference

Let Mongoose infer types from the schema definition. Only use explicit interfaces when adding methods, statics, or virtuals.

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
  },
  { timestamps: true },
);

// TypeScript automatically infers the document type from schema
const User = model("User", userSchema);
export { User, userSchema };
```

**Why good:** TypeScript infers types automatically, `as const` preserves enum literal types, timestamps via schema option, named exports

```typescript
// BAD: Duplicating interface and schema definition
interface IUser {
  name: string;
  email: string;
}
const userSchema = new Schema({ name: String, email: String });
// Types drift apart -- schema allows undefined, interface says required
```

**Why bad:** Manual interface duplicates schema, they drift out of sync, no validation constraints, no error messages

---

### Pattern 3: Explicit Typing (Methods, Statics, Virtuals)

When a model has instance methods, statics, or virtuals, use the full generic parameter set.

```typescript
import {
  Schema,
  model,
  type HydratedDocument,
  type Model,
  type Types,
} from "mongoose";

interface IUser {
  email: string;
  passwordHash: string;
  firstName: string;
  lastName: string;
  role: "admin" | "user" | "moderator";
}

interface IUserMethods {
  comparePassword(candidate: string): Promise<boolean>;
}

interface IUserVirtuals {
  fullName: string;
}

type UserModel = Model<IUser, {}, IUserMethods, IUserVirtuals>;
type UserDocument = HydratedDocument<IUser, IUserMethods & IUserVirtuals>;

const userSchema = new Schema<
  IUser,
  UserModel,
  IUserMethods,
  {},
  IUserVirtuals
>(
  {
    /* fields */
  },
  { toJSON: { virtuals: true } },
);

userSchema.methods.comparePassword = async function (candidate: string) {
  // implementation
  return false;
};

userSchema.virtual("fullName").get(function () {
  return `${this.firstName} ${this.lastName}`;
});

// Middleware BEFORE model()
userSchema.pre("save", async function () {
  if (this.isModified("passwordHash")) {
    // hash password
  }
});

// model() AFTER all middleware and methods
const User = model<IUser, UserModel>("User", userSchema);

export { User, userSchema };
export type { IUser, IUserMethods, UserDocument };
```

**Why good:** Separate interfaces for document, methods, virtuals; correct generic parameter order; `HydratedDocument` exported for consumers; middleware before `model()`

See [examples/core.md](examples/core.md) for the complete implementation with all generic parameters.

---

### Pattern 4: CRUD Operations

```typescript
// Create -- triggers save middleware
const user = await User.create({ name: "Alice", email: "alice@example.com" });

// Read with lean (read-only response)
const PAGE_SIZE = 20;
const users = await User.find({ isActive: true })
  .select("name email role")
  .sort({ createdAt: -1 })
  .limit(PAGE_SIZE)
  .lean();

// Update with save() -- triggers pre('save') middleware
const doc = await User.findById(id);
if (!doc) throw new Error(`User not found: ${id}`);
doc.name = "Updated";
await doc.save();

// Direct update -- does NOT trigger save middleware
await User.findByIdAndUpdate(
  id,
  { $set: { name: "Updated" } },
  {
    new: true, // return updated document
    runValidators: true, // enforce schema validation
  },
);
```

**Why good:** `.lean()` for read-only, `save()` when middleware matters, `{ new: true, runValidators: true }` on direct updates

```typescript
// BAD: lean() then trying to save
const user = await User.findById(id).lean();
user.name = "Updated";
await user.save(); // TypeError: user.save is not a function
```

**Why bad:** `.lean()` returns plain objects without Mongoose methods -- `.save()` does not exist

---

### Pattern 5: Schema Validation

```typescript
const MIN_NAME_LENGTH = 2;
const MAX_NAME_LENGTH = 100;
const SKU_PATTERN = /^[A-Z]{2}-\d{6}$/;

const productSchema = new Schema({
  name: {
    type: String,
    required: [true, "Product name is required"],
    minlength: [
      MIN_NAME_LENGTH,
      `Name must be at least ${MIN_NAME_LENGTH} characters`,
    ],
    maxlength: [
      MAX_NAME_LENGTH,
      `Name must be at most ${MAX_NAME_LENGTH} characters`,
    ],
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
    match: [SKU_PATTERN, "SKU must match format XX-000000"],
  },
  status: {
    type: String,
    enum: {
      values: ["draft", "active", "archived"] as const,
      message: "{VALUE} is not a valid status",
    },
    default: "draft",
  },
});

export { productSchema };
```

**Why good:** Named constants for validation limits, custom error messages on every validator, regex validation with descriptive message, enum with `as const` for TypeScript inference

See [examples/core.md](examples/core.md) for subdocument schemas and array validation.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Registering middleware after `model()` call -- hooks are silently ignored, no error thrown
- Running operations in parallel inside a transaction (`Promise.all()`) -- MongoDB does not support parallel operations within a single transaction session
- Missing `{ session }` on any operation inside a transaction -- that operation runs outside the transaction silently
- Using `localhost` in connection strings on Node.js 18+ -- IPv6 preference causes connection timeouts, use `127.0.0.1`
- Mutating a document fetched with `.lean()` and calling `.save()` -- lean returns plain objects without Mongoose methods

**Medium Priority Issues:**

- Using `findOneAndUpdate`/`updateOne` and expecting `pre('save')` to fire -- only `save()` and `create()` trigger document middleware
- Unbounded `.populate()` without `limit` or field selection -- can return thousands of documents per populate call, each is a separate DB round-trip
- Not passing `runValidators: true` on `findOneAndUpdate` -- schema validation is skipped by default on direct updates
- Using `Schema.Types.ObjectId` in TypeScript interfaces -- use `Types.ObjectId` for interfaces, `Schema.Types.ObjectId` for schema definitions only
- Creating indexes in production application code instead of migration scripts -- index builds can lock the collection

**Common Mistakes:**

- Forgetting `{ new: true }` on `findOneAndUpdate` -- returns the old document by default, not the updated one
- Using `next()` callbacks in pre hooks on Mongoose 9 -- `next()` was removed in v9, use async/await
- Not handling duplicate key errors (error code 11000) from unique indexes
- Using `.lean()` on write operations -- lean is for reads only
- Checking `doc.isNew` in `post('save')` hooks -- always `false` after save; capture in `pre('save')` via `this.$locals.wasNew`
- Defining the same middleware hook multiple times without realizing they stack (all run, not just the last one)
- Using `extends Document` on interfaces -- deprecated pattern that breaks type inference for lean documents and query filters

**Gotchas & Edge Cases:**

- MongoDB has a 16 MB document size limit -- deeply embedded arrays can silently hit this
- Mongoose buffers all operations until connected -- queries queue silently if connection fails, which can mask connection issues in development
- `deleteOne`/`deleteMany` on the Model do not trigger document `pre('deleteOne')` middleware -- they trigger query middleware instead; use `doc.deleteOne()` for document middleware
- Virtual properties are excluded from `toJSON()`/`toObject()` by default -- set `{ toJSON: { virtuals: true } }` in schema options or they disappear in API responses
- `insertMany()` does not trigger `save` middleware -- it triggers `insertMany` model middleware only
- Mongoose 9 renamed `FilterQuery` to `QueryFilter` -- update TypeScript imports if upgrading
- Mongoose 9 disallows pipeline-style updates by default -- pass `{ updatePipeline: true }` or they throw
- `create()` with an array requires array syntax for `{ session }`: `Model.create([data], { session })` -- the non-array form `Model.create(data, { session })` does not work in transactions

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define all middleware (pre/post hooks) BEFORE calling `model()` -- hooks registered after model compilation are silently ignored with no error)**

**(You MUST pass `{ session }` to EVERY operation inside a transaction -- missing session causes that operation to run outside the transaction silently)**

**(You MUST use `.lean()` for read-only queries returning API responses -- skipping lean wastes 3x memory on hydration overhead)**

**(You MUST use `127.0.0.1` instead of `localhost` in connection strings -- Node.js 18+ prefers IPv6 and `localhost` causes connection timeouts)**

**(You MUST NOT use `findOneAndUpdate`/`updateOne` and expect `pre('save')` to fire -- only `save()` and `create()` trigger document middleware)**

**(You MUST NOT use `next()` callbacks in pre hooks on Mongoose 9 -- use async/await instead; `next()` was removed in v9)**

**Failure to follow these rules will cause silent middleware bypass, transaction isolation failures, or connection timeouts.**

</critical_reminders>
