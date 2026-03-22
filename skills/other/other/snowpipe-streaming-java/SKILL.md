---
name: snowpipe-streaming-java
description: "Stream data into Snowflake using the Java Snowpipe Streaming SDK. Use for: setting up RSA auth, building the JAR, running single or parallel streaming, JVM Arrow flags, troubleshooting. Triggers: java streaming, snowpipe java, stream data java, parallel streaming java, streaming SDK java, maven streaming, stream orders java."
---

# Snowpipe Streaming — Java SDK

Stream synthetic e-commerce data (orders + order items) into Snowflake using the Java Snowpipe Streaming SDK (`com.snowflake:snowpipe-streaming:1.1.2`).

## When to Use

- User wants to stream data into Snowflake using Java
- User mentions Java Snowpipe Streaming SDK, Maven streaming, or JVM-based ingestion
- User needs to set up RSA key-pair auth for Java streaming
- User wants to run single or parallel streaming instances with Java
- User needs to troubleshoot JWT, Arrow, or permission errors with the Java SDK

## Tools Used

- `bash` — Build JAR (`mvn clean package`), run streaming, generate RSA keys
- `snowflake_sql_execute` — Create databases, schemas, tables (when CoCo connection matches target)
- `ask_user_question` — Confirm target objects, get approval at checkpoints
- `read` / `write` / `edit` — Configure profile.json and config.properties

## Stopping Points

- ✋ Phase 0: User approves the workflow before any action
- ✋ Step 1: User confirms Snowflake target objects (database, schema, tables, role)
- ✋ Step 2: Java 21+ and Maven verified (or installed)
- ✋ Step 3: RSA public key registered with Snowflake user
- ✋ Step 5: profile.json and config.properties correctly configured
- ✋ Step 8: Confirm data landed in Snowflake

---

## Phase 0: Briefing & Consent

**Goal:** Explain what this skill does and get explicit user approval before executing anything.

**⚠️ STOP:** This phase MUST be completed before ANY other action. Do not run any commands, read any files, or execute any tools until the user approves.

Present the following briefing to the user:

> ### Snowpipe Streaming (Java) — What This Skill Does
>
> **Snowpipe Streaming** is Snowflake's real-time data ingestion API. Instead of staging files and loading them in batches, it streams rows directly into tables with sub-second latency. This skill uses the **Java SDK** (`com.snowflake:snowpipe-streaming:1.1.2`) backed by a Rust engine.
>
> **What will happen (8 steps):**
>
> 1. **Gather target details** — confirm which Snowflake account, database, schema, tables, and role to use
> 2. **Check prerequisites** — verify Java 21+ and Maven are installed
> 3. **RSA key setup** — generate a new key pair (or reuse existing `*.p8` file) and register the public key
> 4. **Create Snowflake objects** — create the target database, schema, and tables (owned by your role)
> 5. **Configure** — fill in `profile.json` and `config.properties` with your Snowflake details
> 6. **Build the JAR** — run `mvn clean package` to produce a shaded uber-jar
> 7. **Run streaming** — stream synthetic e-commerce orders + order items into Snowflake
> 8. **Verify data** — query row counts after ingestion completes
>
> **What this skill will NOT do:**
> - Drop or alter any existing objects not created by this workflow
> - Modify files outside the project directory
> - Run anything without showing you the exact command first
> - Continue past any checkpoint without your explicit approval
>
> **Authentication:** Uses RSA key-pair auth (not password). A new key pair will be generated and the public key registered with your Snowflake user via `ALTER USER`.
>
> **JVM requirement:** Java 21+ is required. The SDK uses Apache Arrow internally, which needs `--add-opens=java.base/java.nio=ALL-UNNAMED` (pre-configured in `.mvn/jvm.config`).

Ask the user: **"Shall I proceed with Step 1 (Gather Target Details)?"**

**⚠️ STOP:** Do NOT proceed until the user confirms.

---

## Workflow

### Step 1: Propose Target Objects

Confirm the Snowflake objects with the user. Propose defaults and let them override:

| Object | Default | Notes |
|--------|---------|-------|
| **User** | *(current Snowflake user)* | The Snowflake user that has the RSA public key registered |
| **Role** | `ACCOUNTADMIN` | Must **own** the target DB/schema/tables — not just have grants |
| **Database** | `SNOWPIPE_STREAMING_DEMO` | Will be created if it doesn't exist |
| **Schema** | `STAGING` | Use `RAW` for production |
| **Orders table** | `ORDERS` | Receives streamed order rows |
| **Order items table** | `ORDER_ITEMS` | Receives streamed item rows |
| **Warehouse** | `COMPUTE_WH` | Any X-Small is fine |

**⚠️ STOP:** Ask the user to confirm or change these before proceeding.

**Table ownership**: The streaming SDK's role **must own** the target database, schema, and tables. `GRANT USAGE` or `GRANT ALL` is **not sufficient** — the SDK's internal pipe-info API returns `ERR_TABLE_DOES_NOT_EXIST_NOT_AUTHORIZED` if the role doesn't own the objects.

---

### Step 2: Prerequisites Check

1. Check Java 21+ is installed: `java --version`
2. Check Maven is installed: `mvn --version`
3. Look for existing project files — the Java code may already exist from a previous session. Check for `pom.xml` and `src/main/java/` in the working directory.
4. If no project exists, create it from scratch (see **Project Structure** at the bottom).

All Java dependencies (streaming SDK, JDBC driver, Jackson, SLF4J) are declared in `pom.xml` and resolved automatically by `mvn clean package`.

**⚠️ STOP:** If Java < 21 or Maven is missing, help the user install them:
- **Java**: `brew install openjdk@21` (macOS)
- **Maven**: `brew install maven` (macOS)

---

### Step 3: RSA Key-Pair Setup

Skip if keys already exist (look for `*.p8` files in the project).

```bash
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out streaming_key.p8 -nocrypt
openssl rsa -in streaming_key.p8 -pubout -out streaming_key.pub
```

Register in Snowflake:
```sql
ALTER USER <username> SET RSA_PUBLIC_KEY='<contents of .pub without header/footer>';
```

**⚠️ STOP:** Key must be registered before continuing.

**Critical**:
- Private key must be **PKCS8 unencrypted** (BEGIN PRIVATE KEY, not BEGIN RSA PRIVATE KEY)
- Role **must** be specified in the profile — the SDK does not default to any role

**Cross-account key registration**: If the target is a different account from the CoCo connection, either:
1. Add a key-pair auth connection to the target account and use it
2. Have the user run ALTER USER directly in Snowsight for the target account

---

### Step 4: Create Snowflake Objects

**CoCo connection vs streaming profile**: The Cortex Code SQL connection may route to a **different account or user** than the streaming target. If so, you **cannot** create tables via the CoCo SQL tool.

**If CoCo connection matches the streaming target account + role**, use SQL directly:
```sql
CREATE DATABASE IF NOT EXISTS <DATABASE>;
CREATE SCHEMA IF NOT EXISTS <DATABASE>.<SCHEMA>;
CREATE TABLE IF NOT EXISTS <DATABASE>.<SCHEMA>.ORDERS (
    ORDER_ID VARCHAR(36), CUSTOMER_ID NUMBER(38,0), ORDER_DATE TIMESTAMP_NTZ,
    ORDER_STATUS VARCHAR(20), TOTAL_AMOUNT FLOAT, DISCOUNT_PERCENT FLOAT, SHIPPING_COST FLOAT);
CREATE TABLE IF NOT EXISTS <DATABASE>.<SCHEMA>.ORDER_ITEMS (
    ORDER_ITEM_ID VARCHAR(36), ORDER_ID VARCHAR(36), PRODUCT_ID NUMBER,
    PRODUCT_NAME VARCHAR, PRODUCT_CATEGORY VARCHAR, QUANTITY NUMBER,
    UNIT_PRICE FLOAT, LINE_TOTAL FLOAT);
```

**If CoCo connection differs**, write and run a temporary Python setup script:
```python
import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

with open("streaming_key.p8", "rb") as f:
    p_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())
pkb = p_key.private_bytes(encoding=serialization.Encoding.DER, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())

conn = snowflake.connector.connect(user="<USER>", account="<ACCOUNT>", private_key=pkb, role="<ROLE>", warehouse="<WAREHOUSE>")
cursor = conn.cursor()
for stmt in [
    "CREATE DATABASE IF NOT EXISTS <DATABASE>",
    "CREATE SCHEMA IF NOT EXISTS <DATABASE>.<SCHEMA>",
    "CREATE TABLE IF NOT EXISTS <DATABASE>.<SCHEMA>.ORDERS (ORDER_ID VARCHAR(36), CUSTOMER_ID NUMBER(38,0), ORDER_DATE TIMESTAMP_NTZ, ORDER_STATUS VARCHAR(20), TOTAL_AMOUNT FLOAT, DISCOUNT_PERCENT FLOAT, SHIPPING_COST FLOAT)",
    "CREATE TABLE IF NOT EXISTS <DATABASE>.<SCHEMA>.ORDER_ITEMS (ORDER_ITEM_ID VARCHAR(36), ORDER_ID VARCHAR(36), PRODUCT_ID NUMBER, PRODUCT_NAME VARCHAR, PRODUCT_CATEGORY VARCHAR, QUANTITY NUMBER, UNIT_PRICE FLOAT, LINE_TOTAL FLOAT)",
]:
    cursor.execute(stmt)
    print(cursor.fetchone()[0])
cursor.close(); conn.close()
```

Streaming pipes are auto-created by Snowflake with the naming convention `<TABLE_NAME>-STREAMING`.

---

### Step 5: Configure Profile and Properties

Create `profile.json` with the user's confirmed values from Step 1:

```json
{
  "user": "<USER>",
  "account": "<ACCOUNT>",
  "url": "https://<ACCOUNT>.snowflakecomputing.com:443",
  "role": "<ROLE>",
  "private_key_file": "../streaming_key.p8",
  "database": "<DATABASE>",
  "schema": "<SCHEMA>",
  "warehouse": "<WAREHOUSE>"
}
```

Create `config.properties`:

```properties
channel.orders.name=orders_channel
channel.order_items.name=order_items_channel
pipe.orders.name=<ORDERS_TABLE>-STREAMING
pipe.order_items.name=<ORDER_ITEMS_TABLE>-STREAMING
max.client.lag=60
batch.size=1000
orders.batch.size=10000
num.orders.per.batch=100
max.retries=3
retry.delay.ms=1000
```

**Profile supports two key formats**:
- `"private_key_file"`: Path to .p8 file (relative to the java/ directory). **Preferred.**
- `"private_key"`: Inline PEM string with `\n` newlines.

**⚠️ STOP:** Confirm profile and config files are created and populated before continuing.

---

### Step 6: Build the JAR

```bash
mvn clean package -q
```

Produces: `target/snowpipe-streaming-app-1.0.0.jar` (shaded uber-jar).

**CRITICAL JVM flag** for Arrow memory compatibility:
```
--add-opens=java.base/java.nio=ALL-UNNAMED
```
Pre-configured in `.mvn/jvm.config`. Must be added manually when running `java -cp` directly.

**If error occurs:**
- Compilation error → check Java version is 21+ (`java --version`)
- Dependency download failure → check network connectivity and Maven settings
- `shade plugin` error → run `mvn clean package` (not just `mvn package`)

---

### Step 7: Run Streaming

**Customer IDs are generated synthetically (1-10000)**. No database lookup or CUSTOMERS table needed.

**Single instance** (1K-50K orders):
```bash
java --add-opens=java.base/java.nio=ALL-UNNAMED \
  -cp target/snowpipe-streaming-app-1.0.0.jar \
  com.snowflake.demo.StreamingApp <num_orders> <config_file> <profile_file>
```

**Parallel** (10K+ orders, recommended):
```bash
java --add-opens=java.base/java.nio=ALL-UNNAMED \
  -cp target/snowpipe-streaming-app-1.0.0.jar \
  com.snowflake.demo.ParallelStreamingOrchestrator <total_orders> <num_instances> [config_file] [profile_file]
```

Examples:
```bash
# 10K orders, 5 instances
java --add-opens=java.base/java.nio=ALL-UNNAMED \
  -cp target/snowpipe-streaming-app-1.0.0.jar \
  com.snowflake.demo.ParallelStreamingOrchestrator 10000 5 config.properties profile.json
```

Use `run_in_background=true` in the Bash tool for long runs.

**If error occurs:**
- `InaccessibleObjectException` → missing `--add-opens` JVM flag
- `ClassNotFoundException` → use `-cp` (not `-jar`) with full class name
- `ERR_TABLE_DOES_NOT_EXIST_NOT_AUTHORIZED` → role doesn't own tables (see Troubleshooting)
- JWT / auth errors → check profile.json account format and key registration

**Parallel details**:
- Each instance gets unique channels: `orders_channel_instance_0`, etc.
- Customer ID range (1-10000) is partitioned across instances
- Config/profile are CLI args 3 and 4

---

### Step 8: Verify Data

After the run completes, the app waits 65 seconds for flush then runs reconciliation.

Data may take **1-3+ minutes** to appear in queries after completion. If COUNT returns 0, **wait 2-3 minutes and retry**.

```sql
SELECT COUNT(*) FROM <DATABASE>.<SCHEMA>.ORDERS;
SELECT COUNT(*) FROM <DATABASE>.<SCHEMA>.ORDER_ITEMS;
```

Expected ratio: ~3-4 order items per order.

**Known issue**: Reconciliation uses JDBC which may fail with org-account format. This is non-critical — data is already ingested. Just verify counts manually.

**⚠️ STOP:** Confirm data landed successfully.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| JWT auth error (390144) | Wrong account format or key not registered | Use hyphens in account, register public key via ALTER USER, use unencrypted PKCS8 |
| `ERR_TABLE_DOES_NOT_EXIST_NOT_AUTHORIZED` | SDK role doesn't **own** the target DB/schema/tables | Recreate objects using the same role specified in profile.json. `GRANT USAGE`/`GRANT ALL` is not enough — the role must own the objects. |
| Arrow / `InaccessibleObjectException` | Missing JVM flag | Add `--add-opens=java.base/java.nio=ALL-UNNAMED` |
| `ClassNotFoundException` | Wrong jar name or `-jar` instead of `-cp` | Use `-cp target/<jar>.jar` with full class name |
| JDBC `Schema does not exist` in reconciliation | JDBC properties unreliable with org-account format | Non-critical — data already ingested. Verify counts manually. |
| ReceiverSaturated / HTTP 429 | Backpressure | Built-in exponential backoff handles it |
| Data not visible after run | Streaming visibility delay | Wait 2-3 minutes, then re-query |

---

## First-Time / Trial Account Setup

Skip this section if the user already has Cortex Code and a Snowflake connection configured.

### Install Cortex Code
```bash
brew install Snowflake-Labs/cortex-code/cortex
# or: npm install -g @snowflake-labs/cortex-code
```

### Set Up Snowflake Connection

If the streaming target is a **different account** from the user's current Cortex Code session, use **key-pair auth** (not `externalbrowser`).

```toml
[streaming]
account = "orgname-accountname"
user = "YOUR_USERNAME"
authenticator = "SNOWFLAKE_JWT"
private_key_file = "/absolute/path/to/key.p8"
host = "orgname-accountname.snowflakecomputing.com"
database = "<DATABASE>"
schema = "<SCHEMA>"
warehouse = "<WAREHOUSE>"
role = "<ROLE>"
```

**Finding your account identifier**:
- Snowsight → click your name (bottom-left) → **Account** → copy the `orgname-accountname` value
- Uses **hyphens** not dots or underscores

Activate: `/connection streaming`

---

## Architecture Notes

- **Customer IDs are synthetic (1-10000)** — no database lookup. Matches Python implementation.
- **One SDK client per pipe/table** — separate clients for orders and order items.
- **Streaming SDK** uses `private_key` as PEM string. **JDBC** (reconciliation) uses parsed `PrivateKey` object — different formats.
- **Rust SDK backend** produces very verbose logs (`cyclone_shared`). Use filters when checking output.
- **Offset tokens** are strings: `order_{uuid}`, `item_{uuid}`.

## Project Structure

If creating from scratch, the project needs:

```
<project_root>/
├── java/
│   ├── pom.xml                                    # Maven build (Java 21, shade plugin)
│   ├── .mvn/jvm.config                            # --add-opens flag
│   ├── config.properties                          # Default config
│   ├── profile.json                               # Default credentials
│   └── src/main/java/com/snowflake/demo/
│       ├── StreamingApp.java                     # Single-instance entry point
│       ├── ParallelStreamingOrchestrator.java     # Multi-instance entry point
│       ├── SnowpipeStreamingManager.java          # SDK client/channel management
│       ├── ReconciliationManager.java             # Post-ingestion cleanup (JDBC)
│       ├── ConfigManager.java                     # Config + profile loader
│       ├── DataGenerator.java                     # Synthetic data generation
│       ├── Order.java                             # Order model with toMap()
│       ├── OrderItem.java                         # OrderItem model with toMap()
│       └── Customer.java                          # Customer model (unused for streaming)
├── streaming_key.p8                               # RSA private key
└── streaming_key.pub                              # RSA public key
```

## Output

- Java project directory with compiled uber-JAR, keys, and profiles
- Snowflake database/schema/tables created and owned by the specified role
- Synthetic e-commerce data (orders + order items) streamed into target tables
- Verified row counts confirming successful ingestion
