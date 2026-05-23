---
name: diagnostic-action
description: Use when the user asks why something happened, what’s wrong, root cause analysis, debugging, or incident explanation.
version: 1.0
---

# Diagnostic Action Skill

## Purpose
Identify and explain likely causes of an observed problem or symptom.

## When to use
- “Why did this happen?”
- Root cause analysis
- Debugging / incident investigation
- Failure analysis

Do NOT use for:
- recommendations or fixes (use prescriptive-actions)
- plans or procedures (use planning-action / procedural-action)

## Operating rules
1. Restate symptoms and scope clearly.
2. Generate multiple plausible hypotheses.
3. Explain the mechanism for each hypothesis.
4. Rank by likelihood and impact.
5. Identify missing data that would disambiguate causes.
6. Do not prescribe fixes unless explicitly asked.

## Outputs
### Symptoms & scope
### Hypotheses (ranked)
- Cause
- Mechanism
- Evidence for/against
- Confidence

### Most likely causes
### Data needed / open questions
