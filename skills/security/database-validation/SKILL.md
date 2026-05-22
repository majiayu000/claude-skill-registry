---
name: database-validation
description: Comprehensive database security scanning and data integrity validation. Identify security vulnerabilities, enforce OWASP compliance, validate data types/formats/ranges, ensure referential integrity, and implement business rules. Use when assessing database security, checking compliance, validating data integrity, or enforcing constraints.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 1.0.0
---

# Database Validation & Security

Ensure database security and data integrity through automated security scanning and comprehensive data validation.

## Overview

This skill empowers you to:
- **Security Scanning**: Identify vulnerabilities, weak passwords, SQL injection risks, and insecure configurations
- **OWASP Compliance**: Ensure adherence to OWASP security guidelines
- **Data Integrity**: Validate data types, ranges, formats, and business rules
- **Referential Integrity**: Verify foreign key relationships and constraints
- **Automated Remediation**: Receive actionable recommendations and fix scripts

---

## Part 1: Database Security Scanning

### How Security Scanning Works

1. **Initiate Scan**: Analyze database configuration and access patterns
2. **Vulnerability Assessment**: Identify weak passwords, injection risks, permission issues
3. **OWASP Compliance Check**: Verify adherence to OWASP Top 10 and database security standards
4. **Report Generation**: Create detailed findings with severity levels
5. **Remediation Guidance**: Provide fix scripts and configuration recommendations

### When to Use Security Scanning

- Assess overall database security posture
- Identify potential security vulnerabilities
- Ensure OWASP compliance before production deployment
- Audit database configurations regularly
- Investigate security incidents
- Prepare for security audits or compliance certifications

### Security Scanning Examples

#### Example 1: PostgreSQL Security Assessment

**User request**: "Scan my PostgreSQL database for security vulnerabilities and generate a report."

**Security Scan Output**:
```
🔴 CRITICAL VULNERABILITIES (3)
─────────────────────────────────

1. Weak Database Password
   - Severity: CRITICAL
   - Database: production_db
   - Issue: Default password still in use
   - Risk: Unauthorized access, data breach
   - Remediation:
     ALTER USER postgres WITH PASSWORD 'NewSecureP@ssw0rd!2025';

2. Public Schema Permissions Too Broad
   - Severity: CRITICAL
   - Schema: public
   - Issue: PUBLIC role has CREATE privilege
   - Risk: Malicious users can create objects
   - Remediation:
     REVOKE CREATE ON SCHEMA public FROM PUBLIC;

3. SSL Connection Not Enforced
   - Severity: CRITICAL
   - Setting: ssl = off
   - Risk: Data transmitted in plaintext
   - Remediation:
     # postgresql.conf
     ssl = on
     ssl_cert_file = '/path/to/server.crt'
     ssl_key_file = '/path/to/server.key'

🟡 WARNINGS (5)
───────────────

4. Overly Permissive User Grants
   - Severity: WARNING
   - User: app_user
   - Issue: Has SUPERUSER privileges
   - Remediation:
     ALTER USER app_user NOSUPERUSER;
     GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;

5. Logging Insufficient for Security Monitoring
   - Severity: WARNING
   - Issue: Statement logging disabled
   - Remediation:
     # postgresql.conf
     log_statement = 'all'
     log_connections = on
     log_disconnections = on

6. No Row-Level Security Enabled
   - Severity: WARNING
   - Tables: users, orders, payments
   - Risk: Users can access all rows
   - Remediation:
     ALTER TABLE users ENABLE ROW LEVEL SECURITY;
     CREATE POLICY user_policy ON users FOR SELECT
       USING (id = current_user_id());

7. Weak Password Policy
   - Severity: WARNING
   - Issue: No password complexity requirements
   - Remediation:
     # Install and configure pgcrypto extension
     CREATE EXTENSION IF NOT EXISTS pgcrypto;

8. Backup Encryption Disabled
   - Severity: WARNING
   - Issue: Database backups not encrypted
   - Remediation: Enable encrypted backups with pgBackRest or similar

✅ PASSED CHECKS (12)
─────────────────────
- SQL injection protection enabled
- Prepared statements used consistently
- Database firewall rules configured
- User authentication method secure (scram-sha-256)
- Audit logging enabled
- Sensitive data encrypted at rest
- No default accounts active
- Connection limits configured
- Query timeout set appropriately
- Idle connection timeout set
- Database patched to latest version
- No outdated extensions found

📊 OWASP COMPLIANCE: 73% (16/22 checks passed)

🔧 RECOMMENDED ACTIONS:
1. Change default passwords immediately
2. Enable SSL/TLS for all connections
3. Implement row-level security on sensitive tables
4. Review and restrict user permissions
5. Enable comprehensive logging and monitoring
6. Schedule regular security scans (monthly)
```

#### Example 2: MySQL OWASP Compliance Check

**User request**: "Perform an OWASP compliance check on the MySQL database."

**Compliance Report**:
```
🛡️  OWASP DATABASE SECURITY CHECKLIST
════════════════════════════════════════

A1: Injection (SQL Injection)
  ✅ Prepared statements used in application
  ✅ Input validation implemented
  ❌ mysql_real_escape_string() found in legacy code
  → Remediation: Replace with prepared statements

A2: Broken Authentication
  ✅ Strong password policy enforced
  ❌ No account lockout after failed attempts
  ❌ Session timeout not configured
  → Remediation:
    SET GLOBAL max_connect_errors = 5;
    SET SESSION wait_timeout = 300;

A3: Sensitive Data Exposure
  ❌ Credit card data stored in plaintext
  ❌ SSL not required for connections
  ✅ Password hashing uses bcrypt
  → Remediation:
    -- Encrypt credit_card column
    ALTER TABLE payments ADD COLUMN cc_encrypted VARBINARY(256);
    -- Require SSL
    ALTER USER 'app_user'@'%' REQUIRE SSL;

A4: XML External Entities (XXE)
  N/A - Not applicable for database layer

A5: Broken Access Control
  ❌ Users have excessive privileges
  ✅ Views used for data access control
  → Remediation:
    REVOKE ALL PRIVILEGES ON *.* FROM 'app_user'@'%';
    GRANT SELECT, INSERT, UPDATE, DELETE ON app_db.* TO 'app_user'@'%';

A6: Security Misconfiguration
  ❌ Anonymous user account exists
  ❌ test database still present
  ✅ Remote root access disabled
  → Remediation:
    DROP USER ''@'localhost';
    DROP USER ''@'%';
    DROP DATABASE test;

A7: Cross-Site Scripting (XSS)
  N/A - Application layer concern

A8: Insecure Deserialization
  N/A - Not applicable for database layer

A9: Using Components with Known Vulnerabilities
  ❌ MySQL version 8.0.25 (outdated)
  → Remediation: Upgrade to MySQL 8.0.35+

A10: Insufficient Logging & Monitoring
  ❌ General query log disabled
  ❌ Slow query log disabled
  ✅ Binary logging enabled
  → Remediation:
    SET GLOBAL general_log = 'ON';
    SET GLOBAL slow_query_log = 'ON';
    SET GLOBAL long_query_time = 2;

OVERALL SCORE: 12/20 checks passed (60%)
STATUS: ⚠️  NEEDS IMPROVEMENT

PRIORITY ACTIONS:
1. [CRITICAL] Remove anonymous users
2. [CRITICAL] Encrypt sensitive data
3. [HIGH] Upgrade MySQL to latest version
4. [HIGH] Implement account lockout policy
5. [MEDIUM] Enable comprehensive logging
```

---

## Part 2: Data Integrity Validation

### How Data Validation Works

1. **Rule Definition**: Analyze schema and identify validation requirements
2. **Constraint Implementation**: Apply CHECK constraints, foreign keys, triggers
3. **Format Validation**: Validate emails, URLs, phone numbers, dates
4. **Business Rule Enforcement**: Implement custom logic (e.g., order total = sum of items)
5. **Verification**: Test constraints with valid and invalid data

### When to Use Data Validation

- Implement data validation for new schemas
- Enforce integrity constraints on existing tables
- Validate user input at database level
- Ensure data quality and consistency
- Prevent invalid data from entering database
- Audit existing data for violations

### Data Validation Examples

#### Example 1: Implementing Comprehensive User Validation

**User request**: "Add data validation to the users table for age, email, and username."

**Validation Implementation**:
```sql
-- PostgreSQL validation constraints
ALTER TABLE users
  -- Age validation: Must be between 13 and 120
  ADD CONSTRAINT check_age_range 
    CHECK (age >= 13 AND age <= 120),
  
  -- Email validation: Must match email format
  ADD CONSTRAINT check_email_format 
    CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
  
  -- Username validation: 3-30 alphanumeric characters
  ADD CONSTRAINT check_username_format 
    CHECK (username ~* '^[A-Za-z0-9_]{3,30}$'),
  
  -- Username uniqueness
  ADD CONSTRAINT unique_username UNIQUE (username),
  
  -- Email uniqueness (case-insensitive)
  ADD CONSTRAINT unique_email_lower UNIQUE (LOWER(email));

-- Test validations
-- ❌ Should fail: age too young
INSERT INTO users (name, age, email, username) 
VALUES ('Kid', 10, 'kid@example.com', 'kiduser');
-- Error: new row violates check constraint "check_age_range"

-- ❌ Should fail: invalid email
INSERT INTO users (name, age, email, username) 
VALUES ('John', 25, 'not-an-email', 'john123');
-- Error: new row violates check constraint "check_email_format"

-- ✅ Should succeed: all validations pass
INSERT INTO users (name, age, email, username) 
VALUES ('John Doe', 25, 'john@example.com', 'john123');
-- Success!
```

#### Example 2: Order and Order Items Integrity

**User request**: "Ensure referential integrity between orders and order_items, and validate that order total matches sum of items."

**Integrity Implementation**:
```sql
-- MySQL validation setup

-- Foreign key for referential integrity
ALTER TABLE order_items
  ADD CONSTRAINT fk_order_items_order_id
    FOREIGN KEY (order_id) REFERENCES orders(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- Ensure item quantity is positive
ALTER TABLE order_items
  ADD CONSTRAINT check_quantity_positive
    CHECK (quantity > 0);

-- Ensure item price is non-negative
ALTER TABLE order_items
  ADD CONSTRAINT check_price_nonnegative
    CHECK (price >= 0);

-- Trigger to validate order total matches sum of items
DELIMITER $$

CREATE TRIGGER validate_order_total_before_update
BEFORE UPDATE ON orders
FOR EACH ROW
BEGIN
  DECLARE calculated_total DECIMAL(10, 2);
  
  -- Calculate actual total from order_items
  SELECT SUM(quantity * price)
  INTO calculated_total
  FROM order_items
  WHERE order_id = NEW.id;
  
  -- Validate total matches
  IF NEW.total != calculated_total THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Order total does not match sum of order items';
  END IF;
END$$

CREATE TRIGGER validate_order_total_after_item_change
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
  DECLARE calculated_total DECIMAL(10, 2);
  DECLARE stored_total DECIMAL(10, 2);
  
  -- Get calculated total
  SELECT SUM(quantity * price)
  INTO calculated_total
  FROM order_items
  WHERE order_id = NEW.order_id;
  
  -- Get stored total
  SELECT total
  INTO stored_total
  FROM orders
  WHERE id = NEW.order_id;
  
  -- Auto-update if mismatch
  IF calculated_total != stored_total THEN
    UPDATE orders
    SET total = calculated_total,
        updated_at = NOW()
    WHERE id = NEW.order_id;
  END IF;
END$$

DELIMITER ;

-- Test referential integrity
-- ❌ Should fail: order_id doesn't exist
INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES (999999, 1, 2, 10.00);
-- Error: Cannot add or update a child row: foreign key constraint fails

-- Test business rule validation
INSERT INTO orders (id, customer_id, total) VALUES (1, 1, 100.00);
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (1, 1, 2, 25.00);
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (1, 2, 1, 50.00);

-- ✅ Total auto-corrected: 2*25 + 1*50 = 100.00
SELECT * FROM orders WHERE id = 1;
-- total = 100.00 (correct!)
```

#### Example 3: Product Inventory Validation

**User request**: "Add validation to prevent negative inventory and ensure product SKUs are unique."

**Validation Rules**:
```sql
-- SQL Server validation

-- Prevent negative inventory
ALTER TABLE products
  ADD CONSTRAINT check_inventory_nonnegative
    CHECK (inventory_quantity >= 0);

-- Ensure SKU is unique and follows format
ALTER TABLE products
  ADD CONSTRAINT unique_product_sku UNIQUE (sku);

ALTER TABLE products
  ADD CONSTRAINT check_sku_format
    CHECK (sku LIKE '[A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]');
    -- Format: ABC-1234

-- Prevent price from being negative
ALTER TABLE products
  ADD CONSTRAINT check_price_positive
    CHECK (price > 0);

-- Ensure discount doesn't exceed price
ALTER TABLE products
  ADD CONSTRAINT check_discount_valid
    CHECK (discount_price IS NULL OR discount_price < price);

-- Test validations
-- ❌ Should fail: negative inventory
UPDATE products SET inventory_quantity = -5 WHERE id = 1;
-- Error: check constraint "check_inventory_nonnegative"

-- ❌ Should fail: invalid SKU format
INSERT INTO products (name, sku, price) 
VALUES ('Test Product', '12345', 29.99);
-- Error: check constraint "check_sku_format"

-- ❌ Should fail: discount > price
INSERT INTO products (name, sku, price, discount_price) 
VALUES ('Test Product', 'ABC-1234', 29.99, 35.00);
-- Error: check constraint "check_discount_valid"

-- ✅ Should succeed
INSERT INTO products (name, sku, price, inventory_quantity) 
VALUES ('Test Product', 'ABC-1234', 29.99, 100);
-- Success!
```

---

## Common Validation Patterns

### Data Type Validation
```sql
-- Integers within range
CHECK (age BETWEEN 0 AND 150)

-- Decimals with precision
CHECK (price >= 0.00 AND price <= 999999.99)

-- Enum values
CHECK (status IN ('pending', 'active', 'completed', 'cancelled'))

-- Boolean
CHECK (is_active IN (0, 1))
```

### Format Validation
```sql
-- Email (PostgreSQL regex)
CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')

-- Phone number (US format)
CHECK (phone ~* '^\+?1?[-.]?\(?[0-9]{3}\)?[-.]?[0-9]{3}[-.]?[0-9]{4}$')

-- URL
CHECK (website ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}')

-- Date not in future
CHECK (birth_date <= CURRENT_DATE)

-- Credit card (basic Luhn check needed at app level)
CHECK (CHAR_LENGTH(credit_card) BETWEEN 13 AND 19)
```

### Referential Integrity
```sql
-- Foreign key with cascade
FOREIGN KEY (user_id) REFERENCES users(id)
  ON DELETE CASCADE
  ON UPDATE CASCADE

-- Foreign key preventing deletion
FOREIGN KEY (category_id) REFERENCES categories(id)
  ON DELETE RESTRICT

-- Composite foreign key
FOREIGN KEY (order_id, product_id) 
  REFERENCES order_items(order_id, product_id)
```

### Business Logic Validation
```sql
-- Start date before end date
CHECK (start_date < end_date)

-- Discount must be less than original price
CHECK (discount_price IS NULL OR discount_price < original_price)

-- Total matches calculation
CHECK (total = subtotal + tax + shipping)

-- Min/max order quantity
CHECK (quantity >= min_order_qty AND quantity <= max_order_qty)
```

---

## Security Best Practices

### ✅ DO:
- Use prepared statements/parameterized queries
- Enforce SSL/TLS for database connections
- Implement principle of least privilege
- Enable comprehensive logging
- Regularly update database software
- Encrypt sensitive data at rest
- Use strong password policies
- Implement row-level security where needed
- Regular security audits and scans
- Enable two-factor authentication for admin access

### ❌ DON'T:
- Store passwords in plaintext
- Grant SUPERUSER/root access to applications
- Use default passwords
- Allow anonymous database access
- Expose database directly to internet
- Ignore security updates
- Use weak encryption algorithms
- Trust user input without validation
- Skip regular backups
- Leave unused accounts active

---

## Integration with Other Tools

- **Security Scanning**: OWASP ZAP, sqlmap, Nessus
- **Monitoring**: Datadog, New Relic, Prometheus
- **CI/CD**: Integrate security scans in deployment pipeline
- **Compliance**: PCI DSS, HIPAA, GDPR validation tools
- **Backup**: Automated encrypted backups
- **Logging**: Centralized logging (ELK stack, Splunk)

---

**Remember**: Database security and data integrity are ongoing processes. Regular scanning, validation, and updates are essential for maintaining a secure and reliable database.
