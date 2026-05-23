---
name: doc-coauthoring
description: Guide users through structured collaborative documentation creation. Use when user wants to write documentation, update README, create architecture docs, draft proposals, technical specs, decision docs, refactor documentation, create API docs, or document code.
---

# Doc Co-Authoring Workflow

Collaborative workflow for creating documentation that works for readers.

## When to Offer This Workflow

**Trigger conditions:**
- Writing documentation: "write a doc", "draft a proposal", "create a spec", "write up"
- Code documentation: "write README", "create API docs", "document this code", "architecture docs"
- Specific doc types: "PRD", "design doc", "decision doc", "RFC", "technical spec"
- User starting any substantial writing task

## Workflow Variants

| Variant | Stages | Use For |
|---------|--------|---------|
| **Full Collaborative** | Context Gathering → Refinement → Reader Testing | Proposals, specs, decisions, RFCs |
| **Streamlined Collaborative** | Context Gathering → Refinement | READMEs, API docs, architecture guides |

Both variants use collaborative principles (clarifying questions, iterative refinement). Streamlined skips Reader Testing since code docs have different validation (working examples, API accuracy).

## Three Stages Overview

### Stage 1: Context Gathering
Close the gap between what the user knows and what Claude knows. Ask about doc type, audience, desired impact, and template. Encourage info dumping. Ask clarifying questions until understanding is sufficient.

### Stage 2: Refinement & Structure
Build the document section by section. For each section: ask clarifying questions, brainstorm options, let user curate, draft, and refine through surgical edits. Use code documentation patterns as scaffolds for READMEs, APIs, etc.

### Stage 3: Reader Testing (Full Collaborative only)
Test the document with a fresh Claude (no context bleed) to verify it works for readers. If sub-agents available, test directly. Otherwise, guide user through manual testing.

## Initial Offer Template

When triggered, offer the workflow:

```
I can help you write that [doc type]. I use a structured workflow that helps
ensure the doc works well when others read it:

1. **Context Gathering**: You share relevant context while I ask clarifying questions
2. **Refinement & Structure**: We build each section through brainstorming and iteration
3. **Reader Testing**: We test the doc with a fresh Claude to catch blind spots
   (or skip for code docs like READMEs)

Would you like to try this workflow, or prefer to work freeform?
```

## Code Documentation Patterns

For code docs, select the appropriate pattern as the starting scaffold:

| Doc Type | Pattern |
|----------|---------|
| README | Features, Installation, Quick Start, Config, API, Contributing |
| API Docs | OpenAPI spec with paths, schemas, examples |
| Architecture | Overview, Component Diagram, Components table, Data Flow |
| Configuration | Required/Optional vars table, example config |
| Module | Purpose, Architecture diagram, Components, Methods table |

See [WORKFLOW.md](WORKFLOW.md) for complete patterns.

## Resources

- [WORKFLOW.md](WORKFLOW.md) - Full stage procedures and code patterns
- [EXAMPLES.md](EXAMPLES.md) - Complete templates for proposals, specs, READMEs
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions

## Tips

- **Be direct and procedural** - explain rationale briefly when it affects user behavior
- **Give user agency** - always allow them to skip stages or work freeform
- **Track context** - address gaps as they come up, don't let them accumulate
- **Use surgical edits** - never reprint entire doc, use str_replace
- **Quality over speed** - each iteration should make meaningful improvements
- **For code docs** - verify examples work, check API signatures against actual code
