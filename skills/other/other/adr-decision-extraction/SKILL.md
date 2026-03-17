---
name: adr-decision-extraction
description: Extract architectural decisions from conversations. Identifies problem-solution pairs, trade-off discussions, and explicit choices. Use when analyzing session transcripts for ADR generation.
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
