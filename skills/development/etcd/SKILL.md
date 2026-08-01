---
name: etcd
description: This document defines the Claude Code skill for troubleshooting etcd
  issues on two-node OpenShift clusters with fencing topology. When activated, Claude
  becomes an expert etcd/Pacemaker troubleshooter capable of iterative diagnosis and
  remediation.
---

# Etcd Troubleshooting Skill

This document defines the Claude Code skill for troubleshooting etcd issues on two-node OpenShift clusters with fencing topology. When activated, Claude becomes an expert etcd/Pacemaker troubleshooter capable of iterative diagnosis and remediation.

## Skill Overview

This skill enables Claude to:
- Validate and test access to cluster components via Ansible and OpenShift CLI
- Iteratively collect diagnostic data from Pacemaker, etcd, and OpenShift
- Analyze symptoms and identify root causes
- Propose and execute remediation steps
- Verify fixes and adjust approach based on results
- Provide comprehensive troubleshooting throughout the diagnostic process

## Step-by-Step Procedure

### 1. Validate Access

**1.1 Ansible Inventory Validation:**
- Check if `deploy/openshift-clusters/inventory.ini` exists
- Verify the inventory file has valid cluster node entries
- Test SSH connectivity to cluster nodes using Ansible ping module

**1.2 OpenShift Cluster Access Validation:**
- Test direct cluster access with `oc version`
- If direct access fails, check for `deploy/openshift-clusters/proxy.env`
- If proxy.env exists, source it before running oc commands
- Verify cluster access with `oc get nodes`
- Remember proxy requirement for all subsequent oc commands

**IMPORTANT: No Cluster Access Scenario**

If OpenShift cluster API access is unavailable (which is expected when etcd is down), **all diagnostics and remediation must be performed via Ansible** using direct VM access. The troubleshooting workflow remains fully functional using only:

- Ansible ad-hoc commands to cluster VMs
- Ansible playbooks for diagnostics collection
- Direct SSH access to nodes via Ansible

When cluster access is unavailable:
- ✓ You can still diagnose and fix etcd issues completely
- ✓ All Pacemaker operations work via Ansible
- ✓ All etcd container operations work via Ansible (podman commands)
- ✓ All logs are accessible via Ansible (journalctl commands)
- ✗ Cannot query OpenShift operators or cluster-level resources
- ✗ Cannot use oc commands for verification (use Ansible equivalents instead)

This is a **normal scenario** when etcd is down - proceed with VM-based troubleshooting.

### 2. Collect Data

**Choose Your Diagnostic Approach**

There are two approaches to data collection:

**Quick Manual Triage (recommended for initial assessment)**

Start with a few targeted commands to assess the situation:
- `pcs status` - Check Pacemaker cluster state and failed actions
- `podman ps -a --filter name=etcd` - Verify etcd containers are running
- `etcdctl endpoint health` - Confirm etcd health

This takes ~30 seconds and is often sufficient to identify simple issues (stale failures, container restarts, etc.) that can be fixed immediately with `pcs resource cleanup etcd`.

**Full Diagnostic Collection (for complex/unclear issues)**

If quick triage reveals complex problems or the root cause is unclear, run the comprehensive diagnostic script:

```bash
./helpers/etcd/collect-all-diagnostics.sh
```

This script (~5-10 minutes):
- Validates Ansible and cluster access automatically
- Collects all VM-level diagnostics via Ansible playbook
- Collects OpenShift cluster-level data (if accessible)
- Saves everything to `/tmp/etcd-diagnostics-<timestamp>/`
- Generates a `DIAGNOSTIC_REPORT.txt` with analysis commands

Use the full collection when:
- Quick triage doesn't reveal the cause
- Multiple components appear affected
- You need to preserve diagnostic data for later analysis
- The issue involves cluster ID mismatches or split-brain scenarios

**Manual Collection Commands**

For manual data collection, use the commands below.

**IMPORTANT: Target the Correct Host Group**

- **All etcd/Pacemaker commands** must target the `cluster_vms` host group (the OpenShift cluster nodes)
- **VM lifecycle commands** (start/stop VMs) target the hypervisor host
- Use Ansible ad-hoc commands with `-m shell` or run playbooks that target `cluster_vms`
- All commands on cluster VMs require sudo/become privileges

**Example Ansible targeting:**
```bash
# Correct - targets cluster VMs
ansible cluster_vms -i deploy/openshift-clusters/inventory.ini -m shell -a "pcs status" -b

# Incorrect - would target hypervisor
ansible hypervisor -i deploy/openshift-clusters/inventory.ini -m shell -a "pcs status" -b
```

**Pacemaker Status (on cluster_vms):**
```bash
sudo pcs status
sudo pcs resource status
sudo pcs constraint list
sudo crm_mon -1
```

**Etcd Container Status (on cluster_vms):**
```bash
sudo podman ps -a --filter name=etcd
sudo podman inspect etcd
sudo podman logs --tail 100 etcd
```

**Etcd Cluster Health (on cluster_vms):**
```bash
sudo podman exec etcd etcdctl member list -w table
sudo podman exec etcd etcdctl endpoint health -w table
sudo podman exec etcd etcdctl endpoint status -w table
```

**System Logs (on cluster_vms):**
```bash
sudo journalctl -u pacemaker --since "1 hour ago" -n 200
sudo journalctl -u corosync --since "1 hour ago" -n 100
sudo journalctl --grep etcd --since "1 hour ago" -n 200
```

**Cluster Attributes (on cluster_vms):**
```bash
sudo crm_attribute --query --name standalone_node
sudo crm_attribute --query --name learner_node
sudo crm_attribute --query --name force_new_cluster --lifetime reboot
```

**OpenShift Cluster Status** (use proxy.env if needed):
```bash
oc get nodes -o wide
oc get co etcd -o yaml
oc get pods -n openshift-etcd
oc get mcp master -o yaml
oc get co --no-headers | grep -v "True.*False.*False"
oc get events -n openshift-etcd --sort-by='.lastTimestamp' | tail -50
```

### 3. Analyze Collected Data

Look for these key issues:

**Cluster Quorum:**
- Corosync quorum status
- Pacemaker partition state
- Node online/offline status

**Etcd Health:**
- Member list consistency
- Leader election status
- Endpoint health
- Learner vs. voting member status
- Cluster ID mismatches between nodes

**Resource State:**
- Etcd resource running status
- Failed actions in Pacemaker
- Resource constraint violations

**Common Error Patterns:**
- Certificate expiration/rotation issues
- Network connectivity problems
- Split-brain scenarios
- Fencing failures
- Data corruption indicators

**OpenShift Integration:**
- Etcd operator status and conditions
- Unexpected etcd pods in openshift-etcd namespace (should not exist in TNF)
- Machine config pool degradation
- Cluster operator degradation related to etcd

### 4. Provide Troubleshooting Procedure

Based on your analysis, provide:

1. **Diagnosis Summary**: Clear statement of identified issues
2. **Root Cause Analysis**: Likely causes based on symptoms
3. **Step-by-Step Remediation**:
   - Ordered steps to resolve issues
   - Specific commands to execute
   - Expected outcomes at each step
   - Rollback procedures if available
4. **Verification Steps**: How to confirm the issue is resolved
5. **Prevention Recommendations**: How to avoid recurrence

## Analysis Guidelines

### Component-Specific Analysis Functions

#### Pacemaker Cluster Analysis

**Key Indicators:**
- Quorum status: `pcs status` shows "quorum" or "no quorum"
- Node status: online, standby, offline, UNCLEAN
- Resource status: Started, Stopped, Failed, Master/Slave
- Failed actions count and descriptions

**Analysis Questions:**
1. Do both nodes show as online in the cluster?
2. Is quorum achieved? (Should show quorum with 2 nodes)
3. Are there any failed actions for the etcd resource?
4. Is stonith enabled and configured correctly?
5. Are there any location/order/colocation constraints preventing etcd from starting?

**Common Issues:**
- **No quorum**: One node is offline or network partition - check corosync logs
- **Failed actions**: Resource failed to start - examine failure reason and run `pcs resource cleanup`
- **UNCLEAN node**: Fencing failed - check fence agent configuration and BMC access

#### Etcd Container Analysis

**Key Indicators:**
- Container state: running, stopped, exited
- Exit code if stopped (0 = clean, non-zero = error)
- Container restart count
- Last log messages from container

**Analysis Questions:**
1. Is the etcd container running on both nodes?
2. If stopped, what was the exit code?
3. What do the last 20 lines of container logs show?
4. Are there certificate errors in the logs?
5. Are there network connectivity errors?

**Common Issues:**
- **Container not found**: Pacemaker hasn't created it yet or resource is stopped
- **Exit code 1**: Check logs for specific error (certs, permissions, corruption)
- **Repeated restarts**: Likely configuration or persistent error - check logs

#### Etcd Cluster Health Analysis

**Key Indicators:**
- Member list: number of members, their status (started/unstarted)
- Endpoint health: healthy/unhealthy, latency
- Endpoint status: leader election, raft index, DB size
- Cluster ID consistency across nodes

**Analysis Questions:**
1. How many members are in the member list?
2. Are all members started?
3. Is there a leader elected?
4. Do both nodes show the same cluster ID in CIB attributes?
5. Are raft indices progressing or stuck?

**Common Issues:**
- **Different cluster IDs**: Nodes are in different etcd clusters - need force-new-cluster
- **No leader**: Split-brain or quorum loss - check network and member list
- **Unstarted member**: Node hasn't joined yet or failed to join - check logs
- **3+ members**: Unexpected member entries from previous configs - need cleanup

#### CIB Attributes Analysis

**Key Indicators:**
- standalone_node: which node (if any) is running alone
- learner_node: which node (if any) is rejoining
- force_new_cluster: which node should bootstrap new cluster
- cluster_id: must match between nodes in healthy state
- member_id: etcd member ID for each node

**Analysis Questions:**
1. Are there conflicting attributes set (e.g., both standalone and learner)?
2. Do cluster_id values match between both nodes?
3. Is force_new_cluster set when it shouldn't be?
4. Are learner/standalone attributes stuck from previous operations?

**Common Issues:**
- **Stuck learner_node**: Previous rejoin didn't complete - may need manual cleanup
- **Mismatched cluster_id**: Nodes diverged - need force-new-cluster recovery
- **Stale force_new_cluster**: Attribute survived reboot when it shouldn't - manual cleanup needed

#### System Logs Analysis

**Key Patterns to Search:**

**Pacemaker Logs:**
- "Failed" - resource failures
- "fencing" - stonith operations
- "could not" - operation failures
- "timeout" - timing issues
- "certificate" - cert problems

**Corosync Logs:**
- "quorum" - quorum changes
- "lost" - connection losses
- "join" - membership changes
- "totem" - ring protocol issues

**Etcd Logs:**
- "panic" - fatal errors
- "error" - general errors
- "certificate" - cert issues
- "member" - membership changes
- "leader" - leadership changes
- "database space exceeded" - quota issues
- "mvcc: database space exceeded" - DB full

### Troubleshooting Decision Tree

Use this decision tree to systematically diagnose issues:

```
START: Etcd not working as expected
│
├─> Can you access cluster VMs via Ansible?
│   ├─ NO → Fix Ansible connectivity first (check inventory, SSH keys, ProxyJump)
│   └─ YES → Continue
│
├─> Is Pacemaker running on both nodes? (systemctl status pacemaker)
│   ├─ NO → Start Pacemaker: systemctl start pacemaker
│   └─ YES → Continue
│
├─> Do both nodes show as online in pcs status?
│   ├─ NO → Check which node is offline
│   │      ├─ Node shows UNCLEAN → Fencing failed
│   │      │  └─ ACTION: Check stonith status, fence agent config, BMC access
│   │      └─ Node shows offline → Network or Pacemaker issue
│   │         └─ ACTION: Check corosync logs, network connectivity
│   └─ YES → Continue
│
├─> Does cluster have quorum? (pcs status shows "quorum")
│   ├─ NO → Investigate corosync/quorum issues
│   │      └─ ACTION: Check corosync logs for membership changes
│   └─ YES → Continue
│
├─> Is etcd resource started? (pcs resource status)
│   ├─ NO → Check for failed actions
│   │      ├─ Failed actions present → Resource failed to start
│   │      │  └─ ACTION: Check failure reason, fix root cause, run pcs resource cleanup
│   │      └─ No failed actions → Check constraints
│   │         └─ ACTION: Review pcs constraint list, check node attributes
│   └─ YES → Continue
│
├─> Is etcd container running on expected nodes? (podman ps)
│   ├─ NO → Container not started or crashed
│   │      └─ ACTION: Check podman logs for errors (certs, corruption, config)
│   └─ YES → Continue
│
├─> Check cluster IDs in CIB attributes on both nodes
│   ├─ DIFFERENT → Nodes are in separate etcd clusters!
│   │      └─ ACTION: Use force-new-cluster helper to recover
│   └─ SAME → Continue
│
├─> Check etcd member list (podman exec etcd etcdctl member list)
│   ├─ Lists unexpected members (>2 members) → Stale members from previous config
│   │      └─ ACTION: Remove stale members with etcdctl member remove
│   ├─ Shows "unstarted" members → Node hasn't joined yet
│   │      └─ ACTION: Check logs on unstarted node, may need cleanup and rejoin
│   └─ Lists 2 members, both started → Continue
│
├─> Check etcd endpoint health (podman exec etcd etcdctl endpoint health)
│   ├─ Unhealthy → Network or performance issues
│   │      └─ ACTION: Check network latency, system load, disk I/O
│   └─ Healthy → Continue
│
├─> Check etcd endpoint status (podman exec etcd etcdctl endpoint status)
│   ├─ No leader → Leadership election failing
│   │      └─ ACTION: Check logs for raft errors, verify member communication
│   ├─ Leader elected but errors in logs → Operational issues
│   │      └─ ACTION: Investigate specific errors (disk full, corruption, etc.)
│   └─ Leader elected, no errors → Cluster appears healthy
│
└─> If still experiencing issues → Check OpenShift integration
    ├─ Etcd operator degraded? (oc get co etcd)
    │  └─ ACTION: Review operator conditions, check for cert rotation, API issues
    └─ Check for related operator degradation (oc get co)
       └─ ACTION: Review degraded operators, may indicate cluster-wide issues
```

### Error Pattern Matching Guidelines

When analyzing logs and status output, look for these common patterns:

#### Certificate Issues
**Symptoms:**
- "certificate has expired" in logs
- "x509: certificate" errors
- etcd container exits immediately
- TLS handshake failures

**Diagnosis:**
```bash
# Check cert expiration on nodes
sudo podman exec etcd ls -la /etc/kubernetes/static-pod-resources/etcd-certs/
# Look at recent cert-related log messages
sudo journalctl --grep certificate --since "2 hours ago"
```

**Resolution:**
- Wait for automatic cert rotation (if in progress)
- Verify etcd operator is healthy and can rotate certs
- Check machine config pool status for cert updates

#### Split-Brain / Cluster ID Mismatch
**Symptoms:**
- Different cluster_id in CIB attributes between nodes
- Nodes can't join each other's cluster
- "cluster ID mismatch" in logs
- Etcd won't start on one or both nodes

**Diagnosis:**
```bash
# Compare cluster IDs
ansible cluster_vms -i inventory.ini -m shell \
  -a "crm_attribute --query --name cluster_id" -b
```

**Resolution (RECOMMENDED):**
```bash
# Use the automated force-new-cluster helper playbook
ansible-playbook helpers/force-new-cluster.yml -i deploy/openshift-clusters/inventory.ini
```

This playbook:
- Takes snapshots for safety
- Clears conflicting CIB attributes
- Auto-detects the etcd leader (or uses first node with running etcd, or falls back to inventory order)
- Removes follower from member list
- Handles all cleanup and recovery steps automatically

#### Resource Failures / Failed Actions
**Symptoms:**
- pcs status shows "Failed Resource Actions"
- Resource shows as "Stopped" but should be running
- Migration failures

**Diagnosis:**
```bash
# Check detailed failure info
sudo pcs resource status --full
sudo pcs resource failcount show etcd
```

**Resolution:**
1. Identify and fix root cause (see logs)
2. Run: `sudo pcs resource cleanup etcd`
3. Verify resource starts successfully

#### Fencing Failures
**Symptoms:**
- Node shows as "UNCLEAN" in pcs status
- "fencing failed" in logs
- Stonith errors
- Cluster can't recover from node failure

**Diagnosis:**
```bash
# Check stonith status and configuration
sudo pcs stonith status
sudo pcs stonith show
# Check fence agent logs
sudo journalctl -u pacemaker --grep fence --since "1 hour ago"
```

**Resolution:**
- Verify BMC/RedFish access from both nodes
- Check fence agent credentials
- Ensure network connectivity to BMC interfaces
- Review stonith timeout settings
- Test fence agent manually: `sudo fence_redfish -a <bmc_ip> -l <user> -p <pass> -o status`

## Key Context

### Cluster States
- **Standalone**: Single node running as "cluster-of-one"
- **Learner**: Node rejoining cluster, not yet voting member
- **Force-new-cluster**: Flag to bootstrap new cluster from single node

### Critical Attributes
- `standalone_node` - Which node is running standalone
- `learner_node` - Which node is rejoining as learner
- `force_new_cluster` - Bootstrap flag (lifetime: reboot)
- `cluster_id` - Etcd cluster ID (must match on both nodes)

### Failure Scenarios

**Graceful Disruption** (4.19+):
- Pacemaker intercepts reboot
- Removes node from etcd cluster
- Cluster continues as single node
- Node resyncs and rejoins on return

**Ungraceful Disruption** (4.20+):
- Unreachable node is fenced (powered off)
- Surviving node restarts etcd as cluster-of-one
- New cluster ID is assigned
- Failed node discards old DB and resyncs on restart

## Available Remediation Tools

**IMPORTANT: Prefer Automated Tools**

When dealing with cluster recovery scenarios (split-brain, mismatched cluster IDs, both nodes down), **always use the automated helper playbook first** before attempting manual recovery:

```bash
ansible-playbook helpers/force-new-cluster.yml -i deploy/openshift-clusters/inventory.ini
```

This playbook handles all the complex steps safely and is the recommended approach. Manual steps should only be used if the playbook is unavailable or fails.

### Pacemaker Resource Cleanup
Use `pcs resource cleanup` to clear failed resource states and retry operations:

```bash
# Clean up etcd resource on specific node
sudo pcs resource cleanup etcd <node-name>

# Clean up etcd resource on all nodes
sudo pcs resource cleanup etcd
```

**When to use:**
- After fixing underlying issues (certificates, network, etc.)
- When resource shows as failed but root cause is resolved
- To retry resource start after transient failures
- After manual CIB attribute changes

### Force New Cluster Helper
Ansible playbook at `helpers/force-new-cluster.yml` automates cluster recovery when both nodes have stopped etcd or cluster IDs are mismatched.

**What it does:**
1. Disables stonith temporarily for safety
2. Takes etcd snapshots on both nodes (if etcd not running)
3. Clears conflicting CIB attributes (learner_node, standalone_node)
4. Sets force_new_cluster attribute on detected leader node
5. Removes follower from etcd member list (if etcd running on leader)
6. Runs `pcs resource cleanup etcd` on both nodes
7. Re-enables stonith
8. Verifies recovery

**Usage:**
```bash
ansible-playbook helpers/force-new-cluster.yml -i deploy/openshift-clusters/inventory.ini
```

**When to use:**
- Both nodes show different etcd cluster IDs
- Etcd is not running on either node and won't start
- After ungraceful disruptions that left cluster in inconsistent state
- Manual recovery attempts have failed
- Need to bootstrap from one node as new cluster

**Precautions:**
- Only use when normal recovery procedures fail
- Ensure follower node can afford to lose its etcd data
- Detected leader will become the source of truth
- This creates a NEW cluster, follower will resync from leader

## Reference Documentation

You have access to these slash commands for detailed information:
- `/etcd:etcd-ops-guide:clustering` - Cluster membership operations
- `/etcd:etcd-ops-guide:recovery` - Recovery procedures
- `/etcd:etcd-ops-guide:monitoring` - Monitoring and health checks
- `/etcd:etcd-ops-guide:failures` - Failure scenarios
- `/etcd:etcd-ops-guide:data_corruption` - Data corruption handling

Pacemaker documentation is available in `.claude/commands/etcd/pacemaker/` directory.

**Podman-etcd Resource Agent Source:**
To consult the resource agent source code, first fetch it from upstream:
```bash
./helpers/etcd/fetch-podman-etcd.sh
```
Then read `.claude/commands/etcd/pacemaker/podman-etcd.txt`

## Output Format

Provide clear, concise diagnostics with:
- Markdown formatting for readability
- Code blocks for commands
- Clear sections for diagnosis, remediation, and verification
- Actionable next steps
- Links to relevant files when referencing code or logs

## Important Notes

- Handle cases where some data collection fails gracefully
- Provide useful output even with partial data
- Warn user clearly if proxy.env is required but missing
- Always use sudo/become for commands on cluster VMs via Ansible
- Be specific about which node to run commands on when relevant
- **CRITICAL: Always target the `cluster_vms` host group for all etcd/Pacemaker operations**
  - Never target the `hypervisor` host for etcd-related commands
  - The hypervisor is only for VM lifecycle management (virsh, kcli commands)
  - All Pacemaker, etcd container, and cluster diagnostics run on cluster VMs
- When cluster API access is unavailable, rely exclusively on Ansible-based VM access
  - This is normal and expected when etcd is down
  - All troubleshooting can be completed without oc commands
