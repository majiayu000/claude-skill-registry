---
name: user-research
version: "2.0.0"
description: User research methods, customer insight gathering, and problem validation for product discovery.
sasmp_version: "1.3.0"
bonded_agent: 02-discovery-research
bond_type: PRIMARY_BOND
parameters:
  - name: research_method
    type: string
    enum: [interviews, surveys, usability, observation, analytics]
    required: true
  - name: sample_size
    type: number
    default: 20
retry_logic:
  max_attempts: 3
  backoff: exponential
logging:
  level: info
  hooks: [start, complete, error]
---

# User Research Skill

Conduct effective user research to understand customer needs, behaviors, and pain points. Master interview techniques and insight synthesis.

## Research Methods

### Method Selection Guide

| Method | When | Sample | Duration |
|--------|------|--------|----------|
| Interviews | Deep understanding | 15-25 | 45-60 min |
| Surveys | Quantitative validation | 100+ | 5-10 min |
| Usability | UX issues | 5-8 | 30-60 min |
| Observation | Real behavior | 3-5 | 2-4 hours |
| Analytics | Scale patterns | All users | Ongoing |

## Qualitative Research

### Interview Structure

```
OPENING (5 min):
- Intro & rapport
- Permission to record
- Context setting

CONTEXT (10 min):
- Role and responsibilities
- Day-to-day workflow
- Tools used

DEEP DIVE (20 min):
- "Walk me through [process]..."
- "Tell me about last time [problem]..."
- "What frustrates you most?"

IMPACT (10 min):
- "What happens when [problem]?"
- "How much time/money does it cost?"

FUTURE (10 min):
- "What would ideal look like?"
- "What would you pay for [solution]?"

CLOSING (5 min):
- "Anything else?"
- "Can I follow up?"
```

### Interview Best Practices

- Listen 70%, talk 30%
- Ask "Why?" 5 times
- Avoid leading questions
- Use silence effectively
- Capture quotes verbatim

## Quantitative Research

### Survey Design

**Question Types:**
- Rating scale (1-5, 1-10)
- Multiple choice
- Open-ended (limit 1-2)
- Ranking

**NPS Question:**
"How likely are you to recommend [product] to a friend? (0-10)"

### Sample Size Calculator

```
For 95% confidence, 5% margin:
- Population 100 → Sample 80
- Population 500 → Sample 217
- Population 1000 → Sample 278
- Population 10000 → Sample 370
```

## Synthesis

### Affinity Mapping

1. Write each insight on sticky note
2. Group similar insights
3. Name each group (theme)
4. Rank by frequency/impact
5. Extract top 5-10 themes

### Persona Template

```
NAME: [Descriptive name]
ROLE: [Job title, company type]
QUOTE: "[Real quote from research]"

GOALS:
- [Goal 1]
- [Goal 2]

FRUSTRATIONS:
- [Pain 1]
- [Pain 2]

BEHAVIORS:
- [How they work]
- [Tools they use]

NEEDS:
- [Need 1]
- [Need 2]
```

### Journey Map

| Stage | Actions | Emotions | Pain Points | Opportunities |
|-------|---------|----------|-------------|---------------|
| Aware | Search | Curious | Hard to find | SEO, content |
| Consider | Compare | Confused | Too many options | Comparison |
| Purchase | Buy | Anxious | Complex checkout | Simplify |
| Use | Onboard | Overwhelmed | Steep learning | Better UX |

## Troubleshooting

### Yaygın Hatalar & Çözümler

| Hata | Olası Sebep | Çözüm |
|------|-------------|-------|
| Low response | Wrong incentive | $50-100 gift card |
| Surface insights | Leading questions | "Why?" 5x |
| Conflicting data | Mixed segments | Segment analysis |
| No show | Scheduling issues | Calendar hold, reminder |

### Debug Checklist

```
[ ] Research plan documented mi?
[ ] Sample size sufficient mi?
[ ] Questions non-leading mi?
[ ] Recording consent alındı mı?
[ ] Synthesis done within 24h mi?
[ ] Insights actionable mi?
```

### Recovery Procedures

1. **Low Participation** → Increase incentive, new channels
2. **Conflicting Data** → Segment by user type
3. **Shallow Insights** → Follow-up interviews

## Learning Outcomes

- Plan effective research studies
- Conduct insightful interviews
- Design valid surveys
- Synthesize research data
- Present actionable insights
