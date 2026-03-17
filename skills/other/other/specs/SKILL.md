---
name: specs
description: |
    Use when working with software specifications, architecture documentation, and diagramming. Covers the full spectrum of spec-driven development — from architectural diagrams to requirements documents to specification tooling.
    USE FOR: specification-driven development, architecture documentation strategy, choosing diagram types, choosing requirements formats, spec-to-implementation workflows
    DO NOT USE FOR: specific diagram syntax (use diagramming sub-skills), specific document templates (use documentation sub-skills), specific tooling (use tools sub-skills)
license: MIT
metadata:
  displayName: "Specifications & Architecture Documentation"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "arc42 — Architecture Documentation Template"
    url: "https://arc42.org/"
  - title: "Documenting Software Architectures — SEI"
    url: "https://www.sei.cmu.edu/our-work/software-architecture/tools/documenting/"
---

# Specifications & Architecture Documentation

## Overview
Good architecture starts with good specs. This skill covers the full spectrum of specification-driven development — from visual diagrams that communicate system structure, to requirements documents that capture intent, to tools that automate the spec-to-code pipeline.

## Specification Landscape

```
┌─────────────────────────────────────────────────────┐
│  Diagramming                                        │
│  Visual representations of architecture & behavior  │
│  C4, Mermaid, UML, TOGAF, ArchiMate, D2, ERD, ...  │
├─────────────────────────────────────────────────────┤
│  Documentation                                      │
│  Written specifications capturing intent & design   │
│  PRD, TRD, BRD, ADR, RFC, Gherkin, Gauge           │
├─────────────────────────────────────────────────────┤
│  Tools                                              │
│  Automation for spec-driven workflows               │
│  GitHub Spec Kit                                    │
└─────────────────────────────────────────────────────┘
```

## Choosing the Right Diagram

| Need | Diagram Type | Tool |
|------|-------------|------|
| System context and containers | C4 diagrams | Structurizr DSL, Mermaid |
| Interaction sequences | Sequence diagrams | Mermaid, PlantUML |
| Object-oriented structure | Class / component diagrams | UML, Mermaid |
| State machines | State diagrams | Mermaid, PlantUML, UML |
| Data models | Entity-Relationship diagrams | Mermaid, ERD tools |
| Enterprise architecture | TOGAF / ArchiMate | Archi, Sparx EA |
| Data flow and processing | Functional diagrams | DFD, Mermaid |
| General architecture | Declarative diagrams | D2, Mermaid |
| Timelines and scheduling | Gantt charts | Mermaid |

## Choosing the Right Document

| Need | Document Type |
|------|--------------|
| What to build and why (product view) | PRD |
| How to build it (engineering view) | TRD |
| Business justification and ROI | BRD |
| Recording an architecture decision | ADR |
| Proposing a significant change | RFC |
| Executable acceptance criteria | Gherkin feature files |
| Markdown-based test specifications | Gauge specs |

## Spec-Driven Development Workflow

```
1. Requirements  →  PRD / BRD (what + why)
2. Architecture  →  C4 / TOGAF diagrams (how it fits)
3. Design        →  TRD + ADRs (how to build + decisions)
4. Acceptance    →  Gherkin / Gauge (verifiable criteria)
5. Implementation → Code (guided by specs)
6. Validation    →  Automated tests from specs
```

## Best Practices
- Start with a C4 Context diagram before diving into implementation — it forces you to define system boundaries and external dependencies.
- Use ADRs to record every significant architecture decision so future developers understand the "why" behind the "what."
- Write Gherkin scenarios alongside PRDs so acceptance criteria are executable from day one.
- Use Mermaid for diagrams embedded in Markdown docs (PRs, ADRs, RFCs) — it renders natively on GitHub.
- Use spec-driven tools like GitHub Spec Kit to automate the spec → plan → tasks → implementation pipeline.
- Keep diagrams as code (Mermaid, D2, PlantUML, Structurizr DSL) and version them in Git alongside the source code they describe.
