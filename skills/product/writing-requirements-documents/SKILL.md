---
name: writing-requirements-documents
description: Use when creating requirements documents, PRDs, or epics with user stories - ensures Obsidian block anchors, wiki links for traceability, and citation-manager validation for link integrity
---

# Writing Requirements Documents

Create requirements documents with Obsidian-native linking (block anchors + wiki links) and mandatory link validation.

## When to Use

Use this skill when:
- Creating new PRD (Product Requirements Document)
- Writing functional/non-functional requirements
- Documenting epics with user stories
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
| Epic (header-based) | Epic 1, Epic 2... | None | `[[#Epic 1 - Name\|Epic 1]]` |
| User Story (header-based) | Story 1.1, 1.2... | None | `[[#Story 1.1 Title\|Story 1.1]]` |
| Acceptance Criteria | AC within story | `^US1-1AC1` | `[[#^US1-1AC1\|AC1]]` |

**Link Types:**
- **Internal wiki link to block anchor**: `[[#^FR1|FR1]]` - For requirements/ACs
- **Internal wiki link to header**: `[[#Story 1.1 Title|Story 1.1]]` - For epics/stories
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

### 4. Reference Template PRD

Before writing, use citation-manager to extract template sections:

```bash
# Extract Requirements section
npm run citation:extract:header /path/to/template-prd.md -- "Requirements"

# Extract Epic with user stories
npm run citation:extract:header /path/to/template-prd.md -- "Epic 1"
```

**Template Source:** `/Users/wesleyfrederick/Documents/ObsidianVaultNew/0_SoftwareDevelopment/claude-code-knowledgebase/design-docs/features/version-based-analysis/version-based-analysis-prd.md`

## Document Structure

### Requirements Section

```markdown
## Requirements

### Functional Requirements

- FR1: The system SHALL [specific, testable action]. ^FR1
- FR2: The system SHALL [another requirement]. ^FR2

### Non-Functional Requirements

- NFR1: [Quality attribute like performance, security]. ^NFR1
- NFR2: [Maintainability, scalability requirement]. ^NFR2
```

### Epic with User Stories

```markdown
## Epic 1 - [Epic Name]

[Epic description and business value]

### Story 1.1: [Story Title]

**As a** [role],
**I want** [capability],
**so that** [business value].

#### Acceptance Criteria

1. WHEN [condition], THEN the system SHALL [expected behavior]. ^US1-1AC1
2. IF [condition], THEN the system shall [behavior]. ^US1-1AC2

*Depends On*: None
*Functional Requirements*: [[#^FR1|FR1]], [[#^FR2|FR2]]
*Non-Functional Requirements*: [[#^NFR1|NFR1]]
```

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
| Wrong ID format (REQ-F1) | Inconsistent with templates | Use FR1, NFR1, US1.1 |

## Red Flags

🚩 Requirements without block anchors
🚩 Cross-references as plain text
🚩 "I'll validate the links manually"
🚩 "Block anchors are extra work"
🚩 "Plain text is more portable"
🚩 Skipping citation-manager validate step
🚩 Using inconsistent ID formats

## Common Rationalizations (And Why They're Wrong)

| Rationalization | Why You Might Think This | The Truth |
|----------------|--------------------------|-----------|
| "Plain text IDs are more portable for export to Word/PDF" | Requirements docs often get exported | We use Obsidian specifically for linked documentation. Portability is not our goal—traceability is. |
| "Easier to reference REQ-F1 in conversations" | Plain text feels simpler | Wiki links display as text (FR1) but provide navigation. No conversation difference, huge usability gain. |
| "This follows professional agile standards" | Generic requirements patterns | Professional ≠ Obsidian-optimized. We have specific standards for our workflow. |
| "I can validate links manually or write a script" | Automation seems unnecessary | We already have citation-manager. Use it. Manual validation is error-prone. |
| "Block anchors aren't necessary for simple docs" | Only complex docs need anchors | Every requirement needs traceability from day one. "Simple" docs become complex. |
| "I'll add the anchors and links later" | Focus on content first | Never happens. Add them now or they'll be missing forever. |
| "Header links are good enough for stories" | Markdown links work | Yes! Headers can use `[[#Story 1.1 Title\|Story 1.1]]` or `[Story 1.1](#story-11-title)`. This is correct. |

## Example: Before vs After

### Before (Wrong)

```markdown
## Requirements

**REQ-F1:** System shall export to JSON.

Related User Stories: US-001
```

### After (Correct)

```markdown
## Requirements

### Functional Requirements

- FR1: The system SHALL export validation reports to JSON format. ^FR1

### User Story Reference

*Functional Requirements*: [[#^FR1|FR1]]
```

## Integration with Other Tools

- **After brainstorming**: Use this skill to formalize design into requirements
- **Before writing-plans**: Requirements feed into implementation plans
- **With citation-manager**: Always validate links before committing

---

**Remember:** If you catch yourself thinking "anchors are tedious" or "I'll add links later" — STOP. Those are rationalizations. Block anchors and wiki links are mandatory, not optional.
