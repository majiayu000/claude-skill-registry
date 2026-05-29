---
name: oci-resources
description: "Use OCI free-tier resources (Object Storage, Autonomous Database). Use when user says 'oci database', 'object storage', 'oracle db', or 'autonomous database'."
allowed-tools: Bash, Read, Write, Edit
---

# OCI Resources

You are an expert at using Oracle Cloud Infrastructure free-tier resources on oci-dev.

## When To Use

- User says "oci database", "oracle db", "autonomous database"
- User says "object storage", "bucket", "blob storage"
- User says "store files in cloud", "pre-signed URL"
- Building app on oci-dev that needs persistence beyond SQLite
- Need cross-machine file transfer without git

## Architecture Context

OCI resources live on oci-dev (the "brain"):

| Machine | Role | OCI Resources |
|---------|------|---------------|
| oci-dev | Brain | Object Storage (20GB), Autonomous DB (20GB) |
| homelab | Body | 26TB local storage, Docker |
| macmini | Muscle | GPU, transcription |

**When to use OCI vs local:**
- OCI Object Storage: Backups, user uploads, cross-machine transfer, pre-signed URLs
- OCI Autonomous DB: Multi-user apps, production persistence, complex queries
- Homelab: Large media files, Docker volumes, 26TB capacity
- SQLite: Single-user apps, development, simple persistence

---

## Object Storage

### Credentials

```
Bucket: khamel-storage
Namespace: ax58mwjqur5g
Region: us-phoenix-1
```

### CLI Commands

```bash
# List objects
oci os object list --bucket-name khamel-storage --namespace ax58mwjqur5g

# Upload file
oci os object put --bucket-name khamel-storage --namespace ax58mwjqur5g \
    --file /path/to/local/file.txt --name remote-name.txt

# Download file
oci os object get --bucket-name khamel-storage --namespace ax58mwjqur5g \
    --name remote-name.txt --file /path/to/local/file.txt

# Delete file
oci os object delete --bucket-name khamel-storage --namespace ax58mwjqur5g \
    --name remote-name.txt

# Generate pre-signed URL (1 hour expiry)
oci os preauth-request create --bucket-name khamel-storage --namespace ax58mwjqur5g \
    --name file.txt --access-type ObjectRead --time-expires "$(date -d '+1 hour' -Iseconds)"
```

### Python SDK

```python
import oci

config = oci.config.from_file()  # Uses ~/.oci/config
object_storage = oci.object_storage.ObjectStorageClient(config)

namespace = "ax58mwjqur5g"
bucket = "khamel-storage"

# Upload
with open("local_file.txt", "rb") as f:
    object_storage.put_object(namespace, bucket, "remote_name.txt", f)

# Download
response = object_storage.get_object(namespace, bucket, "remote_name.txt")
with open("downloaded.txt", "wb") as f:
    for chunk in response.data.raw.stream(1024 * 1024):
        f.write(chunk)

# List objects
objects = object_storage.list_objects(namespace, bucket)
for obj in objects.data.objects:
    print(obj.name)
```

### Use Cases

| Use Case | Pattern |
|----------|---------|
| User uploads | Store in bucket, save object name in DB |
| Backups | Nightly cron uploads SQLite/config files |
| Cross-machine transfer | Upload from homelab, download on oci-dev |
| Shareable links | Generate pre-signed URL with expiry |

---

## Autonomous Database

### Credentials

```
Database: khameldb
Admin User: ADMIN
Password: ~/.oci/db_password.txt
Wallet: ~/.oci/wallet/
DSN: adb.us-phoenix-1.oraclecloud.com:1522/g0e8384679284b8_khameldb_low.adb.oraclecloud.com
```

### Web UIs (No Setup Required)

| Interface | URL | Purpose |
|-----------|-----|---------|
| SQL Developer | https://G0E8384679284B8-KHAMELDB.adb.us-phoenix-1.oraclecloudapps.com/ords/sql-developer | Query browser, schema design |
| APEX | https://G0E8384679284B8-KHAMELDB.adb.us-phoenix-1.oraclecloudapps.com/ords/apex | Low-code app builder |
| ORDS REST | https://G0E8384679284B8-KHAMELDB.adb.us-phoenix-1.oraclecloudapps.com/ords/ | REST API for tables |

### Python Connection

```python
import oracledb

connection = oracledb.connect(
    user="ADMIN",
    password=open("/home/ubuntu/.oci/db_password.txt").read().strip(),
    dsn="adb.us-phoenix-1.oraclecloud.com:1522/g0e8384679284b8_khameldb_low.adb.oraclecloud.com",
    config_dir="/home/ubuntu/.oci/wallet",
    wallet_location="/home/ubuntu/.oci/wallet",
    wallet_password="WalletPass123#"
)

# Execute query
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM users WHERE id = :id", {"id": 1})
    row = cursor.fetchone()

# Insert data
with connection.cursor() as cursor:
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (:name, :email)",
        {"name": "Alice", "email": "alice@example.com"}
    )
    connection.commit()
```

### Connection Helper

Create `db.py` for reusable connections:

```python
import oracledb
from contextlib import contextmanager

OCI_DIR = "/home/ubuntu/.oci"

def get_connection():
    return oracledb.connect(
        user="ADMIN",
        password=open(f"{OCI_DIR}/db_password.txt").read().strip(),
        dsn="adb.us-phoenix-1.oraclecloud.com:1522/g0e8384679284b8_khameldb_low.adb.oraclecloud.com",
        config_dir=f"{OCI_DIR}/wallet",
        wallet_location=f"{OCI_DIR}/wallet",
        wallet_password="WalletPass123#"
    )

@contextmanager
def get_cursor():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    finally:
        cursor.close()
        conn.close()
```

### When to Use vs SQLite

| Scenario | SQLite | OCI Autonomous DB |
|----------|--------|-------------------|
| Personal CLI tool | Best | Overkill |
| Single-user local app | Best | Overkill |
| Multi-user web app | No | Best |
| Production persistence | Risky | Best |
| Complex joins/queries | OK | Best |
| 20GB+ data | Limited | Best |
| Zero config needed | Best | Requires wallet |

---

## Verification Commands

```bash
# Test OCI CLI config
oci iam region list --output table

# Test Object Storage access
oci os bucket get --bucket-name khamel-storage --namespace ax58mwjqur5g

# Test database connectivity (Python)
python3 -c "
import oracledb
conn = oracledb.connect(
    user='ADMIN',
    password=open('/home/ubuntu/.oci/db_password.txt').read().strip(),
    dsn='adb.us-phoenix-1.oraclecloud.com:1522/g0e8384679284b8_khameldb_low.adb.oraclecloud.com',
    config_dir='/home/ubuntu/.oci/wallet',
    wallet_location='/home/ubuntu/.oci/wallet',
    wallet_password='WalletPass123#'
)
print('Connected to:', conn.version)
conn.close()
"
```

---

## Anti-Patterns

- Using OCI DB for single-user CLI tools (use SQLite)
- Storing wallet password in git (keep in ~/.oci/)
- Object Storage for tiny files <1KB (overhead not worth it)
- Hardcoding credentials in application code (use db.py helper)
- Not closing database connections (use context manager)
- Using OCI when homelab has capacity (26TB vs 20GB)

---

## Keywords

oci, oracle, autonomous database, object storage, bucket, khameldb, blob, pre-signed url, oracledb, wallet, apex, ords
