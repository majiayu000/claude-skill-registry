---
name: openstack-kolla-ansible-ops
description: "Kolla-Ansible day-2 operations skill for post-deployment infrastructure lifecycle management. Covers service reconfiguration (globals.yml changes, config overrides, prechecks, targeted reconfigure with --tags), minor and major OpenStack upgrades (image pull, upgrade procedure, rollback), container management (restart, logs, health inspection), maintenance mode (compute disable, instance drain, host maintenance), password rotation, certificate renewal, and rolling updates. This skill is for operations after initial deployment -- the kolla-ansible deployment skill covers initial bootstrap and deploy."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-23"
      triggers:
        intents:
          - "kolla upgrade"
          - "kolla reconfigure"
          - "container restart"
          - "rolling update"
          - "service maintenance"
          - "kolla-ansible ops"
          - "config change"
          - "container management"
        contexts:
          - "upgrading openstack"
          - "reconfiguring services"
          - "managing kolla containers"
          - "performing maintenance"
---

# Kolla-Ansible Day-2 Operations -- Infrastructure Lifecycle Management

Kolla-Ansible is not just a deployment tool -- it is the infrastructure lifecycle manager. The initial `kolla-ansible deploy` is a one-time event. Everything after that -- reconfiguration, upgrades, container management, maintenance -- is what this skill covers. Operators will use these procedures repeatedly throughout the cloud's operational life.

**The operational command set:**

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `kolla-ansible reconfigure` | Regenerate configs and restart affected services | After globals.yml or config override changes |
| `kolla-ansible upgrade` | Pull new images and upgrade services | Minor or major OpenStack release upgrades |
| `kolla-ansible prechecks` | Validate configuration before applying | Always run before reconfigure or upgrade |
| `kolla-ansible stop` | Stop all or specific service containers | Maintenance, troubleshooting |
| `kolla-ansible deploy` | Deploy services (also used for redeployment) | After stop, or for new services |
| `kolla-ansible pull` | Pull container images without deploying | Pre-stage images before upgrade window |

**Relationship to the kolla-ansible deployment skill:** The deployment skill (Phase 313) covers the initial bootstrap, deploy, and post-deploy verification that brings the cloud online for the first time. This skill picks up where deployment left off. They share the same inventory and globals.yml, but the operational context is different: deployment is about getting services running; operations is about keeping them running, changing their configuration, and upgrading them.

**Container lifecycle in Kolla:** Every OpenStack service runs in a Docker container managed by Kolla-Ansible. The container lifecycle is: image pull (from registry or local build) -> deploy (create container with config volumes) -> reconfigure (regenerate config, restart container) -> upgrade (pull new image, recreate container, run migrations). Understanding this lifecycle is essential for day-2 operations.

## Deploy

### Operational Prerequisites

**Kolla-Ansible virtual environment maintenance:**

```bash
# The Kolla-Ansible venv should be maintained separately from system Python
source /path/to/kolla-venv/bin/activate

# Verify kolla-ansible version matches deployed release
kolla-ansible --version
pip show kolla-ansible | grep Version
```

**Inventory file management:**

```bash
# Inventory defines which hosts run which services
# For single-node: all-in-one inventory
# For multi-node: multinode inventory with role assignments

# Verify inventory connectivity
ansible -i /etc/kolla/inventory all -m ping
```

**globals.yml change tracking:**

```bash
# globals.yml is the primary configuration file -- track all changes in git
cd /etc/kolla
git init  # If not already tracked
git add globals.yml
git commit -m "baseline: initial globals.yml configuration"

# Before every change, commit the current state
git add globals.yml
git commit -m "pre-change: document current state before <change-description>"
```

**Password management:**

```bash
# Initial password generation (done once during deployment)
kolla-ansible -i /etc/kolla/inventory genpasswd

# Passwords are stored in /etc/kolla/passwords.yml
# After initial generation, rotate passwords manually
# Never regenerate all passwords on a running system
```

**Image management:**

```bash
# Check current image versions
docker images | grep kolla

# Pull latest images for current release
kolla-ansible -i /etc/kolla/inventory pull

# Pull images for a specific service
kolla-ansible -i /etc/kolla/inventory pull --tags nova
```

## Configure

### Service Reconfiguration Workflow

Reconfiguration is the most common operational action. It regenerates configuration files from templates and globals.yml, then restarts affected containers.

```bash
# Step 1: Make the change in globals.yml or config overrides
vim /etc/kolla/globals.yml

# Step 2: Validate the change
kolla-ansible -i /etc/kolla/inventory prechecks

# Step 3: Apply the change
kolla-ansible -i /etc/kolla/inventory reconfigure

# Step 4: Verify service health
openstack service list
openstack endpoint list
```

### Partial Reconfiguration with --tags

Target specific services to minimize disruption:

```bash
# Reconfigure only Nova
kolla-ansible -i /etc/kolla/inventory reconfigure --tags nova

# Reconfigure only Neutron
kolla-ansible -i /etc/kolla/inventory reconfigure --tags neutron

# Reconfigure only Keystone
kolla-ansible -i /etc/kolla/inventory reconfigure --tags keystone

# Multiple services
kolla-ansible -i /etc/kolla/inventory reconfigure --tags nova,neutron
```

### Config Validation Before Apply

Always run prechecks before reconfigure or upgrade:

```bash
# Full prechecks
kolla-ansible -i /etc/kolla/inventory prechecks

# Service-specific prechecks
kolla-ansible -i /etc/kolla/inventory prechecks --tags nova

# Prechecks verify:
# - Container runtime is available
# - Required images exist
# - Configuration templates render without errors
# - Port conflicts are detected
# - Service dependencies are met
```

### Custom Config Overrides

Kolla-Ansible supports per-service configuration overrides that persist across reconfigures:

```bash
# Override directory structure
/etc/kolla/config/
  nova/
    nova.conf         # Merged into nova.conf
    nova-compute.conf # Merged into nova-compute.conf
  neutron/
    neutron.conf      # Merged into neutron.conf
    ml2_conf.ini      # Merged into ml2_conf.ini
  keystone/
    keystone.conf     # Merged into keystone.conf
```

```ini
# Example: /etc/kolla/config/nova/nova.conf
[DEFAULT]
debug = True

[scheduler]
max_attempts = 5
```

### globals.yml Change Matrix

What changes require which operational action:

| Change Category | Example | Required Action |
|----------------|---------|-----------------|
| Service enable/disable | `enable_heat: "yes"` | `deploy` (new service) or `stop` + remove |
| Backend change | `neutron_plugin_agent: "ovn"` | Full redeploy of affected services |
| Network config | `neutron_external_interface` | `reconfigure --tags neutron` |
| Logging | `enable_central_logging: "yes"` | `reconfigure` |
| TLS | `kolla_enable_tls_internal: "yes"` | `reconfigure` (generates certs, updates all services) |
| Allocation ratios | `nova_cpu_allocation_ratio` | `reconfigure --tags nova` |
| Image tag | `openstack_release` | `upgrade` (not reconfigure) |

## Operate

### Service Reconfigure

**Complete procedure for a configuration change:**

1. Document the change: `git -C /etc/kolla diff globals.yml`
2. Commit pre-change state: `git -C /etc/kolla add globals.yml && git -C /etc/kolla commit -m "pre-change: <description>"`
3. Make the change: edit globals.yml or config overrides
4. Run prechecks: `kolla-ansible -i /etc/kolla/inventory prechecks`
5. Run reconfigure: `kolla-ansible -i /etc/kolla/inventory reconfigure` (or with `--tags`)
6. Verify service health: `openstack service list && openstack endpoint list`
7. Commit post-change state: `git -C /etc/kolla add globals.yml && git -C /etc/kolla commit -m "post-change: <description>"`

### Minor Upgrade (Patch)

**Within the same major OpenStack release (e.g., 2024.1 patch):**

1. Backup databases: `kolla-ansible -i /etc/kolla/inventory mariadb_backup`
2. Pull new images: `kolla-ansible -i /etc/kolla/inventory pull`
3. Run prechecks: `kolla-ansible -i /etc/kolla/inventory prechecks`
4. Run upgrade: `kolla-ansible -i /etc/kolla/inventory upgrade`
5. Verify all services: `openstack service list` -- all services should be `enabled` and endpoints reachable
6. Run smoke test: create a test instance, verify networking, delete test instance

### Major Upgrade

**Across OpenStack releases (e.g., 2024.1 to 2024.2):**

1. **Pre-upgrade backup:**
   ```bash
   # Database backup
   kolla-ansible -i /etc/kolla/inventory mariadb_backup
   # Verify backup: ls -la /var/lib/docker/volumes/mariadb_backup/_data/

   # Configuration backup
   tar czf /root/kolla-config-backup-$(date +%Y%m%d).tar.gz /etc/kolla/
   ```

2. **Update Kolla-Ansible:**
   ```bash
   pip install --upgrade kolla-ansible==<new-version>
   ```

3. **Update globals.yml:**
   ```yaml
   openstack_release: "2024.2"
   ```

4. **Pull new images:**
   ```bash
   kolla-ansible -i /etc/kolla/inventory pull
   ```

5. **Run prechecks:**
   ```bash
   kolla-ansible -i /etc/kolla/inventory prechecks
   ```

6. **Execute upgrade:**
   ```bash
   kolla-ansible -i /etc/kolla/inventory upgrade
   ```

7. **Post-upgrade verification:**
   ```bash
   # Check all containers are running
   docker ps --format '{{.Names}} {{.Status}}' | sort

   # Check all services are healthy
   openstack service list
   openstack compute service list
   openstack network agent list
   openstack volume service list

   # Run integration test
   openstack server create --flavor m1.small --image cirros --network tenant-net upgrade-test
   openstack server delete upgrade-test
   ```

### Container Management

**Restart an individual service:**

```bash
# Restart a single container
docker restart nova_api
docker restart neutron_server

# Check container logs after restart
docker logs --tail 100 nova_api
docker logs --tail 100 --follow neutron_server

# Check container health
docker inspect --format='{{.State.Health.Status}}' keystone
docker inspect --format='{{.State.Status}}' nova_api
```

**Inspect container configuration:**

```bash
# View the running configuration
docker exec nova_api cat /etc/nova/nova.conf | grep -v "^#" | grep -v "^$"

# Check container resource usage
docker stats --no-stream nova_api neutron_server keystone
```

### Maintenance Mode

**Procedure for compute host maintenance:**

1. **Disable the compute service:**
   ```bash
   openstack compute service set --disable --disable-reason "Scheduled maintenance" <hostname> nova-compute
   ```

2. **Drain instances (live migrate to other hosts):**
   ```bash
   # List instances on the host
   openstack server list --host <hostname> --all-projects

   # Live migrate each instance (multi-node only)
   openstack server migrate --live-migration <instance-id>

   # For single-node: shut down instances instead
   openstack server stop <instance-id>
   ```

3. **Perform maintenance** (hardware, OS updates, etc.)

4. **Re-enable the compute service:**
   ```bash
   openstack compute service set --enable <hostname> nova-compute
   ```

5. **Verify:**
   ```bash
   openstack compute service list
   # Service should be enabled and up
   ```

### Password Rotation

```bash
# 1. Edit passwords.yml with new passwords for specific services
vim /etc/kolla/passwords.yml
# Change only the passwords you need to rotate

# 2. Run reconfigure to apply new passwords
kolla-ansible -i /etc/kolla/inventory reconfigure

# 3. Verify all services reconnect with new credentials
openstack service list
openstack endpoint list

# 4. Test authentication
openstack token issue
```

### Certificate Renewal

```bash
# 1. Generate or obtain new certificates
# Place them in /etc/kolla/certificates/

# 2. Update globals.yml if certificate paths changed
# kolla_external_fqdn_cert: /etc/kolla/certificates/haproxy.pem
# kolla_internal_fqdn_cert: /etc/kolla/certificates/haproxy-internal.pem

# 3. Reconfigure HAProxy and affected services
kolla-ansible -i /etc/kolla/inventory reconfigure --tags haproxy

# 4. Verify TLS connectivity
openssl s_client -connect <api-endpoint>:5000 -brief
curl -v https://<api-endpoint>:5000/v3/
```

## Troubleshoot

### Reconfigure Fails Midway

**Symptoms:** `kolla-ansible reconfigure` exits with an error partway through. Some services have new config, others have old config.

**Resolution steps:**
1. Check the Ansible output for the specific task that failed -- note the service name and error
2. Fix the underlying issue (config syntax, missing dependency, connectivity)
3. Rerun with the specific tag: `kolla-ansible -i /etc/kolla/inventory reconfigure --tags <service>`
4. If a single container is stuck, restart it manually: `docker restart <container-name>`
5. After resolution, run a full prechecks to verify consistency: `kolla-ansible -i /etc/kolla/inventory prechecks`

### Upgrade Fails on Prechecks

**Symptoms:** `kolla-ansible prechecks` reports errors before the upgrade can begin.

**Resolution steps:**
1. Read the specific precheck error message -- common causes:
   - Version incompatibility: current release cannot upgrade directly to target (skip releases not supported)
   - Unsupported configuration: a deprecated option in globals.yml
   - Missing migration: database schema migration required before the upgrade
2. Check Kolla-Ansible release notes for the target version -- look for breaking changes and required migration steps
3. Fix globals.yml: remove deprecated options, add required new options
4. Rerun prechecks: `kolla-ansible -i /etc/kolla/inventory prechecks`

### Container Won't Start After Upgrade

**Symptoms:** After `kolla-ansible upgrade`, one or more containers fail to start or crash on startup.

**Resolution steps:**
1. Check container logs: `docker logs --tail 200 <container-name>` -- look for config parse errors or missing dependencies
2. Check image version: `docker inspect <container-name> --format='{{.Config.Image}}'` -- verify the correct version was pulled
3. If image pull failed: `kolla-ansible -i /etc/kolla/inventory pull --tags <service>` then `kolla-ansible upgrade --tags <service>`
4. If config incompatibility: check `/etc/kolla/config/<service>/` for overrides that conflict with the new version
5. If database migration needed: check service logs for migration errors, run migration manually if needed

### Service Unhealthy After Reconfigure

**Symptoms:** Service containers are running but health checks fail, API returns errors, or service cannot authenticate to Keystone.

**Resolution steps:**
1. Check service logs for config errors: `docker logs --tail 100 <service>_server`
2. Verify Keystone connectivity: `docker exec <service>_server curl -s http://keystone:5000/v3/`
3. Check config override syntax: `docker exec <service>_server cat /etc/<service>/<service>.conf | grep -i error` -- look for malformed INI entries
4. Verify database connectivity: `docker exec <service>_server mysql -h mariadb -u <service> -p<password> -e "SELECT 1"`
5. If config override is the problem: fix the file in `/etc/kolla/config/<service>/` and rerun `reconfigure --tags <service>`

### Rollback After Failed Upgrade

**Symptoms:** Upgrade failed partway through and the cloud is in an inconsistent state. Need to restore previous working state.

**Resolution steps:**
1. **Stop all services:** `kolla-ansible -i /etc/kolla/inventory stop`
2. **Restore database from backup:**
   ```bash
   # Find the backup
   ls /var/lib/docker/volumes/mariadb_backup/_data/

   # Restore (Kolla-Ansible provides a restore procedure)
   kolla-ansible -i /etc/kolla/inventory mariadb_recovery
   ```
3. **Revert globals.yml:**
   ```bash
   git -C /etc/kolla checkout HEAD~1 -- globals.yml
   ```
4. **Pull previous release images:**
   ```bash
   # Set openstack_release back to previous version
   kolla-ansible -i /etc/kolla/inventory pull
   ```
5. **Redeploy:**
   ```bash
   kolla-ansible -i /etc/kolla/inventory deploy
   ```
6. **Verify:** Run the full verification suite from the deployment skill

### Ansible Connection Failures

**Symptoms:** Kolla-Ansible commands fail before any container operations with SSH or become errors.

**Resolution steps:**
1. Check SSH connectivity: `ssh <inventory-host>` -- verify SSH key auth works
2. Check become password: if `ansible_become_pass` is required, verify it in the inventory or pass via `--ask-become-pass`
3. Check inventory file: verify hostnames/IPs in `/etc/kolla/inventory` match actual reachable hosts
4. Check Ansible version compatibility: `ansible --version` -- must be compatible with the Kolla-Ansible release
5. Check Python on target: Kolla-Ansible requires Python on managed hosts; verify with `ssh <host> python3 --version`

## Integration Points

- **Kolla-ansible (deployment) skill:** Shares the same inventory file, globals.yml, and passwords.yml. This skill picks up where the deployment skill leaves off. The deployment skill covers the initial `bootstrap-servers` and `deploy` commands; this skill covers everything that happens after the cloud is running. Both skills reference the same Kolla-Ansible documentation and configuration patterns.
- **Backup skill:** Every upgrade and reconfigure operation should be preceded by a backup. The backup skill provides the procedures for database dumps, configuration archives, and volume snapshots. This skill references those procedures at the start of every upgrade workflow.
- **Monitoring skill:** After every operational change (reconfigure, upgrade, restart), verify service health through monitoring dashboards. The monitoring skill provides the metrics and alerts; this skill consumes those health signals to confirm operations succeeded.
- **Security skill:** Certificate renewal triggers reconfigure operations. Password rotation requires updating passwords.yml and running reconfigure. The security skill defines the security policies; this skill implements the operational procedures to apply those policies.
- **All core skills:** Every OpenStack service is managed through Kolla-Ansible containers. A reconfigure operation affects the service's configuration; an upgrade changes its container image. Changes to any service follow the procedures in this skill.
- **EXEC agent:** The primary consumer for infrastructure changes. When the EXEC agent needs to modify the running cloud (change a configuration, upgrade a service, perform maintenance), it uses the procedures in this skill to execute those changes safely and verifiably.

## NASA SE Cross-References

| SE Phase | Kolla-Ansible Ops Activity | Reference |
|----------|---------------------------|-----------|
| Phase C (Final Design) | Configuration management: all Kolla-Ansible configurations (globals.yml, inventory, passwords.yml, config overrides) are version-controlled and baselined. Every change produces a documented commit with rationale. | SP-6105 SS 6.5 (Configuration Management -- change control process) |
| Phase E (Operations) | Maintenance and upgrade operations: service reconfiguration, patch upgrades, major upgrades, container management, maintenance mode. Each operation follows a documented procedure with prechecks, execution, and verification steps. | SP-6105 SS 5.4 (Product Validation -- operational maintenance) |
| Phase E (Sustainment) | Infrastructure lifecycle: the ongoing cycle of monitor -> identify change -> plan change -> precheck -> execute -> verify -> document that keeps the cloud healthy and current. This cycle maps directly to NASA's sustainment process. | NPR 7123.1 SS 5.4 (Sustainment -- operational baseline evolution) |
