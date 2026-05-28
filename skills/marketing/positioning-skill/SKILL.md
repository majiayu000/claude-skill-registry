---
document_name: "positioning.skill.md"
location: ".claude/skills/positioning.skill.md"
codebook_id: "CB-SKILL-POSITION-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for product positioning"
skill_metadata:
  category: "marketing"
  complexity: "advanced"
  estimated_time: "varies"
  prerequisites:
    - "Market knowledge"
    - "Competitive landscape"
category: "skills"
status: "active"
tags:
  - "skill"
  - "marketing"
  - "positioning"
ai_parser_instructions: |
  This skill defines procedures for product positioning.
  Used by Product Marketing Manager agent.
---

# Positioning Skill

=== PURPOSE ===

Procedures for creating and maintaining product positioning.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(pmm) @ref(CB-AGENT-PMM-001) | Primary skill for positioning |

=== PROCEDURE: Positioning Statement ===

**Formula:**
```
For [target customer]
Who [statement of need/opportunity]
The [product name]
Is a [product category]
That [key benefit/reason to buy]
Unlike [primary competitive alternative]
Our product [primary differentiation]
```

**Example:**
```
For software development teams
Who struggle with coordination and context switching
Codebook Framework
Is an AI-powered development orchestration system
That reduces coordination overhead by 50%
Unlike traditional project management tools
Our product uses specialized AI agents to automate routine decisions
```

=== PROCEDURE: Target Customer ===

**Customer Profile Template:**
```markdown
## Target Customer Profile

### Demographics
- Company size: [range]
- Industry: [verticals]
- Role/title: [specific roles]
- Geography: [regions]

### Psychographics
- Goals: [what they want to achieve]
- Frustrations: [current pain points]
- Values: [what they prioritize]

### Behavior
- How they buy: [decision process]
- Where they learn: [information sources]
- Current solutions: [what they use now]
```

=== PROCEDURE: Competitive Positioning ===

**Competitive Matrix:**
```markdown
## Competitive Landscape

| Feature | Us | Competitor A | Competitor B |
|---------|-----|--------------|--------------|
| Feature 1 | ✓ | ✓ | ✗ |
| Feature 2 | ✓ | ✗ | ✓ |
| Feature 3 | ✓ | ✗ | ✗ |

### Our Advantages
1. [Unique strength 1]
2. [Unique strength 2]

### Competitor Strengths
- Competitor A: [their strength]
- Competitor B: [their strength]

### Our Response
- To A's strength: [how we compete]
- To B's strength: [how we compete]
```

=== PROCEDURE: Positioning Validation ===

**Checklist:**
- [ ] Target customer is clearly defined
- [ ] Need/opportunity is real and validated
- [ ] Category is recognizable to buyers
- [ ] Benefit is meaningful and measurable
- [ ] Differentiation is sustainable
- [ ] Claims are defensible

=== PROCEDURE: Positioning Document ===

**Location:** `devdocs/marketing/positioning.md`

**Structure:**
```markdown
# Product Positioning

## Positioning Statement
[The complete positioning statement]

## Target Customer
[Customer profile]

## Market Category
[Where we compete]

## Key Benefit
[Primary value delivered]

## Differentiation
[What makes us unique]

## Proof Points
[Evidence supporting claims]

## Competitive Context
[How we compare]

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0 | YYYY-MM-DD | Initial |
```

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(messaging) | Messaging execution |
| @skill(gtm-planning) | Launch planning |
