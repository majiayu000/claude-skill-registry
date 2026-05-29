---
name: hypothesis-tracking
version: "2.0.0"
description: "Confidence level management and hypothesis lifecycle"

metadata:
  openclaw:
    requires:
      bins:
        - primr-mcp
      env:
        - GEMINI_API_KEY

mcp_server: primr
tools:
  - get_hypotheses
  - save_hypothesis
resources:
  - primr://memory/{company}
---

# Hypothesis Tracking Skill (v2.0)

You are an expert at managing research hypotheses, tracking confidence levels, and maintaining epistemic rigor.

## Confidence Level Framework

Primr uses a four-level confidence system:

| Level | Meaning | Evidence Required |
|-------|---------|-------------------|
| `UNTESTED` | Claim extracted, not yet verified | None (initial state) |
| `VALIDATED` | Supporting evidence found | At least one corroborating source |
| `INVALIDATED` | Contradicting evidence found | At least one contradicting source |
| `CONFIRMED` | High confidence, multiple sources | Multiple independent sources |

## Hypothesis Lifecycle

```
                    ┌─────────────┐
                    │  UNTESTED   │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │  VALIDATED  │ │ INVALIDATED │ │  (remains)  │
    └──────┬──────┘ └─────────────┘ └─────────────┘
           │
           ▼
    ┌─────────────┐
    │  CONFIRMED  │
    └─────────────┘
```

## Hypothesis Structure

```yaml
hypothesis:
  id: "h_001"                    # Unique identifier
  claim: "Company uses AWS"      # The testable claim
  confidence: validated          # Current confidence level
  evidence:                      # Supporting/contradicting evidence
    - "Job posting mentions AWS certifications"
    - "CTO blog post discusses AWS migration"
  topic: "technology"            # Category for filtering
  created_at: "2026-02-01T10:00:00"
  updated_at: "2026-02-03T14:30:00"
  expires_at: "2026-05-01T10:00:00"  # Optional expiration
```

## Operational Capabilities

### 1. Retrieve Hypotheses

**Tool**: `get_hypotheses`

```
# Get all hypotheses for a company
get_hypotheses(company="Acme Corp")

# Filter by confidence level
get_hypotheses(company="Acme Corp", confidence="validated")

# Filter by topic
get_hypotheses(company="Acme Corp", topic="technology")

# Include expired hypotheses
get_hypotheses(company="Acme Corp", include_expired=True)
```

### 2. Update Hypothesis Confidence

**Tool**: `save_hypothesis`

```
# Validate a hypothesis
save_hypothesis(
    company="Acme Corp",
    hypothesis_id="h_001",
    confidence="validated",
    evidence="Found AWS case study on company blog"
)

# Invalidate a hypothesis
save_hypothesis(
    company="Acme Corp",
    hypothesis_id="h_002",
    confidence="invalidated",
    evidence="CEO interview states they use Azure exclusively"
)

# Confirm with high confidence
save_hypothesis(
    company="Acme Corp",
    hypothesis_id="h_001",
    confidence="confirmed",
    evidence="Multiple sources confirm: job posts, blog, press release"
)
```

### 3. Create New Hypothesis

**Tool**: `save_hypothesis`

```
save_hypothesis(
    company="Acme Corp",
    hypothesis_id="h_new_001",  # New ID
    claim="Company is expanding into healthcare",
    confidence="untested",
    topic="strategy"
)
```

## Evidence Quality Guidelines

### Strong Evidence
- Direct quotes from company executives
- Official press releases
- SEC filings (for public companies)
- Published case studies
- Job postings with specific requirements

### Moderate Evidence
- Industry analyst reports
- News articles with named sources
- Partner announcements
- Conference presentations

### Weak Evidence
- Anonymous sources
- Speculation in articles
- Social media posts
- Outdated information (>1 year)

## Hypothesis Generation Patterns

### From Scrape Results
```
Analyst Subagent extracts claims:
- Technology stack mentions → technology hypotheses
- Leadership quotes → strategy hypotheses
- Financial mentions → financial hypotheses
- Market references → market hypotheses
```

### From Deep Research
```
External sources provide:
- Competitive positioning claims
- Market share estimates
- Growth trajectory claims
- Industry trend alignment
```

## Expiration Management

### When to Set Expiration
- Financial claims: 90 days (quarterly updates)
- Technology claims: 180 days (tech changes)
- Strategy claims: 365 days (annual planning)
- Leadership claims: No expiration (until change)

### Handling Expired Hypotheses
```
1. Query with include_expired=True
2. Review expired hypotheses
3. Either:
   - Re-validate with fresh evidence
   - Mark as invalidated if no longer true
   - Extend expiration if still relevant
```

## Example Workflow

```
User: "What do we know about Acme Corp's technology?"

Agent:
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
   
   ✓ CONFIRMED: Uses microservices architecture
     - Multiple sources confirm this
   
   ✓ VALIDATED: AWS as primary cloud
     - One supporting source (job posting)
   
   ? UNTESTED: Considering Kubernetes migration
     - No evidence yet, extracted from blog speculation
   
   Would you like me to research any of these further?"

3. If user provides new evidence:
   save_hypothesis(
       company="Acme Corp",
       hypothesis_id="h_003",
       confidence="validated",
       evidence="User confirmed: spoke with Acme engineer at conference"
   )
```

## Constraints

- **Unique IDs**: Each hypothesis must have a unique ID per company
- **Evidence Trail**: Always record evidence when changing confidence
- **Topic Consistency**: Use consistent topic names for filtering
- **Expiration Awareness**: Check expiration before presenting claims
