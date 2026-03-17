---
name: "nestjs-typeorm-integration"
description: "Use this skill whenever the user wants to set up, configure, or refactor TypeORM within a NestJS TypeScript project, including data sources, entities, migrations, repositories, relations, and transactional patterns."
---

# NestJS + TypeORM Integration Skill

## Purpose

You are a specialized assistant for **integrating TypeORM with NestJS** in a clean, scalable,
and production-friendly way.

Use this skill to:

- Set up **TypeORM** in a NestJS project (data source, modules, config)
- Define or refactor **entities** and their relations
- Configure **migrations** and environment-specific DB settings
- Wire **repositories** into services using Nest DI
- Implement **transactions** and **query patterns** safely
- Optimize DB usage (indexes, query patterns, relations loading) at a structural level

Do **not** use this skill for:

- General NestJS module/service/controller scaffolding → use `nestjs-project-scaffold` / `nestjs-modules-services-controllers`
- Authentication logic → use `nestjs-authentication`
- Supabase-specific flows → use Supabase skills (unless Supabase Postgres is accessed via TypeORM as a plain DB)

If `CLAUDE.md` exists, follow its rules on database choice, naming conventions, and directory layout.

---

## When To Apply This Skill

Trigger this skill when the user asks for things like:

- “Set up TypeORM in this NestJS API.”
- “Create entities and migrations for these tables in NestJS + TypeORM.”
- “Wire repositories into my Nest services.”
- “Fix or refactor our NestJS TypeORM config.”
- “Add relations between these entities and update the service logic.”
- “Handle transactions for this multi-step operation.”

Avoid using this skill when:

- Only high-level REST API contracts are changing without DB impact.
- Only pure in-memory logic is being implemented.

---

## Assumptions & Defaults

Unless the project states otherwise, assume:

- Database: Postgres (can be adapted to MySQL, SQLite, etc.)
- TypeORM version: current stable for NestJS
- Connection is configured via Nest’s `TypeOrmModule`
- Config is environment-driven via `@nestjs/config` and `.env` files
- Entities live in `src/modules/<feature>/entities` or `src/entities` depending on project style
- Migrations live in `src/migrations` or `migrations` directory

---

## High-Level Architecture

Recommended structure (adapt as needed):

```text
project-root/
  src/
    config/
      database.config.ts
    modules/
      user/
        user.module.ts
        user.service.ts
        user.controller.ts
        entities/
          user.entity.ts
      post/
        post.module.ts
        post.service.ts
        post.controller.ts
        entities/
          post.entity.ts
    infrastructure/
      database/
        ormconfig.ts or data-source.ts (optional central place)
  migrations/
    1710000000000-CreateUserTable.ts
    1710000001000-CreatePostTable.ts
```

This skill should align with the existing structure rather than forcing a totally new one, unless the project is greenfield.

---

## Step-by-Step Workflow

When this skill is active, follow these steps:

### 1. Set Up TypeORM Module Configuration

If TypeORM is not configured yet:

- Install TypeORM + DB driver for the chosen database.
- Configure `TypeOrmModule` in `AppModule` or a dedicated `DatabaseModule`.

Example using `@nestjs/config`:

```ts
// src/config/database.config.ts
import { registerAs } from "@nestjs/config";

export default registerAs("database", () => ({
  type: "postgres",
  host: process.env.DB_HOST ?? "localhost",
  port: parseInt(process.env.DB_PORT ?? "5432", 10),
  username: process.env.DB_USERNAME ?? "postgres",
  password: process.env.DB_PASSWORD ?? "postgres",
  database: process.env.DB_NAME ?? "app_db",
}));
```

```ts
// src/app.module.ts
import { Module } from "@nestjs/common";
import { ConfigModule, ConfigService } from "@nestjs/config";
import databaseConfig from "./config/database.config";
import { TypeOrmModule } from "@nestjs/typeorm";

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      load: [databaseConfig],
    }),
    TypeOrmModule.forRootAsync({
      inject: [ConfigService],
      useFactory: (config: ConfigService) => {
        const db = config.get("database");
        return {
          ...db,
          autoLoadEntities: true,
          synchronize: false, // prefer migrations in production
        };
      },
    }),
    // feature modules...
  ],
})
export class AppModule {}
```

Key rules:

- `synchronize: false` in all non-dev environments (this skill encourages migrations).
- `autoLoadEntities: true` is acceptable for many apps; for stricter control, explicitly list entities.

### 2. Environment Variables

Ensure `.env` (and `.env.example`) contain:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_NAME=app_db
```

This skill should help keep secrets out of code and only in env/config.

### 3. Entities Design

For each feature, create entity classes:

```ts
// src/modules/user/entities/user.entity.ts
import {
  Column,
  CreateDateColumn,
  Entity,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
} from "typeorm";

@Entity({ name: "users" })
export class User {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column({ unique: true })
  email!: string;

  @Column()
  passwordHash!: string;

  @Column({ default: true })
  isActive!: boolean;

  @CreateDateColumn()
  createdAt!: Date;

  @UpdateDateColumn()
  updatedAt!: Date;
}
```

Relations example:

```ts
// src/modules/post/entities/post.entity.ts
import {
  Column,
  CreateDateColumn,
  Entity,
  ManyToOne,
  PrimaryGeneratedColumn,
} from "typeorm";
import { User } from "../../user/entities/user.entity";

@Entity({ name: "posts" })
export class Post {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column()
  title!: string;

  @Column({ type: "text" })
  content!: string;

  @ManyToOne(() => User, (user) => user.posts, { onDelete: "CASCADE" })
  author!: User;

  @CreateDateColumn()
  createdAt!: Date;
}
```

This skill should:

- Encourage using `uuid` or bigint for IDs consistently (per project preference).
- Use clear relation options (`onDelete`, `eager`, `lazy`) thoughtfully.
- Avoid putting heavy business logic directly into entities.

### 4. Module & Repository Wiring

Use `TypeOrmModule.forFeature` to inject repositories into feature modules:

```ts
// src/modules/user/user.module.ts
import { Module } from "@nestjs/common";
import { TypeOrmModule } from "@nestjs/typeorm";
import { User } from "./entities/user.entity";
import { UserService } from "./user.service";
import { UserController } from "./user.controller";

@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService],
})
export class UserModule {}
```

In `UserService`, inject the repository:

```ts
// src/modules/user/user.service.ts
import { Injectable } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { Repository } from "typeorm";
import { User } from "./entities/user.entity";
import { CreateUserDto } from "./dto/create-user.dto";

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private readonly usersRepo: Repository<User>,
  ) {}

  create(dto: CreateUserDto) {
    const entity = this.usersRepo.create({
      email: dto.email,
      passwordHash: dto.passwordHash,
    });
    return this.usersRepo.save(entity);
  }

  findAll() {
    return this.usersRepo.find();
  }

  findOne(id: string) {
    return this.usersRepo.findOne({ where: { id } });
  }

  // etc...
}
```

This skill should enforce:

- Repositories are injected via DI, not instantiated manually.
- Services depend on repositories, not on the data source directly (except in advanced scenarios).

### 5. Migrations

Encourage using migrations instead of `synchronize` for schema changes.

- Create a `data-source.ts` file if needed for CLI migrations:

```ts
// data-source.ts (or src/infrastructure/database/data-source.ts)
import "reflect-metadata";
import { DataSource } from "typeorm";
import databaseConfig from "./src/config/database.config";
import { config as loadEnv } from "dotenv";

loadEnv();

const db = databaseConfig();

export const AppDataSource = new DataSource({
  type: "postgres",
  host: db.database.host,
  port: db.database.port,
  username: db.database.username,
  password: db.database.password,
  database: db.database.database,
  entities: ["src/**/*.entity.{ts,js}"],
  migrations: ["migrations/*.{ts,js}"],
});
```

- Add package.json scripts for migrations (exact form depends on project):

```jsonc
{
  "scripts": {
    "typeorm:run": "typeorm-ts-node-commonjs migration:run -d data-source.ts",
    "typeorm:revert": "typeorm-ts-node-commonjs migration:revert -d data-source.ts",
    "typeorm:generate": "typeorm-ts-node-commonjs migration:generate -d data-source.ts migrations/AutoMigration"
  }
}
```

This skill should:

- Prefer explicit migration generation (`migration:generate`) over schema sync.
- Keep migration files small, ordered, and committed to version control.

### 6. Transactions & Complex Operations

For operations that require multiple DB writes, this skill should:

- Use `QueryRunner` or `manager.transaction` where needed.

Example:

```ts
import { DataSource } from "typeorm";

@Injectable()
export class OrderService {
  constructor(private readonly dataSource: DataSource) {}

  async createOrderAndItems(dto: CreateOrderDto) {
    return this.dataSource.transaction(async (manager) => {
      const order = manager.create(Order, { /* ... */ });
      await manager.save(order);

      const items = dto.items.map((itemDto) =>
        manager.create(OrderItem, {
          order,
          // ...
        }),
      );
      await manager.save(items);

      return order;
    });
  }
}
```

Guidelines:

- Use transactions only where needed; avoid wrapping everything by default.
- Handle error propagation correctly; if the transaction throws, it rolls back.

### 7. Performance & Query Patterns

This skill should guide towards:

- Using `select` and projections instead of always loading entire entities.
- Avoiding N+1 queries with relation loading patterns when necessary.
- Adding indexes in migrations for frequently queried columns.
- Using pagination strategies (offset/limit or cursor-based) for large lists.

### 8. Refactoring Existing TypeORM Usage

When refactoring:

- Identify anti-patterns:
  - Manual connection creation (bypassing Nest DI)
  - Direct use of global `getRepository` instead of injected repositories
  - `synchronize: true` in production
- Replace with:
  - `TypeOrmModule` configuration
  - Injected `Repository<T>` or `DataSource`
  - Migrations for schema changes

This skill should try to minimize breaking changes while improving structure.

---

## Interaction with Other Skills

- `nestjs-project-scaffold`:
  - Provides the base Nest structure; this skill plugs DB configuration into it.
- `nestjs-modules-services-controllers`:
  - Uses modules/services; this skill adds entities + repositories behind those services.
- `nestjs-authentication`:
  - Depends on user entities and user repository; this skill provides that layer.
- TypeORM-specific skills (`typeorm-schema-design`, `typeorm-migrations-workflow`):
  - Can be used in addition for deeper DB design and migration strategies.

---

## Example Prompts That Should Use This Skill

- “Connect this NestJS app to Postgres via TypeORM and create User & Post entities.”
- “Refactor this hand-rolled DB code into proper TypeORM modules and services.”
- “Add migrations for these schema changes and wire them into our NestJS project.”
- “Implement a transactional operation that creates an order and its items.”
- “Fix this TypeORM config; it works locally but fails in production.”

For such prompts, rely on this skill to design and implement **NestJS + TypeORM integration** that
is robust, maintainable, and ready for production, while delegating non-DB concerns to other skills.
