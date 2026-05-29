---
name: hypothesis-tracking
version: "1.0.0"
description: "Track and manage research hypotheses with confidence levels. Use when the user asks about prior research, wants to validate claims, or queries what is known about a company."

tools:
  - get_hypotheses
  - save_hypothesis

resources:
  - file://references/confidence_levels

metadata:
  openclaw:
    requires:
      bins:
        - primr-mcp
      env:
        - GEMINI_API_KEY
---

# Hypothesis Tracking

Primr uses a four-level confidence system: UNTESTED, VALIDATED, INVALIDATED, CONFIRMED. See `references/confidence-levels.md` for the full framework and lifecycle.

## Operational Capabilities

### Retrieve Hypotheses

```
get_hypotheses(company="Acme Corp")
get_hypotheses(company="Acme Corp", confidence="validated")
get_hypotheses(company="Acme Corp", topic="technology")
get_hypotheses(company="Acme Corp", include_expired=True)
```

### Update Hypothesis Confidence

```
save_hypothesis(company="Acme Corp", hypothesis_id="h_001",
    confidence="validated", evidence="Found AWS case study on company blog")

save_hypothesis(company="Acme Corp", hypothesis_id="h_002",
    confidence="invalidated", evidence="CEO states they use Azure exclusively")

save_hypothesis(company="Acme Corp", hypothesis_id="h_001",
    confidence="confirmed", evidence="Multiple sources: job posts, blog, press release")
```

### Create New Hypothesis

```
save_hypothesis(company="Acme Corp", hypothesis_id="h_new_001",
    claim="Company is expanding into healthcare",
    confidence="untested", topic="strategy")
```

## Expiration Rules

- Financial claims: 90 days
- Technology claims: 180 days
- Strategy claims: 365 days
- Leadership claims: no expiration

When expired hypotheses exist, query with `include_expired=True`, then re-validate, invalidate, or extend.

## Error Handling

| Error | Resolution |
|-------|------------|
| Hypothesis not found | Verify company name and hypothesis_id |
| Duplicate ID | Use a unique hypothesis_id per company |
| Missing evidence | Always provide evidence string when changing confidence |
| Expired hypothesis | Re-query with `include_expired=True` to access |

## Example Workflow

```
User: "What do we know about Acme Corp's technology?"

1. get_hypotheses("Acme Corp", topic="technology")

   Results:
   - [CONFIRMED] Uses microservices architecture
     Evidence: CTO interview, job posts, tech blog
   - [VALIDATED] AWS as primary cloud
     Evidence: Job posting mentions AWS
   - [UNTESTED] Considering Kubernetes migration
     Evidence: None yet

2. Present to user:
   "Here's what we know about Acme Corp's technology:

   CONFIRMED: Uses microservices architecture
     Multiple sources confirm this

   VALIDATED: AWS as primary cloud
     One supporting source (job posting)

   UNTESTED: Considering Kubernetes migration
     No evidence yet, extracted from blog speculation

   Would you like me to research any of these further?"

3. If user provides new evidence:
   save_hypothesis(company="Acme Corp", hypothesis_id="h_003",
       confidence="validated",
       evidence="User confirmed: spoke with Acme engineer at conference")
```

## Constraints

- **Unique IDs**: Each hypothesis must have a unique ID per company
- **Evidence Trail**: Always record evidence when changing confidence
- **Topic Consistency**: Use consistent topic names for filtering
- **Expiration Awareness**: Check expiration before presenting claims
