---
name: user-intent-parser
description: Parse user requirements into structured format with explicit
  assumptions, constraints, and acceptance criteria. Use when initial
  requirements are ambiguous or informal.
---

# User Intent Parser Skill

## Purpose
Convert informal user requests into structured requirement format.

## When to Use
- User provides vague or informal request
- Requirements are conversational rather than structured
- Non-technical user is specifying features
- Need to formalize verbal requirements

## Parsing Process

### Step 1: Extract Explicit Statements
Identify what user directly stated:
- **Actions (verbs)**: create, update, delete, show, send, etc.
- **Objects (nouns)**: user, product, order, notification, etc.
- **Conditions (when/if)**: triggers, prerequisites
- **Outcomes (so that)**: expected results

### Step 2: Identify Implicit Requirements
What's assumed but not stated:
- Authentication required?
- Error handling expectations
- Performance expectations
- Platform/device support
- Data validation needs

### Step 3: Flag Ambiguities
Mark unclear items:
- Vague terms ("fast", "good", "easy", "simple")
- Missing specifics (quantities, limits)
- Unclear scope (boundaries)
- Undefined actors (who does what)

### Step 4: Generate Structured Format
Use [templates/parsed-intent.md](templates/parsed-intent.md)

## Output Format

### Parsed Intent Document

Save to: `docs/specs/parsed-intent-{session}.md`

The template captures:
- Original user statement
- Extracted functional requirements
- Extracted non-functional requirements
- Assumptions made (with rationale)
- Ambiguities requiring clarification
- Draft acceptance criteria

## Confidence Levels

Assign confidence to each extracted requirement:

| Level | Meaning | Action |
|-------|---------|--------|
| High | Directly stated by user | Proceed |
| Medium | Strongly implied | Confirm |
| Low | Inferred/assumed | Must clarify |

## Common Patterns

### Feature Requests
```
User: "I need users to be able to export their data"

Parsed:
- Action: export
- Object: user data
- Actor: users (authenticated)
- Implicit: format unspecified, permissions assumed
- Ambiguity: which data? what format?
```

### Bug Reports as Features
```
User: "The search is too slow"

Parsed:
- Action: improve search performance
- Implicit: current performance is unacceptable
- Ambiguity: how slow? target speed?
```

### Vague Requests
```
User: "Make the dashboard better"

Parsed:
- Action: improve dashboard
- Ambiguity: which aspects? visual? functional? performance?
- Confidence: Low (requires extensive clarification)
```

## Integration Points

1. Research findings inform implicit requirements
2. Generated ambiguities feed into question generation
3. Structured output becomes input for requirements validation

## Storage Location
Save to: `docs/specs/parsed-intent-{session}.md`

## Quality Checklist

Before completing parsing:
- [ ] All explicit actions identified
- [ ] All objects/entities named
- [ ] Implicit requirements documented
- [ ] Ambiguities clearly flagged
- [ ] Confidence levels assigned
- [ ] Draft acceptance criteria created
