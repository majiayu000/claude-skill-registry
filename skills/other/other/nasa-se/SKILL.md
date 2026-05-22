---
name: nasa-se-methodology
description: "NASA Systems Engineering methodology mapped to cloud operations. Use when planning, executing, verifying, or documenting OpenStack cloud infrastructure following NASA SP-6105 and NPR 7123.1 processes. Provides phase gate criteria, document templates, and cross-references for all 7 SE lifecycle phases applied to cloud deployment and operations."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-22"
      triggers:
        intents:
          - "nasa se"
          - "systems engineering"
          - "phase gate"
          - "sp-6105"
          - "npr 7123"
          - "cloud methodology"
          - "se engine"
          - "verification method"
          - "conops"
          - "semp"
        contexts:
          - "planning cloud deployment"
          - "writing operations documentation"
          - "verifying cloud infrastructure"
          - "conducting design review"
---

# NASA SE Methodology for Cloud Operations

This skill maps NASA's SE Engine (17 common technical processes from NPR 7123.1) to cloud infrastructure operations. It provides the intellectual framework for the GSD OpenStack Cloud Platform project. Every document, procedure, and verification traces back to this methodology.

The SE Engine defines **how** engineering work is performed. The lifecycle phases define **when**. Together they ensure that cloud infrastructure is built with the same disciplined process NASA applies to spacecraft.

## SE Engine Process Groups

### System Design Processes (1-4)

| # | Process | SP-6105 | Cloud Operations Equivalent |
|---|---------|---------|----------------------------|
| 1 | Stakeholder Expectations Definition | SS 4.1 | Identify cloud consumers (developers, operators, security team, management) and capture service level expectations for uptime, performance, capacity, and security posture |
| 2 | Technical Requirements Definition | SS 4.2 | Transform expectations into "shall" statements for each OpenStack service: functional capabilities, API response times, concurrent users, hardware constraints |
| 3 | Logical Decomposition | SS 4.3 | Map cloud requirements to OpenStack services (compute to Nova, network to Neutron, storage to Cinder) and define service interaction architecture |
| 4 | Design Solution Definition | SS 4.4 | Conduct trade studies (Kolla-Ansible vs DevStack, OVS vs OVN, LVM vs Ceph), select preferred design, produce configuration specifications |

### Product Realization Processes (5-9)

| # | Process | SP-6105 | Cloud Operations Equivalent |
|---|---------|---------|----------------------------|
| 5 | Product Implementation | SS 5.1 | Deploy OpenStack services via Kolla-Ansible, validate container versions, verify configurations against requirements |
| 6 | Product Integration | SS 5.2 | Wire Keystone to Nova to Neutron to Cinder into a functioning cloud following dependency order, validate cross-service interfaces |
| 7 | Product Verification | SS 5.3 | Prove each service conforms to requirements using TAID methods: API tests, log analysis, configuration inspection, operational demonstrations |
| 8 | Product Validation | SS 5.4 | Confirm cloud works for intended users under realistic conditions: real workloads, real users, real network traffic |
| 9 | Product Transition | SS 5.5 | Hand off from deployment crew to operations crew with verified ops manuals, runbooks, monitoring dashboards, and trained operators |

### Technical Management Processes (10-17)

| # | Process | SP-6105 | Cloud Operations Equivalent |
|---|---------|---------|----------------------------|
| 10 | Technical Planning | SS 6.1 | Cloud Engineering Management Plan: how the cloud is built, maintained, and evolved |
| 11 | Requirements Management | SS 6.2 | Track requirements changes, maintain traceability from stakeholder needs through tests |
| 12 | Interface Management | SS 6.3 | Service API contracts, network interfaces, storage interfaces between OpenStack components |
| 13 | Technical Risk Management | SS 6.4 | Identify risks (hardware failure, network partition, security breach) and define mitigation plans |
| 14 | Configuration Management | SS 6.5 | Git-controlled configs, change control process, baseline management for all OpenStack settings |
| 15 | Technical Data Management | SS 6.6 | Documentation standards, archive strategy, access control for operational data |
| 16 | Technical Assessment | SS 6.7 | Life-cycle reviews, progress tracking, cloud health monitoring against baselines |
| 17 | Decision Analysis | SS 6.8 | Formal decision records for every design trade-off with alternatives evaluated and rationale documented |

## Lifecycle Phase Mapping

### Pre-Phase A: Concept Studies -- Cloud Architecture Assessment

- **SP-6105 Reference:** Section 4.1
- **NPR 7123.1 Reference:** Section 4.1
- **Cloud Equivalent:** Assess feasibility of proposed cloud architecture against available hardware, identify stakeholders, define Measures of Effectiveness
- **Key Activities:**
  - Identify all cloud consumers and their service level expectations
  - Conduct hardware inventory and resource assessment
  - Develop Cloud Architecture Overview (ConOps)
  - Classify project risk level (Type C-D per SP-6105 SS 3.11)
  - Define Measures of Effectiveness (instance launch time, API availability, storage IOPS)
- **Deliverables:** Cloud Architecture Overview (ConOps), Stakeholder Register, Feasibility Assessment, Risk Classification
- **Review Gate:** MCR (Mission Concept Review) / Cloud Architecture Review
- **Phase Gate Criteria:**
  1. All stakeholders identified with documented expectations
  2. Hardware inventory complete with resource sufficiency confirmed
  3. ConOps reviewed and approved by stakeholders
  4. Risk classification documented with tailoring rationale

### Phase A: Concept and Technology Development -- Technology Selection and Requirements

- **SP-6105 Reference:** Section 4.2
- **NPR 7123.1 Reference:** Section 4.2
- **Cloud Equivalent:** Select deployment technology (Kolla-Ansible), define system-level requirements, establish architecture baseline
- **Key Activities:**
  - Assess deployment technologies (Kolla-Ansible vs DevStack vs manual)
  - Define functional and performance requirements for each service
  - Establish architecture definition (single-node vs multi-node, HA vs lab)
  - Baseline the Systems Engineering Management Plan (SEMP)
  - Establish requirements traceability
- **Deliverables:** Cloud Requirements Document, SEMP Baseline, Technology Assessment Report, Architecture Definition
- **Review Gate:** SRR (System Requirements Review) / Requirements Baseline Review
- **Phase Gate Criteria:**
  1. All requirements captured as traceable "shall" statements
  2. Deployment technology selected with documented trade study
  3. SEMP baselined and approved
  4. Requirements traceability matrix initialized

### Phase B: Preliminary Design and Technology Completion -- Architecture and Configuration Design

- **SP-6105 Reference:** Sections 4.3-4.4
- **NPR 7123.1 Reference:** Section 4.3
- **Cloud Equivalent:** Design service-by-service specifications, define interfaces, produce preliminary V&V plan
- **Key Activities:**
  - Produce service-by-service design specifications
  - Define interface control documents (Keystone-Nova, Nova-Neutron, Nova-Cinder)
  - Design network topology (management, tenant, external, storage networks)
  - Design storage backend (LVM vs Ceph, local vs distributed)
  - Prepare preliminary V&V plan
- **Deliverables:** Service Design Specifications, Interface Control Documents, Network Design, Storage Design, Preliminary V&V Plan
- **Review Gate:** PDR (Preliminary Design Review) / Configuration Review
- **Phase Gate Criteria:**
  1. All service interfaces defined with API contracts
  2. Network and storage designs documented with rationale
  3. Trade studies completed for all design alternatives
  4. Preliminary V&V plan maps every requirement to a verification method

### Phase C: Final Design and Fabrication -- Deployment Configuration and Build

- **SP-6105 Reference:** Section 5.1
- **NPR 7123.1 Reference:** Section 5.1
- **Cloud Equivalent:** Produce final Kolla-Ansible configurations, generate certificates, configure networks and storage
- **Key Activities:**
  - Finalize Kolla-Ansible configuration (globals.yml, inventory, service configs)
  - Generate and deploy TLS certificates
  - Configure network bridges, VLANs, OVS/OVN
  - Configure storage backend
  - Version-control all configs with decision-documenting commit messages
- **Deliverables:** Final Configuration Package, Certificate Bundle, Network Configuration, Storage Configuration, Build Procedures
- **Review Gate:** CDR (Critical Design Review) / Pre-Deployment Review
- **Phase Gate Criteria:**
  1. All configurations finalized and version-controlled
  2. Certificates generated and validated
  3. Rollback procedures documented for every configuration change
  4. Build procedures reviewed and approved

### Phase D: System Assembly, Integration, and Test -- Service Integration and Verification

- **SP-6105 Reference:** Sections 5.2-5.3
- **NPR 7123.1 Reference:** Section 5.2
- **Cloud Equivalent:** Deploy services in dependency order, verify each service individually, then verify integrated system
- **Key Activities:**
  - Deploy services following integration dependency order (Keystone first, then Glance, Nova, Neutron, Cinder, Horizon, Heat, Swift)
  - Run service-by-service verification (each service passes health checks)
  - Execute integration tests (end-to-end: authenticate, create network, launch instance, attach storage)
  - Establish performance baseline
  - Conduct security audit
- **Deliverables:** Deployed System, Service Verification Reports, Integration Test Results, Performance Baseline, Security Audit Report, V&V Report
- **Review Gate:** SIR (System Integration Review) / Integration Test Review
- **Phase Gate Criteria:**
  1. All services deployed and individually verified
  2. Integration tests pass end-to-end scenarios
  3. Performance baseline established and documented
  4. Security audit complete with no critical findings

### Phase E: Operations and Sustainment -- Cloud Operations and Maintenance

- **SP-6105 Reference:** Sections 5.4-5.5
- **NPR 7123.1 Reference:** Section 5.4
- **Cloud Equivalent:** Transition to operations crew, execute day-2 procedures, monitor health, maintain and upgrade
- **Key Activities:**
  - Hand off from deployment crew to operations crew (Operational Readiness Review)
  - Configure monitoring and alerting (Prometheus/Grafana)
  - Execute day-2 operations procedures
  - Perform backup and recovery validation
  - Plan and execute upgrades (minor and major OpenStack releases)
- **Deliverables:** Verified Operations Manual, Runbook Library, Monitoring Configuration, Backup Procedures, Upgrade Procedures, Operational Health Reports
- **Review Gate:** ORR (Operational Readiness Review) / Operations Handoff Review
- **Phase Gate Criteria:**
  1. Operations crew has documented handoff checklist with all items signed off
  2. All runbooks verified against running system with doc-verifier (zero Critical drift items)
  3. Monitoring dashboards accessible and alerting rules fire on synthetic test conditions
  4. Backup procedure executed and restore verified on at least one service database

### Phase F: Closeout -- Decommission and Lessons Learned

- **SP-6105 Reference:** Section 6.1
- **NPR 7123.1 Reference:** Section 6.1
- **Cloud Equivalent:** Graceful cloud shutdown, data migration, resource recovery, mission retrospective
- **Key Activities:**
  - Execute instance migration procedures
  - Export and archive operational data
  - Decommission services in reverse dependency order
  - Recover hardware resources
  - Compile lessons learned in NASA LLIS format
- **Deliverables:** Decommissioning Report, Data Archive, Lessons Learned Document, Final Mission Report
- **Review Gate:** DR (Decommissioning Review) / Cloud Lifecycle Review
- **Phase Gate Criteria:**
  1. All user data migrated or archived with written confirmation from data owners
  2. All services stopped, containers removed, and no OpenStack processes running (`docker ps` empty of kolla containers)
  3. Hardware resources recovered and inventoried with updated asset register
  4. Lessons learned document published in NASA LLIS format with at least 3 actionable recommendations

## Verification Methods (TAID)

NASA defines four verification methods (SP-6105 SS 5.3). Applied to cloud operations:

| Method | Description | Cloud Operations Application |
|--------|-------------|------------------------------|
| **Test** | Exercise the system and observe results | API functional tests (`openstack token issue`, `openstack server create`), integration tests (end-to-end user scenarios), load tests (concurrent API requests, instance density) |
| **Analysis** | Use models, calculations, or data review | Log analysis (service startup sequences, error patterns), configuration analysis (security parameter review), capacity analysis (resource utilization projections) |
| **Inspection** | Visual or automated examination of artifacts | Configuration file review (globals.yml against requirements), certificate validation (expiry, chain, SAN), RBAC policy audit (policy.json completeness) |
| **Demonstration** | Show operational capability in realistic scenarios | End-to-end operational demo: create project, configure network, launch instance, attach storage, access via floating IP, perform backup, execute failover |

Each requirement in the verification matrix specifies which TAID method(s) apply. Complex requirements may use multiple methods (e.g., Test + Inspection for a security requirement).

## Document Templates

Each NASA document type maps to a cloud operations equivalent:

| NASA Document | Cloud Equivalent | Format |
|---------------|-----------------|--------|
| ConOps (SP-6105 SS 4.1, Appendix S) | Cloud Architecture Overview | Markdown: stakeholder identification, operational scenarios, off-nominal scenarios, user interaction modes |
| SEMP (SP-6105 SS 6.1, Appendix J) | Cloud Engineering Management Plan | Markdown: technical approach, org structure, process tailoring, risk management, config management, reviews |
| Requirements Specification | Cloud Requirements Document | Markdown with traceable requirement IDs: `CLOUD-{DOMAIN}-{NNN}` format, each with verification method |
| Interface Control Document (ICD) | Service Integration Guide | Markdown: API contracts between services, network interfaces, authentication flows, data formats |
| V&V Plan (SP-6105 SS 5.3) | Cloud V&V Plan | Markdown: requirements verification matrix mapping every requirement to TAID method and test procedure |
| Operations Manual | Systems Administrator's Guide | Markdown: 7 chapters mapping SE phases, procedures, cross-references to SP-6105 and NPR 7123.1 |
| Operations Procedures | Runbook Library | Markdown: standard format per entry with preconditions, procedure steps, verification, rollback, references |
| Lessons Learned | Operations Journal | Markdown: NASA LLIS format with mission retrospective, actionable improvements, process recommendations |

### Document Template Structures

Heading outlines for the three critical document types. Executors producing these documents should follow this structure.

**Cloud Architecture Overview (ConOps)** -- SP-6105 SS 4.1, Appendix S
```
1. Introduction
   1.1 Purpose
   1.2 Scope
   1.3 Reference Documents
2. Stakeholder Identification
   2.1 Cloud Consumers (developers, operators, end users)
   2.2 Service Level Expectations
   2.3 Measures of Effectiveness
3. System Overview
   3.1 Architecture Diagram
   3.2 Service Inventory
   3.3 Hardware Baseline
4. Operational Scenarios
   4.1 Normal Operations (instance lifecycle, storage, networking)
   4.2 Peak Load Scenarios
   4.3 Maintenance Windows
5. Off-Nominal Scenarios
   5.1 Compute Node Failure
   5.2 Network Partition
   5.3 Storage Backend Failure
   5.4 Identity Service Outage
6. User Interaction Modes
   6.1 Horizon Dashboard
   6.2 CLI (openstack client)
   6.3 API Direct Access
   6.4 Heat Templates (IaC)
7. Risk Classification
   7.1 Project Type (SP-6105 SS 3.11)
   7.2 Tailoring Rationale
```

**Cloud Requirements Document** -- SP-6105 SS 4.2
```
1. Introduction
   1.1 Purpose and Scope
   1.2 Applicable Documents
   1.3 Requirement ID Convention (CLOUD-{DOMAIN}-{NNN})
2. System-Level Requirements
   2.1 Functional Requirements
   2.2 Performance Requirements
   2.3 Security Requirements
   2.4 Availability Requirements
3. Service-Level Requirements
   3.1 Identity (Keystone)
   3.2 Compute (Nova)
   3.3 Networking (Neutron)
   3.4 Block Storage (Cinder)
   3.5 Image (Glance)
   3.6 Object Storage (Swift)
   3.7 Orchestration (Heat)
   3.8 Dashboard (Horizon)
4. Interface Requirements
   4.1 Service-to-Service APIs
   4.2 Network Interfaces
   4.3 External Integrations
5. Constraints
   5.1 Hardware Constraints
   5.2 Software Constraints
   5.3 Operational Constraints
6. Verification Cross-Reference
   6.1 Requirement-to-TAID Method Mapping
   6.2 Verification Phase Assignment
```

**Cloud V&V Plan** -- SP-6105 SS 5.3
```
1. Introduction
   1.1 Purpose
   1.2 Scope
   1.3 V&V Approach (TAID Methods)
2. Requirements Verification Matrix
   2.1 Matrix Format (Req ID, Description, Method, Phase, Status)
   2.2 Functional Requirements Verification
   2.3 Performance Requirements Verification
   2.4 Security Requirements Verification
3. Test Procedures
   3.1 Service-Level Tests (per service)
   3.2 Integration Tests (cross-service scenarios)
   3.3 Performance Tests (load, capacity)
   3.4 Security Tests (vulnerability, policy)
4. Analysis Procedures
   4.1 Log Analysis Methods
   4.2 Configuration Analysis Methods
   4.3 Capacity Analysis Methods
5. Inspection Procedures
   5.1 Configuration File Review Checklist
   5.2 Certificate Validation Checklist
   5.3 RBAC Policy Audit Checklist
6. Demonstration Scenarios
   6.1 End-to-End User Scenario
   6.2 Operational Readiness Scenario
   6.3 Failure Recovery Scenario
7. Acceptance Criteria
   7.1 Per-Requirement Pass/Fail Criteria
   7.2 System-Level Acceptance Criteria
8. Documentation Verification
   8.1 Doc-Verifier Integration
   8.2 Drift Detection Schedule
```

## Tailoring Guidance

This project classifies as Type C-D per SP-6105 SS 3.11 (lab/development cloud, medium complexity, non-safety-critical). Tailoring decisions follow NPR 7123.1 SS 2.2:

| NASA Requirement | Tailoring Decision | Rationale |
|------------------|-------------------|-----------|
| Formal independent review boards | GSD VERIFY agent + HITL review | Appropriate for lab-scale, non-safety-critical infrastructure |
| Standalone SEMP document | Integrated into Cloud Engineering Management Plan within git repo | SP-6105 SS 3.11.4.2 permits for smaller projects |
| Formal RID/RFA process | GSD issue tracking in .planning/ directory | Same information captured, lighter-weight process |
| Hardware qualification testing | Hardware inventory + compatibility verification | COTS hardware, no custom fabrication |
| Full ConOps with all appendices | Focused ConOps covering primary operational scenarios | Tailored scope per NPR 7123.1 SS 2.2 for medium-complexity projects |
| Formal V&V with independent V&V team | VERIFY agent independent from EXEC agents | Separation maintained; formality scaled to risk level |

All tailoring is documented in the Compliance Matrix (NPR 7123.1 Appendix H format) attached to the Cloud Engineering Management Plan.

## Cross-References

| Document | Identifier | Purpose |
|----------|-----------|---------|
| NASA Systems Engineering Handbook | NASA/SP-2016-6105 Rev2 | Primary SE methodology reference: process definitions, lifecycle phases, document templates |
| SE Processes and Requirements | NPR 7123.1D | SE process requirements, lifecycle review criteria, compliance matrix format |
| Space Flight Program and Project Management | NPR 7120.5 | Program management requirements that complement SE processes |
| MBSE Handbook | NASA-HDBK-1009A | Model-based systems engineering guidance for system architecture and design |
