---
name: fsd-writer
description: >
  Generates or updates a Functional Specification Document (FSD) from a rough
  project description. Supports initial generation and incremental evolution of
  existing FSDs. Domain-agnostic — works for embedded, IoT, backend, mobile, SDR,
  energy systems, and hybrid hardware/software projects.
  Triggers on "FSD", "write FSD", "new FSD", "update FSD", "evolve FSD",
  "functional spec", "specification document".
---

# FSD Writer Skill

A general-purpose skill that turns a rough, unstructured project description into
a structured Functional Specification Document (FSD) in Markdown, or surgically
updates an existing FSD with new requirements, corrections, or expansions.

## 1. Purpose

This skill:

- Generates a canonical FSD from a rough description (**initial mode**).
- Updates or expands an existing FSD using a delta description (**evolve mode**).
- Dynamically adjusts depth and verbosity based on inferred system complexity.
- Ensures full requirement traceability (FR / NFR <-> test coverage).
- Surfaces risks, assumptions, and constraints as first-class content.
- Produces deterministic, agent-consumable Markdown.

It supports embedded systems, networking, SDR, IoT, cloud backends, mobile apps,
multi-service orchestrations, and hybrid hardware/software projects.

## 2. Invocation

### 2.1 Mode A — Initial Generation

Start a new FSD from scratch.

```
/fsd-writer
<rough description text>
```

Behavior:
1. Parse the rough description.
2. Ask clarifying questions if critical information is missing (Section 5).
3. Infer complexity tier (Section 6).
4. Generate the complete FSD (Section 7).
5. Write the file (Section 10).

### 2.2 Mode B — Evolve Existing FSD

Update, expand, refactor, or correct an already existing FSD.

```
/fsd-writer update <path-to-existing-fsd>
<delta description — changes, additions, clarifications, new constraints>
```

If no path is given, search the project for an existing FSD:
1. Check `Documents/*-fsd.md`
2. Check `Documents/*-FSD.md`
3. Check `docs/*-fsd.md`
4. Check project root for `*-fsd.md`

Behavior:
1. Read the existing FSD in full using the **Read** tool.
2. Parse the delta description.
3. Ask clarifying questions only if the delta introduces architectural ambiguity.
4. Apply changes surgically — preserve all unaffected sections verbatim.
5. Regenerate only the sections affected by the delta.
6. Maintain numbering, cross-references, and the traceability matrix automatically.
7. Write the updated file using the **Edit** tool (preferred) or **Write** tool
   (if changes are too extensive for surgical edits).

## 3. Tool Usage

This skill uses the following Claude Code tools:

| Tool | When |
|------|------|
| **Read** | Read existing FSD (evolve mode), read project files for context |
| **Glob** | Find existing FSD files, scan project structure for architecture clues |
| **Grep** | Search for protocols, frameworks, dependencies in project source |
| **Write** | Create new FSD file (initial mode) or full rewrite |
| **Edit** | Surgical updates to existing FSD sections (evolve mode) |
| **AskUserQuestion** | Clarifying questions when critical info is missing |
| **Task** (Explore) | Deep codebase exploration when the project has existing source code |

### 3.1 Context Gathering (Before Generation)

Before writing the FSD, the skill should gather context from the project when
source code exists:

1. **Glob** for project structure — `**/*.c`, `**/*.h`, `**/*.py`, `**/*.ts`,
   `**/Cargo.toml`, `**/package.json`, `**/CMakeLists.txt`, `**/go.mod`, etc.
2. **Grep** for protocols and frameworks — BLE, WiFi, MQTT, HTTP, gRPC, REST,
   WebSocket, LoRa, OCPP, etc.
3. **Read** key config files — `sdkconfig.defaults`, `platformio.ini`,
   `docker-compose.yml`, `Makefile`, build configs.
4. Use findings to pre-fill architecture sections and reduce clarifying questions.

### 3.2 Evolve Mode — Diff Discipline

When updating an existing FSD:

- **Never regenerate the entire file.** Only touch sections affected by the delta.
- Use the **Edit** tool with precise `old_string` / `new_string` pairs.
- If a delta adds a new phase, insert it and renumber subsequent phases.
- If a delta adds new FRs, assign the next available FR number in the correct group.
- Always update the traceability matrix when FRs or tests change.
- If the delta invalidates existing content, remove or revise it — do not leave
  contradictions.

## 4. Interaction Model (Clarifying Questions)

### 4.1 When to Ask

The skill must ask clarifying questions when critical architecture-affecting
information is missing. "Critical" means it affects:

- System architecture or component decomposition
- Protocol selection (BLE vs WiFi vs LoRa vs cellular)
- Interface definitions (API style, command format)
- Safety or regulatory constraints
- Multi-phase decomposition
- Hardware or platform selection
- External integrations (MQTT broker, cloud service, Home Assistant, etc.)

### 4.2 How to Ask

Use the **AskUserQuestion** tool with:
- 1-3 precise questions per round (never a wall of questions)
- Multiple-choice options where possible (with sensible defaults)
- Questions phrased to unblock the FSD, not to explore nice-to-haves

Example:

```
Questions:
1. "How does the device connect?" → Options: WiFi, BLE, LoRa, Cellular, USB only
2. "Do you need OTA firmware updates?" → Options: Yes (WiFi), Yes (BLE DFU), No
3. "Who is the primary operator?" → Options: End user, Installer/technician, Automated backend
```

### 4.3 When to Infer Instead of Asking

The skill may silently infer reasonable defaults when:
- The detail does not significantly change high-level architecture, AND
- The cost of being wrong is low.

Safe inferences:
- "web API" mentioned → assume HTTP + JSON
- "logs" mentioned → assume structured logging to console / file / serial
- "dashboard" mentioned → describe generic "dashboard system" without naming tools
- "database" mentioned without type → assume PostgreSQL for relational, SQLite for embedded

When inferring, mark the inference in the FSD with `(assumed)` or group them in
**Section 5: Risks, Assumptions & Dependencies**.

## 5. Complexity Scaling Rules

The skill dynamically scales the FSD depth based on inferred system complexity.

### 5.1 Complexity Tiers

| Tier | Characteristics | Target Length | Phases |
|------|----------------|---------------|--------|
| **Low** | Single MCU/service, simple data flows, 1-2 interfaces | 3-5 pages | 1-2 |
| **Medium** | MCU + app, or multi-service, OTA, 2-4 protocols | 6-12 pages | 2-3 |
| **High** | Distributed system, multi-protocol, real-time constraints, regulatory | 15-25+ pages | 3-5 |

### 5.2 Complexity Signals

Infer complexity from:
- Number of distinct components (devices, services, apps)
- Number of protocols (BLE, WiFi, MQTT, HTTP, LoRa, OCPP, Modbus, etc.)
- Number of external integrations (cloud, Home Assistant, third-party APIs)
- Presence of real-time constraints or safety requirements
- Domain (SDR, energy systems, medical → automatically higher complexity)
- Multi-user or multi-tenant requirements

### 5.3 Scaling Behavior

| FSD Section | Low | Medium | High |
|------------|-----|--------|------|
| System Overview | Brief paragraph | Full section | Full + stakeholder analysis |
| Architecture | Single diagram description | Logical + platform + software | All subsections, detailed |
| Phases | 1-2 phases, brief | 2-3 phases, full exit criteria | 3-5 phases, dependencies mapped |
| Requirements | 5-15 FRs, 3-5 NFRs | 15-30 FRs, 5-10 NFRs | 30+ FRs, 10+ NFRs, constraints |
| Risks & Assumptions | Bullet list | Table with mitigations | Full risk register |
| Interfaces | Inline descriptions | Tables per protocol | Full schemas, sequence descriptions |
| Operational Procedures | Bullet steps | Numbered procedures | Detailed with recovery paths |
| V&V | Checklist | Phase-based test tables | Full traceability matrix + acceptance |
| Troubleshooting | 3-5 common issues | Symptom-cause-fix table | Categorized diagnostic guide |
| Appendix | Constants only | Constants + examples | Constants + schemas + diagrams + logs |

## 6. Information Extraction & Inference Rules

Given the rough description, the skill must extract or infer the following:

### 6.1 Project Name

Derive a short, descriptive name:
- "ESP32 BLE HID Keyboard"
- "Solar-Aware EV Charging Controller"
- "LoRa Mailbox Notifier"

### 6.2 System Purpose & Goals

Extract in 2-4 sentences: what problem is solved, for whom, in what environment.

### 6.3 System Components

Identify major components:
- Hardware / platforms (MCU, SBC, server, cloud)
- Software services / apps / daemons
- User-facing components (mobile app, web UI, CLI)
- External integrations (Home Assistant, OCPP backend, MQTT broker)

If components are implied but not explicit, infer and mark as assumptions.

### 6.4 Functional Requirements (FR)

Convert each described behavior into FR-x.y items:
- Group logically (Communication, Data Processing, User Interaction, Safety)
- Assign priority: **Must** / **Should** / **May**
- Use "shall" language: "The system shall..."

Example:
> "Device sends sensor readings every minute and on threshold events."

Becomes:
- **FR-1.1** [Must]: The device shall send periodic sensor measurements at a
  configurable interval (default: 60 s).
- **FR-1.2** [Must]: The device shall send an immediate measurement when a
  threshold condition is met.

### 6.5 Non-Functional Requirements (NFR)

Extract or infer key NFRs with priorities:
- Performance (latency, throughput)
- Reliability / uptime
- Accuracy / precision
- Scalability
- Power consumption (embedded)
- Security and privacy (authentication, encryption, access control)

### 6.6 Interfaces & Data Models

From the description and answers:
- Identify protocols (BLE, WiFi, USB HID, HTTP, MQTT, LoRa, OCPP, etc.)
- Describe endpoints, characteristics, topics, commands
- Define payload structures (fields, units, types)
- Specify direction (client -> server, device -> cloud, etc.)

### 6.7 Phases

At minimum define:
- **Phase 1**: Infrastructure / Foundation
- **Phase 2**: Core Functional Features
- **Phase 3+** (optional): Optimization, UX, analytics, etc.

Each phase must include: Scope, Deliverables, Exit Criteria, Dependencies.

### 6.8 Operational Procedures

Extract or infer:
- Deployment / flashing / installation
- Configuration / provisioning
- Normal operation workflows
- Failure recovery (reset, re-provisioning, safe-mode)

If not covered in the description, provide a generic but plausible set for the
domain.

### 6.9 Verification & Validation

From extracted requirements:
- Create test cases that verify FRs and critical NFRs
- Organize by phase and feature area
- Use structured format: Objective, Preconditions, Steps, Expected Result
- Build the traceability matrix (Section 8)

## 7. Canonical FSD Structure

All generated or updated FSDs must conform to this structure:

```markdown
# <Project Name> — Functional Specification Document (FSD)

## 1. System Overview
- Purpose
- Problem statement
- Users / stakeholders
- Goals & non-goals
- High-level system flow

## 2. System Architecture
### 2.1 Logical Architecture
- Subsystems
- Data flow
- Runtime interactions

### 2.2 Hardware / Platform Architecture
- Devices, nodes, servers
- Key hardware / runtime platforms
- Connectivity and power (if relevant)

### 2.3 Software Architecture
- Tasks / modules / services
- Boot sequence (if applicable)
- Persistence / storage
- Update model (OTA, rollout strategy, etc.)

## 3. Implementation Phases
### 3.1 Phase 1 — Infrastructure Foundation
### 3.2 Phase 2 — Core Functionality
### 3.3 Phase 3+ — Extensions / Enhancements

Each phase includes:
- Scope (what is included)
- Deliverables (artifacts, running features)
- Exit criteria (tests passed, demos, metrics)
- Dependencies (on previous phases or external factors)

## 4. Functional Requirements
### 4.1 Functional Requirements (FR)
- FR-x.y [Must/Should/May]: requirement text

### 4.2 Non-Functional Requirements (NFR)
- NFR-x.y [Must/Should/May]: requirement text

### 4.3 Constraints
- Technological, regulatory, environmental constraints

## 5. Risks, Assumptions & Dependencies
- Technical risks (with likelihood, impact, mitigation)
- Assumptions (mark items inferred by this skill with "(assumed)")
- External dependencies
- Environmental constraints
- Regulatory constraints

## 6. Interface Specifications
### 6.1 External Interfaces
- APIs, protocols, user-facing interfaces

### 6.2 Internal Interfaces
- Inter-module / inter-service communication

### 6.3 Data Models / Schemas
- Key entities, message formats, payload schemas

### 6.4 Commands / Opcodes
- (If embedded or custom protocol — omit section if not applicable)

## 7. Operational Procedures
- Deployment / installation / flashing
- Provisioning / configuration
- Normal operation workflows
- Maintenance procedures
- Recovery procedures (factory reset, re-provisioning, safe-mode)

## 8. Verification & Validation
### 8.1 Phase 1 Verification
| Test ID | Feature | Procedure | Success Criteria |
|---------|---------|-----------|-----------------|

### 8.2 Phase 2 Verification
| Test ID | Feature | Procedure | Success Criteria |
|---------|---------|-----------|-----------------|

### 8.3 Acceptance Tests
- End-to-end scenarios
- Performance / load / reliability tests (if applicable)

### 8.4 Traceability Matrix
| Requirement | Priority | Test Case(s) | Status |
|------------|----------|-------------|--------|
| FR-1.1     | Must     | TC-1.1, TC-1.2 | Covered |
| NFR-2.1    | Should   | TC-5.1      | Covered |
| FR-3.4     | Must     | ---         | GAP    |

## 9. Troubleshooting Guide
| Symptom | Likely Cause | Diagnostic Steps | Corrective Action |
|---------|-------------|-----------------|-------------------|

## 10. Appendix
- Constants, magic numbers, configuration defaults
- UUIDs, endpoints, topics, pinouts
- Timing diagrams, sequence descriptions
- Example logs, traces, payloads
```

### 7.1 Section Inclusion Rules

Not every section applies to every project. The skill must:

- **Always include**: Sections 1, 2, 3, 4, 5, 7, 8 (with traceability matrix)
- **Include if applicable**: Section 6.4 (Commands/Opcodes) — only for embedded or
  custom protocols
- **Include if complexity >= Medium**: Section 9 (Troubleshooting), full Appendix
- **Include if complexity = High**: All sections, fully expanded
- **Omit empty sections** rather than writing "N/A" — but note the omission reason
  in a comment if it might confuse readers

## 8. Traceability Matrix (Mandatory)

Every FSD must contain a traceability matrix in Section 8.4.

Rules:
- Every FR and NFR with priority **Must** or **Should** must appear in >= 1 test.
- Every test case must reference the FR(s) / NFR(s) it validates.
- Requirements with no test coverage must be flagged as `GAP`.
- **May**-priority requirements may have test coverage but it is not mandatory.
- When updating an FSD (evolve mode), the matrix must be regenerated to reflect
  any added, removed, or changed requirements and tests.

## 9. Formatting & Style Rules

- Output pure Markdown — no HTML tags.
- Use heading levels exactly as defined in Section 7.
- Use bullet lists for requirements; tables for tests, interfaces, and diagnostics.
- Use concise, unambiguous engineering language.
- Use **"shall"** for requirements ("The system shall...").
- Use **"must"** for constraints ("The device must operate on 3.3V").
- Avoid marketing language, filler, and subjective qualifiers.
- Keep requirement IDs stable across evolve updates — never renumber existing IDs
  unless explicitly asked to refactor numbering.
- Use `(assumed)` inline for inferred details.

## 10. Output File Naming & Location

### 10.1 Default Location

If the user does not specify a target path:

```
Documents/<project-name-kebab-case>-fsd.md
```

Create the `Documents/` directory if it does not exist.

Examples:
- `Documents/esp32-ble-hid-keyboard-fsd.md`
- `Documents/solar-ev-charging-controller-fsd.md`
- `Documents/lora-mailbox-notifier-fsd.md`

### 10.2 Explicit Path

If the user provides a path, use it exactly. Do not relocate or rename the file.

### 10.3 Evolve Mode

When updating, write to the same file that was read. Confirm the path before
writing if it was auto-detected.

## 11. Example Output Snippet

The following snippet demonstrates the expected tone, structure, and level of
detail for a medium-complexity project:

```markdown
# ESP32 BLE HID Keyboard — Functional Specification Document (FSD)

## 1. System Overview

The ESP32-S3 BLE HID Keyboard System enables a smartphone app to transmit text
commands via BLE to an ESP32-S3 microcontroller, which converts them into USB HID
keyboard events for any connected host computer. The system eliminates the need
for Bluetooth keyboard pairing on the host side and provides deterministic,
low-latency input paths suitable for accessibility tools, automation, and
assistive typing.

**Primary goals:**
- Reliable BLE -> HID translation with sub-50 ms latency.
- Support for multiple keyboard layouts (US, DE, FR at minimum).
- OTA firmware updates via WiFi for field maintenance.
- Robust provisioning, logging, and recovery mechanisms.

**Non-goals:**
- The system does not act as a general-purpose BLE-to-USB bridge.
- No audio or media key support in Phase 1-2.

**Users / stakeholders:**
- End users who need assistive or automated keyboard input.
- Developers/installers who flash and provision the device.

## 4. Functional Requirements

### 4.1 Functional Requirements

#### Communication
- **FR-1.1** [Must]: The device shall accept text input via BLE Nordic UART
  Service (NUS) from a connected smartphone.
- **FR-1.2** [Must]: The device shall convert received text into USB HID keyboard
  reports and send them to the connected host within 50 ms.
- **FR-1.3** [Should]: The device shall support keyboard layout selection via BLE
  command.

#### Update & Maintenance
- **FR-2.1** [Must]: The device shall support OTA firmware updates triggered via
  BLE command or HTTP endpoint.
- **FR-2.2** [Should]: The device shall report its firmware version via HTTP
  `/status` endpoint.

### 4.2 Non-Functional Requirements

- **NFR-1.1** [Must]: BLE-to-HID latency shall not exceed 50 ms under normal
  operating conditions.
- **NFR-1.2** [Must]: The device shall recover from OTA failure by rolling back
  to the previous firmware partition.

## 5. Risks, Assumptions & Dependencies

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| USB HID descriptor rejected by host OS | Medium | High | Test with macOS, Windows, Linux during Phase 2 |
| BLE connection drops during text entry | Low | Medium | Implement reconnect logic with buffering |

**Assumptions:**
- The host computer provides USB bus power (500 mA) (assumed).
- iOS is the primary mobile platform; Android support is deferred (assumed).

**Dependencies:**
- ESP-IDF v5.x TinyUSB stack for HID support.
- NimBLE stack for BLE.

## 8. Verification & Validation

### 8.4 Traceability Matrix

| Requirement | Priority | Test Case(s)       | Status  |
|------------|----------|--------------------|---------|
| FR-1.1     | Must     | TC-2.1             | Covered |
| FR-1.2     | Must     | TC-2.2, TC-2.3     | Covered |
| FR-1.3     | Should   | TC-2.4             | Covered |
| FR-2.1     | Must     | TC-1.5, TC-2.5     | Covered |
| FR-2.2     | Should   | TC-2.6             | Covered |
| NFR-1.1    | Must     | TC-2.3             | Covered |
| NFR-1.2    | Must     | TC-2.7             | Covered |
```

## 12. Evolve Mode — Detailed Behavior

When operating in evolve mode, the skill must follow these rules:

### 12.1 What to Preserve

- All section headings and numbering for unaffected sections.
- All existing FR/NFR IDs — never renumber unless explicitly asked.
- All existing test case IDs.
- Prose in unaffected sections — do not rephrase or "improve" text that is not
  part of the delta.

### 12.2 What to Update

- Sections directly affected by the delta description.
- The traceability matrix (always — to reflect any FR/test changes).
- Cross-references if section numbers shift (e.g., new phase inserted).
- The Risks & Assumptions section if the delta introduces new risks or invalidates
  existing assumptions.

### 12.3 What to Add

- New FRs/NFRs get the next available ID in their group.
- New phases get inserted in logical order; subsequent phases are renumbered.
- New test cases get the next available TC-x.y ID.
- New traceability rows are appended to the matrix.

### 12.4 What to Remove

- Requirements or sections the delta explicitly deprecates or removes.
- Assumptions that are now confirmed or contradicted by the delta.
- Traceability rows for removed requirements (mark as "Removed" rather than
  deleting, to maintain audit trail).

### 12.5 Conflict Resolution

If the delta contradicts existing FSD content:
1. Flag the contradiction to the user via **AskUserQuestion**.
2. Do not silently overwrite — get explicit confirmation.
3. Once resolved, update all affected sections consistently.

## 13. Quality Checklist

After generating or updating an FSD, the skill must verify:

- [ ] Every **Must** and **Should** FR/NFR appears in the traceability matrix.
- [ ] Every traceability row with no test is marked `GAP`.
- [ ] No `<placeholder>` or `TODO` text remains (flag to user if unresolvable).
- [ ] Section numbering is sequential with no gaps.
- [ ] All phases have scope, deliverables, and exit criteria.
- [ ] The file has been written to the correct path.
- [ ] (Evolve mode) Unaffected sections are identical to the original.

Report any checklist failures to the user before finalizing.
