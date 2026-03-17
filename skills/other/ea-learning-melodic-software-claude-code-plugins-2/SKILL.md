---
name: ea-learning
description: Explain enterprise architecture concepts in practical terms. Use when learning about TOGAF, Zachman, ADRs, or any EA terminology.
allowed-tools: Read, Glob, Grep
---

# Enterprise Architecture Learning

## When to Use This Skill

Use this skill when you need to:

- Understand what an EA concept means
- Learn how to apply EA frameworks practically
- Get context-specific explanations linked to your codebase
- Answer "what would TOGAF/Zachman say about this?"

**Keywords:** explain, what is, why, learn, togaf, zachman, enterprise architecture, adm, viewpoint, stakeholder, architecture principle

## Explanation Approach

This skill provides practical, developer-focused explanations that:

1. **Start with the "why"** - Why does this concept exist?
2. **Use concrete examples** - Real-world applications
3. **Link to code** - How does this apply to your codebase?
4. **Avoid jargon** - Plain language over consultant-speak

## Framework-Agnostic Entry Points

Not sure where to start? Use these practical entry points:

| If you want to... | Start with... |
| --- | --- |
| Document a decision | ADR (Architecture Decision Record) |
| Understand system structure | C4 Model diagrams |
| Plan a migration | Gap Analysis |
| Communicate to executives | Stakeholder Viewpoints |
| Ensure design consistency | Architecture Principles |

## Core Concepts Quick Reference

### Architecture Decision Record (ADR)

**What:** A document capturing a significant design decision and its context.

**Why:** Decisions get forgotten. New team members don't know why things were built a certain way. ADRs preserve institutional knowledge.

**When to use:** Any decision that affects multiple components, is hard to reverse, or involves trade-offs.

### TOGAF (The Open Group Architecture Framework)

**What:** A comprehensive methodology for developing enterprise architecture.

**Why:** Provides structured approach to large-scale architecture work with governance and stakeholder management.

**Key concept:** The ADM (Architecture Development Method) - a cycle of phases from vision through implementation.

### Zachman Framework

**What:** A 6x6 classification matrix for organizing architecture artifacts.

**Why:** Ensures complete coverage - every perspective (who, what, how, when, where, why) is documented for every stakeholder level.

**Key insight:** It's a taxonomy (how to organize), not a methodology (how to create).

### C4 Model

**What:** A hierarchical approach to software architecture diagrams.

**Why:** Provides consistent abstraction levels (Context, Container, Component, Code) that communicate clearly to different audiences.

**Levels:**

1. Context - System and its environment
2. Container - High-level technology choices
3. Component - Major structural elements
4. Code - Class/module level (optional)

### Architecture Principles

**What:** Foundational rules that guide design decisions.

**Why:** Ensure consistency across teams and decisions. Provide guardrails without micromanagement.

**Format:** Statement + Rationale + Implications

## Progressive Learning Path

### Beginner: Start Here

1. **ADRs** - Start documenting decisions immediately
2. **C4 Context Diagram** - Visualize your system's boundaries
3. **Architecture Principles** - Define 3-5 guiding principles

### Intermediate: Add Structure

1. **TOGAF Phases** - Understand the A-H cycle
2. **Zachman Columns** - Use What/How/Where/Who/When/Why as a checklist
3. **Gap Analysis** - Document current vs target state

### Advanced: Enterprise Scale

1. **Full Zachman Matrix** - Multiple stakeholder perspectives
2. **TOGAF Governance** - Architecture board, compliance
3. **Cloud Frameworks** - CAF, Well-Architected alignment

## Connecting to Your Codebase

When explaining concepts, this skill will:

1. Search for existing architecture documentation
2. Identify relevant code patterns
3. Suggest where concepts might apply
4. Provide examples specific to your project

## Common Questions Answered

| Question | Answer |
| --- | --- |
| Do I need TOGAF certification to use EA concepts? | No. The concepts are valuable regardless of certification. Start with ADRs and principles. |
| Is Zachman too heavyweight for my project? | Use it as a checklist, not a requirement. Even checking 2-3 cells improves coverage. |
| How do EA frameworks relate to agile? | EA provides "just enough" architecture upfront. Decisions evolve through ADRs. |
| What's the minimum viable EA? | ADRs + Architecture Principles + C4 Context Diagram. You can build from there. |

## Memory References

For detailed framework information, see:

- `references/togaf-overview.md` - TOGAF 10 ADM phases
- `references/zachman-overview.md` - Zachman 3.0 matrix
- `references/architecture-principles.md` - Principles template

## Version History

- **v1.0.0** (2025-12-05): Initial release
  - Practical explanations for EA concepts
  - Framework-agnostic entry points
  - Progressive learning path (beginner to advanced)
  - Core concepts quick reference (ADR, TOGAF, Zachman, C4)

---

## Last Updated

**Date:** 2025-12-05
**Model:** claude-opus-4-5-20251101
