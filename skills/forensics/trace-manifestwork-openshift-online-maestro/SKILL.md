---
name: trace-manifestwork
description: This skill should be used when tracing ManifestWork resources through the Maestro system to find relationships between user-created work names, resource IDs, and applied manifests, or to debug manifest application issues across the management cluster and database.
---

# Trace ManifestWork

Trace ManifestWork resources through the complete Maestro lifecycle, connecting user-created work names, database resource IDs, and applied manifests on the management cluster.

## When to use this skill

Use this skill when you need to:
- Find the resource ID and manifests from a user-created work name
- Find the user-created work name and resource ID from a manifest name
- Find the user-created work name and manifests from a resource ID
- Debug manifest application issues
- Verify what manifests are in a ManifestWork
- Understand the deletion process for ManifestWorks

## Related Skills

**For debugging request lifecycle issues**, use the `trace-resource-request` skill after obtaining the resource ID:

- **trace-manifestwork** → Identifies WHAT (resource ID, work name, manifests)
- **trace-resource-request** → Debugs WHY (request flow, failures, timing)

**Example workflow:**
1. Use this skill to find resource ID from manifest name
2. Use `trace-resource-request` with that resource ID to trace request through logs
3. Diagnose where in the pipeline the request succeeded or failed

**Common scenario**: You have a manifest that isn't working correctly. Use this skill to map the manifest to its resource ID, then use `trace-resource-request` to analyze the log flow and identify where the request failed (server, broker, agent, or status updates).

## What this skill does

The Maestro system transforms user-created ManifestWorks through multiple stages:

```
User Work Name ←→ Resource ID (DB) ←→ AppliedManifestWork ←→ Applied Manifests
```

This skill traces these relationships bidirectionally, combining database queries and kubectl commands to provide a complete view of a ManifestWork's lifecycle.

## Key Concepts

### Cluster Architecture

**CRITICAL**: Maestro uses a dual-cluster architecture:

- **Service (svc) Cluster**: Runs Maestro Server and Database (postgres-breakglass or maestro-db pods)
- **Management (mgmt) Cluster**: Runs Maestro Agent, AppliedManifestWorks, and applied manifests

**When tracing, you must switch between cluster contexts:**
- Use **svc cluster context** to query the database
- Use **mgmt cluster context** to query AppliedManifestWorks and manifests

### Identifiers

**User-Created Work Name**: The name assigned by the user when creating a ManifestWork via gRPC client (e.g., `e44ec579-9646-549a-b679-db8d19d6da37`). Stored in DB as `payload->'metadata'->>'name'`.

**Resource ID**: The database primary key and CloudEvent `resourceid` (e.g., `55c61e54-a3f6-563d-9fec-b1fe297bdfdb`). Used as `spec.manifestWorkName` in AppliedManifestWork.

**AppliedManifestWork Name**: Format `{agentID}-{resourceID}` (e.g., `f1d8a1049b93dffc1929d57a719c3a09a4dcbfe0cd6e42840325be3b2dde73c8-55c61e54-a3f6-563d-9fec-b1fe297bdfdb`).

**Manifest**: The actual Kubernetes resource (Deployment, Service, etc.) with an ownerReference to the AppliedManifestWork.

## How to use this skill

### Step 1: Determine Entry Point

Ask the user which identifier they have:

**Option A: Resource ID**
- Use when you have the database resource ID or CloudEvent resourceid
- Collect: `resource_id` (e.g., `55c61e54-a3f6-563d-9fec-b1fe297bdfdb`)

**Option B: Manifest Details**
- Use when you only know the manifest kind/name/namespace
- Collect: `manifest_kind` (e.g., "deployment", "service", "configmap")
- Collect: `manifest_name` (e.g., "maestro-e2e-upgrade-test")
- Collect: `manifest_namespace` (optional, defaults to "default")

**Option C: User-Created Work Name**
- Use when you have the work name assigned by the user
- Collect: `work_name` (e.g., `e44ec579-9646-549a-b679-db8d19d6da37`)

### Step 2: Verify Prerequisites and Cluster Access

**CRITICAL**: Verify access to BOTH clusters (svc and mgmt)

**Ask the user which setup they have:**

#### Option A: Single Kubeconfig with Multiple Contexts

If the user has one kubeconfig file with contexts for both clusters:

**Ask for cluster context names:**
- Service cluster context (where database runs): e.g., `svc-cluster-context`
- Management cluster context (where agent runs): e.g., `mgmt-cluster-context`

**Verify kubectl and contexts:**

```bash
# Verify kubectl is available
which kubectl

# List available contexts
kubectl config get-contexts

# Verify service cluster access (database)
kubectl config use-context <svc-cluster-context>
kubectl cluster-info
kubectl get namespace maestro 2>/dev/null

# Verify management cluster access (agent)
kubectl config use-context <mgmt-cluster-context>
kubectl cluster-info
kubectl get appliedmanifestworks -A 2>/dev/null | head -n 5
```

**Common context names:**
- Service cluster: `aro-hcp-int`, `svc-cluster`, `maestro-server`
- Management cluster: `mgmt-cluster`, `management`, `hub-cluster`

#### Option B: Separate Kubeconfig Files

If the user has two separate kubeconfig files:

**Ask for kubeconfig file paths:**
- Service cluster kubeconfig: e.g., `/path/to/svc-kubeconfig.yaml`
- Management cluster kubeconfig: e.g., `/path/to/mgmt-kubeconfig.yaml`

**Verify kubectl and kubeconfig files:**

```bash
# Verify kubectl is available
which kubectl

# Verify service cluster kubeconfig (database)
kubectl --kubeconfig=/path/to/svc-kubeconfig.yaml cluster-info
kubectl --kubeconfig=/path/to/svc-kubeconfig.yaml get namespace maestro 2>/dev/null

# Verify management cluster kubeconfig (agent)
kubectl --kubeconfig=/path/to/mgmt-kubeconfig.yaml cluster-info
kubectl --kubeconfig=/path/to/mgmt-kubeconfig.yaml get appliedmanifestworks -A 2>/dev/null | head -n 5
```

#### Option C: Merge Kubeconfig Files (Recommended)

If using separate files becomes cumbersome, merge them into one:

```bash
# Backup existing kubeconfig
cp ~/.kube/config ~/.kube/config.backup

# Merge kubeconfigs
KUBECONFIG=/path/to/svc-kubeconfig.yaml:/path/to/mgmt-kubeconfig.yaml \
  kubectl config view --flatten > ~/.kube/config

# Verify merged contexts
kubectl config get-contexts

# Rename contexts for clarity (optional)
kubectl config rename-context <old-svc-context> svc-cluster
kubectl config rename-context <old-mgmt-context> mgmt-cluster
```

After merging, use Option A (contexts) for all future traces.

If prerequisites are missing:
- kubectl not found: Ask user to install kubectl
- Context not found: Ask user for correct context names or kubeconfig paths
- Kubeconfig file not found: Verify file paths exist
- Cluster unreachable: Verify kubeconfig, context names/files, and network access
- Namespace not found: Verify correct cluster and namespace

### Step 3: Execute Trace Based on Entry Point

#### Option A: Trace from Resource ID

**Step 3A.1: Query Database for User Work Name**

**Switch to service cluster context:**

```bash
kubectl config use-context <svc-cluster-context>
```

Determine database connection method:

```bash
# Check for postgres-breakglass (ARO-HCP INT)
kubectl -n maestro get pods -l app=postgres-breakglass 2>/dev/null

# Check for maestro-db (Service cluster)
kubectl -n maestro get pods -l name=maestro-db 2>/dev/null
```

Execute SQL query:

```sql
SELECT id,
       payload->'metadata'->>'name' AS user_work_name,
       payload->'spec'->'workload'->'manifests' AS manifests,
       created_at, updated_at, deleted_at
FROM resources
WHERE id = '<resource_id>';
```

Example:
```sql
SELECT id,
       payload->'metadata'->>'name' AS user_work_name,
       payload->'spec'->'workload'->'manifests' AS manifests,
       created_at, updated_at, deleted_at
FROM resources
WHERE id = '55c61e54-a3f6-563d-9fec-b1fe297bdfdb';
```

**Step 3A.2: Query Cluster for AppliedManifestWork**

**Switch to management cluster context:**

```bash
kubectl config use-context <mgmt-cluster-context>
```

Query for AppliedManifestWork:

```bash
# Find AppliedManifestWork by manifestWorkName
resource_id="<resource_id>"

amw_name=$(kubectl get appliedmanifestworks -o json | \
  jq -r ".items[] | select(.spec.manifestWorkName == \"$resource_id\") | .metadata.name")

if [ -z "$amw_name" ]; then
    echo "WARNING: AppliedManifestWork not found. Work may be deleted or not yet applied."
else
    echo "AppliedManifestWork: $amw_name"

    # Get applied resources
    kubectl get appliedmanifestwork "$amw_name" -o yaml

    # List applied manifests
    kubectl get appliedmanifestwork "$amw_name" -o jsonpath='{range .status.appliedResources[*]}{.resource}{"\t"}{.namespace}{"\t"}{.name}{"\n"}{end}'
fi
```

#### Option B: Trace from Manifest Details

**Step 3B.1: Get AppliedManifestWork from Manifest**

**Switch to management cluster context (manifests are on mgmt cluster):**

```bash
kubectl config use-context <mgmt-cluster-context>
```

Query for manifest and extract owner:

```bash
manifest_kind="<manifest_kind>"
manifest_name="<manifest_name>"
manifest_namespace="${manifest_namespace:-default}"

# Get manifest and extract ownerReference
if [ -n "$manifest_namespace" ]; then
    amw_name=$(kubectl get "$manifest_kind" "$manifest_name" -n "$manifest_namespace" \
      -o jsonpath='{.metadata.ownerReferences[?(@.kind=="AppliedManifestWork")].name}' 2>/dev/null)
else
    amw_name=$(kubectl get "$manifest_kind" "$manifest_name" \
      -o jsonpath='{.metadata.ownerReferences[?(@.kind=="AppliedManifestWork")].name}' 2>/dev/null)
fi

if [ -z "$amw_name" ]; then
    echo "ERROR: Manifest not found or has no AppliedManifestWork owner"
    exit 1
fi

echo "AppliedManifestWork: $amw_name"
```

**Step 3B.2: Extract Resource ID from AppliedManifestWork**

```bash
# Get manifestWorkName (Resource ID) from AppliedManifestWork
resource_id=$(kubectl get appliedmanifestwork "$amw_name" \
  -o jsonpath='{.spec.manifestWorkName}' 2>/dev/null)

if [ -z "$resource_id" ]; then
    echo "ERROR: Cannot extract manifestWorkName from AppliedManifestWork"
    exit 1
fi

echo "Resource ID: $resource_id"
```

**Step 3B.3: Query Database for User Work Name**

**Switch to service cluster context:**

```bash
kubectl config use-context <svc-cluster-context>
```

Execute SQL query:

```sql
SELECT id,
       payload->'metadata'->>'name' AS user_work_name,
       created_at, updated_at, deleted_at
FROM resources
WHERE id = '<resource_id>';
```

**Step 3B.4: Get All Applied Resources**

**Switch back to management cluster context:**

```bash
kubectl config use-context <mgmt-cluster-context>
```

List all applied resources:

```bash
# List all applied resources in this work
kubectl get appliedmanifestwork "$amw_name" -o jsonpath='{range .status.appliedResources[*]}{.resource}{"\t"}{.namespace}{"\t"}{.name}{"\n"}{end}'
```

#### Option C: Trace from User-Created Work Name

**Step 3C.1: Query Database for Resource ID**

**Switch to service cluster context:**

```bash
kubectl config use-context <svc-cluster-context>
```

Execute SQL query:

```sql
SELECT id,
       payload->'metadata'->>'name' AS user_work_name,
       payload->'spec'->'workload'->'manifests' AS manifests,
       created_at, updated_at, deleted_at
FROM resources
WHERE payload->'metadata'->>'name' = '<work_name>';
```

Example:
```sql
SELECT id,
       payload->'metadata'->>'name' AS user_work_name,
       payload->'spec'->'workload'->'manifests' AS manifests,
       created_at, updated_at, deleted_at
FROM resources
WHERE payload->'metadata'->>'name' = 'e44ec579-9646-549a-b679-db8d19d6da37';
```

**Step 3C.2: Query Cluster for AppliedManifestWork**

**Switch to management cluster context:**

```bash
kubectl config use-context <mgmt-cluster-context>
```

Query for AppliedManifestWork:

```bash
# Find AppliedManifestWork by manifestWorkName (use Resource ID from DB)
resource_id="<resource_id_from_db>"

amw_name=$(kubectl get appliedmanifestworks -o json | \
  jq -r ".items[] | select(.spec.manifestWorkName == \"$resource_id\") | .metadata.name")

if [ -z "$amw_name" ]; then
    echo "WARNING: AppliedManifestWork not found. Work may be deleted or not yet applied."
else
    echo "AppliedManifestWork: $amw_name"

    # Get applied resources
    kubectl get appliedmanifestwork "$amw_name" -o yaml

    # List applied manifests
    kubectl get appliedmanifestwork "$amw_name" -o jsonpath='{range .status.appliedResources[*]}{.resource}{"\t"}{.namespace}{"\t"}{.name}{"\n"}{end}'
fi
```

### Step 4: Database Connection Methods

**IMPORTANT**: Database pods are on the **service cluster**. Ensure you're on the svc cluster context before running these commands.

```bash
kubectl config use-context <svc-cluster-context>
```

**Environment A: ARO-HCP INT (postgres-breakglass) - CRITICAL**

This environment requires special handling with user confirmations for safety.

The `trace.sh` script automatically:

1. **Checks if postgres-breakglass pod exists:**
   - If not running, prompts user to scale up deployment
   - Waits for pod to be ready (60s timeout)

2. **Shows SQL query for review:**
   - Displays the exact SQL that will be executed
   - **Requires user confirmation** before execution (critical env safety)

3. **Executes query via kubectl exec:**
   - Automatically sources the `connect` script
   - Runs the SQL query
   - Returns results

**Interactive flow:**
```
Environment: ARO-HCP INT (CRITICAL)
Database: postgres-breakglass

⚠️  postgres-breakglass pod is not running

To start the pod, run:
  kubectl -n maestro scale deployment postgres-breakglass --replicas 1

Would you like to scale up the pod now? (yes/no): yes

Scaling up postgres-breakglass deployment...
Waiting for pod to be ready (timeout: 60s)...
✓ Pod ready: postgres-breakglass-7b8c9d6f5-abc12

────────────────────────────────────────
SQL Query to execute:
────────────────────────────────────────
SELECT id, payload->'metadata'->>'name' AS user_work_name
FROM resources WHERE id = '55c61e54...';
────────────────────────────────────────

⚠️  CRITICAL ENVIRONMENT - Confirm before execution
Execute this query on ARO-HCP INT database? (yes/no): yes

Executing query on postgres-breakglass...
[Query results displayed]
```

**Environment B: Service Cluster (maestro-db)**

Standard database pod with direct query execution:

```bash
# Get database pod
pod_name=$(kubectl -n maestro get pods -l name=maestro-db -o jsonpath='{.items[0].metadata.name}')

# Execute query directly (no confirmation needed)
kubectl -n maestro exec -i "$pod_name" -- psql -U maestro -d maestro -c "<SQL_QUERY>"
```

### Step 5: Format and Present Results

Present a comprehensive trace showing all relationships:

```
ManifestWork Trace Results
═══════════════════════════════════════════════════

User-Created Work Name: e44ec579-9646-549a-b679-db8d19d6da37
Resource ID (DB):       55c61e54-a3f6-563d-9fec-b1fe297bdfdb
AppliedManifestWork:    f1d8a1049b93dffc1929d57a719c3a09a4dcbfe0cd6e42840325be3b2dde73c8-55c61e54-a3f6-563d-9fec-b1fe297bdfdb

Database Information:
────────────────────
Created:  2024-01-15 10:30:00
Updated:  2024-01-15 10:32:15
Deleted:  <null> (still active)

Applied Manifests (3 total):
────────────────────────────
Resource Type       Namespace       Name
───────────────     ──────────      ─────────────────────
Deployment          default         maestro-e2e-upgrade-test
Service             default         maestro-e2e-service
ConfigMap           default         maestro-e2e-config

Status: ✓ All manifests successfully applied to cluster
```

For deleted works:
```
ManifestWork Trace Results (DELETED)
═══════════════════════════════════════════════════

User-Created Work Name: e44ec579-9646-549a-b679-db8d19d6da37
Resource ID (DB):       55c61e54-a3f6-563d-9fec-b1fe297bdfdb
AppliedManifestWork:    Not found on cluster (work deleted)

Database Information:
────────────────────
Created:  2024-01-15 10:30:00
Updated:  2024-01-15 10:32:15
Deleted:  2024-01-15 11:00:00

Original Manifests (from DB):
─────────────────────────────
- Deployment/default/maestro-e2e-upgrade-test
- Service/default/maestro-e2e-service
- ConfigMap/default/maestro-e2e-config

Status: ⚠ Work deleted from cluster, data available in DB only
```

### Step 6: Handle Errors

Provide clear, actionable error messages:

| Error | Message | Next Steps |
|-------|---------|------------|
| Resource not in DB | "No resource found with this ID/name" | Verify ID/name is correct; check for typos |
| AppliedManifestWork not found | "Work not applied to cluster" | Check if work was deleted; verify cluster connection |
| Manifest not found | "Manifest {kind}/{namespace}/{name} not found" | Verify manifest details; check if already deleted |
| No owner references | "Not managed by any ManifestWork" | Explain this is a standalone resource |
| kubectl unavailable | "kubectl is required" | Installation instructions |
| DB connection failed | "Cannot connect to database" | Verify kubectl access; check namespace |
| Multiple results | "Multiple resources found" | Show all results; ask user to be more specific |

### Step 7: Suggest Next Steps

Based on results:

**If successful trace:**
- "Complete trace successful. All relationships verified."
- "To view full AppliedManifestWork: `kubectl get appliedmanifestwork {name} -o yaml`"
- "To check manifest status: `kubectl get {kind} {name} -n {namespace} -o yaml`"

**If work deleted:**
- "Work deleted from cluster but found in database."
- "To see deletion timestamp: Check `deleted_at` field in database"
- "To view original manifests: Check DB `payload` field"

**If resource not found:**
- "Resource not found in database."
- "Try searching with partial name:"
  ```sql
  SELECT id, payload->'metadata'->>'name' AS name, created_at, deleted_at
  FROM resources
  WHERE payload->'metadata'->>'name' LIKE '%{partial_name}%'
  ORDER BY created_at DESC
  LIMIT 10;
  ```

**For further investigation:**
- "To check agent logs: `kubectl logs -n maestro-agent -l app=maestro-agent`"
- "To view events: `kubectl get events -n {namespace} --sort-by='.lastTimestamp'`"
- "To see CloudEvents in DB: Query `events` table for resourceid"

## Alternative: Use Included Scripts

The skill includes helper scripts for common operations.

### Method 1: Using Contexts (Single Kubeconfig)

```bash
# By resource ID
.claude/skills/trace-manifestwork/scripts/trace.sh \
  --resource-id "55c61e54-a3f6-563d-9fec-b1fe297bdfdb" \
  --svc-context svc-cluster \
  --mgmt-context mgmt-cluster

# By user work name
.claude/skills/trace-manifestwork/scripts/trace.sh \
  --work-name "e44ec579-9646-549a-b679-db8d19d6da37" \
  --svc-context svc-cluster \
  --mgmt-context mgmt-cluster

# By manifest details
.claude/skills/trace-manifestwork/scripts/trace.sh \
  --manifest-kind deployment \
  --manifest-name maestro-e2e-upgrade-test \
  --manifest-namespace default \
  --svc-context svc-cluster \
  --mgmt-context mgmt-cluster
```

### Method 2: Using Separate Kubeconfig Files

```bash
# By resource ID
.claude/skills/trace-manifestwork/scripts/trace.sh \
  --resource-id "55c61e54-a3f6-563d-9fec-b1fe297bdfdb" \
  --svc-kubeconfig ~/svc-cluster-kubeconfig.yaml \
  --mgmt-kubeconfig ~/mgmt-cluster-kubeconfig.yaml

# By user work name
.claude/skills/trace-manifestwork/scripts/trace.sh \
  --work-name "e44ec579-9646-549a-b679-db8d19d6da37" \
  --svc-kubeconfig ~/svc-cluster-kubeconfig.yaml \
  --mgmt-kubeconfig ~/mgmt-cluster-kubeconfig.yaml

# By manifest details
.claude/skills/trace-manifestwork/scripts/trace.sh \
  --manifest-kind deployment \
  --manifest-name maestro-e2e-upgrade-test \
  --manifest-namespace default \
  --svc-kubeconfig ~/svc-cluster-kubeconfig.yaml \
  --mgmt-kubeconfig ~/mgmt-cluster-kubeconfig.yaml
```

## Technical Reference

**Maestro Resource Data Flow:**

1. User creates ManifestWork with name `e44ec579-9646-549a-b679-db8d19d6da37` via MaestroGRPCSourceWorkClient
2. Client generates UID `55c61e54-a3f6-563d-9fec-b1fe297bdfdb` and sends CloudEvent with `resourceid` extension
3. Maestro server stores in DB with `resourceid` as primary key (`id` column)
4. Server publishes CloudEvent to agent using Resource ID as ManifestWork name
5. Agent creates AppliedManifestWork named `{agentID}-{resourceID}` and applies manifests
6. Manifests have ownerReference to AppliedManifestWork

**Database Schema (resources table):**
- `id`: VARCHAR, primary key (= CloudEvent resourceid)
- `payload`: JSONB containing full CloudEvent
  - `payload->'metadata'->>'name'`: User-created work name
  - `payload->'spec'->'workload'->'manifests'`: Array of manifests
- `created_at`, `updated_at`, `deleted_at`: Timestamps

**AppliedManifestWork Structure:**
- `metadata.name`: `{agentID}-{resourceID}` format
- `spec.manifestWorkName`: Resource ID (used to link to DB)
- `spec.agentID`: Agent identifier
- `status.appliedResources[]`: Array of applied resources
  - `resource`: Resource type (e.g., "deployments")
  - `namespace`: Resource namespace
  - `name`: Resource name
  - `uid`: Kubernetes UID

**Manifest ownerReference:**
- Points to AppliedManifestWork (not original ManifestWork)
- `apiVersion`: `work.open-cluster-management.io/v1`
- `kind`: `AppliedManifestWork`
- `name`: Full AppliedManifestWork name

## Files in this skill

- `scripts/trace.sh` - Complete trace script supporting all entry points
- `references/maestro-data-flow.md` - Detailed Maestro resource flow documentation
- `references/troubleshooting-guide.md` - Common issues and solutions
- `examples/trace-by-resource-id.md` - Example: Resource ID trace
- `examples/trace-by-manifest.md` - Example: Manifest name trace
- `examples/trace-by-work-name.md` - Example: User work name trace
