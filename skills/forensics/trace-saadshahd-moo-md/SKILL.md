---
name: trace
description: Root cause analysis for complex bugs. Use when initial fix fails or incident is severe. Traces Effect → Cause → Root with confidence levels and prevention hierarchy.
---

# trace

Root cause analysis when surface fixes fail.

## When to Use

| Trigger                            | Action    |
| ---------------------------------- | --------- |
| Bug persists after initial fix     | Run trace |
| Production incident (SEV 1-2)      | Run trace |
| Complex failure (multiple sources) | Run trace |
| Trivial bug (< 10 min fix)         | Skip      |

## 1. Timeline

```
HH:MM - [Event] - [System state] - [Action taken]
```

Note: detection time vs. start time (how long hidden?)

## 2. Five Whys

```
Effect: [What users/systems experienced]

Why 1: [Immediate cause] (X-Y% confident)
Why 2: [Underlying mechanism] (X-Y% confident)
Why 3: [System/process gap] (X-Y% confident)
Why 4: [Organizational factor] (X-Y% confident)
Why 5: [Root cause] (X-Y% confident)
```

**Gates**: < 70% any level → request logs/reproduction
Root cause = deepest answer with ≥70% confidence

## 3. Contributing Factors

Beyond root cause, what amplified impact?

**Process**: Monitoring gaps, testing gaps, review gaps
**People**: Unclear ownership, missing runbooks
**Technical**: Dependency failures, capacity limits, config drift
**Context**: Traffic patterns, deployment timing, external factors

List 2-4 factors with specific mechanisms.

**Tools:** [Ishikawa](../soul/references/tools/ishikawa.md) for categorization, [Iceberg](../soul/references/tools/iceberg.md) for deep structure analysis.

## 4. Impact

**Users**: Count, experience, business cost (quantified)
**Systems**: Downstream effects, data integrity, security

## 5. Prevention Hierarchy

### Immediate (< 1 week)

```
1. [Code/config change]
   File: [path:line]
   Verification: [how to confirm]
   Owner: [who]
```

### Short-Term (< 1 month)

```
1. [Alert/test/automation]
   Trigger: [when it fires]
   Owner: [who]
```

### Long-Term (< 1 quarter)

```
1. [Architectural change]
   Problem class: [what it prevents]
   Effort: [story points]
   Owner: [who]
```

Each tier needs ≥1 item.

## 6. Blameless

See `soul/references/blameless.md`

Focus on system gaps, not individual mistakes.

## Output

```
# Incident: [Title]

## Timeline
[Detection → Resolution]

## Five Whys
[With confidence per level]

## Contributing Factors
[2-4 items]

## Impact
[Quantified]

## Prevention
[Immediate / Short-Term / Long-Term]

## Top 3 Actions
1. [Task] | Owner: [Name] | Due: [Date]
2. ...
3. ...
```

## Anti-Patterns

| Bad                     | Good                                   |
| ----------------------- | -------------------------------------- |
| "Human error"           | Identify automation gap                |
| "Communication failure" | Identify process gap                   |
| "Be more careful"       | Add system safeguard                   |
| "Performance issue"     | Specific: "Pool exhausted at 1K req/s" |
