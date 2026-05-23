---
name: dive
description: Dives deep into project questions using layered investigation (docs → code → analysis) to provide evidence-based answers with file:line citations. Use when asking "how does X work", "what is Y", "where is Z", or investigating features, APIs, configuration, codebase structure, or technical decisions.
---

# Dive

Dives deep into your project to investigate any question, from business logic to technical implementation. Uses layered search strategy to find evidence-based answers backed by documentation and code.

## Philosophy

### Why Dive?

Dive exists because **assumptions are dangerous**.

The core question isn't "how do I find the answer?" but "how do I know my answer is true?"

```
The Fundamental Problem:
├── Memory is unreliable (yours and the codebase's docs)
├── Code evolves faster than documentation
├── "I think it works like..." is not evidence
└── Only the current codebase tells the current truth
```

### Evidence Over Intuition

```
Intuition: "This probably uses X pattern"
Dive:      "render.ts:273 shows reconcileKeyedChildren() implementation"
```

Intuition is a starting point, not an answer. Dive converts intuition into verified knowledge through evidence gathering.

### Layered Search: Why This Order?

```
Layer 1: Documentation  → What the project CLAIMS to do
Layer 2: Code           → What the project ACTUALLY does
Layer 3: Deep Analysis  → HOW it all connects
```

Why documentation first?
- It's faster to read
- It gives you vocabulary for code search
- Discrepancies between docs and code are themselves findings

Why code second?
- Code is ground truth—it can't lie about what it does
- Tests show expected behavior in executable form
- Types reveal contracts and constraints

Why deep analysis last?
- It's expensive (time, context)
- Only needed when layers 1-2 don't converge
- Cross-component questions need tracing

### Cross-Referencing Reveals Truth

When documentation says X but code does Y:
- The code is always correct about behavior
- The documentation reveals intent or outdated understanding
- The discrepancy itself is valuable information

This is not a failure of search. It's a success—you found something real.

## Core Concepts

### Evidence Has Hierarchy

Not all evidence is equal:

| Source | Reliability | What it proves |
|--------|-------------|----------------|
| Running code | Highest | Current behavior |
| Tests | High | Expected behavior |
| Implementation | High | How it works |
| Type definitions | Medium-High | Contracts |
| Comments | Medium | Developer intent |
| Documentation | Medium | Claimed behavior |
| Commit messages | Low-Medium | Historical intent |

Multiple sources agreeing = high confidence.
Single source = verify with another layer.

### The Question Shapes the Search

Different questions need different approaches:

**"How does X work?"** → Start with code, verify with tests
**"Why is X designed this way?"** → Start with docs/ADRs, check history
**"What calls X?"** → Start with grep, trace references
**"When did X change?"** → Start with git log, find the commit

Don't apply the same search pattern to every question. Let the question guide you.

### Uncertainty is Information

When you can't find clear evidence:
- State what you searched
- State what you found (even partial)
- State what's missing
- Offer hypotheses, clearly labeled as such

"I couldn't find X" is a valid finding. It tells the next investigator where not to look.

## The Dive Loop

```
1. Understand: What exactly is being asked?
      ↓
2. Search: Layer 1 → Layer 2 → Layer 3 (as needed)
      ↓
3. Collect: Gather evidence with file:line citations
      ↓
4. Synthesize: What do the sources tell us together?
      ↓
5. Respond: Direct answer + evidence + uncertainty
```

This isn't a checklist to follow blindly. It's a mental model for thorough investigation.

## When Layers Conflict

Documentation says one thing, code does another. This is common. Here's how to think about it:

| Situation | What to trust | What to report |
|-----------|---------------|----------------|
| Docs outdated | Code | Note the discrepancy |
| Feature removed | Code | Flag potential doc cleanup |
| Docs wrong | Code | Recommend doc fix |
| Code buggy | Neither | Flag as potential bug |

The key: **always report both**, let context determine action.

## Reference

Load these **as needed**, not upfront:

- [reference/search-strategies.md](reference/search-strategies.md) - Detailed search patterns
- [reference/code-search-patterns.md](reference/code-search-patterns.md) - Code navigation techniques
- [reference/evidence-collection.md](reference/evidence-collection.md) - Citation formats and templates

## Understanding, Not Rules

Instead of memorizing anti-patterns, understand the underlying tensions:

| Tension | Resolution |
|---------|------------|
| Speed vs Thoroughness | Match depth to stakes. Quick question? Layer 1 may suffice. Critical decision? Go deep. |
| Confidence vs Evidence | Never state confidence without evidence. "I'm 90% sure" means nothing without sources. |
| Intuition vs Verification | Use intuition to guide search, not to answer. Then verify. |
| Completeness vs Relevance | Answer the question asked. Note related findings briefly, don't digress. |

The goal isn't to follow a procedure. It's to **know when you know** something is true.
