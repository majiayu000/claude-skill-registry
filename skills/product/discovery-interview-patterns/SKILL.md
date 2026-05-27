---
name: discovery-interview-patterns
description: When gathering requirements for new features or projects. Used by DISCOVERY-AGENT.
version: 1.1.0
tokens: ~450
confidence: high
sources:
  - https://www.nngroup.com/articles/interviewing-users/
  - https://productschool.com/blog/product-fundamentals/what-is-product-discovery
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [discovery, requirements, interview, planning]
---

## When to Use
When gathering requirements for new features or projects. Used by DISCOVERY-AGENT.

## Patterns

### Question Categories

**Problem Space**
```
- What problem are we solving?
- Who experiences this problem?
- What's the impact (cost, time, frustration)?
- How is it solved today?
```

**Solution Space**
```
- What does success look like?
- What are must-have vs nice-to-have features?
- What constraints exist (tech, budget, timeline)?
- What's explicitly out of scope?
```

**Technical Context**
```
- What existing systems must integrate?
- What tech stack is required/preferred?
- What are performance requirements?
- What security/compliance needs exist?
```

### Clarity Scoring
```
Score each answer 1-5:
1 = No answer / "I don't know"
2 = Vague / conflicting
3 = Partial clarity
4 = Clear with minor gaps
5 = Fully clear and actionable

Target: Average ≥3.5 before proceeding
```

### Batch Questions (Max 7)
```
Present max 7 questions per round.
Wait for answers before next batch.
Prioritize blocking questions first.
```

## Anti-Patterns
- Asking leading questions
- Assuming requirements without validation
- Skipping "why" questions
- Too many questions at once (>7)
- Not validating conflicting answers

## Verification Checklist
- [ ] Problem clearly defined
- [ ] Success criteria measurable
- [ ] Scope explicitly bounded
- [ ] Constraints documented
- [ ] Average clarity score ≥3.5
- [ ] All stakeholders consulted
