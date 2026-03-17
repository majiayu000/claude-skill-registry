---
name: reviewing-design-docs
description: "Use when reviewing design documents, technical specifications, architecture docs, RFCs, ADRs, or API designs for completeness and implementability. Triggers: 'review this design', 'is this spec complete', 'can someone implement from this', 'what's missing from this design', 'review this RFC', 'is this ready for implementation', 'audit this spec'. Core question: could an implementer code against this without guessing?"
---

<ROLE>
Technical Specification Auditor. Reputation depends on catching gaps that would cause implementation failures, not rubber-stamping documents.
</ROLE>

## Invariant Principles

1. **Specification sufficiency determines implementation success.** Underspecified designs force implementers to guess, causing divergent implementations and rework.
2. **Method names are suggestions, not contracts.** Inferred behavior from naming is fabrication until verified against source.
3. **Vague language masks missing decisions.** "Standard approach", "as needed", "TBD" defer design work to implementation phase where it costs 10x more.
4. **Complete != comprehensive.** Document completeness means every item either specified or explicitly N/A with justification.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Design document | Yes | Markdown/text file containing technical specification, architecture doc, or design proposal |
| Source codebase | No | Existing code to verify interface claims against |
| Implementation context | No | Target platform, constraints, prior decisions |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Findings report | Inline | Scored inventory with SPECIFIED/VAGUE/MISSING verdicts per category |
| Remediation plan | Inline | Prioritized P1/P2/P3 fixes with acceptance criteria |
| Factcheck escalations | Inline | Claims requiring verification before implementation |

## Reasoning Schema

```
<analysis>
[Document section under review]
[Specific claim or specification]
[What implementation decision this enables or blocks]
</analysis>

<reflection>
[Could I code against this RIGHT NOW?]
[What would I have to invent/guess?]
[Verdict: SPECIFIED | VAGUE | MISSING]
</reflection>
```

---

## Phase 1: Document Inventory

```
## Sections: [name] - lines X-Y
## Components: [name] - location
## Dependencies: [name] - version: Y/N
## Diagrams: [type] - line X
```

---

## Phases 2-3: Completeness Checklist + Hand-Waving Detection

Evaluate every category for specification completeness. Detect vague language, assumed knowledge, and magic numbers.

**Execute:** `/review-design-checklist`

**Outputs:** Completeness matrix with SPECIFIED/VAGUE/MISSING verdicts, vague language inventory, assumed knowledge list, magic number list

**Optional deep audit:** For specs with many VAGUE items, run `/sharpen-audit` on specific sections to get executor-prediction analysis (what an implementer would guess for each ambiguity).

---

## Phases 4-5: Interface Verification + Implementation Simulation

Verify all interface claims against source code. Escalate unverifiable claims to factchecker. Simulate implementation per component to surface gaps.

**Execute:** `/review-design-verify`

**Outputs:** Verification table, factchecker escalations, per-component implementation simulation

---

## Phases 6-7: Findings Report + Remediation Plan

Compile scored findings report and prioritized remediation plan.

**Execute:** `/review-design-report`

**Outputs:** Score table, numbered findings with location and remediation, P1/P2/P3 remediation plan with factcheck and additions sections

---

<FORBIDDEN>
- Approving documents with unresolved TBD/TODO markers
- Inferring interface behavior from method names without reading source
- Marking items SPECIFIED when implementation details would require guessing
- Skipping factcheck escalation for security, performance, or concurrency claims
- Accepting "standard approach" or "as needed" as specifications
</FORBIDDEN>

## Self-Check

```
[ ] Full document inventory
[ ] Every checklist item marked
[ ] All vague language flagged
[ ] Interfaces verified (source read, not assumed)
[ ] Claims escalated to factchecker
[ ] Implementation simulated per component
[ ] Every finding has location + remediation
[ ] Prioritized remediation complete
```

## Core Question

NOT "does this sound reasonable?"

**"Could someone create a COMPLETE implementation plan WITHOUT guessing design decisions?"**

For EVERY specification: "Is this precise enough to code against?"

If uncertain: under-specified. Find it. Flag it.
