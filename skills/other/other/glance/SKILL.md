---
name: openstack-glance
description: "OpenStack Glance image service skill for deploying, configuring, operating, and troubleshooting the VM image registry. Covers image upload/download, format management (qcow2, raw, vmdk, vhd, iso), backend storage selection (file, swift, ceph), image import methods (web-download, glance-direct, copy-image), metadata management, property protections, image sharing between projects, snapshot lifecycle, image caching, and storage usage monitoring. Use when deploying Glance via Kolla-Ansible, managing VM images, converting image formats, or troubleshooting image upload failures."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-22"
      triggers:
        intents:
          - "glance"
          - "image"
          - "snapshot"
          - "image format"
          - "qcow2"
          - "raw"
          - "image import"
          - "image registry"
        contexts:
          - "deploying openstack images"
          - "managing vm images"
          - "troubleshooting image service"
          - "converting image formats"
---

# OpenStack Glance Image Service

Glance is the image catalog and delivery service for OpenStack. It stores, discovers, and serves virtual machine images that Nova uses to boot instances. Glance handles image metadata, format validation, access control, and backend storage abstraction -- it does not care where images are physically stored, only that they are retrievable.

Supported image formats: **qcow2** (default, copy-on-write, thin provisioning), **raw** (direct disk image, fastest I/O), **vmdk** (VMware), **vhd/vhdx** (Hyper-V), **iso** (CD/DVD). Backend storage options: **file** (local filesystem, simplest), **swift** (OpenStack object storage), **ceph** (distributed storage via RBD), **cinder** (block storage as image backend).

## Deploy

### Kolla-Ansible Configuration

**globals.yml settings:**

```yaml
# Backend storage (choose one)
glance_backend_file: "yes"              # Local filesystem (single-node, simplest)
# glance_backend_ceph: "yes"           # Ceph RBD (multi-node, production)
# glance_backend_swift: "yes"          # Swift object storage

# File backend data directory
# glance_file_datadir: "/var/lib/glance/images"  # Default location

# Database and auth
glance_database_password: "{{ vault_glance_database_password }}"
glance_keystone_password: "{{ vault_glance_keystone_password }}"

# Image size limit (bytes, 0 = unlimited)
# glance_image_size_cap: 0

# Enable image import (web-download, glance-direct)
# enable_glance_image_import: "yes"
```

**Deployment:**

```bash
# Deploy Glance
kolla-ansible -i inventory deploy --tags glance

# Verify containers
docker ps --filter "name=glance" --format "table {{.Names}}\t{{.Status}}"
# Expected: glance_api (Up)
```

**Post-deploy verification:**

```bash
source /etc/kolla/admin-openrc.sh

# Verify Glance service in catalog
openstack service list | grep image
openstack endpoint list --service glance

# Test image upload with CirrOS (minimal test image)
wget http://download.cirros-cloud.net/0.6.2/cirros-0.6.2-x86_64-disk.img
openstack image create --file cirros-0.6.2-x86_64-disk.img \
  --disk-format qcow2 --container-format bare \
  --public cirros
openstack image list
openstack image show cirros
```

### Image Import Task Setup

For web-download and glance-direct import methods:

```ini
# glance-api.conf [DEFAULT]
enabled_import_methods = [glance-direct, web-download, copy-image]

# glance-api.conf [task]
task_executor = taskflow
work_dir = /var/lib/glance/tasks_work_dir
```

## Configure

### Backend Storage Selection

| Backend | Use Case | Pros | Cons |
|---------|----------|------|------|
| **file** | Single-node, lab, development | Simplest, no dependencies | No HA, limited by local disk |
| **swift** | Multi-node with Swift deployed | Native OpenStack, scalable | Requires Swift deployment |
| **ceph** | Multi-node production | High availability, consistent performance | Requires Ceph cluster |
| **cinder** | Boot-from-volume workflows | Leverages existing block storage | Higher latency for image serving |

### Image Format Policies

```ini
# glance-api.conf [image_format]
disk_formats = qcow2,raw,iso          # Restrict accepted formats
container_formats = bare,docker        # Restrict container formats
default_disk_format = qcow2
```

### Image Size Limits

```ini
# glance-api.conf [DEFAULT]
image_size_cap = 13743895347           # ~12.8 GB max image size

# Per-user quota (via Keystone project quotas)
# Managed through Oslo quotas framework
```

### Image Caching

Glance cache stores frequently requested images locally on the API node for faster serving:

```ini
# glance-api.conf [DEFAULT]
image_cache_max_size = 10737418240     # 10 GB cache
image_cache_stall_time = 86400         # Stale after 24h
image_cache_dir = /var/lib/glance/image-cache

# Cache management
# glance-cache-manage list-cached
# glance-cache-manage list-queued
# glance-cache-manage delete-all-cached-images
```

### Metadata Definitions

Glance supports structured metadata namespaces for organizing image properties:

```bash
# List metadata namespaces
openstack image metadata namespace list

# Create custom metadata
openstack image set --property os_type=linux \
  --property os_distro=ubuntu \
  --property os_version=22.04 \
  my-image
```

### Property Protections

Control which users can read/write specific image properties:

```ini
# property-protections.conf
[x_billing_code]
create = role:admin
read = role:admin,role:member
update = role:admin
delete = role:admin
```

### Image Import Methods

```bash
# Web-download: import from URL (Glance downloads it)
glance image-create-via-import --name web-image \
  --disk-format qcow2 --container-format bare \
  --import-method web-download \
  --uri http://example.com/image.qcow2

# Glance-direct: stage then import (client uploads data)
glance image-create-via-import --name direct-image \
  --disk-format qcow2 --container-format bare \
  --import-method glance-direct \
  --file local-image.qcow2

# Copy-image: copy between stores (multi-store only)
glance image-import --import-method copy-image --stores fast-store <image-id>
```

## Operate

### Image Upload and Download

```bash
# Upload image from file
openstack image create --file ubuntu-22.04.qcow2 \
  --disk-format qcow2 --container-format bare \
  --min-disk 10 --min-ram 1024 \
  --public ubuntu-22.04

# Download image to file
openstack image save --file downloaded.qcow2 <image-id>

# Upload raw image (for performance-critical workloads)
qemu-img convert -f qcow2 -O raw ubuntu-22.04.qcow2 ubuntu-22.04.raw
openstack image create --file ubuntu-22.04.raw \
  --disk-format raw --container-format bare ubuntu-22.04-raw
```

### Format Conversion

```bash
# Convert qcow2 to raw (better I/O performance)
qemu-img convert -f qcow2 -O raw input.qcow2 output.raw

# Convert vmdk to qcow2 (import from VMware)
qemu-img convert -f vmdk -O qcow2 input.vmdk output.qcow2

# Check image info
qemu-img info image.qcow2
# Shows: format, virtual size, disk size, backing file
```

### Image Sharing Between Projects

```bash
# Share image with another project (as image owner)
openstack image add project <image-id> <target-project-id>

# Accept shared image (as target project member)
openstack image set --accept <image-id>

# List shared images
openstack image list --shared

# Remove sharing
openstack image remove project <image-id> <target-project-id>
```

### Snapshot Management

```bash
# Create instance snapshot (creates a Glance image)
openstack server image create --name my-snapshot my-instance

# List snapshots
openstack image list --property image_type=snapshot

# Monitor snapshot progress
openstack image show my-snapshot -c status
# States: queued -> saving -> active
```

### Storage Usage Monitoring

```bash
# Check total image storage usage
openstack image list --long -f json | python3 -c "
import json, sys
images = json.load(sys.stdin)
total = sum(i.get('Size', 0) or 0 for i in images)
print(f'Total: {total / (1024**3):.2f} GB across {len(images)} images')
"

# Check backend storage directly (file backend)
du -sh /var/lib/docker/volumes/glance/_data/images/

# Cleanup soft-deleted images
glance-manage db purge --age_in_days 30 --max_rows 100
```

### Image Metadata Management

```bash
# Set multiple properties
openstack image set \
  --property hw_disk_bus=scsi \
  --property hw_scsi_model=virtio-scsi \
  --property hw_vif_model=virtio \
  --property os_type=linux \
  <image-id>

# Remove a property
openstack image unset --property hw_disk_bus <image-id>

# Set hardware requirements
openstack image set --min-disk 20 --min-ram 2048 <image-id>
```

## Troubleshoot

### 1. Image Upload Failures

**Symptoms:** `openstack image create` hangs or returns error. Image stuck in "queued" state.

**Diagnosis:**

```bash
docker logs glance_api 2>&1 | tail -50
# Check for: disk space errors, permission denied, size limit exceeded
```

**Common causes:**

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Storage full | `df -h /var/lib/docker/volumes/glance/` | Free space or expand storage |
| Permission denied | Glance logs: "Permission denied" on data dir | Fix ownership: `chown -R 42415:42415 /var/lib/docker/volumes/glance/` |
| Size limit exceeded | Glance logs: "image_size_cap" | Increase `image_size_cap` in glance-api.conf or reduce image |
| Database connection | Glance logs: "OperationalError" | Check MariaDB connectivity |

### 2. Image Download Slow or Fails

**Symptoms:** Nova instance boot takes very long. Image download timeout.

**Diagnosis:**

```bash
# Check image size
openstack image show <image-id> -c size

# Check backend connectivity
docker exec glance_api ls -la /var/lib/glance/images/<image-id>

# Check network between glance and compute
docker logs nova_compute 2>&1 | grep -i "glance\|image\|download"
```

**Fix:**
- Enable image caching on compute nodes (nova.conf `[image_cache]`)
- Convert large qcow2 to raw for faster I/O
- Check network bandwidth between API and compute nodes
- Pre-cache images: `openstack image set --property os_glance_caching=true <id>`

### 3. Format Conversion Errors

**Symptoms:** `qemu-img convert` fails. Image creates but won't boot.

**Diagnosis:**

```bash
# Verify source image integrity
qemu-img check input.qcow2
# Should report: "No errors were found"

# Check format detection
qemu-img info input.qcow2
```

**Fix:**
- Corrupted source: re-download original image
- Unsupported format: convert through an intermediate format (vmdk -> qcow2 -> raw)
- Wrong format specified: verify actual format with `qemu-img info` before uploading

### 4. Image Stuck in "saving" State

**Symptoms:** Image shows status "saving" indefinitely.

**Diagnosis:**

```bash
# Check Glance API logs for write errors
docker logs glance_api 2>&1 | grep <image-id>

# Check if backend write is still in progress
ls -la /var/lib/docker/volumes/glance/_data/images/<image-id>
# File should be growing if transfer is ongoing
```

**Fix:**
- Backend write timeout: increase `[DEFAULT] image_size_cap` and retry
- Storage I/O error: check disk health with `smartctl` and `dmesg`
- Reset stuck image: `openstack image set --status error <image-id>` then delete and re-upload

### 5. Metadata Service Issues

**Symptoms:** Image property updates rejected. "403 Forbidden" when setting properties.

**Diagnosis:**

```bash
# Check property protections
docker exec glance_api cat /etc/glance/property-protections.conf

# Check RBAC policy
docker exec glance_api cat /etc/glance/policy.yaml
```

**Fix:**
- Property protection blocking: update `property-protections.conf` to allow the role
- RBAC denial: check `policy.yaml` for image modification rules
- Reserved property namespace: properties starting with `os_` may require admin role

## Integration Points

| Service | Integration | Mechanism |
|---------|-------------|-----------|
| **Keystone** | Authentication for all API calls; service user for internal operations | keystonemiddleware in glance-api |
| **Nova** | Image retrieval for instance boot; snapshot upload after `server image create` | Nova calls Glance REST API to download images to compute cache |
| **Cinder** | Volume-from-image: create bootable volume from Glance image | Cinder calls Glance API, copies image data into volume |
| **Swift** | Backend storage option: images stored as Swift objects | glance-api uses swift client to store/retrieve image data |

## NASA SE Cross-References

| SE Phase | Glance Activity | Reference |
|----------|-----------------|-----------|
| Phase B (Preliminary Design) | Select image backend (file vs swift vs ceph), define supported formats, plan storage capacity | SP-6105 SS 4.3-4.4 |
| Phase C (Final Design) | Configure Glance in globals.yml: backend, data directory, size limits, import methods | SP-6105 SS 5.1 |
| Phase D (Integration & Test) | Verify: image upload, image download, instance boot from image, snapshot create/restore | SP-6105 SS 5.2-5.3 |
| Phase E (Operations) | Image lifecycle management, format conversion, storage monitoring, cache maintenance, soft-delete cleanup | SP-6105 SS 5.4-5.5, NPR 7123.1 SS 5.4 |
