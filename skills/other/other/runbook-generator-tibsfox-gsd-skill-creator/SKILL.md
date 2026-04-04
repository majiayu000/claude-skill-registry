---
name: runbook-generator
description: "Guidance for generating OpenStack runbooks with dual task/symptom indexing following NASA procedure standards. Use when creating incident response procedures, operational runbooks, or troubleshooting guides that must be verified against running infrastructure."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-22"
      triggers:
        intents:
          - "runbook"
          - "incident response"
          - "troubleshoot"
          - "on-call"
          - "symptom index"
          - "task index"
          - "generate runbook"
        contexts:
          - "creating runbook entries"
          - "building incident response library"
          - "documenting troubleshooting procedures"
---

# Runbook Generator

This skill guides agents producing runbook library content for the GSD OpenStack Cloud Platform. Runbooks provide step-by-step procedures indexed by both task (what you want to do) and symptom (what went wrong), following the NASA procedure format from SP-6105 SS 5.3 (Product Verification) and the operational handoff requirements of NPR 7123.1 Process 9 (Product Transition).

Runbooks differ from operations manual procedures in scope and intent. Operations manual procedures cover planned, routine activities (health checks, upgrades, backups). Runbooks cover reactive activities (incident response, troubleshooting, failure recovery) and operational tasks that may be performed under time pressure.

## Runbook Entry Format

Every runbook entry follows the standard format defined in the project vision (Section 2.3 of gsd-openstack-nasa-vision.md):

```
RUNBOOK: RB-{SERVICE}-{NNN} -- {TITLE}
SE Phase Reference: NPR 7123.1 SS {section}
Last Verified Against: {OpenStack release version}, {YYYY-MM-DD}
Verification Method: {automated / manual / both}

PRECONDITIONS
  1. {System state required before starting}
  2. {Access level or credentials needed}
  3. {Related services that must be available}

PROCEDURE
  Step 1: {Exact command or action}
    Expected: {What you should see}
    If not: {Go to step N / escalate to {role} / see RB-{SERVICE}-{NNN}}

  Step 2: {Exact command or action}
    Expected: {What you should see}
    If not: {Recovery action}

  Step N: ...

VERIFICATION
  1. {How to confirm the procedure resolved the issue}
  2. {Service health check command and expected output}
  3. {Monitoring metric that should return to normal}

ROLLBACK
  1. {How to undo changes if the procedure made things worse}
  2. {Steps to restore previous state}
  3. {Confirmation that rollback succeeded}

RELATED RUNBOOKS
  - RB-{SERVICE}-{NNN}: {Title} -- {When to use instead}
  - OPS-{SERVICE}-{NUMBER}: {Title} -- {Related ops manual procedure}
```

### Runbook ID Format

- Pattern: `RB-{SERVICE}-{NNN}`
- SERVICE: Uppercase service name (KEYSTONE, NOVA, NEUTRON, CINDER, GLANCE, SWIFT, HEAT, HORIZON, KOLLA, GENERAL)
- NNN: 3-digit sequential number per service, starting at 001
- Cross-service runbooks use GENERAL prefix
- Examples: `RB-NOVA-001`, `RB-KEYSTONE-003`, `RB-GENERAL-005`

## Dual Indexing System

Runbooks are indexed two ways so operators can find the right procedure regardless of their starting context. An operator who knows what they want to do uses the task index. An operator responding to an incident uses the symptom index.

### Task Index

The task index organizes runbooks by operational intent. Categories follow the operational lifecycle:

**DEPLOY** -- Initial setup and infrastructure expansion
- Initial deployment (single-node)
- Initial deployment (multi-node)
- Add compute node
- Add storage node
- Add network node

**OPERATE** -- Day-to-day operational tasks
- Create project and users
- Configure networking for project
- Launch instance from image
- Attach block storage
- Create and restore backup
- Apply security update
- Perform rolling upgrade

**MONITOR** -- Scheduled observation and assessment
- Daily health check
- Weekly capacity review
- Monthly security audit
- Quarterly performance baseline

The task index file lives at `docs/runbooks/task-index.md`. Each entry links to the corresponding runbook by RB ID.

### Symptom Index

The symptom index organizes runbooks by failure observation. Operators start here when something is broken and they need to diagnose the cause.

**INSTANCE WON'T LAUNCH**
- Check Nova scheduler logs for placement failures
- Verify hypervisor resources (vCPU, RAM, disk)
- Check Neutron port allocation
- Verify Glance image availability and format
- Check Keystone authentication and service catalog

**NETWORK UNREACHABLE**
- Verify OVS/OVN bridge status and flows
- Check Neutron DHCP agent status
- Verify security group rules allow traffic
- Check floating IP allocation and association
- Trace packet path through SDN layer

**STORAGE UNAVAILABLE**
- Check Cinder volume service status
- Verify backend connectivity (LVM/Ceph/NFS)
- Check iSCSI/NFS target status
- Verify volume attachment state in Nova
- Check disk space on storage nodes

**AUTHENTICATION FAILED**
- Verify Keystone service status and endpoints
- Check token expiration and Fernet key rotation
- Verify service catalog endpoint URLs
- Check TLS certificate validity and chain
- Verify RBAC policy files and project scoping

The symptom index file lives at `docs/runbooks/symptom-index.md`. Each entry links to one or more runbooks that address the symptom.

### Index Requirements

1. Every runbook must appear in at least one task index category.
2. Every runbook must be discoverable from at least one symptom index entry.
3. A single runbook may appear under multiple symptoms (e.g., a Keystone troubleshooting runbook appears under both AUTHENTICATION FAILED and INSTANCE WON'T LAUNCH).
4. Index entries include the runbook ID, title, and a one-line description of when to use it.

## Runbook Categories by Service

Each OpenStack service requires runbook coverage for its most common failure modes and operational tasks. This list defines the minimum runbook set per service.

### Keystone (Identity)
- Token issuance failures (expired Fernet keys, clock skew)
- Service catalog problems (missing endpoints, wrong URLs)
- RBAC failures (policy misconfiguration, project scoping errors)
- Federation issues (IdP connectivity, assertion mapping)

### Nova (Compute)
- Instance launch failures (scheduler, image, network, resource)
- Scheduling problems (host aggregate, availability zone, placement)
- Hypervisor issues (libvirt connectivity, resource reporting)
- Live migration (pre-check, execute, troubleshoot failures)

### Neutron (Networking)
- Network connectivity loss (OVS/OVN bridge, flow rules)
- DHCP failures (agent down, port binding, namespace issues)
- Floating IP issues (allocation exhaustion, association state)
- Security group problems (rule conflicts, default deny)
- OVS/OVN issues (bridge status, flow tables, controller connectivity)

### Cinder (Block Storage)
- Volume creation failures (backend capacity, driver errors)
- Attachment issues (iSCSI/NFS target, multipath, Nova coordination)
- Backend connectivity (LVM health, Ceph cluster status, NFS mount)
- Snapshot problems (consistency groups, backend limitations)

### Glance (Image Service)
- Image upload failures (format validation, backend storage full)
- Format conversion issues (raw to qcow2, image properties)
- Metadata problems (property inheritance, visibility settings)

### Swift (Object Storage)
- Container access issues (ACL misconfiguration, token scoping)
- Replication problems (ring consistency, replicator status)
- Quota issues (account/container quotas, rate limiting)

### Heat (Orchestration)
- Stack creation failures (template validation, dependency resolution)
- Template validation errors (HOT syntax, resource type support)
- Resource dependency issues (circular references, ordering)

### Horizon (Dashboard)
- Dashboard access issues (memcached sessions, Apache config)
- Session problems (timeout, cookie domain, CSRF token)
- Panel errors (service catalog discovery, API version mismatch)

## Naming Convention

Consistent naming ensures runbooks are findable and sortable.

### ID Structure

```
RB-{SERVICE}-{NNN}

SERVICE = KEYSTONE | NOVA | NEUTRON | CINDER | GLANCE | SWIFT | HEAT | HORIZON | KOLLA | GENERAL
NNN     = 001, 002, 003, ... (3-digit sequential per service)
```

### Rules

1. Each service maintains its own number sequence starting at 001.
2. Cross-service runbooks (affecting multiple services) use the GENERAL prefix.
3. Numbers are never reused. If a runbook is deprecated, its number is retired.
4. Runbook files are named by ID: `docs/runbooks/RB-NOVA-001.md`, `docs/runbooks/RB-GENERAL-003.md`.

### Number Allocation Ranges

| Service | Range | Example |
|---------|-------|---------|
| KEYSTONE | RB-KEYSTONE-001 through RB-KEYSTONE-099 | RB-KEYSTONE-001 |
| NOVA | RB-NOVA-001 through RB-NOVA-099 | RB-NOVA-015 |
| NEUTRON | RB-NEUTRON-001 through RB-NEUTRON-099 | RB-NEUTRON-003 |
| CINDER | RB-CINDER-001 through RB-CINDER-099 | RB-CINDER-007 |
| GLANCE | RB-GLANCE-001 through RB-GLANCE-099 | RB-GLANCE-002 |
| SWIFT | RB-SWIFT-001 through RB-SWIFT-099 | RB-SWIFT-004 |
| HEAT | RB-HEAT-001 through RB-HEAT-099 | RB-HEAT-001 |
| HORIZON | RB-HORIZON-001 through RB-HORIZON-099 | RB-HORIZON-005 |
| KOLLA | RB-KOLLA-001 through RB-KOLLA-099 | RB-KOLLA-010 |
| GENERAL | RB-GENERAL-001 through RB-GENERAL-099 | RB-GENERAL-001 |

## Verification Integration

Runbooks connect to the verification pipeline to ensure accuracy against running infrastructure.

### Verification Classification

Each runbook specifies whether its verification is automated, manual, or both:

| Type | Meaning | Doc-Verifier Role |
|------|---------|-------------------|
| Automated | Verification commands can be extracted and run by doc-verifier | doc-verifier executes verification section commands and compares output |
| Manual | Verification requires human judgment or physical access | doc-verifier flags as manual-only; human must confirm |
| Both | Some steps automated, some require human judgment | doc-verifier runs automated steps and flags manual steps for review |

### Verification Tracking

1. **Last-verified date** tracks when the runbook was confirmed against a running system. Stored in the runbook header.
2. **System version** records which OpenStack release the runbook was verified against.
3. **Unverified runbooks must carry a visible warning** at the top of the entry:

```
WARNING: UNVERIFIED RUNBOOK
This runbook has not been verified against the current system version.
Last verified: {date} against {version}.
Current system: {version}.
Execute each step with extra caution and verify results manually.
```

4. **Verification cadence:** All runbooks should be re-verified after any OpenStack upgrade or major configuration change.

## Output Location

All runbook files are written to `docs/runbooks/` following the filesystem contracts:

| File | Content |
|------|---------|
| `docs/runbooks/task-index.md` | Task-organized runbook index (DEPLOY, OPERATE, MONITOR) |
| `docs/runbooks/symptom-index.md` | Symptom-organized runbook index (failure categories) |
| `docs/runbooks/RB-KEYSTONE-*.md` | Keystone service runbooks |
| `docs/runbooks/RB-NOVA-*.md` | Nova service runbooks |
| `docs/runbooks/RB-NEUTRON-*.md` | Neutron service runbooks |
| `docs/runbooks/RB-CINDER-*.md` | Cinder service runbooks |
| `docs/runbooks/RB-GLANCE-*.md` | Glance service runbooks |
| `docs/runbooks/RB-SWIFT-*.md` | Swift service runbooks |
| `docs/runbooks/RB-HEAT-*.md` | Heat service runbooks |
| `docs/runbooks/RB-HORIZON-*.md` | Horizon service runbooks |

## Cross-References

| Resource | Purpose |
|----------|---------|
| `skills/methodology/nasa-se/SKILL.md` | SE lifecycle phase context -- runbooks map to Phase E (Operations & Sustainment) per SP-6105 SS 5.4-5.5 |
| `skills/methodology/ops-manual-writer/SKILL.md` | Procedure format alignment -- runbooks follow compatible format with operations manual procedures |
| `skills/methodology/doc-verifier/SKILL.md` | Automated verification methods for runbook accuracy against running infrastructure |
| `docs/filesystem-contracts.md` | Output location contracts for `docs/runbooks/` directory |
| NASA SP-6105 SS 5.3 | Product Verification process -- runbooks as verification artifacts for operational procedures |
| NPR 7123.1 SS 3.2 Process 9 | Product Transition -- runbooks satisfy operational handoff requirements |
