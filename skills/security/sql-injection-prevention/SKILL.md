---
name: sql-injection-prevention
description: Эксперт по защите от SQL injection. Используй для parameterized queries, input validation и database security.
---

# SQL Injection Prevention Expert

Эксперт по идентификации, предотвращению и митигации SQL injection уязвимостей во всех языках программирования и СУБД.

## Core Principles

### Primary Defense Mechanisms

```yaml
defense_layers:
  - name: "Parameterized Queries"
    priority: 1
    description: "The gold standard for preventing SQL injection"

  - name: "Input Validation"
    priority: 2
    description: "Whitelist validation with strict data type enforcement"

  - name: "Stored Procedures"
    priority: 3
    description: "When implemented correctly with parameterized inputs"

  - name: "Escaping"
    priority: 4
    description: "Last resort, database-specific escaping functions"

  - name: "Least Privilege"
    priority: 5
    description: "Database users with minimal required permissions"
```

### Defense in Depth Strategy

- Никогда не полагайся на один метод защиты
- Комбинируй несколько слоёв: input validation, parameterized queries, WAF, мониторинг
- Внедряй и превентивные, и детектирующие контроли
- Регулярное тестирование безопасности и code review

---

## Parameterized Queries Implementation

### Java (JDBC)

```java
// VULNERABLE - String concatenation
String query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);

// SECURE - Prepared statements
String query = "SELECT * FROM users WHERE username=? AND password=?";
PreparedStatement pstmt = connection.prepareStatement(query);
pstmt.setString(1, username);
pstmt.setString(2, password);
ResultSet rs = pstmt.executeQuery();
```

### Python (SQLAlchemy)

```python
# VULNERABLE - String formatting
query = f"SELECT * FROM users WHERE email = '{email}' AND status = '{status}'"
result = db.execute(query)

# SECURE - Parameterized query
from sqlalchemy import text
query = text("SELECT * FROM users WHERE email = :email AND status = :status")
result = db.execute(query, {"email": email, "status": status})

# SECURE - ORM approach (preferred)
result = db.session.query(User).filter(
    User.email == email,
    User.status == status
).all()
```

### PHP (PDO)

```php
// VULNERABLE - Direct concatenation
$query = "SELECT * FROM products WHERE category = '$category' AND price < $maxPrice";
$result = $pdo->query($query);

// SECURE - Prepared statements
$query = "SELECT * FROM products WHERE category = :category AND price < :maxPrice";
$stmt = $pdo->prepare($query);
$stmt->bindParam(':category', $category, PDO::PARAM_STR);
$stmt->bindParam(':maxPrice', $maxPrice, PDO::PARAM_INT);
$stmt->execute();
```

### Node.js (MySQL2)

```javascript
// VULNERABLE - Template literals
const query = `SELECT * FROM orders WHERE user_id = ${userId} AND status = '${status}'`;
connection.query(query, (error, results) => { /* ... */ });

// SECURE - Parameterized queries
const query = 'SELECT * FROM orders WHERE user_id = ? AND status = ?';
connection.execute(query, [userId, status], (error, results) => {
    // Handle results
});
```

### Go (database/sql)

```go
// VULNERABLE
query := fmt.Sprintf("SELECT * FROM users WHERE id = %s", userID)
rows, err := db.Query(query)

// SECURE - Parameterized query
query := "SELECT * FROM users WHERE id = $1"
rows, err := db.Query(query, userID)
```

---

## Input Validation and Sanitization

### Robust Input Validation

```python
import re
from typing import Optional, List

def validate_user_input(user_id: str, email: str, role: str) -> dict:
    """Validate user input with strict rules"""
    errors: List[str] = []

    # Validate user ID (numeric only)
    if not user_id.isdigit() or int(user_id) <= 0:
        errors.append("Invalid user ID format")

    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        errors.append("Invalid email format")

    # Validate role against whitelist
    allowed_roles = ['user', 'admin', 'moderator']
    if role not in allowed_roles:
        errors.append("Invalid role specified")

    return {'valid': len(errors) == 0, 'errors': errors}


def sanitize_identifier(identifier: str) -> Optional[str]:
    """Sanitize SQL identifiers (table/column names)"""
    # Only allow alphanumeric and underscore
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier):
        return identifier
    return None
```

### TypeScript Input Validation

```typescript
interface ValidationResult {
  valid: boolean;
  errors: string[];
  sanitized?: Record<string, unknown>;
}

function validateSearchParams(params: {
  query?: string;
  limit?: number;
  sortBy?: string;
}): ValidationResult {
  const errors: string[] = [];
  const sanitized: Record<string, unknown> = {};

  // Validate query (alphanumeric, spaces, basic punctuation)
  if (params.query) {
    const cleanQuery = params.query.replace(/[^a-zA-Z0-9\s\-_.]/g, '');
    if (cleanQuery.length > 100) {
      errors.push('Query too long');
    } else {
      sanitized.query = cleanQuery;
    }
  }

  // Validate limit (positive integer, max 100)
  if (params.limit !== undefined) {
    const limit = Number(params.limit);
    if (!Number.isInteger(limit) || limit < 1 || limit > 100) {
      errors.push('Invalid limit');
    } else {
      sanitized.limit = limit;
    }
  }

  // Validate sortBy against whitelist
  const allowedSortFields = ['name', 'created_at', 'updated_at', 'price'];
  if (params.sortBy && !allowedSortFields.includes(params.sortBy)) {
    errors.push('Invalid sort field');
  } else if (params.sortBy) {
    sanitized.sortBy = params.sortBy;
  }

  return {
    valid: errors.length === 0,
    errors,
    sanitized: errors.length === 0 ? sanitized : undefined
  };
}
```

---

## Advanced Prevention Techniques

### Stored Procedures with Parameters

```sql
-- SQL Server stored procedure
CREATE PROCEDURE GetUserOrders
    @UserID INT,
    @Status NVARCHAR(20),
    @StartDate DATE
AS
BEGIN
    SET NOCOUNT ON;

    SELECT OrderID, OrderDate, TotalAmount
    FROM Orders
    WHERE UserID = @UserID
        AND Status = @Status
        AND OrderDate >= @StartDate
    ORDER BY OrderDate DESC;
END
GO
```

### Dynamic Query Building (Secure Approach)

```java
public class SecureQueryBuilder {
    private static final Set<String> ALLOWED_SORT_COLUMNS =
        Set.of("name", "email", "created_date", "status");

    private static final Set<String> ALLOWED_SORT_ORDERS =
        Set.of("ASC", "DESC");

    public PreparedStatement buildUserQuery(
            Connection conn,
            String sortColumn,
            String sortOrder,
            String statusFilter) throws SQLException {

        // Validate sort column against whitelist
        if (!ALLOWED_SORT_COLUMNS.contains(sortColumn)) {
            throw new IllegalArgumentException("Invalid sort column: " + sortColumn);
        }

        // Validate sort order
        String normalizedOrder = sortOrder.toUpperCase();
        if (!ALLOWED_SORT_ORDERS.contains(normalizedOrder)) {
            throw new IllegalArgumentException("Invalid sort order: " + sortOrder);
        }

        // Build query with validated column names and parameterized values
        String query = "SELECT user_id, name, email FROM users " +
                      "WHERE status = ? " +
                      "ORDER BY " + sortColumn + " " + normalizedOrder;

        PreparedStatement stmt = conn.prepareStatement(query);
        stmt.setString(1, statusFilter);
        return stmt;
    }
}
```

### Query Builder Pattern (Node.js)

```typescript
import { Pool } from 'pg';

interface QueryOptions {
  table: string;
  filters: Record<string, unknown>;
  sortBy?: string;
  sortOrder?: 'ASC' | 'DESC';
  limit?: number;
  offset?: number;
}

class SecureQueryBuilder {
  private static readonly ALLOWED_TABLES = new Set([
    'users', 'orders', 'products', 'categories'
  ]);

  private static readonly ALLOWED_COLUMNS: Record<string, Set<string>> = {
    users: new Set(['id', 'name', 'email', 'status', 'created_at']),
    orders: new Set(['id', 'user_id', 'total', 'status', 'created_at']),
    products: new Set(['id', 'name', 'price', 'category_id', 'created_at']),
    categories: new Set(['id', 'name', 'parent_id'])
  };

  buildSelectQuery(options: QueryOptions): { text: string; values: unknown[] } {
    // Validate table
    if (!SecureQueryBuilder.ALLOWED_TABLES.has(options.table)) {
      throw new Error(`Invalid table: ${options.table}`);
    }

    const allowedColumns = SecureQueryBuilder.ALLOWED_COLUMNS[options.table];
    const values: unknown[] = [];
    const conditions: string[] = [];
    let paramIndex = 1;

    // Build WHERE clause with parameterized values
    for (const [column, value] of Object.entries(options.filters)) {
      if (!allowedColumns.has(column)) {
        throw new Error(`Invalid column: ${column}`);
      }
      conditions.push(`${column} = $${paramIndex}`);
      values.push(value);
      paramIndex++;
    }

    let query = `SELECT * FROM ${options.table}`;

    if (conditions.length > 0) {
      query += ` WHERE ${conditions.join(' AND ')}`;
    }

    // Validate and add ORDER BY
    if (options.sortBy) {
      if (!allowedColumns.has(options.sortBy)) {
        throw new Error(`Invalid sort column: ${options.sortBy}`);
      }
      const order = options.sortOrder === 'DESC' ? 'DESC' : 'ASC';
      query += ` ORDER BY ${options.sortBy} ${order}`;
    }

    // Add LIMIT and OFFSET with parameterized values
    if (options.limit !== undefined) {
      query += ` LIMIT $${paramIndex}`;
      values.push(Math.min(Math.max(1, options.limit), 100));
      paramIndex++;
    }

    if (options.offset !== undefined) {
      query += ` OFFSET $${paramIndex}`;
      values.push(Math.max(0, options.offset));
    }

    return { text: query, values };
  }
}
```

---

## Database Security Configuration

### MySQL Security Settings

```sql
-- Create limited privilege user for web application
CREATE USER 'webapp'@'localhost' IDENTIFIED BY 'strong_random_password_here';

-- Grant minimal required permissions
GRANT SELECT, INSERT, UPDATE ON myapp.users TO 'webapp'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON myapp.orders TO 'webapp'@'localhost';
GRANT SELECT ON myapp.products TO 'webapp'@'localhost';

-- Explicitly deny dangerous permissions
-- (These are denied by default, but good to be explicit)
REVOKE FILE, PROCESS, SUPER ON *.* FROM 'webapp'@'localhost';

-- Disable dangerous global settings
SET GLOBAL log_bin_trust_function_creators = 0;
SET GLOBAL local_infile = 0;

-- Flush privileges
FLUSH PRIVILEGES;
```

### PostgreSQL Row Level Security

```sql
-- Enable RLS on sensitive table
ALTER TABLE user_data ENABLE ROW LEVEL SECURITY;

-- Create policy to restrict access by current user
CREATE POLICY user_data_isolation_policy ON user_data
    FOR ALL
    TO webapp_user
    USING (user_id = current_setting('app.current_user_id')::int);

-- Create policy for admin access
CREATE POLICY user_data_admin_policy ON user_data
    FOR ALL
    TO admin_user
    USING (true);

-- Force RLS even for table owners
ALTER TABLE user_data FORCE ROW LEVEL SECURITY;
```

---

## Detection and Monitoring

### SQL Injection Detection Patterns

```python
import re
import logging
from typing import List, Tuple
from datetime import datetime

class SQLInjectionDetector:
    """Detect potential SQL injection patterns in user input"""

    SUSPICIOUS_PATTERNS: List[Tuple[str, str]] = [
        (r"('|(\-\-)|(;)|(\||\|)|(\*|\*))", "SQL metacharacters"),
        (r"((union\s*(all\s*)?select))", "UNION attack"),
        (r"((select\s+.*\s+from)|(insert\s+into)|(update\s+.*\s+set)|(delete\s+from))", "SQL keywords"),
        (r"(exec(ute)?\s*(sp_|xp_))", "Stored procedure execution"),
        (r"(waitfor\s+delay|benchmark\s*\(|sleep\s*\()", "Time-based attack"),
        (r"(0x[0-9a-fA-F]+)", "Hex encoding"),
        (r"(char\s*\(|concat\s*\(|substr\s*\()", "String functions"),
        (r"(information_schema|sys\.)", "Schema enumeration"),
        (r"(or\s+1\s*=\s*1|and\s+1\s*=\s*1|or\s+'[^']*'\s*=\s*'[^']*')", "Boolean injection"),
    ]

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self.compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), name)
            for pattern, name in self.SUSPICIOUS_PATTERNS
        ]

    def detect(self, user_input: str, context: dict = None) -> dict:
        """Detect potential SQL injection in user input"""
        detections = []

        for pattern, attack_type in self.compiled_patterns:
            match = pattern.search(user_input)
            if match:
                detections.append({
                    'type': attack_type,
                    'matched': match.group()[:50],  # Truncate for logging
                    'position': match.start()
                })

        if detections:
            self.logger.warning(
                f"Potential SQL injection detected: {detections}",
                extra={
                    'input_preview': user_input[:100],
                    'context': context,
                    'timestamp': datetime.utcnow().isoformat()
                }
            )

        return {
            'is_suspicious': len(detections) > 0,
            'detections': detections,
            'risk_score': min(len(detections) * 25, 100)
        }
```

### Monitoring Query Patterns

```sql
-- PostgreSQL: Enable query logging for analysis
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_min_duration_statement = 0;

-- Create table for storing suspicious queries
CREATE TABLE security_audit_log (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    query_text TEXT,
    user_name VARCHAR(100),
    client_ip INET,
    risk_indicators JSONB,
    blocked BOOLEAN DEFAULT FALSE
);

-- Function to log suspicious queries
CREATE OR REPLACE FUNCTION log_suspicious_query(
    p_query TEXT,
    p_user VARCHAR,
    p_ip INET,
    p_indicators JSONB
) RETURNS VOID AS $$
BEGIN
    INSERT INTO security_audit_log (query_text, user_name, client_ip, risk_indicators)
    VALUES (p_query, p_user, p_ip, p_indicators);
END;
$$ LANGUAGE plpgsql;
```

---

## Web Application Firewall Rules

### ModSecurity Rules for SQL Injection

```apache
# ModSecurity Core Rule Set - SQL Injection Detection

# Detect SQL injection in request parameters
SecRule ARGS "@detectSQLi" \
    "id:942100,\
    phase:2,\
    block,\
    msg:'SQL Injection Attack Detected',\
    logdata:'Matched Data: %{MATCHED_VAR} found within %{MATCHED_VAR_NAME}',\
    t:none,t:urlDecodeUni,t:htmlEntityDecode,\
    ctl:auditLogParts=+E,\
    ver:'OWASP_CRS/3.3.0',\
    severity:'CRITICAL',\
    setvar:'tx.sql_injection_score=+%{tx.critical_anomaly_score}',\
    setvar:'tx.anomaly_score_pl1=+%{tx.critical_anomaly_score}'"

# Block common SQL injection patterns
SecRule ARGS|ARGS_NAMES|REQUEST_COOKIES|REQUEST_COOKIES_NAMES \
    "(?i:(\b(select|union|insert|update|delete|drop|alter|create|truncate)\b))" \
    "id:942110,\
    phase:2,\
    block,\
    msg:'SQL Keyword Detected in User Input',\
    severity:'WARNING'"

# Block SQL comment sequences
SecRule ARGS "--" \
    "id:942120,\
    phase:2,\
    block,\
    msg:'SQL Comment Sequence Detected',\
    severity:'WARNING'"
```

---

## Testing and Validation

### Automated Security Testing Script

```bash
#!/bin/bash
# SQLMap testing script for your own applications (authorized testing only)

TARGET_URL="http://localhost:8080"
COOKIE="JSESSIONID=your_session_cookie"
OUTPUT_DIR="./sqlmap_results"

mkdir -p "$OUTPUT_DIR"

# Test login form
echo "Testing login form..."
sqlmap -u "$TARGET_URL/login" \
    --data="username=admin&password=pass" \
    --cookie="$COOKIE" \
    --level=3 \
    --risk=2 \
    --batch \
    --output-dir="$OUTPUT_DIR/login" \
    --forms

# Test search endpoint
echo "Testing search endpoint..."
sqlmap -u "$TARGET_URL/api/search?q=test&category=1" \
    --cookie="$COOKIE" \
    --level=3 \
    --risk=2 \
    --batch \
    --output-dir="$OUTPUT_DIR/search"

# Test with different techniques
echo "Testing with all techniques..."
sqlmap -u "$TARGET_URL/api/users?id=1" \
    --cookie="$COOKIE" \
    --technique=BEUSTQ \
    --level=5 \
    --risk=3 \
    --batch \
    --output-dir="$OUTPUT_DIR/users"

echo "Testing complete. Results in $OUTPUT_DIR"
```

### Unit Tests for Input Validation

```python
import pytest
from your_app.security import validate_user_input, SQLInjectionDetector

class TestSQLInjectionPrevention:

    @pytest.fixture
    def detector(self):
        return SQLInjectionDetector()

    def test_clean_input_passes(self, detector):
        result = detector.detect("John Doe")
        assert not result['is_suspicious']

    def test_union_attack_detected(self, detector):
        result = detector.detect("' UNION SELECT * FROM users--")
        assert result['is_suspicious']
        assert any(d['type'] == 'UNION attack' for d in result['detections'])

    def test_comment_attack_detected(self, detector):
        result = detector.detect("admin'--")
        assert result['is_suspicious']

    def test_boolean_injection_detected(self, detector):
        result = detector.detect("' OR '1'='1")
        assert result['is_suspicious']

    def test_valid_email_passes_validation(self):
        result = validate_user_input("123", "user@example.com", "user")
        assert result['valid']

    def test_sql_in_email_fails_validation(self):
        result = validate_user_input("123", "'; DROP TABLE users;--", "user")
        assert not result['valid']
```

---

## Emergency Response Procedures

### Incident Response Checklist

```yaml
sql_injection_incident_response:
  immediate_actions:
    - action: "Block malicious IP addresses"
      command: "iptables -A INPUT -s <attacker_ip> -j DROP"
      priority: 1

    - action: "Disable affected endpoints"
      description: "Temporarily disable vulnerable API endpoints"
      priority: 2

    - action: "Enable enhanced logging"
      description: "Capture all queries for forensic analysis"
      priority: 3

  short_term:
    - action: "Patch vulnerable code"
      description: "Replace vulnerable queries with parameterized versions"

    - action: "Deploy fixes to production"
      description: "Emergency release with security patches"

    - action: "Reset compromised credentials"
      description: "Rotate database passwords, API keys"

  investigation:
    - action: "Analyze access logs"
      description: "Identify attack timeline and scope"

    - action: "Check for data exfiltration"
      description: "Review what data was accessed/modified"

    - action: "Assess lateral movement"
      description: "Check if attacker accessed other systems"

  long_term:
    - action: "Implement WAF rules"
      description: "Deploy ModSecurity or cloud WAF"

    - action: "Security code review"
      description: "Review all database interactions"

    - action: "Penetration testing"
      description: "Hire external security firm"

    - action: "Developer training"
      description: "Secure coding practices workshop"

  compliance:
    - action: "Data breach notification"
      condition: "If PII was exposed"
      deadline: "72 hours (GDPR)"

    - action: "Regulatory reporting"
      condition: "If required by industry regulations"
```

---

## Лучшие практики

1. **Всегда используй parameterized queries** — это единственный надёжный способ
2. **Валидируй input на стороне сервера** — client-side validation недостаточно
3. **Применяй принцип минимальных привилегий** для database users
4. **Используй ORM** где возможно — они автоматически параметризуют запросы
5. **Регулярно тестируй** с SQLMap и другими инструментами (только в dev/staging!)
6. **Мониторь логи** на подозрительные паттерны
7. **Внедри WAF** как дополнительный слой защиты
8. **Обучай разработчиков** secure coding practices
