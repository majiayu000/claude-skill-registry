---
skill: 'document-structure'
version: '2.0.0'
updated: '2025-12-31'
category: 'documentation'
complexity: 'foundational'
prerequisite_skills: []
composable_with: ['technical-writing', 'data-visualization', 'ai-terminology']
---

# Document Structure Skill

## Overview
This skill provides expertise in organizing complex technical documentation with clear hierarchies, logical flow, and intuitive navigation for R&D audiences. It ensures documents are scannable, navigable, and appropriately structured for their purpose and audience.

## Key Capabilities

### Information Architecture
- Create logical document hierarchies (H1-H6 heading structure)
- Organize content from high-level concepts to detailed implementations
- Group related topics and create clear content sections
- Design table of contents and navigation structures
- Implement progressive disclosure patterns
- Balance depth with readability

### Structural Thinking
- Identify document purpose and optimize structure accordingly
- Recognize when content needs splitting vs. consolidation
- Apply consistent patterns across document families
- Design for both sequential reading and random access

## Document Types and Structures

### Strategic Documents

| Document Type | Purpose | Typical Structure | Length |
|---------------|---------|-------------------|--------|
| Executive Summary | Quick decision support | Problem → Solution → Ask | 1-2 pages |
| Business Case | Investment justification | Context → Options → Recommendation | 5-10 pages |
| Roadmap | Strategic direction | Vision → Phases → Milestones | 3-5 pages |
| Assessment Report | Current state analysis | Findings → Analysis → Recommendations | 5-15 pages |

**Executive Summary Structure:**
```markdown
# [Title]

## Executive Summary
[2-3 paragraph overview - can stand alone]

## Current Situation
[Brief context setting]

## Recommended Action
[Clear recommendation]

## Expected Outcomes
[Quantified benefits]

## Request
[Specific ask: approval, resources, decision]
```

**Business Case Structure:**
```markdown
# Business Case: [Title]

## Executive Summary
## Problem Statement
## Proposed Solution
## Options Analysis
### Option 1: [Name]
### Option 2: [Name]
### Option 3: [Name]
## Recommendation
## Financial Analysis
## Risk Assessment
## Implementation Plan
## Appendices
```

### Technical Documents

| Document Type | Purpose | Typical Structure | Length |
|---------------|---------|-------------------|--------|
| Architecture Guide | System design | Overview → Components → Interactions | 10-30 pages |
| API Reference | Integration spec | Authentication → Endpoints → Errors | Varies |
| Implementation Guide | Setup instructions | Prerequisites → Steps → Verification | 5-15 pages |
| Runbook | Operational procedures | Trigger → Steps → Verification | 3-10 pages |

**Architecture Guide Structure:**
```markdown
# [System] Architecture

## Overview
### Purpose
### Scope
### Key Decisions

## System Context
[Where this fits in the larger ecosystem]

## Component Architecture
### Component 1
### Component 2
[...]

## Data Architecture
### Data Models
### Data Flow

## Integration Points
### External Systems
### APIs

## Security Architecture
## Deployment Architecture
## Appendices
```

**API Reference Structure:**
```markdown
# [API Name] Reference

## Overview
## Authentication
## Base URL and Versioning
## Request/Response Formats

## Endpoints

### [Resource] Endpoints
#### GET /resource
#### POST /resource
#### GET /resource/{id}
[...]

## Error Handling
### Error Codes
### Error Response Format

## Rate Limits
## SDKs and Examples
## Changelog
```

### Process Documents

| Document Type | Purpose | Typical Structure | Length |
|---------------|---------|-------------------|--------|
| Standard Operating Procedure | Consistent execution | Purpose → Steps → Verification | 2-5 pages |
| Decision Framework | Consistent decisions | Criteria → Process → Escalation | 3-5 pages |
| Workflow Guide | Process understanding | Overview → Steps → Exceptions | 5-10 pages |
| Checklist | Verification | Categories → Items → Signoff | 1-3 pages |

**SOP Structure:**
```markdown
# [Process Name] SOP

## Purpose
## Scope
## Roles and Responsibilities

## Prerequisites
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

## Procedure

### Step 1: [Action]
[Detailed instructions]

### Step 2: [Action]
[Detailed instructions]

[...]

## Verification
## Exception Handling
## Related Documents
## Revision History
```

### Reference Documents

| Document Type | Purpose | Typical Structure | Length |
|---------------|---------|-------------------|--------|
| Glossary | Term definitions | Alphabetical terms | 2-10 pages |
| FAQ | Common questions | Categorized Q&A | 3-10 pages |
| Configuration Reference | Setting options | Categorized settings | 5-20 pages |
| Quick Reference Card | At-a-glance info | Dense, visual | 1-2 pages |

## Structural Patterns

### Pattern 1: Getting Started Progression
Best for: Tutorials, onboarding, learning content

```markdown
1. Overview (What is it? Why care?)
2. Prerequisites (What do I need?)
3. Quick Start (Minimal viable first step)
4. Core Concepts (Essential understanding)
5. Step-by-Step Tutorial (Guided practice)
6. Common Issues & Troubleshooting (When things go wrong)
7. Next Steps (Where to go from here)
```

### Pattern 2: Problem-Solution-Benefit
Best for: Proposals, recommendations, change requests

```markdown
1. Context & Need (Why are we here?)
2. Problem Statement (What's wrong?)
3. Proposed Solution (What do we do?)
4. Benefits (Why this solution?)
5. Alternatives Considered (What else we looked at)
6. Implementation (How do we do it?)
7. Success Criteria (How do we know it worked?)
```

### Pattern 3: Reference Hierarchy
Best for: Technical specifications, configuration guides

```markdown
1. Purpose & Scope
2. Quick Reference (Most common items)
3. Detailed Reference
   3.1 Category A
       3.1.1 Item 1
       3.1.2 Item 2
   3.2 Category B
       [...]
4. Examples
5. Related Resources
```

### Pattern 4: Decision Support
Best for: Comparison documents, evaluation frameworks

```markdown
1. Context & Decision Needed
2. Evaluation Criteria
3. Options Overview (Summary table)
4. Detailed Analysis
   4.1 Option 1: [Name]
   4.2 Option 2: [Name]
   [...]
5. Comparison Matrix
6. Recommendation
7. Implementation Path
```

### Pattern 5: Operational Runbook
Best for: Procedures, incident response, maintenance

```markdown
1. Purpose (When to use this runbook)
2. Prerequisites (Required access, tools)
3. Procedure
   3.1 Step 1 (with verification)
   3.2 Step 2 (with verification)
   [...]
4. Rollback Procedure
5. Troubleshooting
6. Escalation
```

## Heading Hierarchy Best Practices

### Level Usage

| Level | Use For | Example |
|-------|---------|---------|
| H1 | Document title only | `# API Integration Guide` |
| H2 | Major sections | `## Authentication` |
| H3 | Subsections | `### OAuth 2.0 Flow` |
| H4 | Topics within subsections | `#### Token Refresh` |
| H5 | Sub-topics (use sparingly) | `##### Error Handling` |
| H6 | Rarely used | Consider restructuring |

### Heading Rules

**Do:**
- Use action-oriented headings for procedures: "Configure the API"
- Use question headings for FAQs: "How do I reset my password?"
- Keep headings parallel in structure
- Make headings scannable and descriptive
- Limit to 8 words or fewer

**Don't:**
- Skip heading levels (H2 → H4)
- Use headings for formatting/emphasis
- Start multiple headings with same word
- Use vague headings like "Overview" alone
- End headings with punctuation

### Heading Quality Test

For each heading, ask:
1. **Specific:** Does it tell what this section contains?
2. **Unique:** Is it distinct from other headings?
3. **Scannable:** Can readers find what they need by scanning?
4. **Parallel:** Does it match sibling heading structure?

## Content Organization

### Information Flow Patterns

**Inverted Pyramid:**
- Most important information first
- Supporting details follow
- Background/context last
- Best for: Executive content, summaries

**Narrative Flow:**
- Beginning → Middle → End
- Builds understanding progressively
- Best for: Tutorials, explanations

**Reference Organization:**
- Alphabetical, categorical, or hierarchical
- No assumed reading order
- Best for: API docs, glossaries, configurations

### Section Length Guidelines

| Section Type | Target Length | When to Split |
|--------------|---------------|---------------|
| Executive Summary | 1-3 paragraphs | N/A |
| Introduction | 2-5 paragraphs | If >1 page |
| Conceptual | 3-7 paragraphs | If >2 pages |
| Procedural | 5-15 steps | If >20 steps |
| Reference | Varies | If >50 items per category |

### Chunking Content

**3-5-7 Rule:**
- 3-5 major sections per document
- 5-7 subsections per major section
- 3-7 items per list

**When to Use Different Formats:**

| Format | Best For | Example |
|--------|----------|---------|
| Paragraphs | Explanations, context | Conceptual introductions |
| Numbered lists | Sequential steps | Procedures |
| Bullet lists | Non-sequential items | Features, requirements |
| Tables | Comparisons, structured data | Feature matrices |
| Code blocks | Commands, configurations | Technical instructions |
| Diagrams | Relationships, flows | Architecture |

## Navigation Design

### Table of Contents

**When to Include:**
- Documents >5 pages
- Documents with >5 major sections
- Reference documents of any length

**TOC Format:**
```markdown
## Table of Contents

1. [Section Name](#section-name)
   1.1. [Subsection](#subsection)
   1.2. [Subsection](#subsection)
2. [Section Name](#section-name)
   [...]
```

### Cross-References

**Internal Links:**
```markdown
See [Authentication](#authentication) for details.
Refer to the [Configuration Guide](./configuration.md).
```

**External References:**
```markdown
For more information, see [Official Documentation](https://docs.example.com).
```

### Navigation Aids

**For Long Documents:**
- Back to top links after major sections
- Breadcrumb-style context in headers
- Mini-TOC at section start for complex sections

**For Document Sets:**
- Index or landing page
- Consistent navigation elements
- Clear document type indicators

## Templates

### Universal Section Template
```markdown
## [Section Title] (Clear, Action-Oriented)

**Context:** [Brief explanation of why this matters - 1-2 sentences]

### [Subsection if needed]

[Main content: explanation, steps, or information]

**Key Points:**
- [Main point 1]
- [Main point 2]
- [Main point 3]

[Tables, code blocks, or lists as appropriate]

**Considerations:**
- [Important note 1]
- [Important note 2]

**Related:** [Links to related sections or documents]
```

### Document Metadata Template
```markdown
---
title: [Document Title]
version: [X.Y.Z]
last_updated: [YYYY-MM-DD]
author: [Name/Agent]
status: [Draft|Review|Approved|Published]
audience: [Primary audience]
---
```

## Quality Checklist

### Structure Quality
- [ ] Single H1 (document title only)
- [ ] No skipped heading levels
- [ ] Logical section flow
- [ ] Parallel heading structure
- [ ] Appropriate section lengths

### Navigation Quality
- [ ] TOC for long documents
- [ ] Working internal links
- [ ] Clear cross-references
- [ ] Easy to scan headings

### Content Organization
- [ ] Most important information prominent
- [ ] Related information grouped
- [ ] Progressive disclosure used
- [ ] Appropriate format for content type

### Accessibility
- [ ] Descriptive link text (not "click here")
- [ ] Tables have headers
- [ ] Lists used appropriately
- [ ] Clear visual hierarchy

## Evaluation Criteria

| Criterion | Poor | Acceptable | Excellent |
|-----------|------|------------|-----------|
| **Findability** | Buried information | Searchable | Scannable headings |
| **Hierarchy** | Flat or skipped | Consistent | Intuitive levels |
| **Flow** | Random order | Logical | Optimized for reader |
| **Chunking** | Walls of text | Broken up | Well-paced sections |
| **Navigation** | None | Basic TOC | Rich cross-linking |

## Success Metrics

- **Findability:** Users locate information in <30 seconds
- **Comprehension:** Single read understanding >90%
- **Completion:** Users finish relevant sections
- **Navigation:** <3 clicks to any content
- **Maintenance:** Easy to update without restructuring

## Related Skills

- **#technical-writing** - Content quality within the structure
- **#data-visualization** - Visual elements within documents
- **#ai-terminology** - Consistent terminology
- **#document-structure** is foundational for all documentation skills
