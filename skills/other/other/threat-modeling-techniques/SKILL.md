---
name: threat-modeling-techniques
description: Threat modeling methodologies using STRIDE, attack trees, and risk assessment for proactive security analysis. Use when designing secure systems, conducting security reviews, or identifying potential attack vectors in applications.
---

# Threat Modeling Techniques

Systematic framework for identifying, analyzing, and mitigating security threats during system design and architecture phases using proven methodologies like STRIDE, attack trees, and risk assessment frameworks.

## When to Use This Skill

- Designing new systems or features with security requirements
- Conducting security architecture reviews
- Identifying attack vectors and threat scenarios
- Assessing security risks before implementation
- Creating security requirements and controls
- Evaluating third-party integrations for security impact
- Planning security testing strategies
- Documenting security design decisions
- Training teams on proactive security thinking
- Supporting security compliance initiatives (SOC 2, ISO 27001)

## Core Process

**Five-Stage Threat Modeling Process:**

1. **Define** - Understand the system and create architecture diagrams
2. **Identify** - Enumerate threats using structured methodologies (STRIDE, attack trees)
3. **Assess** - Evaluate risk severity and likelihood (DREAD scoring)
4. **Mitigate** - Design controls and countermeasures
5. **Validate** - Review and test security controls

## Quick Reference

| Task | Load reference |
| --- | --- |
| STRIDE: Spoofing Identity | `skills/threat-modeling-techniques/references/stride-spoofing.md` |
| STRIDE: Tampering with Data | `skills/threat-modeling-techniques/references/stride-tampering.md` |
| STRIDE: Repudiation | `skills/threat-modeling-techniques/references/stride-repudiation.md` |
| STRIDE: Information Disclosure | `skills/threat-modeling-techniques/references/stride-disclosure.md` |
| STRIDE: Denial of Service | `skills/threat-modeling-techniques/references/stride-dos.md` |
| STRIDE: Elevation of Privilege | `skills/threat-modeling-techniques/references/stride-elevation.md` |
| Attack Trees | `skills/threat-modeling-techniques/references/attack-trees.md` |
| Data Flow Diagrams (DFD) | `skills/threat-modeling-techniques/references/data-flow-diagrams.md` |
| DREAD Risk Scoring | `skills/threat-modeling-techniques/references/dread-scoring.md` |
| Mitigation Strategies | `skills/threat-modeling-techniques/references/mitigation-strategies.md` |
| Tools & Process | `skills/threat-modeling-techniques/references/tools-and-process.md` |

## Core Concepts

### STRIDE Methodology

**STRIDE** categorizes threats into six types:

- **S**poofing: Pretending to be someone/something else (authentication bypass, credential theft)
- **T**ampering: Malicious modification of data (MITM attacks, data corruption)
- **R**epudiation: Denying actions without proof (lack of audit trails)
- **I**nformation Disclosure: Exposing sensitive data (data leaks, verbose errors)
- **D**enial of Service: Making systems unavailable (resource exhaustion, DDoS)
- **E**levation of Privilege: Gaining unauthorized capabilities (privilege escalation, IDOR)

**Apply STRIDE to:**
- Each component in data flow diagrams
- Every trust boundary crossing
- All data stores and processes
- External integrations and APIs

### Attack Trees

Hierarchical diagrams showing attack paths from goals to methods:

```
[Root: Attack Goal]
    |
    +-- [OR] Method 1 (alternative paths)
    |       |
    |       +-- [AND] Required Step 1.1
    |       +-- [AND] Required Step 1.2
    |
    +-- [OR] Method 2 (alternative paths)
```

**Use attack trees to:**
- Visualize attack scenarios
- Identify easiest attack paths
- Assign attributes (cost, skill, detection likelihood)
- Prioritize mitigations for high-risk paths

### DREAD Risk Scoring

**DREAD** quantifies threat severity (each criterion scored 0-10, average = risk score):

- **D**amage Potential: How much damage if exploited?
- **R**eproducibility: How easy to reproduce?
- **E**xploitability: How easy to exploit?
- **A**ffected Users: How many users affected?
- **D**iscoverability: How easy to discover?

**Risk Levels:**
- 7.1-10.0: Critical (immediate action)
- 5.1-7.0: High (next sprint)
- 3.1-5.0: Medium (upcoming releases)
- 0.0-3.0: Low (backlog)

### Trust Boundaries

Lines separating different trust levels:

- **Network**: Internet → DMZ → Internal
- **Process**: User Mode → Kernel, Container → Host
- **User**: Anonymous → Authenticated → Admin

**At each boundary, verify:**
- Authentication required?
- Authorization checks enforced?
- Data encrypted?
- Inputs validated?
- Actions logged?

## Practical Workflow

### 1. Scope Definition (30 min)
- Identify system components in scope
- Define trust boundaries
- List assets requiring protection
- Identify compliance requirements

### 2. Architecture Decomposition (1 hour)
- Create data flow diagrams (DFDs)
- Document external dependencies
- Identify authentication/authorization points
- Map data storage locations

### 3. Threat Identification (1-2 hours)
- Apply STRIDE to each DFD element
- Create attack trees for high-value assets
- Brainstorm threat scenarios with team
- Use threat modeling tools for suggestions

### 4. Risk Assessment (1 hour)
- Apply DREAD scoring to each threat
- Prioritize threats by risk score
- Consider business context and compliance
- Identify quick wins vs. long-term efforts

### 5. Mitigation Planning (1 hour)
- Design security controls (eliminate, reduce, transfer, accept)
- Document mitigation strategies
- Create security requirements (SEC-### format)
- Assign ownership for implementation

### 6. Documentation (30 min)
- Export threat model diagrams
- Create security requirements document
- Document risk acceptance decisions
- Share with stakeholders

## Common Mistakes

**Avoid:**
- Threat modeling too late (after implementation complete)
- Focusing only on external threats (ignore insider threats)
- Creating static threat models (never updating them)
- Over-complicating diagrams (too much detail)
- Ignoring low-likelihood, high-impact threats
- Failing to document assumptions and decisions
- Not following through on mitigations

## Best Practices

**Team Involvement:**
- Developers: Implementation details, code-level threats
- Architects: System design, integration points
- Security Team: Threat expertise, attack scenarios
- Operations: Deployment, monitoring, incident response
- Product Owners: Business impact, risk acceptance decisions

**Process Integration:**
- Design phase: Threat model before implementation
- Development: Implement controls, create security tests
- Deployment: Verify controls, enable monitoring
- Maintenance: Update model when features change

## Tools

**Microsoft Threat Modeling Tool**: Visual DFD editor, automated STRIDE threat generation
**OWASP Threat Dragon**: Open source, cross-platform, web and desktop versions
**IriusRisk**: Commercial platform, DevSecOps integration, compliance mapping
**ThreatModeler**: Collaborative, cloud architecture support

## Resources

- **Microsoft Threat Modeling Tool**: https://aka.ms/threatmodelingtool
- **OWASP Threat Dragon**: https://owasp.org/www-project-threat-dragon/
- **STRIDE Documentation**: https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
- **Threat Modeling Manifesto**: https://www.threatmodelingmanifesto.org/
- **NIST Threat Modeling**: https://csrc.nist.gov/projects/threat-modeling
