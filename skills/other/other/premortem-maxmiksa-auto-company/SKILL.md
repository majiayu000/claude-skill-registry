---
name: premortem
description: Pre-mortem analysis that imagines a plan has failed, then works backward to identify causes and preventions. Use before launches, major decisions, or risky initiatives to surface hidden risks.
user-invocable: true
---

# Pre-Mortem Analysis

Imagine the plan has completely failed, then work backward to identify what went wrong and how to prevent it.

## Instructions

Set the scene: "It's [timeframe] in the future. This initiative was a complete disaster. Looking back, what happened?"

Generate failure scenarios without filtering for likelihood—get everything on the table first, then prioritize.

### Output Format

**The Plan**
Summarize what's being attempted and the success criteria.

**Time Jump**
"It's [X months] later. This has failed completely. The outcome: [describe the disaster vividly]."

**What Went Wrong**

Generate 8-12 plausible failure causes across categories:

| Category | Failure Mode | How It Played Out |
|----------|--------------|-------------------|
| Execution | [What failed] | [The story of how] |
| External | [What failed] | [The story of how] |
| People | [What failed] | [The story of how] |
| Technical | [What failed] | [The story of how] |
| Assumptions | [What failed] | [The story of how] |

**Risk Prioritization**

| Failure Mode | Likelihood | Impact | Priority |
|--------------|------------|--------|----------|
| ... | High/Med/Low | High/Med/Low | 1-5 |

**Top 3 Risks & Mitigations**

For each top risk:
- **Risk**: [Description]
- **Early Warning Signs**: What would indicate this is happening?
- **Prevention**: How to reduce likelihood
- **Mitigation**: How to reduce impact if it occurs
- **Owner**: Who's responsible for watching this?

**Pre-Mortem Insights**
What did this exercise reveal that wasn't obvious before?

**Revised Confidence**
After this analysis, how confident are you in success? What would increase confidence?

## Guidelines

- Be vivid and specific—"the database corrupted" not "something went wrong"
- Include uncomfortable possibilities (key person leaves, competitor moves, we were wrong)
- Don't filter for "that won't happen"—the point is to surface hidden concerns
- Assign real owners to mitigations
- Look for single points of failure

$ARGUMENTS
