---
name: sdlc-cross-review
description: Review a document against its SDLC lifecycle context — assess completeness and check consistency with parent documents in the document hierarchy.
argument-hint: <file|folder>...
---

Review the target document(s) at `$ARGUMENTS` against its SDLC lifecycle context.

**Stop after each stage and have changes reviewed with user.**

> **Note**: This skill checks a document's position and consistency within a project hierarchy — it does not polish the document itself. Stages 0-4 are **analysis only** — findings are presented for discussion, not applied as edits. The developer holds final authority on all judgment calls.

0. **Read and identify context** (developer confirms)
   - Read the target document and its surrounding project structure
   - What is this document about and where does it sit in the project?
   - Can you identify a document hierarchy (V-model, or project-defined)?
   - If the project defines its own hierarchy, use that; otherwise ask the developer to clarify
   - Confirm understanding of the document's position before proceeding

1. **Assess completeness** (agent proposes, developer decides)
   - Is this a skeleton that needs **fleshing out**, or a draft that needs **polishing**?
   - Skeletons need generative work (structure, diagrams, missing sections) — that's a **flesh-out** task, not a cross-review
   - Drafts with language issues need **review-steps** first
   - If the document isn't ready for cross-review, recommend the appropriate skill and stop
   - Ask: does the developer want to proceed with cross-review now, or address completeness first?

2. **Review vs parent document** (agent critiques, developer discusses)
   - Identify the parent document(s) that constrain this document (left side, decomposition)
   - Is the target document consistent with decisions and constraints in its parent(s)?
   - Are there contradictions or gaps between the target and its parent documents?
   - Does the target document trace back to requirements or decisions in the parent?
   - Present findings and ask: are any inconsistencies intentional or reflect evolved thinking?

3. **Cross-validate against the right side** (agent critiques, developer discusses)
   - Identify the validation pair for this document (see V-Model Context below)
   - Do validation artifacts exist that cover what the document specifies?
   - Is anything specified in the document that has no corresponding validation?
   - Is anything validated that isn't specified in the document?
   - Ask: are missing validation artifacts a known gap, or an oversight?

4. **Summary and recommendations** (agent leads)
   - What is the document's overall consistency with its hierarchy?
   - What are the top issues to address?
   - Recommendation: consistent / minor gaps / needs rework

## Pipeline Position

This skill sits **outside the main pipeline** (flesh-out -> review-steps -> strong-edit -> agent-optimize). It's a lateral check — validating a document against its project context, not polishing the document itself. Run it when a document is mature enough to check against its hierarchy.

## When to Use This vs Other Skills

| Goal | Use |
|------|-----|
| Raw notes need structure and expansion | **flesh-out** |
| Draft needs polish and consistency | **review-steps** |
| Complete draft needs critical evaluation | **strong-edit** |
| Check document against its SDLC hierarchy | **sdlc-cross-review** |
| Finalized document needs agent-friendly restructuring | **agent-optimize** |

## V-Model Context

The [V-model](https://en.wikipedia.org/wiki/V-model_(software_development)) pairs each definition stage with a corresponding testing stage. The left side decomposes requirements; the right side validates them. Each level on the right validates the corresponding level on the left.

```
Requirements Analysis ◄──────────────────► Acceptance Testing
     │                                              ▲
     │ constrains                                   │ validates
     ▼                                              │
System Design ◄────────────────────────────► System Testing
     │                                              ▲
     │ constrains                                   │ validates
     ▼                                              │
Architecture Design ◄──────────────────────► Integration Testing
     │                                              ▲
     │ constrains                                   │ validates
     ▼                                              │
Module Design ◄────────────────────────────► Unit Testing
     │                                              ▲
     │ constrains                                   │ validates
     ▼                                              │
              Implementation
```

### Standard Cross-Validation Pairs

| Left Side (Definition) | Right Side (Validation) |
|------------------------|-------------------------|
| Requirements analysis | Acceptance testing |
| System design | System testing |
| Architecture design | Integration testing |
| Module design | Unit testing |

Not every project will use all levels. Identify which levels the project uses and apply the relevant checks.

## References

- [V-model (software development) - Wikipedia](https://en.wikipedia.org/wiki/V-model_(software_development))
- [The V-model explained - IAPM](https://www.iapm.net/en/blog/v-model/)
- [What Is the V-Model in Software Development? - Built In](https://builtin.com/software-engineering-perspectives/v-model)
