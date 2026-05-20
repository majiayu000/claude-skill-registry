---
name: database-query-best-practices
description: Prevent connection pool exhaustion when querying Railway PostgreSQL database. Use when (1) Running database queries from local environment, (2) Diagnosing "too many clients" errors, (3) Writing Python scripts that query production DB, (4) Checking connection pool status. CRITICAL - Always close connections immediately after use, use context managers, check pool status before queries.
---

# Database Query Best Practices - Prevent Connection Pool Exhaustion

**CRITICAL SKILL - READ THIS BEFORE QUERYING RAILWAY DATABASE**

## The Problem

When querying Railway production database from local development environment, you may encounter:
```
psycopg2.OperationalError: sorry, too many clients already
```

This happens when:
- Multiple local dev servers are running (`npm run dev`, `npm run develop`)
- Each dev server holds database connections open
- Connection pool limit is reached (300 total connections)
- No new connections can be established

## ALWAYS Use This Approach

### 1. Check Connection Pool Status FIRST

**Before ANY database query, check active connections:**

```bash
python3 << 'EOF'
import psycopg2

DATABASE_URL = "postgresql://postgres:password@host:port/railway"

try:
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
    cur = conn.cursor()

    # Check active connections
    cur.execute("""
        SELECT count(*)
        FROM pg_stat_activity
        WHERE datname = 'railway'
    """)
    active = cur.fetchone()[0]

    # Check pool limit
    cur.execute("SHOW max_connections")
    max_conn = cur.fetchone()[0]

    print(f"Active connections: {active}/{max_conn}")

    if active > int(max_conn) * 0.9:
        print(f"WARNING: Connection pool at {(active/int(max_conn))*100:.1f}% capacity")
        print("Consider closing dev servers before querying")
    else:
        print("Connection pool healthy - safe to query")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Cannot connect: {e}")
    print("\nSOLUTION:")
    print("1. Kill local dev servers: pkill -9 -f 'npm run dev'")
    print("2. Wait 30 seconds for connections to close")
    print("3. Try again")
EOF
```

### 2. Always Use Context Managers

**NEVER do this:**
```python
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute("SELECT * FROM users")
# Forgot to close! Connection leak!
```

**ALWAYS do this:**
```python
import psycopg2

DATABASE_URL = "postgresql://..."

try:
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=30)
    cur = conn.cursor()

    # Do your queries
    cur.execute("SELECT * FROM users")
    results = cur.fetchall()

    # Process results...

finally:
    # ALWAYS close in finally block
    if cur:
        cur.close()
    if conn:
        conn.close()
```

### 3. Use Short-Lived Connections

**For one-off queries, open connection, query, close immediately:**

```python
def get_user_count():
    """Get user count - connection opened and closed in function"""
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=30)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM users")
        count = cur.fetchone()[0]

        cur.close()
        return count

    finally:
        if conn:
            conn.close()  # Connection immediately released

# Good: Connection closed after function returns
user_count = get_user_count()
```

### 4. Kill Dev Servers Before Queries

**If you need to run database queries, stop dev servers first:**

```bash
# Stop all dev servers
pkill -9 -f "npm run dev"
pkill -9 -f "npm run develop"

# Wait for connections to close
sleep 10

# Now safe to query
python3 scripts/your_query_script.py

# Restart dev servers after
cd src/backend && npm run dev &
cd AINative-website && npm run dev &
```

### 5. Use Railway CLI for Quick Queries (RECOMMENDED)

**Instead of Python scripts, use Railway CLI when possible:**

```bash
# Login to Railway
railway login

# Link to project
railway link

# Run SQL query directly
railway run psql -c "SELECT COUNT(*) FROM users WHERE created_at >= NOW() - INTERVAL '30 days'"
```

This uses Railway's managed connections and doesn't consume local pool.

## Emergency: Connection Pool Full

**If you encounter "too many clients already":**

### Option 1: Kill Local Dev Servers
```bash
pkill -9 -f "npm run dev"
pkill -9 -f "npm run develop"
pkill -9 node
sleep 30  # Wait for DB connections to close
```

### Option 2: Check Active Connections on Railway

```bash
railway run psql -c "
SELECT
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start
FROM pg_stat_activity
WHERE datname = 'railway'
ORDER BY query_start DESC
LIMIT 20"
```

### Option 3: Terminate Idle Connections (LAST RESORT)

```bash
railway run psql -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'railway'
  AND state = 'idle'
  AND query_start < NOW() - INTERVAL '10 minutes'"
```

## Pre-Query Checklist

Before running ANY database query, verify:

- [ ] Are local dev servers running? → Stop them first
- [ ] Is connection pool healthy? → Run connection check
- [ ] Using try/finally to close connections? → Yes
- [ ] Using short-lived connections? → Yes
- [ ] Can I use Railway CLI instead? → Prefer this

## Summary

**The Golden Rule:**
> **ALWAYS close database connections immediately after use.**
> **NEVER leave connections open in dev servers during queries.**

**Best Approach:**
1. Stop dev servers
2. Query database
3. Close connection
4. Restart dev servers

**Even Better:**
Use Railway CLI for ad-hoc queries instead of Python scripts.
