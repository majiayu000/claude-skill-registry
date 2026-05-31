---
name: adr-decision-extraction
description: "Use when you need to mine a conversation, session transcript, or design discussion for architectural decisions before writing ADRs. Identifies problem-solution pairs, trade-off debates, technology choices, and explicit \"[ADR]\" tags. Triggers on \"what decisions did we make\", \"extract decisions from this chat\", \"find the choices in our discussion\", or \"summarize architectural decisions\". Also useful after long planning sessions to capture decisions that were made implicitly. Does NOT write ADR documents \u2014 use adr-writing or write-adr for that."
---

# ADR Decision Extraction

Extract architectural decisions from conversation context for ADR generation.

## Detection Signals

| Signal Type | Examples |
|-------------|----------|
| Explicit markers | `[ADR]`, "decided:", "the decision is" |
| Choice patterns | "let's go with X", "we'll use Y", "choosing Z" |
| Trade-off discussions | "X vs Y", "pros/cons", "considering alternatives" |
| Problem-solution pairs | "the problem is... so we'll..." |

## Extraction Rules

### Explicit Tags (Guaranteed Inclusion)

Text marked with `[ADR]` is always extracted:

```
[ADR] Using PostgreSQL for user data storage due to ACID requirements
```

These receive `confidence: "high"` automatically.

### AI-Detected Decisions

Patterns detected without explicit tags require confidence assessment:

| Confidence | Criteria |
|------------|----------|
| **high** | Clear statement of choice with rationale |
| **medium** | Implied decision from action taken |
| **low** | Contextual inference, may need verification |

## Output Format

```json
{
  "decisions": [
    {
      "title": "Use PostgreSQL for user data",
      "problem": "Need ACID transactions for financial records",
      "chosen_option": "PostgreSQL",
      "alternatives_discussed": ["MongoDB", "SQLite"],
      "drivers": ["ACID compliance", "team familiarity"],
      "confidence": "high",
      "source_context": "Discussion about database selection in planning phase"
    }
  ]
}
```

### Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Concise decision summary |
| `problem` | Yes | Problem or context driving the decision |
| `chosen_option` | Yes | The selected solution or approach |
| `alternatives_discussed` | No | Other options mentioned (empty array if none) |
| `drivers` | No | Factors influencing the decision |
| `confidence` | Yes | `high`, `medium`, or `low` |
| `source_context` | No | Brief description of where decision appeared |

## Extraction Workflow

1. **Scan for explicit markers** - Find all `[ADR]` tagged content
2. **Identify choice patterns** - Look for decision language
3. **Extract trade-off discussions** - Capture alternatives and reasoning
4. **Assess confidence** - Rate each non-explicit decision
5. **Capture context** - Note surrounding discussion for ADR writer

## Hard gates

Run these **in order** after the workflow above and **before** returning output. Each step has an objective pass condition.

1. **Explicit `[ADR]` inventory** — Capture every `[ADR]` segment from the full source (verbatim in working notes). **Pass:** a second pass over the same source adds no new `[ADR]` blocks.
2. **De-duplicate** — Merge or drop inferred rows that repeat an explicit `[ADR]` decision (see [Merge Related Decisions](#merge-related-decisions)). **Pass:** at most one row per distinct decision.
3. **Schema validity** — Serialized JSON matches [Output Format](#output-format) and [Field Definitions](#field-definitions). **Pass:** parse succeeds; every `decisions[]` item has non-empty `title`, `problem`, `chosen_option`; `confidence` ∈ {`high`,`medium`,`low`}; `alternatives_discussed` is an array (use `[]` if none); other optional fields per table.
4. **Low-confidence audit** — For any `confidence: "low"`, `source_context` states what was missing, weak, or contradictory. **Pass:** a reader can see why the rating is not higher.

## Pattern Examples

### High Confidence

```
"We decided to use Redis for caching because of its sub-millisecond latency
and native TTL support. Memcached was considered but lacks persistence."
```

Extracts:
- Title: Use Redis for caching
- Problem: Need fast caching with TTL
- Chosen: Redis
- Alternatives: Memcached
- Drivers: sub-millisecond latency, native TTL, persistence
- Confidence: high

### Medium Confidence

```
"Let's go with TypeScript for the frontend since we're already using it
in the backend."
```

Extracts:
- Title: Use TypeScript for frontend
- Problem: Language choice for frontend
- Chosen: TypeScript
- Alternatives: (none stated)
- Drivers: consistency with backend
- Confidence: medium

### Low Confidence

```
"The API seems to be working well with REST endpoints."
```

Extracts:
- Title: REST API architecture
- Problem: API design approach
- Chosen: REST
- Alternatives: (none stated)
- Drivers: (none stated)
- Confidence: low

## Best Practices

### Context Capture

Always capture sufficient context for the ADR writer:
- What was the discussion about?
- Who was involved (if known)?
- What prompted the decision?

### Merge Related Decisions

If multiple statements relate to the same decision, consolidate them:
- Combine alternatives from different mentions
- Aggregate drivers
- Use highest confidence level

### Flag Ambiguity

When decisions are unclear or contradictory:
- Note the ambiguity in `source_context`
- Set confidence to `low`
- Include all interpretations if multiple exist

## When to Use This Skill

- Analyzing session transcripts for ADR generation
- Reviewing conversation history for documentation
- Extracting decisions from design discussions
- Preparing input for ADR writing tools
