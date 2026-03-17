---
name: ELT Modeling
description: Comprehensive guide to ELT (Extract, Load, Transform) modeling patterns, dimensional modeling, fact and dimension tables, and data warehouse design
---

# ELT Modeling

## ELT vs ETL

### ETL (Traditional)
```
Extract → Transform → Load

1. Extract from source
2. Transform in ETL tool (Informatica, Talend)
3. Load to warehouse

Pros: Clean data before loading
Cons: Slow, expensive transformation servers
```

### ELT (Modern)
```
Extract → Load → Transform

1. Extract from source
2. Load raw data to warehouse
3. Transform in warehouse (SQL, dbt)

Pros: Fast loading, leverage warehouse power
Cons: Raw data in warehouse (need governance)
```

### Why ELT?
- **Cloud warehouses:** Snowflake, BigQuery, Redshift (powerful, scalable)
- **Separation of concerns:** EL (Fivetran, Airbyte) + T (dbt)
- **Flexibility:** Transform multiple ways from same raw data
- **Speed:** Parallel processing in warehouse

---

## Dimensional Modeling

### Star Schema
```
        dim_customers
              |
        dim_products
              |
         fct_orders  ← Central fact table
              |
        dim_dates
              |
        dim_locations
```

**Characteristics:**
- One fact table (center)
- Multiple dimension tables (points)
- Denormalized (fast queries)

### Snowflake Schema
```
    dim_customers
          |
    dim_customer_segments
          |
     fct_orders
          |
    dim_products
          |
    dim_product_categories
```

**Characteristics:**
- Normalized dimensions
- Less redundancy
- More joins (slower queries)

**Recommendation:** Use star schema for analytics (faster)

---

## Fact Tables

### Definition
**Fact table:** Stores measurable events (transactions, orders, clicks)

### Characteristics
- **Large:** Millions to billions of rows
- **Numeric measures:** Amounts, quantities, counts
- **Foreign keys:** Links to dimensions
- **Grain:** Level of detail (one row per order, per day, etc.)

### Types of Facts

**Transaction Facts:**
```sql
-- One row per transaction
fct_orders:
  order_id (PK)
  customer_id (FK)
  product_id (FK)
  order_date_id (FK)
  quantity
  amount
```

**Periodic Snapshot Facts:**
```sql
-- One row per period (daily, monthly)
fct_inventory_daily:
  date_id (PK)
  product_id (PK)
  warehouse_id (PK)
  quantity_on_hand
  quantity_sold
```

**Accumulating Snapshot Facts:**
```sql
-- One row per process (order lifecycle)
fct_order_lifecycle:
  order_id (PK)
  order_date
  payment_date
  shipment_date
  delivery_date
  days_to_ship
  days_to_deliver
```

### Fact Table Design
```sql
CREATE TABLE fct_orders (
  -- Surrogate key
  order_key BIGINT PRIMARY KEY,
  
  -- Natural key
  order_id VARCHAR(50) NOT NULL,
  
  -- Foreign keys (dimensions)
  customer_key BIGINT NOT NULL,
  product_key BIGINT NOT NULL,
  date_key INT NOT NULL,
  
  -- Degenerate dimensions (no separate dim table)
  order_number VARCHAR(50),
  
  -- Measures
  quantity INT,
  unit_price DECIMAL(10,2),
  total_amount DECIMAL(10,2),
  discount_amount DECIMAL(10,2),
  
  -- Audit columns
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

---

## Dimension Tables

### Definition
**Dimension table:** Stores descriptive attributes (who, what, where, when)

### Characteristics
- **Small:** Thousands to millions of rows
- **Descriptive:** Text, categories, hierarchies
- **Slowly changing:** Updates over time (SCD)

### Dimension Design
```sql
CREATE TABLE dim_customers (
  -- Surrogate key
  customer_key BIGINT PRIMARY KEY,
  
  -- Natural key
  customer_id VARCHAR(50) NOT NULL,
  
  -- Attributes
  customer_name VARCHAR(255),
  email VARCHAR(255),
  phone VARCHAR(50),
  
  -- Hierarchies
  city VARCHAR(100),
  state VARCHAR(100),
  country VARCHAR(100),
  region VARCHAR(100),
  
  -- Segments
  customer_segment VARCHAR(50),
  customer_tier VARCHAR(50),
  
  -- SCD Type 2 columns
  effective_date DATE,
  expiration_date DATE,
  is_current BOOLEAN,
  
  -- Audit columns
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Slowly Changing Dimensions (SCD)

**Type 1: Overwrite**
```sql
-- Customer moves, update address
UPDATE dim_customers
SET city = 'New York', state = 'NY'
WHERE customer_id = '123';

-- No history preserved
```

**Type 2: Add New Row (Historical)**
```sql
-- Customer moves, add new row
INSERT INTO dim_customers (
  customer_id, city, state,
  effective_date, is_current
) VALUES (
  '123', 'New York', 'NY',
  '2024-01-15', TRUE
);

-- Mark old row as not current
UPDATE dim_customers
SET is_current = FALSE,
    expiration_date = '2024-01-14'
WHERE customer_id = '123'
  AND is_current = TRUE;

-- History preserved
```

**Type 3: Add New Column**
```sql
-- Track previous value
ALTER TABLE dim_customers
ADD COLUMN previous_city VARCHAR(100);

UPDATE dim_customers
SET previous_city = city,
    city = 'New York'
WHERE customer_id = '123';
```

---

## Grain Definition

### What is Grain?
**Grain:** Level of detail in fact table (one row represents what?)

### Examples
```
Order grain:      One row per order
Order line grain: One row per product in order
Daily grain:      One row per day per product
Hourly grain:     One row per hour per product
```

### Choosing Grain
```
Too fine (order line):
- More rows
- More storage
- More flexibility

Too coarse (monthly):
- Fewer rows
- Less storage
- Less flexibility

Balance: Choose finest grain needed for analysis
```

---

## Kimball vs Inmon

### Kimball (Bottom-Up, Dimensional)
```
Data Marts (Star Schemas) → Enterprise Data Warehouse

Pros:
- Fast to implement
- Business-friendly (denormalized)
- Query performance

Cons:
- Data redundancy
- Hard to change
```

### Inmon (Top-Down, Normalized)
```
Enterprise Data Warehouse (3NF) → Data Marts

Pros:
- Single source of truth
- Flexible
- Less redundancy

Cons:
- Slow to implement
- Complex queries (many joins)
```

**Modern Approach:** Hybrid (normalized staging, dimensional marts)

---

## Data Vault

### Components
```
Hubs:       Business keys (customers, products)
Links:      Relationships (orders link customers + products)
Satellites: Descriptive attributes (customer details)
```

### Example
```sql
-- Hub: Customer
CREATE TABLE hub_customer (
  customer_hub_key BIGINT PRIMARY KEY,
  customer_id VARCHAR(50) UNIQUE,
  load_date TIMESTAMP,
  record_source VARCHAR(50)
);

-- Satellite: Customer Details
CREATE TABLE sat_customer_details (
  customer_hub_key BIGINT,
  load_date TIMESTAMP,
  customer_name VARCHAR(255),
  email VARCHAR(255),
  phone VARCHAR(50),
  PRIMARY KEY (customer_hub_key, load_date)
);

-- Link: Order
CREATE TABLE link_order (
  order_link_key BIGINT PRIMARY KEY,
  customer_hub_key BIGINT,
  product_hub_key BIGINT,
  load_date TIMESTAMP
);
```

**Pros:**
- Audit trail
- Flexible
- Handles source changes

**Cons:**
- Complex
- Many joins
- Steep learning curve

---

## Conformed Dimensions

### Definition
**Conformed dimension:** Shared across multiple fact tables

### Example
```sql
-- dim_date used by multiple facts
dim_date ← fct_orders
        ← fct_shipments
        ← fct_returns

-- Ensures consistent date attributes
```

### Benefits
- **Consistency:** Same date logic everywhere
- **Drill-across:** Compare metrics across facts
- **Reusability:** Build once, use many times

---

## Bridge Tables

### Many-to-Many Relationships
```sql
-- Customer can have multiple accounts
-- Account can have multiple customers

CREATE TABLE bridge_customer_account (
  customer_key BIGINT,
  account_key BIGINT,
  allocation_percentage DECIMAL(5,2),
  PRIMARY KEY (customer_key, account_key)
);
```

---

## Junk Dimensions

### Definition
**Junk dimension:** Collection of low-cardinality flags

### Example
```sql
-- Instead of many boolean columns in fact
CREATE TABLE dim_order_flags (
  order_flag_key INT PRIMARY KEY,
  is_gift BOOLEAN,
  is_express_shipping BOOLEAN,
  is_first_order BOOLEAN,
  has_discount BOOLEAN
);

-- Fact table references junk dimension
fct_orders:
  order_key
  customer_key
  order_flag_key  ← Reference to junk dimension
  amount
```

---

## Role-Playing Dimensions

### Definition
**Role-playing dimension:** Same dimension used multiple times with different meanings

### Example
```sql
-- dim_date used multiple times
fct_orders:
  order_key
  order_date_key      ← dim_date (order date)
  ship_date_key       ← dim_date (ship date)
  delivery_date_key   ← dim_date (delivery date)
  amount
```

---

## Surrogate Keys

### Natural Key vs Surrogate Key
```sql
-- Natural key: Business identifier
customer_id = 'CUST-12345'

-- Surrogate key: System-generated
customer_key = 1001 (auto-increment or hash)
```

### Why Surrogate Keys?
- **Performance:** Integer joins faster than string joins
- **SCD Type 2:** Multiple rows for same natural key
- **Independence:** Source system can change natural key
- **Consistency:** Same format across all tables

### Generating Surrogate Keys
```sql
-- Auto-increment
customer_key BIGINT AUTO_INCREMENT PRIMARY KEY

-- Hash (dbt)
{{ dbt_utils.surrogate_key(['customer_id', 'effective_date']) }}

-- Sequence (PostgreSQL)
customer_key BIGINT DEFAULT nextval('customer_key_seq')
```

---

## Data Warehouse Layers

### Bronze (Raw)
```
Purpose: Exact copy of source data
Format: As-is from source
Schema: Source schema
Example: raw_salesforce_accounts
```

### Silver (Cleaned)
```
Purpose: Cleaned, standardized
Format: Consistent types, naming
Schema: Staging schema
Example: stg_salesforce_accounts
```

### Gold (Analytics)
```
Purpose: Business-ready
Format: Dimensional models
Schema: Analytics schema
Example: dim_customers, fct_orders
```

---

## Best Practices

### 1. Define Grain Clearly
```
✓ "One row per order"
✗ "Order data"
```

### 2. Use Surrogate Keys
```
✓ customer_key BIGINT
✗ customer_id VARCHAR(50)
```

### 3. Denormalize Dimensions
```
✓ dim_customers includes city, state, country
✗ Separate dim_cities, dim_states, dim_countries
```

### 4. Keep Facts Narrow
```
✓ fct_orders: Keys + measures only
✗ fct_orders: Keys + measures + customer name, product name
```

### 5. Use Conformed Dimensions
```
✓ dim_date shared across all facts
✗ Each fact has own date dimension
```

---

## Common Patterns

### Daily Snapshot
```sql
-- Capture state once per day
INSERT INTO fct_inventory_daily
SELECT
  CURRENT_DATE as snapshot_date,
  product_id,
  warehouse_id,
  quantity_on_hand,
  quantity_reserved
FROM current_inventory;
```

### Cumulative Metrics
```sql
-- Running totals
SELECT
  order_date,
  SUM(amount) OVER (
    ORDER BY order_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) as cumulative_revenue
FROM fct_orders;
```

---

## Summary

**ELT:** Extract → Load → Transform (modern approach)

**Dimensional Modeling:**
- Star schema (recommended)
- Fact tables (measures)
- Dimension tables (attributes)

**Fact Types:**
- Transaction (one per event)
- Periodic snapshot (one per period)
- Accumulating snapshot (one per process)

**SCD Types:**
- Type 1: Overwrite
- Type 2: Historical (recommended)
- Type 3: Previous value

**Grain:** Level of detail (define clearly!)

**Surrogate Keys:** Use for performance and SCD

**Layers:**
- Bronze: Raw
- Silver: Cleaned
- Gold: Analytics-ready

**Best Practices:**
- Define grain
- Use surrogate keys
- Denormalize dimensions
- Keep facts narrow
- Use conformed dimensions
