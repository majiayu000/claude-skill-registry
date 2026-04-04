---
name: openstack-capacity
description: "OpenStack capacity planning operations skill for resource planning, quota management, and scaling decisions. Covers compute capacity (allocation ratios, vCPU/RAM utilization, host aggregates, availability zones), storage capacity (Cinder pool sizing, thin provisioning, Glance storage, Swift rings), network capacity (floating IP pools, port quotas, subnet sizing), project quota management (templates for small/medium/large profiles), flavor sizing strategy, utilization analysis with placement service, growth forecasting from historical metrics, and right-sizing recommendations for underutilized resources."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-23"
      triggers:
        intents:
          - "capacity"
          - "quota"
          - "scaling"
          - "resources"
          - "utilization"
          - "allocation ratio"
          - "flavor"
          - "sizing"
          - "growth"
          - "density"
        contexts:
          - "capacity planning"
          - "managing quotas"
          - "scaling openstack"
          - "resource utilization analysis"
---

# OpenStack Capacity Planning -- Resource Management Operations

Capacity planning is proactive operations -- the discipline of preventing outages before they happen by ensuring the cloud has sufficient resources to serve its users. A reactive operator discovers capacity problems when `openstack server create` returns "No valid host found." A proactive operator sees the trend weeks before and plans accordingly.

The three capacity domains are **compute** (vCPU, RAM, local disk), **storage** (volume GB, snapshots, images, objects), and **network** (floating IPs, ports, subnets, bandwidth). Each domain has its own exhaustion symptoms, its own metrics, and its own expansion procedures.

Allocation ratios create overcommit flexibility -- a host with 16 physical cores and a 4:1 CPU allocation ratio offers 64 vCPUs. This works because most workloads are idle most of the time. The art of capacity planning is setting ratios high enough to maximize density but low enough that contention does not degrade performance.

This skill maps to NASA SE Phase E sustainment and resource management. In NASA terms, capacity planning is the operational activity that ensures the system continues to meet its Measures of Performance (MOPs) throughout its operational life.

## Deploy

### Capacity Management Tooling

**Placement service** -- the authoritative source for resource inventory:

```bash
# List all resource providers (one per compute node)
openstack resource provider list

# Show resource inventory for a specific provider
openstack resource provider inventory list <provider-uuid>
# Shows: VCPU, MEMORY_MB, DISK_GB with total, reserved, min_unit, max_unit, allocation_ratio

# Show current allocations (what is consumed)
openstack resource provider usage show <provider-uuid>
```

**Quota system** -- per-project resource limits:

```bash
# Show default quotas
openstack quota show --default

# Show quotas for a specific project
openstack quota show <project-name>
```

**Allocation ratios** (in `globals.yml`):

```yaml
# Compute overcommit ratios
nova_cpu_allocation_ratio: 4.0     # 4 vCPUs per physical core
nova_ram_allocation_ratio: 1.5     # 1.5x physical RAM
nova_disk_allocation_ratio: 1.0    # No disk overcommit (recommended)

# These translate to placement inventories:
# VCPU: total = cores * ratio
# MEMORY_MB: total = ram_mb * ratio
# DISK_GB: total = disk_gb * ratio
```

**Initial resource survey** -- baseline capacity before entering operations:

```bash
# Compute capacity
openstack hypervisor stats show
# Key fields: vcpus, vcpus_used, memory_mb, memory_mb_used, local_gb, local_gb_used

# Storage capacity
openstack volume service list
cinder get-pools --detail  # Shows per-backend capacity

# Network capacity
openstack floating ip list --long  # Count used vs available
openstack network list             # Count networks
```

## Configure

### Compute Capacity

**Allocation ratios** -- when to overcommit vs reserve:

| Workload Type | CPU Ratio | RAM Ratio | Rationale |
|---------------|-----------|-----------|-----------|
| Dev/test | 8:1 to 16:1 | 1.5:1 | Workloads mostly idle, density matters |
| Web servers | 4:1 to 8:1 | 1.0:1 | CPU bursty, RAM steady-state |
| Databases | 1:1 to 2:1 | 1.0:1 | CPU and RAM sensitive to contention |
| HPC / ML | 1:1 | 1.0:1 | No overcommit; dedicated resources |

**Host aggregates** for workload separation:

```bash
# Create host aggregates for different workload types
openstack aggregate create --zone general-az general-compute
openstack aggregate create --zone database-az database-compute

# Add hosts to aggregates
openstack aggregate add host general-compute compute01
openstack aggregate add host database-compute compute02

# Set metadata for flavor targeting
openstack aggregate set --property workload=general general-compute
openstack aggregate set --property workload=database database-compute
```

**Availability zones** for fault domain separation:

```bash
# List availability zones
openstack availability zone list --compute
```

### Storage Capacity

**Cinder backend pool sizing:**

```bash
# Check backend pool capacity
cinder get-pools --detail
# Key fields: total_capacity_gb, free_capacity_gb, provisioned_capacity_gb
# provisioned_capacity_gb can exceed total_capacity_gb with thin provisioning
```

**Thin provisioning ratios:**

```yaml
# In Cinder backend config (LVM example)
# lvm_max_over_subscription_ratio: 1.5  # Allow 50% overcommit
# Thin provisioning only works with LVM thin pools or Ceph
```

**Glance storage limits:**

```bash
# Check image storage usage
openstack image list --long -c Name -c Size
# Sum all image sizes; compare against storage backend capacity
# Images are stored in /var/lib/glance/images/ (default) or Swift
```

**Swift ring sizing:**

```bash
# Check Swift ring capacity
swift-ring-builder /etc/kolla/swift/account.builder
# Shows: device count, partition count, replicas, balance
```

### Network Capacity

**Floating IP pool sizing:**

```bash
# Check floating IP usage
openstack floating ip list -c 'Floating IP Address' -c 'Fixed IP Address'
# IPs with no fixed_ip_address are allocated but unused (potential waste)

# Count available IPs in the pool
openstack subnet show provider-subnet -c allocation_pools
# Calculate: pool_end - pool_start + 1 - allocated_count = remaining
```

**DHCP subnet sizing:** plan for the maximum number of instances per subnet. A /24 gives ~250 usable addresses. A /20 gives ~4000.

**Port quotas and network quotas:**

```bash
# Check current port usage
openstack port list --project <project> | wc -l

# Set port and network quotas
openstack quota set --ports 200 --networks 20 --subnets 40 <project>
```

### Project Quota Templates

| Profile | Instances | vCPUs | RAM (MB) | Volumes | Volume GB | Floating IPs | Networks | Ports |
|---------|-----------|-------|----------|---------|-----------|-------------|----------|-------|
| Small | 5 | 10 | 20480 | 10 | 200 | 2 | 2 | 50 |
| Medium | 20 | 50 | 102400 | 40 | 1000 | 10 | 5 | 200 |
| Large | 50 | 200 | 512000 | 100 | 5000 | 25 | 10 | 500 |

```bash
# Apply a quota profile
openstack quota set --instances 20 --cores 50 --ram 102400 \
  --volumes 40 --gigabytes 1000 --floating-ips 10 \
  --networks 5 --ports 200 <project>
```

### Flavor Design

**Sizing strategy:** Use powers of 2 for RAM, matching common workload profiles.

| Flavor | vCPUs | RAM (MB) | Root Disk (GB) | Use Case |
|--------|-------|----------|----------------|----------|
| m1.tiny | 1 | 512 | 1 | Testing, CI/CD agents |
| m1.small | 1 | 2048 | 20 | Light web apps |
| m1.medium | 2 | 4096 | 40 | Standard workloads |
| m1.large | 4 | 8192 | 80 | Application servers |
| m1.xlarge | 8 | 16384 | 160 | Databases, caches |
| c1.large | 8 | 4096 | 40 | CPU-intensive |
| r1.large | 4 | 16384 | 40 | Memory-intensive |

```bash
# Create a flavor
openstack flavor create m1.medium --vcpus 2 --ram 4096 --disk 40 --public

# Target flavor to host aggregate
openstack flavor set --property aggregate_instance_extra_specs:workload=general m1.medium
```

## Operate

### Capacity Review Procedures

**Weekly utilization check:**

```bash
# Compute utilization
openstack hypervisor stats show
# Calculate: vcpus_used / vcpus * 100 = CPU utilization %
# Calculate: memory_mb_used / memory_mb * 100 = RAM utilization %
# Alert threshold: >70% sustained = plan expansion

# Storage utilization
cinder get-pools --detail
# Calculate: (total_capacity_gb - free_capacity_gb) / total_capacity_gb * 100
# Alert threshold: >80% = plan expansion

# Floating IP utilization
TOTAL=$(openstack floating ip list | wc -l)
USED=$(openstack floating ip list -c 'Fixed IP Address' --format value | grep -v None | wc -l)
echo "Floating IPs: $USED used of $TOTAL allocated"
```

**Monthly trend analysis:** Compare current week's utilization against the previous 4 weeks. Calculate linear growth rate. Project when each resource will cross the alert threshold.

**Quarterly growth planning:** Review trend data, plan hardware procurement or configuration changes (adjust allocation ratios, add compute nodes, expand storage backends).

### Quota Management

```bash
# Adjust project quotas
openstack quota set --instances 30 --cores 100 <project>

# Update default quotas (affects new projects)
openstack quota set --class --instances 10 --cores 20 default

# Show quota usage for a project
openstack quota show <project> --usage
```

### Resource Utilization Reporting

**Compute report:**

```bash
# Per-hypervisor utilization
openstack hypervisor list --long
# Fields: vCPUs (used/total), Memory MB (used/total), Local GB (used/total)

# Per-instance resource consumption
openstack server list --all-projects --long -c Name -c Flavor -c Host -c Status
```

**Storage report:**

```bash
# Volume usage by project
openstack volume list --all-projects -c Name -c Size -c Status -c Project
# Sum sizes per project; identify volumes in 'available' state (potentially unused)
```

**Network report:**

```bash
# Floating IP usage by project
openstack floating ip list --all-projects -c 'Floating IP Address' -c 'Fixed IP Address' -c Project
# IPs with no fixed IP = waste
```

### Growth Forecasting

Use historical metrics from Prometheus/Grafana (monitoring skill) to project resource exhaustion:

- **Linear projection:** If vCPU usage grew 10% per month over the last 3 months, and current utilization is 60%, the 80% threshold will be crossed in 2 months
- **Seasonal adjustment:** Development teams create more instances on weekdays; plan for peak, not average
- **Step functions:** A new project onboarding may add 20 instances overnight -- plan for known upcoming events

### Right-Sizing Recommendations

```bash
# Find instances with low CPU utilization (requires monitoring data)
# Check Prometheus: avg(rate(cpu_usage[7d])) by (instance_name)
# Instances averaging <10% CPU may be oversized

# Find unattached volumes (allocated but unused storage)
openstack volume list --status available --all-projects
# These consume capacity but serve no workload

# Find orphaned floating IPs (allocated but not associated)
openstack floating ip list -c 'Fixed IP Address' --format value | grep -c None
```

## Troubleshoot

### "No Valid Host" Errors

**Symptoms:** `openstack server create` fails with "No valid host was found" despite the cloud appearing to have resources.

**Resolution steps:**
1. Check placement inventory: `openstack resource provider usage show <provider-uuid>` -- compare used vs total for VCPU, MEMORY_MB, DISK_GB
2. Check if allocation ratios have been applied: `openstack resource provider inventory list <provider-uuid>` -- the `allocation_ratio` column must match `globals.yml`
3. Check host aggregates: if the flavor has extra specs targeting an aggregate, verify the aggregate has hosts with capacity
4. Check compute service status: `openstack compute service list` -- any service marked `disabled` reduces available capacity
5. Check cells: `nova-manage cell_v2 list_cells` -- verify all cells are registered and database is accessible

### Quota Exceeded but Resources Available

**Symptoms:** User gets "Quota exceeded" error but the cloud has physical capacity remaining.

**Resolution steps:**
1. Check project quota: `openstack quota show <project> --usage` -- compare `in_use` against `limit`
2. Identify the exhausted resource: instances, cores, ram, gigabytes, or floating-ips
3. Increase quota: `openstack quota set --<resource> <new-limit> <project>`
4. Check for orphaned resources: instances in ERROR state, volumes in ERROR state -- these consume quota
5. Clean up: `openstack server delete <error-instance>` to free quota

### Storage Allocation Failures

**Symptoms:** Volume creation fails with "Not enough free space" or "VolumeSizeExceedsAvailableQuota."

**Resolution steps:**
1. Check backend capacity: `cinder get-pools --detail` -- compare `free_capacity_gb` against requested size
2. Check thin provisioning: if `provisioned_capacity_gb` exceeds `total_capacity_gb`, the overcommit ratio is exceeded
3. Check volume quotas: `openstack quota show <project> --usage` -- volumes and gigabytes limits
4. Identify unused volumes: `openstack volume list --status available --all-projects` -- delete or archive
5. Identify snapshot overhead: `openstack volume snapshot list --all-projects` -- snapshots consume backend storage

### Floating IP Pool Exhausted

**Symptoms:** `openstack floating ip create` fails with "No more IP addresses available on network."

**Resolution steps:**
1. Count allocated IPs: `openstack floating ip list | wc -l`
2. Check subnet allocation pool: `openstack subnet show <provider-subnet> -c allocation_pools` -- calculate total pool size
3. Find leaked IPs (allocated but not associated): `openstack floating ip list -c ID -c 'Fixed IP Address' | grep None`
4. Release leaked IPs: `openstack floating ip delete <ip-id>` for each unassociated IP
5. Expand pool: update the subnet allocation pool with a wider range, or add a new provider subnet

### Unexpected Resource Consumption

**Symptoms:** Resources consumed faster than expected, utilization jumps without corresponding user activity.

**Resolution steps:**
1. Check for orphaned instances: `openstack server list --all-projects --status ERROR` -- error instances consume resources
2. Check for zombie instances: `openstack server list --all-projects --status SHUTOFF` -- shut off instances consume RAM and disk quotas
3. Check for leftover volumes: `openstack volume list --all-projects --status available` -- volumes not attached to any instance
4. Check for orphaned ports: `openstack port list --status DOWN --all-projects` -- ports consuming network quotas
5. Audit per-project usage: `openstack limits show --absolute --project <project>` -- compare against expected allocation

## Integration Points

- **Monitoring skill:** Utilization metrics and trend data from Prometheus/Grafana feed every capacity decision. Without monitoring data, capacity planning is guesswork. The monitoring skill provides the metrics pipeline; this skill interprets those metrics for planning decisions.
- **Nova skill:** Compute capacity management -- allocation ratios, host aggregates, flavors, and placement service. Nova controls how compute resources are divided among instances. Capacity changes often require Nova configuration updates.
- **Cinder skill:** Storage capacity management -- backend pool sizing, thin provisioning ratios, volume quotas. Cinder controls how storage resources are allocated. Storage capacity changes require Cinder backend reconfiguration.
- **Neutron skill:** Network capacity management -- floating IP pools, port quotas, subnet sizing. Neutron controls how network resources are allocated. Network capacity changes require subnet and quota adjustments.
- **Backup skill:** Backup storage consumption must be included in total capacity planning. Snapshots, volume backups, and database dumps all consume storage that is not visible in Cinder's capacity pool but affects the underlying storage backend.
- **All core skills:** Resource quotas affect every OpenStack service. Quota templates in this skill define limits that Nova (instances, vCPUs, RAM), Cinder (volumes, gigabytes), and Neutron (floating IPs, networks, ports) all enforce.

## NASA SE Cross-References

| SE Phase | Capacity Planning Activity | Reference |
|----------|---------------------------|-----------|
| Phase A (Concept Development) | Initial capacity requirements: determine how many instances, how much storage, how many floating IPs the cloud must support based on stakeholder expectations. Define capacity MOPs (Measures of Performance). | SP-6105 SS 4.2 (Technical Requirements Definition) |
| Phase B (Preliminary Design) | Capacity design: select hardware, set allocation ratios, design quota templates, plan flavor matrix. Trade study: overcommit vs reserved resources for each workload type. | SP-6105 SS 4.3-4.4 (Logical Decomposition and Design Solution) |
| Phase E (Operations) | Operational capacity management: weekly utilization checks, monthly trend analysis, quarterly growth planning. Adjust quotas, allocation ratios, and flavors as workload patterns evolve. | SP-6105 SS 5.4-5.5 (Product Validation and Transition) |
| Technical Management | Resource allocation planning: ensure capacity decisions are documented, tracked, and reviewed. Capacity changes follow the configuration management process. | SP-6105 SS 6.1 (Technical Planning -- resource allocation) |
