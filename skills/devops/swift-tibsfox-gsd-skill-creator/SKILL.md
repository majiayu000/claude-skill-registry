---
name: openstack-swift
description: "OpenStack Swift object storage service. Provides S3-compatible distributed object storage with containers, ACLs, ring architecture, eventual consistency, large object support (SLO/DLO), tempURL for unauthenticated access, object versioning, and object expiry. Use for deploying, configuring, operating, and troubleshooting OpenStack object storage."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-23"
      triggers:
        intents:
          - "swift"
          - "object storage"
          - "container"
          - "s3 compatible"
          - "large object"
          - "ring"
          - "ACL"
          - "tempurl"
        contexts:
          - "deploying openstack object storage"
          - "managing swift containers"
          - "troubleshooting object storage"
          - "configuring s3 compatibility"
---

# OpenStack Swift -- Object Storage Service

Swift provides distributed object storage with an HTTP-accessible API. Unlike block storage (Cinder), which provides attached devices, Swift stores objects (files) in containers (buckets) accessible via REST API calls. Swift is S3-compatible when the `s3api` middleware is enabled, making it a drop-in replacement for AWS S3 in many applications.

## Architecture

Swift uses a **ring architecture** to determine where objects are stored. Even in a single-node deployment, understanding rings is important because they control data placement and replication.

- **Rings:** Swift maintains three rings -- account, container, and object. Each ring maps a partition to a set of devices (disks). The ring builder calculates this mapping based on the number of replicas, partition power, and device weights.
- **Partition power:** Determines how many partitions exist (2^power). Higher partition power = more granular distribution but more memory usage. Single-node typically uses partition power 10 (1024 partitions).
- **Replicas:** The number of copies of each object. Production uses 3 replicas across failure zones. Single-node uses 1 replica (no redundancy benefit with one node).
- **Eventual consistency:** Swift is designed around eventual consistency. After a write, reads from different nodes may temporarily return different results. Replicator and auditor processes converge state over time.

**Service components:**

- `swift-proxy`: The API frontend. Receives HTTP requests, authenticates via Keystone, routes requests to the appropriate storage nodes using the rings.
- `swift-account`: Manages account-level metadata and container listings.
- `swift-container`: Manages container-level metadata and object listings.
- `swift-object`: Stores and retrieves actual object data on disk.
- Auxiliary services: `object-replicator`, `object-auditor`, `container-updater`, `account-reaper` (background consistency processes).

## Deploy

### Kolla-Ansible Configuration

Key settings in `globals.yml`:

```yaml
# Enable Swift
enable_swift: "yes"

# Disk configuration for Swift storage
# Kolla-Ansible expects dedicated disks or partitions
# Format: label:device pairs
swift_devices_name: "KOLLA_SWIFT_DATA"

# Number of replicas (1 for single-node)
swift_default_replication_count: 1
```

### Disk Setup for Swift

Swift requires dedicated storage devices. For Kolla-Ansible:

```bash
# Format and label a disk for Swift
parted /dev/sdc mklabel gpt
parted /dev/sdc mkpart primary xfs 0% 100%
mkfs.xfs -f /dev/sdc1
# Label must match swift_devices_name
xfs_admin -L KOLLA_SWIFT_DATA /dev/sdc1

# Alternatively, use a loop device for testing
dd if=/dev/zero of=/srv/swift-disk bs=1M count=10240
mkfs.xfs -f /srv/swift-disk
# Mount and label for Kolla-Ansible discovery
```

### Ring Building (Single-Node)

Kolla-Ansible builds rings during deployment. For single-node with 1 replica:

```bash
# Kolla-Ansible handles ring building, but for manual ring management:
# Account ring
swift-ring-builder account.builder create 10 1 1
swift-ring-builder account.builder add --region 1 --zone 1 \
  --ip 10.0.0.1 --port 6202 --device sdc1 --weight 100
swift-ring-builder account.builder rebalance

# Container ring (same pattern)
swift-ring-builder container.builder create 10 1 1
swift-ring-builder container.builder add --region 1 --zone 1 \
  --ip 10.0.0.1 --port 6201 --device sdc1 --weight 100
swift-ring-builder container.builder rebalance

# Object ring (same pattern)
swift-ring-builder object.builder create 10 1 1
swift-ring-builder object.builder add --region 1 --zone 1 \
  --ip 10.0.0.1 --port 6200 --device sdc1 --weight 100
swift-ring-builder object.builder rebalance
```

### Container and Service Verification

```bash
# List Swift containers
docker ps --format '{{.Names}}' | grep swift

# Expected containers:
# swift_proxy_server, swift_account_server, swift_container_server,
# swift_object_server, swift_account_reaper, swift_object_expirer,
# swift_rsyncd

# Verify Swift is operational
openstack object store account show
# Should return account info with container count and bytes used

# Check S3 API availability (if s3api middleware is enabled)
# Use AWS CLI or s3cmd with OpenStack credentials
```

## Configure

### Storage Policies

Storage policies define different tiers of storage with different replication counts, erasure coding parameters, or device assignments.

```ini
# In swift.conf (through Kolla-Ansible config override)
[storage-policy:0]
name = standard
default = yes

# Additional policies for different tiers:
# [storage-policy:1]
# name = high-durability
# (requires separate ring and additional devices)
```

### S3 API Middleware

Swift's `s3api` middleware provides S3-compatible API access:

```ini
# In proxy-server.conf pipeline (Kolla-Ansible configures this when enabled)
# pipeline = ... s3api s3token keystoneauth ... proxy-server
```

Using the S3 API:

```bash
# Create EC2 credentials for S3 access
openstack ec2 credentials create

# Use with AWS CLI
aws configure
# AWS Access Key ID: <ec2-access>
# AWS Secret Access Key: <ec2-secret>
# Default region: RegionOne

# Use with endpoint URL
aws --endpoint-url http://<swift-proxy>:8080 s3 ls
aws --endpoint-url http://<swift-proxy>:8080 s3 mb s3://my-bucket
aws --endpoint-url http://<swift-proxy>:8080 s3 cp file.txt s3://my-bucket/
```

### Container ACLs

Swift provides container-level and account-level access control:

```bash
# Make a container publicly readable
swift post my-container --read-acl ".r:*,.rlistings"

# Grant read access to a specific project
swift post my-container --read-acl "<project-id>:*"

# Grant write access to a specific user
swift post my-container --write-acl "<project-id>:<user-id>"

# Remove ACLs
swift post my-container --read-acl "" --write-acl ""
```

### TempURL Configuration

TempURL allows generating time-limited URLs for unauthenticated access:

```bash
# Set the tempurl key on the account
swift post -m "Temp-URL-Key: mysecretkey"

# Generate a tempurl (valid for 3600 seconds)
swift tempurl GET 3600 /v1/AUTH_<account>/my-container/my-object mysecretkey
```

### Large Object Support

Swift has a 5GB limit per single object. For larger files, use segmented uploads:

- **SLO (Static Large Object):** Upload segments, then create a manifest listing all segments. Immutable after creation.
- **DLO (Dynamic Large Object):** Upload segments with a common prefix. The manifest points to the prefix. Segments can be modified independently.

```bash
# SLO upload using swift CLI
swift upload my-container --segment-size 1073741824 large-file.iso
# Creates segments in my-container_segments/ and a manifest in my-container/

# DLO: manually upload segments with shared prefix
swift upload my-container_segments segment-001 segment-002 segment-003
swift upload my-container large-file --header "X-Object-Manifest: my-container_segments/segment-"
```

### Object Versioning

```bash
# Enable versioning on a container
swift post my-container -H "X-Versions-Location: my-container-versions"
# Create the versions container
swift post my-container-versions

# Now every overwrite of an object in my-container stores the
# previous version in my-container-versions
```

### Object Expiry

```bash
# Set an object to expire after 86400 seconds (24 hours)
swift post my-container my-object -H "X-Delete-After: 86400"

# Set an object to expire at a specific Unix timestamp
swift post my-container my-object -H "X-Delete-At: 1771900000"
```

### Rate Limiting

```ini
# In proxy-server.conf (through config override)
[filter:ratelimit]
account_ratelimit = 100    # requests per second per account
container_ratelimit_0 = 50  # requests per second for containers with 0+ objects
```

## Operate

### Container and Object CRUD

```bash
# Create a container
openstack container create my-container

# Upload an object
openstack object create my-container local-file.txt

# List containers and objects
openstack container list
openstack object list my-container

# Download an object
openstack object save my-container remote-file.txt --file local-copy.txt

# Delete an object and container
openstack object delete my-container remote-file.txt
openstack container delete my-container
```

### Using the Swift CLI

The `swift` CLI provides additional functionality beyond the OpenStack unified CLI:

```bash
# Upload with metadata
swift upload my-container file.txt --header "X-Object-Meta-Author: admin"

# Show container metadata
swift stat my-container

# Show object metadata
swift stat my-container file.txt

# Bulk delete
swift delete my-container --prefix "logs/"
```

### Storage Usage Reporting

```bash
# Account-level usage
openstack object store account show
# Shows: Account, Containers, Objects, Bytes, Content-Type

# Per-container usage
swift stat my-container
# Shows: Object Count, Bytes Used, Read/Write ACLs
```

### Ring Rebalancing

When adding or removing devices (relevant for future multi-node expansion):

```bash
# Add a new device to the object ring
swift-ring-builder object.builder add --region 1 --zone 2 \
  --ip 10.0.0.2 --port 6200 --device sdb1 --weight 100

# Rebalance (distributes partitions to new devices)
swift-ring-builder object.builder rebalance

# Distribute updated ring files to all nodes
# Kolla-Ansible: kolla-ansible -i inventory reconfigure -t swift
```

## Troubleshoot

### Object Upload Failures

**Symptoms:** PUT requests return 503 Service Unavailable or timeout; swift upload hangs.

**Diagnostic sequence:**

1. **Check storage space:** `df -h` on Swift storage devices. If devices are full (>90%), Swift returns 503.
2. **Check ring configuration:** `swift-ring-builder object.builder` to verify devices are listed with appropriate weight. Missing devices prevent uploads.
3. **Check proxy logs:** `docker logs swift_proxy_server 2>&1 | tail -50`. Look for connection refused errors to object servers.
4. **Check object server:** `docker logs swift_object_server 2>&1 | tail -50`. Look for disk I/O errors or permission issues.
5. **Check XFS filesystem:** `xfs_repair -n /dev/sdc1`. XFS corruption can cause silent write failures. Note: `xfs_repair` requires the filesystem to be unmounted.

### S3 API Compatibility Issues

**Symptoms:** AWS CLI or S3 clients return authentication errors, "unsupported operation," or unexpected response format.

**Diagnostic sequence:**

1. **Check middleware pipeline:** Verify `s3api` and `s3token` are in the proxy-server pipeline. `docker exec swift_proxy_server grep pipeline /etc/swift/proxy-server.conf`.
2. **Check EC2 credentials:** `openstack ec2 credentials list`. Credentials must exist for the user.
3. **Signature version:** Swift s3api supports both V2 and V4 signatures. If using V4, ensure the region is correct. Some older clients default to V2.
4. **Unsupported operations:** Swift's S3 API does not support all S3 features (e.g., bucket policies, object lock, some multipart upload options). Check the Swift s3api compatibility matrix.
5. **Check endpoint URL:** The S3 endpoint is typically on port 8080 (same as Swift API), not 443. Ensure the client is configured with the correct endpoint.

### Container Listing Empty or Incomplete

**Symptoms:** Container exists and objects were uploaded, but listing returns empty or partial results.

**Diagnostic sequence:**

1. **Eventual consistency:** Swift container listings are eventually consistent. After a burst of uploads, the container server may not have processed all updates yet. Wait 30-60 seconds and retry.
2. **Container server health:** `docker logs swift_container_server 2>&1 | tail -50`. If the container server is overloaded or has disk issues, updates may be delayed.
3. **Container updater:** `docker logs swift_container_updater 2>&1 | tail -20`. The updater processes deferred container updates. Check for errors.
4. **Object count vs listing:** `swift stat my-container` shows the stored object count. If the count is correct but listing is wrong, the container database may need repair.

### Permission Denied on Container Operations

**Symptoms:** 403 Forbidden when creating containers, uploading objects, or reading container contents.

**Diagnostic sequence:**

1. **Check ACLs:** `swift stat my-container` -- look at Read ACL and Write ACL fields. Verify the user/project has appropriate access.
2. **Check Keystone role:** `openstack role assignment list --user <user> --project <project>`. User needs at least `member` role (or `swiftoperator` if configured).
3. **Check account ownership:** The Swift account maps to a Keystone project. Verify the user is a member of the correct project.
4. **Check reseller prefix:** Swift uses `AUTH_` prefix by default for Keystone integration. Ensure the account name matches `AUTH_<project-id>`.
5. **Check proxy auth pipeline:** `docker exec swift_proxy_server grep -A5 keystoneauth /etc/swift/proxy-server.conf`. Verify `operator_roles` includes the user's role.

### Ring Builder Errors

**Symptoms:** Ring rebalance fails, or Swift cannot find devices.

**Diagnostic sequence:**

1. **No devices added:** `swift-ring-builder <ring>.builder` -- if no devices are listed, none were added to the ring. Add devices before rebalancing.
2. **Partition power mismatch:** All three rings (account, container, object) must use the same partition power. Mismatched rings cause routing failures.
3. **Minimum partition hours:** Ring builder enforces a minimum time between rebalances. If rebalancing too frequently, wait for the cooldown period.
4. **Weight zero:** Devices with weight 0 are being drained. Ensure at least one device has positive weight.
5. **Ring file distribution:** After rebalancing, ring files (`.ring.gz`) must be distributed to all Swift nodes. On single-node, this happens automatically. Multi-node requires manual or Kolla-Ansible reconfigure.

## Integration Points

- **Keystone:** All Swift API calls authenticate through Keystone. Swift uses Keystone tokens for native API access and EC2 credentials for S3 API access. The `keystoneauth` middleware in the proxy pipeline maps Keystone roles to Swift ACL concepts. Swift accounts map to Keystone projects via the `AUTH_<project-id>` naming convention.
- **Glance:** Swift can serve as a backend store for Glance images. When configured, Glance stores image data as objects in Swift containers, providing object-level durability for image files.
- **Cinder:** Cinder's backup service can use Swift as a backup target (`cinder_backup_driver: swift`). Volume backups are stored as segmented objects in Swift containers.
- **TempURL:** Provides time-limited unauthenticated access to objects. Useful for sharing files with external users or applications that cannot perform Keystone authentication. Requires the `tempurl` middleware in the proxy pipeline.

## NASA SE Cross-References

| SE Phase | Swift Activity | Reference |
|----------|---------------|-----------|
| Phase B (Preliminary Design) | Design object storage architecture: ring parameters (partition power, replicas), disk allocation, storage policies. Plan S3 API requirements. Assess capacity needs. | SP-6105 SS 4.3-4.4 |
| Phase C (Final Design & Build) | Configure Swift storage devices and labels. Build rings. Configure proxy pipeline with s3api, tempurl, and ACL middleware. Set storage policies. | SP-6105 SS 5.1 |
| Phase D (Integration & Test) | Verify object upload/download via native and S3 APIs. Test ACLs and tempURL. Verify large object support. Test Cinder backup to Swift integration. Verify Glance image store to Swift. | SP-6105 SS 5.2-5.3 |
| Phase E (Operations) | Day-2 storage management: container/object CRUD, ACL management, storage usage monitoring, ring rebalancing for capacity changes, object expiry policies, S3 credential management. | SP-6105 SS 5.4-5.5 |
