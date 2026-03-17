---
name: Database Designer
description: Database design, schema modeling, and data architecture. USE WHEN user mentions database, schema, tables, columns, relations, SQL, NoSQL, migrations, normalization, ERD, data model, foreign key, or asks about how to structure data.
---

# Database Designer Skill

AI-powered database design guidance for creating efficient, scalable, and maintainable data models with focus on proper normalization, relationship design, and query optimization.

## What This Skill Does

This skill provides expert-level database design guidance including schema modeling, normalization, relationship design, indexing strategies, and migration planning. It combines database theory with practical, production-ready designs.

**Key Capabilities:**
- **Schema Design**: Tables, columns, constraints, types
- **Relationship Modeling**: One-to-one, one-to-many, many-to-many
- **Normalization**: 1NF through BCNF, denormalization trade-offs
- **Indexing Strategy**: Primary, secondary, composite indexes
- **Migration Planning**: Safe schema changes, zero-downtime migrations
- **NoSQL Design**: Document, key-value, graph data modeling

## Core Principles

### The Database Design Mindset
- **Model the Domain**: Schema should reflect business reality
- **Normalize First**: Start normalized, denormalize with data
- **Plan for Queries**: Design for how data will be accessed
- **Think About Scale**: What happens with 10x, 100x data?
- **Migrations Are Inevitable**: Design for change

### Design Quality Metrics
1. **Data Integrity** - Constraints prevent invalid data
2. **Query Performance** - Common queries are efficient
3. **Flexibility** - Schema can evolve
4. **Clarity** - Names and structure are self-documenting
5. **Scalability** - Works at expected data volumes

## Database Design Workflow

### 1. Requirements Gathering
```
Understand the domain:
├── Entities (what objects exist?)
├── Attributes (what properties do they have?)
├── Relationships (how do they connect?)
├── Constraints (what rules must hold?)
└── Access Patterns (how will data be queried?)
```

### 2. Conceptual Design
```
Create high-level model:
├── Entity-Relationship Diagram (ERD)
├── Identify Primary Entities
├── Define Relationships
├── Document Cardinality
└── Note Business Rules
```

### 3. Logical Design
```
Translate to schema:
├── Define Tables
├── Choose Data Types
├── Set Primary Keys
├── Create Foreign Keys
├── Add Constraints
└── Plan Indexes
```

### 4. Physical Design
```
Optimize for implementation:
├── Index Strategy
├── Partitioning (if needed)
├── Storage Considerations
├── Denormalization Decisions
└── Migration Plan
```

## Entity-Relationship Modeling

### ERD Notation
```
┌─────────────────┐         ┌─────────────────┐
│     USERS       │         │     ORDERS      │
├─────────────────┤         ├─────────────────┤
│ PK id           │───┐     │ PK id           │
│    email        │   │     │ FK user_id      │───┐
│    name         │   │     │    total        │   │
│    created_at   │   │     │    status       │   │
└─────────────────┘   │     │    created_at   │   │
                      │     └─────────────────┘   │
                      │                           │
                      │     ┌─────────────────┐   │
                      │     │   ORDER_ITEMS   │   │
                      │     ├─────────────────┤   │
                      │     │ PK id           │   │
                      └────►│ FK order_id     │◄──┘
                            │ FK product_id   │
                            │    quantity     │
                            │    price        │
                            └─────────────────┘
```

### Relationship Types

#### One-to-One (1:1)
```sql
-- User has one profile
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id),  -- UNIQUE enforces 1:1
    bio TEXT,
    avatar_url VARCHAR(500)
);
```

#### One-to-Many (1:N)
```sql
-- User has many orders
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),  -- Many orders per user
    total DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Many-to-Many (M:N)
```sql
-- Products belong to many categories, categories have many products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2)
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Junction/Bridge table
CREATE TABLE product_categories (
    product_id INTEGER REFERENCES products(id),
    category_id INTEGER REFERENCES categories(id),
    PRIMARY KEY (product_id, category_id)  -- Composite PK
);
```

## Normalization Guide

### First Normal Form (1NF)
```sql
-- ✗ WRONG: Repeating groups
CREATE TABLE orders (
    id INT,
    customer_name VARCHAR(100),
    item1 VARCHAR(100), item1_qty INT,
    item2 VARCHAR(100), item2_qty INT,
    item3 VARCHAR(100), item3_qty INT
);

-- ✓ RIGHT: Atomic values, no repeating groups
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    item_name VARCHAR(100),
    quantity INT
);
```

### Second Normal Form (2NF)
```sql
-- ✗ WRONG: Partial dependency on composite key
-- (product_name depends only on product_id, not order_id)
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),  -- Depends only on product_id
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

-- ✓ RIGHT: Remove partial dependencies
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);
```

### Third Normal Form (3NF)
```sql
-- ✗ WRONG: Transitive dependency
-- (city and state depend on zip_code, not directly on user)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    zip_code VARCHAR(10),
    city VARCHAR(100),     -- Depends on zip_code
    state VARCHAR(50)      -- Depends on zip_code
);

-- ✓ RIGHT: Remove transitive dependencies
CREATE TABLE zip_codes (
    code VARCHAR(10) PRIMARY KEY,
    city VARCHAR(100),
    state VARCHAR(50)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    zip_code VARCHAR(10) REFERENCES zip_codes(code)
);
```

### When to Denormalize
```
Consider denormalization when:
├── Read performance is critical
├── Joins are too expensive
├── Data rarely changes
├── Reporting/analytics workloads
└── Caching query results

Common denormalization patterns:
├── Duplicating frequently-accessed columns
├── Pre-computed aggregates
├── Materialized views
└── Summary tables
```

## Data Types Guide

### Choosing the Right Type
| Data | Recommended Type | Avoid |
|------|------------------|-------|
| **IDs** | SERIAL, BIGSERIAL, UUID | VARCHAR |
| **Money** | DECIMAL(10,2), INTEGER (cents) | FLOAT, DOUBLE |
| **Dates** | DATE, TIMESTAMP WITH TIME ZONE | VARCHAR |
| **Booleans** | BOOLEAN | INT, CHAR(1) |
| **Short Text** | VARCHAR(n) with appropriate n | TEXT for short |
| **Long Text** | TEXT | VARCHAR(MAX) |
| **JSON** | JSONB (Postgres), JSON | TEXT |

### Common Patterns
```sql
-- Status as ENUM
CREATE TYPE order_status AS ENUM ('pending', 'paid', 'shipped', 'delivered');
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    status order_status DEFAULT 'pending'
);

-- Money as INTEGER (cents)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    price_cents INTEGER NOT NULL,  -- Store $19.99 as 1999
    currency CHAR(3) DEFAULT 'USD'
);

-- Timestamps with timezone
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- UUID for distributed systems
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER REFERENCES users(id)
);
```

## Constraint Patterns

### Common Constraints
```sql
CREATE TABLE users (
    -- Primary Key
    id SERIAL PRIMARY KEY,
    
    -- Unique constraint
    email VARCHAR(255) UNIQUE NOT NULL,
    
    -- Check constraint
    age INTEGER CHECK (age >= 0 AND age <= 150),
    
    -- Default value
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Not null
    name VARCHAR(100) NOT NULL
);

-- Foreign key with actions
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) 
        ON DELETE CASCADE       -- Delete orders when user deleted
        ON UPDATE CASCADE,      -- Update if user.id changes
    
    -- Or preserve orders
    deleted_user_id INTEGER REFERENCES users(id)
        ON DELETE SET NULL      -- Keep order, null out reference
);

-- Composite unique constraint
CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id),
    role_id INTEGER REFERENCES roles(id),
    UNIQUE (user_id, role_id)  -- User can't have same role twice
);
```

## Index Strategy

### Index Types
```sql
-- B-tree (default, most common)
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- Partial index (filtered)
CREATE INDEX idx_active_users ON users(email) 
WHERE deleted_at IS NULL;

-- Covering index (includes columns)
CREATE INDEX idx_orders_covering ON orders(user_id) 
INCLUDE (total, status);

-- Unique index (also enforces uniqueness)
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- GIN for full-text search
CREATE INDEX idx_posts_search ON posts USING GIN(to_tsvector('english', body));

-- GIN for JSONB
CREATE INDEX idx_metadata ON events USING GIN(metadata);
```

### Index Guidelines
```
DO index:
├── Primary keys (automatic)
├── Foreign keys
├── Columns in WHERE clauses
├── Columns in JOIN conditions
├── Columns in ORDER BY

DON'T over-index:
├── Small tables (< 1000 rows)
├── Columns with low selectivity (boolean, status)
├── Frequently updated columns
├── Wide columns (TEXT, large VARCHAR)
```

## Migration Best Practices

### Safe Schema Changes
```sql
-- ✓ SAFE: Adding nullable column
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- ✓ SAFE: Adding column with default (Postgres 11+)
ALTER TABLE users ADD COLUMN active BOOLEAN DEFAULT true;

-- ✗ DANGEROUS: Adding NOT NULL without default
ALTER TABLE users ADD COLUMN required_field VARCHAR(50) NOT NULL;
-- Fix: Add nullable, backfill, then add constraint

-- ✓ SAFE: Creating index concurrently
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- ✗ DANGEROUS: Regular index locks table
CREATE INDEX idx_users_email ON users(email);
```

### Multi-Step Migrations
```
Renaming a column safely:

Step 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(200);

Step 2: Backfill data
UPDATE users SET full_name = name;

Step 3: Deploy code that writes to both
-- Application writes to both 'name' and 'full_name'

Step 4: Deploy code that reads from new
-- Application reads from 'full_name'

Step 5: Drop old column
ALTER TABLE users DROP COLUMN name;
```

## NoSQL Design Patterns

### Document Database (MongoDB)
```javascript
// Embedded documents (one-to-few)
{
    "_id": "user_123",
    "email": "user@example.com",
    "addresses": [
        { "type": "home", "city": "NYC", "zip": "10001" },
        { "type": "work", "city": "NYC", "zip": "10012" }
    ]
}

// References (one-to-many, many-to-many)
// Users collection
{ "_id": "user_123", "email": "user@example.com" }

// Orders collection
{ 
    "_id": "order_456", 
    "user_id": "user_123",  // Reference
    "items": [
        { "product_id": "prod_789", "quantity": 2 }
    ]
}
```

### Key-Value (Redis)
```
# User session
SET session:abc123 '{"user_id": 456, "expires": 1234567890}'
EXPIRE session:abc123 3600

# Counters
INCR pageviews:homepage:2024-01-15
INCR user:456:login_count

# Leaderboard
ZADD leaderboard 1000 "user:123"
ZADD leaderboard 950 "user:456"
ZREVRANGE leaderboard 0 9  # Top 10
```

### Time-Series Data
```sql
-- Partitioned by time (TimescaleDB, Postgres)
CREATE TABLE metrics (
    time TIMESTAMPTZ NOT NULL,
    device_id INTEGER,
    temperature FLOAT,
    humidity FLOAT
);

-- Create hypertable (TimescaleDB)
SELECT create_hypertable('metrics', 'time');

-- Efficient time-range queries
SELECT device_id, AVG(temperature)
FROM metrics
WHERE time > NOW() - INTERVAL '1 day'
GROUP BY device_id;
```

## When to Use This Skill

**Trigger Phrases:**
- "How should I structure this data?"
- "What tables do I need?"
- "Should I normalize this?"
- "How do I model this relationship?"
- "What indexes should I add?"
- "Help me design a schema for..."
- "Is this the right data type?"
- "How do I migrate this safely?"

**Example Requests:**
1. "Design a database schema for an e-commerce app"
2. "How should I model users and their roles?"
3. "What's the best way to store this many-to-many relationship?"
4. "Should I use UUIDs or auto-increment IDs?"
5. "How do I add a column without downtime?"
6. "Help me normalize these tables"

## Database Design Checklist

Before finalizing a schema:

- [ ] **Normalized?** At least 3NF, denormalize intentionally
- [ ] **Keys defined?** Primary keys on all tables
- [ ] **Foreign keys?** Relationships properly constrained
- [ ] **Indexes planned?** For common query patterns
- [ ] **Types appropriate?** Right sizes, right types
- [ ] **Constraints in place?** NOT NULL, CHECK, UNIQUE
- [ ] **Naming consistent?** snake_case, singular tables
- [ ] **Migration safe?** Can deploy without downtime

## Integration with Other Skills

- **Architect**: Database design follows system architecture
- **Performance Optimizer**: Indexes and queries for performance
- **Documenter**: Schema documentation and data dictionaries
- **Reviewer**: Database changes in code review

---

*Skill designed for Thanos + Antigravity integration*
