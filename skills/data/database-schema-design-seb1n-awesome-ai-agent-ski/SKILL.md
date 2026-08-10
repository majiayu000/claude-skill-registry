---
name: database-schema-design
description: Design normalized database schemas with tables, relationships, indexes, and constraints for any application domain. Use when the user requests database schema design or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: AI Agent Skills Community
  version: 1.0.0
---

# Database Schema Design

This skill enables an AI agent to design robust, normalized relational database schemas from application requirements. The agent analyzes entities, defines tables with appropriate data types and constraints, establishes relationships (one-to-one, one-to-many, many-to-many), applies normalization up to 3NF, creates indexes for query performance, and produces complete SQL DDL scripts ready for execution.

## Workflow

1. **Gather and analyze requirements:** Interview the user or parse a specification document to identify all entities, their attributes, and the relationships between them. Clarify cardinality (1:1, 1:N, M:N), required vs. optional fields, and any domain-specific constraints such as unique emails, positive prices, or enumerated statuses. Document assumptions explicitly before proceeding.

2. **Model entities and relationships:** Translate requirements into a logical data model. Define each entity as a table, choose appropriate primary keys (prefer surrogate integer or UUID keys for stability), and map relationships. For one-to-many, add a foreign key on the "many" side. For many-to-many, create a junction table with composite primary keys referencing both parent tables. For one-to-one, use a shared primary key or a unique foreign key.

3. **Apply normalization:** Review the schema against normal forms. Ensure every non-key column depends on the whole primary key (2NF) and only on the primary key (3NF). Split tables that contain transitive dependencies. Strategically denormalize only when justified by read-heavy query patterns, and document the trade-off.

4. **Define constraints and indexes:** Add NOT NULL, UNIQUE, CHECK, and DEFAULT constraints to enforce data integrity at the database level. Create indexes on foreign key columns, columns used in WHERE clauses, and columns used for sorting or grouping. Consider composite indexes for multi-column query patterns.

5. **Generate SQL DDL scripts:** Produce complete CREATE TABLE statements with all columns, types, constraints, and indexes. Use IF NOT EXISTS for idempotency. Order statements so that referenced tables are created before referencing tables.

6. **Validate and iterate:** Review the schema against the original requirements. Verify that all entities are represented, all relationships are correctly modeled, and no data integrity gaps exist. Adjust based on feedback.

## Supported Technologies

- **Relational databases:** PostgreSQL, MySQL, MariaDB, SQLite, SQL Server, Oracle
- **Schema tools:** dbdiagram.io, pgModeler, MySQL Workbench, DBeaver
- **Migration frameworks:** Flyway, Liquibase, Alembic, Prisma Migrate, Knex

## Usage

Provide a description of your application domain and its data requirements. Include the main entities, their attributes, and how they relate to each other. The agent will produce a normalized schema with full DDL. You can request specific databases (e.g., PostgreSQL vs. MySQL syntax) or ask for schema modifications such as adding audit columns or soft deletes.

## Examples

### Example 1: E-Commerce Application Schema

**Request:** Design a schema for an e-commerce app with users, products, orders, and order items.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    sku VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
    total_amount NUMERIC(12, 2) NOT NULL CHECK (total_amount >= 0),
    shipping_address TEXT NOT NULL,
    ordered_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    UNIQUE (order_id, product_id)
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
```

### Example 2: Adding a Reviews Feature via Schema Migration

**Request:** Add a product reviews table to the existing e-commerce schema. Users can leave one review per product with a rating and optional comment.

```sql
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    rating SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, product_id)
);

CREATE INDEX idx_reviews_product_id ON reviews(product_id);
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
```

This enforces one review per user per product via the UNIQUE constraint, restricts ratings to 1-5, and cascades deletes so removing a user or product also removes their reviews.

## Best Practices

- **Always define foreign keys explicitly** to enforce referential integrity at the database level rather than relying on application code alone.
- **Use CHECK constraints for domain rules** such as positive prices, valid status enums, and rating ranges to prevent invalid data from entering the database.
- **Index all foreign key columns** since they are used in JOINs and lookups; unindexed foreign keys cause full table scans during cascading operations.
- **Prefer surrogate keys over natural keys** for primary keys to avoid issues when natural values change (e.g., email addresses or SKUs).
- **Add created_at and updated_at timestamps** to all tables for auditability and debugging; use database defaults to ensure consistency.
- **Document denormalization decisions** explicitly when you deviate from normal forms for performance, so future developers understand the trade-off.

## Edge Cases

- **Circular foreign key dependencies:** When two tables reference each other, create one table first without the FK, add the second table, then ALTER TABLE to add the missing FK. Use deferred constraints in PostgreSQL to handle circular inserts within transactions.
- **Self-referencing relationships:** For hierarchical data (e.g., categories with subcategories), use a nullable parent_id column that references the same table. Add a CHECK constraint or trigger to prevent a row from being its own parent.
- **Polymorphic associations:** When multiple tables need to reference a shared entity (e.g., comments on both posts and products), prefer separate FK columns with a CHECK constraint ensuring exactly one is non-null, rather than a generic `entity_type` + `entity_id` pattern which cannot enforce referential integrity.
- **Large text or binary data:** Store BLOBs and large text in separate tables linked by FK to keep the main table's row size small and avoid slowing down queries that don't need the large data.
- **Multi-tenant schemas:** Decide between shared tables with a `tenant_id` column (simpler) vs. separate schemas per tenant (stronger isolation). Add tenant_id to all indexes and enforce it via row-level security policies.
