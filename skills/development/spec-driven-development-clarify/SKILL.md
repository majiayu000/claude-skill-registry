---
name: spec_driven_development.clarify
description: "Resolves ambiguities and gaps in the specification through structured questioning. Use after specification to ensure completeness."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **Ambiguities Identified**: Were underspecified areas systematically identified?
            2. **Questions Asked**: Did the agent ask structured questions to resolve each ambiguity?
            3. **Answers Documented**: Are clarification answers recorded in the spec document?
            4. **Edge Cases Covered**: Are edge cases and error scenarios now defined?
            5. **Acceptance Checklist**: Is the acceptance criteria checklist complete and validated?
            6. **Spec Updated**: Has spec.md been updated with all clarifications?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response AND
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met OR the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
  SubagentStop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **Ambiguities Identified**: Were underspecified areas systematically identified?
            2. **Questions Asked**: Did the agent ask structured questions to resolve each ambiguity?
            3. **Answers Documented**: Are clarification answers recorded in the spec document?
            4. **Edge Cases Covered**: Are edge cases and error scenarios now defined?
            5. **Acceptance Checklist**: Is the acceptance criteria checklist complete and validated?
            6. **Spec Updated**: Has spec.md been updated with all clarifications?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response AND
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met OR the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
---

# spec_driven_development.clarify

**Step 3/6** in **spec_driven_development** workflow

> Spec-driven development workflow that turns specifications into working implementations through structured planning.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/spec_driven_development.specify`

## Instructions

**Goal**: Resolves ambiguities and gaps in the specification through structured questioning. Use after specification to ensure completeness.

# Clarify Specification

## Objective

Resolve ambiguities, fill gaps, and validate completeness of the specification through systematic questioning. The goal is to ensure the spec is detailed enough for technical planning.

## Task

Review the existing specification, identify underspecified areas, and ask structured questions to resolve them. Update the spec.md with clarifications.

**Important**: Use the AskUserQuestion tool to ask structured questions when gathering information from the user.

**Critical**: This step refines requirements, not implementation. Do not add code examples or technical solutions. Keep clarifications focused on user needs, acceptance criteria, and behavior - not how things will be coded.

### Prerequisites

Before starting, verify:

1. The specification exists at `specs/[feature-name]/spec.md`
2. Read the specification thoroughly

If no specification exists, inform the user they should run `/spec_driven_development.specify` first.

### Step 1: Identify the Feature

Ask the user which feature specification to clarify:

```
Which feature specification would you like to clarify?
```

If they provide a name, look for `specs/[feature-name]/spec.md`.

### Step 2: Analyze for Ambiguities

Read the specification and identify gaps in these categories:

1. **Underspecified User Stories**
   - Stories missing acceptance criteria
   - Vague or unmeasurable criteria
   - Missing edge case definitions

2. **Unclear Requirements**
   - Requirements with ambiguous language ("fast", "user-friendly", "secure")
   - Missing quantitative thresholds
   - Undefined terms or jargon

3. **Missing Scenarios**
   - Error handling not defined
   - Edge cases not covered
   - Multi-user scenarios not addressed

4. **Integration Gaps**
   - Undefined interactions with other features
   - Missing data flow definitions
   - Unclear state transitions

5. **Open Questions**
   - Any questions listed in the "Open Questions" section
   - Implicit assumptions that need validation

### Step 3: Systematic Clarification

For each ambiguity identified, ask structured questions:

**Format your questions systematically:**

```
I've identified [N] areas that need clarification in your specification.

**Ambiguity 1: [Category] - [Brief Description]**

The spec says: "[Quote from spec]"

This is ambiguous because: [Explanation]

Question: [Specific clarifying question]

Options:
- [Option A with implications]
- [Option B with implications]
- [Other - user can specify]
```

**Question best practices:**

- One topic per question
- Provide options when possible
- Explain implications of each option
- Reference specific parts of the spec

### Step 4: Validate Edge Cases

For each user story, ensure edge cases are covered:

1. **What happens if the user...**
   - Provides invalid input?
   - Cancels midway?
   - Loses connection?
   - Times out?

2. **What happens when...**
   - The system is under load?
   - Required data is missing?
   - External services are unavailable?

3. **What about...**
   - First-time users vs returning users?
   - Different user permission levels?
   - Concurrent access scenarios?

### Step 5: Update the Specification

After gathering clarifications, update `specs/[feature-name]/spec.md`:

1. **Add a Clarifications section:**

   ```markdown
   ## Clarifications

   ### [Date] Clarification Session

   **Q1: [Original question]**
   A: [Answer received]
   Impact: [How this affects the spec]

   **Q2: [Original question]**
   A: [Answer received]
   Impact: [How this affects the spec]
   ```

2. **Update affected sections:**
   - Refine vague acceptance criteria with specific thresholds
   - Add missing edge cases to user stories
   - Update non-functional requirements with concrete numbers
   - Remove or resolve open questions

3. **Mark resolved questions:**
   - Move resolved items from "Open Questions" to "Clarifications"
   - Add any new questions discovered during clarification

### Step 6: Validate Acceptance Checklist

Create or update an acceptance checklist:

```markdown
## Acceptance Checklist

### User Stories

- [ ] All stories have 3+ acceptance criteria
- [ ] All criteria are testable/measurable
- [ ] Edge cases are documented

### Requirements

- [ ] Performance thresholds defined (response times, throughput)
- [ ] Security requirements are specific
- [ ] Accessibility standards identified

### Scope

- [ ] In-scope items are detailed
- [ ] Out-of-scope items are explicit
- [ ] Assumptions are documented

### Completeness

- [ ] No open questions remain
- [ ] All ambiguities resolved
- [ ] Ready for technical planning
```

## Example Dialog

```
Claude: I'll help clarify the specification. Which feature would you like to work on?

User: user-authentication

Claude: Let me review the spec at `specs/user-authentication/spec.md`...

[Reads specification]

I've identified 4 areas that need clarification:

**Ambiguity 1: Performance - "Quick signup flow"**

The spec says: "The whole flow should take under a minute"

This is ambiguous because: It's unclear if this refers to user time, system response time,
or includes email verification.

What does "under a minute" mean for the signup flow?

[Uses AskUserQuestion with options:
- User can complete form in under 1 minute (not including email verification)
- System processes signup in under 1 minute (including sending verification email)
- End-to-end including email verification click
- Other]

User: User can complete form in under 1 minute, not including verification

Claude: Got it. I'll update the spec to say:
"Users can complete the signup form within 60 seconds. Email verification is asynchronous
and not included in this timing."

**Ambiguity 2: Security - "Email verification required"**

The spec doesn't define what happens if verification isn't completed.

What should happen to unverified accounts?

[Uses AskUserQuestion with options:
- Allow limited access for 24 hours, then restrict
- No access until verified
- Full access but with reminder prompts
- Other]

User: Allow limited access for 24 hours

Claude: What does "limited access" mean? What can unverified users do vs not do?

[Continues clarification...]

After resolving all ambiguities:

✓ Specification clarified!

**Updates made to** specs/user-authentication/spec.md:
- Added 4 clarifications with answers
- Updated 3 acceptance criteria with specific thresholds
- Added 5 edge cases to user stories
- Resolved all open questions

**Acceptance checklist:** All items complete ✓

**Next step:**
Run `/spec_driven_development.plan` to create the technical implementation plan.
```

## Output Format

### Updated specs/[feature-name]/spec.md

The specification file updated with:

- Clarifications section with Q&A
- Refined acceptance criteria
- Additional edge cases
- Resolved open questions
- Acceptance checklist (all items checked)

**Location**: `specs/[feature-name]/spec.md` (same file, updated)

After updating the file:

1. Summarize the clarifications made
2. Confirm the acceptance checklist is complete
3. Tell the user to run `/spec_driven_development.plan` to create the technical plan

## Quality Criteria

- All ambiguities in the spec were identified
- Structured questions were asked for each ambiguity
- Answers are documented in Clarifications section
- Acceptance criteria now have specific, measurable thresholds
- Edge cases are comprehensively covered
- Open questions are resolved
- Acceptance checklist is complete
- Spec is ready for technical planning
- **No implementation code**: Clarifications describe behavior, not code



## Required Inputs


**Files from Previous Steps** - Read these first:
- `specs/[feature-name]/spec.md` (from `specify`)

## Work Branch

Use branch format: `deepwork/spec_driven_development-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/spec_driven_development-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `specs/[feature-name]/spec.md`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

Stop hooks will automatically validate your work. The loop continues until all criteria pass.

**Criteria (all must be satisfied)**:
1. **Ambiguities Identified**: Were underspecified areas systematically identified?
2. **Questions Asked**: Did the agent ask structured questions to resolve each ambiguity?
3. **Answers Documented**: Are clarification answers recorded in the spec document?
4. **Edge Cases Covered**: Are edge cases and error scenarios now defined?
5. **Acceptance Checklist**: Is the acceptance criteria checklist complete and validated?
6. **Spec Updated**: Has spec.md been updated with all clarifications?


**To complete**: Include `<promise>✓ Quality Criteria Met</promise>` in your final response only after verifying ALL criteria are satisfied.

## On Completion

1. Verify outputs are created
2. Inform user: "Step 3/6 complete, outputs: specs/[feature-name]/spec.md"
3. **Continue workflow**: Use Skill tool to invoke `/spec_driven_development.plan`

---

**Reference files**: `.deepwork/jobs/spec_driven_development/job.yml`, `.deepwork/jobs/spec_driven_development/steps/clarify.md`