---
name: spring-boot-database-migrations
description: Guide for creating and managing Flyway database migrations. Use this when adding new tables, columns, or modifying database schema.
---

# Database Migrations with Flyway

Follow these practices when making database schema changes.

## Migration File Location

```
src/main/resources/db/migration/
├── V1__Initial_schema.sql
├── V2__Add_customers_table.sql
├── V3__Add_appointments_table.sql
├── V4__Add_employee_columns.sql
└── V[N]__description.sql
```

## Naming Convention

**REQUIRED FORMAT**: `V[version]__[description].sql`

- Version: Sequential integer (V1, V2, V3, ...)
- Description: Snake_case describing the change
- Double underscore between version and description

**Examples:**
```
V1__Initial_schema.sql
V2__Create_customers_table.sql
V3__Add_email_to_customers.sql
V4__Create_appointments_table.sql
V5__Add_foreign_keys.sql
V6__Add_guest_column_to_customers.sql
```

## Creating New Migrations

### For New Tables

```sql
-- V[N]__Create_service_types_table.sql
CREATE TABLE service_types (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    duration_minutes INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add index for commonly queried columns
CREATE INDEX idx_service_types_active ON service_types(active);
```

### For Adding Columns

```sql
-- V[N]__Add_guest_column_to_customers.sql
ALTER TABLE customers 
ADD COLUMN guest BOOLEAN DEFAULT FALSE NOT NULL;

-- For nullable columns
ALTER TABLE customers 
ALTER COLUMN email DROP NOT NULL;
```

### For Adding Foreign Keys

```sql
-- V[N]__Add_foreign_keys_to_appointments.sql
ALTER TABLE appointments 
ADD CONSTRAINT fk_appointments_customer 
FOREIGN KEY (customer_id) REFERENCES customers(id);

ALTER TABLE appointments 
ADD CONSTRAINT fk_appointments_employee 
FOREIGN KEY (employee_id) REFERENCES employees(id);
```

## PostgreSQL vs H2 Compatibility

For development with H2 and production with PostgreSQL, use compatible syntax:

```sql
-- Use BIGSERIAL for PostgreSQL auto-increment
CREATE TABLE customers (
    id BIGSERIAL PRIMARY KEY,  -- PostgreSQL
    -- id BIGINT AUTO_INCREMENT PRIMARY KEY,  -- H2 only
    name VARCHAR(255) NOT NULL
);

-- For H2 compatibility, use application-h2.yml with ddl-auto
```

## Migration Rules

1. **NEVER modify applied migrations** - Create new migration files instead
2. **NEVER delete migration files** - Keep full history
3. **Test migrations locally** before committing
4. **Use transactions** for complex migrations (PostgreSQL)
5. **Add rollback comments** for complex changes

## Handling Migration Errors

### Checksum Mismatch Error

```
FlywayValidateException: Migration checksum mismatch for migration version X
```

**Solution (Development Only):**
```powershell
# Complete database reset
docker-compose down -v
docker system prune -f
.\gradlew.bat bootJar
docker-compose up --build
```

### Failed Migration Recovery

```
FlywayValidateException: Detected failed migration to version X
```

**Solution:**
1. Fix the migration SQL syntax
2. Reset the database (development)
3. Or run Flyway repair (with caution)

## Test Fixtures Updates

**When adding new migrations, update test fixtures:**

1. Create/update database defaults in `src/testFixtures/java/com/salonhub/api/[domain]/`
2. Update `ServerSetupExtension` if schema changes affect test data
3. Ensure integration tests use the new schema

**Example Database Default:**
```java
public class ServiceTypeDatabaseDefault {
    public static final Long HAIRCUT_ID = 1L;
    public static final String HAIRCUT_NAME = "Haircut";
    
    public static final String INSERT_HAIRCUT = 
        "INSERT INTO service_types (id, name, duration_minutes, price, active) VALUES " +
        "(1, 'Haircut', 30, 25.00, true)";
}
```

## Checklist for Schema Changes

- [ ] Create new migration file with correct naming
- [ ] Test migration locally with H2 profile
- [ ] Test migration with Docker PostgreSQL
- [ ] Update JPA entities to match schema
- [ ] Update test fixtures/database defaults
- [ ] Run full test suite: `.\gradlew.bat check`
- [ ] Verify integration tests pass
