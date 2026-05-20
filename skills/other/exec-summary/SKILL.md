---
skill: exec-summary
description: Generate non-technical executive summary from technical notes
context: fork
arguments:
  - name: note
    description: Note title or path to summarise
    required: true
  - name: audience
    description: Target audience (optional - exec, manager, stakeholder)
    required: false
---

# /exec-summary Skill

Generate a non-technical executive summary from technical ADRs, Pages, or Project notes.

## Purpose

Translate technical architecture content for non-technical stakeholders. Useful for:
- Board presentations
- Stakeholder updates
- Management briefings
- Cross-team communication

## Usage

```
/exec-summary "ADR - API Gateway Selection"
/exec-summary "Project - AIIncidentProcessor" exec
/exec-summary "Page - Kafka Integration" manager
```

## Instructions

1. **Read the source note** completely

2. **Identify the audience** (default: exec):
   - `exec` - C-suite, board level (business impact, risk, cost)
   - `manager` - Department heads (operational impact, timeline, resources)
   - `stakeholder` - Project stakeholders (what changes, how affects them)

3. **Extract key information**:

   **For ADRs:**
   - What decision was made (one sentence)
   - Why it matters to the business
   - What it costs / saves
   - Key risks and mitigations
   - Timeline / when it takes effect

   **For Projects:**
   - What the project delivers
   - Business benefit
   - Current status (RAG)
   - Key milestones
   - Resources / budget

   **For Pages:**
   - What this document describes
   - Why it matters
   - Key takeaways
   - Actions required (if any)

4. **Generate summary** using this template:

```markdown
# Executive Summary: {{Title}}

**Generated:** {{date}}
**Source:** [[{{source note}}]]
**Audience:** {{audience}}

---

## One-Line Summary

{{Single sentence explaining what this is about in business terms}}

## Why This Matters

{{2-3 sentences on business impact - avoid technical jargon}}

## Key Points

- {{Point 1 - business language}}
- {{Point 2 - business language}}
- {{Point 3 - business language}}

## Impact

| Area | Impact |
|------|--------|
| **Cost** | {{cost impact or "No direct cost impact"}} |
| **Timeline** | {{when does this happen}} |
| **Risk** | {{key risk in plain language}} |
| **Benefit** | {{main business benefit}} |

## Recommendation / Decision

{{What was decided or what action is recommended - one paragraph}}

## Questions This Answers

- {{Question a stakeholder might ask}}
- {{Another likely question}}

---

*This summary was generated from technical documentation. For full details, see [[{{source note}}]].*
```

5. **Translation rules** (technical → business language):

| Technical Term | Business Translation |
|----------------|---------------------|
| API | System connection / interface |
| Database | Data storage |
| Cloud | Online infrastructure |
| Microservices | Modular system design |
| Latency | Response time / speed |
| Scalability | Ability to grow |
| Redundancy | Backup systems |
| Migration | System move / upgrade |
| Integration | Connecting systems |
| Authentication | Security / login |
| Encryption | Data protection |
| AI/ML | Automated intelligence |
| DevOps | Delivery automation |
| Kubernetes | Container management |
| Kafka | Message system |

6. **Tone guidelines**:
   - Active voice ("We will..." not "It has been decided...")
   - Short sentences (max 20 words)
   - No acronyms without explanation
   - Focus on outcomes, not process
   - Quantify where possible (£, %, dates)

## Example Output

**Input:** `/exec-summary "ADR - Use PostgreSQL for Customer Data"`

**Output:**

```markdown
# Executive Summary: Database Selection for Customer Services

**Generated:** 2026-01-11
**Source:** [[ADR - Use PostgreSQL for Customer Data]]
**Audience:** Executive

---

## One-Line Summary

We're using PostgreSQL as our database for all customer transaction records in the new cloud system.

## Why This Matters

This decision affects how we store and protect customer payment data. PostgreSQL provides the financial-grade security we need while reducing our monthly infrastructure costs by approximately £700 compared to alternatives.

## Key Points

- Customer transaction data will be stored securely with bank-level protection
- Our team already has the skills to manage this system (no additional training needed)
- We can scale to handle 10 million records in the first year without changes

## Impact

| Area | Impact |
|------|--------|
| **Cost** | £2,400/month (£700 saving vs alternative) |
| **Timeline** | Implementation begins Q2 2026 |
| **Risk** | Low - proven technology, team expertise |
| **Benefit** | Secure, cost-effective data storage |

## Recommendation / Decision

Use PostgreSQL on AWS for all customer-facing transaction data. This gives us the security guarantees we need for financial data while leveraging existing team skills and keeping costs competitive.

## Questions This Answers

- How are we protecting customer payment data?
- What's the cost of the new database system?
- Do we have the skills to support this?

---

*This summary was generated from technical documentation. For full details, see [[ADR - Use PostgreSQL for Customer Data]].*
```

## Multiple Notes

To summarise multiple related notes:

```
/exec-summary "Project - Cloud Migration" with-adrs
```

This will:
1. Read the project note
2. Find all linked ADRs
3. Generate a combined executive summary

## Output Location

By default, outputs to conversation. To save as a note:

```
/exec-summary "ADR - API Gateway" --save
```

Creates: `Page - Executive Summary - API Gateway.md`
