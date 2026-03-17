---
name: documentation
description: |
    Use when writing or structuring software specifications, requirements documents, and architecture decision records. Covers PRDs, TRDs, BRDs, ADRs, RFCs, and executable spec formats.
    USE FOR: choosing requirements document types, documentation strategy, specification templates, combining written specs with executable tests, architecture decision documentation
    DO NOT USE FOR: specific document formats (use prd, trd, brd, adr, rfc, gherkin, gauge sub-skills), diagramming (use diagramming sub-skills)
license: MIT
metadata:
  displayName: "Documentation & Requirements"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Architectural Decision Records"
    url: "https://adr.github.io/"
  - title: "Cucumber — Gherkin Reference"
    url: "https://cucumber.io/docs/gherkin/reference/"
---

# Documentation & Requirements

## Overview
Software specifications capture the "what" and "why" before implementation addresses the "how." Well-structured requirements documents, architecture decisions, and executable specs reduce ambiguity, align stakeholders, and create verifiable acceptance criteria.

## Document Types

### Requirements Documents
| Type | Audience | Focus |
|------|----------|-------|
| **PRD** (Product Requirements) | Product + Engineering | Features, user stories, success metrics |
| **TRD** (Technical Requirements) | Engineering | Architecture, APIs, data models, constraints |
| **BRD** (Business Requirements) | Business + Leadership | ROI, market need, business objectives |

### Architecture Documents
| Type | Audience | Focus |
|------|----------|-------|
| **ADR** (Architecture Decision Record) | Engineering | Single decision with context and consequences |
| **RFC** (Request for Comments) | Engineering + Stakeholders | Proposed change seeking feedback |

### Executable Specifications
| Type | Audience | Focus |
|------|----------|-------|
| **Gherkin** (Given/When/Then) | QA + Product + Engineering | Acceptance criteria as executable tests |
| **Gauge** (Markdown specs) | QA + Engineering | Free-form test specifications in Markdown |

## Document Flow

```
Business Need
    │
    ▼
  BRD ──► "Should we build this?"
    │
    ▼
  PRD ──► "What are we building?"
    │
    ├──► ADR ──► "Why did we choose X over Y?"
    │
    ▼
  TRD ──► "How do we build it?"
    │
    ├──► RFC ──► "Proposing approach Z for feedback"
    │
    ▼
  Gherkin / Gauge ──► "How do we verify it works?"
    │
    ▼
  Implementation + Automated Tests
```

## Best Practices
- Write the PRD before the TRD — define what you're building before deciding how to build it.
- Use ADRs for every significant architecture decision — they're short, structured, and invaluable for future developers.
- Make specifications executable where possible — Gherkin and Gauge connect written specs directly to automated tests.
- Keep documents close to the code in the same repository so they evolve together.
- Use lightweight templates rather than heavyweight processes — a short, focused ADR beats a 50-page design doc nobody reads.
- Review specs before implementation, not after — specifications are cheapest to change when they're still text.
