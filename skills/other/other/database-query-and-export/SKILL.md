---
name: database-query-and-export
description: "Query SQLite, PostgreSQL, and MySQL databases and export results to CSV/JSON. Use when: (1) Extracting data for reports, (2) Database backup and migration, (3) Data analysis workflows, or (4) Automated database queries."
---

# Database Query and Export

Query relational databases (SQLite, PostgreSQL, MySQL) and export results to CSV, JSON, or other formats. Essential for data extraction, reporting, backup automation, and analytics pipelines.

## When to use

- Use case 1: When the user asks to query a database and export results
- Use case 2: When you need to extract data for analysis or reporting
- Use case 3: For backup and data migration workflows
- Use case 4: When building automated database monitoring and alerts

## Required tools / APIs

- **SQLite** — Lightweight file-based database (often pre-installed)
- **PostgreSQL client** — For PostgreSQL databases
- **MySQL client** — For MySQL/MariaDB databases
- No external API required

Install options:

```bash
# Ubuntu/Debian
sudo apt-get install -y sqlite3 postgresql-client mysql-client

# macOS
brew install sqlite3 postgresql mysql-client

# Node.js (database drivers)
npm install better-sqlite3  # SQLite
npm install pg              # PostgreSQL
npm install mysql2          # MySQL
```

## Skills

### query_sqlite_to_json

Query SQLite database and export to JSON format.

```bash
# Basic query to JSON
sqlite3 database.db "SELECT * FROM users LIMIT 10;" -json

# With pretty formatting using jq
sqlite3 database.db "SELECT * FROM users WHERE active=1;" -json | jq '.'

# Export entire table to JSON file
sqlite3 database.db "SELECT * FROM orders;" -json > orders.json

# Query with WHERE clause
sqlite3 database.db "SELECT id, name, email FROM users WHERE created_at > '2024-01-01';" -json
```

**Node.js:**

```javascript
const Database = require('better-sqlite3');

function querySQLiteToJSON(dbPath, query) {
  const db = new Database(dbPath, { readonly: true });
  const rows = db.prepare(query).all();
  db.close();
  return rows;
}

// Usage
// const users = querySQLiteToJSON('./database.db', 'SELECT * FROM users LIMIT 10');
// console.log(JSON.stringify(users, null, 2));
```

### query_sqlite_to_csv

Query SQLite database and export to CSV format.

```bash
# Basic query to CSV
sqlite3 database.db <<EOF
.mode csv
.headers on
SELECT * FROM users LIMIT 10;
EOF

# Export to CSV file
sqlite3 database.db <<EOF
.mode csv
.headers on
.output users.csv
SELECT id, name, email, created_at FROM users WHERE active=1;
EOF

# Query multiple tables with JOIN
sqlite3 database.db <<EOF
.mode csv
.headers on
SELECT u.name, o.order_id, o.total 
FROM users u 
JOIN orders o ON u.id = o.user_id 
WHERE o.created_at > '2024-01-01';
EOF
```

**Node.js:**

```javascript
const Database = require('better-sqlite3');
const fs = require('fs');

function querySQLiteToCSV(dbPath, query, outputPath) {
  const db = new Database(dbPath, { readonly: true });
  const rows = db.prepare(query).all();
  db.close();
  
  if (rows.length === 0) {
    return 'No results';
  }
  
  // Generate CSV
  const headers = Object.keys(rows[0]).join(',');
  const csvRows = rows.map(row => 
    Object.values(row).map(val => 
      typeof val === 'string' && val.includes(',') ? `"${val}"` : val
    ).join(',')
  );
  
  const csv = [headers, ...csvRows].join('\n');
  
  if (outputPath) {
    fs.writeFileSync(outputPath, csv);
    return `Exported ${rows.length} rows to ${outputPath}`;
  }
  
  return csv;
}

// Usage
// querySQLiteToCSV('./database.db', 'SELECT * FROM users LIMIT 10', './users.csv');
```

### query_postgresql

Query PostgreSQL database and export results.

```bash
# Set connection string (alternative: use individual flags)
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=mydb
export PGUSER=postgres
export PGPASSWORD=mypassword

# Query to JSON (using psql with formatted output)
psql -t -A -F"," -c "SELECT row_to_json(t) FROM (SELECT * FROM users LIMIT 10) t;"

# Query to CSV
psql -c "COPY (SELECT * FROM users WHERE active=true) TO STDOUT WITH CSV HEADER;" > users.csv

# Query with connection string
psql "postgresql://user:password@localhost:5432/mydb" -c "SELECT * FROM users LIMIT 5;"

# Query to formatted table
psql -c "SELECT id, name, email FROM users ORDER BY created_at DESC LIMIT 10;"
```

**Node.js:**

```javascript
const { Pool } = require('pg');

async function queryPostgreSQL(connectionString, query) {
  const pool = new Pool({ connectionString });
  
  try {
    const result = await pool.query(query);
    return result.rows;
  } finally {
    await pool.end();
  }
}

// Usage
// const connStr = 'postgresql://user:password@localhost:5432/mydb';
// queryPostgreSQL(connStr, 'SELECT * FROM users LIMIT 10')
//   .then(rows => console.log(JSON.stringify(rows, null, 2)));
```

### query_mysql

Query MySQL/MariaDB database and export results.

```bash
# Query to CSV with headers
mysql -h localhost -u root -p'mypassword' -D mydb \
  -e "SELECT * FROM users WHERE active=1;" \
  --batch --silent \
  | cat > users.csv

# Query to JSON-like format (requires jq for proper formatting)
mysql -h localhost -u root -p'mypassword' -D mydb \
  -e "SELECT * FROM users LIMIT 10;" \
  --batch --silent

# Export entire table to CSV
mysql -h localhost -u root -p'mypassword' -D mydb \
  -e "SELECT * FROM orders INTO OUTFILE '/tmp/orders.csv' 
      FIELDS TERMINATED BY ',' 
      ENCLOSED BY '\"' 
      LINES TERMINATED BY '\n';"

# Query with timeout
mysql -h localhost -u root -p'mypassword' -D mydb \
  --connect-timeout=10 \
  -e "SELECT COUNT(*) as total FROM users;"
```

**Node.js:**

```javascript
const mysql = require('mysql2/promise');

async function queryMySQL(config, query) {
  const connection = await mysql.createConnection({
    host: config.host || 'localhost',
    user: config.user,
    password: config.password,
    database: config.database,
    connectTimeout: 10000
  });
  
  try {
    const [rows] = await connection.execute(query);
    return rows;
  } finally {
    await connection.end();
  }
}

// Usage
// const config = {
//   host: 'localhost',
//   user: 'root',
//   password: 'mypassword',
//   database: 'mydb'
// };
// queryMySQL(config, 'SELECT * FROM users LIMIT 10')
//   .then(rows => console.log(JSON.stringify(rows, null, 2)));
```

### advanced_sqlite_export_with_error_handling

Production-ready SQLite export with validation and error handling.

```bash
#!/bin/bash
DB_PATH="database.db"
QUERY="SELECT * FROM users WHERE active=1;"
OUTPUT_FILE="users.csv"

# Check if database exists
if [ ! -f "$DB_PATH" ]; then
  echo "Error: Database file not found: $DB_PATH" >&2
  exit 1
fi

# Check if table exists
if ! sqlite3 "$DB_PATH" "SELECT name FROM sqlite_master WHERE type='table' AND name='users';" | grep -q "users"; then
  echo "Error: Table 'users' not found in database" >&2
  exit 1
fi

# Execute query and export to CSV
if sqlite3 "$DB_PATH" <<EOF > "$OUTPUT_FILE" 2>&1
.mode csv
.headers on
$QUERY
EOF
then
  ROW_COUNT=$(wc -l < "$OUTPUT_FILE")
  echo "Success: Exported $((ROW_COUNT - 1)) rows to $OUTPUT_FILE"
else
  echo "Error: Query failed" >&2
  exit 1
fi
```

**Node.js:**

```javascript
const Database = require('better-sqlite3');
const fs = require('fs');

async function exportSQLiteWithValidation(options) {
  const { dbPath, query, outputPath, format = 'json' } = options;
  
  // Validate database exists
  if (!fs.existsSync(dbPath)) {
    throw new Error(`Database file not found: ${dbPath}`);
  }
  
  let db;
  try {
    db = new Database(dbPath, { readonly: true, timeout: 10000 });
    
    // Prepare and execute query
    const stmt = db.prepare(query);
    const rows = stmt.all();
    
    if (rows.length === 0) {
      return { success: true, rowCount: 0, message: 'No rows returned' };
    }
    
    // Export based on format
    let output;
    if (format === 'json') {
      output = JSON.stringify(rows, null, 2);
    } else if (format === 'csv') {
      const headers = Object.keys(rows[0]).join(',');
      const csvRows = rows.map(row => 
        Object.values(row).map(val => 
          typeof val === 'string' && val.includes(',') ? `"${val.replace(/"/g, '""')}"` : val
        ).join(',')
      );
      output = [headers, ...csvRows].join('\n');
    } else {
      throw new Error(`Unsupported format: ${format}`);
    }
    
    // Write to file
    fs.writeFileSync(outputPath, output);
    
    return {
      success: true,
      rowCount: rows.length,
      outputPath,
      format,
      message: `Exported ${rows.length} rows to ${outputPath}`
    };
    
  } catch (err) {
    throw new Error(`Database export failed: ${err.message}`);
  } finally {
    if (db) db.close();
  }
}

// Usage
// exportSQLiteWithValidation({
//   dbPath: './database.db',
//   query: 'SELECT * FROM users WHERE active=1',
//   outputPath: './users.json',
//   format: 'json'
// }).then(result => console.log(result));
```

## Rate limits / Best practices

- ✅ **Use readonly connections** — Open databases in readonly mode when only querying
- ✅ **Set connection timeouts** — Use 10-30 second timeouts to prevent hanging
- ✅ **Validate inputs** — Check that database files/tables exist before querying
- ✅ **Escape user inputs** — Use parameterized queries to prevent SQL injection
- ✅ **Handle large datasets** — Use LIMIT/OFFSET for pagination on large tables
- ✅ **Close connections** — Always close database connections after queries
- ⚠️ **Secure credentials** — Store database passwords in environment variables, never hardcode
- ⚠️ **Export file permissions** — Ensure export directories have proper write permissions

## Agent prompt

```text
You have database query and export capability. When a user asks to query a database:

1. Identify the database type (SQLite, PostgreSQL, MySQL) from:
   - File extension (.db, .sqlite, .sqlite3 = SQLite)
   - Connection string (postgresql://, mysql://)
   - User specification

2. For SQLite:
   - Use `sqlite3 database.db "QUERY" -json` for JSON output
   - Use `.mode csv` with `.headers on` for CSV output
   - Always check if the database file exists first

3. For PostgreSQL:
   - Use `psql` with connection string or environment variables
   - Use `COPY ... TO STDOUT WITH CSV HEADER` for CSV export
   - Export JSON using `row_to_json()` function

4. For MySQL:
   - Use `mysql` with `-e` flag for queries
   - Use `--batch --silent` for CSV-like output
   - Set connection timeout with `--connect-timeout=10`

5. Always:
   - Validate database/table exists before querying
   - Use readonly connections when only reading
   - Handle errors gracefully with clear messages
   - Sanitize outputs (escape commas in CSV, quote strings)

6. For large datasets:
   - Add LIMIT clause to queries
   - Use pagination with OFFSET for very large tables
   - Warn user if result set is likely to be huge
```

## Troubleshooting

**Error: "unable to open database file"**
- Symptom: SQLite cannot find or access the database file
- Solution: Check file path is correct and file has read permissions

**Error: "connection refused"**
- Symptom: Cannot connect to PostgreSQL or MySQL server
- Solution: Verify host/port are correct, database service is running, and firewall allows connections

**Error: "authentication failed"**
- Symptom: Database rejects username/password
- Solution: Verify credentials are correct, user has necessary privileges

**Error: "table does not exist"**
- Symptom: Query references non-existent table
- Solution: List available tables first (`sqlite3 db.db ".tables"` or `\dt` in psql)

**CSV output has broken formatting:**
- Symptom: Commas in data break CSV columns
- Solution: Properly escape values with commas using quotes, escape existing quotes

**Query takes too long:**
- Symptom: Query hangs or runs for minutes
- Solution: Add LIMIT clause, optimize query with indexes, increase timeout

## See also

- [../json-and-csv-data-transformation/SKILL.md](../json-and-csv-data-transformation/SKILL.md) — Transform exported data between formats
- [../file-tracker/SKILL.md](../file-tracker/SKILL.md) — Track database file changes over time
- [../chat-logger/SKILL.md](../chat-logger/SKILL.md) — Example of SQLite usage for logging
