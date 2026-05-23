---
name: typeorm-patterns
description: Enforces TypeORM implementation patterns for this NestJS backend project. This skill should be used when creating or modifying TypeORM entities, repositories, database configuration, migrations, or any database-related code. It covers configuration patterns (TypeOrmModule.forRootAsync, replication, naming strategy), entity patterns (base entity, comments, indexes), and observability (X-Ray logging).
---

# TypeORM Patterns

## Overview

This skill enforces TypeORM implementation patterns for the NestJS backend project. It ensures consistent database configuration, entity design, repository patterns, and observability across the codebase.

## Core Requirements

### Configuration Requirements

| Requirement | Details |
|-------------|---------|
| **Module Pattern** | `TypeOrmModule.forRootAsync()` with `dataSourceFactory` |
| **Naming Strategy** | `SnakeNamingStrategy` from `typeorm-naming-strategies` |
| **Synchronize** | Always `false` - migrations only, no auto-sync |
| **Entity Loading** | Explicit entity exports via index.ts (esbuild compatibility) |
| **Database** | PostgreSQL (local Docker, AWS Aurora Serverless v2 production) |

### Environment-Based Configuration

| Environment | Connection Type | Authentication |
|-------------|-----------------|----------------|
| **Local** | Direct connection | Environment variables |
| **Production** | Read-write replication | AWS RDS Signer (IAM) |

### Entity Requirements

| Requirement | Details |
|-------------|---------|
| **Abstract Base** | All entities extend `TimestampedEntity` (NOT TypeORM's `BaseEntity`) |
| **Primary Key** | UUID via `@PrimaryGeneratedColumn("uuid")` |
| **Column Comments** | Required on all columns via `@Column({ comment: "..." })` |
| **Foreign Keys** | Must be indexed via `@Index()` decorator |
| **Cascade Deletes** | Use `orphanedRowAction: "delete"` on OneToMany relations |

**Note**: We use `TimestampedEntity` to avoid confusion with TypeORM's built-in `BaseEntity` class which provides Active Record pattern methods. Our abstract class only provides column inheritance.

### Observability Requirements

| Requirement | Details |
|-------------|---------|
| **Logger** | Custom `TypeOrmXRayLogger` for distributed tracing |
| **Graceful Degradation** | Logger must work locally without X-Ray SDK |
| **Query Tracking** | Extract query type and table name for metrics |

## Quick Reference

### Database Module Setup

Use the standard NestJS `TypeOrmModule.forRootAsync()` with `dataSourceFactory` for full control:

```typescript
import { Module } from "@nestjs/common";
import { TypeOrmModule } from "@nestjs/typeorm";
import { DataSource } from "typeorm";
import { createTypeOrmOptions } from "./database.config";

/**
 * Database module using official NestJS TypeORM integration.
 *
 * @remarks
 * Uses forRootAsync with dataSourceFactory for:
 * - Async configuration (environment-based)
 * - Custom DataSource initialization
 * - Replication support with dynamic passwords
 */
@Module({
  imports: [
    TypeOrmModule.forRootAsync({
      useFactory: createTypeOrmOptions,
      dataSourceFactory: async (options) => {
        const dataSource = new DataSource(options);
        return dataSource.initialize();
      },
    }),
  ],
})
export class DatabaseModule {}
```

### Creating a New Entity

```typescript
import { Column, Entity, Index, JoinColumn, ManyToOne, OneToMany } from "typeorm";
import { TimestampedEntity } from "./timestamped.entity";

/**
 * Represents a user in the system.
 *
 * @remarks
 * Users belong to organizations and can have multiple watchlists.
 */
@Entity({ comment: "Application users with organization membership" })
export class User extends TimestampedEntity {
  @Column({ comment: "User email address for authentication" })
  @Index()
  email: string;

  @Column({ comment: "User display name", nullable: true })
  name: string | null;

  @Column({ comment: "Foreign key to organization", type: "uuid" })
  @Index()
  organizationId: string;

  @ManyToOne(() => Organization, { onDelete: "SET NULL", nullable: true })
  @JoinColumn()
  organization: Organization;

  @OneToMany(() => Watchlist, w => w.user, { orphanedRowAction: "delete" })
  watchlists: Watchlist[];
}
```

**Important**: The abstract `TimestampedEntity` does NOT have an `@Entity()` decorator - only concrete child entities get this decorator.

### Adding Entity to Exports

After creating any entity, add it to `src/database/entities/index.ts`:

```typescript
export { User } from "./user.entity";
export { Organization } from "./organization.entity";
// Add new entity here
```

### Using Repository Injection

With `TypeOrmModule`, use `@InjectRepository()` for standard repository access:

```typescript
import { Injectable } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { Repository } from "typeorm";
import { User } from "../entities/user.entity";

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private readonly userRepository: Repository<User>
  ) {}

  async findByEmail(email: string): Promise<User | null> {
    return this.userRepository.findOne({ where: { email } });
  }
}
```

### Creating a Custom Repository (When Needed)

Only create custom repositories when you need reusable query methods:

```typescript
import { Injectable } from "@nestjs/common";
import { DataSource, Repository } from "typeorm";
import { User } from "../entities/user.entity";

/**
 * Custom repository for complex User queries.
 */
@Injectable()
export class UserRepository extends Repository<User> {
  constructor(private readonly dataSource: DataSource) {
    super(User, dataSource.createEntityManager());
  }

  /**
   * Find users with full-text search.
   */
  async searchByName(query: string): Promise<User[]> {
    return this.createQueryBuilder("user")
      .where("user.name ILIKE :query", { query: `%${query}%` })
      .getMany();
  }
}
```

### Custom Repositories in Transactions

**Critical**: Class-based repositories extending `Repository<T>` do NOT work correctly inside transactions. Per [TypeORM documentation](https://typeorm.io/docs/working-with-entity-manager/custom-repository/), you must use `withRepository()`:

```typescript
// WRONG - repository uses wrong EntityManager, won't be transactional
async transferFunds(fromId: string, toId: string, amount: number): Promise<void> {
  await this.dataSource.transaction(async manager => {
    const from = await this.accountRepository.findOne({ where: { id: fromId } });
    // This query runs OUTSIDE the transaction!
  });
}

// CORRECT - use withRepository() for transactional operations
async transferFunds(fromId: string, toId: string, amount: number): Promise<void> {
  await this.dataSource.transaction(async manager => {
    const accountRepo = manager.withRepository(this.accountRepository);
    const from = await accountRepo.findOne({ where: { id: fromId } });
    // This query runs INSIDE the transaction
  });
}
```

## Read-Write Routing

TypeORM automatically routes queries based on operation type when replication is configured:

| Operation | Endpoint | Method Examples |
|-----------|----------|-----------------|
| **Read** | Slave (read replica) | `find()`, `findOne()`, `query()` with SELECT |
| **Write** | Master | `save()`, `insert()`, `update()`, `delete()` |

To force a specific connection:

```typescript
// Force master for reads (when consistency required)
await this.userRepository.manager.transaction(async manager => {
  const user = await manager.findOne(User, { where: { id } });
  // This read uses master connection
});

// QueryRunner for explicit control
const queryRunner = dataSource.createQueryRunner("master");
try {
  await queryRunner.query("SELECT * FROM users WHERE id = $1", [id]);
} finally {
  await queryRunner.release();
}
```

## Migration Workflow

Always use the migration scripts - never modify migration files directly:

```bash
# Generate migration from entity changes
bun migration:generate --name=AddUserEmailIndex

# Run pending migrations
bun migration:run

# Revert last migration
bun migration:revert
```

## File Structure

```
src/database/
├── database.module.ts          # NestJS module with TypeOrmModule.forRootAsync
├── database.config.ts          # Configuration factory
├── typeorm-xray-logger.ts      # Custom X-Ray logger
├── entities/
│   ├── index.ts                # Explicit entity exports
│   ├── timestamped.entity.ts   # Abstract base entity (no @Entity decorator)
│   ├── user.entity.ts
│   └── ...
├── repositories/               # Only if custom repositories needed
│   ├── index.ts
│   ├── user.repository.ts
│   └── ...
└── migrations/
    └── {timestamp}-{name}.ts
```

## Detailed References

For comprehensive implementation details, see:

- **[references/configuration-patterns.md](references/configuration-patterns.md)** - TypeOrmModule setup, replication, environment configuration
- **[references/entity-patterns.md](references/entity-patterns.md)** - Base entity, relationships, indexes, enums, views
- **[references/observability-patterns.md](references/observability-patterns.md)** - X-Ray logger implementation with graceful degradation
