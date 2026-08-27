---
name: prism
description: 'Split one artifact across independent lenses and return where they clash, plus the single question that resolves the clash. Use when one reviewer angle is not enough, such as a spec read for security, cost, and operability at once, or when the user says "prism this" or "review this from different angles". It reports the disagreement and never the average. To repeat one identical read to measure divergence, use fan-out-fresh-reads.'
disable-model-invocation: true
---
# Prism

Split one artifact across independent lenses and return where they converge and where they disagree.

## Method

1. **Read end to end** before choosing lenses.
2. **Choose 2 to 5 lenses**, one per genuinely distinct failure mode. Two candidates sharing a failure mode are one lens, not two. No default count; the artifact's modes set it.
3. **One verdict per lens** - pass, fail, or unclear - with its single most load-bearing reason. No hedging list.
4. **Group the verdicts:** full agreement, agreement for different reasons, disagreement.
5. **Where lenses disagree**, name the single next question that would resolve it. That question is the output, not the individual verdicts.
6. **Where every lens agrees**, return the shared verdict with reasons load-bearing for at least two lenses.

## Completion

A reader sees which lenses agreed, which disagreed, and the one question that matters, and can act without re-running the prism.

