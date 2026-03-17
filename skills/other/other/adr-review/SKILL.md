---
name: adr-review
description: Reviews implemented ADRs by comparing them against actual implementation and updating feedback sections. Use this when the user wants to review an ADR implementation, validate architectural decisions, or update ADR feedback logs.
---

# ADR Review Skill

This skill performs post-implementation reviews of Architecture Decision Records (ADRs) by comparing the documented decision against the actual implementation.

## Purpose

After implementing an ADR, this skill:

1. Analyzes the ADR's expectations and success criteria
2. Reviews the actual implementation in the codebase
3. Compares expected vs actual outcomes
4. Documents findings in the ADR's Feedback Log section
5. Identifies gaps, successes, and lessons learned

## Instructions

When reviewing an ADR implementation, follow these steps:

### 1. Identify the ADR to Review

If the user specifies an ADR number (e.g., "Review ADR-0002"):

- Locate the ADR file in `docs/decisions/XXXX-*.md`

If no specific ADR is mentioned:

- Ask which ADR to review
- List available ADRs in `docs/decisions/`

### 2. Read and Analyze the ADR

Extract key information:

- **Decision Outcome**: What was decided?
- **Confirmation criteria**: How should success be validated?
- **Test Expectations**: What tests were expected?
- **Dependencies**: What components were expected to be created?
- **Timeline**: When was implementation expected?
- **Risk Assessment**: What risks were identified?
- **AI-Specific Extensions**: Any AI tool guidance

### 3. Review the Implementation

Systematically check:

#### Code Review

- Locate implementation files mentioned in the ADR
- Verify core functionality exists
- Check code quality and patterns
- Look for implementation notes or comments

#### Testing Review

- Find and run tests related to the ADR
- Verify test coverage meets expectations
- Check if all test scenarios from ADR are covered
- Document test results (passing/failing)

#### Dependencies Review

- Check if all dependencies were installed
- Verify versions match requirements
- Look for dependency conflicts

#### Documentation Review

- Check if examples/docs were created
- Verify README updates
- Look for inline documentation

### 4. Compare Against ADR Criteria

For each section in the ADR:

#### Confirmation Criteria

- Go through each criterion
- Mark as ✅ Met, ⚠️ Partially Met, or ❌ Not Met
- Provide evidence for each assessment

#### Test Expectations

- Check if expected tests exist
- Verify they pass
- Note any missing tests

#### Risk Assessment

- Review each identified risk
- Document whether mitigation strategies were implemented
- Note any risks that materialized

### 5. Update the ADR Feedback Log

Modify the "Feedback Log" section at the end of the ADR with:

```markdown
### Feedback Log

- Implementation date: {actual date}
- Actual outcomes:
  - {outcome 1 with evidence}
  - {outcome 2 with evidence}
  - {outcome 3 with evidence}
- Challenges encountered:
  - {challenge 1 and how it was resolved}
  - {challenge 2 and how it was resolved}
- Lessons learned:
  - {lesson 1}
  - {lesson 2}
- Suggested improvements:
  - {improvement 1 for future similar decisions}
  - {improvement 2 for future similar decisions}
- Confirmation Status:
  - ✅ {met criterion}
  - ⚠️ {partially met criterion - explanation}
  - ❌ {unmet criterion - reason}
```

### 6. Generate Summary Report

After updating the ADR, provide the user with:

- Overall implementation status (Success/Partial/Needs Work)
- Key achievements
- Areas needing attention
- Recommendations for next steps

## Review Checklist

Use this checklist when performing reviews:

- [ ] ADR file located and read
- [ ] Implementation files identified
- [ ] Tests located and executed
- [ ] Test results documented (X/Y passing)
- [ ] Dependencies verified
- [ ] Examples/documentation checked
- [ ] Each confirmation criterion evaluated
- [ ] Each risk assessment reviewed
- [ ] Feedback Log section updated
- [ ] Lessons learned documented
- [ ] Summary report provided to user

## Example Usage

**User request**: "Review ADR-0002"

**Your response should**:

1. Read `docs/decisions/0002-use-litellm-for-llm-provider-abstraction.md`
2. Extract confirmation criteria and expectations
3. Search for implementation files (`src/cllm/client.py`, etc.)
4. Run tests (`pytest tests/`)
5. Check examples exist
6. Compare actual vs expected outcomes
7. Update the Feedback Log section in the ADR
8. Report findings to user

## Output Format

Provide the user with a structured report:

```
# ADR-XXXX Review Report

## Summary
[Brief overview: Fully Implemented / Partially Implemented / Not Implemented]

## Confirmation Criteria Status
✅ Criterion 1 - [evidence]
⚠️ Criterion 2 - [partially met because...]
❌ Criterion 3 - [not met because...]

## Test Results
- Tests found: X
- Tests passing: Y/X
- Coverage: [assessment]

## Key Achievements
- Achievement 1
- Achievement 2

## Challenges Identified
- Challenge 1
- Challenge 2

## Recommendations
- Recommendation 1
- Recommendation 2

## ADR Updated
✅ Feedback Log section has been updated with findings.
```

## Best Practices

1. **Be Objective**: Base assessments on evidence, not assumptions
2. **Run Tests**: Actually execute tests, don't just check if they exist
3. **Check Recent Changes**: Use git log to see recent implementation activity
4. **Look for Side Effects**: Note unexpected benefits or issues
5. **Document Evidence**: Provide file paths, line numbers, test output
6. **Be Constructive**: Frame gaps as opportunities for improvement
7. **Update Accurately**: Only mark criteria as met if truly satisfied

## Notes

- Reviews should happen after implementation is considered "complete"
- Multiple reviews over time can track evolution
- Previous feedback logs should be preserved (append, don't replace)
- Reviews can identify need for follow-up ADRs
- Use git history to understand implementation timeline
