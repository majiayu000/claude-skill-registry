---
name: openstack-security
description: "OpenStack security operations skill for hardening, certificate management, and security posture assessment of cloud infrastructure. Covers TLS certificate lifecycle (generation, deployment, rotation, expiry monitoring), security group management (default deny, minimum required openings), RBAC policy customization (per-service policy.yaml), network segmentation (management vs tenant vs external), audit logging (Keystone CADF events), vulnerability assessment procedures, compliance auditing, intrusion detection patterns, incident response procedures (credential compromise, instance compromise), password rotation, and API rate limiting. Use when hardening OpenStack, managing certificates, auditing security posture, or responding to security incidents."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-22"
      triggers:
        intents:
          - "security"
          - "hardening"
          - "certificate"
          - "TLS"
          - "CVE"
          - "vulnerability"
          - "compliance"
          - "audit"
          - "firewall"
          - "security group"
          - "RBAC"
        contexts:
          - "hardening openstack"
          - "managing certificates"
          - "security auditing"
          - "responding to security incident"
---

# OpenStack Security Operations

Security posture management for OpenStack requires defense-in-depth: no single control prevents all threats, so multiple overlapping layers protect the cloud. The defense layers are **network segmentation** (isolate management from tenant from external traffic), **TLS everywhere** (encrypt all API communication), **RBAC least-privilege** (users and services get only the permissions they need), and **audit logging** (record every authentication and authorization decision).

Security is not a one-time deployment task. Certificates expire. Vulnerabilities are disclosed. Passwords must rotate. Security groups drift. The GUARD agent consumes this skill for continuous security posture assessment, evaluating whether the cloud's security controls remain effective against evolving threats.

In NASA SE terms, security spans multiple phases: **Phase B** (security design and architecture), **Phase C** (certificate generation and TLS deployment), **Phase D** (security audit verification), and **Phase E** (ongoing security operations). SP-6105 SS 6.4 (Technical Risk Management) provides the framework for identifying, assessing, and mitigating security risks throughout the cloud lifecycle.

## Deploy

### Security-First Deployment

**Kolla-Ansible TLS configuration (globals.yml):**

```yaml
# Enable TLS on all interfaces
kolla_enable_tls_internal: "yes"
kolla_enable_tls_external: "yes"
kolla_copy_ca_into_containers: "yes"

# Certificate paths
kolla_external_fqdn_cert: "/etc/kolla/certificates/haproxy.pem"
kolla_internal_fqdn_cert: "/etc/kolla/certificates/haproxy-internal.pem"
kolla_admin_openrc_cacert: "/etc/kolla/certificates/ca/root.crt"

# Optional: client certificate verification
kolla_enable_tls_backend: "yes"  # Encrypt HAProxy-to-service traffic
```

**Generating certificates:**

```bash
# Self-signed CA (lab/development)
mkdir -p /etc/kolla/certificates/ca
openssl genrsa -out /etc/kolla/certificates/ca/root.key 4096
openssl req -x509 -new -nodes -key /etc/kolla/certificates/ca/root.key \
  -sha256 -days 3650 -out /etc/kolla/certificates/ca/root.crt \
  -subj "/C=US/ST=Lab/O=OpenStack/CN=Kolla-CA"

# HAProxy certificate (external)
openssl genrsa -out /etc/kolla/certificates/haproxy.key 2048
openssl req -new -key /etc/kolla/certificates/haproxy.key \
  -out /etc/kolla/certificates/haproxy.csr \
  -subj "/C=US/ST=Lab/O=OpenStack/CN=${KOLLA_EXTERNAL_FQDN}" \
  -addext "subjectAltName=DNS:${KOLLA_EXTERNAL_FQDN},IP:${KOLLA_EXTERNAL_VIP}"

openssl x509 -req -in /etc/kolla/certificates/haproxy.csr \
  -CA /etc/kolla/certificates/ca/root.crt \
  -CAkey /etc/kolla/certificates/ca/root.key \
  -CAcreateserial -out /etc/kolla/certificates/haproxy.crt \
  -days 365 -sha256

# Combine into PEM (required by HAProxy)
cat /etc/kolla/certificates/haproxy.crt \
    /etc/kolla/certificates/haproxy.key \
    > /etc/kolla/certificates/haproxy.pem

# Internal certificate (same process with internal FQDN/VIP)
# ... repeat with kolla_internal_fqdn and kolla_internal_vip
```

**HAProxy TLS termination:**

HAProxy handles TLS for all OpenStack API endpoints. Kolla-Ansible configures this automatically when TLS is enabled. Verify:

```bash
# Check HAProxy is serving TLS
openssl s_client -connect ${KOLLA_EXTERNAL_VIP}:443 -showcerts </dev/null 2>/dev/null | head -20

# Verify certificate chain
openssl s_client -connect ${KOLLA_EXTERNAL_VIP}:5000 -CAfile /etc/kolla/certificates/ca/root.crt </dev/null 2>/dev/null | grep "Verify return code"
# Expected: Verify return code: 0 (ok)
```

**Firewall rules for management network:**

```bash
# Allow only necessary ports on management interface
firewall-cmd --zone=management --add-service=ssh --permanent
firewall-cmd --zone=management --add-port=5000/tcp --permanent  # Keystone
firewall-cmd --zone=management --add-port=8774/tcp --permanent  # Nova
firewall-cmd --zone=management --add-port=9696/tcp --permanent  # Neutron
firewall-cmd --zone=management --add-port=8776/tcp --permanent  # Cinder
firewall-cmd --zone=management --add-port=9292/tcp --permanent  # Glance
firewall-cmd --zone=management --add-port=8080/tcp --permanent  # Swift
firewall-cmd --zone=management --add-port=8004/tcp --permanent  # Heat
firewall-cmd --zone=management --add-port=443/tcp --permanent   # Horizon
firewall-cmd --zone=management --add-port=3000/tcp --permanent  # Grafana
firewall-cmd --zone=management --add-port=9090/tcp --permanent  # Prometheus
firewall-cmd --reload

# Default deny on all other ports
firewall-cmd --zone=management --set-target=DROP --permanent
firewall-cmd --reload
```

**Security group defaults:**

```bash
# Create restrictive default security group rules
openstack security group rule delete $(openstack security group rule list default -f value -c ID)
# Start with no rules (default deny)

# Add only SSH and ICMP for management
openstack security group rule create --protocol tcp --dst-port 22 --remote-ip 10.0.0.0/8 default
openstack security group rule create --protocol icmp default
```

## Configure

### Certificate Lifecycle Management

**Certificate inventory:**

| Certificate | Location | Expiry | Rotation Frequency |
|-------------|----------|--------|-------------------|
| CA root | `/etc/kolla/certificates/ca/root.crt` | 10 years | Rarely (re-sign all on rotation) |
| HAProxy external | `/etc/kolla/certificates/haproxy.pem` | 1 year | Annually (or before expiry) |
| HAProxy internal | `/etc/kolla/certificates/haproxy-internal.pem` | 1 year | Annually |
| Service backend | Per-service in `/etc/kolla/<service>/` | 1 year | Annually |

**Expiry monitoring:**

```bash
#!/bin/bash
# check-cert-expiry.sh -- alert on certificates expiring within 30 days
THRESHOLD_DAYS=30
THRESHOLD_SECS=$((THRESHOLD_DAYS * 86400))

for cert in /etc/kolla/certificates/*.pem /etc/kolla/certificates/*.crt; do
  [ -f "$cert" ] || continue
  expiry=$(openssl x509 -in "$cert" -noout -enddate 2>/dev/null | cut -d= -f2)
  expiry_epoch=$(date -d "$expiry" +%s 2>/dev/null)
  now_epoch=$(date +%s)
  remaining=$((expiry_epoch - now_epoch))

  if [ $remaining -lt $THRESHOLD_SECS ]; then
    echo "WARNING: $cert expires in $((remaining / 86400)) days ($expiry)"
  fi
done
```

**Rotation procedure:**

```bash
# 1. Generate new certificate (see Deploy section)
# 2. Replace PEM file
cp /etc/kolla/certificates/haproxy-new.pem /etc/kolla/certificates/haproxy.pem

# 3. Reconfigure HAProxy to pick up new cert
kolla-ansible -i inventory reconfigure --tags haproxy

# 4. Verify
openssl s_client -connect ${KOLLA_EXTERNAL_VIP}:443 </dev/null 2>/dev/null | openssl x509 -noout -dates
```

### RBAC Policy Customization

**Per-service policy files:**

Each OpenStack service has a `policy.yaml` (or `policy.json`) that defines authorization rules:

```bash
# Location: /etc/kolla/<service>/policy.yaml
# Kolla-Ansible merges custom policies with code defaults

# Example: Keystone -- restrict user creation to domain admins
# /etc/kolla/keystone/policy.yaml
"identity:create_user": "rule:admin_required and domain_id:%(target.user.domain_id)s"

# Example: Nova -- restrict flavor management to cloud admins
# /etc/kolla/nova/policy.yaml
"os_compute_api:os-flavor-manage": "role:admin and is_admin_project:True"

# Example: Neutron -- restrict external network creation
# /etc/kolla/neutron/policy.yaml
"create_network:router:external": "role:admin"
```

**Best practices:**
- Start with defaults; override only what you need
- Document every policy override with rationale
- Test policy changes with a non-admin user before deploying
- Use `oslopolicy-checker` to validate policy files

```bash
# Validate policy syntax
docker exec nova_api oslopolicy-checker --policy /etc/nova/policy.yaml
```

### Network Segmentation

| Network | Purpose | VLAN/Subnet | Access Control |
|---------|---------|-------------|---------------|
| Management | API endpoints, admin access | VLAN 100 / 10.0.100.0/24 | Firewall: SSH + API ports only |
| Tenant (overlay) | VM-to-VM traffic | VXLAN / 10.0.1.0/24 | Neutron security groups |
| External (provider) | Internet-facing, floating IPs | VLAN 200 / 192.168.1.0/24 | NAT + security groups |
| Storage (optional) | Cinder/Swift backend | VLAN 300 / 10.0.200.0/24 | No external access |

### Audit Logging

**Keystone CADF events:**

```ini
# keystone.conf
[DEFAULT]
notification_driver = messagingv2
notification_format = cadf

# CADF events include:
# - authentication.authenticate (success/failure)
# - identity.authenticate.pending
# - identity.create_user
# - identity.update_project
# - identity.delete_role_assignment
```

**Log aggregation for security events:**

```bash
# Search for failed authentication attempts
docker logs keystone_api 2>&1 | grep -i "authentication failed\|401\|Unauthorized" | tail -20

# Search for RBAC denials
docker logs nova_api 2>&1 | grep -i "policy\|403\|Forbidden" | tail -20

# Aggregate across all services
for svc in keystone nova neutron cinder glance; do
  echo "=== ${svc} ==="
  docker logs ${svc}_api 2>&1 | grep -c "401\|403" || echo 0
done
```

### Password Rotation

```bash
# 1. Generate new passwords
kolla-genpwd  # Or manually update /etc/kolla/passwords.yml

# 2. Reconfigure services to use new passwords
kolla-ansible -i inventory reconfigure

# 3. Verify all services authenticate with new credentials
openstack token issue
openstack service list
```

### API Rate Limiting

Configure HAProxy rate limiting to prevent brute-force attacks:

```
# /etc/kolla/haproxy/haproxy.cfg (via Kolla-Ansible custom config)
frontend keystone_api
  stick-table type ip size 100k expire 30s store http_req_rate(10s)
  http-request deny deny_status 429 if { sc_http_req_rate(0) gt 100 }
  http-request track-sc0 src
```

### Service Account Hardening

```bash
# List all service accounts
openstack user list --domain default --project service

# Verify each service account has only the required role
for svc in nova neutron cinder glance swift heat; do
  echo "=== ${svc} ==="
  openstack role assignment list --user ${svc} --names
done
# Each should have exactly "admin" role on "service" project -- no more
```

## Operate

### Certificate Rotation Procedures

**Planned rotation (before expiry):**

1. Generate new certificate with same SAN entries
2. Verify new certificate: `openssl x509 -in new.crt -noout -text`
3. Create combined PEM: `cat new.crt new.key > new.pem`
4. Backup current certificate: `cp haproxy.pem haproxy.pem.bak`
5. Replace: `cp new.pem haproxy.pem`
6. Reconfigure: `kolla-ansible -i inventory reconfigure --tags haproxy`
7. Verify all endpoints: `openstack token issue`

**Emergency rotation (compromised key):**

1. Revoke compromised certificate (if using CA with CRL)
2. Generate new key pair immediately (do not reuse old key)
3. Issue new certificate from CA
4. Deploy and reconfigure (same as planned rotation steps 3-7)
5. Audit: review logs for unauthorized access during compromise window
6. Rotate all service passwords as precaution

### Security Audit Checklist

**Weekly:**
- [ ] Review failed authentication logs (Keystone CADF)
- [ ] Check for unauthorized API access patterns
- [ ] Verify security group rules unchanged from baseline
- [ ] Confirm certificate expiry > 30 days

**Monthly:**
- [ ] Run vulnerability scan against API endpoints
- [ ] Review RBAC policies against least-privilege baseline
- [ ] Audit service account permissions
- [ ] Check for CVEs affecting deployed OpenStack version
- [ ] Verify audit logging is active and rotated properly

**Quarterly:**
- [ ] Conduct penetration test scope review
- [ ] Review network segmentation effectiveness
- [ ] Rotate service account passwords
- [ ] Update security baseline documentation

### Incident Response Procedures

**Compromised credential (user or service account):**

```bash
# 1. Immediately revoke all tokens for the compromised user
openstack token revoke $(openstack token issue -c id -f value)  # For current token
# Disable user to prevent new token issuance
openstack user set --disable <compromised-user>

# 2. Rotate the compromised password
openstack user set --password-prompt <compromised-user>

# 3. Rotate Fernet keys to invalidate all outstanding tokens
kolla-ansible -i inventory keystone_fernet_rotate

# 4. Audit: review what the compromised credential accessed
docker logs keystone_api 2>&1 | grep "<compromised-user>" | tail -100

# 5. Re-enable user with new password after investigation
openstack user set --enable <compromised-user>
```

**Compromised instance:**

```bash
# 1. Isolate: remove from all security groups (cuts network)
openstack server remove security group <instance-id> default

# 2. Snapshot for forensics
openstack server image create --name "forensic_$(date +%Y%m%d)" <instance-id>

# 3. Review console log for indicators of compromise
openstack console log show <instance-id> | tail -200

# 4. Terminate if confirmed compromised
openstack server delete <instance-id>

# 5. Audit: check if lateral movement occurred
# Review Neutron flow logs, Keystone auth logs for the instance's IP
```

### Compliance Reporting

Generate compliance evidence for auditors:

```bash
# TLS status across all endpoints
for port in 5000 8774 9696 8776 9292 8080 8004 443; do
  echo "=== Port ${port} ==="
  echo | openssl s_client -connect ${KOLLA_EXTERNAL_VIP}:${port} 2>/dev/null | \
    openssl x509 -noout -subject -dates -issuer
done

# RBAC policy summary
for svc in keystone nova neutron cinder glance swift heat horizon; do
  echo "=== ${svc} ==="
  [ -f /etc/kolla/${svc}/policy.yaml ] && wc -l /etc/kolla/${svc}/policy.yaml || echo "Using defaults"
done

# Security group audit
openstack security group list --all-projects -f table
openstack security group rule list default -f table
```

### Security Patch Workflow

```bash
# 1. Check for CVEs
# Review: https://security.openstack.org/ossalist.html

# 2. Assess impact against deployed version
openstack versions show  # or check container image tags
docker inspect --format '{{.Config.Labels}}' nova_api | python3 -m json.tool

# 3. If patch required, update container images
kolla-ansible -i inventory pull  # Pull latest images

# 4. Deploy updated containers
kolla-ansible -i inventory upgrade  # Rolling upgrade

# 5. Verify services after upgrade
openstack token issue
openstack server list
openstack network list
```

## Troubleshoot

### 1. TLS Certificate Expired

**Symptoms:** All API calls fail with SSL errors. Services cannot communicate. `curl: (60) SSL certificate problem: certificate has expired`.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| HAProxy cert expired | `openssl s_client -connect VIP:443 </dev/null 2>/dev/null \| openssl x509 -noout -dates` | Generate new cert; replace PEM; `kolla-ansible reconfigure --tags haproxy` |
| CA cert expired | All services fail simultaneously with chain verification errors | Regenerate CA; re-sign all service certs; full reconfigure |
| Backend cert expired | HAProxy healthy but individual services fail internally | Check: `docker exec nova_api openssl x509 -in /etc/nova/ssl/cert.pem -noout -dates` |

### 2. Certificate Chain Incomplete

**Symptoms:** Browser warnings on Horizon ("Not Secure"). API clients reject connection with `unable to get local issuer certificate`.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Intermediate CA missing from PEM | `openssl verify -CAfile ca.crt haproxy.crt` fails | Concatenate intermediate: `cat cert.crt intermediate.crt key.key > haproxy.pem` |
| CA not distributed to containers | `docker exec nova_api openssl verify -CAfile /etc/pki/tls/certs/ca-bundle.crt /etc/nova/ssl/cert.pem` | Set `kolla_copy_ca_into_containers: yes`; reconfigure |
| Wrong certificate order in PEM | HAProxy serves wrong cert for SNI | Verify order: server cert first, then intermediates, then key |

### 3. Security Group Blocking Legitimate Traffic

**Symptoms:** Instances cannot reach expected services. SSH works from some IPs but not others.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Overly restrictive rules | `openstack security group rule list <sg-id>` -- missing required port/protocol | Add rule: `openstack security group rule create --protocol tcp --dst-port <port> <sg-id>` |
| Wrong direction (ingress vs egress) | Rule exists but for wrong direction | Delete and recreate with correct `--ingress` or `--egress` |
| Remote IP/group mismatch | Source CIDR too narrow or references wrong security group | Update remote-ip or remote-group in rule |
| Stateful tracking table full | High-connection services (web, database) drop new connections | Increase conntrack limit or use stateless rules for high-traffic ports |

### 4. RBAC Policy Denying Authorized Actions

**Symptoms:** Users with correct roles get `403 Forbidden`. Actions worked previously but stopped.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| policy.yaml syntax error | `python3 -c "import yaml; yaml.safe_load(open('policy.yaml'))"` fails | Fix YAML syntax; validate before deploying |
| Role mismatch | User has `member` but rule requires `admin` | Update policy to accept correct role, or assign correct role to user |
| Scope mismatch | Project-scoped token but rule requires domain scope | Reauth with correct scope: `--os-domain-name` instead of `--os-project-name` |
| Policy file not loaded | Service using cached old policy | Restart service container: `docker restart nova_api` |

### 5. Audit Log Overflow

**Symptoms:** Disk filling with log data. Log rotation not working. Log queries extremely slow.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Log storage full | `df -h /var/lib/docker/containers/` high | Prune old container logs: `docker system prune --volumes`; configure log rotation |
| Rotation misconfigured | Logs growing without bound | Set Docker log driver options: `"max-size": "100m", "max-file": "5"` in daemon.json |
| Excessive debug logging | Debug mode left enabled after troubleshooting | Disable debug: set `debug = false` in service configs; restart containers |

### 6. Service Account Password Expired or Changed

**Symptoms:** Cross-service calls fail. Token validation works but service-to-service 401. `docker logs nova_api` shows `Unauthorized` accessing Keystone.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Password rotated without updating all consumers | One service has old password in config | Run `kolla-ansible reconfigure` to sync all passwords from passwords.yml |
| Manual password change not propagated | `openstack user show nova` password hash differs from config | Update password in passwords.yml; reconfigure |
| Password expired (if password policy enforced) | Keystone logs: `Password expired for user nova` | Rotate password: update in Keystone + passwords.yml + reconfigure |

## Integration Points

Security connects to every component of the cloud stack because every component has attack surface:

**Keystone skill:** RBAC policies are Keystone's domain. Token security (Fernet key management, token lifetime, revocation) is a joint concern. Federation security (SAML assertion validation, OIDC token verification) requires coordinated configuration between Keystone and the external IdP.

**Monitoring skill:** Security event alerting -- failed authentication spikes trigger monitoring alerts. Certificate expiry countdown is a Prometheus metric. Unauthorized API access patterns detected through metric analysis feed security incident response.

**Backup skill:** Backup encryption protects sensitive data at rest. Credential backup (passwords.yml, Fernet keys) requires secure storage with access controls separate from general backup storage. Backup access itself is a security-auditable activity.

**Networking-debug skill:** Security group analysis is a core part of network troubleshooting. When traffic is blocked, the first question is "is it a security group rule?" Network segmentation verification (management vs tenant vs external isolation) is a joint security/networking concern.

**All core OpenStack skills:** TLS configuration affects every service endpoint. Each service has keystonemiddleware for token validation, service account credentials, and API endpoint security. Security hardening is not a separate layer -- it is woven into every service deployment.

**GUARD agent:** Primary consumer. GUARD uses this skill for continuous security posture assessment: "Are certificates current? Are RBAC policies least-privilege? Any suspicious authentication patterns? Any unpatched CVEs?" Security data is GUARD's primary input for posture evaluation.

## NASA SE Cross-References

| SE Phase | Security Activity | Reference |
|----------|-------------------|-----------|
| Phase B (Preliminary Design) | Define security architecture: network segmentation, TLS strategy, RBAC model, audit requirements | SP-6105 SS 4.3-4.4 |
| Phase C (Final Design & Build) | Generate certificates, configure TLS in globals.yml, establish security group baselines, deploy firewall rules | SP-6105 SS 5.1 |
| Phase D (Integration & Test) | Security audit: verify TLS on all endpoints, validate RBAC policies, test security group isolation, vulnerability scan | SP-6105 SS 5.2-5.3 |
| Phase E (Operations & Sustainment) | Certificate rotation, security audit cadence (weekly/monthly/quarterly), incident response, CVE monitoring, compliance reporting | SP-6105 SS 5.4-5.5 |
| Phase E (Technical Risk Management) | Ongoing risk assessment: identify new threats, evaluate impact, update mitigations, track residual risk | SP-6105 SS 6.4 |
| Phase F (Closeout) | Secure data destruction, credential revocation, audit log archive, final security posture report | SP-6105 SS 6.1 |
