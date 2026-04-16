---
name: systems-engineering
description: Systems engineering covering requirements management, the V-model lifecycle, integration planning, verification and validation (V&V), interface control, trade studies, and the NASA Systems Engineering Handbook. Spans the full lifecycle from concept through operations and disposal. Includes requirements decomposition, traceability matrices, configuration management, and technical performance measures. Use when managing complex system development, writing requirements, planning integration, or conducting V&V activities.
type: skill
category: engineering
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/engineering/systems-engineering/SKILL.md
superseded_by: null
---
# Systems Engineering

Systems engineering is the interdisciplinary approach to designing, integrating, and managing complex engineered systems over their life cycles. When an engineering problem grows beyond a single component -- when multiple subsystems must work together, when requirements span disciplines, when interfaces between parts are as critical as the parts themselves -- systems engineering provides the framework for managing that complexity. This skill covers the V-model, requirements management, integration, verification, validation, and the NASA SE Handbook approach.

**Agent affinity:** johnson-k (aerospace systems, trajectory and mission analysis), brunel (integrated design oversight)

**Concept IDs:** engr-design-cycle, engr-control-systems, engr-testing-methodology, engr-codes-of-ethics

## The Systems Engineering Landscape

| # | Topic | Key question |
|---|---|---|
| 1 | The V-model | What is the lifecycle structure? |
| 2 | Requirements management | What must the system do? |
| 3 | Architecture and decomposition | How is the system organized? |
| 4 | Interface control | How do subsystems connect? |
| 5 | Integration | How are pieces assembled? |
| 6 | Verification | Does the system meet its specs? |
| 7 | Validation | Does the system meet the user's need? |
| 8 | Configuration management | How is change controlled? |
| 9 | Technical performance measures | Is the design on track? |

## Topic 1 -- The V-Model

The V-model is the canonical systems engineering lifecycle. The left side decomposes (top-down): system requirements flow down to subsystem requirements to component requirements. The bottom is implementation (build/code/fabricate). The right side integrates and verifies (bottom-up): components are tested, then integrated and tested at subsystem level, then at system level.

```
Stakeholder Needs ←——————————————————————→ Validation
    ↓                                           ↑
System Requirements ←————————————————→ System Verification
    ↓                                       ↑
Subsystem Requirements ←——————→ Subsystem Verification
    ↓                               ↑
Component Requirements ←→ Component Verification
    ↓                       ↑
    └→ Implementation →→→→→→┘
```

The horizontal arrows represent traceability: each level on the right verifies the requirements written at the corresponding level on the left. This is the defining feature of the V-model -- every requirement has a corresponding verification activity, planned at the same time the requirement is written.

**Why the V-model.** It forces early planning of verification. Writing a requirement without planning how to verify it is writing a wish, not a requirement. The V-model makes this impossible by pairing the two sides of the V.

## Topic 2 -- Requirements Management

Requirements management is the continuous process of eliciting, documenting, analyzing, tracing, prioritizing, and controlling requirements throughout the system lifecycle.

### Requirements Hierarchy

| Level | Scope | Owner | Example |
|---|---|---|---|
| Stakeholder requirements | What the user needs | Customer/sponsor | "The spacecraft shall reach lunar orbit" |
| System requirements | What the system must do | Systems engineer | "The propulsion system shall deliver 3,200 m/s delta-v" |
| Subsystem requirements | What each subsystem must do | Subsystem lead | "The main engine shall produce 100 kN thrust at Isp 450s" |
| Component requirements | What each component must do | Component engineer | "The turbopump shall deliver 50 kg/s at 20 MPa" |

### Good Requirements

A well-written requirement is:

- **Necessary:** It traces to a stakeholder need. If no stakeholder needs it, delete it.
- **Verifiable:** A test, analysis, inspection, or demonstration can confirm it.
- **Unambiguous:** One reader, one interpretation. "Adequate" is ambiguous. "Greater than 100 kN" is not.
- **Complete:** No TBDs at CDR. Placeholder requirements are acceptable in early phases but must be resolved before design commitment.
- **Consistent:** No two requirements contradict each other.
- **Achievable:** The requirement is technically and economically feasible.
- **Traceable:** Upward to the need, downward to the design, and laterally to the verification method.

### Requirements Traceability Matrix (RTM)

| Req ID | Requirement | Source | Allocated to | Verification method | Status |
|---|---|---|---|---|---|
| SYS-001 | System shall deliver 3,200 m/s delta-v | Mission requirements doc | Propulsion subsystem | Analysis + test | Verified |
| SUB-P-001 | Main engine thrust >= 100 kN | SYS-001 | Engine assembly | Test | Verified |
| SUB-P-002 | Engine Isp >= 450 s | SYS-001 | Engine assembly | Test | Open |

The RTM is the backbone of systems engineering. It ensures no requirement is orphaned (unallocated), no verification is missing, and every stakeholder need is addressed.

## Topic 3 -- Architecture and Decomposition

System architecture defines how the system is partitioned into subsystems and how those subsystems interact. Decomposition follows the function-to-form mapping: identify what functions the system must perform, then allocate those functions to physical subsystems.

### Functional Decomposition

Break the system's mission into functions, sub-functions, and so on until each function can be assigned to a single subsystem or component.

### Physical Architecture

Map functions to physical elements. Multiple functions may map to one physical element (integration). One function may map to multiple elements (distribution). The mapping is documented in the N-squared diagram or architecture block diagram.

### Architecture Trade Study

Evaluate alternative architectures using the same trade study methods as the design process skill (Pugh matrix, weighted scoring). Architecture decisions are among the most consequential in a program because they are difficult and expensive to change later.

## Topic 4 -- Interface Control

Interfaces between subsystems are where most integration problems occur. Interface control documents (ICDs) define the physical, functional, and data interfaces between subsystems.

### Interface Types

| Type | What it defines | Example |
|---|---|---|
| Physical | Geometry, mounting, connectors | Bolt pattern, connector pinout |
| Functional | Signals, power, data | Voltage levels, data rates, protocols |
| Thermal | Heat transfer across boundaries | Maximum heat flux at interface |
| Structural | Loads transmitted across boundaries | Maximum force and moment at mounting plane |

**The interface rule.** If two teams do not agree on the interface definition in writing before they start building, they will discover the disagreement during integration -- the most expensive possible time.

## Topic 5 -- Integration

Integration is the process of assembling subsystems into the complete system. It proceeds bottom-up (the right side of the V): components into subsystems, subsystems into the system.

### Integration Strategy

| Strategy | Description | Risk |
|---|---|---|
| Big bang | Integrate everything at once | High -- failures are hard to isolate |
| Incremental | Add one subsystem at a time, test after each addition | Lower -- failures can be attributed to the latest addition |
| Thread-based | Integrate along functional threads (e.g., a single end-to-end signal path) | Moderate -- verifies cross-cutting functionality early |

Incremental integration is preferred for most systems because it localizes problems. Big bang integration is only justified when schedule pressure is extreme and risk is accepted.

## Topic 6 -- Verification

Verification answers: "Did we build the system right?" It confirms that the system meets its specified requirements.

### Verification Methods (TIAD)

| Method | How it works | When used |
|---|---|---|
| **T**est | Operate the system and measure performance | When physical measurement is required |
| **I**nspection | Visual or dimensional examination | For physical characteristics (dimensions, workmanship) |
| **A**nalysis | Mathematical or simulation-based evaluation | When testing is impractical (orbital mechanics, thermal) |
| **D**emonstration | Operate the system to show a capability without quantitative measurement | For qualitative requirements ("the system shall be operable by a single operator") |

Each requirement in the RTM must be assigned at least one verification method. The choice depends on cost, fidelity, and feasibility.

## Topic 7 -- Validation

Validation answers: "Did we build the right system?" It confirms that the system meets the stakeholder's actual need -- not just the written requirements, but the underlying intent.

**The distinction matters.** A system can pass every verification test and still fail validation if the requirements were wrong. Verification checks requirements; validation checks intent.

**Worked example.** Katherine Johnson's trajectory calculations for Mercury and Apollo missions were verified by comparing hand calculations to computer output (verification: do the calculations match?). But the real validation was: does the capsule reach orbit, and does it come home safely? The calculations were verified; the mission validated them.

### Validation Methods

- **Operational testing:** Use the system in its intended environment with real users.
- **Mission simulation:** End-to-end simulation of the operational scenario.
- **User acceptance testing:** Stakeholders confirm the system meets their needs.
- **Pilot deployment:** Limited deployment to a subset of users before full rollout.

## Topic 8 -- Configuration Management

Configuration management (CM) controls changes to the system baseline -- the approved set of requirements, designs, and documents at each lifecycle phase.

### CM Activities

| Activity | Purpose |
|---|---|
| Configuration identification | Define and label the baseline items |
| Configuration control | Evaluate, approve/reject, and implement changes |
| Configuration status accounting | Record and report the status of all changes |
| Configuration audit | Verify that the as-built system matches the approved baseline |

**Change control boards (CCBs)** review proposed changes and assess their impact on requirements, schedule, cost, and risk before approving or rejecting them. Uncontrolled changes -- like the Hyatt Regency connection detail change -- are a primary cause of engineering failures.

## Topic 9 -- Technical Performance Measures (TPMs)

TPMs track how well the design is meeting its most critical requirements throughout development. They provide early warning when a design is drifting off-target.

**Example TPMs for a spacecraft:**

| TPM | Threshold | Current estimate | Status |
|---|---|---|---|
| Total mass | 2,500 kg max | 2,380 kg | Green |
| Power budget | 3,000 W max | 2,850 W | Green |
| Delta-v | 3,200 m/s min | 3,150 m/s | Yellow |
| Data rate | 1 Mbps min | 1.2 Mbps | Green |

A yellow or red TPM triggers a trade study or design change before the problem becomes a showstopper at integration.

## The NASA Systems Engineering Handbook

NASA SP-2016-6105 Rev 2 is the gold standard reference for systems engineering practice. Its key contributions:

- **17 SE processes** organized into system design, product realization, and technical management
- **Life cycle phases** (Pre-A through F) with reviews at each transition
- **Technical authority** model separating engineering judgment from program management pressure
- **Lessons learned** from decades of spaceflight programs

The handbook is freely available and applicable far beyond aerospace. Any complex system development benefits from its structured approach.

## Cross-References

- **johnson-k agent:** Primary agent for systems engineering, especially aerospace applications and computational verification.
- **brunel agent:** Integrated design oversight that spans the full V-model.
- **tesla agent:** Electrical and systems-level thinking, especially for feedback and control systems.
- **design-process skill:** The design cycle is the inner loop; systems engineering is the outer framework.
- **engineering-ethics skill:** Professional responsibility in systems decisions, especially change control and safety.
- **technical-communication skill:** Documentation standards for requirements, ICDs, and verification reports.

## References

- NASA. (2020). *NASA Systems Engineering Handbook*. SP-2016-6105 Rev 2. National Aeronautics and Space Administration.
- INCOSE. (2023). *Systems Engineering Handbook*. 5th edition. Wiley.
- Blanchard, B. S., & Fabrycky, W. J. (2011). *Systems Engineering and Analysis*. 5th edition. Prentice Hall.
- Kossiakoff, A., Sweet, W. N., Seymour, S. J., & Biemer, S. M. (2011). *Systems Engineering Principles and Practice*. 2nd edition. Wiley.
- Crawley, E. F., Cameron, B., & Selva, D. (2016). *System Architecture: Strategy and Product Development for Complex Systems*. Pearson.
