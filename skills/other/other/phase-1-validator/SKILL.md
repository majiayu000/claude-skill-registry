---
name: phase-1-validator
description: Validates Requirements Phase completion before advancing to Design Phase. Checks business requirements document for completeness, quality gate compliance, and readiness for design work.
---

# Phase 1 (Requirements) Validation Skill

**Purpose**: Automate validation of Requirements Phase completion before advancing to Design Phase.

**When to Use**: When orchestrator or agents need to verify requirements are ready for design work.

## How to Use This Skill

**Executable Script**: `execute.sh`

```bash
# Basic usage with requirements document path
bash .claude/skills/phase-1-validator/execute.sh <requirements-document-path>

# With work type specification
bash .claude/skills/phase-1-validator/execute.sh <path> <work-type>

# With custom quality gate threshold
bash .claude/skills/phase-1-validator/execute.sh <path> Feature 95

# Examples:
bash .claude/skills/phase-1-validator/execute.sh docs/functional-areas/events/new-work/business-requirements.md
bash .claude/skills/phase-1-validator/execute.sh docs/functional-areas/checkin/new-work/business-requirements.md Bug 80
```

**Parameters**:
- `requirements-document-path`: Path to business-requirements.md file
- `work-type`: (optional) Feature|Bug|Hotfix|Docs|Refactor (default: Feature)
- `required-percentage`: (optional) Override quality gate threshold

**Script validates**:
- Document structure (10 points): Executive Summary, Business Context, Success Metrics, User Stories, Business Rules, Security & Privacy, Quality Gate Checklist
- Content quality (10 points): User stories count, acceptance criteria, business rules specificity
- WitchCityRope-specific (5 points): Safety considerations, mobile experience, consent workflows

**Exit codes**:
- 0: Validation passed - ready for Design Phase
- 1: Validation failed - requirements incomplete

## Quality Gate Checklist (95% Required for Features)

### Document Structure (10 points)
- [ ] Executive Summary present (1 point)
- [ ] Business Context section complete (2 points)
- [ ] Success Metrics defined (2 points)
- [ ] User Stories section present (2 points)
- [ ] Business Rules documented (1 point)
- [ ] Security & Privacy section present (1 point)
- [ ] Quality Gate Checklist at bottom (1 point)

### Content Quality (10 points)
- [ ] At least 3 user stories for different roles (2 points)
- [ ] Each story has acceptance criteria (2 points)
- [ ] Business rules are specific and measurable (2 points)
- [ ] Security requirements address data protection (2 points)
- [ ] Success metrics are measurable (1 point)
- [ ] Examples/scenarios provided (1 point)

### WitchCityRope-Specific (5 points)
- [ ] Safety implications considered (1 point)
- [ ] Consent workflows addressed if applicable (1 point)
- [ ] Mobile experience considered (1 point)
- [ ] Impact on user roles documented (1 point)
- [ ] Community standards alignment verified (1 point)


## Usage Examples

### From Orchestrator
```
Use the phase-1-validator skill to check if requirements are ready for design
```

### Manual Validation
```bash
# Find requirements document
REQ_DOC=$(find docs/functional-areas -name "business-requirements.md" -path "*/new-work/*" -type f | tail -1)

# Run validation
bash .claude/skills/phase-1-validator.md "$REQ_DOC"
```

### Integration with Workflow
The orchestrator should automatically invoke this skill:
- Before Phase 1 → Phase 2 transition
- After business-requirements agent completes work
- When user requests to "continue to design"

## Common Issues

### Issue: Missing Success Metrics
**Solution**: Business requirements agent should add specific, measurable metrics like:
- "Reduce event registration time by 50%"
- "Support 100+ concurrent users"
- "95% of users complete registration in 3 minutes"

### Issue: Generic User Stories
**Solution**: User stories should be specific to WitchCityRope context:
- ❌ "As a user, I want to see events"
- ✅ "As a Vetted Member, I want to browse members-only workshops"

### Issue: Missing Safety Considerations
**Solution**: Every feature should address safety implications:
- Data privacy for sensitive community
- Consent requirements for features
- Anonymous reporting options

## Output Format

The skill should output a validation report:

```json
{
  "phase": "requirements",
  "status": "pass|fail",
  "score": 23,
  "maxScore": 25,
  "percentage": 92,
  "requiredPercentage": 95,
  "missingItems": [
    "Mobile experience not mentioned",
    "Only 2 user stories (need 3+)"
  ],
  "recommendations": [
    "Add user story for mobile registration flow",
    "Add user story for admin monitoring"
  ],
  "readyForNextPhase": true
}
```

## Integration with Quality Gates

This skill enforces the quality gate thresholds by work type:

- **Feature**: 95% required (24/25 points)
- **Bug Fix**: 80% required (20/25 points)
- **Hotfix**: 70% required (18/25 points)
- **Documentation**: 85% required (21/25 points)
- **Refactoring**: 90% required (23/25 points)

## Progressive Disclosure

**Initial Context**: Show quick checklist
**On Request**: Show full validation script
**On Failure**: Show specific missing items and recommendations
**On Pass**: Show concise summary only

---

**Remember**: This skill automates validation, it doesn't replace the business-requirements agent's judgment. If validation fails, the orchestrator should loop back to business-requirements agent for completion.
