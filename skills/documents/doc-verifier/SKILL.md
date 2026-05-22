---
name: doc-verifier
description: "Guidance for verifying documentation accuracy against running OpenStack infrastructure. Use when detecting documentation drift, validating operations procedures against live systems, or confirming that runbooks produce expected results on the deployed cloud. Implements NASA Product Verification (SP-6105 SS 5.3) applied to documentation artifacts."
user-invocable: true
allowed-tools: Read Grep Glob Bash
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-22"
      triggers:
        intents:
          - "verify docs"
          - "validate procedure"
          - "doc drift"
          - "documentation accuracy"
          - "check runbook"
          - "verify operations manual"
          - "documentation verification"
        contexts:
          - "verifying documentation against running system"
          - "detecting configuration drift"
          - "validating runbook procedures"
          - "auditing operations manual accuracy"
---

# Documentation Verifier

This skill guides agents performing documentation verification for cloud infrastructure. Documentation drift -- the gap between what docs say and what the system does -- is the primary failure mode for operations manuals. The doc-verifier detects drift using NASA's TAID (Test, Analysis, Inspection, Demonstration) verification methods applied to documentation artifacts.

Documentation drift is insidious because it compounds silently. A single undetected drift item erodes operator trust. Once operators stop trusting documentation, they stop reading it and start improvising. The doc-verifier breaks this cycle by making verification systematic and repeatable.

## Drift Detection Methods

Four categories of documentation drift exist, each with distinct detection strategies.

### Configuration Drift

**Definition:** Document says setting `X=A` but the running system has `X=B`.

**Detection strategy:**
1. Parse documented configuration values from procedures (grep for `=`, `:`, or YAML key-value patterns)
2. Read actual configuration files (`/etc/kolla/*/` for Kolla-Ansible deployments, `globals.yml`)
3. Query API for runtime configuration where available (`openstack configuration show`)
4. Compare documented values against actual values
5. Flag mismatches with severity based on operational impact

**Common sources:** Kolla-Ansible `globals.yml` changes, service reconfiguration, security hardening, upgrades.

**Detection patterns:**
- `OPS-KEYSTONE-*`: Compare documented Fernet key rotation interval against `keystone.conf [fernet_tokens]`
- `OPS-NOVA-*`: Compare documented compute driver against `nova.conf [DEFAULT] compute_driver`
- `OPS-NEUTRON-*`: Compare documented ML2 plugin against `ml2_conf.ini [ml2] mechanism_drivers`

### Endpoint Drift

**Definition:** Document references a URL, port, or API endpoint that has changed or is unreachable.

**Detection strategy:**
1. Extract documented endpoints (URLs, `host:port` patterns, API paths)
2. Verify reachability using non-destructive probes (`curl -s -o /dev/null -w "%{http_code}"`)
3. Verify service catalog entries match documented endpoints (`openstack endpoint list`)
4. Check port availability where direct HTTP probes are inappropriate

**Common sources:** TLS migration (HTTP to HTTPS), port changes, VIP address changes, service catalog updates.

### Procedure Drift

**Definition:** Documented steps no longer produce the documented results.

**Detection strategy:**
1. Parse procedure steps to extract commands and expected output
2. Execute read-only commands against the running system
3. Compare actual output to documented expected output
4. For destructive commands, verify preconditions and rollback sections exist without executing

**Common sources:** CLI argument changes across OpenStack releases, output format changes, deprecated subcommands, renamed resources.

**Detection patterns:**
- `RB-KEYSTONE-*`: Run `openstack token issue` and compare output fields to documented fields
- `RB-NOVA-*`: Run `openstack server list` and verify column headers match documentation
- `RB-NEUTRON-*`: Run `openstack network list` and verify output structure

### Version Drift

**Definition:** Document references a software version that has been upgraded or changed.

**Detection strategy:**
1. Extract version references from documentation (OpenStack release names, package versions, container image tags)
2. Compare against installed versions (`openstack versions show`, `rpm -qa | grep openstack`, `docker image ls`)
3. Check Kolla-Ansible container image tags against documented tags
4. Flag version mismatches with assessment of whether procedures are still valid for the new version

**Common sources:** OpenStack minor releases, Kolla container rebuilds, base OS updates, Python package updates.

## Verification Methods (TAID Applied to Documentation)

NASA SP-6105 SS 5.3 defines four verification methods. Applied to documentation verification:

### Test

Execute documented commands and compare output to documented expected results.

**Approach:**
- For each procedure, extract commands (lines starting with `$`, `#`, or indented code blocks)
- Extract expected output (lines following "Expected:" or "Output:" or indented below commands)
- Execute the command on the running system
- Compare actual output to expected output using the appropriate comparison strategy

**Comparison strategies:**
- **Exact match:** Deterministic output (version strings, configuration values, boolean results)
- **Pattern match:** Dynamic values using regex (timestamps, UUIDs, request IDs, IP addresses)
- **Presence check:** Structural elements that must exist but whose values vary (column headers, section markers)
- **Subset check:** Output must contain documented elements but may have additional items

### Analysis

Compare documented configuration values against running configuration without executing commands.

**Approach:**
- Parse documented config values from procedures and operations manual
- Read actual configuration files from disk or API
- Compute the diff between documented and actual values
- Assess whether differences affect procedure validity

**Targets:** `globals.yml`, service `.conf` files, policy files, network configurations, certificate parameters.

### Inspection

Review documentation structure for completeness against the required format.

**Checklist for operations procedures (OPS-* format):**
- [ ] Procedure ID present and matches `OPS-{SERVICE}-{NNN}` pattern
- [ ] Title clearly states what the procedure accomplishes
- [ ] SE Phase reference present
- [ ] NPR reference present
- [ ] Last verified date and system version present
- [ ] Purpose section exists
- [ ] Preconditions section exists and lists system state requirements
- [ ] Safety considerations section exists
- [ ] Procedure section has numbered steps with expected results
- [ ] Verification section exists with confirmation steps
- [ ] Rollback section exists with undo steps
- [ ] References section exists

**Checklist for runbooks (RB-* format):**
- [ ] Runbook ID present and matches `RB-{SERVICE}-{NNN}` pattern
- [ ] SE Phase Reference present
- [ ] Last Verified Against date and version present
- [ ] Preconditions section exists
- [ ] Procedure section has numbered steps with expected output
- [ ] Each step has "If not" guidance for unexpected results
- [ ] Verification section exists
- [ ] Rollback section exists
- [ ] Related Runbooks section exists

### Demonstration

Walk through an end-to-end documented scenario and confirm each step works as described.

**Approach:**
- Select a complete operational scenario (e.g., "Create project, configure network, launch instance")
- Follow the documented procedure exactly as written
- Record actual results at each step
- Compare end state to documented end state
- Document any deviations with severity assessment

**Demonstration scenarios (non-destructive):**
- Authentication flow: `openstack token issue` through documented steps
- Resource listing: `openstack server list`, `openstack network list`, `openstack volume list`
- Service health: `openstack compute service list`, `openstack network agent list`

## Automated Verification Framework

### Script Structure

For each documented procedure, build a verification script:

```
INPUT:  Procedure document (Markdown)
PARSE:  Extract (command, expected_output) pairs
FILTER: Remove destructive commands (create, delete, set, update, migrate)
RUN:    Execute read-only commands against running system
COMPARE: Actual vs documented using appropriate strategy
REPORT: Per-procedure pass/fail with specific drift items
```

### Drift Severity Classification

| Severity | Definition | Example |
|----------|-----------|---------|
| **Critical** | Procedure will fail if followed as written | Documented command uses deprecated flag; documented port is wrong |
| **Warning** | Procedure works but output differs from documentation | Column headers changed; additional fields in output |
| **Info** | Cosmetic differences that do not affect procedure outcome | Timestamp format change; UUID casing difference |

### Reporting Format

Each verification run produces a report:

```
VERIFICATION REPORT
Date: [ISO timestamp]
System: [hostname, OpenStack version]
Scope: [which documents were verified]

RESULTS:
  Procedures verified: [N]
  Pass: [N]
  Fail: [N] (Critical: [N], Warning: [N], Info: [N])

DRIFT ITEMS:
  1. [CRITICAL] OPS-NOVA-003 Step 4: 'openstack server create --nic'
     Expected: "net-id" parameter
     Actual: "network" parameter (changed in Zed release)
     Fix: Update command in procedure

  2. [WARNING] RB-KEYSTONE-001 Step 2: 'openstack token issue'
     Expected: 4 columns in output
     Actual: 5 columns (project_domain_id added)
     Fix: Update expected output in runbook
```

## Verification Workflow

**Step 1: Inventory.** Scan `docs/operations-manual/` and `docs/runbooks/` for all documented procedures. Build a registry of procedure IDs, commands, and expected outputs.

**Step 2: Extract assertions.** For each procedure, extract verifiable assertions: commands paired with expected outputs. Tag each assertion as read-only or destructive.

**Step 3: Execute read-only assertions.** Run all read-only commands against the running system. For destructive commands, verify only that preconditions and rollback sections exist.

**Step 4: Compare.** Match actual output to documented output using the appropriate comparison strategy (exact, pattern, presence, subset).

**Step 5: Report.** Generate verification report with drift items classified by severity. Flag Critical items for immediate documentation update.

**Step 6: Update metadata.** For verified documents, update `LAST VERIFIED` date and system version. For documents with Critical drift, mark as `UNVERIFIED` with drift details.

## Safety Constraints

- **NEVER** execute destructive operations during verification (no `openstack server delete`, `openstack network delete`, `openstack volume delete`, `openstack project delete`)
- **NEVER** execute state-modifying operations (no `openstack server create`, `openstack network create`, `openstack user set`)
- **ONLY** read-only verification commands: `list`, `show`, `token issue`, config file reads, service status checks
- For procedures involving destructive operations, verify that preconditions and rollback sections **exist** but do **not** execute the destructive steps
- All verification runs are logged with timestamp, scope, and results for audit trail
- Verification must not generate load that impacts production workloads

## Doc Sync Loop Integration

The doc-verifier operates on the **doc-sync communication loop** (Priority 4) within the GSD communication framework.

**Message flow:**
1. SURGEON detects system change (config update, upgrade, service restart) via the health loop
2. SURGEON sends drift alert to doc-sync loop
3. Doc-verifier receives alert, runs targeted verification against affected procedures
4. Doc-verifier reports drift findings to FLIGHT via doc-sync loop
5. FLIGHT directs EXEC-docs to update affected documentation
6. Updated documentation is re-verified before publication

**Trigger conditions:**
- Scheduled verification (daily/weekly depending on change velocity)
- Post-upgrade verification (after any OpenStack service upgrade)
- Post-configuration change verification (after any `globals.yml` or service config change)
- On-demand verification (operator requests documentation audit)

## Cross-References

- **NASA SE Methodology skill** -- TAID verification methods (SP-6105 SS 5.3) provide the methodological foundation
- **ops-manual-writer skill** -- Defines the procedure format (OPS-*) that doc-verifier validates against
- **runbook-generator skill** -- Defines the runbook format (RB-*) that doc-verifier validates against
- **Filesystem contracts** -- `docs/operations-manual/` and `docs/runbooks/` are the verification targets
- **Communication loop schemas** -- Doc-sync loop (Priority 4) carries verification results
