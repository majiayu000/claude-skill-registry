---
name: image-backup-restore
description: Implementing and debugging PostgreSQL image backup and restore features. Use when working with database snapshots, backup jobs, restore operations, azcopy blob transfers, or troubleshooting image-related provisioning failures.
---

# PostgreSQL Image Backup & Restore

## Overview

Image backup creates point-in-time snapshots of PostgreSQL instances by:
1. Running pg_dump to create a logical backup
2. Uploading to Azure Blob Storage via azcopy
3. Recording metadata in CMS database

Image restore provisions new instances from existing backups by:
1. Creating PVC, Secret, ConfigMap for the new instance
2. Running pg_restore to load data from blob storage
3. Starting PostgreSQL with recovery configuration

## Key Files

```
toygres-orchestrations/src/
├── orchestrations/
│   ├── create_image.rs        # Backup orchestration
│   └── create_instance.rs     # Restore flow (v1.0.2+)
├── activities/
│   ├── run_backup_job.rs      # pg_dump + azcopy upload
│   ├── run_restore_job.rs     # azcopy download + pg_restore
│   ├── deploy_postgres_from_pvc.rs  # Start from existing PVC
│   ├── get_instance_password.rs     # Retrieve source password
│   └── cms/
│       └── image_ops.rs       # Image CMS operations
├── templates/
│   ├── backup-job.yaml        # K8s Job for backup
│   ├── restore-job.yaml       # K8s Job for restore
│   ├── postgres-config.yaml   # ConfigMap with pg_hba.conf
│   └── postgres-secret.yaml   # Secret with password
└── activity_types.rs          # ImageOperation enum
```

## Backup Flow

```rust
// create_image.rs orchestration
1. CreateImageRecord        // Reserve ID in CMS
2. GetInstanceByK8sName     // Get source instance details
3. RunBackupJob             // pg_dump + azcopy to blob
4. UpdateImageStatus        // Mark as available
```

### Backup Job Template

```yaml
# backup-job.yaml key commands
command:
  - /bin/sh
  - -c
  - |
    # Login with workload identity (NOT --identity!)
    azcopy login --login-type=workload

    # Create backup
    PGPASSWORD=$POSTGRES_PASSWORD pg_dump -h $SOURCE_HOST -U postgres -Fc $DATABASE > /backup/backup.dump

    # Upload to blob
    azcopy copy /backup/backup.dump "$BLOB_URL"
```

## Restore Flow

```rust
// create_instance.rs v1.0.2 restore path
1. CreatePvc                // Create empty PVC
2. GetSourcePassword        // Get password from source image
3. CreateImageRecord        // Reserve in CMS (with correct image_type!)
4. RunRestoreJob            // azcopy download + pg_restore
5. DeployPostgresFromPvc    // Start PostgreSQL
6. TestConnection           // Verify connectivity (120s timeout for DNS)
7. UpdateInstanceStatus     // Mark as running
```

### Critical: Password Handling

The restore flow must use the **source image's password**, not a new password:

```rust
// activity_types.rs
pub enum ImageOperation {
    GetSourcePassword { id: Uuid },  // Get password from image record
    // ...
}

pub enum ImageOperationResult {
    PasswordFound { password: String },
    // ...
}

// image_ops.rs
ImageOperation::GetSourcePassword { id } => {
    let encrypted = sqlx::query_scalar::<_, Vec<u8>>(
        "SELECT source_password_encrypted FROM cms.images WHERE id = $1"
    )
    .bind(id)
    .fetch_one(pool)
    .await?;

    let password = String::from_utf8(encrypted)?;
    Ok(ImageOperationResult::PasswordFound { password })
}
```

### Critical: Image Type Preservation

When restoring, fetch image details BEFORE creating CMS record:

```rust
// create_instance.rs v1.0.2
let (effective_image_type, effective_postgres_version) = if let Some(ref image_id) = input.source_image_id {
    ctx.trace_info(format!("[v1.0.2] Fetching source image details: {}", image_id));

    let details = ctx.schedule_activity_typed::<ImageOperationInput, ImageOperationResult>(
        activities::cms::image_ops::NAME,
        &ImageOperationInput {
            operation: ImageOperation::GetImageDetails { id: image_id.parse()? },
        },
    ).await?;

    match details {
        ImageOperationResult::ImageDetails { image_type, postgres_version, .. } => {
            (image_type, postgres_version)
        }
        _ => return Err("Failed to get image details".into()),
    }
} else {
    (input.image_type.clone(), postgres_version.clone())
};
```

## azcopy Workload Identity

**CRITICAL:** On AKS, always use `--login-type=workload`:

```bash
# WRONG - Uses IMDS (VM managed identity), fails with 403
azcopy login --identity

# CORRECT - Uses federated token from pod
azcopy login --login-type=workload
```

Debug workload identity issues:

```bash
# Check env vars are injected
kubectl exec <pod> -- env | grep AZURE_

# Should see:
# AZURE_CLIENT_ID=...
# AZURE_TENANT_ID=...
# AZURE_FEDERATED_TOKEN_FILE=/var/run/secrets/azure/tokens/azure-identity-token
```

## pg_hba.conf for pg_durable

The pg_durable background worker connects via TCP (127.0.0.1), not Unix socket.
**Must use `trust` for localhost connections:**

```yaml
# postgres-config.yaml
pg_hba.conf: |
  # IPv4 local connections (trust for pg_durable background worker)
  host    all             all             127.0.0.1/32            trust
  # IPv6 local connections (trust for pg_durable background worker)
  host    all             all             ::1/128                 trust
  # Remote connections require password
  host    all             all             10.0.0.0/8              scram-sha-256
```

## Common Issues

### test_connection Timeout

**Symptom:** Instance provisioning fails at test_connection step.

**Root cause:** Azure LoadBalancer DNS propagation can take 60-90+ seconds.

**Fix:** Use 120s timeout:

```rust
ctx.schedule_activity_with_retry_typed::<TestConnectionInput, TestConnectionOutput>(
    activities::test_connection::NAME,
    &test_input,
    RetryPolicy::new(5)
        .with_backoff(BackoffStrategy::Exponential {
            base: Duration::from_secs(2),
            multiplier: 2.0,
            max: Duration::from_secs(30),
        })
        .with_timeout(Duration::from_secs(120)), // Not 60s!
)
.await?;
```

### pg_durable Worker Not Starting

**Symptom:** PostgreSQL starts but pg_durable background worker fails with "password authentication failed".

**Root cause:** pg_hba.conf uses `scram-sha-256` for localhost TCP connections.

**Fix:** Change to `trust` for 127.0.0.1 and ::1 (see pg_hba.conf section above).

### Restore Shows Wrong image_type

**Symptom:** Restored instance shows "stock" instead of "pg_durable" in CMS.

**Root cause:** Using input.image_type instead of source image's image_type.

**Fix:** Fetch source image details before creating CMS record (see Image Type Preservation section).

### azcopy 403 AuthorizationPermissionMismatch

**Symptom:** `azcopy login --identity` succeeds but operations fail with 403.

**Root cause:** `--identity` uses IMDS, not AKS workload identity.

**Fix:** Use `--login-type=workload` (see azcopy section above).

## Debugging Commands

```bash
# Watch backup/restore job logs
kubectl logs -n toygres-managed job/<job-name> -f

# Check blob storage
az storage blob list --account-name <acct> --container-name images --auth-mode login

# Test PostgreSQL connection
kubectl exec -it <postgres-pod> -n toygres-managed -- psql -U postgres -c "SELECT 1"

# Check pg_durable worker
kubectl exec -it <postgres-pod> -n toygres-managed -- psql -U postgres -c "SELECT * FROM pg_stat_activity WHERE backend_type = 'pg_durable background worker'"

# View job completion status
kubectl get jobs -n toygres-managed
```

## API Endpoints

```rust
// Create backup image
POST /api/images
{
    "name": "my-backup",
    "instance_id": "uuid",
    "description": "Optional description"
}

// Create instance from image
POST /api/instances
{
    "name": "restored-instance",
    "password": "ignored-uses-source",
    "source_image_id": "image-uuid",
    "dns_label": "restored-instance"
}
```

## Orchestration Versioning

Use `start_orchestration` which automatically picks the latest version:

```rust
// api.rs - uses latest version (currently 1.0.2 with restore support)
runtime
    .start_orchestration(
        &orchestration_id,
        orchestrations::CREATE_INSTANCE,
        input_json,
    )
    .await?;
```

## Development Workflow: Test Then Deploy

When making changes to backup/restore functionality, follow this workflow:

### 1. Build Release Version
```bash
cargo build --release
```

### 2. Test Locally with Azure PostgreSQL
Connect to the same CMS database used by AKS:

```bash
# Get the database URL from AKS secret
kubectl get secret toygres-secrets -n toygres-system -o jsonpath='{.data.DATABASE_URL}' | base64 -D

# Start local server
DATABASE_URL="postgresql://azureuser:xxx@xxx.postgres.azure.com:5432/postgres?sslmode=require" \
RUST_LOG=info,toygres_server=debug,toygres_orchestrations=debug \
./target/release/toygres-server standalone

# Test endpoints
curl http://localhost:8080/health
curl -X POST http://localhost:8080/login -H "Content-Type: application/x-www-form-urlencoded" -d "username=$TOYGRES_ADMIN_USERNAME&password=$TOYGRES_ADMIN_PASSWORD" -c /tmp/cookies.txt
curl -b /tmp/cookies.txt http://localhost:8080/api/instances
curl -b /tmp/cookies.txt http://localhost:8080/api/images
```

### 3. Deploy to AKS
After local testing succeeds:

```bash
./deploy/deploy-to-aks.sh
```

### 4. Verify AKS Deployment
```bash
# Check health
curl http://4.249.80.96/health

# View logs
kubectl logs -n toygres-system -l app.kubernetes.io/component=server -f

# Check pods
kubectl get pods -n toygres-system
```

### Key Points
- Local testing uses the **same Azure PostgreSQL** as AKS (not local Docker)
- This ensures CMS state and duroxide orchestrations are consistent
- The `standalone` mode runs API + workers in a single process
