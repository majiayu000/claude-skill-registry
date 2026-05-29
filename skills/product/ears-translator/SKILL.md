---
name: ears-translator
description: Translate user stories and informal requirements into EARS (Easy Approach to Requirements Syntax) format. Use when Claude needs to (1) convert user stories to formal requirements, (2) transform informal requirements into structured EARS format, (3) review and improve existing requirements using EARS patterns, (4) create testable, unambiguous system requirements. Triggers on requests like "convert to EARS", "write requirements", "formalize these user stories", "EARS format".
---

# EARS Requirements Translator

Translate user stories and informal requirements into precise, testable EARS format requirements.

## Workflow

### Step 1: Gather Requirements
Read all stories and requirements provided by user. Identify:
- The system/component being specified
- Functional behaviors described
- Conditions, triggers, and states mentioned
- Error scenarios and edge cases

### Step 2: Ask Clarification Questions
Use AskUserQuestion to clarify ambiguities. Common questions:
- What is the exact system/component name?
- What are the specific thresholds or timing requirements?
- Are there error conditions to handle?
- Is this an optional feature or always present?

Continue until at least 90% confident about requirements.

### Step 3: Select Output Format
Ask user preference:
- **Individual REQs**: Each requirement listed separately with IDs (REQ-001, REQ-002...)
- **Grouped by feature**: Requirements organized under feature headings

### Step 4: Transform to EARS
Apply the appropriate EARS pattern for each requirement. See `references/ears-patterns.md` for pattern details.

**Requirement Splitting:**
Always attempt to split compound requirements into individual atomic requirements:
- If a requirement mentions multiple tools (e.g., "RSpec and Rubocop"), create separate requirements for each
- If a requirement mentions multiple services or components, create separate requirements for each
- If a requirement mentions multiple actions, create separate requirements for each
- Use sub-numbering (1a, 1b, 1c) to indicate requirements derived from the same source

**Pattern Selection:**
- Always active property → Ubiquitous (no keyword)
- Continuous state dependency → State-Driven (While)
- Discrete event trigger → Event-Driven (When)
- Error/fault handling → Unwanted Behavior (If...Then)
- Optional feature → Optional Feature (Where)
- Multiple conditions → Complex (combine)

**Testing & Linting Requirements:**
Requirements about testing (RSpec, Jest, pytest, etc.) and linting (Rubocop, ESLint, etc.) should use the **Ubiquitous** pattern because they describe always-active quality properties of the system:
- "Tests shall pass" = always-active property
- "Linter shall report no errors" = always-active property

Example transformations:
- Input: "When claude runs rspec it passes"
- Output: "The admin/ test suite **shall** pass all RSpec tests without errors."

- Input: "When rubocop runs it has no errors"
- Output: "The admin/ codebase **shall** pass Rubocop linting without errors."

### Step 5: Validate with Checklist
For each requirement, verify:

**Structure:**
- [ ] Correct EARS pattern
- [ ] Explicit system name
- [ ] One "shall" per requirement
- [ ] Temporal ordering (precondition → trigger → system → response)

**Content:**
- [ ] Verifiable/testable
- [ ] Measurable criteria (no vague terms)
- [ ] Units for numerical values
- [ ] No escape clauses

**Language:**
- [ ] Active voice
- [ ] Consistent terminology

### Step 6: Present Results
Show the EARS requirements to user with:
- Requirement IDs
- Pattern type used
- Original source reference (which user story/requirement it came from)

### Step7: Writing Results
Write the EARS requirements with concise format

## Quick Pattern Reference

| Pattern | Keyword | Template |
|---------|---------|----------|
| Ubiquitous | (none) | The <system> shall <response> |
| State-Driven | While | While <condition>, the <system> shall <response> |
| Event-Driven | When | When <trigger>, the <system> shall <response> |
| Unwanted Behavior | If...Then | If <error>, then the <system> shall <response> |
| Optional Feature | Where | Where <feature>, the <system> shall <response> |

## Example Transformations

### Example 1: Splitting Compound Requirements

**Input:**
> When CI sees changes in admin/ it runs rspec and rubocop

**Output (Split + Pattern Selection):**
```
REQ-001a [Event-Driven]
When CI detects changes in admin/, the CI pipeline shall execute RSpec for admin/.

REQ-001b [Event-Driven]
When CI detects changes in admin/, the CI pipeline shall execute Rubocop for admin/.
```

**Output (Concise version):**
```
When CI detects changes in admin/, the CI pipeline shall execute RSpec for admin/.
When CI detects changes in admin/, the CI pipeline shall execute Rubocop for admin/.
```

### Example 2: Testing/Linting as Ubiquitous

**Input:**
> When claude runs rspec in admin/ it passes without errors
> When claude runs rubocop in admin/ it passes without errors

**Output (Ubiquitous Pattern):**
```
REQ-001 [Ubiquitous]
The admin/ test suite shall pass all RSpec tests without errors.

REQ-002 [Ubiquitous]
The admin/ codebase shall pass Rubocop linting without errors.
```

**Output (Concise version):**
```
The admin/ test suite shall pass all RSpec tests without errors.
The admin/ codebase shall pass Rubocop linting without errors.
```

### Example 3: User Story Transformation

**Input (User Story):**
> As a user, I want to receive a notification when my file upload completes, so I know it's done.

**Output (EARS):**
```
REQ-001 [Event-Driven]
When a file upload completes successfully, the application shall display a success notification within 2 seconds.

REQ-002 [Unwanted Behavior]
If a file upload fails, then the application shall display an error message indicating the failure reason.
```

**Output (Concise version):**
```
When a file upload completes successfully, the application shall display a success notification within 2 seconds.
If a file upload fails, then the application shall display an error message indicating the failure reason.
```

## Resources

- `references/ears-patterns.md` - Complete EARS pattern reference with examples and quality checklist
