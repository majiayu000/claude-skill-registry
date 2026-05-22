---
name: openstack-kolla-ansible
description: "Kolla-Ansible deployment engine skill for containerized OpenStack lifecycle management. Use when bootstrapping, deploying, reconfiguring, or upgrading OpenStack environments. Covers globals.yml configuration, inventory management, container operations, rolling upgrades, password management, and troubleshooting deployment failures across all service containers. This is the meta-skill that manages the deployment lifecycle for all OpenStack services."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-23"
      triggers:
        intents:
          - "kolla-ansible"
          - "kolla"
          - "deploy openstack"
          - "bootstrap"
          - "reconfigure"
          - "upgrade openstack"
          - "globals.yml"
          - "inventory"
          - "container"
          - "docker"
        contexts:
          - "deploying openstack"
          - "upgrading openstack"
          - "reconfiguring services"
          - "managing openstack containers"
          - "bootstrap environment"
---

# OpenStack Kolla-Ansible -- Deployment Engine

## Introduction

Kolla-Ansible is the production-grade deployment engine for containerized OpenStack. It uses Ansible playbooks to deploy, configure, and manage Docker containers for each OpenStack service. Every core service -- Keystone, Nova, Neutron, Cinder, Glance, Swift, Heat, Horizon -- plus supporting infrastructure (MariaDB, RabbitMQ, Memcached, HAProxy) runs in its own Docker container, managed through a single unified tool.

The Kolla project has two components: **Kolla** builds the Docker images for each OpenStack service. **Kolla-Ansible** deploys those images to target hosts using Ansible. In practice, most operators use pre-built images from the Kolla registry and only interact with Kolla-Ansible for deployment and lifecycle management.

Kolla-Ansible supports CentOS Stream 9, Rocky Linux 9, and Ubuntu 22.04 as host operating systems. Container images are available in two variants: `source` (built from OpenStack source code) and `binary` (built from distribution packages). For production stability, `binary` images pinned to a specific OpenStack release are recommended.

The deployment lifecycle follows four primary operations: **bootstrap** (prepare the host environment), **deploy** (install and start all services), **reconfigure** (change configuration on a running deployment), and **upgrade** (move to a new OpenStack release). Each operation is idempotent -- running it again produces the same result.

## Bootstrap

Bootstrap prepares the host environment for OpenStack deployment. This is a one-time operation per host.

### Prerequisites

```bash
# System requirements
# - CentOS Stream 9 (recommended), Rocky Linux 9, or Ubuntu 22.04
# - Minimum 16 GB RAM, 100 GB disk, 2 network interfaces
# - Python 3.9+
# - Docker CE or Podman (Kolla-Ansible installs Docker if missing)

# Verify Python version
python3 --version

# Verify network interfaces
ip link show
# You need at least 2 interfaces: one for management (API traffic)
# and one for Neutron external (tenant/provider network traffic)
```

### Install Kolla-Ansible

```bash
# Create a Python virtual environment (recommended)
python3 -m venv /opt/kolla-venv
source /opt/kolla-venv/bin/activate

# Install kolla-ansible (pin to a specific OpenStack release)
pip install 'kolla-ansible==17.0.*'    # For 2024.1 (Caracal)
# Or for the latest stable:
pip install kolla-ansible

# Install Ansible dependencies
kolla-ansible install-deps
```

### Generate Configuration

```bash
# Copy default configuration files
cp -r /opt/kolla-venv/share/kolla-ansible/etc_examples/kolla/* /etc/kolla/

# This creates:
# /etc/kolla/globals.yml    - Main configuration file
# /etc/kolla/passwords.yml  - Service passwords (empty, needs generation)

# Generate random passwords for all services
kolla-genpwd

# IMPORTANT: Back up passwords.yml immediately after generation
cp /etc/kolla/passwords.yml /etc/kolla/passwords.yml.backup
```

### Configure globals.yml

This is the central configuration file. Every deployment decision is encoded here:

```yaml
# /etc/kolla/globals.yml

# Base configuration
kolla_base_distro: "centos"
kolla_install_type: "binary"
openstack_release: "2024.1"

# Networking
kolla_internal_vip_address: "10.0.0.100"    # VIP for internal API traffic
network_interface: "eth0"                     # Management network interface
neutron_external_interface: "eth1"            # Neutron external bridge interface

# Optional: External VIP for public API access
# kolla_external_vip_address: "192.168.1.100"
# kolla_enable_tls_external: "yes"

# Docker configuration
# docker_registry: "quay.io"                 # Custom registry if needed
# docker_namespace: "openstack.kolla"

# Service enablement (enable what you need)
enable_keystone: "yes"      # Identity (always required)
enable_nova: "yes"          # Compute
enable_neutron: "yes"       # Networking
enable_cinder: "yes"        # Block storage
enable_glance: "yes"        # Image service
enable_horizon: "yes"       # Web dashboard
enable_heat: "yes"          # Orchestration
enable_swift: "yes"         # Object storage

# Optional services
# enable_ceilometer: "yes"  # Telemetry
# enable_aodh: "yes"        # Alarming
# enable_magnum: "yes"      # Container orchestration

# Storage backend
# cinder_backend_lvm: "yes"                  # LVM for Cinder (default)
# cinder_volume_group: "cinder-volumes"

# Neutron networking
neutron_plugin_agent: "openvswitch"           # OVS or OVN
# neutron_plugin_agent: "ovn"                 # For OVN backend
```

### Configure Inventory

```bash
# For single-node (all-in-one) deployment
cp /opt/kolla-venv/share/kolla-ansible/ansible/inventory/all-in-one /etc/kolla/

# For multi-node deployment
cp /opt/kolla-venv/share/kolla-ansible/ansible/inventory/multinode /etc/kolla/
# Then edit /etc/kolla/multinode to assign hosts to groups:
# [control], [network], [compute], [storage], [monitoring]
```

### Bootstrap Servers

```bash
# Bootstrap the host(s) - installs Docker, configures system
kolla-ansible -i /etc/kolla/all-in-one bootstrap-servers

# This performs:
# - Installs Docker CE and configures the Docker daemon
# - Configures kernel modules (br_netfilter, overlay)
# - Sets sysctl parameters (net.bridge.bridge-nf-call-iptables)
# - Creates kolla user and directory structure
# - Pulls base container images
```

### Pre-Deployment Checks

```bash
# Run pre-deployment validation
kolla-ansible -i /etc/kolla/all-in-one prechecks

# Prechecks verify:
# - Network interfaces exist and are configured
# - Required ports are not in use (5000, 8774, 9696, etc.)
# - Docker is running and functional
# - Required packages are installed
# - Disk space is sufficient
# - Firewall rules allow required traffic
```

If prechecks fail, address each reported issue before proceeding to deploy. Common fixes are documented in the Troubleshoot section.

## Deploy

Deploy installs and starts all enabled OpenStack services.

### Execute Deployment

```bash
# Deploy all enabled services
kolla-ansible -i /etc/kolla/all-in-one deploy

# Deployment proceeds in phases:
# 1. Infrastructure (MariaDB, RabbitMQ, Memcached, HAProxy)
# 2. Identity (Keystone)
# 3. Image (Glance)
# 4. Compute (Nova)
# 5. Network (Neutron)
# 6. Block Storage (Cinder)
# 7. Object Storage (Swift)
# 8. Orchestration (Heat)
# 9. Dashboard (Horizon)
# 10. Monitoring/Telemetry (if enabled)

# Duration: 15-45 minutes depending on hardware and number of services
```

### Post-Deploy

```bash
# Generate admin credentials and register endpoints
kolla-ansible -i /etc/kolla/all-in-one post-deploy

# This creates:
# /etc/kolla/admin-openrc.sh  - Admin credentials for CLI
```

### Verify Deployment

```bash
# Source admin credentials
source /etc/kolla/admin-openrc.sh

# Verify all services are registered
openstack service list

# Verify each service endpoint
openstack endpoint list

# Verify compute is available
openstack hypervisor list

# Verify networking
openstack network agent list

# Verify images service
openstack image list

# Verify block storage
openstack volume service list

# Verify orchestration
openstack orchestration service list

# Quick health check -- all services should respond
openstack token issue         # Keystone
openstack flavor list         # Nova
openstack network list        # Neutron
openstack volume type list    # Cinder
openstack image list          # Glance
openstack stack list          # Heat
```

### Initialize Demo Resources

```bash
# Run the init-runonce script to create demo networks, images, and flavors
# This script ships with Kolla-Ansible
/opt/kolla-venv/share/kolla-ansible/init-runonce

# It creates:
# - External network (public) and internal network (demo-net)
# - A router connecting internal to external
# - Cirros test image
# - Basic flavors (m1.tiny through m1.xlarge)
# - Security group rules for SSH and ICMP

# Test with an instance launch
openstack server create --image cirros --flavor m1.tiny \
  --network demo-net test-instance
openstack server list
```

## Reconfigure

Reconfigure changes the configuration of a running deployment without full redeployment.

### When to Reconfigure vs Redeploy

| Change Type | Use |
|------------|-----|
| Modify service settings (timeouts, logging, tuning) | `reconfigure` |
| Change globals.yml settings (VIP, interfaces) | `reconfigure` |
| Enable a new service | `deploy` (with the new service enabled) |
| Disable an existing service | Manual removal + `deploy` |
| Change passwords | `reconfigure` |
| Update TLS certificates | `reconfigure` |

### Config Override Directory

Kolla-Ansible applies service-specific configuration overrides from `/etc/kolla/config/`:

```
/etc/kolla/config/
  nova/
    nova.conf            # Overrides merged into nova.conf inside container
  neutron/
    neutron.conf         # Overrides merged into neutron.conf
    ml2_conf.ini         # ML2 plugin configuration overrides
  keystone/
    keystone.conf        # Keystone configuration overrides
  horizon/
    custom_local_settings  # Horizon Django settings overrides
  cinder/
    cinder.conf          # Cinder configuration overrides
  glance/
    glance-api.conf      # Glance API configuration overrides
```

Override files are INI-format (for most services) and are merged with the default configuration. Only include the sections and keys you want to change:

```ini
# /etc/kolla/config/nova/nova.conf
[DEFAULT]
cpu_allocation_ratio = 16.0
ram_allocation_ratio = 1.5

[libvirt]
virt_type = kvm
```

### Execute Reconfigure

```bash
# Reconfigure all services
kolla-ansible -i /etc/kolla/all-in-one reconfigure

# Reconfigure only specific services (faster)
kolla-ansible -i /etc/kolla/all-in-one reconfigure --tags nova
kolla-ansible -i /etc/kolla/all-in-one reconfigure --tags neutron
kolla-ansible -i /etc/kolla/all-in-one reconfigure --tags horizon
```

### Verify Changes

After reconfiguration, verify the changes took effect:

```bash
# Check a specific config value inside a container
docker exec nova_compute grep cpu_allocation_ratio \
  /etc/nova/nova.conf

# Verify service is running with new config
docker inspect --format '{{.State.StartedAt}}' nova_compute
# StartedAt should be recent (container was restarted during reconfigure)
```

## Upgrade

Upgrade moves the OpenStack deployment to a new release version. This is the most complex lifecycle operation.

### Pre-Upgrade Preparation

```bash
# 1. Document current state
openstack service list > /backup/pre-upgrade-services.txt
openstack hypervisor list > /backup/pre-upgrade-hypervisors.txt
openstack network agent list > /backup/pre-upgrade-agents.txt

# 2. Back up critical data
# Database backup (MariaDB)
docker exec mariadb mysqldump --all-databases --single-transaction \
  > /backup/pre-upgrade-all-databases.sql

# Back up configuration
cp -r /etc/kolla/ /backup/pre-upgrade-kolla-config/

# Back up passwords
cp /etc/kolla/passwords.yml /backup/pre-upgrade-passwords.yml

# 3. Snapshot running instances (if applicable)
for server in $(openstack server list -f value -c ID); do
  openstack server image create --name "pre-upgrade-$server" "$server"
done
```

### Update Kolla-Ansible

```bash
# Upgrade kolla-ansible to the new release version
source /opt/kolla-venv/bin/activate
pip install --upgrade 'kolla-ansible==18.0.*'    # New release version

# Update globals.yml with new release
# Edit /etc/kolla/globals.yml:
# openstack_release: "2024.2"

# Regenerate any new passwords added in the new release
# IMPORTANT: Use --include-unset to only generate missing passwords
# Do NOT run plain kolla-genpwd -- it would overwrite existing passwords!
kolla-genpwd --include-unset
```

### Pull New Images

```bash
# Pull container images for the new release
kolla-ansible -i /etc/kolla/all-in-one pull

# This downloads all container images for enabled services
# Duration depends on network speed and number of services
```

### Execute Upgrade

```bash
# Run the upgrade
kolla-ansible -i /etc/kolla/all-in-one upgrade

# The upgrade process:
# 1. Stops each service container
# 2. Runs database migrations
# 3. Starts containers with new images
# 4. Verifies each service is healthy
# Services are upgraded in dependency order (infrastructure first, then services)
```

### Post-Upgrade Verification

```bash
# Source updated credentials
source /etc/kolla/admin-openrc.sh

# Verify all services are running
openstack service list
openstack endpoint list
openstack hypervisor list
openstack network agent list

# Verify API versions match expected release
openstack versions show

# Compare with pre-upgrade state
diff /backup/pre-upgrade-services.txt <(openstack service list)
diff /backup/pre-upgrade-hypervisors.txt <(openstack hypervisor list)

# Test basic operations
openstack token issue
openstack server list
openstack network list
```

### Rollback Procedure

If the upgrade fails and services are not recoverable:

```bash
# 1. Stop all Kolla containers
docker stop $(docker ps -q --filter label=kolla_role)

# 2. Restore database from backup
docker start mariadb
docker exec -i mariadb mysql < /backup/pre-upgrade-all-databases.sql

# 3. Restore configuration
cp -r /backup/pre-upgrade-kolla-config/* /etc/kolla/

# 4. Downgrade kolla-ansible
pip install 'kolla-ansible==17.0.*'

# 5. Redeploy with previous version
kolla-ansible -i /etc/kolla/all-in-one deploy

# 6. Verify rollback
source /etc/kolla/admin-openrc.sh
openstack service list
```

## Troubleshoot

### Bootstrap Fails

**Python dependency conflicts:**
Kolla-Ansible requires specific Ansible and Python library versions. If the system Python has conflicting packages, bootstrap fails. Fix: always install Kolla-Ansible in a virtual environment (`python3 -m venv`) to isolate dependencies.

**Docker not installed or not running:**
Bootstrap-servers installs Docker, but if the installation fails (repository unreachable, package conflicts), subsequent steps fail. Check: `systemctl status docker`. Manual fix: install Docker CE following the official Docker documentation for your distribution, then re-run bootstrap-servers.

**Network interface not found:**
If the `network_interface` or `neutron_external_interface` specified in globals.yml does not exist on the host, bootstrap fails. Verify: `ip link show`. The interface names must match exactly (e.g., `ens192` not `eth0` on systems using predictable network interface naming).

### Prechecks Fail

**Port conflicts:**
Another service is listening on a port that OpenStack needs (5000 for Keystone, 8774 for Nova, 9696 for Neutron, etc.). Check: `ss -tlnp | grep <port>`. Fix: stop the conflicting service or change the OpenStack service port in globals.yml.

**Missing packages:**
Required system packages are not installed. Kolla-Ansible reports which packages are missing. Install them: `dnf install <package>` (CentOS/Rocky) or `apt install <package>` (Ubuntu).

**Firewall rules blocking:**
The host firewall blocks required ports. For testing: `systemctl stop firewalld` or `ufw disable`. For production: add rules for each required port. Kolla-Ansible expects unrestricted communication between all nodes in a multi-node deployment.

**SELinux issues:**
On CentOS/Rocky, SELinux may block container operations. Check: `getenforce`. For testing: `setenforce 0`. For production: configure SELinux policies for Docker containers rather than disabling entirely.

### Deploy Fails

**Image pull failure:**
Docker cannot pull container images. Check: Docker registry connectivity (`docker pull quay.io/openstack.kolla/keystone:2024.1`), DNS resolution, and proxy settings. If behind a corporate proxy, configure Docker's proxy settings in `/etc/systemd/system/docker.service.d/http-proxy.conf`.

**Container start failure:**
A container starts but immediately exits. Check: `docker logs <container_name>`. Common causes: configuration file syntax errors (YAML/INI parsing failure), missing required configuration values, database connection refused (MariaDB not ready yet).

**Service dependency timeout:**
A service waits for a dependency (e.g., Nova waits for Keystone) that has not started. Kolla-Ansible handles dependency ordering, but if a dependency service fails, downstream services timeout. Fix the root cause (usually the first service that failed), then re-run deploy.

### Reconfigure Fails

**Invalid config override:**
A file in `/etc/kolla/config/<service>/` has a syntax error. Kolla-Ansible copies the override into the container but the service cannot parse it. Check: validate the override file's INI/YAML syntax before reconfiguring. For INI files: ensure sections are properly bracketed and key-value pairs use `=`.

**YAML syntax error in globals.yml:**
An edit to globals.yml introduced a YAML parsing error. Validate: `python3 -c "import yaml; yaml.safe_load(open('/etc/kolla/globals.yml'))"`. Common issues: missing quotes around values with special characters, incorrect indentation, tabs instead of spaces.

**Service won't restart after reconfigure:**
The new configuration is invalid for the service. Check the container logs: `docker logs <service_name>`. Revert the config override and reconfigure again to restore the working state.

### Upgrade Fails

**Database migration error:**
A schema migration fails during upgrade. Check: `docker logs <service>_api` or the specific migration container logs. Database migrations are the most fragile part of the upgrade. If a migration fails: restore the database from backup and retry, or if the migration is known-broken, check the OpenStack release notes for workarounds.

**Incompatible configuration:**
A configuration option was deprecated or removed in the new release. Check the OpenStack release notes for the target version. Remove or rename deprecated options in `/etc/kolla/config/` before upgrading.

**Container image version mismatch:**
The pulled images do not match the expected version. Verify: `docker images | grep kolla`. Ensure `openstack_release` in globals.yml matches the kolla-ansible version and the pulled images. If mismatched: `kolla-ansible pull` to re-pull correct images.

### Container Keeps Restarting

Check the container logs for the specific error:

```bash
# View container logs
docker logs <container_name>
docker logs <container_name> --tail 50

# Check container restart count and state
docker inspect <container_name> --format '{{.RestartCount}} {{.State.Error}}'
```

Common causes: configuration error (service fails to parse config on startup), dependency service not ready (connection refused to MariaDB/RabbitMQ), permission error (file ownership inside container), out-of-memory (container exceeds memory limit).

### Password and Credential Issues

**passwords.yml mismatch:**
If passwords.yml is regenerated after deployment (`kolla-genpwd` without `--include-unset`), the new passwords do not match what is stored in the running databases and services. Fix: restore the original passwords.yml from backup. Prevention: always back up passwords.yml before running kolla-genpwd, and always use `--include-unset` for partial regeneration.

**Admin credentials not working:**
After post-deploy, the admin-openrc.sh file contains the correct credentials. If authentication fails: verify the `keystone_admin_password` in passwords.yml matches what is in admin-openrc.sh. If they diverge: regenerate admin-openrc.sh via `kolla-ansible post-deploy`.

## Container Management

Kolla containers follow a consistent naming convention and management pattern.

### Container Operations

```bash
# List all Kolla containers
docker ps --filter label=kolla_role

# List containers for a specific service
docker ps --filter name=nova
docker ps --filter name=neutron
docker ps --filter name=keystone

# View container logs
docker logs keystone
docker logs nova_compute --tail 100
docker logs neutron_server --follow

# Execute commands inside a container
docker exec -it nova_compute bash
docker exec keystone cat /etc/keystone/keystone.conf
docker exec neutron_server neutron-status upgrade check

# Inspect container configuration
docker inspect keystone --format '{{json .Config.Env}}' | python3 -m json.tool
docker inspect nova_compute --format '{{.HostConfig.Binds}}'
```

### Service-Specific Containers

| Service | Container Names |
|---------|----------------|
| Keystone | keystone, keystone_fernet, keystone_ssh |
| Nova | nova_api, nova_conductor, nova_scheduler, nova_compute, nova_novncproxy |
| Neutron | neutron_server, neutron_dhcp_agent, neutron_l3_agent, neutron_metadata_agent, neutron_openvswitch_agent |
| Cinder | cinder_api, cinder_scheduler, cinder_volume, cinder_backup |
| Glance | glance_api |
| Horizon | horizon |
| Heat | heat_api, heat_engine, heat_api_cfn |
| Swift | swift_proxy_server, swift_account_*, swift_container_*, swift_object_* |
| Infrastructure | mariadb, rabbitmq, memcached, haproxy, keepalived |

### Restarting Individual Services

```bash
# Restart a single container
docker restart nova_compute

# Restart all containers for a service
docker restart $(docker ps -q --filter name=nova)

# Full service restart via Kolla-Ansible (preferred -- handles dependencies)
kolla-ansible -i /etc/kolla/all-in-one reconfigure --tags nova
```

### Log Locations

```bash
# Container logs (stdout/stderr)
docker logs <container_name>

# Persistent log files (mounted from host)
ls /var/log/kolla/
# /var/log/kolla/keystone/     - Keystone logs
# /var/log/kolla/nova/         - Nova logs
# /var/log/kolla/neutron/      - Neutron logs
# /var/log/kolla/cinder/       - Cinder logs
# /var/log/kolla/glance/       - Glance logs
# /var/log/kolla/horizon/      - Horizon logs
# /var/log/kolla/heat/         - Heat logs
# /var/log/kolla/mariadb/      - MariaDB logs
# /var/log/kolla/rabbitmq/     - RabbitMQ logs

# Common log analysis patterns
grep ERROR /var/log/kolla/nova/nova-compute.log | tail -20
grep "WARN\|ERROR" /var/log/kolla/neutron/neutron-server.log | tail -20
```

### Container Health

```bash
# Check health status of all Kolla containers
docker ps --filter label=kolla_role --format "table {{.Names}}\t{{.Status}}"

# Check specific container health
docker inspect --format '{{.State.Health.Status}}' keystone

# Quick health check script
for c in $(docker ps --filter label=kolla_role --format '{{.Names}}'); do
  status=$(docker inspect --format '{{.State.Status}}' "$c")
  health=$(docker inspect --format '{{.State.Health.Status}}' "$c" 2>/dev/null || echo "no-healthcheck")
  echo "$c: $status ($health)"
done
```

### Configuration Inside Containers

```bash
# Service configs are mounted into containers from /etc/kolla/<service>/
# The config merge order is:
# 1. Default config (built into container image)
# 2. Kolla-Ansible generated config (/etc/kolla/<service>/<config>.conf)
# 3. User overrides (/etc/kolla/config/<service>/<config>.conf)

# View the final merged config inside a container
docker exec nova_compute cat /etc/nova/nova.conf
docker exec keystone cat /etc/keystone/keystone.conf
docker exec neutron_server cat /etc/neutron/neutron.conf
```

## NASA SE Cross-References

- **Phase C (Final Design and Fabrication):** Bootstrap and deployment configuration map to the "fabrication" phase of the SE lifecycle (SP-6105 SS 5.1). The globals.yml file is the design-to specification -- it encodes every architectural decision into a machine-readable configuration. The inventory file defines the deployment topology. Together they represent the "build instructions" that transform design into operational infrastructure. Configuration management (SS 6.5) requires that all configs are version-controlled with decision-documenting commit messages.

- **Phase D (Integration and Test):** Prechecks and post-deploy verification map to "integration and test" (SP-6105 SS 5.2-5.3). The prechecks playbook performs pre-integration inspection -- verifying that the deployment environment meets all prerequisites before committing to installation. Post-deploy verification (`openstack service list`, endpoint checks, health checks) constitutes the system integration test -- proving that all services are deployed, registered, interconnected, and functioning as a coherent system. The init-runonce script performs a basic operational demonstration (TAID-D) -- creating networks, images, and launching an instance to prove end-to-end functionality.

- **Phase E (Operations and Sustainment):** Reconfigure and upgrade operations map to "operations and sustainment" (SP-6105 SS 5.4-5.5). Reconfigure is the controlled configuration change process -- modifying operational parameters while maintaining service continuity. Upgrade is the major revision process -- moving the entire platform to a new release with database migrations, image updates, and service restarts. Both operations require pre-action backups, post-action verification, and documented rollback procedures, following the same change control rigor NASA applies to operational system modifications. Container management provides the day-2 operations toolkit for monitoring, troubleshooting, and maintaining the deployed infrastructure.
