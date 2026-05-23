---
name: requirement-validator
description: Analyze task descriptions and requirements for completeness, clarity, and implementability. Use when evaluating if a task has sufficient detail to begin implementation or if clarification is needed.
---

# Requirement Validator

## Instructions

### When to Invoke This Skill
- Before starting implementation on an issue or task
- User asks if requirements are clear enough
- After reading issue/task description
- When planning implementation
- Before creating branches for new work

### Core Validation Criteria

1. **Clarity** - Is the goal clearly stated?
2. **Completeness** - Are all necessary details provided?
3. **Specificity** - Are requirements specific or vague?
4. **Testability** - Can success be measured/verified?
5. **Feasibility** - Is implementation possible with current system?

### Standard Workflow

#### 1. Extract Requirements

From issue/task description, identify:
- **Goal**: What needs to be accomplished?
- **Scope**: What's included and excluded?
- **Constraints**: Technical limitations or requirements
- **Success criteria**: How to know it's complete?
- **Context**: Why is this needed?

#### 2. Assess Clarity

Check if the requirement answers:
- **What** needs to be done?
- **Why** it needs to be done?
- **How** it should be done (if specified)?
- **Who** is the user/audience?

**Red Flags:**
- Vague language: "improve", "enhance", "optimize" without metrics
- Missing details: "add feature" without describing functionality
- Ambiguous terms: "fast", "easy", "better" without definition
- Multiple interpretations possible

#### 3. Evaluate Completeness

**Essential Elements:**
- Problem statement or user need
- Desired outcome or behavior
- Acceptance criteria or success metrics
- Any specific implementation constraints

**Missing Elements:**
Check for gaps:
- No success criteria defined
- Missing technical requirements
- Unclear scope boundaries
- No error handling specified
- Missing edge cases

#### 4. Verify Specificity

**Specific (Good):**
- "Add dark mode toggle to settings page that persists in localStorage"
- "Fix null pointer exception in login handler when email is empty"
- "Update Python dependencies to latest minor versions"

**Vague (Bad):**
- "Make the UI better"
- "Fix the login bug"
- "Update dependencies"

#### 5. Check Testability

Can you verify completion by:
- Running specific test cases?
- Checking measurable criteria?
- Demonstrating to stakeholder?
- Automated tests passing?

**Not Testable:**
- "Make it feel faster"
- "Improve user experience"
- "Better error handling"

**Testable:**
- "Reduce page load time to under 2 seconds"
- "Show loading spinner during API calls"
- "Display specific error messages for each validation failure"

#### 6. Assess Feasibility

Consider:
- **Technical constraints**: Can current system support this?
- **Dependencies**: Are required libraries/services available?
- **Breaking changes**: Will this break existing functionality?
- **Scope**: Is this one issue or multiple?

### Output Format

Provide structured assessment:

```
Requirement Validation: [CLEAR/NEEDS CLARIFICATION]

✅ Strengths:
- <What's well-defined>
- <Clear aspects>

⚠️ Concerns/Gaps:
- <Missing information>
- <Ambiguities>
- <Unclear aspects>

❓ Questions to Resolve:
1. <Specific question about requirement>
2. <Another question>

Recommendation:
[PROCEED/CLARIFY FIRST]

If clarify first: <Specific points needing clarification>
If proceed: <Summary of what will be implemented>
```

### Decision Matrix

| Criteria | Status | Action |
|----------|--------|--------|
| All clear | ✅ | Proceed with implementation |
| Minor gaps | ⚠️ | Proceed with assumptions, document them |
| Major gaps | ❌ | STOP - Request clarification |
| Ambiguous | ❌ | STOP - Request specific details |

## Examples

### Example 1: Clear requirement
```
Requirement: "Add dark mode toggle to user settings page. Toggle should be
persisted in localStorage and apply theme immediately without page reload."

Validation:
✅ Strengths:
- Clear feature: dark mode toggle
- Specific location: settings page
- Defined behavior: immediate apply, localStorage persistence

⚠️ Concerns/Gaps:
- No mockup/design specified (minor)
- Default theme not specified (assume light)

Recommendation: PROCEED
Implementation is clear. Will use CSS variables for theming.
```

### Example 2: Vague requirement
```
Requirement: "Make the login page better"

Validation:
❌ Concerns/Gaps:
- "Better" is not defined - no success criteria
- No specific issues identified
- No proposed changes mentioned
- No user feedback or pain points provided

❓ Questions to Resolve:
1. What specific problems exist with current login page?
2. What does "better" mean (UX, performance, security)?
3. Are there user complaints or analytics driving this?
4. What specific changes are being requested?

Recommendation: STOP - CLARIFY FIRST
Cannot proceed without understanding what needs improvement.
```

### Example 3: Partially clear requirement
```
Requirement: "Fix the bug where users can't log in"

Validation:
⚠️ Concerns/Gaps:
- Bug description is vague
- No error message or logs provided
- No reproduction steps
- Scope unclear (all users? specific conditions?)

❓ Questions to Resolve:
1. What error appears when login fails?
2. Does this affect all users or specific scenarios?
3. When did this start occurring?
4. What are the steps to reproduce?

Recommendation: STOP - Need reproduction steps and error details
```

### Example 4: Over-specified requirement
```
Requirement: "Add user authentication using JWT tokens with RS256 algorithm,
store tokens in httpOnly cookies, implement refresh token rotation, add
CSRF protection, and integrate with OAuth2 providers (Google, GitHub)"

Validation:
⚠️ Concerns:
- Very large scope for single issue
- Multiple distinct features bundled together
- Should be broken into smaller tasks

✅ Strengths:
- Technically detailed
- Clear security considerations
- Specific technologies mentioned

Recommendation: SUGGEST BREAKING INTO SUBTASKS
1. Basic JWT authentication with RS256
2. Refresh token rotation
3. OAuth2 integration
4. CSRF protection
Each should be separate issue for incremental delivery.
```

### Example 5: Technical constraint check
```
Requirement: "Add real-time collaborative editing to markdown files"

Validation:
⚠️ Feasibility Concerns:
- Requires WebSocket infrastructure (check if available)
- Operational transform or CRDT algorithm needed (complex)
- Conflict resolution strategy required
- May need third-party service

❓ Questions to Resolve:
1. Is WebSocket support available in current stack?
2. Is there budget for third-party service (e.g., Yjs, Automerge)?
3. What's the expected number of concurrent editors?
4. Are there existing collaborative editing libraries we can use?

Recommendation: CLARIFY TECHNICAL APPROACH FIRST
Significant architectural decision needed before implementation.
```
