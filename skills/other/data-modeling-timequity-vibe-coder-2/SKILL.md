---
name: data-modeling
description: Dimensional modeling, normalization, and schema design for analytics.
---

# Data Modeling

## Dimensional Modeling

### Star Schema

```
        ┌─────────────┐
        │ dim_date    │
        └──────┬──────┘
               │
┌──────────┐   │   ┌──────────────┐
│dim_store │───┼───│  fct_sales   │
└──────────┘   │   └──────────────┘
               │
        ┌──────┴──────┐
        │dim_product  │
        └─────────────┘
```

### Fact Tables

```sql
CREATE TABLE fct_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    store_key INT REFERENCES dim_store(store_key),
    product_key INT REFERENCES dim_product(product_key),
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Dimension Tables

```sql
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),  -- Natural key
    name VARCHAR(255),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    -- SCD Type 2 fields
    valid_from DATE,
    valid_to DATE,
    is_current BOOLEAN
);
```

## SCD Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Type 1** | Overwrite | Corrections |
| **Type 2** | New row + versioning | Track history |
| **Type 3** | Previous value column | Limited history |

## Normalization

| Form | Rule |
|------|------|
| **1NF** | Atomic values, no repeating groups |
| **2NF** | 1NF + no partial dependencies |
| **3NF** | 2NF + no transitive dependencies |

## Naming Conventions

- `dim_` prefix for dimensions
- `fct_` prefix for facts
- `stg_` prefix for staging
- `int_` prefix for intermediate
- Snake_case for columns
