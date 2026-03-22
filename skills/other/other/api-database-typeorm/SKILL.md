---
name: api-database-typeorm
description: Decorator-based ORM for TypeScript with Active Record and Data Mapper patterns
---

# Database with TypeORM

> **Quick Guide:** Use TypeORM for decorator-based database access with full TypeScript support. Schema defined via entity classes with `@Entity`, `@Column`, `@PrimaryGeneratedColumn`. Use Data Mapper pattern (repositories) over Active Record for non-trivial apps. **Never use `synchronize: true` in production** - use migrations. Prefer `insert()`/`update()` over `save()` when you know the operation type - `save()` always executes a SELECT first. Use `QueryRunner` transactions for full control. Eager relations only work with `find*` methods, not QueryBuilder.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST NEVER use `synchronize: true` in production - it can drop columns and lose data when entities change)**

**(You MUST use `insert()`/`update()` instead of `save()` when the operation type is known - `save()` always runs an extra SELECT query)**

**(You MUST use the provided `transactionalEntityManager` or `queryRunner.manager` inside transactions - NEVER use the global entity manager or repository)**

**(You MUST define relations with explicit `@JoinColumn()` on the owning side of `@OneToOne` and optionally `@ManyToOne`, and `@JoinTable()` on one side of `@ManyToMany`)**

</critical_requirements>

---

**Auto-detection:** typeorm, TypeORM, DataSource, @Entity, @Column, @PrimaryGeneratedColumn, @ManyToOne, @OneToMany, @ManyToMany, createQueryBuilder, getRepository, EntityManager, QueryRunner, migration:generate, migration:run

**When to use:**

- Decorator-based entity definitions with TypeScript
- Applications requiring both Active Record and Data Mapper patterns
- Complex queries needing QueryBuilder with joins and subqueries
- Projects where class-based ORM feels natural (especially with DI-based frameworks)

**When NOT to use:**

- Schema-first workflows (consider schema-first ORMs instead)
- Needing fully type-safe queries without runtime decorators (consider lighter ORMs)
- Edge/serverless with minimal cold start (decorator metadata adds weight)
- Projects avoiding `reflect-metadata` and `experimentalDecorators`

**Key patterns covered:**

- DataSource configuration and entity registration
- Entity definitions with decorators and column types
- Relations (OneToOne, OneToMany, ManyToOne, ManyToMany)
- Repository CRUD and QueryBuilder
- Migrations (generate, run, revert)
- Transactions (EntityManager callback, QueryRunner manual)
- `save()` vs `insert()`/`update()` performance

**Detailed Resources:**

- [examples/core.md](examples/core.md) - DataSource setup, entities, CRUD, repository patterns
- [examples/relations.md](examples/relations.md) - All relation types, eager/lazy loading, cascades
- [examples/query-builder.md](examples/query-builder.md) - Joins, subqueries, pagination, raw queries
- [examples/migrations.md](examples/migrations.md) - Generate, run, revert, CLI configuration
- [examples/transactions.md](examples/transactions.md) - EntityManager, QueryRunner, isolation levels
- [examples/advanced.md](examples/advanced.md) - Subscribers, listeners, tree entities, embedded entities
- [reference.md](reference.md) - Decision frameworks, anti-patterns, performance, checklists

---

<philosophy>

## Philosophy

**TypeORM** uses TypeScript decorators to define database entities as classes. It supports both the Active Record and Data Mapper patterns, giving teams flexibility in how they structure data access.

**Core principles:**

1. **Decorator-based schema** - Entities are classes decorated with `@Entity`, `@Column`, etc.
2. **Pattern flexibility** - Active Record for simplicity, Data Mapper for separation of concerns
3. **QueryBuilder power** - SQL-like fluent API for complex queries beyond simple `find*`
4. **Migration-driven** - Schema changes through versioned migration files, never auto-sync in production

**Active Record vs Data Mapper:**

- **Active Record**: Entities extend `BaseEntity`, call `User.find()`, `user.save()` directly. Good for small apps and rapid prototyping.
- **Data Mapper**: Entities are plain classes, repositories handle persistence (`userRepo.find()`, `userRepo.save()`). Better for complex apps, testing, and separation of concerns.

**Recommendation:** Use Data Mapper for any non-trivial application. Active Record couples domain logic to persistence, making testing and refactoring harder.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: DataSource Configuration

Configure the DataSource as a singleton. Export it for both the application and migration CLI.

```typescript
// data-source.ts
import { DataSource } from "typeorm";
import { User } from "./entities/user.entity";
import { Post } from "./entities/post.entity";

export const AppDataSource = new DataSource({
  type: "postgres",
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT),
  username: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME,
  entities: [User, Post],
  migrations: ["./src/migrations/*.ts"],
  synchronize: false, // NEVER true in production
  logging: process.env.NODE_ENV === "development",
});
```

**Why good:** Single DataSource export used by both app and CLI, `synchronize: false` prevents data loss, env vars for config

```typescript
// BAD: synchronize in production
const AppDataSource = new DataSource({
  synchronize: true, // Drops columns, loses data on entity changes
  entities: ["./src/**/*.entity.ts"], // Glob patterns are fragile
});
```

**Why bad:** `synchronize: true` alters schema on startup (can drop columns with data), glob entity paths break with bundlers and are non-deterministic

> See [examples/core.md](examples/core.md) for initialization, graceful shutdown, and entity registration patterns.

---

### Pattern 2: Entity Definition

Entities are classes with decorators mapping to database tables and columns.

```typescript
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  Index,
} from "typeorm";

@Entity("users") // Explicit table name
export class User {
  @PrimaryGeneratedColumn("uuid")
  id: string;

  @Column({ unique: true })
  email: string;

  @Column()
  name: string;

  @Column({ type: "enum", enum: ["user", "admin"], default: "user" })
  role: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

**Why good:** Explicit table name avoids casing issues, `uuid` for distributed-safe IDs, `CreateDateColumn`/`UpdateDateColumn` auto-managed by TypeORM, enum column with default

```typescript
// BAD: Missing explicit table name, no index on frequently queried column
@Entity() // Table name derived from class name - casing varies by database
export class UserProfile {
  @PrimaryGeneratedColumn() // Auto-increment integer - problematic for distributed systems
  id: number;

  @Column()
  userId: string; // No index, no foreign key relation defined
}
```

**Why bad:** Derived table names cause casing inconsistency across databases, auto-increment IDs conflict in distributed systems, missing indexes on lookup columns

> See [examples/core.md](examples/core.md) for column types, nullable columns, and default values.

---

### Pattern 3: Repository CRUD - `save()` vs `insert()`/`update()`

The critical performance distinction: `save()` always runs a SELECT first. Use `insert()`/`update()` when you know the operation.

```typescript
const userRepo = AppDataSource.getRepository(User);

// CREATING: Use insert() - single INSERT query
await userRepo.insert({
  email: "alice@example.com",
  name: "Alice",
});

// UPDATING: Use update() - single UPDATE query
const ACTIVE_ROLE = "admin";
await userRepo.update({ id: userId }, { role: ACTIVE_ROLE });

// UPSERTING: Use upsert() - INSERT ... ON CONFLICT
await userRepo.upsert(
  { email: "alice@example.com", name: "Alice Updated" },
  ["email"], // conflict columns
);

// save() - only when you need cascade saves or don't know if inserting/updating
const user = userRepo.create({ email: "bob@example.com", name: "Bob" });
await userRepo.save(user); // SELECT + INSERT (2 queries)
```

**Why good:** `insert()`/`update()` execute single queries, `upsert()` handles conflicts atomically, `save()` reserved for when cascades or ambiguous operations are needed

```typescript
// BAD: Using save() for everything
const user = new User();
user.email = "alice@example.com";
user.name = "Alice";
await userRepo.save(user); // Runs SELECT first, then INSERT - 2 round trips

// BAD: Using save() in a loop
for (const data of users) {
  await userRepo.save(data); // 2N queries instead of 1 bulk insert
}
```

**Why bad:** `save()` always runs SELECT + INSERT/UPDATE (2 round trips), in loops this becomes 2N queries; use `insert()` for bulk creates

> See [examples/core.md](examples/core.md) for find operations, bulk operations, and soft delete patterns.

---

### Pattern 4: Relations

Define relations with decorators. The owning side holds the foreign key.

```typescript
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  OneToMany,
  JoinColumn,
} from "typeorm";

@Entity("posts")
export class Post {
  @PrimaryGeneratedColumn("uuid")
  id: string;

  @Column()
  title: string;

  // Owning side - holds the foreign key column
  @ManyToOne(() => User, (user) => user.posts, { onDelete: "CASCADE" })
  @JoinColumn({ name: "author_id" }) // Explicit FK column name
  author: User;

  @Column()
  authorId: string; // Expose FK for queries without joining
}

@Entity("users")
export class User {
  @PrimaryGeneratedColumn("uuid")
  id: string;

  // Inverse side - no FK column here
  @OneToMany(() => Post, (post) => post.author)
  posts: Post[];
}
```

**Why good:** Explicit `@JoinColumn` names the FK column, `authorId` exposed for direct queries, `onDelete: "CASCADE"` prevents orphans, inverse side defined for bidirectional navigation

```typescript
// BAD: Missing JoinColumn, no onDelete, relation typed as required
@ManyToOne(() => User)
author: User; // No explicit FK column name, no cascade delete
```

**Why bad:** Auto-generated FK column name may not match conventions, missing `onDelete` leaves orphaned rows, relation property should be `User | undefined` since it's not always loaded

> See [examples/relations.md](examples/relations.md) for all relation types, ManyToMany with JoinTable, and eager/lazy loading.

---

### Pattern 5: QueryBuilder

For queries beyond simple `find*`, use the QueryBuilder's fluent API.

```typescript
const DEFAULT_PAGE_SIZE = 20;
const MAX_PAGE_SIZE = 100;

const users = await AppDataSource.getRepository(User)
  .createQueryBuilder("user")
  .leftJoinAndSelect("user.posts", "post", "post.published = :pub", {
    pub: true,
  })
  .where("user.role = :role", { role: "admin" })
  .andWhere("user.createdAt > :date", { date: new Date("2024-01-01") })
  .orderBy("user.createdAt", "DESC")
  .take(DEFAULT_PAGE_SIZE)
  .skip(0)
  .getMany();
```

**Why good:** Parameterized queries prevent SQL injection, `leftJoinAndSelect` loads relations in one query, `take`/`skip` for pagination (relation-safe unlike `limit`/`offset`)

```typescript
// BAD: String interpolation in where clause
const users = await userRepo
  .createQueryBuilder("user")
  .where(`user.email = '${email}'`) // SQL INJECTION!
  .getMany();
```

**Why bad:** String interpolation opens SQL injection vulnerability; always use `:paramName` with parameter objects

> See [examples/query-builder.md](examples/query-builder.md) for subqueries, aggregations, raw queries, and advanced joins.

---

### Pattern 6: Migrations

Generate migrations from entity changes, never manually write SQL unless necessary.

```bash
# Generate migration from entity diff
npx typeorm-ts-node-esm migration:generate ./src/migrations/AddUserRole -d ./src/data-source.ts

# Run all pending migrations
npx typeorm-ts-node-esm migration:run -d ./src/data-source.ts

# Revert last migration
npx typeorm-ts-node-esm migration:revert -d ./src/data-source.ts
```

**Why good:** Auto-generated migrations capture exact schema diff, `-d` flag points to DataSource config, `revert` undoes one migration at a time

> See [examples/migrations.md](examples/migrations.md) for migration class structure, manual migrations, and transaction control.

---

### Pattern 7: Transactions

Two approaches: EntityManager callback (simple) and QueryRunner (full control).

```typescript
// Approach 1: EntityManager callback - simple, auto-commits/rollbacks
await AppDataSource.transaction(async (manager) => {
  await manager.save(User, userData);
  await manager.save(Post, postData);
  // If any operation throws, entire transaction rolls back
});

// Approach 2: QueryRunner - manual control, reusable connection
const queryRunner = AppDataSource.createQueryRunner();
await queryRunner.connect();
await queryRunner.startTransaction();
try {
  await queryRunner.manager.save(User, userData);
  await queryRunner.manager.save(Post, postData);
  await queryRunner.commitTransaction();
} catch (error) {
  await queryRunner.rollbackTransaction();
  throw error;
} finally {
  await queryRunner.release(); // ALWAYS release
}
```

**Why good:** EntityManager callback is concise with auto-rollback, QueryRunner gives explicit commit/rollback control, `finally` block ensures connection release

```typescript
// BAD: Using global manager inside transaction
await AppDataSource.transaction(async (manager) => {
  await AppDataSource.manager.save(User, userData); // WRONG: bypasses transaction!
  await manager.save(Post, postData);
});
```

**Why bad:** `AppDataSource.manager` is the global manager, not the transactional one - operations using it run outside the transaction and won't roll back

> See [examples/transactions.md](examples/transactions.md) for isolation levels, QueryRunner patterns, and nested transactions.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- `synchronize: true` in production - alters schema on startup, can drop columns and lose data
- Using `save()` for all writes - always runs SELECT first, 2x round trips for known inserts/updates
- String interpolation in QueryBuilder `.where()` - SQL injection vulnerability
- Using global entity manager inside transactions - bypasses transaction context
- Missing `queryRunner.release()` in finally block - leaks database connections

**Medium Priority Issues:**

- No indexes on frequently filtered columns - slow queries as data grows
- Missing `onDelete` cascade on relations - orphaned rows when parent deleted
- Using `eager: true` on both sides of a relation - TypeORM disallows this, throws error
- Glob patterns for entity paths (`"./src/**/*.entity.ts"`) - breaks with bundlers
- Initializing relation arrays with `= []` - causes TypeORM to detach all existing relations on save

**Common Mistakes:**

- Expecting eager relations to work with QueryBuilder - eager only works with `find*` methods, use `leftJoinAndSelect` instead
- Using `@BeforeUpdate`/`@AfterUpdate` with `update()` - listeners only fire with `save()`, not `update()`/`insert()`
- Forgetting `reflect-metadata` import at app entry point - decorators silently fail
- Using `limit()`/`offset()` with joins in QueryBuilder - returns wrong results; use `take()`/`skip()` instead
- Not exposing FK column (e.g., `authorId`) alongside relation - forces a join for simple lookups

**Gotchas & Edge Cases:**

- `save()` returns the saved entity but reloads it from DB - the returned object may differ from input
- `update()` and `delete()` return `UpdateResult`/`DeleteResult` with affected count, not the entity
- `findOne({ where: {} })` with empty where returns the first row, not null - always provide conditions
- Enum changes in entity require a migration - database enum types don't auto-update
- `@Column({ select: false })` excludes column from default SELECTs - must explicitly select with QueryBuilder
- Lazy relations require `Promise<T>` type on the property - not intuitive for JS/TS developers
- `cascade: true` can save unintended nested objects - be explicit with `cascade: ["insert"]` or `cascade: ["update"]`
- Transaction isolation varies by database driver - not all levels available on all databases
- `QueryRunner` must be released even on success - failure to release leaks connections until pool exhaustion

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST NEVER use `synchronize: true` in production - it can drop columns and lose data when entities change)**

**(You MUST use `insert()`/`update()` instead of `save()` when the operation type is known - `save()` always runs an extra SELECT query)**

**(You MUST use the provided `transactionalEntityManager` or `queryRunner.manager` inside transactions - NEVER use the global entity manager or repository)**

**(You MUST define relations with explicit `@JoinColumn()` on the owning side of `@OneToOne` and optionally `@ManyToOne`, and `@JoinTable()` on one side of `@ManyToMany`)**

**Failure to follow these rules will cause data loss from schema sync, doubled query counts from unnecessary SELECTs, broken transaction atomicity, and connection pool exhaustion.**

</critical_reminders>
