---
name: document-writer
description: Expert in creating technical documentation, architectural decision records (ADRs), and RFCs. Specializes in structured knowledge management and system documentation. Use when writing technical docs, ADRs, RFCs, or system design documents.
---

# Document Writer

## Purpose
Provides expertise in creating structured technical documentation for software systems. Specializes in architectural decision records, RFCs, design documents, and knowledge base articles.

## When to Use
- Writing architectural decision records (ADRs)
- Creating RFC (Request for Comments) documents
- Documenting system designs
- Writing technical specifications
- Creating runbooks and playbooks
- Building internal knowledge bases
- Documenting incidents (post-mortems)

## Quick Start
**Invoke this skill when:**
- Writing architectural decision records (ADRs)
- Creating RFC documents
- Documenting system designs
- Writing technical specifications
- Creating runbooks and playbooks

**Do NOT invoke when:**
- Writing API documentation (use api-documenter)
- Writing user-facing docs (use technical-writer)
- Creating Word documents (use docx-skill)
- Writing marketing content (use content-marketer)

## Decision Framework
```
Document Type Selection:
├── Decision needed → ADR
├── Proposal for review → RFC
├── System explanation → Design doc
├── How to operate → Runbook
├── Incident occurred → Post-mortem
├── Process definition → SOP
└── Knowledge capture → Wiki article
```

## Core Workflows

### 1. ADR Creation
1. Identify decision to be made
2. List context and constraints
3. Enumerate options considered
4. Analyze pros and cons
5. State decision and rationale
6. Document consequences
7. Get stakeholder review

### 2. RFC Process
1. Write problem statement
2. Propose solution approach
3. Detail implementation plan
4. Address risks and mitigations
5. Define success metrics
6. Open for comments
7. Iterate based on feedback
8. Move to accepted/rejected

### 3. Design Document
1. State purpose and scope
2. Describe current state
3. Present proposed design
4. Include diagrams (C4, sequence)
5. Address non-functional requirements
6. List alternatives considered
7. Define rollout plan

## Best Practices
- Use templates for consistency
- Include diagrams for complex systems
- Write for the reader, not yourself
- Keep documents updated
- Link related documents
- Version control all documentation

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| No template | Inconsistent docs | Use standard templates |
| Write-only docs | Never updated | Schedule reviews |
| Missing context | Readers confused | Include background |
| Too verbose | Nobody reads | Be concise, link details |
| Undiscoverable | Docs go unused | Organize and index |
