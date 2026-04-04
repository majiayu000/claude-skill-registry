---
name: database-schema-design
description: Database schema design for PostgreSQL/MySQL with normalization, relationships, constraints. Use for new databases, schema reviews, migrations, or encountering missing PKs/FKs, wrong data types, premature denormalization, EAV anti-pattern.
license: MIT
metadata:
  keywords: "database schema, schema design, database normalization, 1nf 2nf 3nf, primary key, foreign key, database relationships, one to many, many to many, data types postgresql, constraints check, audit columns, soft delete, database best practices, schema patterns, database anti-patterns, missing primary key, no foreign key, varchar max, denormalization, entity relationship, composite key, uuid vs bigserial, timestamptz"
---

# database-schema-design

Comprehensive database schema design patterns for PostgreSQL and MySQL with normalization, relationships, constraints, and error prevention.

---

## Quick Start (10 Minutes)

**Step 1**: Choose your schema pattern from templates:
```bash
# Basic schema with users, products, orders
cat templates/basic-schema.sql

# Relationship patterns (1:1, 1:M, M:M)
cat templates/relationships.sql

# Constraint examples
cat templates/constraints.sql

# Audit patterns
cat templates/audit-columns.sql
```

**Step 2**: Apply normalization rules (at minimum 3NF):
- **1NF**: No repeating groups, atomic values
- **2NF**: No partial dependencies on composite keys
- **3NF**: No transitive dependencies
- **Load** `references/normalization-guide.md` for detailed examples

**Step 3**: Add essential elements to every table:
```sql
CREATE TABLE your_table (
  -- Primary key (required)
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Business columns with proper types
  name VARCHAR(200) NOT NULL,  -- Use appropriate lengths

  -- Audit columns (always include)
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);
```

---

## Critical Rules

### ✓ Always Do

| Rule | Reason |
|------|--------|
| **Every table has PRIMARY KEY** | Ensures row uniqueness, enables relationships |
| **Foreign keys defined explicitly** | Enforces referential integrity, prevents orphans |
| **Index all foreign keys** | Prevents slow JOINs, critical for performance |
| **NOT NULL on required fields** | Data integrity, prevents NULL pollution |
| **Audit columns (created_at, updated_at)** | Track changes, debugging, compliance |
| **Appropriate data types** | Storage efficiency, validation, indexing |
| **Check constraints for enums** | Enforces valid values at database level |
| **ON DELETE/UPDATE rules specified** | Prevents accidental data loss or orphans |

### ✗ Never Do

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| **VARCHAR(MAX) everywhere** | Wastes space, slows indexes, no validation |
| **Dates as VARCHAR** | No date math, no validation, sorting broken |
| **Missing foreign keys** | No referential integrity, orphaned records |
| **Premature denormalization** | Hard to maintain, data anomalies |
| **EAV (Entity-Attribute-Value)** | Query complexity, no type safety, slow |
| **Polymorphic associations** | No foreign key integrity, complex queries |
| **Circular dependencies** | Impossible to populate, breaks CASCADE |
| **No indexes on foreign keys** | Extremely slow JOINs, performance killer |

---

## Top 7 Critical Errors

### Error 1: Missing Primary Key
**Symptom**: Cannot uniquely identify rows, duplicate data
**Fix**:
```sql
-- ❌ Bad
CREATE TABLE users (
  email VARCHAR(255),
  name VARCHAR(100)
);

-- ✅ Good
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL
);
```

### Error 2: No Foreign Key Constraints
**Symptom**: Orphaned records, data inconsistency
**Fix**:
```sql
-- ❌ Bad
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_id UUID  -- No constraint!
);

-- ✅ Good
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

-- Index the foreign key
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### Error 3: VARCHAR(MAX) Everywhere
**Symptom**: Wasted space, slow indexes, no validation
**Fix**:
```sql
-- ❌ Bad
CREATE TABLE products (
  name VARCHAR(MAX),
  sku VARCHAR(MAX),
  status VARCHAR(MAX)
);

-- ✅ Good
CREATE TABLE products (
  name VARCHAR(200) NOT NULL,
  sku VARCHAR(50) UNIQUE NOT NULL,
  status VARCHAR(20) NOT NULL
    CHECK (status IN ('draft', 'active', 'archived'))
);
```

### Error 4: Wrong Data Types (Dates as Strings)
**Symptom**: No date validation, broken sorting, no date math
**Fix**:
```sql
-- ❌ Bad
CREATE TABLE events (
  event_date VARCHAR(50)  -- '2025-12-15' or 'Dec 15, 2025'?
);

-- ✅ Good
CREATE TABLE events (
  event_date DATE NOT NULL,  -- Validated, sortable
  event_time TIMESTAMPTZ     -- With timezone
);
```

### Error 5: No Indexes on Foreign Keys
**Symptom**: Extremely slow JOINs, poor query performance
**Fix**:
```sql
-- Always index foreign keys
CREATE TABLE order_items (
  order_id UUID NOT NULL REFERENCES orders(id),
  product_id UUID NOT NULL REFERENCES products(id)
);

-- ✅ Required indexes
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
```

### Error 6: Missing Audit Columns
**Symptom**: Cannot track when records created/modified
**Fix**:
```sql
-- ❌ Bad
CREATE TABLE products (
  id UUID PRIMARY KEY,
  name VARCHAR(200)
);

-- ✅ Good
CREATE TABLE products (
  id UUID PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Auto-update trigger (PostgreSQL)
CREATE TRIGGER products_updated_at
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

### Error 7: EAV Anti-Pattern
**Symptom**: Complex queries, no type safety, slow performance
**Fix**:
```sql
-- ❌ Bad (EAV)
CREATE TABLE product_attributes (
  product_id UUID,
  attribute_name VARCHAR(100),  -- 'color', 'size', 'price'
  attribute_value TEXT           -- Everything as text!
);

-- ✅ Good (Structured + JSONB)
CREATE TABLE products (
  id UUID PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  price DECIMAL(10,2) NOT NULL,  -- Required fields as columns
  color VARCHAR(50),              -- Common attributes as columns
  size VARCHAR(20),
  attributes JSONB                -- Optional/dynamic attributes
);

-- Index JSONB
CREATE INDEX idx_products_attributes ON products USING GIN(attributes);
```

**Load** `references/error-catalog.md` for all 12 errors with detailed fixes.

---

## Common Schema Patterns

| Pattern | Use Case | Template |
|---------|----------|----------|
| **Basic CRUD** | Standard users/products/orders | `templates/basic-schema.sql` |
| **One-to-One** | User → Profile | `templates/relationships.sql` (lines 7-17) |
| **One-to-Many** | User → Orders | `templates/relationships.sql` (lines 23-34) |
| **Many-to-Many** | Students ↔ Courses | `templates/relationships.sql` (lines 40-60) |
| **Hierarchical** | Categories tree, org chart | `templates/relationships.sql` (lines 66-83) |
| **Soft Delete** | Mark deleted, keep history | `templates/audit-columns.sql` (lines 55-80) |
| **Versioning** | Track changes over time | `templates/audit-columns.sql` (lines 86-108) |
| **Multi-Tenant** | Isolated data per organization | `references/schema-design-patterns.md` (lines 228-258) |

---

## Normalization Quick Reference

| Form | Rule | Example |
|------|------|---------|
| **1NF** | Atomic values, no repeating groups | `phone1, phone2` → `phones` table |
| **2NF** | 1NF + no partial dependencies | Composite key dependency → separate table |
| **3NF** | 2NF + no transitive dependencies | `user.city` → `city.id` reference |
| **BCNF** | 3NF + every determinant is candidate key | Rare edge cases |
| **4NF** | BCNF + no multi-valued dependencies | Complex many-to-many |
| **5NF** | 4NF + no join dependencies | Very rare, academic |

**Recommendation**: Design to 3NF, denormalize only with measured performance data.

**Load** `references/normalization-guide.md` for detailed examples with before/after.

---

## Configuration Summary

### PostgreSQL Recommended Types

```sql
-- Primary Keys
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
-- OR for performance-critical:
id BIGSERIAL PRIMARY KEY

-- Text
name VARCHAR(200) NOT NULL
description TEXT
code CHAR(10)  -- Fixed-length codes only

-- Numbers
price DECIMAL(10,2) NOT NULL  -- Money: NEVER use FLOAT
quantity INT NOT NULL
rating DECIMAL(3,2)  -- 0.00 to 9.99

-- Dates/Times
created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL  -- With timezone
event_date DATE
duration INTERVAL

-- Boolean
is_active BOOLEAN DEFAULT true NOT NULL

-- JSON
attributes JSONB  -- Binary, faster, indexable

-- Enum Alternative (preferred over ENUM type)
status VARCHAR(20) NOT NULL
  CHECK (status IN ('draft', 'active', 'archived'))
```

### MySQL Differences

```sql
-- MySQL doesn't have:
TIMESTAMPTZ  -- Use TIMESTAMP (stored as UTC)
gen_random_uuid()  -- Use UUID() function
JSONB  -- Use JSON (same performance in 8.0+)

-- MySQL equivalent:
id CHAR(36) PRIMARY KEY DEFAULT (UUID())
-- OR:
id BIGINT AUTO_INCREMENT PRIMARY KEY

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
attributes JSON
```

**Load** `references/data-types-guide.md` for comprehensive type selection guide.

---

## When to Load References

### Schema Design Process
**Load** `references/schema-design-patterns.md` when:
- Starting a new database design
- Need pattern examples (audit columns, soft deletes, versioning)
- Implementing multi-tenancy
- Choosing between UUID vs BIGSERIAL
- Following naming conventions

### Normalization
**Load** `references/normalization-guide.md` when:
- Schema has data duplication
- Unsure what normal form you're in
- Need to normalize existing schema
- Planning database structure

### Relationships
**Load** `references/relationship-patterns.md` when:
- Defining table relationships
- Implementing junction tables
- Creating hierarchical structures
- Setting up cascade rules

### Data Types
**Load** `references/data-types-guide.md` when:
- Choosing column types
- Migrating between PostgreSQL/MySQL
- Optimizing storage
- Implementing JSON fields

### Constraints
**Load** `references/constraints-catalog.md` when:
- Adding validation rules
- Implementing CHECK constraints
- Setting up foreign key cascades
- Creating unique constraints

### Error Prevention
**Load** `references/error-catalog.md` when:
- Schema review needed
- Troubleshooting schema issues
- All 12 documented errors with fixes

---

## Complete Setup Checklist

**Before Creating Tables**:
- [ ] Normalized to at least 3NF
- [ ] All relationships identified
- [ ] Data types chosen appropriately
- [ ] Cascade rules defined

**Every Table Must Have**:
- [ ] Primary key defined
- [ ] Audit columns (created_at, updated_at)
- [ ] NOT NULL on required fields
- [ ] Appropriate VARCHAR lengths (not MAX)
- [ ] CHECK constraints for enums/ranges

**Foreign Keys**:
- [ ] All foreign keys defined with REFERENCES
- [ ] ON DELETE/UPDATE actions specified
- [ ] All foreign keys indexed

**Indexes**:
- [ ] Foreign keys indexed
- [ ] Frequently queried columns indexed
- [ ] Composite indexes for multi-column queries

**Validation**:
- [ ] No circular dependencies
- [ ] No EAV patterns
- [ ] No polymorphic associations
- [ ] Proper data types (no dates as strings)

---

## Production Example

**Before** (Multiple issues):
```sql
CREATE TABLE users (
  email VARCHAR(MAX),           -- Issue: No primary key, VARCHAR(MAX)
  password VARCHAR(MAX),
  created VARCHAR(50)           -- Issue: Date as string
);

CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_email VARCHAR(MAX),      -- Issue: No foreign key
  total VARCHAR(20),            -- Issue: Money as string
  status VARCHAR(MAX)           -- Issue: No validation
);
```

**After** (Production-ready):
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
  status VARCHAR(20) NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'canceled')),
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
```

**Result**: ✅ All constraints enforced, proper types, indexed, auditable

---

## Known Issues Prevention

All 12 documented errors prevented:
1. ✅ Missing primary key → UUID/BIGSERIAL required
2. ✅ No foreign key constraints → REFERENCES required
3. ✅ VARCHAR(MAX) everywhere → Appropriate lengths
4. ✅ Denormalization without justification → 3NF minimum
5. ✅ Missing NOT NULL constraints → Required fields marked
6. ✅ No indexes on foreign keys → All FKs indexed
7. ✅ Wrong data types → Proper type selection
8. ✅ Missing CHECK constraints → Validation rules
9. ✅ No audit columns → created_at/updated_at required
10. ✅ Circular dependencies → Dependency analysis
11. ✅ Missing ON DELETE/UPDATE cascades → Cascade rules
12. ✅ EAV anti-pattern → Structured schema + JSONB

**See**: `references/error-catalog.md` for detailed fixes

---

## Resources

**Templates**:
- `templates/basic-schema.sql` - Users, products, orders starter
- `templates/relationships.sql` - All relationship types
- `templates/constraints.sql` - Constraint examples
- `templates/audit-columns.sql` - Audit patterns + triggers

**References**:
- `references/normalization-guide.md` - 1NF through 5NF detailed
- `references/relationship-patterns.md` - Relationship types
- `references/data-types-guide.md` - PostgreSQL vs MySQL types
- `references/constraints-catalog.md` - All constraints
- `references/schema-design-patterns.md` - Best practices
- `references/error-catalog.md` - All 12 errors documented

**Official Documentation**:
- PostgreSQL Data Types: https://www.postgresql.org/docs/current/datatype.html
- PostgreSQL Constraints: https://www.postgresql.org/docs/current/ddl-constraints.html
- MySQL Data Types: https://dev.mysql.com/doc/refman/8.0/en/data-types.html

---

**Production-tested** | **12 errors prevented** | **MIT License**
