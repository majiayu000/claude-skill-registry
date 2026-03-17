---
name: requirement-summarizer
description: Extract and summarize core features, constraints, and priorities from requirement documents. Use when analyzing PRDs, RFCs, business requirements, user stories, epics, or any requirement documentation to identify must-have features, technical constraints, priority levels (P0/P1/P2/MoSCoW), and key decision points. Triggers when users ask to summarize, analyze, extract, or understand requirements from documents.
---

# Requirement Summarizer

## Overview

Extract and organize the essential information from requirement documents into a structured markdown summary that highlights core features, constraints, and priorities.

## Workflow

Follow these steps to summarize requirement documents:

### 1. Read and Understand the Document

First, read the entire requirement document to understand its structure and content:

- Identify document type (PRD, RFC, user story, business requirement, etc.)
- Note any existing structure (sections, headers, numbering)
- Understand the context and scope of the requirements

### 2. Extract Key Information

Systematically identify and extract:

**Core Features:**
- Main functionality being proposed or required
- User-facing capabilities
- System behaviors and interactions
- Integration points with other systems

**Constraints:**
- Technical limitations or requirements
- Business constraints (budget, timeline, resources)
- Regulatory or compliance requirements
- Compatibility or platform constraints
- Security or privacy requirements
- Performance requirements (latency, throughput, scalability)

**Priorities:**
- Explicit priority labels (P0, P1, P2, Critical, High, Medium, Low)
- MoSCoW categorization (Must have, Should have, Could have, Won't have)
- MVP vs future phases
- Required vs optional features
- Blocking vs non-blocking items

### 3. Generate Structured Summary

Create a markdown report with the following structure:

```markdown
# Requirements Summary: [Document Name]

## Document Metadata
- **Source**: [Document title/filename]
- **Type**: [PRD/RFC/User Story/Business Requirement/etc.]
- **Date Analyzed**: [Current date]

## Executive Summary
[2-3 sentence overview of what this requirement document defines]

## Core Features

### [Feature Category 1]
- **[Feature Name]**: [Brief description]
  - Priority: [P0/P1/P2 or Must/Should/Could]
  - Notes: [Any relevant context]

### [Feature Category 2]
...

## Constraints

### Technical Constraints
- [Constraint description]
- [Constraint description]

### Business Constraints
- [Constraint description]
- [Constraint description]

### Compliance/Regulatory Constraints
- [Constraint description]

### Performance Constraints
- [Constraint description]

## Priority Breakdown

### Critical/Must-Have (P0)
1. [Feature/requirement]
2. [Feature/requirement]

### High Priority/Should-Have (P1)
1. [Feature/requirement]
2. [Feature/requirement]

### Medium Priority/Could-Have (P2)
1. [Feature/requirement]
2. [Feature/requirement]

### Future/Won't-Have (P3)
1. [Feature/requirement]

## Key Decisions & Open Questions
- **Decision**: [What needs to be decided]
  - Options: [If applicable]
  - Impact: [Why this matters]

- **Open Question**: [Unclear requirement or missing information]

## Success Criteria
[How will we know this is successful? Metrics, acceptance criteria, or outcomes]

## Dependencies
- [External dependencies or prerequisites]
- [Related systems or teams]

## Timeline & Milestones
- [Key dates if mentioned in requirements]
- [Phase breakdown if applicable]
```

### 4. Quality Checks

Before presenting the summary, verify:

- **Completeness**: All major features, constraints, and priorities captured
- **Clarity**: Each item is clearly described without ambiguity
- **Accuracy**: Information faithfully represents the source document
- **Organization**: Related items grouped logically
- **Priorities**: Priority levels are consistently applied
- **Actionability**: Summary provides clear understanding of what needs to be built

### 5. Handle Edge Cases

**Multiple conflicting priorities:**
- Note conflicts in "Key Decisions & Open Questions"
- Flag for stakeholder clarification

**Implicit vs explicit priorities:**
- If priorities aren't explicitly stated, infer from context (deadline pressure, business value, user impact)
- Mark inferred priorities with "(inferred)" notation

**Vague or ambiguous requirements:**
- Capture them in "Open Questions"
- Suggest clarifying questions

**Missing information:**
- Note gaps in "Open Questions"
- Highlight critical missing details

## Best Practices

**Be concise but comprehensive:**
- Capture essential details without copying entire paragraphs
- Use bullet points for scanability
- Link back to specific sections of source document if helpful

**Maintain objectivity:**
- Extract what's written, not what should be written
- Flag concerns or gaps but don't rewrite requirements

**Prioritize based on evidence:**
- Use explicit priority markers from the document
- When inferring, base on business value, user impact, dependencies, and timeline

**Adapt to document type:**
- **PRDs/RFCs**: Focus on technical details, system design, and architecture constraints
- **Business requirements**: Emphasize business value, ROI, stakeholder needs
- **User stories**: Extract acceptance criteria, user journeys, and UX requirements
- **Epics**: Break down into constituent stories and themes

**Handle different priority systems:**
- P0/P1/P2/P3 (common in tech)
- Critical/High/Medium/Low
- MoSCoW (Must/Should/Could/Won't)
- Phase 1/2/3 or MVP/Future
- Convert between systems when helpful for clarity

## Example Usage

**User request:**
> "Summarize the requirements from this PRD and identify what's critical for the first release"

**Response approach:**
1. Read the PRD document
2. Extract all features, noting which are marked for MVP/Phase 1
3. Identify technical and business constraints
4. Map explicit and implicit priorities
5. Generate structured markdown summary
6. Highlight critical items for first release in Priority Breakdown section

**User request:**
> "What are the main features and constraints in these user stories?"

**Response approach:**
1. Read all user stories
2. Group related stories by feature theme
3. Extract acceptance criteria as feature details
4. Identify technical constraints from story details
5. Note priorities if labeled (or infer from sprint assignment)
6. Generate summary organized by feature theme

## Tips for Effective Summarization

- **Look for patterns**: Similar requirements may be scattered; group them logically
- **Read between the lines**: Performance needs, security concerns may be implicit
- **Note what's missing**: Gaps in requirements are as important as what's present
- **Preserve traceability**: Link summary items back to source sections when possible
- **Stay neutral**: Don't judge requirement quality, just extract and organize
- **Be specific**: "Fast API response" → "API response time < 200ms"
