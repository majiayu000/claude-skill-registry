---
name: healthcare-poa
description: >-
  Drafts a state-compliant Healthcare Power of Attorney (HCPOA) designating an
  agent to make medical decisions for an incapacitated principal. Covers scope
  of authority, life-sustaining treatment directives, HIPAA authorization, organ
  donation preferences, and jurisdiction-specific execution formalities. Use
  when the user mentions healthcare power of attorney, medical power of
  attorney, healthcare proxy, healthcare agent designation, HCPOA, medical
  decision-making authority, or advance healthcare directive naming an agent.
  Also trigger when the user asks about HIPAA authorization for a healthcare
  agent, life-sustaining treatment elections, or state-specific execution
  requirements for healthcare proxy documents.
tags:
  - agreement
  - drafting
  - regulatory
---

# Healthcare Power of Attorney

Drafts a jurisdiction-compliant HCPOA that designates an agent, defines scope of authority, captures principal treatment directives, and satisfies state execution formalities.

## Prerequisites

1. **Principal** — full legal name, address, DOB
2. **Agent** — full legal name, address, contact; confirm eligibility under state law (some states disqualify treating physicians, facility employees)
3. **Successor agent(s)** — same details if designated; activation sequence
4. **Jurisdiction** — governs statutory form, witness/notary rules, mandatory language
5. **Healthcare preferences** — wishes on life-sustaining treatment, ANH, CPR, palliative care, organ donation
6. **Religious/moral directives** or limitations on agent authority (if any)

## Output Structure

### 1. Jurisdictional Research (pre-draft)

Complete before drafting:

| Requirement | Details |
|---|---|
| Statutory form required? | Yes / No — cite statute `[VERIFY]` |
| Witness count & eligibility | Typically 2; confirm exclusions (agent, providers, relatives) |
| Notarization | Required / Optional / Not required |
| Mandatory warnings/notices | Include verbatim if required by statute |
| Prohibited provisions | E.g., some states bar agent from refusing comfort care |
| Duration / revocation | Durable by default in most states; confirm revocation methods |

### 2. Document Sections

**TITLE:** Healthcare Power of Attorney of [Principal Full Name] — State of [Jurisdiction]

**ARTICLE 1 — DESIGNATION OF AGENT**
- Primary agent: name, address, relationship
- Successor agent(s): same; activation sequence when primary is unavailable/unwilling

**ARTICLE 2 — EFFECTIVE DATE AND DURABILITY**
- Springing (incapacity-triggered) vs. immediate authority
- Durability language per state statute; incapacity determination standard

**ARTICLE 3 — SCOPE OF AUTHORITY**

Standard grant:
- [ ] Medical treatment decisions (surgical, diagnostic, medication)
- [ ] Facility placement and transfer
- [ ] Hiring/discharging healthcare providers
- [ ] Access to medical records (HIPAA release — see Article 6)
- [ ] Organ/tissue donation and anatomical gifts
- [ ] Disposition of remains (if principal elects)

Principal-specified limitations:

**ARTICLE 4 — SPECIFIC HEALTHCARE DIRECTIVES**

| Scenario | Terminal Condition | Persistent Vegetative State |
|---|---|---|
| Artificial nutrition & hydration | Withhold / Provide / Agent discretion | Withhold / Provide / Agent discretion |
| Mechanical ventilation | Withhold / Provide / Agent discretion | Withhold / Provide / Agent discretion |
| CPR | Withhold / Provide / Agent discretion | Withhold / Provide / Agent discretion |
| Dialysis | Withhold / Provide / Agent discretion | Withhold / Provide / Agent discretion |
| Pain management / palliative care | Principal directive | Principal directive |

Distinguish **binding directives** from **guidance for agent discretion**.

**ARTICLE 5 — RELIGIOUS/MORAL GUIDANCE**
- Faith traditions or values to guide agent decision-making

**ARTICLE 6 — HIPAA AUTHORIZATION**
- Explicit authorization for agent to access all PHI necessary to perform duties
- Reference 45 C.F.R. § 164.510(b) `[VERIFY current reg]`
- Effective immediately upon execution (not contingent on incapacity trigger)

**ARTICLE 7 — REVOCATION**
- Principal may revoke orally, in writing, or by destruction
- Later-executed document controls; notification instructions to agent and providers

**ARTICLE 8 — SEVERABILITY AND GOVERNING LAW**

**ARTICLE 9 — CAPACITY DECLARATION**
- Principal affirms voluntary execution, without duress or undue influence, while of sound mind

### 3. Execution Block

```
PRINCIPAL SIGNATURE

_______________________________   Date: __________
[Principal Full Name]

WITNESS ATTESTATIONS (confirm count per jurisdiction)

We affirm the principal signed voluntarily, appears competent, and we are not the
designated agent, not related by blood/marriage, and not involved in the principal's healthcare.

Witness 1: _______________________________   Date: __________
Address: ________________________________

Witness 2: _______________________________   Date: __________
Address: ________________________________

NOTARIAL CERTIFICATE (if required by jurisdiction)

State of ___________, County of ___________
Subscribed and sworn before me on __________ by ______________________.

_______________________________
Notary Public — Commission Expires: __________
```

## Guidelines

- **Verify statutory form** — CA, NY, TX, FL and others have mandatory or model forms; use or adapt as required `[VERIFY each state]`
- **HIPAA gap** — an HCPOA without explicit HIPAA language may be rejected by providers; always include Article 6
- **Co-agent conflicts** — if co-agents appointed, specify joint vs. independent authority and deadlock resolution
- **Provider immunity** — note state good-faith immunity provisions to aid provider acceptance
- **Organ donation** — some states require a separate anatomical gift form; confirm whether HCPOA alone suffices `[VERIFY]`
- **Comfort care** — do not include provisions barring palliative care where prohibited by state law
- **Distribution** — recommend principal retain original; copies to agent, primary physician, and hospital of choice
- **Do not fabricate** statutory citations or execution requirements; mark uncertain references `[VERIFY]`
- **Attorney review required** — include disclaimer that document requires attorney review before execution
