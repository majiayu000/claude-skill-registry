---
name: ops-manual-writer
description: "Guidance for writing OpenStack operations manual procedures following NASA document standards. Use when authoring per-service procedures, maintenance workflows, or operational documentation that must be verified against running infrastructure."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-22"
      triggers:
        intents:
          - "write procedure"
          - "operations manual"
          - "document procedure"
          - "nasa procedure format"
          - "ops manual"
          - "maintenance procedure"
        contexts:
          - "writing operations documentation"
          - "creating service procedures"
          - "documenting OpenStack operations"
---

# Operations Manual Writer

This skill guides agents producing operations manual content for the GSD OpenStack Cloud Platform. Every procedure must follow NASA document standards adapted for cloud operations per SP-6105 SS 5.5 (Product Transition) and NPR 7123.1 Process 9 (Product Transition). The operations manual is the primary handoff artifact between the deployment crew and the operations crew.

The goal is consistency and verifiability: every procedure an operator follows must be structured so that another agent (doc-verifier) can confirm the procedure matches the running system, and another operator can execute it without ambiguity.

## Procedure Format Template

Every operational procedure follows the standard format derived from NASA-STD-3001 (adapted for cloud operations) as specified in the project reference document (Section 3.4 of gsd-openstack-nasa-reference.md):

```
PROCEDURE ID: OPS-{SERVICE}-{NUMBER}
TITLE: {What this procedure accomplishes}
SE PHASE: Phase E (Operations & Sustainment)
NPR REFERENCE: NPR 7123.1 SS 3.2 Process 9 (Product Transition)
LAST VERIFIED: {YYYY-MM-DD} against {OpenStack release version}
VERIFIED BY: {doc-verifier agent / manual verification}

PURPOSE
  {One to three sentences explaining why an operator would perform this
  procedure and when it should be executed.}

PRECONDITIONS
  1. {System state required before starting}
  2. {Services that must be running}
  3. {Access credentials or permissions needed}
  4. {Backup state confirmed if procedure is destructive}

SAFETY CONSIDERATIONS
  - {What could go wrong during this procedure}
  - {Data loss risks and mitigation}
  - {Service disruption scope and duration}
  - {Dependencies that may be affected}

PROCEDURE
  Step 1: {Exact command or action}
    Expected result: {What the operator should see}
    If unexpected: {What to do -- specific recovery action or escalation}

  Step 2: {Exact command or action}
    Expected result: {What the operator should see}
    If unexpected: {What to do}

  Step N: ...

VERIFICATION
  1. {How to confirm the procedure succeeded}
  2. {Specific command and expected output}
  3. {Service health check to run after completion}

ROLLBACK
  1. {How to undo the procedure if needed}
  2. {Steps in reverse order with commands}
  3. {How to confirm rollback succeeded}

REFERENCES
  - {Related OPS procedures by ID}
  - {Related runbooks by RB-{SERVICE}-{NNN} ID}
  - {OpenStack documentation URL}
  - {SP-6105 or NPR 7123.1 section reference}
```

### Procedure ID Format

- Pattern: `OPS-{SERVICE}-{NUMBER}`
- SERVICE: Uppercase service name (KEYSTONE, NOVA, NEUTRON, CINDER, GLANCE, SWIFT, HEAT, HORIZON, KOLLA, GENERAL)
- NUMBER: 3-digit sequential number per service, starting at 001
- Cross-service procedures use GENERAL prefix
- Example: `OPS-KEYSTONE-001`, `OPS-NOVA-003`, `OPS-GENERAL-002`

## Writing Standards

These rules are mandatory for all procedure authoring. Violations cause verification failures.

### Language Rules

1. **Imperative mood for all procedure steps.** Write "Run", "Verify", "Check" -- never "You should run" or "The operator runs".
2. **Exact commands only.** Every step must include the precise command or action. Never write "configure as needed" or "adjust accordingly".
3. **Expected results for every step.** State what the operator should see after executing the step. Include example output where practical.
4. **If-unexpected branches for failure-prone steps.** Any step that could fail must include a recovery path: retry, escalate, or redirect to a troubleshooting runbook.
5. **No assumptions about operator knowledge.** Spell out paths, service names, and configuration file locations. Do not assume the operator knows where files are stored.

### Safety Rules

6. **Safety considerations before any destructive operation.** If a procedure can cause data loss, service disruption, or configuration damage, the safety section must be populated.
7. **Backup confirmation before destructive steps.** Any procedure that modifies data or configuration must confirm backup state in preconditions.
8. **Rollback section is mandatory.** Every procedure must have a rollback path. If a procedure is truly irreversible, the rollback section must state this explicitly with justification.

### Reference Rules

9. **All external references must include NASA document identifiers.** Cross-references to NASA methodology use SP-6105 SS {section} or NPR 7123.1 SS {section} format.
10. **OpenStack documentation links must be specific.** Link to the exact page, not the top-level docs site. Include the OpenStack release name when relevant.
11. **Related procedures linked by ID.** Use OPS-{SERVICE}-{NUMBER} for operations manual cross-references and RB-{SERVICE}-{NNN} for runbook cross-references.

## Per-Service Procedure Categories

Each OpenStack service in the operations manual requires procedures in these standard categories. This ensures consistent coverage across all services.

### Required Categories

| Category | Frequency | Description |
|----------|-----------|-------------|
| Service Health Check | Daily | Verify service is running, API responds, logs show no errors |
| Configuration Verification | After changes | Confirm configuration matches expected state after any modification |
| Backup and Restore | As scheduled | Create backup of service data/config and verify restore capability |
| Upgrade (Minor) | Per release | Apply minor version updates with pre-check, upgrade, post-verify |
| Upgrade (Major) | Per release cycle | Apply major version updates with extended testing and rollback plan |
| Troubleshooting Common Failures | On demand | Diagnose and resolve the 3-5 most common failure modes per service |
| Security Audit | Monthly | Verify security configuration, certificates, RBAC policies, and access logs |

### Service-Specific Additions

Some services require additional procedure categories beyond the standard set:

- **Keystone:** Token rotation, federation configuration, catalog management
- **Nova:** Live migration, flavor management, hypervisor maintenance
- **Neutron:** Network topology changes, floating IP management, security group audit
- **Cinder:** Volume migration, backend failover, snapshot management
- **Glance:** Image format conversion, metadata management, backend rotation
- **Swift:** Ring rebalancing, replication monitoring, container quota management
- **Heat:** Stack template validation, resource dependency analysis, orphan cleanup
- **Horizon:** Session management, custom panel deployment, theme configuration

## Verification Requirements

Procedures are not complete until they are verified. This section defines how verification works within the documentation lifecycle.

### Verification Process

1. **Every procedure must have a verification section** that proves the procedure succeeded. The verification section contains specific commands with expected output.
2. **Procedures must be testable against a running system.** A procedure that cannot be verified against the actual infrastructure is incomplete.
3. **The doc-verifier skill handles automated verification.** When a procedure is marked for automated verification, doc-verifier extracts the verification commands and runs them against the system.
4. **Last-verified date and system version must be recorded.** The LAST VERIFIED field in the procedure header tracks when the procedure was last confirmed accurate.
5. **Unverified procedures must carry a visible warning.** If a procedure has not been verified against the current system version, add a warning block at the top.

### Unverified Warning Format

```
WARNING: This procedure has not been verified against the current system.
Last verified: {date} against {version}.
Current system: {version}.
Use with caution and verify each step manually.
```

## Output Location

All operations manual procedures are written to `docs/operations-manual/` following the filesystem contracts:

| File | Content |
|------|---------|
| `docs/operations-manual/keystone-procedures.md` | All OPS-KEYSTONE-* procedures |
| `docs/operations-manual/nova-procedures.md` | All OPS-NOVA-* procedures |
| `docs/operations-manual/neutron-procedures.md` | All OPS-NEUTRON-* procedures |
| `docs/operations-manual/cinder-procedures.md` | All OPS-CINDER-* procedures |
| `docs/operations-manual/glance-procedures.md` | All OPS-GLANCE-* procedures |
| `docs/operations-manual/swift-procedures.md` | All OPS-SWIFT-* procedures |
| `docs/operations-manual/heat-procedures.md` | All OPS-HEAT-* procedures |
| `docs/operations-manual/horizon-procedures.md` | All OPS-HORIZON-* procedures |

Each file contains all procedures for that service, ordered by procedure number.

## Cross-References

| Resource | Purpose |
|----------|---------|
| `skills/methodology/nasa-se/SKILL.md` | SE lifecycle phase context -- procedures map to Phase E (Operations & Sustainment) per SP-6105 SS 5.4-5.5 |
| `skills/methodology/doc-verifier/SKILL.md` | Automated verification methods for procedure accuracy against running infrastructure |
| `skills/methodology/runbook-generator/SKILL.md` | Runbook format alignment -- procedures reference runbooks for troubleshooting branches |
| `docs/filesystem-contracts.md` | Output location contracts for `docs/operations-manual/` directory |
| NASA SP-6105 SS 5.5 | Product Transition process -- operations documentation as transition artifact |
| NPR 7123.1 SS 3.2 Process 9 | Product Transition requirements -- procedures satisfy handoff documentation |
| NASA-STD-3001 (adapted) | Procedure format origin -- adapted from crew procedures standard for cloud operations |
