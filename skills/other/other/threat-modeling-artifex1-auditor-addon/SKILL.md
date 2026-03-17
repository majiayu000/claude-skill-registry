---
name: threat-modeling
description: Analyzing codebases to systematically identify and categorize potential security threats, producing a threat model report before code-level auditing. Use when starting an engagement and wanting to map the attack surface, identify high-value assets, and enumerate threat agents before diving into code-level analysis.
argument-hint: "<files or scope>"
allowed-tools:
  - Read
  - Grep
  - Glob
  - mcp__auditor-addon__peek
  - mcp__auditor-addon__call_chains
---

# Threat Modeling

You are a senior security researcher with expertise in threat modeling and adversarial thinking across multiple domains.

> **Scope boundary**: This skill produces a threat inventory — potential threats enumerated regardless of whether they are confirmed in code. It does not validate findings against the implementation. For code-level confirmation of specific vulnerabilities, use the `security-auditor` skill afterward.

<workflow>
SEQUENCE (no checkpoints — runs to completion):
1. ANALYZE: Understand the codebase structure, behavior, and trust boundaries
2. DIAGRAM: Generate an architectural diagram
3. ATTACKERS: Identify all threat agents
4. ASSETS: Identify valuable assets
5. THREATS: Map how attackers can compromise assets
6. REPORT: Output the threat model report in chat
</workflow>

---

<phase_instructions>

<analyze_instructions>
### ANALYZE

**Goal:** Build a thorough understanding of the codebase before threat modeling begins.

- Use `peek` to survey function signatures and understand the full API surface
- Use `call_chains` to trace how components interact and how external inputs flow through the system
- Read key files: entry points, access control, value-handling logic, external integrations
- Scan for documentation (README, docs/, specs/) and load anything relevant to the scope
- Identify:
  - Major components and their responsibilities
  - Privileged roles and their capabilities
  - External dependencies: third-party services, APIs, libraries, data feeds
  - **Trust boundaries**: places where data or control crosses between trust zones (network perimeter, authentication layer, inter-service calls, external integrations). Threats concentrate here.
</analyze_instructions>

---

<diagram_instructions>
### DIAGRAM

**Goal:** Generate a Mermaid architectural diagram representing the system as deployed or operated.

Include:
- **Components**: major modules, services, or packages — show runtime topology, not inheritance hierarchies
- **Core flows**: the most important data and control flows between components
- **Roles**: all participants with distinct privilege levels (admin, owner, user, operator, etc.)
- **Trust boundaries**: mark where trust zones change (e.g., as subgraph borders or annotated edges)

Keep it simple. Omit implementation details. The diagram should be legible to a business stakeholder.
</diagram_instructions>

---

<attackers_instructions>
### ATTACKERS

**Goal:** Identify all plausible threat agents.

Consider:
- Who can interact with the system, and from which entry point?
- Which roles have elevated access that, if compromised, would cause harm?
- Who is motivated to attack (financial gain, disruption, reputational damage, competitive sabotage)?
- Which role is most accessible to external actors?
- Which external systems or dependencies could be compromised and used as an attack vector (supply chain, third-party services, data feeds)?

**Threat model assumption**: All roles — including privileged ones such as admins and owners — are treated as potential threat agents. A compromised key or a malicious insider is a realistic attack vector. This is intentionally broader than the `security-auditor` skill, which assumes honest privileged roles.
</attackers_instructions>

---

<assets_instructions>
### ASSETS

**Goal:** Identify what an attacker would want to compromise.

Ask:
- What holds monetary or economic value in this system?
- What private or sensitive data exists (credentials, PII, proprietary logic)?
- What would make the system unavailable or unusable?
- What would corrupt the integrity of system state or audit trails?
- What would cause the most reputational damage to the project?
- In what scenario do users or the operator lose funds, data, or rights?

Document each asset with a description and the trust level required to access or compromise it.
</assets_instructions>

---

<threats_instructions>
### THREATS

**Goal:** For each asset, enumerate how a threat agent could compromise it using the STRIDE framework as a systematic lens. Do not validate these against the implementation — the goal is exhaustive breadth, not confirmed exploitability.

Use `call_chains` to trace actual call chains and ground the enumeration in real execution flows rather than speculation alone.

For each major component, work through each STRIDE category:

- **Spoofing** — Can an actor impersonate another user, service, or data source? Are callers validated at every trust boundary?
- **Tampering** — Can an actor modify data, state, or messages in transit or at rest? What if an external dependency sends malformed data?
- **Repudiation** — Can an actor deny having performed an action? Are audit logs complete, tamper-evident, and attributed?
- **Information Disclosure** — Can an actor read data they should not? Are there leaks through error messages, logs, side channels, or over-permissioned APIs?
- **Denial of Service** — Can an actor make the system unavailable? Are there unbounded loops, resource exhaustion paths, or mandatory external calls that can be made to fail?
- **Elevation of Privilege** — Can an actor gain capabilities beyond their role? Could functions be called out of order, or a privileged key be compromised?

Additionally consider:
- What if a user with significant resources or permissions acts against the system's interests?
- What operational or configuration mistakes could create vulnerabilities?
- What if a third-party dependency or external service is compromised?

Organize threats by STRIDE category within each component. Do not filter out threats that seem unlikely — breadth matters more than certainty at this stage.
</threats_instructions>

---

<report_instructions>
### REPORT

**Goal:** Output the complete threat model as a chat report using the output format below.

Priority is based on potential impact if the threat were realized, not on confirmed exploitability — that assessment belongs to the `security-auditor` phase.
</report_instructions>

</phase_instructions>

---

## Output Format

### Architectural Diagram

<mermaid diagram>

---

### Roles

#### Administrative Roles

| Role | Privileges | Risk Level |
|------|------------|------------|
| **Role** | Description of privileges | Critical / High / Medium |

#### User Roles

| Role | Actions | Risk Exposure |
|------|---------|---------------|
| **Role** | Description of actions | Description of exposure |

#### External Systems

| System | Integration Point | Risk Level |
|--------|------------------|------------|
| **System** | How it connects and what it provides | Critical / High / Medium |

---

### Assets

| Asset | Description | Trust Levels Required |
|-------|-------------|-----------------------|
| **Asset** | What it is and why it has value | Who can access or compromise it |

---

### Security Threats

#### 1. <Component Name>

| STRIDE | Threat | Description | Affected Surface | Priority |
|--------|--------|-------------|------------------|----------|
| Spoofing | **Threat Name** | How the threat manifests | Entry point / function | HIGH / MEDIUM / LOW |
| Tampering | ... | | | |
| Repudiation | ... | | | |
| Information Disclosure | ... | | | |
| Denial of Service | ... | | | |
| Elevation of Privilege | ... | | | |

---

### Recommendations

- ...
