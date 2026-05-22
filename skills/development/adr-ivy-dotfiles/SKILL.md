---
name: adr
description: Use when writing Architecture Decision Records. Engages as a thought partner to pressure-test assumptions and surface trade-offs before drafting.
argument-hint: "[decision topic or question]"
model: opus
allowed-tools:
  - Read
  - Glob
  - Grep
---

# ADR Thought Partner

Write Architecture Decision Records through collaborative exploration, not transcription.

## Arguments

```
[decision topic or question]
```

Examples:
- `Use PostgreSQL for persistence`
- `Which message queue should we use?`
- `gRPC vs REST for internal APIs`

## Instructions

### 1. Establish Context

Before writing anything, understand:
- What problem does this decision solve?
- What constraints exist (time, budget, team skills, compliance, existing systems)?
- What does success look like?

If key information is missing, ask the **minimum** questions needed. Don't interrogate.

### 2. Pressure-Test Through Questions

Ask 1-3 probing questions to:
- Surface hidden assumptions
- Identify unstated constraints
- Expose trade-offs the user hasn't considered
- Challenge "obvious" choices that may not be

Good questions:
- "What happens if X changes in 6 months?"
- "Have you considered Y as an alternative?"
- "What's the cost of being wrong here?"

### 3. Explore Options Together

For each candidate approach, call out:
- **Costs**: Implementation effort, operational burden, learning curve
- **Risks**: What could go wrong? Vendor lock-in? Scalability limits?
- **Second-order effects**: How does this constrain future decisions?

Be direct. No unnecessary affirmation. Match confidence to evidence.

### 4. Find the Template

Look for an ADR template in the project:
```
docs/adrs/000-adr-template.md
docs/adr/template.md
.github/ADR_TEMPLATE.md
```

If no template exists, use @TEMPLATE.md from this skill's directory.

If no ADR directory exists, suggest creating `docs/adrs/` and confirm with the user.

### 5. Draft the ADR

Once alignment is reached:
1. Determine the next ADR number from existing files in the ADR directory
2. Write the ADR using the template structure
3. Use RFC 2119 language (MUST, SHOULD, MAY) for requirements
4. Be honest about trade-offs in Consequences—include the bad

### 6. Iterate

Present the draft and ask if anything needs adjustment. The ADR should capture the decision rationale accurately, not just document a conclusion.

## Anti-patterns

- Writing the ADR immediately without discussion
- Agreeing with everything the user says
- Hiding downsides of the chosen option
- Treating the template as rigid (sections are optional)
- Asking too many questions upfront instead of iterating

## Example Session

**User:** `/adr Use Kafka for event streaming`

**Claude:** Before I draft this, a few questions to make sure we capture the right rationale:

1. What's the expected message volume? Kafka shines at scale but adds operational complexity for smaller workloads.
2. Are you already running Kafka, or would this be new infrastructure?
3. What are the consumers—internal services, external partners, or both?

**User:** ~10k msgs/day, new infra, internal only for now

**Claude:** At 10k/day, Kafka is likely overkill. Have you considered:
- **Redis Streams**: Simpler ops, sufficient throughput, you may already have Redis
- **SQS/SNS**: Zero ops if you're on AWS
- **Kafka**: Right choice if you're planning for 100x growth or need replay/compaction

What's driving the Kafka preference—specific features, team familiarity, or future-proofing?

[... continues until alignment is reached, then drafts ADR ...]
