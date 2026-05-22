---
name: database-schema-architect
description: Expert guidance for designing, optimizing, and maintaining database schemas for SQL and NoSQL systems. Use when creating new databases, optimizing existing schemas, planning migrations, implementing security policies, or ensuring GDPR compliance. Covers normalization, indexing, data types, relationships, performance optimization, and audit logging.
license: Apache-2.0
---

# Database Schema Architect

## Overview
This skill provides comprehensive guidance for database schema design, from initial planning through production deployment and ongoing maintenance. It covers both relational (SQL) and NoSQL databases with focus on scalability, performance, security, and compliance.

## Core Design Principles

### 1. Start with Requirements Analysis
Before designing any schema:
- Identify primary use cases and query patterns
- Determine read/write ratio (OLTP vs OLAP)
- Establish data volume projections (current and 2-5 year growth)
- Define compliance requirements (GDPR, HIPAA, SOC2, etc.)
- List critical performance requirements (response times, throughput)

### 2. Naming Conventions (Critical for Maintainability)

**Tables**: Plural nouns in lowercase
- ✅ `customers`, `orders`, `order_items`
- ❌ `Customer`, `order`, `OrderItem`

**Columns**: Singular nouns, descriptive
- ✅ `customer_id`, `email_address`, `created_at`
- ❌ `custId`, `e_mail`, `date`

**Primary Keys**: `table_name_id` format
- ✅ `customer_id`, `order_id`
- Use SERIAL/AUTO_INCREMENT for SQL
- Use UUID for distributed systems

**Foreign Keys**: Reference the table they point to
- ✅ `customer_id`, `product_id`
- Always index foreign key columns

**Indexes**: Prefix with `idx_` followed by table and columns
- ✅ `idx_orders_customer_id`, `idx_products_category_status`

**Constraints**: Descriptive of their purpose
- ✅ `fk_orders_customer_id`, `ck_price_positive`, `uq_users_email`

### 3. Normalization Strategy

**Start with Third Normal Form (3NF)**:
- 1NF: Atomic values (no arrays, sets, or repeating groups)
- 2NF: All non-key attributes fully depend on primary key
- 3NF: No transitive dependencies (non-key attributes don't depend on other non-key attributes)

**When to Denormalize**:
- High read frequency with stable data (lookup tables)
- Performance-critical queries with complex joins
- Reporting/analytics workloads (consider separate reporting DB)
- Document frequently accessed together (NoSQL)

**Use scripts/normalization_checker.py to validate normalization level**

## Step-by-Step Schema Design Workflow

### Phase 1: Entity Identification
1. List all business entities (nouns from requirements)
2. Identify entity attributes
3. Determine relationships (one-to-one, one-to-many, many-to-many)
4. Create initial Entity-Relationship Diagram (ERD)

### Phase 2: Table Design
1. Convert entities to tables
2. Define primary keys (prefer surrogate keys for most tables)
3. Add foreign keys for relationships
4. Apply normalization rules (aim for 3NF initially)

**Example - E-commerce Schema**:
```sql
-- Normalized approach
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_customers_email UNIQUE (email)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    inventory_count INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_products_category FOREIGN KEY (category_id) 
        REFERENCES categories(category_id),
    CONSTRAINT ck_products_price_positive CHECK (price >= 0),
    CONSTRAINT ck_products_inventory_non_negative CHECK (inventory_count >= 0)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    subtotal DECIMAL(10, 2) NOT NULL,
    tax_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    total_amount DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id),
    CONSTRAINT ck_orders_amounts_positive CHECK (
        subtotal >= 0 AND 
        tax_amount >= 0 AND 
        total_amount >= 0
    )
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) 
        REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_order_items_product FOREIGN KEY (product_id) 
        REFERENCES products(product_id),
    CONSTRAINT ck_order_items_quantity_positive CHECK (quantity > 0),
    CONSTRAINT ck_order_items_price_positive CHECK (price_at_purchase >= 0)
);
```

### Phase 3: Data Type Selection

**Use scripts/datatype_optimizer.py to analyze and recommend optimal types**

**Key Principles**:
- Use smallest appropriate data type
- Prefer fixed-length types when size is known
- Use NOT NULL when appropriate (improves performance)
- Avoid TEXT/BLOB unless necessary (use VARCHAR with reasonable limit)

**Common Patterns**:
- IDs: INTEGER/BIGINT (or UUID for distributed systems)
- Booleans: Use BOOLEAN/BIT (not INTEGER)
- Money: DECIMAL(10,2) or DECIMAL(19,4) (NEVER use FLOAT for money)
- Dates: Use DATE for date-only, TIMESTAMP for datetime
- Email: VARCHAR(255)
- Phone: VARCHAR(20) (store with country code)
- Names: VARCHAR(100) for most cases
- Descriptions: TEXT only if exceeding 500 chars regularly

**See references/DATA_TYPES_REFERENCE.md for comprehensive guide**

### Phase 4: Index Strategy

**Critical Rule**: Index foreign keys ALWAYS
**Secondary Rule**: Index columns used in WHERE, JOIN, ORDER BY

**Types of Indexes**:
- **Primary Index**: Automatically created with PRIMARY KEY
- **Unique Index**: For UNIQUE constraints
- **Composite Index**: Multiple columns (order matters!)
- **Covering Index**: Includes all columns for a query
- **Partial Index**: Filtered index (PostgreSQL)

**Create indexes for**:
```sql
-- Foreign keys (CRITICAL)
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Frequent WHERE clauses
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_is_active ON products(is_active) WHERE is_active = TRUE; -- Partial index

-- Composite indexes for common query patterns
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);
CREATE INDEX idx_products_category_active ON products(category_id, is_active) WHERE is_active = TRUE;

-- Covering index for specific query
CREATE INDEX idx_products_search ON products(category_id, is_active) 
    INCLUDE (name, price); -- PostgreSQL 11+
```

**Index Trade-offs**:
- ✅ Dramatically faster reads
- ❌ Slower writes (INSERT, UPDATE, DELETE)
- ❌ Additional storage overhead
- Rule: Don't over-index. Target 3-5 indexes per table maximum

**Use scripts/index_analyzer.py to analyze existing queries and suggest optimal indexes**

### Phase 5: Constraints and Data Integrity

**Always Define**:
1. **Primary Keys**: Every table needs one
2. **Foreign Keys**: Maintain referential integrity
3. **NOT NULL**: For required fields
4. **UNIQUE**: For naturally unique data (email, SKU, etc.)
5. **CHECK**: For business rule validation

**Example Constraints**:
```sql
-- Price validation
CONSTRAINT ck_price_positive CHECK (price >= 0)

-- Status validation (enum-like behavior)
CONSTRAINT ck_order_status CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled'))

-- Date logic validation
CONSTRAINT ck_dates_logical CHECK (end_date >= start_date)

-- Conditional constraints
CONSTRAINT ck_discount_valid CHECK (
    (discount_type = 'percentage' AND discount_value BETWEEN 0 AND 100) OR
    (discount_type = 'fixed' AND discount_value >= 0)
)
```

## Security and Compliance

### Row-Level Security (RLS) - PostgreSQL

**Enable for multi-tenant applications**:
```sql
-- Enable RLS on table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Create policy for users to see only their orders
CREATE POLICY orders_user_policy ON orders
    FOR SELECT
    USING (customer_id = current_setting('app.current_user_id')::INTEGER);

-- Policy for admins to see all
CREATE POLICY orders_admin_policy ON orders
    FOR ALL
    USING (current_setting('app.user_role') = 'admin');
```

**See references/SECURITY_BEST_PRACTICES.md for comprehensive RLS patterns**

### Audit Logging

**Standard Audit Log Table**:
```sql
CREATE TABLE audit_logs (
    audit_id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL, -- INSERT, UPDATE, DELETE
    user_id INTEGER NOT NULL,
    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT
);

CREATE INDEX idx_audit_logs_table_record ON audit_logs(table_name, record_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_changed_at ON audit_logs(changed_at);
```

**Implement via triggers or application-level logging**
**See assets/audit_log_setup.sql for trigger-based implementation**

### GDPR Compliance Patterns

1. **Data Retention Policies**:
```sql
-- Add deleted_at column for soft deletes
ALTER TABLE customers ADD COLUMN deleted_at TIMESTAMP;

-- Create retention policy (example: 7 years)
CREATE INDEX idx_customers_deleted_at ON customers(deleted_at) WHERE deleted_at IS NOT NULL;
```

2. **Right to be Forgotten**:
```sql
-- Anonymization function
CREATE OR REPLACE FUNCTION anonymize_customer(cust_id INTEGER)
RETURNS VOID AS $$
BEGIN
    UPDATE customers 
    SET 
        email = 'deleted_' || customer_id || '@anonymized.com',
        first_name = 'DELETED',
        last_name = 'DELETED',
        phone = NULL,
        deleted_at = CURRENT_TIMESTAMP
    WHERE customer_id = cust_id;
END;
$$ LANGUAGE plpgsql;
```

3. **Consent Tracking**:
```sql
CREATE TABLE user_consents (
    consent_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    consent_type VARCHAR(50) NOT NULL, -- marketing, analytics, etc.
    consented BOOLEAN NOT NULL,
    consented_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    CONSTRAINT uq_user_consent UNIQUE (user_id, consent_type)
);
```

**See references/GDPR_COMPLIANCE.md for complete patterns**

## Migration Management

### Migration Workflow
1. Design schema changes
2. Generate migration scripts using scripts/migration_generator.py
3. Test in development environment
4. Create rollback script
5. Apply to staging
6. Verify data integrity
7. Deploy to production with monitoring

**Migration Script Template** (see assets/migration_template.sql):
```sql
-- Migration: [DESCRIPTION]
-- Date: YYYY-MM-DD
-- Author: [NAME]

BEGIN;

-- Forward migration
-- Add your DDL statements here

-- Verify data integrity
DO $$
BEGIN
    -- Add verification queries
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'new_table') THEN
        RAISE EXCEPTION 'Migration verification failed';
    END IF;
END $$;

COMMIT;
```

**Rollback Script Template**:
```sql
-- Rollback for: [MIGRATION_NAME]

BEGIN;

-- Reverse operations in reverse order
-- DROP statements, ALTER TABLE drops, etc.

COMMIT;
```

### Common Migration Patterns

**Adding Columns (Safe)**:
```sql
-- Add column with default (can lock table on large tables)
ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(100);

-- For large tables, add without default first
ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(100);
-- Then update in batches
UPDATE orders SET tracking_number = generate_tracking_number() WHERE tracking_number IS NULL;
```

**Renaming Columns**:
```sql
-- Rename column
ALTER TABLE customers RENAME COLUMN phone TO phone_number;

-- Update dependent views and functions
```

**Changing Data Types**:
```sql
-- Safe: Expanding VARCHAR
ALTER TABLE customers ALTER COLUMN phone TYPE VARCHAR(30);

-- Risky: Reducing size (requires validation)
-- First check if data fits
SELECT MAX(LENGTH(phone)) FROM customers; -- Must be ≤ new size

-- Then alter
ALTER TABLE customers ALTER COLUMN phone TYPE VARCHAR(15);
```

**Adding Indexes (Non-Blocking in PostgreSQL)**:
```sql
-- Use CONCURRENTLY to avoid locking
CREATE INDEX CONCURRENTLY idx_orders_created_at ON orders(created_at);
```

## NoSQL Schema Design

### MongoDB Patterns

**Embed vs Reference**:
```javascript
// Embed when data is accessed together
{
    _id: ObjectId("..."),
    customer: {
        name: "John Doe",
        email: "john@example.com"
    },
    items: [
        { product: "Widget", quantity: 2, price: 19.99 },
        { product: "Gadget", quantity: 1, price: 29.99 }
    ],
    total: 69.97
}

// Reference when data is large or frequently updated independently
{
    _id: ObjectId("..."),
    customer_id: ObjectId("..."), // Reference to customers collection
    product_ids: [ObjectId("..."), ObjectId("...")], // References
    status: "shipped"
}
```

**Indexing in MongoDB**:
```javascript
// Single field index
db.customers.createIndex({ email: 1 });

// Compound index
db.orders.createIndex({ customer_id: 1, status: 1, created_at: -1 });

// Text index for full-text search
db.products.createIndex({ name: "text", description: "text" });

// Unique index
db.users.createIndex({ email: 1 }, { unique: true });
```

## Performance Optimization

### Query Analysis Workflow
1. Identify slow queries using database logs
2. Use EXPLAIN ANALYZE to understand execution plan
3. Check if indexes are being used
4. Analyze query patterns
5. Add appropriate indexes or rewrite query
6. Test performance improvement
7. Monitor in production

**Use scripts/query_analyzer.py to automate analysis**

### Common Performance Patterns

**Avoid N+1 Queries**:
```sql
-- Bad: Separate queries in loop
SELECT * FROM customers WHERE customer_id = ?; -- Called N times

-- Good: Single query with JOIN
SELECT c.*, o.order_id, o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

**Use Appropriate JOIN Types**:
- INNER JOIN: Only matching rows
- LEFT JOIN: All from left, matching from right
- RIGHT JOIN: Rare, usually rewrite as LEFT JOIN
- FULL OUTER JOIN: Rare in most applications

**Pagination**:
```sql
-- Basic pagination (works well for small offsets)
SELECT * FROM products ORDER BY product_id LIMIT 20 OFFSET 40;

-- Keyset pagination (better for large offsets)
SELECT * FROM products 
WHERE product_id > 1000 
ORDER BY product_id 
LIMIT 20;
```

**Partial Indexes for Boolean Columns**:
```sql
-- Index only TRUE values (if most are FALSE)
CREATE INDEX idx_products_active ON products(is_active) WHERE is_active = TRUE;
```

## Validation and Testing

### Pre-Deployment Checklist
- [ ] All tables have primary keys
- [ ] All foreign keys are indexed
- [ ] Naming conventions followed consistently
- [ ] Appropriate data types selected
- [ ] NOT NULL constraints on required fields
- [ ] CHECK constraints for business rules
- [ ] Audit logging implemented for sensitive tables
- [ ] Migration scripts tested with rollback
- [ ] EXPLAIN ANALYZE run on critical queries
- [ ] Backup and restore procedure tested

**Use scripts/schema_validator.py to automate validation**

### Load Testing
1. Generate realistic test data
2. Run representative query load
3. Monitor database metrics:
   - Query response times
   - CPU and memory usage
   - Disk I/O
   - Connection pool utilization
4. Identify bottlenecks
5. Optimize and retest

## Tools and Scripts

This skill includes several helper scripts in the scripts/ directory:

- **schema_validator.py**: Validates schema against best practices
- **migration_generator.py**: Generates migration scripts from schema changes
- **index_analyzer.py**: Analyzes queries and suggests optimal indexes
- **normalization_checker.py**: Checks normalization level and suggests improvements
- **datatype_optimizer.py**: Reviews data types and suggests optimizations
- **query_analyzer.py**: Analyzes slow queries and provides recommendations

**Usage**: Run scripts with `python scripts/[script_name].py [arguments]`

## Additional Resources

For detailed information, see:
- **references/NORMALIZATION_GUIDE.md**: Complete normalization forms and examples
- **references/DATA_TYPES_REFERENCE.md**: Comprehensive data type selection guide
- **references/SECURITY_BEST_PRACTICES.md**: RLS, encryption, and security patterns
- **references/GDPR_COMPLIANCE.md**: Complete GDPR compliance implementation
- **references/QUERY_OPTIMIZATION.md**: Advanced query optimization techniques
- **assets/migration_template.sql**: Standard migration script template
- **assets/audit_log_setup.sql**: Complete audit logging implementation

## Best Practices Summary

1. **Start Normalized**: Begin with 3NF, denormalize only when necessary
2. **Name Consistently**: Follow naming conventions throughout
3. **Index Strategically**: Focus on foreign keys and frequent WHERE/JOIN columns
4. **Constrain Appropriately**: Use constraints to enforce data integrity
5. **Plan for Scale**: Consider future growth in initial design
6. **Document Decisions**: Record why certain design choices were made
7. **Test Thoroughly**: Validate schema changes before production deployment
8. **Monitor Performance**: Regularly analyze query performance and optimize
9. **Implement Security**: RLS, audit logs, and encryption from the start
10. **Stay Compliant**: Build in GDPR and other compliance requirements early

## Example: Complete Workflow

**User Request**: "Design a database schema for a SaaS project management application"

**Response**:
1. Gather requirements and identify entities
2. Create initial ERD with tables: users, organizations, projects, tasks, comments
3. Design tables with proper normalization
4. Add indexes for common queries
5. Implement RLS for multi-tenant security
6. Set up audit logging for compliance
7. Create migration scripts
8. Validate schema with scripts/schema_validator.py
9. Generate documentation

**This skill guides you through each step with specific examples and validation tools.**
