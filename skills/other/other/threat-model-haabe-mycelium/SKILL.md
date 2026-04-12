---
name: threat-model
description: "Use to conduct STRIDE threat modeling for a system or feature design."
---

# Threat Model Skill

STRIDE threat modeling for secure design.

## Workflow

1. **Define scope**: What system/feature/component is being modeled?

2. **Draw data flow diagram** (textual):
   - Identify actors (users, external systems)
   - Identify processes (services, functions)
   - Identify data stores (databases, caches, files)
   - Identify data flows (what moves between components)
   - Identify trust boundaries (where trust level changes)

3. **For each component and data flow, assess STRIDE threats**:

   | Threat | Description | Question to Ask |
   |--------|------------|----------------|
   | **S**poofing | Impersonating something or someone | Can an attacker pretend to be this user/system? |
   | **T**ampering | Modifying data or code | Can data be changed in transit or at rest? |
   | **R**epudiation | Claiming to not have done something | Can a user deny an action without accountability? |
   | **I**nfo Disclosure | Exposing data to unauthorized parties | Can sensitive data leak? |
   | **D**enial of Service | Making the system unavailable | Can this component be overwhelmed? |
   | **E**levation of Privilege | Gaining unauthorized access | Can a user escalate their permissions? |

4. **For each identified threat**:
   - Severity: Critical / High / Medium / Low
   - Likelihood: High / Medium / Low
   - Existing mitigations (if any)
   - Recommended mitigations
   - Residual risk after mitigation

   **For AI-powered systems**: Extend STRIDE with AI-specific threat dimensions:
   - **Autonomy risk**: Can the AI take actions beyond its intended scope?
   - **Oversight gap**: Is human-in-the-loop oversight meaningful? (Test Authority/Time/Understanding per Bannerman's triad -- see security-trust.md)
   - **Feedback poisoning**: Can adversarial inputs degrade the system over time?
   - **Opacity risk**: Can decisions be explained to affected parties?

5. **Output**:
   ```
   ## Threat Model: [System/Feature]

   ### Data Flow
   [textual diagram]

   ### Trust Boundaries
   - [boundary 1]: [what changes]
   - [boundary 2]: [what changes]

   ### Threats
   | ID | Component | STRIDE | Threat | Severity | Likelihood | Mitigation |
   |----|-----------|--------|--------|----------|-----------|------------|
   | T1 | ... | S | ... | ... | ... | ... |

   ### Priority Actions
   1. [highest priority mitigation]
   2. [next priority]
   3. [next priority]
   ```

## Theory Citations
- STRIDE: Microsoft threat modeling methodology
- OWASP: Threat modeling guidance
