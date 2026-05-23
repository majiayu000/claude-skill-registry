---
name: product-management
description: Assist with core product management activities including writing PRDs, analyzing features, synthesizing user research, planning roadmaps, and communicating product decisions. Use when you need help with PM documentation, analysis, or planning workflows that integrate with your codebase.
---
# Skill: Product management AI

## Purpose

Assist with core product management activities including writing product requirements documents (PRDs), analyzing feature requests, synthesizing user research, planning roadmaps, and communicating product decisions to stakeholders and engineering teams.

## When to use this skill

- You need to **write or update PRDs** with clear requirements, success metrics, and technical considerations.
- You're **evaluating feature requests** and need structured analysis of impact, effort, and priority.
- You need to **synthesize user research** findings into actionable insights.
- You're **planning roadmaps** and need to organize, prioritize, and communicate plans.
- You need to **communicate product decisions** clearly to engineering, design, and business stakeholders.
- You're doing **competitive analysis** or market research synthesis.
- You need to **track and analyze product metrics** to inform decisions.

## Key capabilities

Unlike point-solution PM tools:

- **Integrated with codebase**: Can reference actual code, APIs, and technical constraints.
- **Context-aware**: Understands your specific product, architecture, and technical debt.
- **Flexible templates**: Adapt documentation to your organization's needs.
- **Version controlled**: All artifacts live in git alongside code.
- **Collaborative**: Works within existing dev workflows (PRs, issues, docs).

## Inputs

- **Product context**: Current state, key stakeholders, strategic goals.
- **Feature requests**: User feedback, business needs, or strategic initiatives.
- **Technical constraints**: Known limitations, dependencies, or technical debt.
- **User research**: Interview notes, survey results, analytics data.
- **Business goals**: Metrics, OKRs, or success criteria to optimize for.

## Out of scope

- Making final product decisions (this is the PM's job; the skill assists).
- Managing stakeholder relationships and politics.
- Detailed UI/UX design work (use design tools and collaborate with designers).
- Project management and sprint planning (use project management tools).

## Conventions and best practices

### PRD structure
A good PRD should include:

1. **Problem statement**: What user pain point or business need are we addressing?
2. **Goals and success metrics**: What does success look like quantitatively?
3. **User stories and use cases**: Who will use this and how?
4. **Requirements**: Functional and non-functional requirements, prioritized.
5. **Technical considerations**: Architecture implications, dependencies, constraints.
6. **Design and UX notes**: Key interaction patterns or design requirements.
7. **Risks and mitigations**: What could go wrong and how to address it.
8. **Launch plan**: Rollout strategy, feature flags, monitoring.
9. **Open questions**: What still needs to be decided or researched.

### Feature prioritization
Use structured frameworks to evaluate features:

- **RICE**: Reach × Impact × Confidence / Effort
- **ICE**: Impact × Confidence × Ease
- **Value vs. Effort**: 2×2 matrix plotting value against implementation cost
- **Kano Model**: Categorize features into basic, performance, and delighters

### User research synthesis
When synthesizing research:

1. **Identify patterns**: What themes emerge across participants?
2. **Quote verbatim**: Include actual user quotes to illustrate points.
3. **Quantify when possible**: "7 out of 10 participants said..."
4. **Segment findings**: Different user types may have different needs.
5. **Connect to metrics**: How do qualitative findings explain quantitative data?

### Roadmap planning
Effective roadmaps should:

- **Theme-based**: Group work into strategic themes, not just feature lists.
- **Time-horizoned**: Now / Next / Later or Quarterly structure.
- **Outcome-focused**: Emphasize goals and outcomes, not just outputs.
- **Flexible**: Leave room for learning and adjustment.
- **Communicated clearly**: Different views for different audiences.

## Required behavior

1. **Understand context deeply**: Review existing docs, code, and prior discussions before proposing changes.
2. **Ask clarifying questions**: Don't assume; clarify ambiguous requirements or goals.
3. **Be specific and actionable**: Avoid vague language; provide concrete, testable requirements.
4. **Consider tradeoffs**: Explicitly discuss pros/cons of different approaches.
5. **Connect to strategy**: Tie features and decisions back to higher-level goals.
6. **Involve stakeholders**: Identify who needs to review or approve.
7. **Think through edge cases**: Don't just focus on happy paths.
8. **Make it measurable**: Propose concrete metrics to track success.

## Required artifacts

Depending on the task, generate:

- **PRD document**: Comprehensive product requirements in markdown format.
- **Feature analysis**: Structured evaluation of a feature request.
- **Research synthesis**: Summary of user research findings with insights.
- **Roadmap document**: Organized view of planned work with themes and timelines.
- **Decision document**: Record of key product decisions and rationale.
- **Competitive analysis**: Comparison of competitor features and approaches.
- **Metric definitions**: Clear definitions of success metrics and how to measure them.

## Implementation checklist

### Writing a PRD
- [ ] Understand the problem space and strategic context
- [ ] Review related code, APIs, and technical constraints
- [ ] Interview key stakeholders (engineering, design, business)
- [ ] Research user needs and competitive landscape
- [ ] Draft problem statement and goals
- [ ] Define user stories and use cases
- [ ] Specify functional and non-functional requirements
- [ ] Document technical considerations and dependencies
- [ ] Define success metrics and measurement approach
- [ ] Identify risks and mitigation strategies
- [ ] Plan rollout and launch approach
- [ ] Review with stakeholders and iterate

### Analyzing a feature request
- [ ] Clarify the user problem or business need
- [ ] Identify target users and use cases
- [ ] Estimate impact (users affected, business value)
- [ ] Assess implementation effort and complexity
- [ ] Identify dependencies and risks
- [ ] Check alignment with product strategy
- [ ] Compare against alternatives
- [ ] Calculate prioritization score (RICE, ICE, etc.)
- [ ] Make recommendation with clear reasoning

### Synthesizing user research
- [ ] Review all research materials (transcripts, notes, data)
- [ ] Identify key themes and patterns
- [ ] Extract representative quotes
- [ ] Segment findings by user type if relevant
- [ ] Connect qualitative findings to quantitative data
- [ ] Formulate insights and implications
- [ ] Generate actionable recommendations
- [ ] Prioritize recommendations by impact

### Planning a roadmap
- [ ] Review strategic goals and OKRs
- [ ] Collect input from stakeholders
- [ ] Assess current state and technical debt
- [ ] Group potential work into strategic themes
- [ ] Prioritize themes and initiatives
- [ ] Estimate sizing and dependencies
- [ ] Organize into time horizons (Now/Next/Later)
- [ ] Define success criteria for each initiative
- [ ] Create views for different audiences
- [ ] Review and socialize with stakeholders

## Example workflows

### Example 1: Writing a PRD for a new feature

```markdown
# PRD: Advanced Search Functionality

## Problem Statement
Users frequently report difficulty finding specific items in our catalog when they have multiple criteria (price range, location, category, features). Our current search only supports simple text queries, leading to:
- High bounce rates on search results pages (65% bounce rate vs 32% site average)
- Increased support tickets asking for search help (150/month)
- Lost conversion opportunities (estimated $500K annual revenue impact)

## Goals and Success Metrics
**Primary Goal**: Enable users to find relevant items quickly using multiple filters.

**Success Metrics**:
- Reduce search result page bounce rate from 65% to <40%
- Increase search-to-purchase conversion rate by 25%
- Reduce search-related support tickets by 50%
- 70% of users engage with at least one filter within 30 days

## User Stories

### Must Have
1. As a buyer, I want to filter by price range so I can find items within my budget
2. As a buyer, I want to filter by location so I can find items near me
3. As a buyer, I want to filter by category so I can narrow down item types
4. As a buyer, I want to combine multiple filters so I can find exactly what I need
5. As a buyer, I want to see filter counts so I know how many items match before applying

### Should Have
6. As a buyer, I want to save my filter preferences so I don't have to reapply them
7. As a buyer, I want to see suggested filters based on my search query
8. As a buyer, I want to sort filtered results by relevance, price, or date

### Nice to Have
9. As a buyer, I want to create saved searches that notify me of new matches
10. As a buyer, I want to share a filtered search URL with others
```

### Example 2: Feature request analysis

```markdown
# Feature Analysis: Dark Mode Support

## Request Summary
**Source**: User feedback (150+ requests in past 6 months), competitive pressure
**Description**: Add dark mode theme option to web and mobile apps

## User Need
Users working in low-light environments report eye strain with current light-only theme. Power users (25% of DAU) spend 3+ hours/day in app and strongly prefer dark mode.

## Prioritization Score

Using RICE framework:
- **Reach**: 750K users = 750
- **Impact**: 8/10 (high for target segment) = 0.8
- **Confidence**: 85% = 0.85
- **Effort**: 7 weeks = 7

**RICE Score**: (750 × 0.8 × 0.85) / 7 = **73.2**

## Recommendation

**Proceed with Option 1 (Full Dark Mode)**

**Reasoning**:
- High impact for large user segment (45% of base)
- Strong user demand and competitive pressure
- Effort is reasonable relative to value
- RICE score above our threshold (>50)
- Aligns with product, technical, and business strategy
```

## Common PM artifacts

### PRD (Product Requirements Document)
Comprehensive specification of what to build and why. Include problem statement, goals, user stories, requirements, technical considerations, risks, and launch plan.

### Feature Brief
Lighter-weight than PRD; quick summary of a feature idea with key details. Use for early-stage exploration before committing to full PRD.

### User Research Synthesis
Summary of user research findings (interviews, surveys, usability tests) with patterns, insights, and recommendations.

### Roadmap
Strategic plan of what to build over time. Organize by themes and time horizons; focus on outcomes not just outputs.

### Decision Document
Record of important product decisions, the options considered, the decision made, and the reasoning. Critical for institutional memory.

### Launch Plan
Detailed plan for rolling out a feature including phases, feature flags, metrics, monitoring, and rollback procedures.

### Competitive Analysis
Comparison of competitors' features, approaches, and positioning. Inform product strategy and feature prioritization.

### One-Pager
Executive summary of a product initiative. Use to communicate to leadership and get alignment.

## Best practices for AI-assisted PM work

### When using AI to write PRDs
- Provide comprehensive context about the product, users, and technical constraints.
- Review and edit generated content carefully; AI may miss nuances or make wrong assumptions.
- Use AI for structure and first drafts; refine with human judgment and stakeholder input.
- Validate technical details with engineering; don't assume AI knows your architecture.

### When using AI for feature analysis
- Provide quantitative data when possible (usage numbers, customer feedback counts).
- Use structured frameworks (RICE, ICE) to make analysis consistent and defensible.
- Don't let AI make the final decision; use it to organize thinking and surface considerations.
- Supplement AI analysis with qualitative stakeholder input and strategic context.

### When using AI for research synthesis
- Provide full transcripts or detailed notes for best results.
- Ask AI to identify patterns but validate with your own reading of the data.
- Use AI to extract quotes and organize themes; add your own interpretation and implications.
- Don't let AI over-summarize; sometimes important details are in the nuances.

## Safety and escalation

- **Strategic decisions**: AI should inform, not make, key product decisions. Involve human PMs and stakeholders.
- **User data**: Don't feed PII or sensitive user data to AI without proper data handling procedures.
- **Technical feasibility**: Always validate technical assumptions and effort estimates with engineering.
- **Competitive intelligence**: Be cautious about including confidential competitive info in prompts.
- **Tone and voice**: Review and adjust tone for your audience; AI may be too formal or informal.

## Integration with other skills

This skill can be combined with:

- **Data querying**: To analyze product metrics and user behavior data.
- **AI data analyst**: To perform deeper quantitative analysis for feature decisions.
- **Frontend UI integration**: To implement features designed in PRDs.
- **Internal tools**: To build PM tools like feature flag dashboards or metrics viewers.
