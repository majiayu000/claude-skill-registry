---
name: speckit-specify
description: Create or update feature specification from natural language feature description
---

# Speckit-Specify: Feature Specification Creation

## Purpose

Create a formal, technology-agnostic specification that describes **WHAT** users need and **WHY** it matters, without prescribing **HOW** to implement it.

## Prerequisites

- Completed brainstorming session (use `brainstorming` skill first)
- Clear understanding of user requirements and constraints

## What This Skill Does

1. Generates feature branch and directory structure
2. Creates comprehensive `spec.md` following template
3. Validates specification quality
4. Resolves remaining clarifications (max 3)
5. Ensures specification is ready for technical planning

## Key Principles

### Focus on WHAT and WHY
- Describe user capabilities and business value
- Avoid implementation details (no languages, frameworks, APIs)
- Written for business stakeholders, not developers

### Technology-Agnostic Success Criteria
- Measurable outcomes from user/business perspective
- No mention of frameworks, databases, or tools
- Examples: "Users can complete checkout in <3 minutes", "System supports 10,000 concurrent users"

### Quality Over Speed
- Make informed guesses for reasonable defaults
- Only mark [NEEDS CLARIFICATION] for critical decisions (max 3)
- Validate against quality checklist before completion

## Template Location

**IMPORTANT:** The specification template is located at:
`.github/skills/speckit-specify/spec-template.md`

This template MUST be loaded and used as the base structure for all specification creation.

## Execution Flow

All execution logic is now contained within this skill. The skill handles:
- Feature branch creation and numbering
- Spec template loading and filling
- Quality validation
- Clarification handling

### Quick Summary

1. **Parse user description** from arguments
2. **Generate branch name** (2-4 words, action-noun format)
3. **Check existing branches** (remote, local, specs directories)
4. **Run create-new-feature.sh** with next available number
5. **Load spec template** from `.github/skills/speckit-specify/spec-template.md`
6. **Fill specification** with concrete details from brainstorming
7. **Validate quality** against checklist criteria
8. **Resolve clarifications** (max 3, with suggested answers)
9. **Report completion** with branch, spec path, and readiness

## Specification Quality Validation

After writing the spec, validate against these criteria:

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Success criteria are technology-agnostic (no implementation details)
- [ ] All acceptance scenarios are defined
- [ ] Edge cases are identified
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

### Feature Readiness
- [ ] All functional requirements have clear acceptance criteria
- [ ] User scenarios cover primary flows
- [ ] Feature meets measurable outcomes defined in Success Criteria
- [ ] No implementation details leak into specification

## Clarification Handling

If [NEEDS CLARIFICATION] markers exist (max 3):

1. **Extract markers** from spec
2. **Limit to 3** most critical (scope → security → UX → technical details)
3. **Present as Q&A format:**
   - **Recommended:** Option X - <reasoning>
   - Table with options A-E
   - User can say "yes"/"recommended" to accept suggestion
4. **Update spec** with user's answers
5. **Re-validate** quality after clarifications resolved

## Success Indicators

Specification is ready when:
- ✅ Zero implementation details present
- ✅ All success criteria are measurable and technology-agnostic
- ✅ No [NEEDS CLARIFICATION] markers remain
- ✅ All quality checklist items pass
- ✅ Requirements are testable and unambiguous
- ✅ Written for business stakeholders (no technical jargon)

## Output

```
specs/N-feature-name/
├── spec.md                    # Feature specification (WHAT & WHY)
└── checklists/
    └── requirements.md        # Quality validation checklist
```

## Next Step

After specification is complete:
- **Option A:** Use `speckit-plan` to create technical plan
- **Option B:** Use `speckit-checklist` to generate domain-specific quality checks first

## Common Mistakes

### ❌ Implementation Details in Spec
**Wrong:** "Use React hooks for state management"
**Right:** "Users can update their profile information"

### ❌ Technology-Specific Success Criteria
**Wrong:** "API response time is under 200ms"
**Right:** "Users see search results instantly"

### ❌ Too Many Clarifications
**Wrong:** 10 [NEEDS CLARIFICATION] markers
**Right:** Max 3, make informed guesses for the rest

### ❌ Vague Requirements
**Wrong:** "System should be fast and secure"
**Right:** "Users can log in within 2 seconds, all data encrypted at rest and in transit"

## Related Skills

- **brainstorming** - REQUIRED before this skill (explore requirements)
- **speckit-plan** - Next step after specification (design technical approach)
- **speckit-checklist** - Generate quality validation checklists
