---
name: plan-feature
description: Create a detailed implementation plan for a new feature, exploring codebase and loading relevant architecture patterns
user-invocable: true
---

# Feature Planning

Create a plan in `specs/<current-timestamp>-<feature-name>.md` for the `Feature` below.

## Instructions

1. **Declare scope first** - Determine if this is API-only, Web-only, Full-stack, or Shared
2. **Load only relevant context** based on scope:
   - API: `<root>/.claude/context/api/00-overview.md` + specific patterns needed
   - Web: `<root>/apps/web/CLAUDE.md` + specific patterns needed
   - Full-stack: Both overviews + specific patterns as needed
3. **Explore targeted directories** - Don't explore everything:
   - API: `<root>/apps/api/src/[relevant-module]/`
   - Web: `<root>/apps/web/src/features/[relevant-feature]/`
   - Shared: `<root>/packages/shared/src/`
4. **Testing principles** - Each test should verify a distinct behavior:
   - Ask: "If test A passes, would test B always pass?" → If yes, test B is redundant
   - Ask: "What unique failure mode does this test catch?"
   - Avoid redundant tests (e.g., "response validation" covered by happy path)
5. Follow existing patterns. Report new library needs in Notes.

## Plan Format

````md
# Feature: <name>

## Feature Overview
<describe the feature in detail, including its purpose and value to users>
<How does the solution work? 2-3 sentences.>

## User Story
As a <user type>, I want to <goal> so that <benefit>.

## Scope
- [ ] API-only
- [ ] Web-only
- [ ] Full-stack
- [ ] Shared package

## Solution Statement
<describe the proposed solution approach and how it solves the problem>

## Relevant Files
Use these files to implement the feature:

<find and list the files that are relevant to the feature, describe why they are relevant in bullet points>

## Files to Deliver

### Test Files
<!-- List ALL test files that must be created. These are implemented FIRST. -->
| File Path | Tests | Verifies |
|-----------|-------|----------|
| `path/to/file.spec.ts` | test case 1, test case 2 | `path/to/production-file.ts` |

### Production Files
<!-- List ALL production files to create or modify. Implemented AFTER tests. -->
| File Path | Purpose |
|-----------|---------|
| `path/to/new-file.ts` | Description of what this file does |
| `path/to/existing-file.ts` | What modifications are needed |

## Step by Step Tasks
<list step by step tasks as h3 headers plus bullet points. Order matters, start with foundational shared changes.

IMPORTANT: For each step that creates new functionality:
1. First list the test file(s) to create with their test cases
2. Then list the production code to implement
3. End with running tests to verify

Your last step should be running the `Validation Commands`.>

## Acceptance Criteria
<list specific, measurable criteria that must be met for the feature to be considered complete>

## Testing Strategy

### Unit Tests
<describe unit tests needed - each should test a distinct behavior>

### Integration Tests
<describe integration tests needed - typically: happy path, error cases, edge cases>

### Edge Cases
<list edge cases that need to be tested - only if they catch distinct failure modes>

## Validation Commands
<Specific commands to validate with 100% confidence the feature is implemented with zero regressions. Start with the most specific commands and end with broader ones.>

## Notes
<Optional: list any additional notes, future considerations, or context>
````

## Feature
$ARGUMENTS
