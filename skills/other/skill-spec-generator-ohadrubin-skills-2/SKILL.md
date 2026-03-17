---
name: skill-spec-generator
description: Generate structured skill specifications for independent skill creators. Use when asked to ideate, brainstorm, or specify multiple skills for a domain, workflow, or problem space. Outputs self-contained specs with list-level context so each skill can be built independently. Triggers on requests like "what skills would help with X", "generate skill ideas for Y", "specify skills to cover Z workflow".
---

# Skill Spec Generator

Generate a set of skill specifications that independent skill creators can implement without coordination. Each spec must be self-contained; list-level context explains how specs relate.

## Process

### 1. Analyze Input

Inputs vary. Identify what's provided and what needs discovery:

| Input Type | What to Extract |
|------------|-----------------|
| Domain description | Core workflows, tools, file types, pain points |
| Gap analysis | Existing coverage, missing capabilities, overlap risks |
| Pain points | Repetitive tasks, error-prone steps, knowledge gaps |
| Workflow description | Sequential steps, decision points, variations |
| Existing skills list | Patterns, naming conventions, granularity level |

Ask clarifying questions only for critical ambiguities. Prefer generating specs with stated assumptions over excessive back-and-forth.

### 2. Identify Skill Boundaries

Good skill boundaries:
- **Single responsibility**: One clear purpose, describable in one sentence
- **Natural triggers**: Obvious when to use it (file type, task verb, domain term)
- **Standalone value**: Useful even if other skills don't exist
- **Composable**: Can combine with other skills without overlap

Watch for:
- Skills too broad (should be split)
- Skills too narrow (should be merged or dropped)
- Overlapping triggers (will confuse skill selection)

### 3. Generate Specifications

For each skill, produce a spec block:

```
## Skill: [name]

**Description**: [Triggering description - what it does AND when to use it]

**Rationale**: [Why this skill is needed, what problem it solves]

**Example triggers**:
- "[example user request 1]"
- "[example user request 2]"

**Expected components**:
- scripts/: [what executable code, if any]
- references/: [what documentation, if any]
- assets/: [what templates/files, if any]

**Complexity**: [Low/Medium/High] - [brief justification]

**Dependencies**: [other skills from this list, or "None"]

**Notes for implementer**: [any non-obvious considerations, edge cases, or implementation hints]
```

Adjust detail level based on context:
- Spec-only request → focus on description, rationale, triggers
- Implementation-ready request → include full component breakdown
- Prioritization request → add effort estimates and dependencies

### 4. Provide List-Level Context

Wrap the specs with framing that helps skill creators understand the set:

```
# Skill Specification Set: [theme/domain]

## Overview
[1-2 paragraphs: what domain this covers, why these skills were chosen, what workflows they enable]

## Coverage Map
[How these skills relate: sequential workflow? parallel options? layered capabilities?]
[Visual or textual representation of relationships]

## Priority Order
[Recommended implementation sequence with rationale]

## Gaps and Future Work
[What's intentionally excluded, what might be added later]

---

[Individual skill specs follow]
```

## Output Principles

1. **Self-contained specs**: Each spec should give an implementer everything they need. Don't assume they'll read other specs.

2. **Consistent granularity**: Skills in a set should be roughly similar in scope. Don't mix "process all documents" with "add page numbers".

3. **Clear triggers**: The description field is the primary trigger mechanism. Make it specific enough to fire correctly, broad enough to catch variants.

4. **Honest complexity**: Skill creators need accurate effort estimates. A "Low" skill that actually takes a week erodes trust.

5. **Explicit relationships**: If skills depend on or complement each other, state it. Don't make implementers discover this.

## Anti-Patterns

- **Kitchen sink skills**: Trying to do too much. Split them.
- **Orphan skills**: Skills that only make sense with others. Either merge or make standalone.
- **Vague triggers**: "Use for document tasks" - too broad, will misfire.
- **Assumed context**: "Works with the output of skill X" without explaining what that output is.
- **Scope creep notes**: "Could also do X, Y, Z" - either include it or don't.
