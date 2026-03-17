---
name: togaf
description: |
    Use when applying The Open Group Architecture Framework (TOGAF) for enterprise architecture development. Covers the Architecture Development Method (ADM), Architecture Repository, Enterprise Continuum, content metamodel, and key deliverables per phase.
    USE FOR: enterprise architecture development lifecycle, ADM phase guidance, architecture governance, architecture repository structure, enterprise continuum classification, TOGAF deliverables and artifacts, architecture capability planning
    DO NOT USE FOR: detailed element-level modeling notation (use archimate), system-level container diagrams (use c4-diagrams), general-purpose diagramming (use mermaidjs or d2)
license: MIT
metadata:
  displayName: "TOGAF"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "TOGAF — The Open Group"
    url: "https://www.opengroup.org/togaf"
  - title: "TOGAF Standard — Digital Edition"
    url: "https://pubs.opengroup.org/togaf-standard/"
---

# TOGAF - The Open Group Architecture Framework

## Overview
TOGAF is an enterprise architecture framework that provides a structured approach for designing, planning, implementing, and governing enterprise information technology architecture. It is maintained by The Open Group and is the most widely adopted enterprise architecture framework globally.

TOGAF's core is the **Architecture Development Method (ADM)** — an iterative cycle of phases that transforms business requirements into architecture deliverables.

## Architecture Development Method (ADM)

The ADM is an iterative, cyclic process of continuous architecture development. Each phase produces defined deliverables, is validated against requirements, and feeds into the next phase.

```
                    ┌──────────────┐
                    │  Preliminary │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Architecture│
                    │  Vision (A)  │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼───────┐   │   ┌────────▼─────┐
       │  Business     │   │   │ Technology   │
       │  Arch (B)     │   │   │ Arch (D)     │
       └──────┬───────┘   │   └────────┬─────┘
              │     ┌──────▼───────┐   │
              │     │  Info Systems │   │
              │     │  Arch (C)    │   │
              │     └──────┬───────┘   │
              └────────────┼───────────┘
                           │
                    ┌──────▼───────┐
                    │ Opportunities│
                    │ & Solutions  │
                    │    (E)       │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Migration   │
                    │  Planning(F) │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Implementation│
                    │ Governance(G)│
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Architecture│
                    │  Change Mgmt │
                    │    (H)       │
                    └──────────────┘

      Requirements Management (center, continuous)
```

### Preliminary Phase
**Purpose:** Establish the architecture capability and tailor TOGAF for the organization.

| Activity | Output |
|----------|--------|
| Define architecture organization | Architecture team structure |
| Identify stakeholders and concerns | Stakeholder map |
| Establish architecture principles | Principles catalog |
| Tailor the ADM | Customized ADM process |
| Select architecture tools | Tooling strategy |

**Key Deliverables:**
- Organizational Model for Enterprise Architecture
- Tailored Architecture Framework
- Architecture Principles catalog
- Architecture Repository (initial structure)

### Phase A: Architecture Vision
**Purpose:** Set the scope, constraints, and expectations for the architecture engagement. Secure stakeholder buy-in.

| Activity | Output |
|----------|--------|
| Establish architecture project | Request for Architecture Work |
| Identify stakeholders and concerns | Stakeholder Map matrix |
| Confirm architecture principles | Refined Principles catalog |
| Develop Architecture Vision | Architecture Vision document |
| Obtain approval | Statement of Architecture Work |

**Key Deliverables:**
- Architecture Vision document
- Statement of Architecture Work
- Refined stakeholder map
- High-level baseline and target descriptions
- Gap analysis (high-level)

### Phase B: Business Architecture
**Purpose:** Develop the Target Business Architecture that supports the Architecture Vision.

| Activity | Output |
|----------|--------|
| Develop Baseline Business Architecture | Baseline description |
| Develop Target Business Architecture | Target description |
| Perform gap analysis | Gap analysis report |
| Define roadmap components | Business Architecture roadmap |

**Key Deliverables:**
- Business Architecture document (Baseline and Target)
- Gap analysis results
- Business Architecture components of the Architecture Roadmap

**Catalogs, Matrices, and Diagrams:**
- Organization/Actor catalog
- Business Service/Function catalog
- Business Interaction matrix
- Business Footprint diagram
- Business Service/Information diagram

### Phase C: Information Systems Architecture
**Purpose:** Develop Target Data Architecture and Target Application Architecture.

This phase has two sub-phases that can be done in either order or in parallel:

**Data Architecture:**
- Data Entity/Data Component catalog
- Data Entity/Business Function matrix
- Conceptual/Logical Data diagrams
- Data Dissemination diagram
- Data Lifecycle diagram

**Application Architecture:**
- Application Portfolio catalog
- Interface catalog
- Application/Organization matrix
- Application Communication diagram
- Application and User Location diagram

**Key Deliverables:**
- Data Architecture document (Baseline and Target)
- Application Architecture document (Baseline and Target)
- Gap analysis for data and application domains

### Phase D: Technology Architecture
**Purpose:** Develop the Target Technology Architecture that enables the data and application components.

| Activity | Output |
|----------|--------|
| Develop Baseline Technology Architecture | Current technology landscape |
| Develop Target Technology Architecture | Target technology landscape |
| Perform gap analysis | Technology gaps identified |
| Define candidate roadmap components | Technology roadmap elements |

**Key Deliverables:**
- Technology Architecture document (Baseline and Target)
- Technology Standards catalog
- Technology Portfolio catalog
- Gap analysis results
- Environments and Locations diagram
- Platform Decomposition diagram
- Network Computing/Hardware diagram

### Phase E: Opportunities and Solutions
**Purpose:** Generate the initial Architecture Roadmap based on gap analysis from Phases B, C, and D. Identify major work packages and transition architectures.

**Key Deliverables:**
- Architecture Roadmap (initial, consolidated)
- Transition Architectures (intermediate states between baseline and target)
- Implementation and Migration Strategy
- Work package descriptions

### Phase F: Migration Planning
**Purpose:** Finalize the Architecture Roadmap and the Implementation and Migration Plan. Prioritize projects and create detailed migration plans.

**Key Deliverables:**
- Implementation and Migration Plan (finalized)
- Architecture Roadmap (finalized)
- Transition Architecture descriptions (detailed)
- Architecture implementation governance model

### Phase G: Implementation Governance
**Purpose:** Provide architecture oversight for the implementation. Ensure conformance of projects to the Target Architecture.

| Activity | Output |
|----------|--------|
| Confirm scope and priorities | Implementation governance plan |
| Identify deployment resources | Resource plan |
| Guide implementation | Architecture Contract compliance |
| Perform architecture compliance reviews | Compliance assessment |

**Key Deliverables:**
- Architecture Contract
- Compliance assessments
- Change requests (for architecture updates)
- Architecture-compliant implemented solutions

### Phase H: Architecture Change Management
**Purpose:** Establish procedures for managing change to the architecture. Monitor ongoing enterprise changes and determine whether to initiate a new ADM cycle.

**Key Deliverables:**
- Architecture updates and changes
- New Request for Architecture Work (when significant change detected)
- Change management process documentation
- Updated Architecture Requirements Specification

### Requirements Management (Continuous)
**Purpose:** Operate continuously throughout the ADM cycle to manage architecture requirements as they are identified, stored, and fed into relevant phases.

**Key Activities:**
- Identify and document requirements
- Baseline requirements
- Monitor and manage requirements changes
- Assess impact of changed requirements on current and previous ADM phases
- Ensure requirements traceability

## Architecture Repository

The Architecture Repository stores all architecture outputs and serves as a holding area for architecture deliverables at various levels of abstraction.

```
┌─────────────────────────────────────────────────┐
│              Architecture Repository             │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌───────────────┐   ┌────────────────────────┐ │
│  │ Architecture   │   │ Standards Information  │ │
│  │ Metamodel      │   │ Base                   │ │
│  └───────────────┘   └────────────────────────┘ │
│                                                  │
│  ┌───────────────┐   ┌────────────────────────┐ │
│  │ Architecture   │   │ Reference Library      │ │
│  │ Capability     │   │                        │ │
│  └───────────────┘   └────────────────────────┘ │
│                                                  │
│  ┌───────────────┐   ┌────────────────────────┐ │
│  │ Architecture   │   │ Governance Log         │ │
│  │ Landscape      │   │                        │ │
│  └───────────────┘   └────────────────────────┘ │
│                                                  │
└─────────────────────────────────────────────────┘
```

| Component | Contents |
|-----------|----------|
| **Architecture Metamodel** | Definitions of architecture content types and their relationships |
| **Architecture Capability** | Parameters, structures, and processes for the architecture practice |
| **Architecture Landscape** | Baseline, target, and transition architectures at Strategic, Segment, and Capability levels |
| **Standards Information Base** | Standards that the architecture must comply with (regulatory, industry, organizational) |
| **Reference Library** | Reference architectures, patterns, templates, and guidelines |
| **Governance Log** | Decision records, compliance assessments, capability assessments, change requests |

## Enterprise Continuum

The Enterprise Continuum classifies architecture and solution assets along a spectrum from generic to organization-specific.

```
Generic ◄──────────────────────────────────────► Specific

┌──────────────┬──────────────┬──────────────┬──────────────┐
│  Foundation   │  Common      │  Industry    │ Organization │
│  Architecture │  Systems     │  Architecture│ -Specific    │
│               │  Architecture│              │ Architecture │
├──────────────┼──────────────┼──────────────┼──────────────┤
│  Foundation   │  Common      │  Industry    │ Organization │
│  Solutions    │  Systems     │  Solutions   │ -Specific    │
│               │  Solutions   │              │ Solutions    │
└──────────────┴──────────────┴──────────────┴──────────────┘
  Architecture Continuum (top row)
  Solutions Continuum (bottom row)
```

- **Architecture Continuum:** Ranges from Foundation Architectures (e.g., TOGAF TRM) through Common Systems Architectures (e.g., III-RM) to Industry and Organization-Specific Architectures.
- **Solutions Continuum:** Ranges from Foundation Solutions (e.g., platforms, operating systems) through to Organization-Specific Solutions (e.g., custom applications).

## TOGAF Content Metamodel

The Content Metamodel defines a formal structure for architectural artifacts. It specifies the types of entities that make up an architecture and how they relate.

### Core Content Metamodel Entities

| Entity | Domain | Description |
|--------|--------|-------------|
| **Actor** | Business | A person, organization, or system that performs behavior |
| **Role** | Business | Responsibility or part played by an actor |
| **Business Service** | Business | Supports business capabilities, exposed via interfaces |
| **Business Process** | Business | Ordered set of activities producing a defined outcome |
| **Data Entity** | Data | An encapsulation of data recognized by a business domain expert |
| **Logical Data Component** | Data | A boundary grouping of related data entities |
| **Application Component** | Application | An encapsulation of application functionality |
| **Logical Application Component** | Application | A conceptual grouping of application functionality |
| **Technology Component** | Technology | A technology building block (hardware, infrastructure, middleware) |
| **Platform Service** | Technology | A technical capability required to support application components |

### Key Metamodel Relationships

```
Actor ──performs──► Role
Role ──participates-in──► Business Process
Business Process ──produces──► Business Service
Business Service ──is-realized-by──► Logical Application Component
Logical Application Component ──is-implemented-by──► Application Component
Application Component ──is-hosted-on──► Technology Component
Data Entity ──is-accessed-by──► Logical Application Component
```

### Extensions to the Core Metamodel
TOGAF defines optional extensions:
- **Governance Extensions:** Architecture Contract, Standard, Principle
- **Services Extensions:** Information System Service, Platform Service
- **Process/Event Extensions:** Event, Control, Product
- **Data Extensions:** Physical Data Component, Data Entity relationships
- **Infrastructure Consolidation Extensions:** Physical Technology Component, Location

## Key Deliverables Summary

| Phase | Primary Deliverables |
|-------|---------------------|
| Preliminary | Tailored Architecture Framework, Principles |
| A - Vision | Architecture Vision, Statement of Architecture Work |
| B - Business | Business Architecture document, Gap analysis |
| C - Info Systems | Data Architecture, Application Architecture, Gap analysis |
| D - Technology | Technology Architecture, Standards catalog, Gap analysis |
| E - Opportunities | Architecture Roadmap, Transition Architectures |
| F - Migration | Implementation and Migration Plan |
| G - Governance | Architecture Contract, Compliance assessments |
| H - Change Mgmt | Change requests, Updated requirements |
| Requirements Mgmt | Architecture Requirements Specification (continuous) |

## Best Practices
- **Iterate, don't waterfall.** The ADM is explicitly iterative. Complete a lightweight pass through all phases before deep-diving into any single phase.
- **Tailor the ADM.** TOGAF is a framework, not a methodology. Adapt the depth and formality of each phase to your organization's maturity and project scope.
- **Maintain the Architecture Repository.** Treat architecture outputs as living assets. Keep the repository current with baseline and target descriptions.
- **Use the Enterprise Continuum.** Classify reusable architecture assets along the continuum so teams can find and leverage existing patterns before inventing new ones.
- **Align with ArchiMate for notation.** TOGAF defines what to produce; ArchiMate defines how to model it visually. Use ArchiMate as the modeling language for TOGAF deliverables.
- **Engage stakeholders early.** Phase A exists specifically to secure buy-in. Do not skip stakeholder identification and concern mapping.
- **Define Architecture Principles before modeling.** Principles in the Preliminary Phase guide all subsequent architecture decisions and serve as tie-breakers.
- **Trace requirements continuously.** Requirements Management is not a phase you pass through once — it runs throughout every ADM cycle.
- **Use gap analysis rigorously.** In Phases B, C, and D, the gap between baseline and target drives the roadmap in Phase E. Incomplete gap analysis leads to incomplete migration plans.
- **Govern the implementation.** Phase G ensures that the actual implementation conforms to the architecture. Without governance, architectures become shelfware.
