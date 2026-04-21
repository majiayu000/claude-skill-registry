---
name: threat-model
description: "Use to conduct STRIDE threat modeling for a system or feature design."
instruction_budget: 28
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

## OWASP Top 10 for LLM Applications (2025)

For AI-powered products (`product_type: ai_tool` or any product using LLM components), extend the STRIDE analysis with LLM-specific threats:

| # | Threat | Description |
|---|--------|-------------|
| LLM01 | Prompt Injection | Manipulating model via crafted inputs (direct or indirect) |
| LLM02 | Sensitive Information Disclosure | Model leaking training data, PII, or system prompts |
| LLM03 | Supply Chain Vulnerabilities | Compromised model weights, training data, or plugins |
| LLM04 | Data and Model Poisoning | Corrupting training/fine-tuning data to alter behavior |
| LLM05 | Improper Output Handling | Trusting LLM output without validation (enables injection downstream) |
| LLM06 | Excessive Agency | Granting LLM too many permissions, functions, or autonomy |
| LLM07 | System Prompt Leakage | Extraction of system-level instructions via adversarial prompts |
| LLM08 | Vector and Embedding Weaknesses | Manipulating RAG pipelines via poisoned embeddings |
| LLM09 | Misinformation | Model generating false but plausible content (hallucination in high-stakes contexts) |
| LLM10 | Unbounded Consumption | Resource exhaustion via expensive queries, denial-of-wallet attacks |

*Source: OWASP Top 10 for LLM Applications v2025.1 (genai.owasp.org). Updated from v1.1 (2023) — new entries: System Prompt Leakage (LLM07), Vector and Embedding Weaknesses (LLM08), Misinformation (LLM09), Unbounded Consumption (LLM10).*

For each LLM component in the threat model, assess all 10 threats. Use alongside STRIDE — STRIDE covers system-level threats, OWASP LLM covers model-level threats.

## Theory Citations
- STRIDE: Microsoft threat modeling methodology (Shostack)
- OWASP Top 10:2025: Web application security risks
- OWASP Top 10 for LLM Applications v2025: AI/LLM-specific security risks
