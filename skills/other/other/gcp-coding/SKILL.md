---
name: gcp-coding
description: Language-agnostic GCP best practices and common pitfalls. Use when writing code that integrates with GCP services (Cloud Run, Secret Manager, Cloud Storage, Pub/Sub, etc.) to avoid anti-patterns and follow Google Cloud's recommended approaches.
---

# GCP Coding Best Practices

This skill provides language-agnostic guidance for integrating with Google Cloud Platform services. Apply these patterns regardless of your programming language (Python, Node.js, Go, Java, etc.).

---

## 🔴 Critical Anti-Pattern: Runtime Secret Manager API Calls

### ❌ NEVER DO THIS:

**Anti-pattern:** Store secret NAMES as environment variables, then make API calls to fetch secret VALUES at runtime.

```python
# Python example (applies to all languages)
# Environment variable stores the secret NAME
SECRET_NAME = os.getenv("GITHUB_API_KEY_SECRET")  # "gh-app-key-prod"

# Application makes runtime API call to Secret Manager
secret_client = secretmanager.SecretManagerServiceClient()
response = secret_client.access_secret_version(
    request={"name": f"projects/{project}/secrets/{SECRET_NAME}/versions/latest"}
)
secret_value = response.payload.data.decode("UTF-8")
```

**Why this is bad:**
- Adds network latency (especially on cold starts)
- Requires error handling for API failures
- Creates runtime dependencies on Secret Manager availability
- Increases code complexity unnecessarily
- Slower than native integration
- Requires Secret Manager client library dependency

### ✅ CORRECT APPROACH: Use Cloud Run Native Secret Integration

**Best practice:** Let Cloud Run inject secret VALUES directly as environment variables.

**Terraform/Infrastructure:**
```hcl
# Cloud Run service configuration
env {
  name = "GITHUB_API_KEY"  # Direct value, not a reference
  value_source {
    secret_key_ref {
      secret  = google_secret_manager_secret.github_api_key.id
      version = "latest"  # or pin to specific version
    }
  }
}
```

**Application code (any language):**
```python
# Python
api_key = os.environ["GITHUB_API_KEY"]

# Node.js
const apiKey = process.env.GITHUB_API_KEY;

# Go
apiKey := os.Getenv("GITHUB_API_KEY")

# Java
String apiKey = System.getenv("GITHUB_API_KEY");
```

**Benefits:**
- Zero network latency (secrets pre-injected before container starts)
- No API client library needed
- Simpler code (direct environment variable reads)
- Fail-fast validation (Cloud Run verifies access during deployment)
- Supports automatic secret rotation (for volume mounts)
- Works the same in all languages

---

## Secret Manager: Environment Variables vs Volume Mounts

Cloud Run supports two methods for injecting secrets. Choose based on your use case:

### Method 1: Environment Variables (Most Common)

**When to use:**
- Static configuration values (API keys, database URLs)
- Secrets that don't change frequently
- When you need simple `os.environ` access

**Terraform:**
```hcl
env {
  name = "DATABASE_URL"
  value_source {
    secret_key_ref {
      secret  = google_secret_manager_secret.db_url.id
      version = "3"  # Pin to specific version for predictability
    }
  }
}
```

**Behavior:**
- Secret value fetched ONCE at container startup
- Cached for the lifetime of the container instance
- Requires container restart to pick up new secret versions
- **Best practice:** Pin to specific version (not "latest")

### Method 2: Volume Mounts (For Rotation)

**When to use:**
- Credentials that rotate frequently (OAuth tokens, TLS certs)
- Large secrets (multi-line certificates, JSON key files)
- When you need automatic rotation without redeployment

**Terraform:**
```hcl
volumes {
  name = "secrets"
  secret {
    secret = google_secret_manager_secret.tls_cert.id
    items {
      version = "latest"  # Use "latest" for auto-rotation
      path    = "tls.crt"
    }
  }
}

# Mount in container
volume_mounts {
  name       = "secrets"
  mount_path = "/secrets"
}
```

**Application code:**
```python
# Python: Read file every time you need it (gets latest value)
with open("/secrets/tls.crt") as f:
    cert = f.read()

# Node.js
const cert = fs.readFileSync('/secrets/tls.crt', 'utf8');

# Go
cert, err := os.ReadFile("/secrets/tls.crt")
```

**Behavior:**
- Cloud Run fetches CURRENT secret value on every file read
- Automatically picks up new versions without redeployment
- No startup validation (errors occur when reading file)
- **Best practice:** Use "latest" version for automatic rotation

---

## IAM Permissions for Secrets

Your Cloud Run service account needs `roles/secretmanager.secretAccessor`:

```hcl
# Project-level (grants access to all secrets)
resource "google_project_iam_member" "secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.app.email}"
}

# Secret-level (grants access to specific secret)
resource "google_secret_manager_secret_iam_member" "app_access" {
  secret_id = google_secret_manager_secret.api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.app.email}"
}
```

**Cloud Run validates IAM permissions at deployment time.** If the service account lacks access, deployment fails (fail-fast).

---

## Cloud Run Best Practices

### 1. **Use Dedicated Service Accounts (Least Privilege)**

❌ **Bad:** Using default Compute Engine service account (overly permissive)
```hcl
# Default service account has Editor role on project
service_account = "PROJECT_NUMBER-compute@developer.gserviceaccount.com"
```

✅ **Good:** Create service account with only required permissions
```hcl
resource "google_service_account" "app" {
  account_id   = "my-app-service"
  display_name = "My App Service Account"
}

# Grant only what's needed
resource "google_project_iam_member" "secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.app.email}"
}

# Use in Cloud Run
resource "google_cloud_run_v2_service" "app" {
  template {
    service_account = google_service_account.app.email
  }
}
```

### 2. **Set Resource Limits**

Always specify CPU and memory limits to control costs:

```hcl
resources {
  limits = {
    cpu    = "1"      # 1 vCPU
    memory = "512Mi"  # 512 MB
  }
  cpu_idle = true  # Only allocate CPU during requests
}
```

### 3. **Configure Proper Health Checks**

```hcl
startup_probe {
  http_get {
    path = "/health"
  }
  initial_delay_seconds = 10
  timeout_seconds       = 3
  period_seconds        = 5
  failure_threshold     = 3
}

liveness_probe {
  http_get {
    path = "/health"
  }
  period_seconds    = 10
  failure_threshold = 3
}
```

### 4. **Control Scaling**

```hcl
scaling {
  min_instance_count = 0   # Scale to zero when idle
  max_instance_count = 10  # Prevent runaway costs
}
```

---

## GCP Project ID: Don't Hardcode

### ❌ Avoid Hardcoding Project IDs

```python
# Bad: Hardcoded project ID
PROJECT_ID = "my-project-prod-12345"
```

### ✅ Use Environment Variables or Metadata

**Option 1: Environment variable (simplest)**
```hcl
# Terraform
env {
  name  = "GCP_PROJECT_ID"
  value = var.project_id
}
```

```python
# Application
project_id = os.environ["GCP_PROJECT_ID"]
```

**Option 2: Metadata service (no env var needed)**
```python
# Python
import google.auth
_, project_id = google.auth.default()

# Node.js
const {auth} = require('google-auth-library');
const client = await auth.getClient();
const projectId = await auth.getProjectId();

# Go
import "google.golang.org/api/option"
projectID, err := metadata.ProjectID()
```

---

## Cloud Storage: Use Signed URLs for Public Access

### ❌ Don't Make Buckets Public

```hcl
# Bad: Public bucket (security risk)
resource "google_storage_bucket_iam_member" "public" {
  bucket = google_storage_bucket.app.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"  # Everyone can read!
}
```

### ✅ Use Signed URLs for Temporary Access

```python
# Python
from google.cloud import storage

def generate_signed_url(bucket_name: str, blob_name: str) -> str:
    """Generate a temporary signed URL (valid for 1 hour)."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(hours=1),
        method="GET",
    )
    return url
```

```javascript
// Node.js
const {Storage} = require('@google-cloud/storage');
const storage = new Storage();

async function generateSignedUrl(bucketName, fileName) {
  const [url] = await storage
    .bucket(bucketName)
    .file(fileName)
    .getSignedUrl({
      version: 'v4',
      action: 'read',
      expires: Date.now() + 60 * 60 * 1000, // 1 hour
    });
  return url;
}
```

---

## Pub/Sub: Acknowledge Messages Properly

### ❌ Don't Forget to Acknowledge

```python
# Bad: Message never acknowledged (will be redelivered repeatedly)
def process_message(message):
    data = json.loads(message.data)
    process_data(data)
    # Missing: message.ack()
```

### ✅ Always Acknowledge or Nack

```python
# Good: Explicit acknowledgment
def process_message(message):
    try:
        data = json.loads(message.data)
        process_data(data)
        message.ack()  # Success: remove from queue
    except Exception as e:
        logger.error(f"Failed to process message: {e}")
        message.nack()  # Failure: requeue for retry
```

**Cloud Run Pub/Sub integration handles this automatically:**
- Returns 200-299: Message acknowledged
- Returns 400-499: Message discarded (won't retry)
- Returns 500-599: Message nacked (will retry)

---

## Firestore: Use Batched Writes

### ❌ Don't Write Documents One-by-One

```python
# Bad: N separate writes (slow, expensive)
for item in items:
    db.collection('users').document(item.id).set(item.to_dict())
```

### ✅ Use Batched Writes (500 ops/batch)

```python
# Good: Single batch write
from google.cloud import firestore

db = firestore.Client()
batch = db.batch()

for item in items:
    doc_ref = db.collection('users').document(item.id)
    batch.set(doc_ref, item.to_dict())

batch.commit()  # All writes in single transaction
```

---

## Cloud Logging: Structured Logs

### ❌ Don't Use Plain Strings

```python
# Bad: Unstructured logs (hard to query)
print(f"User {user_id} performed action {action}")
```

### ✅ Use Structured Logging (JSON)

```python
# Good: Structured logs (easy to query in Cloud Logging)
import logging
import json

logger = logging.getLogger(__name__)

logger.info("User action performed", extra={
    "json_fields": {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": {"source": "webhook"}
    }
})
```

**Query in Cloud Logging:**
```
jsonPayload.user_id="12345"
jsonPayload.action="pr_opened"
```

---

## Common Pitfalls Summary

| Anti-Pattern | Why Bad | Correct Approach |
|--------------|---------|------------------|
| Runtime Secret Manager API calls | Adds latency, complexity, network deps | Cloud Run native secret injection |
| Hardcoded project IDs | Not portable across environments | Environment vars or metadata service |
| Public Cloud Storage buckets | Security risk | Signed URLs for temporary access |
| Default service accounts | Over-permissive (security risk) | Dedicated service accounts (least privilege) |
| Unstructured logs | Hard to query/filter | Structured JSON logging |
| One-by-one Firestore writes | Slow, expensive | Batched writes |
| Missing Pub/Sub acknowledgments | Infinite redelivery | Always ack() or nack() |
| No resource limits | Runaway costs | Explicit CPU/memory limits |

---

## Testing Locally

### Use Emulators for Local Development

```bash
# Firestore emulator
gcloud emulators firestore start

# Pub/Sub emulator
gcloud emulators pubsub start

# Set environment variables to use emulator
export FIRESTORE_EMULATOR_HOST=localhost:8080
export PUBSUB_EMULATOR_HOST=localhost:8085
```

### Mock GCP Services in Tests

```python
# Python with pytest
from unittest.mock import patch, MagicMock

def test_secret_access():
    with patch.dict('os.environ', {'DATABASE_URL': 'postgres://test'}):
        # Your test code that reads DATABASE_URL
        assert get_database_url() == 'postgres://test'
```

---

## Deployment Verification Checklist

Before deploying to production:

- [ ] Service account has minimal required permissions (not Editor/Owner)
- [ ] Secrets use Cloud Run native integration (not runtime API calls)
- [ ] Resource limits set (CPU, memory)
- [ ] Health checks configured
- [ ] Max instances set (cost control)
- [ ] Structured logging implemented
- [ ] IAM permissions validated (`gcloud run services describe`)
- [ ] Environment variables verified (no hardcoded secrets)
- [ ] Error handling for GCP API calls
- [ ] Emulators used for local testing

---

## Additional Resources

- **Secret Manager Best Practices**: https://cloud.google.com/run/docs/configuring/services/secrets
- **IAM Best Practices**: https://cloud.google.com/iam/docs/best-practices-service-accounts
- **Cloud Run Best Practices**: https://cloud.google.com/run/docs/tips/general
- **Structured Logging**: https://cloud.google.com/logging/docs/structured-logging
