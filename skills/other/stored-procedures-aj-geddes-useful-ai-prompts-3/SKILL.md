---
name: stored-procedures
description: Implement stored procedures and functions for database logic. Use when creating reusable database routines, complex queries, or server-side calculations.
---

# Stored Procedures & Functions

## Overview

Implement stored procedures, functions, and triggers for business logic, data validation, and performance optimization. Covers procedure design, error handling, and performance considerations.

## When to Use

- Business logic encapsulation
- Complex multi-step operations
- Data validation and constraints
- Audit trail maintenance
- Performance optimization
- Code reusability across applications
- Trigger-based automation

## PostgreSQL Procedures & Functions

### Simple Functions

**PostgreSQL - Scalar Function:**

```sql
-- Create function returning single value
CREATE OR REPLACE FUNCTION calculate_order_total(
  p_subtotal DECIMAL,
  p_tax_rate DECIMAL,
  p_shipping DECIMAL
)
RETURNS DECIMAL AS $$
BEGIN
  RETURN ROUND((p_subtotal * (1 + p_tax_rate) + p_shipping)::NUMERIC, 2);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Use in queries
SELECT id, subtotal, calculate_order_total(subtotal, 0.08, 10) as total
FROM orders;

-- Or in application code
SELECT * FROM orders
WHERE calculate_order_total(subtotal, 0.08, 10) > 100;
```

**PostgreSQL - Table Returning Function:**

```sql
-- Return set of rows
CREATE OR REPLACE FUNCTION get_user_orders(p_user_id UUID)
RETURNS TABLE (
  order_id UUID,
  order_date TIMESTAMP,
  total DECIMAL,
  status VARCHAR
) AS $$
BEGIN
  RETURN QUERY
  SELECT o.id, o.created_at, o.total, o.status
  FROM orders o
  WHERE o.user_id = p_user_id
  ORDER BY o.created_at DESC;
END;
$$ LANGUAGE plpgsql STABLE;

-- Use function
SELECT * FROM get_user_orders('user-123');
```

### Stored Procedures

**PostgreSQL - Procedure with OUT Parameters:**

```sql
-- Stored procedure with output parameters
CREATE OR REPLACE PROCEDURE process_order(
  p_order_id UUID,
  OUT p_success BOOLEAN,
  OUT p_message VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
  BEGIN
    -- Start transaction
    UPDATE orders SET status = 'processing' WHERE id = p_order_id;

    UPDATE inventory
    SET quantity = quantity - 1
    WHERE product_id IN (
      SELECT product_id FROM order_items WHERE order_id = p_order_id
    );

    -- Check inventory
    IF EXISTS (SELECT 1 FROM inventory WHERE quantity < 0) THEN
      RAISE EXCEPTION 'Insufficient inventory';
    END IF;

    p_success := true;
    p_message := 'Order processed successfully';
  EXCEPTION WHEN OTHERS THEN
    p_success := false;
    p_message := SQLERRM;
    -- Transaction automatically rolled back
  END;
END;
$$;

-- Call procedure
CALL process_order('order-123', success, message);
SELECT success, message;
```

**Complex Procedure with Logic:**

```sql
CREATE OR REPLACE PROCEDURE transfer_funds(
  p_from_account_id INT,
  p_to_account_id INT,
  p_amount DECIMAL,
  OUT p_success BOOLEAN,
  OUT p_error_message VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
  v_from_balance DECIMAL;
BEGIN
  BEGIN
    -- Check balance
    SELECT balance INTO v_from_balance
    FROM accounts
    WHERE id = p_from_account_id
    FOR UPDATE;

    IF v_from_balance < p_amount THEN
      RAISE EXCEPTION 'Insufficient funds';
    END IF;

    -- Debit from account
    UPDATE accounts
    SET balance = balance - p_amount
    WHERE id = p_from_account_id;

    -- Credit to account
    UPDATE accounts
    SET balance = balance + p_amount
    WHERE id = p_to_account_id;

    -- Log transaction
    INSERT INTO transaction_log (from_id, to_id, amount, status)
    VALUES (p_from_account_id, p_to_account_id, p_amount, 'completed');

    p_success := true;
    p_error_message := NULL;
  EXCEPTION WHEN OTHERS THEN
    p_success := false;
    p_error_message := SQLERRM;
  END;
END;
$$;
```

## MySQL Stored Procedures

### Simple Procedures

**MySQL - Basic Procedure:**

```sql
-- Simple procedure
DELIMITER //

CREATE PROCEDURE get_user_by_email(IN p_email VARCHAR(255))
BEGIN
  SELECT id, email, name, created_at
  FROM users
  WHERE email = p_email;
END //

DELIMITER ;

-- Call procedure
CALL get_user_by_email('john@example.com');
```

**MySQL - Procedure with OUT Parameters:**

```sql
DELIMITER //

CREATE PROCEDURE calculate_user_stats(
  IN p_user_id INT,
  OUT p_total_orders INT,
  OUT p_total_spent DECIMAL
)
BEGIN
  SELECT
    COUNT(*),
    SUM(total)
  INTO p_total_orders, p_total_spent
  FROM orders
  WHERE user_id = p_user_id AND status != 'cancelled';

  IF p_total_orders IS NULL THEN
    SET p_total_orders = 0;
    SET p_total_spent = 0;
  END IF;
END //

DELIMITER ;

-- Call procedure
CALL calculate_user_stats(123, @orders, @spent);
SELECT @orders as total_orders, @spent as total_spent;
```

### Complex Procedures with Error Handling

**MySQL - Transaction Management:**

```sql
DELIMITER //

CREATE PROCEDURE create_order(
  IN p_user_id INT,
  IN p_items JSON,
  OUT p_order_id INT,
  OUT p_success BOOLEAN,
  OUT p_error VARCHAR(500)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    SET p_success = FALSE;
    SET p_error = 'Transaction failed';
  END;

  START TRANSACTION;

  -- Create order
  INSERT INTO orders (user_id, status, created_at)
  VALUES (p_user_id, 'pending', NOW());

  SET p_order_id = LAST_INSERT_ID();

  -- Add items to order (assuming items is JSON array)
  -- Would require JSON parsing in MySQL 5.7+
  -- INSERT INTO order_items (order_id, product_id, quantity)
  -- SELECT p_order_id, JSON_EXTRACT(...), ...

  -- Update inventory
  UPDATE inventory
  SET quantity = quantity - 1
  WHERE product_id IN (
    SELECT product_id FROM order_items WHERE order_id = p_order_id
  );

  -- Check inventory
  IF EXISTS (SELECT 1 FROM inventory WHERE quantity < 0) THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Insufficient inventory';
  END IF;

  COMMIT;
  SET p_success = TRUE;
  SET p_error = NULL;
END //

DELIMITER ;
```

## Triggers

### PostgreSQL Triggers

**Audit Trail Trigger:**

```sql
-- Audit table
CREATE TABLE user_audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID,
  operation VARCHAR(10),
  old_values JSONB,
  new_values JSONB,
  changed_at TIMESTAMP DEFAULT NOW()
);

-- Trigger function
CREATE OR REPLACE FUNCTION audit_user_changes()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO user_audit_log (user_id, operation, old_values, new_values)
  VALUES (
    COALESCE(NEW.id, OLD.id),
    TG_OP,
    to_jsonb(OLD),
    to_jsonb(NEW)
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER user_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION audit_user_changes();
```

**Update Timestamp Trigger:**

```sql
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER update_orders_timestamp
BEFORE UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
```

**Validation Trigger:**

```sql
CREATE OR REPLACE FUNCTION validate_order()
RETURNS TRIGGER AS $$
BEGIN
  -- Validate order total
  IF NEW.total < 0 THEN
    RAISE EXCEPTION 'Order total cannot be negative';
  END IF;

  -- Validate user exists
  IF NOT EXISTS (SELECT 1 FROM users WHERE id = NEW.user_id) THEN
    RAISE EXCEPTION 'User does not exist';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_order_trigger
BEFORE INSERT OR UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION validate_order();
```

### MySQL Triggers

**MySQL - Insert Trigger:**

```sql
DELIMITER //

CREATE TRIGGER create_order_trigger
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
  -- Update user statistics
  UPDATE user_stats
  SET total_orders = total_orders + 1,
      total_spent = total_spent + NEW.total
  WHERE user_id = NEW.user_id;

  -- Create audit log
  INSERT INTO audit_log (table_name, operation, record_id, timestamp)
  VALUES ('orders', 'INSERT', NEW.id, NOW());
END //

DELIMITER ;
```

**MySQL - Update Prevention Trigger:**

```sql
DELIMITER //

CREATE TRIGGER prevent_old_order_update
BEFORE UPDATE ON orders
FOR EACH ROW
BEGIN
  IF OLD.status = 'completed' THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Cannot update completed orders';
  END IF;
END //

DELIMITER ;
```

## Function Performance

**PostgreSQL - IMMUTABLE vs STABLE vs VOLATILE:**

```sql
-- IMMUTABLE: Result always same for same arguments (can be optimized)
CREATE FUNCTION calculate_tax(p_amount DECIMAL)
RETURNS DECIMAL AS $$
BEGIN
  RETURN p_amount * 0.08;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- STABLE: Result consistent within query (can use as index)
CREATE FUNCTION get_current_year()
RETURNS INT AS $$
BEGIN
  RETURN EXTRACT(YEAR FROM CURRENT_DATE);
END;
$$ LANGUAGE plpgsql STABLE;

-- VOLATILE: Can change (function executed every time)
CREATE FUNCTION get_random_user()
RETURNS UUID AS $$
BEGIN
  RETURN (SELECT id FROM users ORDER BY RANDOM() LIMIT 1);
END;
$$ LANGUAGE plpgsql VOLATILE;
```

## Parameter Validation

**PostgreSQL - Input Validation:**

```sql
CREATE OR REPLACE FUNCTION create_user(
  p_email VARCHAR,
  p_name VARCHAR
)
RETURNS UUID AS $$
DECLARE
  v_user_id UUID;
BEGIN
  -- Validate inputs
  IF p_email IS NULL OR p_email = '' THEN
    RAISE EXCEPTION 'Email cannot be empty';
  END IF;

  IF p_name IS NULL OR LENGTH(p_name) < 2 THEN
    RAISE EXCEPTION 'Name must be at least 2 characters';
  END IF;

  -- Check email format
  IF NOT p_email ~ '^\w+@\w+\.\w+$' THEN
    RAISE EXCEPTION 'Invalid email format';
  END IF;

  -- Create user
  INSERT INTO users (email, name)
  VALUES (LOWER(p_email), TRIM(p_name))
  RETURNING id INTO v_user_id;

  RETURN v_user_id;
EXCEPTION WHEN unique_violation THEN
  RAISE EXCEPTION 'Email already exists';
END;
$$ LANGUAGE plpgsql;
```

## Testing Procedures

**PostgreSQL - Test Function:**

```sql
-- Test transfer_funds procedure
DO $$
DECLARE
  v_success BOOLEAN;
  v_error VARCHAR;
BEGIN
  CALL transfer_funds(1, 2, 100, v_success, v_error);
  ASSERT v_success, 'Transfer should succeed: ' || v_error;

  -- Verify transfer
  ASSERT (SELECT balance FROM accounts WHERE id = 1) = 900,
    'Account 1 balance should be 900';
  ASSERT (SELECT balance FROM accounts WHERE id = 2) = 1100,
    'Account 2 balance should be 1100';

  RAISE NOTICE 'All tests passed';
END $$;
```

## Procedure Maintenance

**PostgreSQL - Drop Procedure:**

```sql
-- Drop function
DROP FUNCTION IF EXISTS calculate_order_total(DECIMAL, DECIMAL, DECIMAL);

-- Drop procedure
DROP PROCEDURE IF EXISTS process_order(UUID);

-- Drop trigger
DROP TRIGGER IF EXISTS user_audit_trigger ON users;
DROP FUNCTION IF EXISTS audit_user_changes();
```

## Best Practices

✅ DO use procedures for complex operations
✅ DO validate inputs in procedures
✅ DO handle errors gracefully
✅ DO document procedure parameters
✅ DO test procedures thoroughly
✅ DO use transactions appropriately
✅ DO monitor procedure performance

❌ DON'T put all business logic in procedures
❌ DON'T use procedures for simple queries
❌ DON'T ignore error handling
❌ DON'T create poorly documented procedures
❌ DON'T use procedures as security layer only

## Resources

- [PostgreSQL Functions Documentation](https://www.postgresql.org/docs/current/sql-createfunction.html)
- [PostgreSQL PL/pgSQL Guide](https://www.postgresql.org/docs/current/plpgsql.html)
- [MySQL Stored Procedures](https://dev.mysql.com/doc/refman/8.0/en/stored-routines.html)
- [PostgreSQL Triggers](https://www.postgresql.org/docs/current/sql-createtrigger.html)
