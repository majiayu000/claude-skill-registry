---
name: spec-writer
description: >
  Transform conversations and ideas into structured technical specifications.
  Outputs: User stories, acceptance criteria, technical requirements, edge cases.
  Use when user wants to document requirements before coding.
  Triggers: write spec, create user stories, document requirements, /spec
---

# Spec Writer

Transform vague ideas into precise, implementable specifications that Claude Code can execute without ambiguity.

## Purpose

Most AI coding failures happen because specifications are unclear. This skill extracts implicit requirements from conversations and outputs structured specs that eliminate guesswork.

## Process

### Phase 1: Context Extraction

#### Entry Check

```
IF user provided: problem statement + target users + success criteria
    → Proceed to Phase 2
ELSE
    → Gather missing information below (one question at a time)
```

#### Information Needed

| Item        | Question                              | Why Required                |
| ----------- | ------------------------------------- | --------------------------- |
| Problem     | "What problem are you solving?"       | Defines scope boundaries    |
| Users       | "Who will use this?"                  | Shapes UX requirements      |
| Success     | "How will you know it works?"         | Creates acceptance criteria |
| Constraints | "Any technical/business constraints?" | Prevents wasted effort      |

#### Transition Criteria

All four items gathered + user confirmed → Phase 2

---

### Phase 2: Requirement Analysis

#### Entry Check

```
IF Phase 1 complete:
    → Analyze and categorize requirements
ELSE
    → Return to Phase 1
```

#### Categorization Framework

```
FOR each requirement mentioned:
    Classify as:
    - MUST: Core functionality, non-negotiable
    - SHOULD: Important but has workarounds
    - COULD: Nice to have, time permitting
    - WON'T: Explicitly out of scope (important to document)
```

#### Output: Requirements Table

| ID  | Requirement   | Priority          | Rationale           |
| --- | ------------- | ----------------- | ------------------- |
| R1  | [requirement] | MUST/SHOULD/COULD | [why this priority] |

#### Edge Case Discovery

```
FOR each MUST requirement:
    Ask: "What happens when [edge case]?"

    Common edge cases to probe:
    - Empty/null inputs
    - Maximum scale (1000x normal)
    - Concurrent access
    - Network failure
    - Permission denied
    - Invalid data format
```

---

### Phase 3: User Story Generation

#### Entry Check

```
IF requirements table complete + edge cases documented:
    → Generate user stories
ELSE
    → Return to Phase 2
```

#### Story Format

```
AS A [user type]
I WANT TO [action]
SO THAT [benefit]

ACCEPTANCE CRITERIA:
- GIVEN [context]
  WHEN [action]
  THEN [expected result]

EDGE CASES:
- [edge case]: [expected behavior]

TECHNICAL NOTES:
- [implementation hints, if relevant]
```

#### Story Generation Rules

```
FOR each MUST requirement:
    → Generate 1 user story
    → Include 2-4 acceptance criteria
    → Include 1-3 edge cases

FOR each SHOULD requirement:
    → Generate 1 user story (simpler format)
    → Include 1-2 acceptance criteria
```

---

### Phase 4: Technical Specification

#### Entry Check

```
IF user stories generated:
    → Ask: "Ready for technical spec, or need to adjust stories first?"

IF user confirms:
    → Generate technical specification
ELSE
    → Revise stories based on feedback
```

#### Technical Spec Structure

```markdown
## Technical Specification: [Feature Name]

### Overview

[1-2 sentences describing the feature]

### Data Models

[If new data structures needed]

### API Endpoints

[If applicable]
| Method | Path | Request | Response |
|--------|------|---------|----------|

### State Changes

[What changes when this feature runs]

### Dependencies

[External services, libraries, existing code]

### Security Considerations

[Auth, validation, rate limits]

### Testing Strategy

- Unit: [what to unit test]
- Integration: [what to integration test]
- E2E: [critical user flows]
```

---

### Phase 5: Output Delivery

#### Output Format Selection

```
IF user's project has existing spec format:
    → Match that format
ELSE IF user specified format preference:
    → Use requested format
ELSE
    → Use default markdown format below
```

#### Default Output Structure

```markdown
# [Feature Name] Specification

## Summary

[One paragraph overview]

## Requirements

[Requirements table from Phase 2]

## User Stories

[Stories from Phase 3]

## Technical Specification

[Spec from Phase 4]

## Out of Scope

[Explicitly excluded items - prevents scope creep]

## Open Questions

[Unresolved items needing decisions]
```

---

## Self-Check (Read before every response)

□ Am I gathering context or assuming?
→ Missing info = ask, never fill in

□ Am I asking one question at a time?
→ Multiple questions overwhelm users

□ Are requirements testable?
→ Vague requirements = implementation arguments later

□ Did I include edge cases?
→ Happy path only = bugs in production

□ Is the spec implementable by Claude Code?
→ Read it as if you'll code it: any ambiguity?

□ Did I document what's OUT of scope?
→ Scope creep starts with undefined boundaries

□ Are acceptance criteria specific?
→ "Works correctly" is not acceptance criteria
→ "Returns 200 with user object containing id, email" is

---

## Integration with Other Skills

```
AFTER spec complete:
    Suggest: "Spec ready. Next steps:"
    - "Use /prd to expand into full PRD"
    - "Use architect-planner to design structure"
    - "Start coding with this spec as context"
```
