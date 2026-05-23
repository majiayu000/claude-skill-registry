---
name: thinking-lindy-effect
description: For non-perishable things, future life expectancy is proportional to current age. Use for technology selection, evaluating frameworks/libraries, and predicting tool longevity.
---

# The Lindy Effect

## Overview

The Lindy Effect, named after a New York deli where comedians discussed career longevity, states that for non-perishable things (ideas, technologies, books, practices), future life expectancy is proportional to current age. If a technology has survived 20 years, it's likely to survive another 20. If it's survived 2 years, expect another 2.

**Core Principle:** Time is the ultimate test. Old things that still exist have proven their value; new things are still being tested.

## When to Use

- Technology selection (languages, frameworks, databases)
- Evaluating libraries and dependencies
- Predicting tool longevity
- Career skill investment
- Methodology and practice adoption
- Architectural patterns
- Vendor/product selection

Decision flow:

```
Choosing between options?
  → Are some options significantly older? → yes → APPLY LINDY HEURISTIC
  → Is longevity important for this choice? → yes → FAVOR OLDER, PROVEN OPTIONS
  → Is the new thing solving a new problem? → yes → NEW MIGHT BE APPROPRIATE
```

## Understanding Lindy

### What Lindy Applies To (Non-Perishable)

- **Technologies:** Languages, databases, protocols
- **Ideas:** Mathematical concepts, design patterns, algorithms
- **Practices:** Testing, version control, code review
- **Books:** Technical references, foundational texts
- **Institutions:** Standards bodies, open source foundations

### What Lindy Doesn't Apply To (Perishable)

- **Hardware:** Physical degradation limits life
- **Individual careers:** Humans have biological limits
- **Specific products:** Companies can fail, be acquired
- **Fashion-driven choices:** Popularity cycles aren't Lindy

### The Math

```
Expected remaining life ≈ Current age

If survived 10 years → Expected to survive another ~10
If survived 50 years → Expected to survive another ~50
If survived 2 years → Expected to survive another ~2
```

## Applying Lindy to Technology

### Programming Languages

| Language | Age | Lindy Expectation | Evidence |
|----------|-----|-------------------|----------|
| C | 50+ years | 50+ more years | Powers OS, embedded, will outlive us |
| Java | 30 years | 30+ more years | Enterprise backbone, not going away |
| Python | 30 years | 30+ more years | Scientific computing, ML, scripting |
| Go | 15 years | 15+ more years | Proven for infra, backed by Google |
| Rust | 10 years | 10+ more years | Growing, solving real problems |
| New hotness | 2 years | 2-5 years | Unproven, might disappear |

### Databases

| Database | Age | Lindy Expectation | Notes |
|----------|-----|-------------------|-------|
| PostgreSQL | 35+ years | 35+ more years | SQL is 50+ years old |
| MySQL | 30 years | 30+ more years | LAMP stack foundation |
| MongoDB | 15 years | 15+ more years | Survived NoSQL hype cycle |
| CockroachDB | 10 years | 10+ more years | NewSQL, still proving itself |
| Latest DB | 2 years | Unknown | High risk for production use |

### Frameworks

| Framework | Age | Lindy Expectation | Notes |
|-----------|-----|-------------------|-------|
| React | 10+ years | 10+ more years | Dominant, ecosystem mature |
| Rails | 20 years | 20+ more years | Productive, battle-tested |
| Django | 18 years | 18+ more years | Python's Rails, stable |
| Express | 14 years | 14+ more years | Node.js standard |
| Newest framework | 1 year | 1-3 years | Likely to be replaced |

### Patterns and Practices

| Practice | Age | Lindy Expectation |
|----------|-----|-------------------|
| Version control | 50+ years | Permanent |
| Automated testing | 40+ years | Permanent |
| Code review | 40+ years | Permanent |
| Agile (core ideas) | 30+ years | Very long |
| CI/CD | 20+ years | Very long |
| Microservices | 10 years | Moderate |
| Latest methodology | 2 years | Unknown |

## The Lindy Decision Process

### Step 1: Assess Age of Options

For each option, determine how long it's been in significant use:

```markdown
Options for message queue:
- RabbitMQ: 17 years (2007)
- Kafka: 13 years (2011)
- NATS: 11 years (2013)
- NewQueue: 2 years (2022)
```

### Step 2: Apply Lindy Heuristic

```markdown
Lindy expectation:
- RabbitMQ: 17+ more years
- Kafka: 13+ more years
- NATS: 11+ more years
- NewQueue: 2-5 more years (high uncertainty)
```

### Step 3: Consider Context

Lindy is a heuristic, not a law. Consider:

```markdown
When older is better:
- Long-term production systems
- Core infrastructure
- Skills investment
- Dependencies with many consumers

When newer might be appropriate:
- Solving genuinely new problems
- Performance-critical new workloads
- Specific capability older tools lack
- Temporary/experimental projects
```

### Step 4: Calibrate by Ecosystem Age

A 5-year-old tool in a 5-year-old ecosystem is "old" for that ecosystem:

```markdown
Kubernetes ecosystem: ~10 years old
- Helm: 8 years → "Lindy" for K8s
- ArgoCD: 7 years → "Lindy" for K8s
- New tool: 1 year → Not Lindy yet

Node.js ecosystem: 14 years old
- Express: 14 years → Maximally Lindy for Node
- Fastify: 8 years → Moderately Lindy
- New framework: 1 year → Unproven
```

## Lindy Failure Modes

### Survivor Bias Confusion

Lindy predicts future survival given current survival. It doesn't say all old things are good:

```
Correct: "COBOL has survived 60 years, will survive 60 more"
Incorrect: "COBOL is the best choice for new projects"
(Survival ≠ Optimal for new use cases)
```

### Ignoring Paradigm Shifts

Lindy works within stable paradigms. Paradigm shifts create discontinuities:

```
- Pre-cloud: On-premise databases were Lindy
- Post-cloud: Managed databases emerged
- But: Core database concepts (SQL, ACID) remained Lindy
```

### Confusing Perishable and Non-Perishable

```
Perishable: Specific SaaS vendor → Can be acquired, pivoted, shut down
Non-perishable: The practice the vendor enables → Likely Lindy

E.g., Heroku might change, but "platform-as-a-service" concept is Lindy
```

## Lindy in Practice

### Technology Selection

```markdown
## Lindy Analysis: Database for New Product

Requirements: ACID transactions, relational data, long-term stability

Options:
| Option | Age | Lindy Score | Fit for Requirements |
|--------|-----|-------------|---------------------|
| PostgreSQL | 35 years | Excellent | Excellent |
| MySQL | 30 years | Excellent | Good |
| CockroachDB | 10 years | Good | Excellent |
| PlanetScale | 5 years | Moderate | Good |

Decision: PostgreSQL (Lindy + excellent fit)
         Consider CockroachDB for scale needs (worth the Lindy tax)
```

### Skill Investment

```markdown
## Lindy Career Analysis

Which skills to invest in?

Lindy skills (high confidence in future value):
- SQL (50+ years)
- Unix/Linux (50+ years)
- Git/version control (40+ years)
- Testing fundamentals (40+ years)

Moderate Lindy (good bet):
- Python (30+ years)
- JavaScript (28 years)
- Docker/containers (12 years)
- Kubernetes (10 years)

Low Lindy (speculative):
- Latest framework (1-3 years)
- Trending language (variable)

Investment strategy: Core in Lindy skills, experiments in new
```

### Dependency Selection

```markdown
## Lindy Dependency Audit

For each critical dependency:
| Dependency | Age | Last Update | Contributors | Lindy Risk |
|------------|-----|-------------|--------------|------------|
| lodash | 12 years | Active | Many | Low |
| express | 14 years | Active | Many | Low |
| new-lib | 1 year | Active | 3 | High |

Policy: Critical path requires 5+ year Lindy
        Experimental features can use newer dependencies
```

## Lindy Template

```markdown
# Lindy Analysis: [Decision]

## Options with Age
| Option | First Stable | Age | Category |
|--------|--------------|-----|----------|
| | | | Proven/Moderate/New |

## Lindy Expectations
| Option | Expected Longevity | Confidence |
|--------|-------------------|------------|
| | | High/Medium/Low |

## Context Adjustments
- Is this a new problem domain? [Yes/No]
- Is the ecosystem mature? [Yes/No]
- Do newer options solve critical gaps? [Yes/No]

## Lindy-Adjusted Decision
Primary choice: [Option with best Lindy + fit]
Rationale: [Why this balances Lindy with requirements]

## Risk if Lindy is Wrong
[What happens if the non-Lindy option outlasts expectations?]
```

## Verification Checklist

- [ ] Identified age of all options
- [ ] Applied Lindy heuristic to estimate longevity
- [ ] Distinguished perishable from non-perishable
- [ ] Considered paradigm shift possibilities
- [ ] Checked if newer options solve genuinely new problems
- [ ] Balanced Lindy with specific requirements
- [ ] Documented reasoning

## Key Questions

- "How long has this technology/practice existed?"
- "Is this Lindy (non-perishable) or perishable?"
- "What's the Lindy expectation for each option?"
- "Is the newer option solving a problem that didn't exist before?"
- "Am I betting against Lindy? If so, why?"
- "What's proven vs. what's hyped?"

## Taleb's Wisdom

"If a book has been in print for forty years, I can expect it to be in print for another forty years. But, and that is the main difference, if it survives another decade, then it will be expected to be in print another fifty years."

"Technology is at its best when it is invisible."

The technologies you don't think about—TCP/IP, Unix, SQL—are the most Lindy. The technologies that demand constant attention are still being tested.

"The old is to be respected; the new is to be examined."

Lindy doesn't mean reject the new. It means: the burden of proof is on the new. New must demonstrate value; old has already demonstrated survival.
