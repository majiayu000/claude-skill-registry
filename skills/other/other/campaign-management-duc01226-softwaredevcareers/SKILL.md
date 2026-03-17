---
name: campaign-management
description: Activate for marketing campaign planning, execution, and optimization. Use when launching campaigns, coordinating multi-channel efforts, managing budgets, or tracking campaign performance.
license: MIT
---

# Campaign Management

End-to-end campaign planning, execution, and optimization frameworks.

## When to Use

- Campaign planning
- Multi-channel coordination
- Budget allocation
- Timeline management
- Launch execution
- Performance tracking
- Campaign optimization

## Core Capabilities

### Campaign Brief Template
Load: `references/campaign-brief.md`

### Launch Checklist
Load: `references/launch-checklist.md`

### Budget Planning
Load: `references/budget-allocation.md`

### Optimization Framework
Load: `references/optimization-framework.md`

## Quick Reference

**Campaign Types:**
- Product Launch
- Seasonal/Promotional
- Brand Awareness
- Lead Generation
- Re-engagement

**Key Milestones:**
- Brief approved
- Assets complete
- Tech setup done
- Launch
- Mid-campaign review
- Post-mortem

## Workflow

### Campaign Planning
1. Define objective and KPIs
2. Identify target audience
3. Set budget and timeline
4. Plan channel mix
5. Create campaign brief
6. Develop creative strategy
7. Build asset list

### Campaign Execution
1. Complete all assets
2. Set up tracking/pixels
3. Configure campaigns in platforms
4. QA all elements
5. Launch
6. Monitor first 24-48 hours
7. Optimize based on data

### Post-Campaign
1. Compile performance data
2. Analyze vs. targets
3. Document learnings
4. Identify winners/losers
5. Create post-mortem report

## Output Format

```markdown
## Campaign Brief: [Name]

**Objective:** [Goal]
**KPIs:** [Metrics + targets]
**Timeline:** [Start - End]
**Budget:** $[X]
**Target Audience:** [Segment]

### Channel Mix
| Channel | Budget | Role |
|---------|--------|------|

### Key Messages
[Primary and secondary messages]

### Creative Requirements
[Asset list with specs]

### Success Criteria
[What defines success]
```

## Report Output

**Activate:** `assets-organizing` skill for report file paths

| Report Type | Path |
|-------------|------|
| Campaign Reports | `assets/reports/campaigns/{date}-{campaign}-report.md` |
| Post-Mortems | `assets/reports/campaigns/{date}-{campaign}-postmortem.md` |
| Performance | `assets/reports/performance/{date}-weekly.md` |

## Agent Integration

**Primary Agents:** campaign-manager, data-analyst, content-creator

**Skill Dependencies:** creativity, assets-organizing (report organization)

## Best Practices

1. Start with objective, not tactics
2. Plan tracking before launch
3. Build in buffer time
4. Test small before scaling
5. Review at regular intervals
6. Document everything
