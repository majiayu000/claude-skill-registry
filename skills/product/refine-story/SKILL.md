---
name: refine-story
description: Transform vague or incomplete user stories into sprint-ready stories with clear acceptance criteria, test scenarios, and technical guidance. This skill should be used before sprint commitment for definition of ready check.
acceptance:
  - story_quality_improved: "Story quality score increased by at least 1 point on 4-point scale"
  - acceptance_criteria_complete: "At least 5 specific, testable acceptance criteria defined"
  - technical_guidance_provided: "Technical notes added with tech stack, patterns, security, and data models"
  - definition_of_ready_met: "Story meets all 6 INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)"
inputs:
  story_id:
    type: string
    required: true
    description: "ID of story file in .claude/stories/"
  focus:
    type: enum
    values: ["all", "acceptance-criteria", "technical-notes", "edge-cases", "test-scenarios"]
    default: "all"
    description: "Specific aspect to focus refinement on"
  interactive:
    type: boolean
    default: false
    description: "Ask user questions during refinement for clarification"
outputs:
  refined_story:
    type: object
    description: "Updated story with enhanced narrative, AC, technical notes, edge cases, test scenarios"
  quality_score_before:
    type: number
    description: "Quality score before refinement (0-4 scale)"
  quality_score_after:
    type: number
    description: "Quality score after refinement (0-4 scale)"
  ready_for_sprint:
    type: boolean
    description: "Whether story meets definition of ready"
  refinement_report:
    type: string
    description: "Path to detailed refinement report file"
telemetry:
  emit: "skill.refine-story.completed"
  track:
    - story_id
    - duration_ms
    - quality_score_before
    - quality_score_after
    - quality_improvement
    - ac_count_before
    - ac_count_after
    - ready_for_sprint
---

# Story Refinement

Transform vague, incomplete, or ambiguous user stories into clear, sprint-ready stories with well-defined acceptance criteria, test scenarios, and technical guidance.

## Purpose

Apply structured refinement techniques to improve story quality:
- Enhance user story narrative (As a... I want... So that...)
- Develop comprehensive acceptance criteria (5-8 specific, testable AC)
- Add technical guidance (tech stack, patterns, security, data models)
- Identify edge cases (boundary conditions, unusual input, concurrency)
- Create test scenarios (unit, integration, E2E)
- Ensure definition of ready compliance (INVEST criteria)

## When to Use This Skill

This skill should be used when:
- Story has vague or unclear requirements
- Acceptance criteria are missing or incomplete
- Story is too large and needs decomposition
- Technical approach is unclear
- Before sprint commitment (definition of ready check)
- After stakeholder feedback requiring clarification

This skill should NOT be used when:
- Story already has comprehensive AC and technical notes
- Story is just being created (use breakdown-epic first)
- Story is in progress (use refine-task instead)

## Prerequisites

- Story file must exist in `.claude/stories/`
- Basic user story narrative present (or at minimum a title)
- General understanding of feature context

## Sequential Refinement Process

Execute steps in order - each builds on previous enhancements:

### Step 0: Load Story and Assess Quality

**Purpose:** Evaluate current story quality against definition of ready.

**Actions:**

1. Read story file from `.claude/stories/{story-id}.md`

2. Parse story components:
   - Title
   - User story narrative (As a... I want... So that...)
   - Acceptance criteria
   - Technical notes
   - Edge cases
   - Test scenarios
   - Dependencies

3. Assess quality against definition of ready (INVEST):
   - **Independent:** Can be worked on without other stories
   - **Negotiable:** Flexible on implementation details
   - **Valuable:** Delivers clear value to user/business
   - **Estimable:** Team can estimate with confidence
   - **Small:** Fits in one sprint (typically ≤13 points)
   - **Testable:** Clear how to verify it works

4. Calculate quality score (0-4 scale):
   ```
   Quality Score = Average of:
   - Title quality (1-4)
   - Narrative quality (1-4)
   - AC quality (1-4)
   - Technical notes quality (1-4)
   - Edge cases coverage (1-4)
   - Dependencies clarity (1-4)
   ```

5. Identify specific gaps and determine refinement strategy

**Output:** Story assessment with current quality score (0-4 scale), sprint readiness (yes/no), issues identified (list), estimated refinement time

**See:** `references/templates.md#step-0-story-quality-assessment-output` for complete format and scoring rubric

**Reference:** See [story-quality-assessment.md](references/story-quality-assessment.md) for detailed assessment criteria.

---

### Step 1: Enhance User Story Narrative

**Purpose:** Transform vague narrative into clear, valuable user story.

**Standard Format:**
```
As a [persona],
I want to [action],
So that [benefit/value].
```

**Actions:**

1. **Identify Persona:**
   - Who is the user? (end user, admin, system, developer)
   - Be specific: "registered user" not just "user"

2. **Clarify Action:**
   - What does user want to do?
   - Use specific, action-oriented verbs
   - Avoid technical jargon unless developer story

3. **Articulate Value:**
   - Why does user want this?
   - What problem does it solve?
   - What outcome does it enable?

**Example:** "Users should be able to login" → "As a registered user, I want to log in with my email and password so that I can access my personalized account and data securely" (added persona, specified mechanism, articulated value)

**See:** `references/templates.md#step-1-user-story-narrative-refinement` for more before/after examples and patterns

---

### Step 2: Develop Comprehensive Acceptance Criteria

**Purpose:** Define specific, testable criteria for "done".

**AC Best Practices:**
- **Specific:** No ambiguity about what needs to be true
- **Testable:** Can verify with a test case
- **Implementation-independent:** What, not how
- **User-focused:** From user perspective when possible
- **Numbered:** For easy reference (AC-1, AC-2, etc.)

**AC Categories to Cover:**

1. **Happy Path** (2-3 AC): Core functionality working correctly
2. **Validation** (2-3 AC): Input validation and format checking
3. **Error Handling** (2-3 AC): Failure scenarios with clear error messages
4. **Security** (1-2 AC): Authentication, authorization, data protection
5. **Performance** (1 AC): Response time or throughput requirements

**Example:** 2 vague AC ("Login works", "Error handling") → 11 specific, testable AC organized by category (Happy Path: 3, Validation: 2, Error Handling: 2, Security: 3, Performance: 1)

**See:** `references/templates.md#step-2-acceptance-criteria-development` for complete before/after examples and AC development patterns

**Reference:** See [refinement-techniques.md](references/refinement-techniques.md) for AC development patterns.

---

### Step 3: Identify and Document Edge Cases

**Purpose:** Anticipate boundary conditions, unusual inputs, and failure scenarios.

**Edge Case Categories:**

1. **Boundary Conditions:** Min/max lengths, exactly at limit values
2. **Unusual Input:** Special characters, unicode, whitespace
3. **Timing & Concurrency:** Simultaneous requests, race conditions
4. **State Transitions:** User already logged in, account changes mid-operation
5. **External Dependencies:** Database down, Redis unavailable, network failures
6. **Security Scenarios:** Brute force, injection attempts, XSS

**Example:** For login story, identify 7+ edge cases: boundary (min password length), unusual input (+symbol in email, whitespace), concurrency (simultaneous logins), state transitions (password change mid-login), external dependencies (DB down), security (brute force)

**See:** `references/templates.md#step-3-edge-cases-identification` for complete edge case examples and identification guide

**Reference:** See [refinement-techniques.md](references/refinement-techniques.md) for edge case identification guide.

---

### Step 4: Add Technical Guidance

**Purpose:** Provide technical context for implementation.

**Technical Notes Structure:**

1. **Technology Stack:** Languages, frameworks, libraries to use
2. **Architecture Patterns:** Repository, service layer, middleware patterns
3. **Security Considerations:** Hashing algorithms, rate limiting, validation
4. **Data Models:** Database schemas, field types, relationships
5. **API Contracts:** Request/response formats, status codes
6. **Performance Requirements:** Response times, throughput, indexes

**Example:** For login story, add tech stack (Node/Express/PostgreSQL/Redis/bcrypt/JWT), implementation approach (3-layer architecture), security (password hashing, rate limiting, no enumeration), data models (users table with lockout fields), API contract (POST endpoint with request/response formats), performance targets (< 500ms p95)

**See:** `references/templates.md#step-4-technical-guidance` for complete technical notes templates and examples

**Reference:** See [story-templates.md](references/story-templates.md) for technical notes templates.

---

### Step 5: Create Test Scenarios

**Purpose:** Define how to verify story works correctly.

**Test Types:**

1. **Unit Tests** (Fast, Isolated): Test individual functions
2. **Integration Tests** (Medium, With Dependencies): Test multiple components
3. **E2E Tests** (Slow, Full System): Test complete workflows
4. **Performance Tests** (Optional): Test under load

**Example:** For login story, create unit tests (email validation, password hashing), integration tests (success, failure, lockout), E2E tests (complete signup → login → protected access flow)

**See:** `references/templates.md#step-5-test-scenarios` for complete test scenario templates and examples

**Reference:** See [refinement-techniques.md](references/refinement-techniques.md) for test scenario templates.

---

### Step 6: Define Story Size and Splitting Criteria

**Purpose:** Ensure story fits in one sprint (≤13 points).

**Size Categories:**
- **XS (1-2 points):** < 4 hours, minimal complexity
- **S (3-5 points):** 4-8 hours, moderate complexity
- **M (8 points):** 1-2 days, higher complexity
- **L (13 points):** 2-3 days, very complex
- **XL (21+ points):** MUST SPLIT

**Splitting Triggers:**
- Estimated at > 13 points
- More than 10 acceptance criteria
- Involves 3+ distinct components
- Team has low confidence in estimate (<70%)

**Splitting Strategies:**
1. By workflow steps (signup → verify email → complete profile)
2. By CRUD operations (view → edit → delete)
3. By persona (standard user → admin)
4. By priority (MVP → nice-to-have → future)
5. By happy path vs edge cases

**Reference:** See [refinement-techniques.md](references/refinement-techniques.md) for detailed splitting strategies.

---

### Step 7: Update Story File with Refinements

**Purpose:** Save all refinements to story file.

**Updated Story Structure:** Story file includes title, ID, priority, status, estimate, user story (As a/I want/So that), categorized AC, technical notes, edge cases, test scenarios, dependencies, definition of done checklist

**See:** `references/templates.md#step-7-complete-story-file-structure` for full template and complete login story example

**Reference:** See [story-templates.md](references/story-templates.md) for complete story template.

---

### Step 8: Generate Refinement Report

**Purpose:** Document changes made and quality improvement.

**Report File:** `.claude/refinements/{story-id}-refinement-{date}.md`

**Report Contents:** Summary (quality before/after, sprint readiness), key improvements (narrative, AC count, technical notes, edge cases, test scenarios), specific changes (before/after comparisons), definition of ready assessment table, quality score breakdown, next steps (estimate, add to sprint, assign)

**See:** `references/templates.md#step-8-refinement-report-template` for complete report format with all sections

---

### Step 9: Present Refinement Summary to User

**Purpose:** Communicate improvements clearly.

**Summary Format:** Display completion status, story ID/title, quality improvement (before/after/change), key enhancements checklist, sprint readiness, files updated, next steps (estimate, add to sprint, implement)

**See:** `references/templates.md#step-9-refinement-summary` for complete summary format

---

## Common Refinement Patterns

**Login Story:** "Users can log in" → add persona, mechanism (email+password), AC (validation/errors/security), tech notes (JWT/bcrypt/rate limiting)
**CRUD Story:** "Manage profile" → split into View/Edit/Delete (3 stories) with specific AC, API contracts, validation
**Integration Story:** "Integrate payment" → add value, AC (success/failures/refunds), tech notes (API keys/webhooks/PCI compliance)

**See:** `references/integration-patterns.md` and `references/templates.md` for more refinement patterns and examples

---

## Integration with Other Skills

**Before Refinement:**
- `breakdown-epic` → Create initial stories from epic (stories start rough, need refinement)

**After Refinement:**
- `estimate-stories` → Estimate refined stories (refinement increases confidence)
- `sprint-plan` → Add to sprint plan
- `implement-feature` → Implement with clear guidance

---

## Best Practices

Refine collaboratively (involve dev/QA/PO) | Keep stories independent (minimize dependencies) | Make AC testable (specific numbers, exact error messages) | Document assumptions (what exists, what we're NOT building) | Balance detail vs flexibility (enough to estimate/implement, not constraining)

**See:** `references/integration-patterns.md` for workflow integration details

---

## References

Detailed documentation in `references/`:

- **templates.md**: All output formats, before/after examples, complete story templates, refinement reports, test scenarios, technical notes templates, splitting strategies, AC development patterns
- **story-quality-assessment.md**: Quality matrix, definition of ready, assessment criteria, INVEST evaluation
- **refinement-techniques.md**: AC development patterns, edge case identification, test scenario creation, story splitting strategies
- **story-templates.md**: Before/after story examples, story file structures, technical notes templates
- **integration-patterns.md**: Common refinement patterns, workflow integration with other skills, best practices
