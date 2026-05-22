---
name: threat-modeling
description: Structured security analysis using OWASP Four-Question Framework and STRIDE methodology. Generates threat matrices with risk ratings, mitigations, and prioritization. Use for attack surface analysis, security architecture review, or when asking what can go wrong.
license: MIT
metadata:
  version: 1.0.0
  model: claude-sonnet-4-5
---

# Threat Modeling

Systematic identification, documentation, and mitigation of security threats.

## Triggers

| Phrase | Context |
|--------|---------|
| `threat model` | Starting or updating a threat model |
| `attack surface analysis` | Identifying exposure points |
| `security architecture review` | Reviewing design for vulnerabilities |
| `STRIDE analysis` | Applying STRIDE methodology |
| `what can go wrong` | Brainstorming security concerns |

## Quick Reference

| Input | Output | Destination |
|-------|--------|-------------|
| Architecture diagram or description | Threat matrix with STRIDE categories | `.agents/security/threat-models/` |
| Component list | Trust boundary analysis | `.agents/security/threat-models/` |
| Data flow description | Data flow diagram threats | `.agents/security/threat-models/` |
| Prior threat model | Updated model with delta analysis | `.agents/security/threat-models/` |

---

## Process Overview

```text
                         OWASP Four-Question Framework
                         =============================

          Q1: What are we        Q2: What can         Q3: What do we      Q4: Did we do
          working on?            go wrong?            do about it?        a good job?
               |                      |                    |                   |
               v                      v                    v                   v
        +-----------+          +------------+        +-----------+       +----------+
        | Phase 1   |          | Phase 2    |        | Phase 3   |       | Phase 4  |
        | Scope &   |  ----->  | Threat     | -----> | Mitigation| ----> | Validate |
        | Decompose |          | Identify   |        | Strategy  |       | Model    |
        +-----------+          +------------+        +-----------+       +----------+
              |                      |                    |                   |
              v                      v                    v                   v
        Trust Boundaries       STRIDE Matrix         Prioritized         Threat Model
        Data Flows             Kill Chains           Mitigations         Document
        Assets                 Attack Trees          Risk Ratings
```

---

## Phase 1: Scope and Decompose

> OWASP Q1: What are we working on?

### 1.1 Define Scope

Determine what you are threat modeling:

| Scope Level | Examples | Typical Depth |
|-------------|----------|---------------|
| **Sprint** | Single feature, API endpoint | 1-2 hours |
| **Component** | Auth module, payment service | Half day |
| **System** | Entire application | 1-2 days |
| **Enterprise** | Multiple systems | Multi-day workshop |

Document scope in the threat model header:

```markdown
## Scope

- **Subject**: [Feature/Component/System name]
- **Boundaries**: [What is IN scope and OUT of scope]
- **Stakeholders**: [Who requested, who will review]
- **Date**: [When analysis performed]
- **Version**: [Model version for tracking changes]
```

### 1.2 Create Architecture Model

Choose appropriate diagram type:

| Diagram Type | Best For | Tools |
|--------------|----------|-------|
| **Data Flow Diagram (DFD)** | Most threat models | Mermaid, draw.io |
| **Component Diagram** | Service boundaries | Mermaid, PlantUML |
| **Sequence Diagram** | Auth/data flows | Mermaid |
| **Deployment Diagram** | Infrastructure threats | Mermaid |

**Required DFD Elements:**

```text
+----------+     HTTPS      +----------+     SQL       +----------+
| External | -------------> |  Process | ------------> |  Data    |
|  Entity  |                |          |               |  Store   |
+----------+                +----------+               +----------+
     |                           |
     |     Trust Boundary        |
     +---------------------------+
```

- **External Entities**: Users, third-party systems (outside your control)
- **Processes**: Code that transforms data (your application)
- **Data Stores**: Databases, files, caches (where data persists)
- **Data Flows**: Arrows showing data movement (labeled with protocol)
- **Trust Boundaries**: Dashed lines showing privilege changes

### 1.3 Identify Assets

List what attackers want:

| Asset Category | Examples |
|----------------|----------|
| **Data** | PII, credentials, financial, health |
| **Compute** | CPU cycles, storage, network bandwidth |
| **Access** | Admin privileges, API keys, tokens |
| **Reputation** | Brand trust, user confidence |
| **Availability** | Service uptime, response time |

### 1.4 Map Trust Boundaries

Identify where privilege levels change:

- Network boundaries (internet to internal)
- Process boundaries (user to kernel)
- Authentication boundaries (anonymous to authenticated)
- Authorization boundaries (user to admin)

---

## Phase 2: Threat Identification

> OWASP Q2: What can go wrong?

### 2.1 Apply STRIDE per Element

For each element in your diagram, apply STRIDE:

| Category | Definition | Applies To | Example Questions |
|----------|------------|------------|-------------------|
| **S**poofing | Pretending to be someone else | External entities, data flows | Can an attacker impersonate a user? |
| **T**ampering | Modifying data or code | Processes, data stores, data flows | Can data be modified in transit/at rest? |
| **R**epudiation | Denying an action | Processes | Can users deny performing actions? |
| **I**nfo Disclosure | Exposing information | Data stores, data flows | Can sensitive data leak? |
| **D**enial of Service | Making service unavailable | Processes, data stores | Can resources be exhausted? |
| **E**levation of Privilege | Gaining unauthorized access | Processes | Can users escalate privileges? |

**STRIDE Applicability Matrix:**

| Element Type | S | T | R | I | D | E |
|--------------|---|---|---|---|---|---|
| External Entity | X | | | | | |
| Process | X | X | X | X | X | X |
| Data Store | | X | | X | X | |
| Data Flow | | X | | X | X | |

### 2.2 Build Threat Matrix

Use the generate script to create a structured matrix:

```bash
python .claude/skills/threat-modeling/scripts/generate_threat_matrix.py \
    --scope "Authentication Service" \
    --output .agents/security/threat-models/auth-threats.md
```

**Manual Format:**

```markdown
## Threat Matrix

| ID | Element | STRIDE | Threat | Likelihood | Impact | Risk |
|----|---------|--------|--------|------------|--------|------|
| T001 | Login API | S | Credential stuffing | High | High | Critical |
| T002 | Session Store | T | Session fixation | Medium | High | High |
| T003 | Audit Log | R | Log tampering | Low | Medium | Medium |
```

### 2.3 Apply Attack Trees (Optional)

For complex threats, decompose with attack trees:

```text
              [Steal User Data]
                    |
        +-----------+-----------+
        |                       |
   [SQL Injection]      [Compromised API Key]
        |                       |
   +----+----+             +----+----+
   |         |             |         |
[Error]  [Blind]      [Phishing]  [Git Leak]
```

### 2.4 Apply Kill Chains (Optional)

Map attacker progression for sophisticated threats:

| Phase | Attacker Action | Detection Opportunity |
|-------|-----------------|----------------------|
| Recon | Port scanning | Network monitoring |
| Weaponize | Craft exploit | Threat intelligence |
| Deliver | Send phishing email | Email filtering |
| Exploit | Execute payload | Endpoint detection |
| Install | Persist access | File integrity monitoring |
| Command | Establish C2 | Network anomaly detection |
| Action | Exfiltrate data | DLP, egress monitoring |

---

## Phase 3: Mitigation Strategy

> OWASP Q3: What are we going to do about it?

### 3.1 Risk Rating

Calculate risk for prioritization:

```text
Risk = Likelihood x Impact

Likelihood Scale:
  High (3)   = Exploitable with public tools, no auth required
  Medium (2) = Requires some skill or access
  Low (1)    = Requires significant effort or insider access

Impact Scale:
  High (3)   = Data breach, system compromise, regulatory violation
  Medium (2) = Limited data exposure, service degradation
  Low (1)    = Minor inconvenience, no sensitive data
```

**Risk Matrix:**

|              | Impact: Low | Impact: Medium | Impact: High |
|--------------|-------------|----------------|--------------|
| **High** Likelihood | Medium | High | Critical |
| **Medium** Likelihood | Low | Medium | High |
| **Low** Likelihood | Low | Low | Medium |

### 3.2 Select Mitigation Strategy

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Mitigate** | Risk can be reduced to acceptable level | Add input validation |
| **Accept** | Cost of mitigation exceeds risk | Low-impact, unlikely threat |
| **Transfer** | Someone else can manage risk better | Cyber insurance, third-party service |
| **Eliminate** | Remove the vulnerable component | Drop unused feature |

### 3.3 Document Mitigations

For each threat, document:

```markdown
### T001: Credential Stuffing on Login API

**Risk**: Critical (High Likelihood x High Impact)

**Mitigations**:

1. **Implement rate limiting** (Mitigate)
   - Max 5 attempts per IP per minute
   - Progressive delays after failures
   - Status: Planned for Sprint 23

2. **Add CAPTCHA after failures** (Mitigate)
   - Trigger after 3 failed attempts
   - Status: In progress

3. **Enable MFA** (Mitigate)
   - TOTP or WebAuthn
   - Status: Blocked on product decision

**Residual Risk**: Medium (after mitigations applied)
```

### 3.4 Generate Mitigation Roadmap

```bash
python .claude/skills/threat-modeling/scripts/generate_mitigation_roadmap.py \
    --input .agents/security/threat-models/auth-threats.md \
    --output .agents/security/threat-models/auth-roadmap.md
```

---

## Phase 4: Validation

> OWASP Q4: Did we do a good job?

### 4.1 Model Validation

Run the validation script:

```bash
python .claude/skills/threat-modeling/scripts/validate_threat_model.py \
    .agents/security/threat-models/auth-threats.md
```

**Validation Checks:**

- [ ] All components have at least one threat identified
- [ ] All trust boundaries are crossed by at least one data flow
- [ ] All STRIDE categories considered for applicable elements
- [ ] All Critical/High risks have mitigations planned
- [ ] No orphaned threats (threats without parent component)

### 4.2 Peer Review

Request review from:

- Security team member
- Architect familiar with the system
- Developer implementing mitigations

### 4.3 Schedule Updates

Threat models are living documents. Update when:

- New features added
- Architecture changes
- Security incident occurs
- During regular security reviews (quarterly recommended)

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `generate_threat_matrix.py` | Create structured threat matrix | `python scripts/generate_threat_matrix.py --scope "Name" --output path.md` |
| `generate_mitigation_roadmap.py` | Create prioritized roadmap | `python scripts/generate_mitigation_roadmap.py --input threats.md --output roadmap.md` |
| `validate_threat_model.py` | Validate model completeness | `python scripts/validate_threat_model.py <model.md>` |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success / Validation passed |
| 1 | General failure |
| 10 | Validation failed (missing required elements) |

---

## Templates

### Threat Model Document

Use the template at: `templates/threat-model-template.md`

### Threat Entry

```markdown
### T{NNN}: {Threat Title}

**Element**: {Component name from DFD}
**STRIDE**: {S/T/R/I/D/E}
**Description**: {What the threat is}

**Attack Scenario**:
1. Attacker does X
2. System responds with Y
3. Attacker achieves Z

**Likelihood**: {High/Medium/Low} - {Justification}
**Impact**: {High/Medium/Low} - {Justification}
**Risk**: {Critical/High/Medium/Low}

**Mitigations**:
- [ ] {Mitigation 1} - {Status}
- [ ] {Mitigation 2} - {Status}

**Residual Risk**: {After mitigations}
**References**: {CVEs, OWASP links, etc.}
```

---

## Integration with Agent System

### Related Agents

| Agent | Relationship |
|-------|--------------|
| **security** | Invoke for detailed vulnerability analysis |
| **architect** | Review threat model during design |
| **analyst** | Research specific attack patterns |
| **qa** | Include threat scenarios in test strategy |

### Memory Integration

Query Forgetful memory for prior threat models:

```python
mcp__forgetful__execute_forgetful_tool("query_memory", {
    "query": "threat model authentication",
    "query_context": "Finding prior security analysis"
})
```

Store threat model summaries:

```python
mcp__forgetful__execute_forgetful_tool("create_memory", {
    "title": "Auth Service Threat Model Summary",
    "content": "Key threats: credential stuffing, session hijacking...",
    "context": "Security analysis Q1 2026",
    "keywords": ["threat-model", "authentication", "STRIDE"],
    "tags": ["security"],
    "importance": 8,
    "project_ids": [1]
})
```

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Threat model once and forget | Security landscape evolves | Schedule regular updates |
| Skip trust boundary analysis | Miss privilege escalation paths | Always map boundaries first |
| Generic threats only | Not actionable | Be specific to your system |
| No risk ratings | Cannot prioritize | Rate every threat |
| Mitigations without owners | Never implemented | Assign owners and deadlines |
| Copy-paste from templates | Miss system-specific threats | Use templates as starting points |

---

## References

- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [Microsoft STRIDE](https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [Attack Trees (Schneier)](https://www.schneier.com/academic/archives/1999/12/attack_trees.html)
- [Lockheed Martin Cyber Kill Chain](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html)

---

## Verification

### Success Criteria

| Criterion | Verification |
|-----------|--------------|
| All components have threats | Validation script check |
| All STRIDE categories considered | Validation script check |
| All Critical/High risks have mitigations | Validation script check |
| Risk ratings consistent | Manual review |
| Peer review completed | Stakeholder sign-off |

### Verification Command

```bash
python .claude/skills/threat-modeling/scripts/validate_threat_model.py <model.md>
```

Exit code 0 indicates a valid, complete threat model.

---

## Extension Points

| Extension | How to Add |
|-----------|------------|
| Custom STRIDE questions | Add to `references/stride-methodology.md` |
| New risk rating methodology | Add to `references/risk-rating-guide.md` |
| Additional threat categories | Extend STRIDE sections in template |
| Custom validation rules | Modify `validate_threat_model.py` |
| Integration with SAST tools | Add script in `scripts/` |

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `security-detection` | Triggers threat model review on sensitive file changes |
| `codeql-scan` | Validates code against identified threats |
| `adr-review` | Security agent reviews architecture decisions |
