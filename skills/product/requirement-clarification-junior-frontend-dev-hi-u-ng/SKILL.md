---
name: requirement-clarification
description: Generate clarifying questions from research findings. MUST be used
  before planning phase. Validates requirements are complete and unambiguous
  before technical work begins.
---

# Requirement Clarification Skill

## Purpose
Transform ambiguous user requests into clear, implementable requirements.

## When to Use
- After research phase completes
- Before planning phase begins
- When user requirements are unclear
- For non-technical user requests

## Question Templates

### For Scope Clarification
See [question-templates/scope-questions.md](question-templates/scope-questions.md)

Common patterns:
- "Should [feature] also handle [edge case]?"
- "When [condition], what should happen?"
- "Is [assumption] correct, or do you need [alternative]?"

### For Technical Decisions
See [question-templates/technical-questions.md](question-templates/technical-questions.md)

Common patterns:
- "Do you have a preference between [A] and [B] for [purpose]?"
- "Should this integrate with [existing system]?"
- "What level of [performance/security] is required?"

### For Constraints
See [question-templates/constraint-questions.md](question-templates/constraint-questions.md)

Common patterns:
- "Is there a deadline for this?"
- "Are there any [technology/approach] restrictions?"
- "Who will be using this feature?"

## Question Quality Checklist

Each question must be:
- [ ] Specific (not vague)
- [ ] Answerable (user has the information)
- [ ] Impactful (answer affects implementation)
- [ ] Non-technical (accessible language)
- [ ] Defaultable (has fallback assumption)

## Question Priority Levels

### Must Answer (Blocking)
- Questions that block planning if unanswered
- Maximum 10 blocking questions
- Always provide defaults

### Should Answer (Important)
- Questions that improve implementation quality
- Can proceed with defaults if not answered

### Could Answer (Nice to Have)
- Questions for optimization
- Low impact on core implementation

## Validation Script

Run `scripts/validate-requirements.py` to check:
- All blocking questions answered
- No contradictory requirements
- Technical feasibility confirmed
- Confidence levels assigned

```bash
python scripts/validate-requirements.py <session-id>
```

## Output Location
- Questions: `docs/specs/questions-{session}.md`
- Requirements: `docs/specs/requirements-{session}.md`

## Integration with Workflow

1. Research phase produces findings in `docs/research/`
2. This skill generates questions from those findings
3. User answers questions
4. Validated requirements document is produced
5. Planning phase can begin
