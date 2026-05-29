---
document_name: "messaging.skill.md"
location: ".claude/skills/messaging.skill.md"
codebook_id: "CB-SKILL-MESSAGE-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for messaging frameworks"
skill_metadata:
  category: "marketing"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Positioning document"
    - "Target audience knowledge"
category: "skills"
status: "active"
tags:
  - "skill"
  - "marketing"
  - "messaging"
ai_parser_instructions: |
  This skill defines procedures for messaging frameworks.
  Used by Product Marketing Manager agent.
---

# Messaging Skill

=== PURPOSE ===

Procedures for creating messaging frameworks and key messages.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(pmm) @ref(CB-AGENT-PMM-001) | Primary skill for messaging |

=== PROCEDURE: Messaging Hierarchy ===

**Structure:**
```
Brand Promise
    └── Value Proposition
        └── Key Messages (3-5)
            └── Supporting Points
                └── Proof Points
```

**Definitions:**
- **Brand Promise:** The overarching commitment (emotional)
- **Value Proposition:** What you offer (rational)
- **Key Messages:** Main themes/pillars
- **Supporting Points:** Evidence for each pillar
- **Proof Points:** Specific data, testimonials, examples

=== PROCEDURE: Value Proposition ===

**Template:**
```markdown
## Value Proposition

### Headline
[One sentence that captures the core benefit]

### Subheadline
[2-3 sentences expanding on the headline]

### Key Benefits
1. [Benefit 1] - [Brief explanation]
2. [Benefit 2] - [Brief explanation]
3. [Benefit 3] - [Brief explanation]

### Proof
[Evidence that supports the claim]
```

**Example:**
```markdown
### Headline
Ship faster without the coordination tax.

### Subheadline
Codebook uses AI agents to handle routine decisions,
reducing context switching and keeping your team focused
on what matters: building great software.

### Key Benefits
1. 50% less coordination overhead
2. Consistent code quality without constant review
3. Documentation that stays current automatically
```

=== PROCEDURE: Key Messages ===

**Message Pillar Template:**
```markdown
## Key Message: [Pillar Name]

### The Message
[One sentence statement]

### Why It Matters
[Why this resonates with target audience]

### Supporting Points
1. [Evidence/example 1]
2. [Evidence/example 2]
3. [Evidence/example 3]

### Proof Points
- [Statistic]
- [Customer quote]
- [Third-party validation]

### Usage
- Website: [where to use]
- Sales: [when to emphasize]
- Content: [topic areas]
```

=== PROCEDURE: Messaging Matrix ===

**By Audience:**
```markdown
| Audience | Pain Point | Key Message | Proof |
|----------|------------|-------------|-------|
| Developer | Context switching | Focus on code, not process | 50% fewer interruptions |
| Manager | Team velocity | Ship 2x faster | Case study: Acme Corp |
| Executive | Cost/efficiency | Reduce coordination cost | ROI calculator |
```

**By Funnel Stage:**
```markdown
| Stage | Objective | Message Focus |
|-------|-----------|---------------|
| Awareness | Get attention | Problem agitation |
| Consideration | Build interest | Solution overview |
| Decision | Drive action | Differentiation, proof |
| Retention | Build loyalty | Advanced value, community |
```

=== PROCEDURE: Messaging Document ===

**Location:** `devdocs/marketing/messaging.md`

**Structure:**
```markdown
# Messaging Framework

## Brand Promise
[Overarching commitment]

## Value Proposition
[Core value statement]

## Key Messages

### Pillar 1: [Name]
[Full pillar details]

### Pillar 2: [Name]
[Full pillar details]

### Pillar 3: [Name]
[Full pillar details]

## Messaging by Audience
[Audience matrix]

## Messaging by Stage
[Funnel matrix]

## Boilerplate
### Short (25 words)
[Brief description]

### Medium (50 words)
[Standard description]

### Long (100 words)
[Full description]

## Version History
```

=== PROCEDURE: Message Testing ===

**Validation Questions:**
- Is it clear? (Can someone understand in 5 seconds?)
- Is it credible? (Do we have proof?)
- Is it compelling? (Does it motivate action?)
- Is it differentiated? (Could a competitor say this?)
- Is it memorable? (Can someone repeat it?)

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(positioning) | Foundation for messaging |
| @skill(voice-tone) | Execution guidance |
