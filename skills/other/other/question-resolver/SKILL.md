---
name: question-resolver
description: Systematically resolve questions - determine if answerable, gather evidence
category: Thinking Analysis
---

# Skill: question-resolver

## What I do

I manage the process of finding answers to technical and domain-specific questions. I ensure that every question is classified, systematically researched using appropriate tools, and documented once resolved.

## When to use me

- When faced with an unknown API, library, or codebase pattern
- To resolve ambiguity in user requests or requirements
- During research spikes to understand a new technology
- To track "known unknowns" that need resolution before proceeding

## Core principles

1. **Classify first** — Is it answerable now (documentation), through research (spikes/data), or unanswerable (requires stakeholder input)?
2. **Structured investigation** — Use a methodical approach: hypothesise, search, verify.
3. **Gather evidence** — Rely on documentation, code, or experimental results rather than hearsay.
4. **Document the "why"** — Once resolved, record the answer and the evidence that supports it.

## Patterns & examples

**Question Log Template:**
| Question | Type (Doc/Spike/Stake) | Priority | Resolution Status | Link to Evidence |
| :--- | :--- | :--- | :--- | :--- |
| "Does library X support IPv6 natively?" | Doc | High | Resolved | [Link to API Doc] |
| "What is the max latency our users accept?" | Stake | Medium | Pending | N/A |

**Escalation Triggers:**
- **Stuck:** 30+ minutes without a clear path forward → Escalate or shift approach.
- **Ambiguous:** Requirement contradicts existing system behaviour → Escalate to stakeholder.
- **Contradictory:** Documentation differs from actual code behaviour → Trust code, but verify why.

## Anti-patterns to avoid

- ❌ **Rabbit holing** — Spending hours researching a low-priority question.
- ❌ **The "I think" trap** — Accepting a plausible answer without actual verification.
- ❌ **Ignoring "known unknowns"** — Proceeding with a plan while key questions remain unanswered.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Thinking-Analysis/Question Resolver.md`

## Related skills

- `critical-thinking` — Validating the answers found
- `assumption-tracker` — Identifying the questions that need to be asked
- `knowledge-base` — Searching for existing answers
- `epistemic-rigor` — Distinguishing between theories and facts
