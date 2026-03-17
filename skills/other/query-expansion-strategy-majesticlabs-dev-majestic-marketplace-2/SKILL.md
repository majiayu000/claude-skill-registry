---
name: query-expansion-strategy
description: Query fan-out coverage for AI visibility. Covers semantic variation analysis and sub-question targeting.
allowed-tools: WebSearch
---

# Query Expansion Strategy

Maximize AI visibility through query fan-out coverage.

## How LLMs Process Queries

LLMs expand queries into 5-10 semantic variations (sub-questions) before generating responses. To get cited:

1. Cover topic clusters comprehensively
2. Include semantic variations naturally
3. Address related questions
4. Build entity relationships
5. Create topical depth

## Query Fan-Out Analysis

**Example:** "How to prioritize leads" fans out to:
- "What methodologies exist for lead prioritization?"
- "What tools help with lead scoring?"
- "What metrics indicate lead quality?"
- "How do sales teams rank prospects?"
- "What is lead scoring automation?"

Your content must answer ALL sub-questions to maximize visibility.

## Tools for Fan-Out Analysis

| Tool | Use |
|------|-----|
| Kuforia | Visualizes how AI breaks down topics |
| Dan's Fan-out Tool | Shows sub-question decomposition |
| ChatGPT/Perplexity | Ask "what sub-questions would you ask to answer X?" |

## Semantic Coverage Checklist

For any target topic:

1. **Core question** - Direct answer to primary query
2. **Definition** - What is X? (for newcomers)
3. **How-to** - How do you do X?
4. **Why** - Why is X important?
5. **Comparison** - How does X compare to Y?
6. **Examples** - What are examples of X?
7. **Tools** - What tools help with X?
8. **Metrics** - How do you measure X?
9. **Mistakes** - What mistakes to avoid with X?
10. **Trends** - What's changing about X?

## Content Structure for Fan-Out

**Recommended sections:**

```markdown
## What is [Topic]?
[Definition for newcomers]

## Why [Topic] Matters
[Business case, importance]

## How to [Topic]
[Step-by-step methodology]

## [Topic] Tools and Software
[Tool comparison table]

## [Topic] Metrics to Track
[KPIs and measurement]

## Common [Topic] Mistakes
[What to avoid]

## FAQ
### [Sub-question 1]?
[Complete answer]

### [Sub-question 2]?
[Complete answer]
```

## Semantic Footprint Expansion

Build entity relationships around your topic:

```
Primary Topic: Lead Scoring
├── Related Concepts: lead qualification, MQL, SQL, BANT
├── Tools: HubSpot, Salesforce, Marketo
├── Metrics: conversion rate, lead velocity
├── Personas: sales rep, marketing manager, SDR
└── Use Cases: B2B sales, SaaS, enterprise
```

Include related terms naturally throughout content.

## Analysis Output

When analyzing content for query expansion:

```
Target Query: [query]

Sub-Questions Covered: X/10
☑ Definition/What is
☑ How-to/Process
☐ Why/Importance (MISSING)
☐ Comparison (MISSING)
☑ Tools/Software
...

Semantic Coverage: X%
Missing Entities: [list]

Recommendations:
1. Add section on [missing sub-question]
2. Include comparison with [related concept]
3. Add FAQ addressing [query variation]
```
