---
name: database-seeding
description: Populate databases with realistic, reproducible test data for development, testing, and staging environments. Use when the user requests database seeding or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: AI Agent Skills Community
  version: 1.0.0
---

# Database Seeding

This skill enables an AI agent to generate and insert realistic test data into databases for development, testing, and staging environments. The agent creates idempotent seed scripts using deterministic generators or faker libraries, handles relational data with proper foreign key ordering, supports environment-specific seed profiles (minimal dev data vs. large-scale load testing), and ensures seeds can be run repeatedly without duplicating data.

## Workflow

1. **Analyze the target schema:** Inspect the database schema to identify all tables, their columns, data types, constraints (NOT NULL, UNIQUE, CHECK, foreign keys), and relationships. Determine the correct insertion order to satisfy foreign key dependencies — parent tables must be seeded before child tables.

2. **Design the seed data strategy:** Choose the appropriate approach based on the use case. Use deterministic data with fixed seeds for reproducible test suites. Use faker-based generation for realistic-looking development data. Use anonymized production snapshots for staging environments that need realistic data distributions. Define the volume of data for each table.

3. **Generate seed scripts:** Write seed scripts in the project's language (Python, JavaScript, SQL, etc.) that create data matching all schema constraints. Use the Faker library or equivalent for realistic names, emails, addresses, and dates. Handle unique constraints by generating unique values or using sequence-based patterns. Wrap inserts in transactions for atomicity.

4. **Ensure idempotency:** Design scripts to be safely re-runnable. Use INSERT ON CONFLICT DO NOTHING, UPSERT patterns, or truncate-then-insert strategies. Check for existing data before inserting to avoid duplicates or constraint violations on repeated runs.

5. **Support environment-specific profiles:** Create different seed profiles — a small dataset (10-50 records per table) for local development, a medium dataset (1,000-10,000 records) for integration testing, and a large dataset (100K+ records) for performance testing. Control the profile via environment variables or command-line arguments.

6. **Execute and verify:** Run the seed script against the target database, verify row counts match expectations, and confirm relational integrity by checking that all foreign keys reference existing rows. Log the seeding results with counts per table.

## Supported Technologies

- **Python:** Faker, Factory Boy, SQLAlchemy, psycopg2
- **JavaScript/TypeScript:** @faker-js/faker, Prisma seed, Knex seed files, TypeORM
- **SQL:** Raw INSERT statements, COPY FROM CSV
- **Ruby:** FactoryBot, Faker gem, Rails db:seed
- **Frameworks:** Django fixtures, Laravel seeders, Rails seeds.rb

## Usage

Provide the database schema (or point to your migration files) and specify the target environment and desired data volume. The agent will generate a complete seed script that respects all constraints and relationships. You can request specific data characteristics (e.g., "include users from multiple time zones" or "create orders spanning the last 12 months").

## Examples

### Example 1: Python Seed Script Using Faker

**Request:** Seed a PostgreSQL database with users, products, and orders for development.

```python
"""seed.py — Seed development database with realistic test data."""
import random
from datetime import datetime, timedelta
from faker import Faker
import psycopg2

fake = Faker()
Faker.seed(42)  # Deterministic output for reproducibility
random.seed(42)

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "dev_db",
    "user": "dev_user",
    "password": "dev_password",
}

NUM_USERS = 50
NUM_PRODUCTS = 30
NUM_ORDERS = 100


def seed():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Seed users
    user_ids = []
    for _ in range(NUM_USERS):
        cur.execute(
            """INSERT INTO users (email, password_hash, full_name, created_at)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (email) DO NOTHING
               RETURNING id""",
            (
                fake.unique.email(),
                fake.sha256(),
                fake.name(),
                fake.date_time_between(start_date="-2y", end_date="now"),
            ),
        )
        row = cur.fetchone()
        if row:
            user_ids.append(row[0])

    # Seed products
    product_ids = []
    for i in range(NUM_PRODUCTS):
        cur.execute(
            """INSERT INTO products (name, description, price, stock_quantity, sku)
               VALUES (%s, %s, %s, %s, %s)
               ON CONFLICT (sku) DO NOTHING
               RETURNING id""",
            (
                fake.catch_phrase(),
                fake.paragraph(nb_sentences=3),
                round(random.uniform(9.99, 499.99), 2),
                random.randint(0, 500),
                f"SKU-{i+1:05d}",
            ),
        )
        row = cur.fetchone()
        if row:
            product_ids.append(row[0])

    # Seed orders with order items
    statuses = ["pending", "confirmed", "shipped", "delivered"]
    for _ in range(NUM_ORDERS):
        user_id = random.choice(user_ids)
        status = random.choice(statuses)
        items = random.sample(product_ids, k=random.randint(1, 5))
        total = 0.0

        cur.execute(
            """INSERT INTO orders (user_id, status, total_amount, shipping_address, ordered_at)
               VALUES (%s, %s, 0, %s, %s) RETURNING id""",
            (user_id, status, fake.address(), fake.date_time_between("-1y", "now")),
        )
        order_id = cur.fetchone()[0]

        for pid in items:
            qty = random.randint(1, 4)
            price = round(random.uniform(9.99, 499.99), 2)
            total += qty * price
            cur.execute(
                """INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                   VALUES (%s, %s, %s, %s)""",
                (order_id, pid, qty, price),
            )

        cur.execute(
            "UPDATE orders SET total_amount = %s WHERE id = %s", (round(total, 2), order_id)
        )

    conn.commit()
    cur.close()
    conn.close()
    print(f"Seeded {len(user_ids)} users, {len(product_ids)} products, {NUM_ORDERS} orders.")


if __name__ == "__main__":
    seed()
```

### Example 2: SQL Seed File with Realistic Test Data

**Request:** Create a plain SQL seed file for a small development dataset.

```sql
-- seed.sql — Idempotent seed data for local development
-- Run with: psql -U dev_user -d dev_db -f seed.sql

BEGIN;

-- Users
INSERT INTO users (id, email, password_hash, full_name, created_at) VALUES
  (1, 'alice@example.com',  'hash_alice',  'Alice Johnson',  '2024-03-15 09:00:00'),
  (2, 'bob@example.com',    'hash_bob',    'Bob Martinez',   '2024-05-20 14:30:00'),
  (3, 'carol@example.com',  'hash_carol',  'Carol Chen',     '2024-07-01 11:15:00'),
  (4, 'dave@example.com',   'hash_dave',   'Dave Okafor',    '2024-09-10 08:45:00'),
  (5, 'eve@example.com',    'hash_eve',    'Eve Andersson',  '2024-11-28 16:00:00')
ON CONFLICT (id) DO NOTHING;

-- Products
INSERT INTO products (id, name, description, price, stock_quantity, sku) VALUES
  (1, 'Wireless Keyboard',   'Bluetooth mechanical keyboard',  79.99,  150, 'SKU-00001'),
  (2, 'USB-C Hub',           '7-in-1 USB-C docking station',   49.99,  300, 'SKU-00002'),
  (3, 'Noise-Cancelling Headphones', 'Over-ear ANC headphones', 199.99, 75, 'SKU-00003'),
  (4, '4K Monitor',          '27-inch IPS 4K display',         399.99,  40, 'SKU-00004'),
  (5, 'Laptop Stand',        'Adjustable aluminum stand',       34.99, 200, 'SKU-00005')
ON CONFLICT (id) DO NOTHING;

-- Orders
INSERT INTO orders (id, user_id, status, total_amount, shipping_address, ordered_at) VALUES
  (1, 1, 'delivered',  129.98, '123 Oak St, Portland, OR 97201',   '2024-12-01 10:00:00'),
  (2, 2, 'shipped',    199.99, '456 Elm Ave, Austin, TX 78701',    '2025-01-05 14:20:00'),
  (3, 3, 'confirmed',  484.98, '789 Pine Rd, Seattle, WA 98101',   '2025-01-10 09:30:00'),
  (4, 1, 'pending',     49.99, '123 Oak St, Portland, OR 97201',   '2025-01-12 16:45:00')
ON CONFLICT (id) DO NOTHING;

-- Order items
INSERT INTO order_items (id, order_id, product_id, quantity, unit_price) VALUES
  (1, 1, 1, 1, 79.99),
  (2, 1, 2, 1, 49.99),
  (3, 2, 3, 1, 199.99),
  (4, 3, 4, 1, 399.99),
  (5, 3, 5, 1, 34.99),
  (6, 4, 2, 1, 49.99)
ON CONFLICT (id) DO NOTHING;

-- Reset sequences to avoid conflicts with future inserts
SELECT setval('users_id_seq',    (SELECT MAX(id) FROM users));
SELECT setval('products_id_seq', (SELECT MAX(id) FROM products));
SELECT setval('orders_id_seq',   (SELECT MAX(id) FROM orders));
SELECT setval('order_items_id_seq', (SELECT MAX(id) FROM order_items));

COMMIT;
```

## Best Practices

- **Set a fixed random seed** (e.g., `Faker.seed(42)`) to produce deterministic data that makes test results reproducible and diffs in seed output meaningful.
- **Always respect foreign key ordering** — insert parent rows before child rows. Map out the dependency graph before writing the script to avoid constraint violations.
- **Use ON CONFLICT DO NOTHING or UPSERT** patterns to make seed scripts idempotent. Running the seed twice should produce the same result, not duplicate data or throw errors.
- **Separate seed profiles by environment** — a small, fast seed for local development, a larger seed for CI integration tests, and an even larger one for load testing. Control via environment variables.
- **Never seed production databases** with test data. Use environment checks (e.g., `assert os.environ["ENV"] != "production"`) at the top of seed scripts as a safety guard.
- **Reset auto-increment sequences** after seeding with explicit IDs to prevent primary key collisions when the application inserts new rows.

## Edge Cases

- **Unique constraint collisions with faker:** Faker does not guarantee uniqueness across large datasets. Use `fake.unique.email()` or append a counter to generated values to avoid duplicates. Reset the unique tracker between test runs with `fake.unique.clear()`.
- **Circular foreign keys:** When table A references table B and table B references table A, insert rows into both tables with nullable FK columns first, then update the FK values in a second pass.
- **Large seed datasets and performance:** For seeding more than 10,000 rows, use bulk insert methods (COPY in PostgreSQL, LOAD DATA INFILE in MySQL) rather than individual INSERT statements. Disable indexes and constraints during bulk load, then re-enable them afterward.
- **Time-dependent test data:** If your application logic depends on dates (e.g., "orders from the last 30 days"), generate dates relative to the current date rather than hardcoded dates that will become stale.
- **Seeding binary or file data:** For tables that reference uploaded files or images, seed with placeholder file paths or small base64-encoded test images rather than attempting to generate full binary content.
