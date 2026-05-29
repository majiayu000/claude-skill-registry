---
name: faion-landing-page
description: "High-converting landing pages. Copy + design + implementation. Triggers: landing page, conversion page."
user-invocable: false
allowed-tools: Read, Write, Edit, Task, WebSearch, AskUserQuestion, TodoWrite
---

# Landing Page Skill

**Communication: User's language. Content: target audience language.**

## Agents

| Agent | Purpose |
|-------|---------|
| faion-landing-copywriter-agent | AIDA/PAS copy, headlines |
| faion-landing-designer-agent | HTML/Tailwind, mobile-first |
| faion-landing-analyzer-agent | Conversion audit, A/B tests |

## Workflow

```
Discovery → Copy (AIDA/PAS) → Design → Implementation → Analysis
```

## Copy Frameworks

**AIDA (cold traffic):** Attention → Interest → Desire → Action
**PAS (aware audience):** Problem → Agitate → Solution

## High-Converting Elements

**Above fold:** Headline, subhead, hero, CTA, trust badges
**Below fold:** Problem, solution, benefits, social proof, FAQ, final CTA

## Execution

```python
# Copywriting
Task(subagent_type="faion-landing-copywriter-agent",
     prompt=f"PRODUCT: {p}, AUDIENCE: {a}, FRAMEWORK: AIDA")

# Design
Task(subagent_type="faion-landing-designer-agent",
     prompt=f"COPY: {copy}, STYLE: {modern|minimal|bold}")

# Analysis
Task(subagent_type="faion-landing-analyzer-agent",
     prompt=f"Analyze {url_or_code} for conversion")
```

## Conversion Checklist

- [ ] Single CTA goal
- [ ] Message match (ad → page)
- [ ] Benefits > features
- [ ] Social proof
- [ ] Mobile responsive
- [ ] Fast load (<3s)
- [ ] Contrast CTA button

## Benchmarks

- Average: 2-5%
- Good: 5-10%
- Excellent: 10%+
