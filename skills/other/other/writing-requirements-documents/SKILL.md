---
name: writing-requirements-documents
description: Use when creating requirements documents or PRDs - ensures Obsidian block anchors, wiki links for traceability, and citation-manager validation for link integrity
---

# Writing Requirements Documents

Create PRDs with Obsidian-native linking (block anchors + wiki links) and mandatory link validation.

## When to Use

Use this skill when:
- Creating new PRD (Product Requirements Document)
- Writing functional/non-functional requirements
- Adding acceptance criteria that need traceability
- Any requirements documentation needing cross-references

**Do NOT use** for:
- Simple feature descriptions without formal requirements
- Informal notes or brainstorming docs
- Documentation that doesn't need traceability

## Quick Reference

| Element | ID Format | Block Anchor | Internal Link Example |
|---------|-----------|--------------|-------------------|
| Functional Requirement | FR1, FR2... | `^FR1` | `[[#^FR1\|FR1]]` |
| Non-Functional Requirement | NFR1, NFR2... | `^NFR1` | `[[#^NFR1\|NFR1]]` |
| Acceptance Criteria (in Sequencing docs) | AC1, AC2... | `^AC1` | `[[#^AC1\|AC1]]` with `([[#^FR1\|FR1]])` traceability |
| Draft AC (in whiteboards) | AC-draft-1... | `^AC-draft-1` | Promoted to `^AC1` in Sequencing phase |

**Link Types:**
- **Internal wiki link to block anchor**: `[[#^FR1|FR1]]` - For requirements/ACs
- **Internal wiki link to header**: `[[#Requirements|Requirements]]` - For sections
- **Internal markdown link**: `[Requirements](#requirements)` - Alternative for headers
- **Cross-document link**: `[Architecture](../design-docs/Architecture.md)` - Always use markdown syntax

## Core Principles

### 1. Every Requirement Needs a Block Anchor

**Why:** Block anchors enable precise linking within Obsidian. Without them, you cannot create reliable cross-references.

**Format:**

```markdown
- FR1: The system SHALL detect the Claude Code version from the binary. ^FR1
- NFR1: The system should follow Single Responsibility Principle. ^NFR1
```

**NOT this:**

```markdown
- REQ-F1: The system shall detect version.
```

### 2. Use Wiki Links for Internal References, Markdown Links for Cross-Document

**Internal references (same document):** Use wiki links with block anchors
**Cross-document references:** Use markdown links with file paths

**Internal Format:**

```markdown
*Functional Requirements*: [[#^FR1|FR1]], [[#^FR2|FR2]], [[#^FR3|FR3]]
*Non-Functional Requirements*: [[#^NFR5|NFR5]], [[#^NFR7|NFR7]]
```

**Cross-Document Format:**

```markdown
*Related Design*: [ARCHITECTURE-PRINCIPLES.md](../../../ARCHITECTURE-PRINCIPLES.md)
*Implementation Guide*: [Setup Guide](./guides/setup.md#installation)
```

**NOT this:**

```markdown
Related Requirements: REQ-F1, REQ-NF1  <!-- Plain text, not clickable -->
```

### 3. Use RFC 2119 Keywords in Requirements

**Mandatory requirements:** SHALL, SHALL NOT, REQUIRED
**Recommended:** SHOULD, SHOULD NOT, RECOMMENDED
**Optional:** MAY, OPTIONAL

**Example:**

```markdown
- FR1: The system SHALL validate all citations before commit. ^FR1
- FR2: The system SHOULD provide warnings for missing metadata. ^FR2
- FR3: The system MAY cache validation results for performance. ^FR3
```

### 4. Follow JTBD → FR → AC Layering

**Conceptual model source:** `.claude/agents/product-manager.md` (Requirements Pipeline section)

Requirements follow a three-layer structure that progresses from motivation to specification to verification:

**JTBD (Job To Be Done) — Why:**
- Captured in **Overview/Business Value** section of PRD
- Explains user needs and business outcomes
- No block anchors needed (contextual, not referenced)

**FR (Functional Requirement) — What:**
- Listed in **Requirements** section with block anchors: `^FR1`, `^FR2`
- Outcome-oriented and testable
- NOT implementation details

**Success Criteria — How you'll know the feature works:**
- Already exists in PRD **Overview** section
- High-level, outcome-focused verification
- NOT the same as detailed Acceptance Criteria

**Acceptance Criteria (AC) — Detailed test conditions:**
- **Do NOT belong in PRD** — emerge during Design/Sequencing phases
- During whiteboarding, capture draft ACs as `^AC-draft-1`, `^AC-draft-2`
- Formalized in **Sequencing Document** with `^AC1`, `^AC2` anchors
- Each AC must trace back to an FR: `([[#^FR1|FR1]])`
- ACs become literal test cases during Implementation phase

**Why this matters:** PRDs are high-level and generic. Detailed, testable ACs require system context that only exists after Design. Don't force premature precision.

### 5. Reference Template PRD

Before writing, use citation-manager to extract template sections:

```bash
# Extract Requirements section
npm run citation:extract:header /path/to/template-prd.md -- "Requirements"

# Extract Acceptance Criteria
npm run citation:extract:header /path/to/template-prd.md -- "Acceptance Criteria"
```

**Template Source:** `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/cc-workflows/tools/citation-manager/design-docs/features/20251119-type-contract-restoration/typescript-migration-prd.md`

## PRD Document Structure

A PRD follows this section structure:

```text
- Overview (Business Value, Success Criteria)
- Scope (In Scope / Out of Scope)
- Requirements (FR + NFR with block anchors)
- Non-Goals
- Dependencies (Technical, Knowledge, Process)
- Risks & Mitigations
- Acceptance Criteria (with block anchors)
- References (Context Docs, Architecture Standards, Technical Baseline)
```

### Overview Section

```markdown
## Overview

[1-2 sentence description of what this PRD covers and why.]

### Business Value

- **[Category]**: [Concrete benefit]
- **[Category]**: [Concrete benefit]

### Success Criteria

**Done when:**
- [Measurable criterion 1]
- [Measurable criterion 2]
- [Measurable criterion 3]
```

**Token-efficient Overview guidance:**
- Overview = WHAT + WHY (outcomes), never HOW (implementation)
- Keep capability descriptions ("enables pattern detection")
- Remove mechanism details ("via deterministic hooks") → belongs in Design
- "Done when" not "Port complete when" — simpler language

### Scope Section

```markdown
## Scope

### In Scope

**[Category]:**
- [Specific deliverable or activity]
- [Specific deliverable or activity]

### Out of Scope

- [Explicitly excluded item] — [Phase if deferred]
- [Explicitly excluded item]
```

**Out of Scope format:**
- Pattern: `<item> — <phase>` (terse)
- Write `/evolve — Phase A.2` not "deferred to Phase A.2"
- Don't repeat terms already evident from item name

### Requirements Section

```markdown
## Requirements

### Functional Requirements

- FR1: The system SHALL [specific, testable action]. ^FR1
- FR2: The system SHALL [another requirement]. ^FR2

### Non-Functional Requirements

#### Quality Requirements

- NFR1: The system SHALL NOT [constraint]. ^NFR1
- NFR2: [Quality attribute] SHALL [measurable target]. ^NFR2

#### Maintainability Requirements

- NFR3: [Maintainability requirement]. ^NFR3

#### Process Requirements

- NFR4: [Process constraint or workflow requirement]. ^NFR4
```

### Non-Goals Section

```markdown
## Non-Goals

Explicitly **out of scope** for this effort:

- **[Category]**: [Why this is excluded]
- **[Category]**: [Why this is excluded]
```

### Dependencies Section

```markdown
## Dependencies

### Technical Dependencies

- [Technology/tool and version requirement]
- [Existing infrastructure dependency]

### Knowledge Dependencies

- [Documentation or expertise needed]
- [Understanding of existing systems]

### Process Dependencies

- [Workflow or process requirement]
- [Team or organizational dependency]
```

### Risks & Mitigations Section

```markdown
## Risks and Mitigations

### Risk 1: [Risk Title]
**Impact**: [What happens if this risk materializes]
**Mitigation**: [How to prevent or address it]

### Risk 2: [Risk Title]
**Impact**: [What happens if this risk materializes]
**Mitigation**: [How to prevent or address it]
```

**Note:** PRDs do NOT include detailed Acceptance Criteria sections. The **Success Criteria** in the Overview section serves as the high-level completion criteria. Detailed, testable ACs emerge during the Design/Sequencing phase when system context is available.

### References Section

```markdown
## References

### Context Documents

- **[Doc Name]**: [link](path/to/doc.md) - [Brief description]

### Architecture Standards

- **[Principle Name]**: [link](path/to/ARCHITECTURE-PRINCIPLES.md#Section) - [Why relevant]

### Technical Baseline

- **[Baseline Name]**: [Commit hash or version] - [What it represents]
```

**References guidance:**
- Link synthesized artifacts only (whiteboards, design docs)
- Don't link raw research (agent outputs, session transcripts)
- Raw research is working material; PRD references curated artifacts
- "Traceability" means tracing to synthesis, not raw dumps — whiteboard already traces decisions
- If reviewer asks for "sources", point to whiteboard (which cites raw research internally)

## Mandatory Validation Checklist

After writing requirements documentation, create TodoWrite todos for:

1. ☐ Verify every requirement has block anchor
2. ☐ Verify every acceptance criterion has block anchor
3. ☐ Verify all cross-references use wiki link syntax
4. ☐ Run `npm run citation:validate <file-path>`
5. ☐ Fix any broken links reported by citation-manager
6. ☐ Re-run validation until zero errors

**You MUST run citation-manager validate as the final step.** This is non-negotiable.

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Plain text IDs (REQ-F1) | Not clickable, breaks navigation | Use `[[#^FR1\|FR1]]` |
| Missing block anchors | Cannot create precise links | Add `^FR1` at end of line |
| "Portability" rationalization | We use Obsidian for linked docs | Wiki links are our standard |
| Skipping validation | Broken links in docs | Run citation-manager validate |
| Wrong ID format (REQ-F1) | Inconsistent with templates | Use FR1, NFR1, AC1 |
| Missing Non-Goals section | Scope creep without boundaries | Always document what's excluded |
| Requirements without categories | Hard to navigate large PRDs | Group NFRs by Quality, Maintainability, Process |
| ACs in PRD instead of Sequencing | Violates progressive disclosure | PRD gets Success Criteria; ACs formalize in Sequencing |
| ACs without FR traceability | Can't verify which requirement is satisfied | Add `([[#^FR1\|FR1]])` to each AC |
| Implementation details in Overview | Overview = WHAT/WHY, not HOW | Move mechanisms to Design doc |
| Verbose Out of Scope ("deferred to Phase A.2") | Wastes tokens, harder to scan | Use `— Phase A.2` format |
| Linking raw research (agent outputs) | Working material, not curated | Link synthesized artifacts only |

## Red Flags

🚩 Requirements without block anchors
🚩 Cross-references as plain text
🚩 "I'll validate the links manually"
🚩 "Block anchors are extra work"
🚩 "Plain text is more portable"
🚩 Skipping citation-manager validate step
🚩 Using inconsistent ID formats
🚩 Missing Non-Goals or Scope sections
🚩 Detailed acceptance criteria in PRD (use Success Criteria instead)
🚩 Acceptance criteria without FR traceability links
🚩 Implementation mechanisms in Overview (hooks, APIs, technologies)
🚩 Verbose Out of Scope items ("deferred to", redundant descriptions)
🚩 Raw research artifacts in References (agent outputs, session transcripts)

## Common Rationalizations (And Why They're Wrong)

| Rationalization | Why You Might Think This | The Truth |
|----------------|--------------------------|-----------|
| "Plain text IDs are more portable for export to Word/PDF" | Requirements docs often get exported | We use Obsidian specifically for linked documentation. Portability is not our goal—traceability is. |
| "Easier to reference REQ-F1 in conversations" | Plain text feels simpler | Wiki links display as text (FR1) but provide navigation. No conversation difference, huge usability gain. |
| "This follows professional standards" | Generic requirements patterns | Professional ≠ Obsidian-optimized. We have specific standards for our workflow. |
| "I can validate links manually or write a script" | Automation seems unnecessary | We already have citation-manager. Use it. Manual validation is error-prone. |
| "Block anchors aren't necessary for simple docs" | Only complex docs need anchors | Every requirement needs traceability from day one. "Simple" docs become complex. |
| "I'll add the anchors and links later" | Focus on content first | Never happens. Add them now or they'll be missing forever. |
| "Non-Goals aren't needed for small PRDs" | Seems like overhead | Non-Goals prevent scope creep. Even small PRDs benefit from explicit boundaries. |
| "Implementation details help understanding" | Context feels helpful | Overview = WHAT/WHY only. HOW belongs in Design doc. Readers scan for outcomes, not mechanisms. |
| "Verbose Out of Scope is clearer" | More words = more clarity | Terse is scannable. `— Phase A.2` conveys same info as "deferred to Phase A.2". |
| "Raw research links show my work" | Transparency is good | PRDs reference curated artifacts. Working materials (agent outputs) clutter the doc. |

## Example: Before vs After

### Before (Wrong)

```markdown
## Requirements

**REQ-F1:** System shall export to JSON.

Related: See acceptance criteria in appendix.
```

### After (Correct)

```markdown
## Requirements

### Functional Requirements

- FR1: The system SHALL export validation reports to JSON format. ^FR1

## Acceptance Criteria

1. **Export**: JSON output matches documented schema. ^AC1

*Functional Requirements*: [[#^FR1|FR1]]
```

## Integration with Other Tools

- **After brainstorming**: Use this skill to formalize design into PRD requirements
- **Before writing-plans**: PRD requirements feed into implementation plans
- **With citation-manager**: Always validate links before committing

---

**Remember:** If you catch yourself thinking "anchors are tedious" or "I'll add links later" — STOP. Those are rationalizations. Block anchors and wiki links are mandatory, not optional.
