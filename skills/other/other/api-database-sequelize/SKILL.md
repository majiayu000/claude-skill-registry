---
name: api-database-sequelize
description: Sequelize ORM, model definitions, associations, queries, transactions, migrations
---

# Database with Sequelize ORM

> **Quick Guide:** Sequelize is a promise-based ORM for PostgreSQL, MySQL, MariaDB, SQLite, and MS SQL Server. Use class-based models with `Model.init()` (v6) or decorators (v7) for type-safe definitions. Always use `InferAttributes`/`InferCreationAttributes` with `declare` for TypeScript models. Use `include` for eager loading to avoid N+1. Prefer managed transactions (auto-commit/rollback). Association alias (`as`) must match between definition and `include`. Paranoid mode requires `timestamps: true`. v7 is alpha --- most production code uses v6.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `declare` on all model class properties to prevent TypeScript from emitting class fields that conflict with Sequelize's internal attribute storage)**

**(You MUST pass `{ transaction: t }` to every query inside a transaction callback --- missing this causes operations to run outside the transaction and skip rollback)**

**(You MUST use `include` for eager loading related models --- fetching associations in loops creates N+1 query problems)**

**(You MUST match the `as` alias in `include` with the alias used in the association definition --- mismatches silently return `null` for the association)**

</critical_requirements>

---

**Auto-detection:** sequelize, Sequelize, Model.init, DataTypes, InferAttributes, InferCreationAttributes, CreationOptional, belongsTo, hasMany, hasOne, belongsToMany, findAll, findByPk, Op.and, Op.or, sequelize-cli, queryInterface, paranoid

**When to use:**

- SQL database access with model-based ORM (PostgreSQL, MySQL, MariaDB, SQLite, MSSQL)
- Projects needing fine-grained control over generated SQL and query composition
- Legacy codebases already using Sequelize
- Applications needing raw SQL escape hatches alongside ORM queries

**When NOT to use:**

- Greenfield TypeScript projects wanting schema-first design with auto-generated types
- Edge/serverless with cold-start sensitivity (Sequelize has heavy initialization)
- Projects needing auto-generated TypeScript types from schema (Sequelize types are manual)

**Key patterns covered:**

- Model definitions with TypeScript (InferAttributes, CreationOptional, declare)
- Associations (hasOne, hasMany, belongsTo, belongsToMany) and alias gotchas
- Eager loading (include), lazy loading, and N+1 prevention
- Transactions (managed vs unmanaged) and CLS auto-pass
- Scopes (defaultScope, named scopes, merging behavior)
- Paranoid mode (soft deletes) and its interaction with queries
- Hooks/lifecycle and their bulk operation gaps
- Migrations with queryInterface
- Raw queries and operators (Op)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Instance setup, model definitions, TypeScript patterns, CRUD
- [examples/associations.md](examples/associations.md) - Association types, eager loading, alias patterns
- [examples/transactions.md](examples/transactions.md) - Managed/unmanaged transactions, CLS, error handling
- [examples/advanced.md](examples/advanced.md) - Scopes, hooks, paranoid mode, raw queries, operators, migrations
- [reference.md](reference.md) - Decision frameworks, operator tables, hook order, anti-patterns

---

<philosophy>

## Philosophy

**Sequelize** is a traditional, feature-rich ORM that maps JavaScript classes to database tables. Unlike schema-first ORMs, you define models in code and optionally generate migrations from them.

**Core principles:**

1. **Model-first design** --- Define models as classes, then sync or migrate the database
2. **Explicit over implicit** --- Associations, hooks, and scopes are declared manually
3. **SQL escape hatch** --- Raw queries available when ORM abstractions are insufficient
4. **Dialect abstraction** --- Same API across PostgreSQL, MySQL, SQLite, MariaDB, MSSQL

**v6 vs v7:**

- **v6** is the current stable release used in production. Uses `Model.init()` for model definitions.
- **v7** is in alpha. Uses decorators (`@Attribute`, `@PrimaryKey`), scoped packages (`@sequelize/core`), and CLS is enabled by default via `AsyncLocalStorage`. The CLI is not yet ready for v7.
- All examples in this skill default to **v6 patterns** with v7 differences noted where significant.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Sequelize Instance Setup

Configure the connection with dialect, pool, and logging options.

```typescript
import { Sequelize } from "sequelize";

const MIN_POOL_SIZE = 0;
const MAX_POOL_SIZE = 10;
const POOL_ACQUIRE_TIMEOUT_MS = 30000;
const POOL_IDLE_TIMEOUT_MS = 10000;

export const sequelize = new Sequelize({
  dialect: "postgres",
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT),
  database: process.env.DB_NAME,
  username: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  logging: process.env.NODE_ENV === "development" ? console.log : false,
  pool: {
    min: MIN_POOL_SIZE,
    max: MAX_POOL_SIZE,
    acquire: POOL_ACQUIRE_TIMEOUT_MS,
    idle: POOL_IDLE_TIMEOUT_MS,
  },
});
```

**Why good:** Named constants for pool config, conditional logging, explicit pool sizing

```typescript
// BAD: Connection string with no pool config
const sequelize = new Sequelize("postgres://user:pass@localhost:5432/db");
```

**Why bad:** Default pool settings may exhaust connections under load, no logging control

> See [examples/core.md](examples/core.md) for connection URI patterns and graceful shutdown.

---

### Pattern 2: Model Definition with TypeScript

Use `InferAttributes`, `InferCreationAttributes`, and `declare` for type-safe models.

```typescript
import {
  Model,
  DataTypes,
  type InferAttributes,
  type InferCreationAttributes,
  type CreationOptional,
} from "sequelize";
import { sequelize } from "./connection";

export class User extends Model<
  InferAttributes<User>,
  InferCreationAttributes<User>
> {
  declare id: CreationOptional<number>;
  declare email: string;
  declare name: string | null;
  declare role: CreationOptional<string>;
  declare createdAt: CreationOptional<Date>;
  declare updatedAt: CreationOptional<Date>;
}

User.init(
  {
    id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true },
    email: { type: DataTypes.STRING, allowNull: false, unique: true },
    name: { type: DataTypes.STRING, allowNull: true },
    role: { type: DataTypes.STRING, allowNull: false, defaultValue: "user" },
    createdAt: DataTypes.DATE,
    updatedAt: DataTypes.DATE,
  },
  { sequelize, tableName: "users" },
);
```

**Why good:** `declare` prevents TS from emitting class fields, `CreationOptional` marks auto-generated fields, explicit `tableName` avoids pluralization surprises

```typescript
// BAD: Missing declare keyword
export class User extends Model {
  id!: number; // Emitted as class field, conflicts with Sequelize internals
  email!: string;
}
```

**Why bad:** Without `declare`, TypeScript emits class fields that override Sequelize's internal getters/setters, causing silent data loss

> See [examples/core.md](examples/core.md) for association mixin typing and NonAttribute usage.

---

### Pattern 3: Associations

Define relationships between models. The `as` alias is critical for eager loading.

```typescript
// One-to-Many: User has many Posts
User.hasMany(Post, { foreignKey: "authorId", as: "posts" });
Post.belongsTo(User, { foreignKey: "authorId", as: "author" });

// Many-to-Many: Post has many Tags through PostTag
Post.belongsToMany(Tag, { through: PostTag, foreignKey: "postId", as: "tags" });
Tag.belongsToMany(Post, { through: PostTag, foreignKey: "tagId", as: "posts" });
```

**Why good:** Explicit `foreignKey` prevents naming ambiguity, `as` enables clean eager loading

```typescript
// BAD: No alias, then trying to include with one
User.hasMany(Post, { foreignKey: "authorId" });
// Later:
User.findAll({ include: { model: Post, as: "posts" } }); // Error or null!
```

**Why bad:** If you define the association without `as`, you cannot use `as` in `include` --- Sequelize won't find the association. The alias must match exactly between definition and query.

> See [examples/associations.md](examples/associations.md) for all association types, eager loading, and the include alias contract.

---

### Pattern 4: Eager Loading with Include

Fetch related models in a single query to avoid N+1.

```typescript
const DEFAULT_PAGE_SIZE = 20;

// Include with alias (must match association definition)
const users = await User.findAll({
  include: [{ model: Post, as: "posts" }],
  limit: DEFAULT_PAGE_SIZE,
});

// Nested includes
const posts = await Post.findAll({
  include: [
    {
      model: User,
      as: "author",
      include: [{ model: Profile, as: "profile" }],
    },
    { model: Tag, as: "tags" },
  ],
});
```

**Why good:** Single query with JOINs, nested includes for deep relations, alias matches definition

```typescript
// BAD: N+1 query pattern
const users = await User.findAll();
for (const user of users) {
  const posts = await Post.findAll({ where: { authorId: user.id } }); // N queries!
}
```

**Why bad:** 1 query for users + N queries for posts, performance degrades linearly with record count

> See [examples/associations.md](examples/associations.md) for required includes (INNER JOIN), separate queries, and filtering included models.

---

### Pattern 5: Transactions (Managed)

Prefer managed transactions --- Sequelize auto-commits on success and auto-rolls back on thrown errors.

```typescript
const result = await sequelize.transaction(async (t) => {
  const user = await User.create(
    { email: "alice@example.com", name: "Alice" },
    { transaction: t },
  );

  await Profile.create(
    { userId: user.id, bio: "Developer" },
    { transaction: t },
  );

  return user;
});
// result is the return value of the callback
```

**Why good:** Auto-commit/rollback, clean error propagation, return value passed through

```typescript
// BAD: Forgetting to pass transaction
await sequelize.transaction(async (t) => {
  const user = await User.create({ email: "a@b.com" }); // Missing { transaction: t }!
  await Profile.create({ userId: user.id }, { transaction: t });
});
```

**Why bad:** `User.create` runs outside the transaction --- if `Profile.create` fails and rolls back, the user record persists, leaving inconsistent data

> See [examples/transactions.md](examples/transactions.md) for unmanaged transactions, CLS auto-pass, and isolation levels.

---

### Pattern 6: Paranoid Mode (Soft Deletes)

Paranoid mode sets `deletedAt` instead of deleting the row. Requires `timestamps: true`.

```typescript
export class Post extends Model<
  InferAttributes<Post>,
  InferCreationAttributes<Post>
> {
  declare id: CreationOptional<number>;
  declare title: string;
  declare deletedAt: CreationOptional<Date | null>;
  // ...
}

Post.init(
  {
    id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true },
    title: { type: DataTypes.STRING, allowNull: false },
  },
  { sequelize, tableName: "posts", paranoid: true },
);

// Soft delete --- sets deletedAt
await post.destroy();

// Hard delete --- actually removes the row
await post.destroy({ force: true });

// Restore soft-deleted record
await post.restore();

// Include soft-deleted records in queries
const allPosts = await Post.findAll({ paranoid: false });
```

**Why good:** `paranoid: true` enables soft deletes, `force: true` for hard delete escape hatch, `paranoid: false` in queries to include deleted records, `restore()` to undo

> See [examples/advanced.md](examples/advanced.md) for paranoid mode with eager loading gotchas.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using model properties without `declare` --- TypeScript emits class fields that override Sequelize getters/setters, causing silent data corruption
- Forgetting `{ transaction: t }` on queries inside transaction callbacks --- operations run outside the transaction and skip rollback
- N+1 queries in loops --- use `include` to eager load associations in a single query
- Mismatched `as` alias between association definition and `include` --- silently returns `null` for the association

**Medium Priority Issues:**

- Using `paranoid: true` with `timestamps: false` --- paranoid mode silently does nothing without timestamps
- Defining association without `as` then using `as` in `include` --- Sequelize cannot find the association
- Not defining both sides of an association --- only the model that calls `hasMany`/`belongsTo` gets accessor methods
- Missing `foreignKey` on associations --- Sequelize auto-generates names that may not match your database columns
- Using `findAll` without `limit` in production --- unbounded queries can crash the server

**Gotchas & Edge Cases:**

- `bulkCreate`/`update`/`destroy` (static) do NOT fire individual hooks (`beforeCreate`, `afterUpdate`) by default --- pass `{ individualHooks: true }` to enable (performance cost: loads all instances into memory)
- `defaultScope` is applied to ALL queries including `findByPk` --- use `.unscoped()` when you need unfiltered access
- Scopes with `where` on the same field **overwrite** (not AND) by default --- enable `whereMergeStrategy: 'and'` for combining
- `required: true` on `include` converts LEFT JOIN to INNER JOIN --- parent records without the association are excluded
- `save()` on a parent does NOT cascade to eager-loaded children --- save each child individually
- `belongsToMany` `through` junction table data is accessible via `record.JunctionModel` but easy to miss
- `Op.not` in v6 sometimes produces unexpected SQL depending on dialect --- test complex operator combinations
- Sequelize pluralizes table names by default (`User` -> `Users`) --- always set explicit `tableName`
- `BIGINT` and `DECIMAL` return strings in JavaScript, not numbers --- parse them at your boundary
- `afterCommit` hook only fires on successful commit, not on rollback --- don't use it for cleanup that must always run
- `findOrCreate` can fail with race conditions if no unique constraint exists on the `where` field
- `upsert` returns `[instance, created]` but `created` is unreliable on some dialects (MySQL/SQLite may always return `true` or `null`)
- Paranoid `findAll` with `where` on included paranoid models may unexpectedly return soft-deleted items
- Not calling `sequelize.close()` on shutdown leaks connections from the pool

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `declare` on all model class properties to prevent TypeScript from emitting class fields that conflict with Sequelize's internal attribute storage)**

**(You MUST pass `{ transaction: t }` to every query inside a transaction callback --- missing this causes operations to run outside the transaction and skip rollback)**

**(You MUST use `include` for eager loading related models --- fetching associations in loops creates N+1 query problems)**

**(You MUST match the `as` alias in `include` with the alias used in the association definition --- mismatches silently return `null` for the association)**

**Failure to follow these rules will cause silent data corruption, broken transactions, N+1 performance degradation, and missing association data.**

</critical_reminders>
