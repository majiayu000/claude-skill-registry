---
name: sequelize
description: Guidelines for developing with Sequelize, a promise-based Node.js ORM supporting PostgreSQL, MySQL, MariaDB, SQLite, and SQL Server
---

# Sequelize Development Guidelines

You are an expert in Sequelize ORM, Node.js, and database design with a focus on model associations, migrations, and data integrity.

## Core Principles

- Sequelize is a promise-based ORM for Node.js and TypeScript
- Supports PostgreSQL, MySQL, MariaDB, SQLite, and Microsoft SQL Server
- Uses model definitions with DataTypes for schema declaration
- Provides comprehensive support for associations, transactions, and hooks
- Migrations should be used for all schema changes in production

## Database Connection

### Basic Setup

```typescript
import { Sequelize } from "sequelize";

// Option 1: Connection URI
const sequelize = new Sequelize(process.env.DATABASE_URL!, {
  dialect: "postgres",
  logging: process.env.NODE_ENV === "development" ? console.log : false,
  pool: {
    max: 10,
    min: 0,
    acquire: 30000,
    idle: 10000,
  },
});

// Option 2: Individual parameters
const sequelize = new Sequelize({
  dialect: "postgres",
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || "5432"),
  username: process.env.DB_USERNAME,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  logging: false,
});

// Test connection
async function testConnection() {
  try {
    await sequelize.authenticate();
    console.log("Connection established successfully.");
  } catch (error) {
    console.error("Unable to connect to the database:", error);
  }
}
```

## Model Definition

### Basic Model with TypeScript

```typescript
import {
  Model,
  DataTypes,
  InferAttributes,
  InferCreationAttributes,
  CreationOptional,
} from "sequelize";
import { sequelize } from "./database";

class User extends Model<InferAttributes<User>, InferCreationAttributes<User>> {
  declare id: CreationOptional<number>;
  declare email: string;
  declare name: string | null;
  declare isActive: CreationOptional<boolean>;
  declare createdAt: CreationOptional<Date>;
  declare updatedAt: CreationOptional<Date>;
}

User.init(
  {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
    },
    email: {
      type: DataTypes.STRING(255),
      allowNull: false,
      unique: true,
      validate: {
        isEmail: true,
      },
    },
    name: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    isActive: {
      type: DataTypes.BOOLEAN,
      defaultValue: true,
    },
    createdAt: DataTypes.DATE,
    updatedAt: DataTypes.DATE,
  },
  {
    sequelize,
    tableName: "users",
    modelName: "User",
    underscored: true, // Use snake_case for column names
  }
);

export { User };
```

### Data Types Reference

```typescript
// String types
DataTypes.STRING(255)      // VARCHAR(255)
DataTypes.TEXT             // TEXT
DataTypes.TEXT("tiny")     // TINYTEXT (MySQL)

// Numeric types
DataTypes.INTEGER          // INTEGER
DataTypes.BIGINT           // BIGINT
DataTypes.FLOAT            // FLOAT
DataTypes.DOUBLE           // DOUBLE
DataTypes.DECIMAL(10, 2)   // DECIMAL(10,2)

// Boolean
DataTypes.BOOLEAN          // BOOLEAN / TINYINT(1)

// Date/Time
DataTypes.DATE             // DATETIME/TIMESTAMP
DataTypes.DATEONLY         // DATE
DataTypes.TIME             // TIME

// Binary
DataTypes.BLOB             // BLOB

// JSON
DataTypes.JSON             // JSON (if supported)
DataTypes.JSONB            // JSONB (PostgreSQL)

// UUID
DataTypes.UUID             // UUID
DataTypes.UUIDV4           // Auto-generate UUID v4

// Enum
DataTypes.ENUM("active", "inactive", "pending")

// Array (PostgreSQL only)
DataTypes.ARRAY(DataTypes.STRING)
```

## Associations

### One-to-One

```typescript
class User extends Model {
  declare id: number;
  declare profile?: Profile;
}

class Profile extends Model {
  declare id: number;
  declare userId: number;
  declare bio: string;
  declare user?: User;
}

// Define associations
User.hasOne(Profile, {
  foreignKey: "userId",
  as: "profile",
});

Profile.belongsTo(User, {
  foreignKey: "userId",
  as: "user",
});
```

### One-to-Many

```typescript
class User extends Model {
  declare id: number;
  declare posts?: Post[];
}

class Post extends Model {
  declare id: number;
  declare authorId: number;
  declare title: string;
  declare author?: User;
}

// Define associations
User.hasMany(Post, {
  foreignKey: "authorId",
  as: "posts",
});

Post.belongsTo(User, {
  foreignKey: "authorId",
  as: "author",
});
```

### Many-to-Many

```typescript
class Post extends Model {
  declare id: number;
  declare tags?: Tag[];
}

class Tag extends Model {
  declare id: number;
  declare name: string;
  declare posts?: Post[];
}

// Define associations with junction table
Post.belongsToMany(Tag, {
  through: "PostTags",
  foreignKey: "postId",
  otherKey: "tagId",
  as: "tags",
});

Tag.belongsToMany(Post, {
  through: "PostTags",
  foreignKey: "tagId",
  otherKey: "postId",
  as: "posts",
});
```

## Querying

### Basic Queries

```typescript
// Find all
const users = await User.findAll();

// Find with conditions
const activeUsers = await User.findAll({
  where: {
    isActive: true,
  },
});

// Find one
const user = await User.findOne({
  where: { email: "user@example.com" },
});

// Find by primary key
const user = await User.findByPk(1);

// Find or create
const [user, created] = await User.findOrCreate({
  where: { email: "user@example.com" },
  defaults: {
    name: "New User",
  },
});
```

### Advanced Queries with Operators

```typescript
import { Op } from "sequelize";

// Multiple conditions
const users = await User.findAll({
  where: {
    [Op.and]: [
      { isActive: true },
      { createdAt: { [Op.gte]: new Date("2024-01-01") } },
    ],
  },
});

// OR condition
const users = await User.findAll({
  where: {
    [Op.or]: [{ name: "John" }, { name: "Jane" }],
  },
});

// LIKE
const users = await User.findAll({
  where: {
    email: { [Op.like]: "%@example.com" },
  },
});

// IN
const users = await User.findAll({
  where: {
    id: { [Op.in]: [1, 2, 3] },
  },
});

// Comparison operators
const users = await User.findAll({
  where: {
    id: { [Op.gt]: 10 },      // Greater than
    age: { [Op.gte]: 18 },    // Greater than or equal
    score: { [Op.lt]: 100 },  // Less than
    rank: { [Op.lte]: 5 },    // Less than or equal
    status: { [Op.ne]: "inactive" }, // Not equal
  },
});
```

### Eager Loading (Include)

```typescript
// Load user with posts
const user = await User.findOne({
  where: { id: 1 },
  include: [
    {
      model: Post,
      as: "posts",
    },
  ],
});

// Nested includes
const user = await User.findOne({
  where: { id: 1 },
  include: [
    {
      model: Post,
      as: "posts",
      include: [
        {
          model: Tag,
          as: "tags",
        },
      ],
    },
  ],
});

// Include with conditions
const users = await User.findAll({
  include: [
    {
      model: Post,
      as: "posts",
      where: {
        publishedAt: { [Op.ne]: null },
      },
      required: false, // LEFT JOIN (include users without posts)
    },
  ],
});
```

### Pagination and Ordering

```typescript
const page = 1;
const pageSize = 20;

const { count, rows: users } = await User.findAndCountAll({
  where: { isActive: true },
  order: [
    ["createdAt", "DESC"],
    ["name", "ASC"],
  ],
  limit: pageSize,
  offset: (page - 1) * pageSize,
});

const totalPages = Math.ceil(count / pageSize);
```

### Aggregations

```typescript
// Count
const count = await User.count({
  where: { isActive: true },
});

// Sum
const total = await Order.sum("amount", {
  where: { status: "completed" },
});

// Max/Min
const maxPrice = await Product.max("price");
const minPrice = await Product.min("price");

// Group by
const stats = await Order.findAll({
  attributes: [
    "status",
    [sequelize.fn("COUNT", sequelize.col("id")), "count"],
    [sequelize.fn("SUM", sequelize.col("amount")), "total"],
  ],
  group: ["status"],
});
```

## CRUD Operations

### Create

```typescript
// Create single record
const user = await User.create({
  email: "user@example.com",
  name: "John Doe",
});

// Bulk create
const users = await User.bulkCreate(
  [
    { email: "user1@example.com", name: "User 1" },
    { email: "user2@example.com", name: "User 2" },
  ],
  {
    validate: true, // Run validations on each record
  }
);

// Create with associations
const user = await User.create(
  {
    email: "user@example.com",
    name: "John",
    profile: {
      bio: "Hello world",
    },
  },
  {
    include: [{ model: Profile, as: "profile" }],
  }
);
```

### Update

```typescript
// Update single record
const user = await User.findByPk(1);
if (user) {
  user.name = "Jane Doe";
  await user.save();
}

// Update with new data
await user.update({
  name: "Jane Doe",
  isActive: false,
});

// Bulk update
await User.update(
  { isActive: false },
  {
    where: {
      lastLoginAt: { [Op.lt]: new Date("2024-01-01") },
    },
  }
);
```

### Delete

```typescript
// Delete single record
const user = await User.findByPk(1);
if (user) {
  await user.destroy();
}

// Bulk delete
await User.destroy({
  where: {
    isActive: false,
  },
});

// Soft delete (requires paranoid: true in model options)
await user.destroy(); // Sets deletedAt instead of deleting

// Restore soft-deleted record
await user.restore();
```

## Transactions

```typescript
// Managed transaction (recommended)
const result = await sequelize.transaction(async (t) => {
  const user = await User.create(
    {
      email: "user@example.com",
      name: "User",
    },
    { transaction: t }
  );

  const post = await Post.create(
    {
      title: "First Post",
      authorId: user.id,
    },
    { transaction: t }
  );

  return { user, post };
});

// Unmanaged transaction
const t = await sequelize.transaction();

try {
  const user = await User.create(
    { email: "user@example.com" },
    { transaction: t }
  );

  await Post.create(
    { title: "Post", authorId: user.id },
    { transaction: t }
  );

  await t.commit();
} catch (error) {
  await t.rollback();
  throw error;
}
```

## Hooks

```typescript
User.init(
  {
    // ... columns
  },
  {
    sequelize,
    hooks: {
      beforeValidate: (user) => {
        // Normalize email
        if (user.email) {
          user.email = user.email.toLowerCase().trim();
        }
      },
      beforeCreate: async (user) => {
        // Hash password
        if (user.password) {
          user.password = await bcrypt.hash(user.password, 10);
        }
      },
      afterCreate: async (user) => {
        // Send welcome email
        await sendWelcomeEmail(user.email);
      },
      beforeDestroy: async (user) => {
        // Clean up related data
        await Post.destroy({ where: { authorId: user.id } });
      },
    },
  }
);

// Or define hooks separately
User.addHook("beforeSave", "hashPassword", async (user) => {
  if (user.changed("password")) {
    user.password = await bcrypt.hash(user.password, 10);
  }
});
```

### Hook with Transaction Access

```typescript
User.addHook("beforeCreate", async (user, options) => {
  if (options.transaction) {
    // Use the same transaction for related operations
    await AuditLog.create(
      {
        action: "user_created",
        userId: user.id,
      },
      { transaction: options.transaction }
    );
  }
});
```

## Validations

```typescript
User.init(
  {
    email: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        isEmail: {
          msg: "Must be a valid email address",
        },
        notEmpty: true,
      },
    },
    age: {
      type: DataTypes.INTEGER,
      validate: {
        min: {
          args: [0],
          msg: "Age must be non-negative",
        },
        max: {
          args: [150],
          msg: "Age must be realistic",
        },
      },
    },
    username: {
      type: DataTypes.STRING,
      validate: {
        len: {
          args: [3, 30],
          msg: "Username must be between 3 and 30 characters",
        },
        isAlphanumeric: {
          msg: "Username must contain only letters and numbers",
        },
        // Custom validator
        async isUnique(value: string) {
          const existing = await User.findOne({
            where: { username: value },
          });
          if (existing) {
            throw new Error("Username already taken");
          }
        },
      },
    },
  },
  { sequelize }
);
```

## Migrations

### Creating Migrations

```bash
# Generate migration
npx sequelize-cli migration:generate --name create-users

# Run migrations
npx sequelize-cli db:migrate

# Undo last migration
npx sequelize-cli db:migrate:undo

# Undo all migrations
npx sequelize-cli db:migrate:undo:all
```

### Migration File Structure

```typescript
// migrations/20240101000000-create-users.js
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable("users", {
      id: {
        type: Sequelize.INTEGER,
        autoIncrement: true,
        primaryKey: true,
      },
      email: {
        type: Sequelize.STRING(255),
        allowNull: false,
        unique: true,
      },
      name: {
        type: Sequelize.STRING(255),
        allowNull: true,
      },
      is_active: {
        type: Sequelize.BOOLEAN,
        defaultValue: true,
      },
      created_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal("CURRENT_TIMESTAMP"),
      },
      updated_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal("CURRENT_TIMESTAMP"),
      },
    });

    await queryInterface.addIndex("users", ["email"]);
  },

  async down(queryInterface) {
    await queryInterface.dropTable("users");
  },
};
```

## Best Practices

### Use Eager Loading to Avoid N+1

```typescript
// Bad: N+1 queries
const users = await User.findAll();
for (const user of users) {
  const posts = await user.getPosts(); // Query per user
}

// Good: Single query with include
const users = await User.findAll({
  include: [{ model: Post, as: "posts" }],
});
```

### Always Use Migrations in Production

```typescript
// sequelize config
{
  development: {
    // ...
  },
  production: {
    // ...
    migrationStorageTableName: "sequelize_migrations",
    seederStorageTableName: "sequelize_seeds",
  }
}
```

### Use Aliases for Associations

```typescript
// Good: Using aliases for clarity
User.hasMany(Post, { as: "posts", foreignKey: "authorId" });

// Query with alias
const user = await User.findOne({
  include: [{ model: Post, as: "posts" }],
});
```

### Validate in Bulk Operations

```typescript
// Always validate when using bulkCreate
await User.bulkCreate(users, { validate: true });
```

### Use Transactions for Data Integrity

```typescript
// Wrap related operations in transactions
await sequelize.transaction(async (t) => {
  // All operations use the same transaction
  const order = await Order.create({ ... }, { transaction: t });
  await OrderItem.bulkCreate(items, { transaction: t });
  await Inventory.decrement("quantity", { ... }, { transaction: t });
});
```

### Scope Common Queries

```typescript
User.addScope("active", {
  where: { isActive: true },
});

User.addScope("withPosts", {
  include: [{ model: Post, as: "posts" }],
});

// Use scopes
const activeUsers = await User.scope("active").findAll();
const usersWithPosts = await User.scope(["active", "withPosts"]).findAll();
```
