---
name: vendure-entity-writing
description: Define Vendure database entities extending VendureEntity, with TypeORM decorators, relations, custom fields, and channel-awareness. Use when creating database models in Vendure.
version: 1.0.0
---

# Vendure Entity Writing

## Purpose

Guide creation of Vendure database entities following TypeORM and Vendure patterns.

## When NOT to Use

- Plugin structure only (use vendure-plugin-writing)
- GraphQL schema only (use vendure-graphql-writing)
- Reviewing entities (use vendure-entity-reviewing)

---

## FORBIDDEN Patterns

- Not extending VendureEntity
- Missing @Entity() decorator
- No migration file created
- Using `any` type on columns
- Missing indexes on foreign keys
- Direct repository access (use TransactionalConnection)
- Storing dates as strings (use Date type)

---

## REQUIRED Patterns

- extends VendureEntity
- @Entity() decorator
- DeepPartial<T> constructor input
- @Column() with proper types
- Migration file for schema changes
- TransactionalConnection for queries
- Proper relation decorators

---

## Workflow

### Step 1: Create Entity Class

```typescript
// my-entity.entity.ts
import { DeepPartial, VendureEntity } from "@vendure/core";
import { Column, Entity, Index, ManyToOne, OneToMany } from "typeorm";

@Entity()
export class MyEntity extends VendureEntity {
  constructor(input?: DeepPartial<MyEntity>) {
    super(input);
  }

  @Column()
  name: string;

  @Column({ type: "text", nullable: true })
  description: string | null;

  @Column({ type: "int", default: 0 })
  sortOrder: number;

  @Column({ type: "boolean", default: true })
  isActive: boolean;

  @Column({ type: "timestamp", nullable: true })
  publishedAt: Date | null;
}
```

### Step 2: Add Relations

```typescript
import { Product, Channel } from "@vendure/core";

@Entity()
export class MyEntity extends VendureEntity {
  constructor(input?: DeepPartial<MyEntity>) {
    super(input);
  }

  // Many-to-One (this entity belongs to one Product)
  @Index()
  @ManyToOne(() => Product, { onDelete: "CASCADE" })
  product: Product;

  // Store the foreign key explicitly (optional but recommended)
  @Column()
  productId: number;

  // One-to-Many (this entity has many children)
  @OneToMany(() => ChildEntity, (child) => child.parent)
  children: ChildEntity[];

  // Many-to-Many with join table
  @ManyToMany(() => Channel)
  @JoinTable()
  channels: Channel[];
}
```

### Step 3: Register in Plugin

```typescript
@VendurePlugin({
  imports: [PluginCommonModule],
  entities: [MyEntity, ChildEntity],
})
export class MyPlugin {}
```

### Step 4: Generate Migration

```bash
# Generate migration from entity changes
npm run migration:generate -- --name=AddMyEntity

# Or with TypeORM CLI
npx typeorm migration:generate -d ./src/migrations -n AddMyEntity
```

### Step 5: Create Service for Entity

```typescript
// my-entity.service.ts
import { Injectable } from "@nestjs/common";
import { TransactionalConnection, RequestContext, ID } from "@vendure/core";
import { MyEntity } from "./my-entity.entity";

@Injectable()
export class MyEntityService {
  constructor(private connection: TransactionalConnection) {}

  async findAll(ctx: RequestContext): Promise<MyEntity[]> {
    return this.connection.getRepository(ctx, MyEntity).find();
  }

  async findOne(ctx: RequestContext, id: ID): Promise<MyEntity | null> {
    return this.connection.getRepository(ctx, MyEntity).findOne({
      where: { id },
    });
  }

  async findWithRelations(
    ctx: RequestContext,
    id: ID,
  ): Promise<MyEntity | null> {
    return this.connection.getRepository(ctx, MyEntity).findOne({
      where: { id },
      relations: ["product", "children"],
    });
  }

  async create(ctx: RequestContext, input: CreateInput): Promise<MyEntity> {
    const entity = new MyEntity(input);
    return this.connection.getRepository(ctx, MyEntity).save(entity);
  }

  async update(
    ctx: RequestContext,
    id: ID,
    input: UpdateInput,
  ): Promise<MyEntity> {
    const entity = await this.findOne(ctx, id);
    if (!entity) {
      throw new Error(`Entity with id ${id} not found`);
    }

    // Handle InputMaybe - check both undefined AND null
    if (input.name !== undefined && input.name !== null) {
      entity.name = input.name;
    }
    if (input.description !== undefined) {
      entity.description = input.description; // null is valid for nullable
    }

    return this.connection.getRepository(ctx, MyEntity).save(entity);
  }

  async delete(ctx: RequestContext, id: ID): Promise<boolean> {
    const result = await this.connection
      .getRepository(ctx, MyEntity)
      .delete(id);
    return result.affected ? result.affected > 0 : false;
  }
}
```

---

## Common Patterns

### Channel-Aware Entity

```typescript
import { ChannelAware, VendureEntity, Channel } from "@vendure/core";
import { Entity, ManyToMany, JoinTable } from "typeorm";

@Entity()
export class MyChannelAwareEntity
  extends VendureEntity
  implements ChannelAware
{
  constructor(input?: DeepPartial<MyChannelAwareEntity>) {
    super(input);
  }

  @ManyToMany(() => Channel)
  @JoinTable()
  channels: Channel[];
}
```

### Soft Delete Entity

```typescript
import { SoftDeletable, VendureEntity } from "@vendure/core";
import { Column, Entity, DeleteDateColumn } from "typeorm";

@Entity()
export class MySoftDeleteEntity extends VendureEntity implements SoftDeletable {
  constructor(input?: DeepPartial<MySoftDeleteEntity>) {
    super(input);
  }

  @DeleteDateColumn()
  deletedAt: Date | null;
}
```

### Custom Fields on Existing Entity

```typescript
// In plugin configuration
@VendurePlugin({
  imports: [PluginCommonModule],
  configuration: (config) => {
    config.customFields.Product.push(
      {
        name: "myStringField",
        type: "string",
        label: [{ languageCode: "en", value: "My String Field" }],
      },
      {
        name: "myIntField",
        type: "int",
        defaultValue: 0,
      },
      {
        name: "myRelation",
        type: "relation",
        entity: MyEntity,
        eager: false,
      },
    );
    return config;
  },
})
export class CustomFieldsPlugin {}
```

### Entity with JSON Column

```typescript
@Entity()
export class MyEntityWithJson extends VendureEntity {
  constructor(input?: DeepPartial<MyEntityWithJson>) {
    super(input);
  }

  @Column({ type: "simple-json", nullable: true })
  metadata: Record<string, any> | null;

  @Column({ type: "simple-array", default: "" })
  tags: string[];
}
```

### Date Handling (UTC)

```typescript
@Entity()
export class MyEntityWithDates extends VendureEntity {
  constructor(input?: DeepPartial<MyEntityWithDates>) {
    super(input);
  }

  // Store as timestamp (UTC)
  @Column({ type: "timestamp", nullable: true })
  scheduledAt: Date | null;

  // For date-only comparisons, store as string
  @Column({ type: "varchar", length: 10, nullable: true })
  specificDate: string | null; // Format: YYYY-MM-DD
}
```

---

## Examples

### Example 1: Delivery Time Block Entity

```typescript
// Based on DeliveryManager plugin pattern
@Entity()
export class DeliveryTimeBlock extends VendureEntity {
  constructor(input?: DeepPartial<DeliveryTimeBlock>) {
    super(input);
  }

  @Column()
  startTime: string; // "09:00"

  @Column()
  endTime: string; // "12:00"

  @Column({ type: "int" })
  fee: number; // In smallest currency unit (cents)

  @Column()
  currencyCode: string;

  @Column({ type: "int" })
  maxDeliveries: number;

  @ManyToMany(() => DeliveryDay, (day) => day.timeBlocks)
  deliveryDays: DeliveryDay[];
}
```

### Example 2: Entity with Computed Property

```typescript
@Entity()
export class OrderExtension extends VendureEntity {
  constructor(input?: DeepPartial<OrderExtension>) {
    super(input);
  }

  @Index()
  @ManyToOne(() => Order)
  order: Order;

  @Column()
  orderId: number;

  @Column({ type: "int", default: 0 })
  deliveryAttempts: number;

  // Computed property (not stored in DB)
  get hasExceededAttempts(): boolean {
    return this.deliveryAttempts >= 3;
  }
}
```

---

## Migration Best Practices

```typescript
// migrations/1234567890-AddMyEntity.ts
import { MigrationInterface, QueryRunner, Table, TableIndex } from "typeorm";

export class AddMyEntity1234567890 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(
      new Table({
        name: "my_entity",
        columns: [
          { name: "id", type: "int", isPrimary: true, isGenerated: true },
          {
            name: "createdAt",
            type: "timestamp",
            default: "CURRENT_TIMESTAMP",
          },
          {
            name: "updatedAt",
            type: "timestamp",
            default: "CURRENT_TIMESTAMP",
          },
          { name: "name", type: "varchar" },
          { name: "productId", type: "int" },
        ],
      }),
    );

    await queryRunner.createIndex(
      "my_entity",
      new TableIndex({ columnNames: ["productId"] }),
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable("my_entity");
  }
}
```

---

## Troubleshooting

| Problem              | Cause                      | Solution                                |
| -------------------- | -------------------------- | --------------------------------------- |
| Entity not created   | Not in plugin entities     | Add to @VendurePlugin({ entities: [] }) |
| Column doesn't exist | Missing migration          | Generate and run migration              |
| Relation not loading | Missing eager or relations | Use relations: ['x'] in query           |
| Type error           | Wrong column type          | Match TypeScript type with DB type      |

---

## Related Skills

- **vendure-entity-reviewing** - Entity review
- **vendure-plugin-writing** - Plugin structure
- **vendure-graphql-writing** - GraphQL schema
