---
name: snowpipe-streaming-python
description: "Stream data into Snowflake using the Python Snowpipe Streaming SDK. Use for: setting up RSA auth, configuring profiles, running single or parallel streaming, staging vs production, reconciliation, troubleshooting JWT errors. Triggers: python streaming, snowpipe python, stream data python, parallel streaming python, streaming SDK python, stream orders python."
---

# Snowpipe Streaming — Python SDK

This skill is **self-contained**. All source code, configs, and dependencies are bundled. The agent's job is to **copy, configure, and run** — not to generate code from scratch.

## When to Use

- User wants to stream data into Snowflake in real-time using Python
- User mentions Snowpipe Streaming, the Python SDK, or real-time ingestion
- User needs to set up RSA key-pair auth for streaming
- User wants to run single or parallel streaming instances
- User needs to troubleshoot JWT, key, or permission errors with streaming

## Tools Used

- `bash` — Copy files, run setup.sh, execute streaming scripts
- `snowflake_sql_execute` — Create databases, schemas, tables (when CoCo connection matches target)
- `ask_user_question` — Confirm target objects, get approval at checkpoints
- `read` / `write` / `edit` — Configure profile.json and config.properties

## Bundled Files

```
snowpipe-streaming-python/
├── SKILL.md                        # This file (agent instructions)
├── LEARNINGS.md                    # Append-only log of run deviations and fixes
├── FEEDBACK_TEMPLATE.md            # Template for new learning entries
├── requirements.txt                # Python dependencies
├── .gitignore                      # Protects keys and credentials
├── setup.sh                        # Bootstrap: venv + deps + keys + config templates
├── profile.template.json           # Snowflake connection template
├── config.template.properties      # Streaming config template
└── src/
    ├── models.py                   # Customer, Order, OrderItem dataclasses
    ├── data_generator.py           # Synthetic e-commerce data (customer IDs 1-10000)
    ├── config_manager.py           # Loads .properties + profile JSON, resolves key files
    ├── snowpipe_streaming_manager.py  # SDK client/channel lifecycle + retry logic
    ├── reconciliation_manager.py   # Post-ingestion row count + orphan check
    ├── streaming_app.py            # Single-instance entry point
    └── parallel_streaming_orchestrator.py  # Multi-instance entry point
```

The skill base directory is available via the skill loader. Reference it as `SKILL_DIR` in instructions below.

## Stopping Points

- ✋ Phase 0: User approves the workflow before any action
- ✋ Step 1: User confirms Snowflake target objects (database, schema, tables, role)
- ✋ Step 3: RSA public key registered with Snowflake user (if new key generated)
- ✋ Step 4: profile.json correctly configured before proceeding
- ✋ Step 7: Confirm data landed in Snowflake

---

## Phase 0: Briefing & Consent

**Goal:** Explain what this skill does and get explicit user approval before executing anything.

**⚠️ STOP:** This phase MUST be completed before ANY other action. Do not run any commands, read any files, or execute any tools until the user approves.

Present the following briefing to the user:

> ### Snowpipe Streaming (Python) — What This Skill Does
>
> **Snowpipe Streaming** is Snowflake's real-time data ingestion API. Instead of staging files and loading them in batches, it streams rows directly into tables with sub-second latency. This skill uses the **Python SDK** (`snowflake.ingest.streaming`, v1.2.0+) backed by a Rust engine.
>
> The skill is **self-contained** — all source code, configs, and dependencies are bundled. The agent's job is to copy, configure, and run — not generate code from scratch.
>
> **What will happen (7 steps):**
>
> 1. **Gather target details** — confirm which Snowflake account, database, schema, tables, and role to use
> 2. **Copy project files** — copy bundled source code, configs, and requirements to a project directory
> 3. **Bootstrap environment** — run `setup.sh` to create venv, install deps, generate RSA keys
> 4. **Configure** — fill in `profile.json` and `config.properties` with your Snowflake details
> 5. **Create Snowflake objects** — create the target database, schema, and tables (owned by your role)
> 6. **Run streaming** — stream synthetic e-commerce orders + order items into Snowflake
> 7. **Verify data** — query row counts after ingestion completes
>
> **What this skill will NOT do:**
> - Drop or alter any existing objects not created by this workflow
> - Modify files outside the project directory
> - Run anything without showing you the exact command first
> - Continue past any checkpoint without your explicit approval
>
> **Authentication:** Uses RSA key-pair auth (not password). A new key pair will be generated and the public key registered with your Snowflake user via `ALTER USER`.

Ask the user: **"Shall I proceed with Step 1 (Gather Target Details)?"**

**⚠️ STOP:** Do NOT proceed until the user confirms.

---

## Workflow

> **Pre-flight**: Before starting, read `LEARNINGS.md` in the skill directory. If there are **PENDING** entries, apply fixes to bundled files before copying them to the user's project. Update applied entries from `PENDING` to `APPLIED`.

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

### Step 2: Copy Project Files

Copy the entire skill directory to the user's desired project location:

```bash
SKILL_DIR="<path to snowpipe-streaming-python skill>"
PROJECT_DIR="<user's chosen project directory>"

mkdir -p "${PROJECT_DIR}"
cp -r "${SKILL_DIR}/src" "${PROJECT_DIR}/src"
cp "${SKILL_DIR}/requirements.txt" "${PROJECT_DIR}/"
cp "${SKILL_DIR}/setup.sh" "${PROJECT_DIR}/"
cp "${SKILL_DIR}/profile.template.json" "${PROJECT_DIR}/"
cp "${SKILL_DIR}/config.template.properties" "${PROJECT_DIR}/"
cp "${SKILL_DIR}/.gitignore" "${PROJECT_DIR}/"
```

Do **not** copy `SKILL.md` — it's agent instructions, not user-facing.

---

### Step 3: Bootstrap Environment

Run the setup script:

```bash
cd "${PROJECT_DIR}"
bash setup.sh
```

This will:
1. Create `.venv/` with a Python virtual environment
2. Install all packages from `requirements.txt`
3. Generate `streaming_key.p8` and `streaming_key.pub` (if not present)
4. Copy template configs to `profile.json` and `config.properties` (if not present)

If the user already has an RSA key (e.g., `rsa_key.p8`), copy or symlink it as `streaming_key.p8` before running setup, or update `profile.json` to point to the existing key path.

**If error occurs:**
- `pip` install failure → check Python version (3.8+ required) and network connectivity
- Key generation failure → ensure `openssl` is available on PATH

**⚠️ STOP:** If setup.sh generated a new key pair, the public key **must** be registered with the Snowflake user before continuing:

```sql
ALTER USER <username> SET RSA_PUBLIC_KEY='<contents of streaming_key.pub without header/footer>';
```

**Cross-account key registration**: If the target is a different account from the CoCo connection, either:
1. Add a key-pair auth connection to the target account and use it
2. Have the user run ALTER USER directly in Snowsight for the target account

---

### Step 4: Configure Profile and Properties

Edit `profile.json` with the user's confirmed values from Step 1:

```json
{
  "user": "<USER>",
  "account": "<ORG>-<ACCOUNT>",
  "url": "https://<ORG>-<ACCOUNT>.snowflakecomputing.com:443",
  "role": "<ROLE>",
  "private_key_file": "streaming_key.p8",
  "database": "<DATABASE>",
  "schema": "<SCHEMA>",
  "warehouse": "<WAREHOUSE>"
}
```

Edit `config.properties` if the user changed table names from defaults — update the pipe names:

```properties
pipe.orders.name=<ORDERS_TABLE>-STREAMING
pipe.order_items.name=<ORDER_ITEMS_TABLE>-STREAMING
```

Use `private_key_file` (path to .p8 file) instead of inline `private_key`. The bundled `config_manager.py` reads the file at runtime and passes the full PEM to the SDK.

**⚠️ STOP:** Confirm profile.json is correctly filled in before continuing.

---

### Step 5: Create Snowflake Objects

**CoCo connection vs streaming profile**: The Cortex Code SQL connection may route to a **different account or user** than the streaming target. If so, you **cannot** create tables via the CoCo SQL tool. Instead, use a Python script that connects via the streaming RSA key.

**If CoCo connection matches the streaming target account + role**, use SQL directly:
```sql
CREATE DATABASE IF NOT EXISTS <DATABASE>;
CREATE SCHEMA IF NOT EXISTS <DATABASE>.<SCHEMA>;
CREATE TABLE IF NOT EXISTS <DATABASE>.<SCHEMA>.ORDERS (ORDER_ID VARCHAR, CUSTOMER_ID VARCHAR, ORDER_DATE TIMESTAMP_NTZ, STATUS VARCHAR, TOTAL_AMOUNT NUMBER(12,2));
CREATE TABLE IF NOT EXISTS <DATABASE>.<SCHEMA>.ORDER_ITEMS (ORDER_ITEM_ID VARCHAR, ORDER_ID VARCHAR, PRODUCT_NAME VARCHAR, CATEGORY VARCHAR, QUANTITY NUMBER, UNIT_PRICE NUMBER(12,2), TOTAL_PRICE NUMBER(12,2));
```

**If CoCo connection differs**, write and run a temporary Python setup script using the project's venv:
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
    "CREATE TABLE IF NOT EXISTS <DATABASE>.<SCHEMA>.ORDERS (ORDER_ID VARCHAR, CUSTOMER_ID VARCHAR, ORDER_DATE TIMESTAMP_NTZ, STATUS VARCHAR, TOTAL_AMOUNT NUMBER(12,2))",
    "CREATE TABLE IF NOT EXISTS <DATABASE>.<SCHEMA>.ORDER_ITEMS (ORDER_ITEM_ID VARCHAR, ORDER_ID VARCHAR, PRODUCT_NAME VARCHAR, CATEGORY VARCHAR, QUANTITY NUMBER, UNIT_PRICE NUMBER(12,2), TOTAL_PRICE NUMBER(12,2))",
]:
    cursor.execute(stmt)
    print(cursor.fetchone()[0])
cursor.close(); conn.close()
```

Streaming pipes are auto-created by Snowflake with the naming convention `<TABLE_NAME>-STREAMING`.

---

### Step 6: Run Streaming

**Customer IDs are generated synthetically (1-10000)**. No database lookup or CUSTOMERS table needed.

All commands use the project venv Python: `.venv/bin/python`

**Single instance** (1K-50K orders):
```bash
.venv/bin/python src/streaming_app.py <num_orders> [config_file] [profile_file]
```

**Parallel** (10K+ orders, recommended):
```bash
.venv/bin/python src/parallel_streaming_orchestrator.py <total_orders> <num_instances> [config_file] [profile_file]
```

Examples:
```bash
# 1K orders, single instance
.venv/bin/python src/streaming_app.py 1000

# 10K orders, 5 parallel instances
.venv/bin/python src/parallel_streaming_orchestrator.py 10000 5

# 100K orders, 10 parallel instances, staging config
.venv/bin/python src/parallel_streaming_orchestrator.py 100000 10 config_staging.properties profile_staging.json
```

Use `run_in_background=true` in the Bash tool for long runs.

**If error occurs:**
- `ModuleNotFoundError` → use `.venv/bin/python`, not system Python
- `ERR_TABLE_DOES_NOT_EXIST_NOT_AUTHORIZED` → role doesn't own tables (see Troubleshooting)
- JWT / auth errors → check profile.json account format and key registration
- `ReceiverSaturated` / HTTP 429 → built-in backoff handles this, just wait

**Parallel details**:
- Each instance gets unique channels: `orders_channel_instance_0`, etc.
- Customer ID range (1-10000) is partitioned across instances
- Default batch: 10,000 orders per `append_rows` call
- Benchmark: 10K orders across 5 instances in ~12 seconds

---

### Step 7: Verify Data

The parallel orchestrator waits **65 seconds** after streaming before reconciliation. This prevents falsely detecting orphaned records.

```sql
SELECT COUNT(*) FROM <DATABASE>.<SCHEMA>.ORDERS;
SELECT COUNT(*) FROM <DATABASE>.<SCHEMA>.ORDER_ITEMS;
```

Expected ratio: ~3-4 order items per order.

Data may take **1-3 minutes** to become queryable after run completes. If COUNT returns 0, wait and retry.

**⚠️ STOP:** Confirm data landed successfully.

---

### Post-Run: Record Learnings

If the run had **any deviations** from what SKILL.md instructed (changed imports, added dependencies, modified configs, encountered undocumented errors), record them:

1. Read `FEEDBACK_TEMPLATE.md` for the entry format
2. Append an entry to `LEARNINGS.md` in the skill directory (not the user's project copy)
3. Set status to `PENDING` or `APPLIED` depending on whether you also patched the bundled files

If the run succeeded with no deviations, skip this — do not add a "no issues" entry.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'snowflake'` | Wrong Python binary | Use `.venv/bin/python`, not system Python |
| `ERR_TABLE_DOES_NOT_EXIST_NOT_AUTHORIZED` | SDK role doesn't **own** the target DB/schema/tables | Recreate objects using the same role specified in profile.json. `GRANT USAGE`/`GRANT ALL` is not enough — the role must own the objects. |
| `PEM Base64 error` | Key without PEM headers | Ensure `private_key_file` points to a valid `.p8` file with headers |
| JWT auth error (390144) | Wrong account format or key not registered | Use hyphens in account, register public key, use unencrypted PKCS8 |
| `externalbrowser` wrong account | Browser session cached | Use key-pair auth (`SNOWFLAKE_JWT`) for cross-account |
| Reconciliation deletes valid data | Ran too soon | Built-in 65s wait handles this |
| ReceiverSaturated / HTTP 429 | Backpressure | Built-in exponential backoff handles it |
| Data not visible | Streaming visibility delay | Wait 2-3 minutes, then re-query |

---

## SDK v1.2.0 API Reference

**Import Path:**
```python
# CORRECT
from snowflake.ingest.streaming.streaming_ingest_client import StreamingIngestClient

# WRONG — does NOT exist:
# from snowpipe_streaming.client import StreamingIngestClient
```

**Client Constructor — One Client Per Pipe:**
```python
orders_client = StreamingIngestClient(
    client_name="ORDERS_CLIENT_abc123",
    db_name="<DATABASE>",
    schema_name="<SCHEMA>",
    pipe_name="<ORDERS_TABLE>-STREAMING",
    properties={
        "account": "ORG-ACCOUNT",
        "user": "USERNAME",
        "private_key": open("key.p8").read(),  # FULL PEM with headers
        "role": "ACCOUNTADMIN",
        "url": "https://ORG-ACCOUNT.snowflakecomputing.com:443",
    }
)
```

**Channel Operations:**
```python
channel, status = client.open_channel(channel_name="my_channel")

channel.append_rows(
    rows=[{"COL1": "val1"}],
    start_offset_token="orders_0",   # String tokens
    end_offset_token="orders_999",
)

channel.close(wait_for_flush=True)
client.close()
```

**Private Key Format:** Must be the **full PEM string** including `-----BEGIN PRIVATE KEY-----` headers. The bundled `config_manager.py` handles this automatically when `private_key_file` is set in the profile.

---

## First-Time / Trial Account Setup

Skip this section if the user already has Cortex Code and a Snowflake connection configured.

### Install Cortex Code
```bash
brew install Snowflake-Labs/cortex-code/cortex
# or: npm install -g @snowflake-labs/cortex-code
```

### Set Up Snowflake Connection

If the streaming target is a **different account** from the user's current Cortex Code session, use **key-pair auth** (not `externalbrowser`). Browser auth silently routes to whatever account the user is logged into.

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

- **Customer IDs are synthetic (1-10000)** — no database lookup needed.
- **One `StreamingIngestClient` per target table** (not one for all tables).
- **`config_manager.py`** accepts both `private_key` (inline PEM) and `private_key_file` (path).
- **Reconciliation** connects via `snowflake.connector` with DER-encoded private key (separate from SDK).
- **Parallel orchestrator** waits 65s between streaming and reconciliation.
- **Private key must be PKCS8 unencrypted** (BEGIN PRIVATE KEY, not BEGIN RSA PRIVATE KEY).
- **Role must be specified in profile** — SDK does not default to any role.

## Output

- Streaming project directory with configured venv, keys, and profiles
- Snowflake database/schema/tables created and owned by the specified role
- Synthetic e-commerce data (orders + order items) streamed into target tables
- Verified row counts confirming successful ingestion
