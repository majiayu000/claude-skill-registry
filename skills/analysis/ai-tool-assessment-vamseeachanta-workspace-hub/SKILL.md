---
name: ai-tool-assessment
description: Assess and report on AI tool subscriptions, usage patterns, and cost-effectiveness. Use for reviewing AI subscriptions, analyzing tool usage, optimizing AI spend.
version: 2.0.0
category: tools
last_updated: 2026-01-02
related_skills:
  - background-service-manager
  - session-start-routine
---

# AI Tool Usage Assessment

Assess and report on AI tool subscriptions, usage patterns, and cost-effectiveness.

## Overview

This skill provides a structured framework for evaluating AI tool subscriptions, identifying underutilized services, and optimizing AI-related spending. It generates comprehensive reports with actionable recommendations.

## Quick Start

1. **Trigger assessment** - Ask to "assess AI tools" or "review AI subscriptions"
2. **Answer questions** - Provide usage patterns when asked
3. **Review report** - Generated at `reports/ai-tool-assessment/assessment-YYYYMMDD.md`
4. **Take action** - Follow recommendations for optimization

```bash
# View latest assessment
cat reports/ai-tool-assessment/assessment-$(date +%Y%m%d).md

# List all assessments
ls -la reports/ai-tool-assessment/
```

## When to Use

- Monthly subscription reviews
- Quarterly budget planning
- When evaluating new AI tools
- After significant workflow changes
- Cost optimization initiatives
- Annual AI strategy reviews

## Trigger

User asks to assess AI tools, review AI subscriptions, or analyze AI tool usage.

## Instructions

When triggered, perform the following assessment:

### 1. Subscription Inventory

Review current paid memberships from `docs/AI_development_tools.md`:

| Service | Plan | Monthly Cost | Annual Cost |
|---------|------|--------------|-------------|
| Claude (Anthropic) | Max Plan | $106.60 | $1,279.20 |
| OpenAI | ChatGPT Plus | $21.28 | $255.36 |
| Google AI | Pro | $19.99 | $239.88 |
| GitHub Copilot | Pro | $8.88/mo | $106.60 |
| **TOTAL** | | **$156.75** | **$1,881.04** |

### 2. Tool Usage Analysis

Assess each tool category:

**Primary AI Assistants:**
- Claude Max: Code generation, complex reasoning, long-context tasks
- OpenAI Plus: Alternative perspective, GPT-4o access, DALL-E
- Google AI Pro: Gemini access, Google ecosystem integration

**Development Tools:**
- GitHub Copilot: Inline code completion, IDE integration
- Claude-flow: Multi-agent orchestration
- Factory.ai: Automated droids for CI/CD
- Google Antigravity: Agent-first IDE (in evaluation)

### 3. Generate Assessment Report

Create report at `reports/ai-tool-assessment/assessment-YYYYMMDD.md` with:

```markdown
# AI Tool Usage Assessment - [DATE]

## Executive Summary
- Total monthly spend: $X
- Primary tools in active use: [list]
- Tools underutilized: [list]
- Recommended actions: [list]

## Subscription Status
[Table of all subscriptions with renewal dates if known]

## Usage Patterns
[Analysis of which tools are used for what purposes]

## Cost-Effectiveness Analysis
| Tool | Cost/Month | Usage Level | Value Rating |
|------|------------|-------------|--------------|
| ... | ... | High/Medium/Low | 1-5 stars |

## Overlap Analysis
[Identify redundant capabilities across tools]

## Recommendations
1. [Keep/Cancel/Downgrade recommendations]
2. [Usage optimization suggestions]
3. [New tools to consider]

## Next Review Date
[Set quarterly review schedule]
```

### 4. Questions to Ask User

Before generating report, ask:
1. Which tools have you used most this month?
2. Are there specific tasks where one tool excels?
3. Any tools you haven't used in 30+ days?
4. New capabilities you need that current tools lack?

## Execution Checklist

Before assessment:
- [ ] Access to subscription documentation
- [ ] User available for questions
- [ ] Previous assessments reviewed (if any)

During assessment:
- [ ] All subscriptions inventoried
- [ ] Usage patterns documented
- [ ] Cost-effectiveness analyzed
- [ ] Overlap identified
- [ ] User questions asked

After assessment:
- [ ] Report generated in correct location
- [ ] Recommendations prioritized
- [ ] Next review date set
- [ ] Source docs updated if needed

## Error Handling

### Common Issues

**Error: Missing subscription data**
- Cause: `docs/AI_development_tools.md` not found or outdated
- Solution: Ask user for current subscription list, create/update doc

**Error: Incomplete usage data**
- Cause: User unsure about usage patterns
- Solution: Suggest tracking usage for 2 weeks before full assessment

**Error: Can't determine value**
- Cause: Tool usage overlaps with others
- Solution: Run overlap analysis first, identify unique value per tool

**Error: Outdated pricing**
- Cause: Subscription costs changed
- Solution: Verify current pricing on vendor websites

## Output

- Assessment report in `reports/ai-tool-assessment/`
- Updated `docs/AI_development_tools.md` if status changes
- Summary printed to console

## Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Cost per active tool | <$50/mo | Total spend / tools used weekly |
| Utilization rate | >70% | Tools used / tools subscribed |
| Value rating average | >3.5/5 | Average across all tools |
| Overlap reduction | <20% | Redundant capabilities identified |
| Assessment frequency | Quarterly | Days since last assessment |

## Report Templates

### Executive Summary Template

```markdown
## Executive Summary

**Assessment Date:** YYYY-MM-DD
**Review Period:** [Month/Quarter]
**Total Monthly Spend:** $XXX.XX

### Key Findings
1. [Primary finding]
2. [Secondary finding]
3. [Tertiary finding]

### Immediate Actions Required
- [ ] [Action 1]
- [ ] [Action 2]

### Long-term Recommendations
1. [Recommendation with timeline]
2. [Recommendation with timeline]
```

### Tool Comparison Template

```markdown
## Tool Comparison Matrix

| Capability | Claude | OpenAI | Google | Copilot |
|------------|--------|--------|--------|---------|
| Code Generation | ★★★★★ | ★★★★☆ | ★★★☆☆ | ★★★★☆ |
| Long Context | ★★★★★ | ★★★☆☆ | ★★★★☆ | N/A |
| IDE Integration | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★★ |
| Cost Value | ★★★☆☆ | ★★★★☆ | ★★★★★ | ★★★★★ |
```

## Best Practices

1. **Regular cadence** - Assess quarterly at minimum
2. **Track trends** - Compare assessments over time
3. **User feedback** - Include qualitative input
4. **Trial before commit** - Use free tiers to evaluate
5. **Document decisions** - Record why tools kept/cancelled
6. **Consider switching costs** - Factor in workflow disruption

## Related Skills

- [background-service-manager](../background-service-manager/SKILL.md) - For running assessment scripts
- [session-start-routine](../../meta/session-start-routine/SKILL.md) - Includes tool health checks

---

## Version History

- **2.0.0** (2026-01-02): Upgraded to v2 template - added Quick Start, When to Use, Execution Checklist, Error Handling, Metrics sections; enhanced frontmatter with version, category, related_skills
- **1.0.0** (2024-10-15): Initial release with subscription inventory, usage analysis, cost-effectiveness reporting, recommendation framework
