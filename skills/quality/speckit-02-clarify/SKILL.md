---
name: speckit-02-clarify
description: Identify underspecified areas and ask targeted clarification questions
---

# Spec-Kit Clarify

Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Constitution Loading (REQUIRED)

Before ANY action, load and internalize the project constitution:

1. Read constitution:
   ```bash
   cat .specify/memory/constitution.md 2>/dev/null || echo "NO_CONSTITUTION"
   ```

2. If exists, parse all principles, constraints, and governance rules.

## Prerequisites Check

1. Run prerequisites check:
   ```bash
   .specify/scripts/bash/check-prerequisites.sh --json --paths-only
   ```

2. Parse JSON for:
   - `FEATURE_DIR`
   - `FEATURE_SPEC`

3. If JSON parsing fails, abort and instruct user to run `/speckit-01-specify` first.

## Goal

Detect and reduce ambiguity or missing decision points in the active feature specification and record the clarifications directly in the spec file.

**Note**: This clarification workflow should run BEFORE invoking `/speckit-03-plan`. If the user explicitly states they are skipping clarification, proceed but warn that downstream rework risk increases.

## Execution Steps

### 1. Load Spec and Scan for Ambiguities

Load the current spec file and perform a structured ambiguity & coverage scan using this taxonomy. For each category, mark status: Clear / Partial / Missing.

**Functional Scope & Behavior:**
- Core user goals & success criteria
- Explicit out-of-scope declarations
- User roles / personas differentiation

**Domain & Data Model:**
- Entities, attributes, relationships
- Identity & uniqueness rules
- Lifecycle/state transitions
- Data volume / scale assumptions

**Interaction & UX Flow:**
- Critical user journeys / sequences
- Error/empty/loading states
- Accessibility or localization notes

**Non-Functional Quality Attributes:**
- Performance (latency, throughput targets)
- Scalability (horizontal/vertical, limits)
- Reliability & availability
- Observability (logging, metrics, tracing)
- Security & privacy
- Compliance / regulatory constraints

**Integration & External Dependencies:**
- External services/APIs and failure modes
- Data import/export formats
- Protocol/versioning assumptions

**Edge Cases & Failure Handling:**
- Negative scenarios
- Rate limiting / throttling
- Conflict resolution

**Constraints & Tradeoffs:**
- Technical constraints
- Explicit tradeoffs or rejected alternatives

**Terminology & Consistency:**
- Canonical glossary terms
- Avoided synonyms / deprecated terms

**Completion Signals:**
- Acceptance criteria testability
- Measurable Definition of Done indicators

### 2. Generate Question Queue

Generate a prioritized queue of candidate clarification questions (maximum 5).

**Constraints:**
- Each question must be answerable with EITHER:
  - A short multiple-choice selection (2-5 options), OR
  - A one-word / short-phrase answer (<=5 words)
- Only include questions whose answers materially impact architecture, data modeling, task decomposition, test design, UX behavior, operational readiness, or compliance validation
- Ensure category coverage balance
- Exclude questions already answered
- Favor clarifications that reduce downstream rework risk

### 3. Sequential Questioning Loop

Present EXACTLY ONE question at a time.

**For multiple-choice questions:**

1. **Analyze all options** and determine the **most suitable option** based on:
   - Best practices for the project type
   - Common patterns in similar implementations
   - Risk reduction (security, performance, maintainability)
   - Alignment with project goals or constraints

2. Present your **recommended option prominently**:
   ```
   **Recommended:** Option [X] - <reasoning>
   ```

3. Render all options as a table:

   | Option | Description |
   |--------|-------------|
   | A | Option A description |
   | B | Option B description |
   | C | Option C description |
   | Short | Provide a different short answer (<=5 words) |

4. Add: `You can reply with the option letter (e.g., "A"), accept the recommendation by saying "yes" or "recommended", or provide your own short answer.`

**After user answers:**
- If user replies with "yes", "recommended", or "suggested", use your stated recommendation
- Validate the answer maps to one option or fits the <=5 word constraint
- If ambiguous, ask for quick disambiguation
- Record in working memory and move to next question

**Stop asking when:**
- All critical ambiguities resolved early
- User signals completion ("done", "good", "no more")
- You reach 5 asked questions

### 4. Integration After Each Answer

For each accepted answer:

1. Ensure a `## Clarifications` section exists in the spec
2. Under it, create a `### Session YYYY-MM-DD` subheading for today
3. Append: `- Q: <question> -> A: <final answer>`
4. Apply the clarification to the appropriate section:
   - Functional ambiguity -> Functional Requirements
   - User interaction -> User Stories
   - Data shape -> Data Model
   - Non-functional constraint -> Quality Attributes
   - Edge case -> Edge Cases / Error Handling
   - Terminology conflict -> Normalize across spec

5. **Save the spec file AFTER each integration** to minimize risk of context loss

### 5. Validation

After EACH write plus final pass:
- Clarifications session contains exactly one bullet per accepted answer
- Total asked questions <= 5
- Updated sections contain no lingering vague placeholders
- No contradictory earlier statements remain
- Markdown structure valid

### 6. Report Completion

Output:
- Number of questions asked & answered
- Path to updated spec
- Sections touched
- Coverage summary table:

| Category | Status |
|----------|--------|
| [Category] | Resolved / Deferred / Clear / Outstanding |

- If Outstanding or Deferred remain, recommend next steps
- Suggested next command (`/speckit-03-plan`)

## Behavior Rules

- If no meaningful ambiguities found, respond: "No critical ambiguities detected worth formal clarification." and suggest proceeding
- If spec file missing, instruct user to run `/speckit-01-specify` first
- Never exceed 5 total asked questions
- Avoid speculative tech stack questions unless absence blocks functional clarity
- Respect user early termination signals ("stop", "done", "proceed")

## Next Steps

After completing clarification:
- Run `/speckit-03-plan` to create the technical implementation plan

The plan skill will validate that the spec exists before proceeding.
