---
name: nfr-review
skill: nfr-review
description: Review an existing HLD against NFR reference and generate gap report
context: fork
arguments:
  - name: system
    description: System name or Confluence page ID/URL of the HLD
    required: true
  - name: tier
    description: CS tier (CS1-CS4) — if omitted, skill will infer or ask
    required: false
  - name: output
    description: Output format — "vault" (creates Concept note, default), "confluence" (pushes to Confluence), "console" (prints to terminal)
    required: false
model: opus
---

# /nfr-review

Review an existing HLD from Confluence against the NFR YAML reference and generate a gap report with scoring and remediation recommendations. Uses parallel sub-agents for efficient analysis.

## Usage

```
/nfr-review ERPSystem
/nfr-review "AlertHub" CS1
/nfr-review 664765269 CS2 confluence
/nfr-review https://britishairways.atlassian.net/wiki/spaces/BDOC/pages/12345 CS2
```

## Data Source

NFR reference data: `.claude/data/nfr-reference.yaml` — single source of truth for all 66 NFRs.

## Scoring Rubric (0-3 Scale)

| Score | Rating              | Meaning                                                                                          |
|-------|---------------------|--------------------------------------------------------------------------------------------------|
| **3** | Explicitly Addressed | NFR requirement clearly documented with specific evidence, links, or implementation details      |
| **2** | Mentioned           | NFR topic discussed but lacking evidence, specifics, or measurable targets                       |
| **1** | Implied             | Related concept mentioned but NFR not explicitly addressed; may be inferred from context         |
| **0** | Not Covered         | NFR not mentioned at all; no evidence of consideration                                           |
| **N/A** | Not Applicable     | NFR section does not apply to this system (e.g., PCI for non-payment system)                    |

## Instructions

### Phase 1: Load NFR Reference

1. **Read** `.claude/data/nfr-reference.yaml`
2. Parse all 66 NFRs with their requirements, tier values, and evidence guidance
3. Note the section applicability matrix

### Phase 2: Fetch the HLD

1. **Resolve the system HLD** using Atlassian MCP tools:
   - If argument is a URL with `pageId`: extract ID and use `getConfluencePage`
   - If argument is a numeric ID: use `getConfluencePage` directly
   - If argument is a system name: search for "[System Name] HLD" or "High-Level Design" in Confluence
   - Search pattern: `searchConfluenceUsingCql` with `title ~ "[system] HLD" OR title ~ "[system] High-Level Design"`

2. **Read the full page content** including child pages if present:
   ```
   getConfluencePage with pageId
   getConfluencePageDescendants with pageId (check for child pages)
   ```

3. **Record metadata**: page title, space, author, last modified date

4. **Determine tier**: If tier argument not provided:
   - Search HLD content for tier references (CS1/CS2/CS3/CS4 or SL1/SL2/SL3/SL4)
   - If found, use it
   - If not found, ask the user

5. **Determine applicable sections**: Look for indicators of project type:
   - Payment/card/PCI references → include PCI section
   - Personal data/GDPR/DPIA references → include PRIV section
   - Aviation/ERPSystem/EWS/flight/airworthiness references → include CAA section
   - Always include: OE, SEC, DATA, CE, INT, REL, PERF, COST, SUS, COMP

### Phase 3: Parallel Analysis (Sub-agents)

Launch **3 parallel Sonnet sub-agents**, each reviewing different NFR sections:

**Agent 1 — Security, Privacy & Compliance:**

```
You are reviewing an HLD document against NFR requirements. Score each NFR on a 0-3 scale.

**System:** [system name]
**Tier:** [CS/SL tier]
**HLD Content:** [full page content]

**NFRs to Assess:**
[List all NFRs from sections: SEC, PRIV, COMP]

For each NFR:
1. Search the HLD for evidence that this requirement is addressed
2. Score 0-3 using the rubric (3=explicitly addressed with evidence, 2=mentioned without evidence, 1=implied, 0=not covered)
3. Quote the specific HLD text that provides evidence (or note absence)
4. Provide a remediation recommendation for any NFR scoring 0-1

Output format per NFR:
NFR_ID: [id]
SCORE: [0-3 or N/A]
EVIDENCE: "[quoted text from HLD or 'Not found']"
GAP: "[what's missing]"
RECOMMENDATION: "[specific remediation action]"
```

**Agent 2 — Reliability, Performance & Operational Excellence:**

```
[Same structure as Agent 1 but covering NFRs from sections: OE, REL, PERF]
```

**Agent 3 — Regulatory, Cost & Sustainability:**

```
[Same structure as Agent 1 but covering NFRs from sections: PCI (if applicable), CE, CAA (if applicable), DATA, INT, COST, SUS]
```

### Phase 4: Synthesise Results

1. **Collect all agent outputs** and merge into unified assessment
2. **Calculate scores:**
   - Per-NFR score (from agents)
   - Per-section average score
   - Overall average score (excluding N/A sections)
3. **Categorise gaps:**
   - **Critical gaps** (score 0): NFRs completely absent — highest remediation priority
   - **Partial coverage** (score 1-2): NFRs mentioned but incomplete — need evidence or specifics
   - **Fully addressed** (score 3): No action needed
4. **Rank remediation** by section criticality: Security > Reliability > Regulatory > Operations > Performance > Cost > Sustainability

### Phase 5: Generate Gap Report

Create the gap report using the template below.

**Default output:** Vault note at root directory as `Concept - NFR Gap Analysis - [System Name].md`

If `output` is `console`, print to terminal instead. If `output` is `confluence`, push as Confluence page.

## Output Template

```markdown
---
type: Concept
title: "NFR Gap Analysis - [System Name]"
created: [today]
modified: [today]
tags:
  - activity/evaluation
  - activity/architecture
  - activity/governance
  - domain/engineering
  - [technology tags from HLD]
  - [project tags if identifiable]
confidence: high
freshness: current
source: synthesis
verified: false
reviewed: [today]
keywords: [nfr, gap-analysis, nfr-review, [system-name lowercase]]
relatedTo:
  - "[[Pattern - NFR Standards and Governance]]"
  - "[[Concept - NFR Gap Analysis]]"
relatedTo: []
---

# NFR Gap Analysis: [System Name]

**Source HLD:** [Confluence URL or page title]
**Space:** [Confluence space]
**Last Modified:** [HLD last modified date]
**Review Date:** [today]
**System Tier:** [CS tier] / [SL tier]
**Applicable Sections:** [list of included sections]

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Overall Score** | X.X / 3.0 |
| **NFRs Assessed** | XX of 66 |
| **Fully Addressed (3)** | XX |
| **Mentioned (2)** | XX |
| **Implied (1)** | XX |
| **Not Covered (0)** | XX |
| **Not Applicable** | XX |
| **Critical Gaps** | XX NFRs not addressed |

## Section Scores

| Section | Score | Fully Addressed | Gaps | RAG |
|---------|-------|-----------------|------|-----|
| Operational Excellence (OE) | X.X/3.0 | X of 5 | [gap IDs] | [colour] |
| Security (SEC) | X.X/3.0 | X of 10 | [gap IDs] | [colour] |
| Privacy (PRIV) | X.X/3.0 | X of 8 | [gap IDs] | [colour] |
| Data Retention (DATA) | X.X/3.0 | X of 1 | [gap IDs] | [colour] |
| Compliance (COMP) | X.X/3.0 | X of 1 | [gap IDs] | [colour] |
| PCI DSS (PCI) | X.X/3.0 | X of 8 | [gap IDs] | [colour] |
| Cyber Essentials (CE) | X.X/3.0 | X of 6 | [gap IDs] | [colour] |
| CAA/NIS (CAA) | X.X/3.0 | X of 9 | [gap IDs] | [colour] |
| Interoperability (INT) | X.X/3.0 | X of 1 | [gap IDs] | [colour] |
| Reliability (REL) | X.X/3.0 | X of 6 | [gap IDs] | [colour] |
| Performance (PERF) | X.X/3.0 | X of 4 | [gap IDs] | [colour] |
| Cost (COST) | X.X/3.0 | X of 4 | [gap IDs] | [colour] |
| Sustainability (SUS) | X.X/3.0 | X of 3 | [gap IDs] | [colour] |

**RAG:** 🟢 2.5+ | 🟡 1.5-2.4 | 🔴 <1.5

---

## Critical Gaps (Score 0)

NFRs completely absent from the HLD — require immediate attention.

| NFR ID | Requirement | Section | Remediation |
|--------|------------|---------|-------------|
| [id] | [title] | [section] | [specific action to address] |

## Partial Coverage (Score 1-2)

NFRs mentioned but lacking evidence or specifics.

| NFR ID | Score | Requirement | Evidence Found | Gap | Remediation |
|--------|-------|------------|----------------|-----|-------------|
| [id] | [1-2] | [title] | "[quoted text]" | [what's missing] | [action] |

## Fully Addressed (Score 3)

NFRs with clear evidence in the HLD.

| NFR ID | Requirement | Evidence |
|--------|------------|---------|
| [id] | [title] | "[quoted text or summary]" |

---

## Remediation Priority

### Immediate (Security & Compliance Gaps)

1. [Specific remediation action with NFR ID]
2. ...

### Short-term (Reliability & Operations Gaps)

1. [Specific remediation action with NFR ID]
2. ...

### Medium-term (Performance & Cost Gaps)

1. [Specific remediation action with NFR ID]
2. ...

---

## Tier Compliance

For tiered NFRs, verify the HLD targets match the [SL tier] requirements:

| NFR ID | Expected ([SL tier]) | Found in HLD | Match |
|--------|---------------------|--------------|-------|
| [tiered NFR id] | [expected tier value] | [found value or "Not specified"] | [Yes/No/Partial] |

---

*Gap analysis generated by Claude Code /nfr-review skill against NFR reference v[version] ([source_page_id]). Scores reflect HLD document completeness, not implementation quality.*
```

## Post-Generation Actions

After generating the report, offer the user:

1. **Create Jira tickets** for critical gaps (score 0-1) — one ticket per gap with NFR requirement as acceptance criteria
2. **Generate remediation plan** — prioritised list of actions to close gaps
3. **Compare with previous review** — if a prior gap analysis note exists for this system, show progress

## Related

- `.claude/data/nfr-reference.yaml` — NFR single source of truth
- `.claude/skills/nfr-capture/SKILL.md` — Generate NFR tables for new HLDs
- `.claude/skills/confluence-review/SKILL.md` — General Confluence page review (8-dimension scoring)
- `Concept - NFR Gap Analysis` — Gap analysis methodology
- `Pattern - NFR Standards and Governance` — Tiered framework context
