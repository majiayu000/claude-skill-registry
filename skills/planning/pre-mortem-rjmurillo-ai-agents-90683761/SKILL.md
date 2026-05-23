---
name: pre-mortem
description: Guide prospective hindsight analysis to identify project risks before failure occurs. Teams imagine the project has failed spectacularly, then work backward to identify causes. Increases risk identification by 30% compared to traditional planning.
license: MIT
metadata:
  version: 1.0.0
  model: claude-sonnet-4-5
  author: SkillForge
  academic_source: "HBR 2007 - Performing a Project Premortem by Gary Klein"
---

# Pre-Mortem Risk Identification

When this skill activates, you become a pre-mortem facilitator. Your role is to guide users through prospective hindsight analysis, helping them identify project risks by imagining failure has already occurred.

## Triggers

Activate when the user:

- "Run a pre-mortem on..."
- "What could cause this project to fail?"
- "Identify project risks for..."
- "What could go wrong with..."
- "Risk identification for..."
- "Pre-mortem analysis"

## Quick Reference

| Phase | Duration | Output |
|-------|----------|--------|
| 1. Brief | 2-3 min | Project context documented |
| 2. Failure Announcement | 30 sec | Mindset shift established |
| 3. Independent Analysis | 3-5 min | Individual failure reasons |
| 4. Round-Robin Collection | 5-10 min | Consolidated failure list |
| 5. Review and Mitigate | 10-15 min | Risk inventory with mitigations |

## Why Pre-Mortem Works

Research by Gary Klein demonstrates that **prospective hindsight** (imagining an event has already occurred) increases the ability to identify reasons for outcomes by 30%.

**Key psychological benefits:**

1. **Reduces "damn-the-torpedoes" attitude** - Acknowledging failure is possible
2. **Creates psychological safety** - Dissenters can voice concerns as analysis, not criticism
3. **Surfaces hidden knowledge** - People share what they know but fear saying
4. **Catches blind spots early** - Before commitment and sunk costs

## Process

### Phase 1: Project Brief (2-3 minutes)

**Input Required:**

- Project name and objective
- Timeline and key milestones
- Team composition (if team context)
- Success criteria

**Actions:**

1. Document the project scope clearly
2. Identify key stakeholders
3. Note any constraints or dependencies
4. Confirm understanding with user

**Output:** Project context document

### Phase 2: Failure Announcement (30 seconds)

**The critical mindset shift.**

Announce to the user (or team):

> "The project has failed. It is [timeline endpoint]. The project did not just miss its goals, it failed spectacularly. Your task now is to identify all the reasons why it failed."

**Important:** Use past tense. The failure has already happened. This is not speculation about what "might" happen; it "did" happen.

### Phase 3: Independent Analysis (3-5 minutes)

**For individual context:**

- User writes down 5-10 reasons why the project failed
- No filtering or evaluation yet
- Include both obvious and "unlikely" causes
- Consider technical, human, organizational, and external factors

**For team context:**

- Each person writes independently
- No discussion or sharing yet
- Silent reflection maximizes diversity of thought

**Prompt the user:**
> "Write down every reason you can think of for why this project failed. Include causes you consider unlikely. Do not filter yourself. You have 3-5 minutes."

**Output:** Raw list of failure reasons

### Phase 4: Round-Robin Collection (5-10 minutes)

**For individual context:**

- Review each failure reason
- Group by category (see Categories below)
- No evaluation yet, just collection

**For team context:**

- Go around the room, each person shares ONE reason
- Continue rounds until all reasons exhausted
- Record without discussion or debate
- No "that won't happen" or "we already thought of that"

**Categories for grouping:**

1. **Technical** - Technology, architecture, implementation
2. **People** - Skills, availability, communication
3. **Process** - Methodology, workflow, coordination
4. **Organizational** - Politics, priorities, resources
5. **External** - Market, competitors, regulations, dependencies
6. **Unknown Unknowns** - Black swan events, assumptions

**Output:** Categorized failure reasons

### Phase 5: Review and Mitigate (10-15 minutes)

**For each failure reason:**

1. **Assess likelihood** (1-5 scale)
   - 1: Very unlikely
   - 2: Unlikely
   - 3: Possible
   - 4: Likely
   - 5: Very likely

2. **Assess impact** (1-5 scale)
   - 1: Minor inconvenience
   - 2: Delays
   - 3: Significant setback
   - 4: Major failure
   - 5: Project-killing

3. **Calculate risk score**: Likelihood x Impact

4. **Identify mitigation strategies:**
   - Prevention: How to stop it from happening
   - Detection: How to know early if it is happening
   - Response: What to do if it happens

5. **Assign ownership** (if team context)

**Prioritization:**

- Risk score 15-25: Critical, address immediately
- Risk score 8-14: High, plan mitigation
- Risk score 4-7: Medium, monitor
- Risk score 1-3: Low, accept or defer

**Output:** Complete risk inventory (see template)

## Output Template

Generate the risk inventory using this structure:

```markdown
# Pre-Mortem Risk Inventory

**Project:** [Name]
**Date:** [Date]
**Participants:** [Names or "Individual Analysis"]

## Project Context

- **Objective:** [What success looks like]
- **Timeline:** [Start to end]
- **Key Dependencies:** [Critical external factors]

## Risk Summary

| Priority | Count | Top Risk |
|----------|-------|----------|
| Critical | N | [Highest scoring risk] |
| High | N | [Second highest category risk] |
| Medium | N | |
| Low | N | |

## Critical Risks (Score 15-25)

### R1: [Risk Name]

- **Category:** [Technical/People/Process/Organizational/External]
- **Failure Scenario:** [How this causes project failure]
- **Likelihood:** [1-5] | **Impact:** [1-5] | **Score:** [L x I]
- **Root Cause:** [Why this might happen]
- **Mitigation:**
  - Prevention: [How to avoid]
  - Detection: [Early warning signs]
  - Response: [Contingency plan]
- **Owner:** [Person responsible]
- **Status:** [Open/Mitigating/Accepted]

[Repeat for each critical risk]

## High Risks (Score 8-14)

[Same structure as Critical]

## Medium Risks (Score 4-7)

[Abbreviated: Name, Category, Score, One-line mitigation]

## Low Risks (Score 1-3)

[List only: Name and score]

## Action Items

| Action | Owner | Due Date | Risk Addressed |
|--------|-------|----------|----------------|
| [Specific action] | [Name] | [Date] | R1, R3 |

## Review Schedule

- **Next review:** [Date]
- **Review frequency:** [Weekly/Bi-weekly/Monthly]
```

## Scripts

### pre-mortem.py

Validates risk inventory completeness and calculates aggregate statistics.

```bash
python3 .claude/skills/pre-mortem/scripts/pre-mortem.py \
  --inventory-path <path-to-risk-inventory.md> \
  --validate
```

**Exit Codes:**

- 0: Valid inventory with all required fields
- 1: Invalid arguments
- 10: Validation failed (missing required sections)

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Skipping Phase 2 | Mindset shift is critical for effectiveness | Always announce failure explicitly |
| Allowing discussion during Phase 3 | Reduces diversity of thought | Enforce silent writing |
| Filtering "unlikely" causes | Miss black swan events | Include all causes, prioritize later |
| Stopping at identification | Risk without mitigation is incomplete | Always complete Phase 5 |
| One-time exercise | Projects evolve, new risks emerge | Schedule periodic reviews |

## Facilitation Tips

**For team settings:**

- Emphasize no blame or criticism
- Senior members speak last in round-robin
- Celebrate thorough risk identification
- Treat skeptics as valuable, not negative

**For individual use:**

- Role-play multiple perspectives (developer, user, manager)
- Challenge your own assumptions explicitly
- Consider "what would my critics say?"

## Extension Points

1. **Custom Categories:** Add domain-specific risk categories
2. **Risk Templates:** Pre-built risks for common project types
3. **Integration:** Link to issue trackers for action item follow-up
4. **Quantification:** Add financial impact estimation

## Related Skills

| Skill | Relationship |
|-------|--------------|
| decision-critic | Post-decision validation (pre-mortem is pre-decision) |
| planner | Use pre-mortem output to inform planning |
| architect | Technical risks feed into ADR considerations |

## References

- Klein, G. (2007). "Performing a Project Premortem." Harvard Business Review.
- Mitchell, D. J., et al. (1989). "Back to the Future: Temporal Perspective in the Explanation of Events." Journal of Behavioral Decision Making.
