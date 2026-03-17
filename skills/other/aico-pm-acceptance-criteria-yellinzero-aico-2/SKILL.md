---
name: aico-pm-acceptance-criteria
description: |
  Define clear, testable acceptance criteria using Given/When/Then (Gherkin) format that can be directly used for testing.

  Use this skill when:
  - User asks for "acceptance criteria", "AC", "test criteria", "done criteria"
  - User asks "how do we know it's done?", "what counts as complete?"
  - User story needs testable success conditions
  - QA needs test scenarios or test cases
  - Running /pm.plan and need to add AC to stories
  - Reviewing story and AC is missing or vague

  Format: Always use Given [context], When [action], Then [expected result] structure.
---

# Acceptance Criteria

## ⚠️ CRITICAL RULES - READ FIRST

1. **READ STORY FIRST**: Always read the story file from `docs/reference/pm/stories/` before writing criteria
2. **USE GIVEN/WHEN/THEN**: All criteria must follow this format
3. **UPDATE STORY FILE**: Add criteria to existing story file, don't create new files

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Review story/feature**: Understand what needs to be done
2. **Identify success scenarios**: Happy paths first
3. **Write Given/When/Then**: For each scenario
4. **Add edge cases**: Boundary conditions and errors
5. **Verify testability**: Each criterion must be independently verifiable

## Acceptance Criteria Template

```markdown
### Acceptance Criteria for [Story/Feature]

#### Scenario 1: [Scenario Name]

- **Given** [precondition/context]
- **When** [action/trigger]
- **Then** [expected outcome]

#### Scenario 2: [Scenario Name]

- **Given** [precondition/context]
- **When** [action/trigger]
- **Then** [expected outcome]

#### Edge Cases

- **Given** [edge case condition]
- **When** [action]
- **Then** [expected behavior]
```

## Criteria Categories

| Category       | Examples                    |
| -------------- | --------------------------- |
| Functional     | Feature works as specified  |
| Validation     | Input validation rules      |
| Error handling | Error messages and recovery |
| Performance    | Response time expectations  |
| Accessibility  | A11y requirements           |

## Quality Checklist

- [ ] Each criterion is independently testable
- [ ] No ambiguous language ("should", "might", "could")
- [ ] Edge cases are covered
- [ ] Error states are defined
- [ ] Performance expectations stated (if relevant)

## Key Rules

- ALWAYS use Given/When/Then structure
- MUST make each criterion independently testable
- ALWAYS include edge cases and error scenarios
- NEVER use vague language - be specific

## Common Mistakes

- ❌ Vague criteria ("works correctly") → ✅ Specific conditions
- ❌ Missing edge cases → ✅ Include boundary conditions
- ❌ Implementation details → ✅ Focus on observable behavior
