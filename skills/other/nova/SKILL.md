---
name: openstack-nova
description: "OpenStack Nova compute service skill for deploying, configuring, operating, and troubleshooting cloud compute infrastructure. Covers instance lifecycle management (create/stop/start/reboot/resize/migrate/evacuate), compute scheduling with filters and weights, flavor management, live migration procedures, hypervisor management (KVM/QEMU via libvirt), placement service for resource tracking, CPU pinning, NUMA topology, huge pages, cell mapping, VNC/SPICE console access, and capacity planning. Use when deploying compute via Kolla-Ansible, managing instances, debugging scheduler failures, or planning compute capacity."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-22"
      triggers:
        intents:
          - "nova"
          - "compute"
          - "instance"
          - "server"
          - "flavor"
          - "live migration"
          - "hypervisor"
          - "placement"
          - "scheduler"
        contexts:
          - "deploying openstack compute"
          - "managing instances"
          - "troubleshooting compute"
          - "capacity planning"
---

# OpenStack Nova Compute Service

Nova is the compute scheduler and instance lifecycle manager for OpenStack. It receives instance creation requests, selects an appropriate hypervisor through the scheduler and placement service, coordinates with Glance for images, Neutron for networking, and Cinder for volumes, then manages the full instance lifecycle through libvirt/KVM.

Nova operates in a cell-based architecture. Cell0 holds instances that failed to schedule. Cell1 (and beyond) holds running instances. The placement service tracks resource inventories (vCPUs, RAM, disk) independently from Nova, providing accurate capacity data for scheduling decisions.

## Deploy

### Kolla-Ansible Configuration

**globals.yml settings:**

```yaml
# Hypervisor type
nova_compute_virt_type: "kvm"        # Production: hardware KVM
# nova_compute_virt_type: "qemu"     # Nested virt or no VT-x/AMD-V

# Libvirt container
enable_nova_libvirt_container: "yes"

# CPU and RAM allocation ratios
nova_cpu_allocation_ratio: 4.0       # 4:1 vCPU to pCPU (adjust for workload)
nova_ram_allocation_ratio: 1.5       # 1.5:1 vRAM to pRAM
nova_disk_allocation_ratio: 1.0      # 1:1 (do not overcommit disk)

# Console access
nova_console: "novnc"               # Options: novnc, spice
# nova_console: "spice"             # Better performance, less browser support

# Metadata service
enable_nova_metadata: "yes"

# Nova database password
nova_database_password: "{{ vault_nova_database_password }}"
nova_api_database_password: "{{ vault_nova_api_database_password }}"
nova_keystone_password: "{{ vault_nova_keystone_password }}"
```

**Deployment:**

```bash
# Deploy Nova (as part of full deploy or targeted)
kolla-ansible -i inventory deploy --tags nova

# Verify containers
docker ps --filter "name=nova" --format "table {{.Names}}\t{{.Status}}"
# Expected: nova_api, nova_conductor, nova_scheduler, nova_novncproxy,
#           nova_compute, nova_libvirt (all Up)
```

**Post-deploy verification:**

```bash
source /etc/kolla/admin-openrc.sh

# Verify compute service registration
openstack compute service list
# All services should show Status=enabled, State=up

# Verify cell mapping
nova-manage cell_v2 list_cells
# Expected: cell0 and cell1 with transport_url and database

# Verify hypervisor
openstack hypervisor list
# Should show each compute node with vCPUs, Memory, Disk

# Verify placement
openstack resource provider list
# Should match hypervisor list
```

## Configure

### Flavor Management

Flavors define instance resource profiles. Create a standard set:

```bash
# Standard flavors (name, RAM-MB, disk-GB, vCPUs)
openstack flavor create --ram 512   --disk 1   --vcpus 1 m1.tiny
openstack flavor create --ram 2048  --disk 20  --vcpus 1 m1.small
openstack flavor create --ram 4096  --disk 40  --vcpus 2 m1.medium
openstack flavor create --ram 8192  --disk 80  --vcpus 4 m1.large
openstack flavor create --ram 16384 --disk 160 --vcpus 8 m1.xlarge

# Private flavor (restricted to specific project)
openstack flavor create --ram 32768 --disk 320 --vcpus 16 \
  --private m1.xxlarge
openstack flavor set --project dev-team m1.xxlarge
```

### CPU Pinning and NUMA

```ini
# nova.conf [DEFAULT] on compute nodes
vcpu_pin_set = 4-15          # Pin guest vCPUs to physical cores 4-15
                              # Reserve cores 0-3 for host OS

# NUMA topology filter
[filter_scheduler]
enabled_filters = ...,NUMATopologyFilter
```

**Flavor extra specs for NUMA:**

```bash
openstack flavor set m1.large \
  --property hw:cpu_policy=dedicated \
  --property hw:numa_nodes=1
```

### Huge Pages

```bash
# On compute host: allocate huge pages
echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages

# Flavor with huge pages
openstack flavor set m1.large \
  --property hw:mem_page_size=large
```

### Live Migration Configuration

```yaml
# globals.yml
nova_compute_virt_type: "kvm"
enable_nova_libvirt_container: "yes"

# For live migration, all compute nodes need:
# 1. Shared storage (NFS, Ceph) or block migration
# 2. Same CPU model (or cpu_mode=host-model)
# 3. Matching libvirt versions
```

```ini
# nova.conf [libvirt]
live_migration_tunnelled = false     # Use native QEMU migration
live_migration_uri = qemu+tcp://%s/system
cpu_mode = host-model                # Consistent CPU features across hosts
```

### Scheduler Filters and Weights

```ini
# nova.conf [filter_scheduler]
enabled_filters = AvailabilityZoneFilter,ComputeFilter,
  ComputeCapabilitiesFilter,ImagePropertiesFilter,
  ServerGroupAntiAffinityFilter,ServerGroupAffinityFilter,
  AggregateInstanceExtraSpecsFilter,NUMATopologyFilter

# Weight classes determine host preference after filtering
weight_classes = nova.scheduler.weights.ram.RAMWeigher
ram_weight_multiplier = 1.0          # Prefer hosts with more free RAM
```

### VNC Console Configuration

```yaml
# globals.yml
nova_console: "novnc"

# For external access, set the proxy base URL
nova_novncproxy_base_url: "http://controller:6080/vnc_auto.html"
```

## Operate

### Instance Lifecycle

```bash
# Create instance
openstack server create --flavor m1.small --image cirros \
  --network private --security-group default my-instance

# Status checks
openstack server show my-instance -c status -c OS-EXT-STS:vm_state

# Power operations
openstack server stop my-instance
openstack server start my-instance
openstack server reboot my-instance          # Soft reboot
openstack server reboot --hard my-instance   # Hard reboot

# Resize (change flavor)
openstack server resize --flavor m1.medium my-instance
openstack server resize confirm my-instance   # After verification
openstack server resize revert my-instance    # If problems

# Live migration (to specific host or auto-select)
openstack server migrate --live controller2 my-instance
openstack server migrate --live-migration my-instance   # Auto-select

# Cold migration
openstack server migrate my-instance

# Evacuate (from failed host)
openstack server evacuate my-instance --host controller2
```

### Compute Node Maintenance

```bash
# Disable compute node (stop scheduling new instances)
openstack compute service set --disable \
  --disable-reason "Maintenance window" controller nova-compute

# Migrate all instances off the node
nova host-evacuate-live controller

# After maintenance
openstack compute service set --enable controller nova-compute
```

### Orphan Instance Cleanup

```bash
# Find instances in ERROR state
openstack server list --all-projects --status ERROR

# Force delete stuck instances
openstack server delete --force <instance-id>

# Clean orphan ports (instances deleted but ports remain)
openstack port list --device-owner compute:nova --network private
# Cross-reference with server list; delete unattached ports
```

### Aggregate and Availability Zone Management

```bash
# Create host aggregate
openstack aggregate create --zone az1 ssd-aggregate
openstack aggregate set --property ssd=true ssd-aggregate
openstack aggregate add host ssd-aggregate compute-node-1

# Flavor targeting aggregate
openstack flavor set m1.ssd --property aggregate_instance_extra_specs:ssd=true
```

### Image Caching

```ini
# nova.conf [image_cache]
manager_interval = 2400        # Check for stale images every 40 min
remove_unused_base_images = true
remove_unused_original_minimum_age_seconds = 86400  # 24 hours
```

## Troubleshoot

### 1. Instance Stuck in BUILD or ERROR

**Symptoms:** Instance stays in BUILD state or transitions to ERROR immediately.

**Diagnosis:**

```bash
# Check instance fault message
openstack server show <instance-id> -c fault

# Check scheduler logs
docker logs nova_scheduler 2>&1 | tail -50

# Check compute logs
docker logs nova_compute 2>&1 | tail -50
```

**Common causes:**

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| No valid host (scheduler) | Logs: "NoValidHost" | Check placement resources, scheduler filters |
| Image download failure | Compute logs: "ImageNotFound" or download timeout | Verify Glance connectivity, image exists, disk space |
| Libvirt error | Compute logs: "libvirtError" | Check `docker logs nova_libvirt`, verify KVM modules loaded |
| Network setup failure | Compute logs: "VirtualInterfaceCreateException" | Check Neutron agent status, OVS bridges |
| Quota exceeded | API logs: "OverQuota" | `openstack quota show <project>` and adjust |

### 2. Live Migration Failures

**Symptoms:** Migration starts but fails partway through, or never begins.

**Diagnosis:**

```bash
openstack server migration list --server <instance-id>
docker logs nova_compute 2>&1 | grep -i "migration\|migrate"
```

**Common causes:**

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| No shared storage | "Cannot migrate with non-shared storage" | Use `--block-migration` or configure shared storage (NFS/Ceph) |
| CPU incompatibility | "Unable to connect to qemu" or CPU feature mismatch | Set `cpu_mode = host-model` in nova.conf, ensure same CPU vendor |
| libvirt version mismatch | "Incompatible libvirt" in logs | Upgrade libvirt on older node |
| Network config mismatch | Migration completes but instance loses connectivity | Ensure consistent OVS bridge naming and tunnel endpoints |

### 3. "No Valid Host" Errors

**Symptoms:** `openstack server create` returns "No valid host was found."

**Diagnosis:**

```bash
# Check placement resource inventory
openstack resource provider inventory list <compute-rp-uuid>

# Check resource usage
openstack resource provider usage show <compute-rp-uuid>

# Verify scheduler filters are not eliminating all hosts
docker logs nova_scheduler 2>&1 | grep -i "filter\|no valid"
```

**Fix:** Identify which filter eliminated all candidates. Common: insufficient RAM/vCPU/disk in placement, availability zone mismatch, aggregate filter mismatch, anti-affinity constraint.

### 4. Console Access Failures

**Symptoms:** VNC console shows "Failed to connect" or blank screen.

**Diagnosis:**

```bash
# Get console URL
openstack console url show my-instance

# Check novncproxy
docker logs nova_novncproxy 2>&1 | tail -20

# Verify port 6080 is open
ss -tlnp | grep 6080
```

**Fix:**
- Firewall blocking port 6080: `firewall-cmd --add-port=6080/tcp --permanent`
- Wrong proxy base URL: Check `nova_novncproxy_base_url` in globals.yml
- Instance not running: verify `openstack server show -c status`

### 5. Compute Service Down

**Symptoms:** `openstack compute service list` shows State=down for a compute node.

**Diagnosis:**

```bash
# Check Nova compute container
docker ps --filter "name=nova_compute"
docker logs nova_compute 2>&1 | tail -50

# Check libvirt
docker logs nova_libvirt 2>&1 | tail -20

# Check hypervisor resources
openstack hypervisor show <hostname>
```

**Fix:**
- Container crashed: `docker restart nova_compute nova_libvirt`
- libvirt socket missing: check `/var/run/libvirt/libvirt-sock` exists
- KVM module not loaded: `lsmod | grep kvm` -- load with `modprobe kvm_intel` or `kvm_amd`
- Disk full on compute: `df -h /var/lib/nova/instances`

### 6. Cell Mapping Issues

**Symptoms:** Instances exist in database but not visible via API. New instances not appearing.

**Diagnosis:**

```bash
# List cells
nova-manage cell_v2 list_cells
# Check: cell1 has correct transport_url and database connection

# Discover new hosts
nova-manage cell_v2 discover_hosts --verbose
```

**Fix:**
- Missing host mapping: `nova-manage cell_v2 discover_hosts`
- Instance in cell0 (scheduling failed): check cell0 database for error records
- Database connection string wrong: verify `[database]` in nova.conf matches cell mapping

## Integration Points

| Service | Integration | Mechanism |
|---------|-------------|-----------|
| **Keystone** | Authentication for all API calls; service user for internal calls | keystonemiddleware in nova-api |
| **Glance** | Image download for instance boot; snapshot upload | REST API via service catalog endpoint |
| **Neutron** | Port creation/deletion for instance networking; security groups | REST API; nova calls Neutron to allocate ports during instance build |
| **Cinder** | Volume attach/detach; boot-from-volume | REST API; os-brick for iSCSI/FC/NFS attachment on compute |
| **Placement** | Resource inventory tracking; allocation claims during scheduling | REST API; scheduler claims resources before instance build |
| **Metadata** | Instance cloud-init configuration; user-data, vendor-data | HTTP service on link-local 169.254.169.254 via Neutron router |

## NASA SE Cross-References

| SE Phase | Nova Activity | Reference |
|----------|---------------|-----------|
| Phase B (Preliminary Design) | Design compute architecture: virt type, allocation ratios, scheduler filters, flavor matrix | SP-6105 SS 4.3-4.4 |
| Phase C (Final Design) | Configure Nova in globals.yml: hypervisor settings, VNC, placement, cell mapping | SP-6105 SS 5.1 |
| Phase D (Integration & Test) | Verify: `openstack server create` end-to-end, live migration test, scheduler filter validation | SP-6105 SS 5.2-5.3 |
| Phase E (Operations) | Instance lifecycle management, compute node maintenance, capacity monitoring, image cache management | SP-6105 SS 5.4-5.5, NPR 7123.1 SS 5.4 |
