---
name: trace-resource-request
description: This skill should be used when tracing resource requests through the Maestro system to debug resource lifecycle issues, track request flow from client to agent and back, or troubleshoot failures in resource creation, update, or deletion operations across the server-agent-server pipeline. Supports both Kubernetes log files and ARO HCP Kusto CSV exports.
---

# Trace Resource Request

## Overview

Trace the complete lifecycle of resource requests through the Maestro system, following the path: Client → Maestro Server → Message Broker → Maestro Agent → Manifests → Status Updates → Maestro Server → gRPC Clients.

This skill automates log analysis to identify where requests succeed or fail in the pipeline, combining automated scripts with manual troubleshooting guidance.

## When to Use This Skill

Use this skill when:
- A resource request (create/update/delete) is not completing as expected
- Status updates from the agent are not reaching the client
- Investigating why manifests are not being applied to the target cluster
- Debugging message broker (MQTT/gRPC) communication issues
- Tracing the full path of a request using operation ID, resource ID, work name, or manifest name
- Understanding the timeline and flow of events for a specific resource

## Related Skills

**For identifying resource IDs and relationships**, use the `trace-manifestwork` skill first:

- **trace-manifestwork** → Maps manifest names to resource IDs and work names
- **trace-resource-request** → Traces those resources through the system logs

**Example workflow:**
1. Use `trace-manifestwork` if you only know manifest details (kind/name/namespace)
2. Extract the resource ID from the trace results
3. Use this skill with that resource ID to analyze request flow in logs

**Common scenario**: You know a deployment or service isn't working, but only know its Kubernetes name. Use `trace-manifestwork` to find the associated resource ID and work name, then use this skill to trace through server and agent logs to identify where the request failed or stalled.

## Terminology

**IMPORTANT**: In Maestro colloquial usage, **ManifestWork** and **resource bundle** are the same concept and are used interchangeably:

- **ManifestWork**: The formal Kubernetes Custom Resource Definition (CRD) name used by the Open Cluster Management SDK
- **Resource bundle**: The term used in Maestro's RESTful API endpoints (e.g., `/api/maestro/v1/resource-bundles`)
- **Resource**: The term used in database tables (`resources` table) and some internal code

When users refer to "resource bundles," "resources," or "ManifestWorks," they are all talking about the same thing: a collection of Kubernetes manifests packaged together for delivery to target clusters. In log messages and traces, you'll see all three terms used to refer to this concept.

## Request Flow Overview

Understanding the complete request flow is critical for effective troubleshooting:

```
1. Client sends spec request
   ↓ (gRPC)
2. Maestro Server receives request
   ↓ (Database write)
3. Server publishes to message broker
   ↓ (MQTT/gRPC)
4. Maestro Agent receives spec
   ↓ (Apply to cluster)
5. Agent applies manifests
   ↓ (Status generation)
6. Agent publishes status update
   ↓ (MQTT/gRPC)
7. Server receives status update
   ↓ (Database write + broadcast)
8. Server broadcasts to other instances
   ↓ (gRPC publish)
9. Server sends to gRPC clients
```

Each step can fail independently, and this skill helps identify the exact failure point.

## Key Identifiers

Resource requests can be traced using multiple identifiers:

- **Operation ID (`op-id`)**: Tracks the entire operation from client request through to status updates. Embedded in log messages across the system. Format: UUID (e.g., `2dd9d768-a02d-4539-a99f-8a2c801a1c4b`)

- **Resource ID (`resourceid` or `resourceID`)**: The database primary key and CloudEvent identifier for the resource bundle. Format: UUID (e.g., `9936a444-051a-5658-9b57-af855e27b01b`)

- **Work Name**: The user-assigned name for the ManifestWork. Stored in resource metadata. Format: string (e.g., `nginx-work`)

- **Manifest Name**: The name of a specific Kubernetes manifest within the resource bundle. Format: string (e.g., `nginx-deployment`)

**Best Practice**: Start tracing with `op-id` when available, as it provides end-to-end correlation across all components and log messages.

## Workflow Decision Tree

**START**: What identifier do you have?

```
Have logs already?
├─ YES: Go to → Step 2: Analyze Logs with Automated Script
└─ NO: Go to → Step 1: Collect Logs

What identifier are you using?
├─ Operation ID (op-id)
│  └─ Best choice - traces entire request lifecycle
├─ Resource ID
│  └─ Good for database and CloudEvent correlation
├─ Work Name
│  └─ Good for identifying resources by user-assigned name
└─ Manifest Name
   └─ Useful for finding which resource contains a specific manifest

Found the failure point?
├─ YES: Go to → Step 4: Detailed Error Analysis
└─ NO: Go to → Step 3: Manual Log Review
```

## Step 1: Collect Logs

### Option A: Collect from Kubernetes Clusters

If Maestro server and agent are running in Kubernetes, use the provided script to collect logs.

**Script:** `scripts/dump_logs.sh`

**Usage:**

```bash
# Set kubeconfig to the cluster running Maestro server
export KUBECONFIG=/path/to/maestro-server-kubeconfig

# Collect Maestro server logs
namespace=maestro label="app=maestro" container=service logs_dir=$HOME/maestro-logs \
  bash .claude/skills/trace-resource-request/scripts/dump_logs.sh

# Set kubeconfig to the cluster running Maestro agent
export KUBECONFIG=/path/to/maestro-agent-kubeconfig

# Collect Maestro agent logs
namespace=maestro label="app=maestro-agent" container=agent logs_dir=$HOME/maestro-logs \
  bash .claude/skills/trace-resource-request/scripts/dump_logs.sh
```

**Environment Variables:**
- `namespace`: Kubernetes namespace (default: `maestro`)
- `label`: Pod label selector (default: `app=maestro`)
- `container`: Container name (default: `service`)
- `logs_dir`: Output directory (default: `$HOME/maestro-logs`)

**Output:** Log files will be saved to `logs_dir` with names like `maestro-maestro-556dfb55f-x8mtx.log`

### Option B: Use Existing Log Files

If you already have log files, ensure they are organized in a single directory with clear naming:
- Server logs: `maestro*.log` (excluding files with `agent` in the name)
- Agent logs: `maestro-agent*.log` or `maestro.agent*.log`

Place all log files in a directory (e.g., `$HOME/maestro-logs`) for analysis.

### Option C: Collect from ARO HCP Kusto (Azure)

For ARO HCP environments, logs are stored in Azure Kusto. Export logs using the Kusto queries below, then use the Kusto-specific trace script.

**Kusto Query for Server Logs:**

```kusto
// Export Maestro server logs from Kusto
// Limit the query time window (e.g., to 5 minutes) to avoid overwhelming log sizes
let start_time = datetime(2026-01-15T09:00:00Z);
let end_time = datetime(2026-01-15T09:05:00Z);
database('HCPServiceLogs').table('kubesystem')
| where TIMESTAMP between (start_time .. end_time)
| where namespace_name == "maestro"
    and container_name contains "service"
| where log contains "op-id"                     // Operation tracing
    or log contains "error"                      // Errors
    or log contains "failed"                     // Failures
    or log contains "eventType="                 // CloudEvents
    or log contains "resourceID="                // Resource operations
    or log contains "Publishing resource"        // Resource publishing
    or log contains "Received event"             // Event receiving
    or log contains "Sending event"              // Event sending
    or log contains "status update"              // Status updates
| project TIMESTAMP, pod_name, log
| order by TIMESTAMP asc
```

**Kusto Query for Agent Logs:**

```kusto
// Export Maestro agent logs from Kusto
// Limit the query time window (e.g., to 5 minutes) to avoid overwhelming log sizes
let start_time = datetime(2026-01-15T09:00:00Z);
let end_time = datetime(2026-01-15T09:05:00Z);
database('HCPServiceLogs').table('kubesystem')
| where TIMESTAMP between (start_time .. end_time)
| where namespace_name == "maestro"
    and container_name contains "maestro-agent"
| where log !contains "Object is patched"        // Exclude noise
    and log !contains "Patching resource"        // Exclude noise
    and log !contains "Caches are synced"        // Exclude noise
    and log !contains "Starting worker"          // Exclude noise
    and log !contains "Waiting for caches"       // Exclude noise
| where log contains "op-id"                     // Operation tracing
    or log contains "error"                      // Errors
    or log contains "failed"                     // Failures
    or log contains "Received event"             // Event receiving
    or log contains "Sending event"              // Event sending
    or log contains "Server side applied"        // Resource application
    or log contains "Deleted resource"           // Resource deletion
    or log contains "manifestwork"               // ManifestWork operations
    or log contains "Requeue"                    // Requeue operations
| project TIMESTAMP, pod_name, log
| order by TIMESTAMP asc
```

**Important Notes:**
- Adjust `start_time` and `end_time` to cover the time window of your request (check timestamps in your application logs)
- Keep time windows small (5-10 minutes) to avoid overwhelming log sizes
- Export the results as CSV files (e.g., `export.svc.csv` for server, `export.agent.csv` for agent)
- The CSV will have 3 columns: TIMESTAMP, pod_name, log

**After exporting, proceed to Step 2 Option B for Kusto CSV analysis.**

## Step 2: Analyze Logs with Automated Script

Once logs are collected, use the automated tracing script to analyze the request flow.

### Option A: Analyze Kubernetes Log Files

For logs collected from Kubernetes (Step 1 Option A or B), use the standard trace script.

**Script:** `scripts/trace_request.sh`

**Basic Usage Examples:**

```bash
# Trace by operation ID (recommended - most comprehensive)
bash .claude/skills/trace-resource-request/scripts/trace_request.sh \
  --op-id 2dd9d768-a02d-4539-a99f-8a2c801a1c4b \
  --logs-dir $HOME/maestro-logs

# Trace by resource ID
bash .claude/skills/trace-resource-request/scripts/trace_request.sh \
  --resource-id 9936a444-051a-5658-9b57-af855e27b01b \
  --logs-dir $HOME/maestro-logs

# Trace by work name
bash .claude/skills/trace-resource-request/scripts/trace_request.sh \
  --work-name nginx-work \
  --logs-dir $HOME/maestro-logs

# Trace by manifest name
bash .claude/skills/trace-resource-request/scripts/trace_request.sh \
  --manifest-name nginx-deployment \
  --logs-dir $HOME/maestro-logs

# Combine multiple identifiers for comprehensive analysis
bash .claude/skills/trace-resource-request/scripts/trace_request.sh \
  --op-id 2dd9d768-a02d-4539-a99f-8a2c801a1c4b \
  --resource-id 9936a444-051a-5658-9b57-af855e27b01b \
  --work-name nginx-work \
  --logs-dir $HOME/maestro-logs
```

**Script Output:**

The script generates a markdown trace report with:
1. **Request Flow Analysis**: Log entries for each stage of the request lifecycle
2. **Timestamp Correlation**: Shows timing of events across components
3. **Error Detection**: Automatically identifies common error patterns
4. **Next Steps**: Suggestions based on findings

**Output File:** `$HOME/maestro-logs/trace_request.<timestamp>.log`

**Reading the Output:**

The trace report is structured by request flow stages:

1. **Server Receives Spec Request**: Confirms client request reached the server
2. **Server Publishes to Message Broker**: Confirms server sent to MQTT/gRPC
3. **Agent Receives Spec Request**: Confirms agent received the CloudEvent
4. **Agent Handles ManifestWork**: Confirms manifests were applied
5. **Agent Publishes Status Update**: Confirms agent sent status back
6. **Server Receives Status Update**: Confirms server got the status
7. **Server Broadcasts Status**: Confirms status propagated to other instances
8. **Server Sends to gRPC Subscribers**: Confirms client received status

**Interpretation:**

- ✅ **Section has log entries**: Step completed successfully
- ⚠️ **"No matching entries found"**: Step failed or is not visible in logs
- 🔍 **Error Analysis section**: Lists detected error patterns

If any section shows "No matching entries found", that indicates the failure point. Proceed to Step 4 for detailed troubleshooting.

### Option B: Analyze Kusto CSV Exports

For logs exported from ARO HCP Kusto (Step 1 Option C), use the Kusto-specific trace script that works directly with CSV files.

**Script:** `scripts/trace_request_kusto.sh`

**Basic Usage Examples:**

```bash
# Trace by operation ID with both server and agent logs (recommended)
bash .claude/skills/trace-resource-request/scripts/trace_request_kusto.sh \
  --server-csv export.svc.csv \
  --agent-csv export.agent.csv \
  --op-id 2dd9d768-a02d-4539-a99f-8a2c801a1c4b

# Trace by resource ID
bash .claude/skills/trace-resource-request/scripts/trace_request_kusto.sh \
  --server-csv export.svc.csv \
  --agent-csv export.agent.csv \
  --resource-id 9936a444-051a-5658-9b57-af855e27b01b

# Server logs only (when agent logs not available)
bash .claude/skills/trace-resource-request/scripts/trace_request_kusto.sh \
  --server-csv export.svc.csv \
  --op-id 2dd9d768-a02d-4539-a99f-8a2c801a1c4b

# Save output to specific directory
bash .claude/skills/trace-resource-request/scripts/trace_request_kusto.sh \
  --server-csv export.svc.csv \
  --agent-csv export.agent.csv \
  --op-id <op-id> \
  --output-dir /tmp/traces
```

**Script Output:**

The Kusto trace script produces the same markdown trace report format as the standard trace script:
1. **Request Flow Analysis**: Log entries for each stage of the request lifecycle
2. **Timestamp Correlation**: Shows timing of events across components
3. **Error Detection**: Automatically identifies common error patterns
4. **Next Steps**: Suggestions based on findings

**Output File:** `./trace_request.<timestamp>.log` (or in `--output-dir` if specified)

**Reading the Output:**

Same interpretation as Option A:
- ✅ **Section has log entries**: Step completed successfully
- ⚠️ **"No matching entries found"**: Step failed or is not visible in logs
- 🔍 **Error Analysis section**: Lists detected error patterns

**CSV Format Requirements:**

The script expects CSV files exported from Kusto with exactly 3 columns:
- Column 1: TIMESTAMP
- Column 2: pod_name
- Column 3: log (the actual log message)

The script automatically handles CSV quoting and escaped characters in the log messages.

## Step 3: Manual Log Review

When automated analysis doesn't reveal the issue, perform manual log review to find subtle problems.

### Search Patterns for Each Stage

Use `grep` or your preferred log viewer to search for these patterns:

**1. Server Receives Request:**
```bash
grep 'op-id="<op-id>".*receive the event from client' maestro*.log
```

**2. Server Publishes to Broker:**
```bash
grep 'Publishing resource.*resourceID="<resource-id>"' maestro*.log
grep 'Sending event.*resourceID="<resource-id>"' maestro*.log
```

**3. Agent Receives Request:**
```bash
grep 'resourceid="<resource-id>".*Received event' maestro-agent*.log
```

**4. Agent Applies Manifests:**
```bash
# Success indicators
grep 'Server Side Applied\|Created\|Updated' maestro-agent*.log
grep '<work-name>' maestro-agent*.log

# Failure indicators
grep 'error\|Error\|failed' maestro-agent*.log | grep -i manifest
```

**5. Agent Publishes Status:**
```bash
grep 'resourceid="<resource-id>".*Sending event.*status' maestro-agent*.log
```

**6. Server Receives Status:**
```bash
grep 'resourceID="<resource-id>".*received status update' maestro*.log
grep 'resourceID="<resource-id>".*Updating resource status' maestro*.log
```

**7. Server Broadcasts Status:**
```bash
grep 'resourceID="<resource-id>".*Broadcast the resource status' maestro*.log
```

**8. Server Sends to Clients:**
```bash
grep 'op-id="<op-id>".*send the event to status subscribers' maestro*.log
```

### Common Log Patterns

**Normal "no clients registered" message:**

The log message `"no clients registered on this instance"` is **normal** in the following scenarios:
- Server is running with `--subscription-type=broadcast` and another instance handled the status
- gRPC client disconnected after sending the request
- Status update is being broadcasted to other server instances

**Only investigate further if:**
- The client did NOT receive the status update AND
- No server instance has logs showing "send the event to status subscribers"

**Skipping resource status update:**

The log `"skipping resource status update"` in broadcast mode is **normal behavior**. It indicates that another server instance is handling the status update for this resource.

## Step 4: Detailed Error Analysis

When you've identified the failure point, consult the error analysis reference for specific troubleshooting steps.

**Reference:** `references/error_analysis.md`

The error analysis reference provides:
- Detailed diagnostic steps for each failure point
- Common causes and resolutions
- Database queries for debugging
- Log pattern references
- Component health checks

**How to Use the Reference:**

1. Identify the failure point from Step 2 or Step 3
2. Find the corresponding error section in `references/error_analysis.md`:
   - §1: Server Does Not Receive Spec Request
   - §2: Server Does Not Publish Spec Request
   - §3: Agent Does Not Receive Spec Request
   - §4: Agent Does Not Handle Spec Request
   - §5: Agent Does Not Publish Status Update
   - §6: Server Does Not Receive Status Update
   - §7: Server Does Not Handle Status Update
   - §8: Server Does Not Broadcast Status Update
   - §9: Server Does Not Publish Status to Clients

3. Follow the diagnostic steps and resolution guidance
4. Use the provided database queries to verify state
5. Check for the specific error patterns listed

**Example Workflow:**

```
Trace shows: "Agent Does Not Receive Spec Request"
↓
Open references/error_analysis.md → §3
↓
Check: MQTT/gRPC subscription in agent logs
Check: Message broker connectivity
Check: Server publish errors
↓
Diagnosis: MQTT broker connection lost
↓
Resolution: Restart agent to restore connection
```

## Step 5: Database Verification

For issues involving database state, run SQL queries to verify resource and event records.

**Connect to Database:**

```bash
# Using kubectl port-forward
kubectl -n maestro port-forward svc/postgres-breakglass 5432:5432

# Or use make target
make db/login
```

**Useful Queries:**

```sql
-- Find resource by ID
SELECT
    id,
    consumer_name,
    version,
    created_at,
    jsonb_pretty(payload) as payload,
    jsonb_pretty(status) as status
FROM resources
WHERE id = '<resource-id>';

-- Find resource by work name
SELECT
    id as resource_id,
    payload->'metadata'->>'name' as work_name,
    consumer_name,
    created_at
FROM resources
WHERE payload->'metadata'->>'name' = '<work-name>';

-- Check events for resource
SELECT
    id,
    event_type,
    reconciled_date,
    created_at
FROM events
WHERE source_id = '<resource-id>'
ORDER BY created_at DESC;

-- Check status events
SELECT
    id,
    status_event_type,
    created_at,
    reconciled_at
FROM status_events
WHERE resource_id = '<resource-id>'
ORDER BY created_at DESC;
```

**What to Look For:**

- **Resource exists**: Confirms server received and stored the request
- **Events exist with reconciled_date**: Confirms server published to broker
- **Status events exist**: Confirms server received status updates from agent
- **Null reconciled_date or reconciled_at**: Indicates processing stalled

More database queries are available in `references/error_analysis.md` → Database Queries section.

## Step 6: Component Health Checks

If the request flow is broken, verify that all components are healthy and connected.

### Maestro Server

```bash
# Check server is running
kubectl -n maestro get pods -l app=maestro

# Check server logs for startup
kubectl -n maestro logs -l app=maestro -c service | grep "Starting"

# Verify gRPC server started
kubectl -n maestro logs -l app=maestro -c service | grep "Starting gRPC server"

# Verify message broker connection
kubectl -n maestro logs -l app=maestro -c service | grep "mqtt is connected\|gRPC.*connected"

# Verify database connection
kubectl -n maestro logs -l app=maestro -c service | grep "Starting listener"
```

### Maestro Agent

```bash
# Check agent is running
kubectl -n maestro get pods -l app=maestro-agent

# Check agent controllers started
kubectl -n maestro logs -l app=maestro-agent | grep "Caches are synced"

# Verify message broker connection
kubectl -n maestro logs -l app=maestro-agent | grep "mqtt is connected\|subscribed to.*broker"

# Check ManifestWork controller
kubectl -n maestro logs -l app=maestro-agent | grep "ManifestWorkController"
```

### Message Broker (MQTT)

```bash
# Check MQTT broker is running
kubectl -n maestro get pods -l app=maestro-mqtt

# Check MQTT broker logs
kubectl -n maestro logs -l app=maestro-mqtt
```

### Database

```bash
# Check database is running
kubectl -n maestro get pods -l app=postgres

# Test database connection
kubectl -n maestro exec -it deployment/maestro -c service -- psql -U maestro -d maestro -c "SELECT 1"
```

## Step 7: Resolution and Validation

After fixing the issue, validate that requests now flow correctly:

1. **Trigger a new request** with a different operation ID
2. **Collect fresh logs** using Step 1
3. **Run trace script** using Step 2 with the new op-id
4. **Verify all stages succeed** in the trace output
5. **Confirm client receives status update** as expected

If issues persist:
- Review `references/error_analysis.md` for additional troubleshooting steps
- Check component configurations (consumer name, subscription type, topics)
- Consider restarting components to reset connections
- Investigate network policies and firewall rules

## Example: Complete Trace (Kubernetes)

**Scenario:** Client reports that a resource create request (op-id: `2dd9d768-a02d-4539-a99f-8a2c801a1c4b`) never completed.

**Step 1:** Collect logs
```bash
# Collected to $HOME/maestro-logs/
namespace=maestro label="app=maestro" container=service logs_dir=$HOME/maestro-logs \
  bash .claude/skills/trace-resource-request/scripts/dump_logs.sh

namespace=maestro label="app=maestro-agent" container=agent logs_dir=$HOME/maestro-logs \
  bash .claude/skills/trace-resource-request/scripts/dump_logs.sh
```

**Step 2:** Run automated trace
```bash
bash .claude/skills/trace-resource-request/scripts/trace_request.sh \
  --op-id 2dd9d768-a02d-4539-a99f-8a2c801a1c4b \
  --logs-dir $HOME/maestro-logs
```

**Step 3:** Review trace output

Output shows:
- ✅ Server Receives Spec Request - Found
- ✅ Server Publishes to Message Broker - Found
- ✅ Agent Receives Spec Request - Found
- ⚠️ Agent Handles ManifestWork - No matching entries found
- ⚠️ Agent Publishes Status Update - No matching entries found

**Conclusion:** Agent received the request but failed to apply manifests.

**Step 4:** Consult error analysis reference

Open `references/error_analysis.md` → §4: Agent Does Not Handle Spec Request

**Step 5:** Follow diagnostic steps
```bash
# Check for errors in agent logs
grep 'error\|Error\|failed' $HOME/maestro-logs/maestro-agent*.log | grep -i manifest

# Found: "failed to apply manifest: Deployment.apps 'nginx' is invalid:
# spec.template.spec.containers[0].image: Required value"
```

**Root Cause:** Invalid manifest in resource bundle (missing container image).

**Resolution:** Fix manifest and retry the request.

## Example: Complete Trace (ARO HCP / Kusto)

**Scenario:** In ARO HCP environment, client reports resource with op-id `3a1d53f4-4d0c-4ce6-b820-88276ed4050b` is not being applied.

**Step 1:** Export logs from Kusto

Use the Kusto queries from Step 1 Option C with appropriate time window:
```kusto
let start_time = datetime(2026-01-15T09:45:00Z);
let end_time = datetime(2026-01-15T09:55:00Z);
// ... rest of server query
```

Export to `export.svc.csv` and `export.agent.csv`

**Step 2:** Run Kusto trace script

```bash
bash .claude/skills/trace-resource-request/scripts/trace_request_kusto.sh \
  --server-csv export.svc.csv \
  --agent-csv export.agent.csv \
  --op-id 3a1d53f4-4d0c-4ce6-b820-88276ed4050b
```

**Step 3:** Review trace output

Output shows:
- ⚠️ Server Receives Spec Request - No matching entries found
- ✅ Server Receives Status Update - Found (multiple entries)
- ✅ Server Broadcasts Status - Found

**Conclusion:** The server is only receiving status updates, not spec requests. This indicates:
1. The client request may not have reached this server instance
2. Another server instance may have handled the initial request
3. The op-id might only be present in status updates, not the original spec request

**Step 4:** Further investigation

Extract resource ID from the status update logs:
```bash
# From trace output, see resourceID=""2e146da1-1d4d-54f0-86eb-08e6887f5a71""
```

Re-trace with resource ID:
```bash
bash .claude/skills/trace-resource-request/scripts/trace_request_kusto.sh \
  --server-csv export.svc.csv \
  --agent-csv export.agent.csv \
  --resource-id 2e146da1-1d4d-54f0-86eb-08e6887f5a71
```

This reveals the complete flow including the initial spec request.

## Best Practices

1. **Always collect both server and agent logs** - The issue could be in either component

2. **Use op-id when available** - It provides the most comprehensive end-to-end tracing

3. **Check timestamps** - Look for unusual delays between stages that might indicate performance issues

4. **Compare with successful requests** - Trace a working request to understand normal log patterns

5. **Preserve logs** - Keep logs from failed requests for future debugging and pattern analysis

6. **Automate collection** - Set up log aggregation (e.g., ELK, Loki) for real-time analysis

7. **Monitor patterns** - Watch for recurring errors that might indicate systemic issues

## Troubleshooting Tips

**Can't find op-id in logs?**
- Check if the request actually reached the server (verify client-side logs)
- Search by resource-id or work-name instead
- Verify log files are from the correct time period

**Script shows "No matching entries found" for all stages?**
- Verify identifiers are correct (check for typos)
- Ensure logs are from the correct clusters (server vs agent)
- Check log file naming matches expected patterns
- Verify time range overlap between request and collected logs

**Agent logs not showing manifest application?**
- Check if ManifestWork was created: `kubectl get manifestworks`
- Review agent controller logs for errors
- Verify agent has correct RBAC permissions
- Check if agent is watching the correct namespace

**Database queries return no results?**
- Verify resource-id format (should be UUID)
- Check if request was soft-deleted (deleted_at IS NOT NULL)
- Ensure connecting to correct database/schema
- Try searching by work-name instead of resource-id

## Additional Resources

- **Error Analysis Reference**: `references/error_analysis.md` - Comprehensive troubleshooting guide
- **Dump Logs Script**: `scripts/dump_logs.sh` - Collect logs from Kubernetes
- **Trace Script (Kubernetes)**: `scripts/trace_request.sh` - Automated log analysis for Kubernetes logs
- **Trace Script (Kusto)**: `scripts/trace_request_kusto.sh` - Automated log analysis for ARO HCP Kusto CSV exports
- **Maestro Documentation**: Project root `README.md` and `docs/` directory
- **CloudEvents Spec**: Understanding the event format and extensions

## Quick Reference

### Common Commands

**Kubernetes Environments:**

```bash
# Collect server logs
bash scripts/dump_logs.sh

# Collect agent logs
namespace=maestro label="app=maestro-agent" bash scripts/dump_logs.sh

# Trace by op-id
bash scripts/trace_request.sh --op-id <op-id> --logs-dir $HOME/maestro-logs

# Trace by resource-id
bash scripts/trace_request.sh --resource-id <resource-id> --logs-dir $HOME/maestro-logs
```

**ARO HCP (Kusto) Environments:**

```bash
# Trace by op-id with both server and agent CSV exports
bash scripts/trace_request_kusto.sh \
  --server-csv export.svc.csv \
  --agent-csv export.agent.csv \
  --op-id <op-id>

# Trace by resource-id
bash scripts/trace_request_kusto.sh \
  --server-csv export.svc.csv \
  --agent-csv export.agent.csv \
  --resource-id <resource-id>
```

**Database Queries:**

```sql
-- Database lookup
SELECT * FROM resources WHERE id = '<resource-id>';

-- Find resource by work name
SELECT * FROM resources WHERE payload->'metadata'->>'name' = '<work-name>';
```

### Error Patterns Quick Reference

| Error Message | Likely Cause | Section |
|---------------|--------------|---------|
| `Failed to publish resource` | Message broker issue | §2, §3, §5 |
| `unmatched consumer name` | Configuration mismatch | §7 |
| `failed to convert resource` | CloudEvent decode error | §7 |
| `failed to create status event` | Database error | §7 |
| `recreate the listener` | PostgreSQL notification issue | §2, §7 |
| `no clients registered` | Normal in broadcast mode | §9 |
| `skipping resource status update` | Normal in broadcast mode | §9 |

For detailed explanations, see `references/error_analysis.md`.
