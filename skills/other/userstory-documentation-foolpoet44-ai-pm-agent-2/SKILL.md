---
name: userstory-documentation
description: User story, epic, and task creation with acceptance criteria. Use when breaking down requirements into user stories, creating epics, writing acceptance criteria, or planning sprints. Triggers on "user story", "epic", "acceptance criteria", "sprint planning", "story points".
allowed-tools: Read, Write, Edit, Grep, Glob
model: inherit
---

# User Story Documentation Skill - Agile Story & Epic Writing

This Skill provides expertise in breaking down product requirements into actionable user stories, epics, and tasks with clear acceptance criteria.

## When to Use This Skill

Use this Skill when you need to:
- Break down PRD into user stories
- Create epics for large features
- Write acceptance criteria
- Decompose stories into tasks
- Estimate story points
- Prioritize backlog
- Plan sprints

## Core Process

### Step 1: Input Analysis

**Required Inputs:**
- Complete PRD (from prd-agent)
- Feature specifications
- User personas
- Business priorities

**If Missing:**
- Request PRD or feature list
- Clarify target users
- Understand technical constraints
- Confirm priority order

### Step 2: Use Reference Templates

**Always read these:**

```bash
# Use Read tool:
/reference/userstory-templates/epic-story-task-structure.md
/reference/userstory-templates/acceptance-criteria-guide.md
/reference/userstory-templates/estimation-techniques.md
```

These provide:
- Epic/Story/Task hierarchy
- INVEST criteria
- Given-When-Then format
- Story point estimation scales
- Prioritization frameworks

### Step 3: Epic-Story-Task Hierarchy

```
Epic (2-8 weeks, large feature area)
├── Story 1 (1-5 days, user-facing feature)
│   ├── Task 1.1 (2-8 hours, technical implementation)
│   ├── Task 1.2
│   └── Task 1.3
├── Story 2
│   ├── Task 2.1
│   └── Task 2.2
└── Story 3
```

### Step 4: Epic Template

```markdown
## Epic ID: [PROJ-E###]
## Epic: [Feature Area Name]

**Description:**
As a [user type],
I want [high-level capability],
So that [business value].

**Business Value:**
- [Why this matters to business]
- [Expected impact on revenue/users/metrics]
- [Strategic alignment]

**Success Metrics:**
- Metric 1: [KPI + Target value]
- Metric 2: [KPI + Target value]
- Metric 3: [KPI + Target value]

**User Stories in this Epic:**
- [ ] [PROJ-001]: [Story name]
- [ ] [PROJ-002]: [Story name]
- [ ] [PROJ-003]: [Story name]
- [ ] [PROJ-004]: [Story name]

**Timeline:** [4-6 weeks estimated]
**Priority:** High | Medium | Low
**Status:** Backlog | Planned | In Progress | Done
```

### Step 5: User Story Template

**INVEST Criteria Check:**
- **I**ndependent: Can develop in any order
- **N**egotiable: Details can be discussed
- **V**aluable: Delivers user value
- **E**stimable: Can be sized
- **S**mall: Fits in one sprint (1-2 weeks)
- **T**estable: Has clear acceptance criteria

**Story Format:**

```markdown
### Story ID: [PROJ-###]
**Title:** [Concise user action/outcome]

**User Story:**
As a [specific user type/persona],
I want to [specific action],
So that [specific benefit/value].

**Acceptance Criteria:**

#### Scenario 1: Happy Path
Given [precondition/context]
When [user action/event]
Then [expected outcome]
And [additional expected outcome]
And [system state]

#### Scenario 2: Error Handling
Given [precondition]
When [error condition occurs]
Then [error is handled]
And [user sees appropriate message]
And [system remains in safe state]

#### Scenario 3: Edge Case
Given [unusual but valid condition]
When [action]
Then [expected behavior]

#### Scenario 4: Validation
Given [invalid input condition]
When [user attempts action]
Then [validation error shown]
And [clear guidance provided]

**Non-Functional Requirements:**
- Performance: [e.g., Response time < 500ms]
- Security: [e.g., Input sanitized, XSS prevented]
- Accessibility: [e.g., Keyboard navigable, ARIA labels]
- Browser Support: [e.g., Chrome, Firefox, Safari latest 2]

**UI/UX Requirements:**
- Loading state: [e.g., Spinner while processing]
- Success feedback: [e.g., Toast "Item added to cart"]
- Error feedback: [e.g., Inline error under field]
- Empty state: [e.g., "No items found" message]

**Priority:** P0 (Must) | P1 (Should) | P2 (Could) | P3 (Won't)
**Story Points:** 1 | 2 | 3 | 5 | 8 | 13
**Sprint:** [Sprint name/number or Backlog]
**Dependencies:** [Story IDs that must complete first]
**Technical Notes:** [Implementation considerations]
**Design:** [Link to mockups/wireframes]

**Definition of Done:**
- [ ] Code complete and peer reviewed
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests passing
- [ ] Acceptance criteria verified
- [ ] Documentation updated
- [ ] No critical/high bugs
- [ ] Product Owner approved
- [ ] Deployed to staging
```

### Step 6: Acceptance Criteria Guidelines

**Format 1: Given-When-Then (Preferred)**
```
Given [context/precondition]
When [action/event]
Then [expected outcome]
And [additional outcome]
```

**Benefits:**
- Clear scenario structure
- Easy to automate (BDD)
- Covers context explicitly

**Example:**
```
Given I am a logged-in user on the product page
When I click "Add to Cart"
Then the item is added to my cart
And the cart count badge updates to show 1 item
And I see a confirmation toast "Item added successfully"
```

**Format 2: Checklist**
```
- [ ] User can [action]
- [ ] System validates [condition]
- [ ] Error displays when [scenario]
```

**Use for:**
- Simple, straightforward features
- Quick reference
- Less complex scenarios

**Coverage Checklist:**

Ensure AC covers:
- [ ] Happy path (successful scenario)
- [ ] Error handling (invalid inputs, system errors)
- [ ] Edge cases (boundary conditions, empty states)
- [ ] Validation rules (format, length, required fields)
- [ ] Performance (load time, response time)
- [ ] Security (auth, authorization, data protection)
- [ ] Accessibility (keyboard nav, screen reader)
- [ ] Visual feedback (loading, success, error states)
- [ ] Cross-browser compatibility
- [ ] Mobile responsiveness (if applicable)

### Step 7: Task Breakdown

**Task Template:**

```markdown
#### Task ID: [PROJ-###-T#]
**Task:** [Technical action to be performed]

**Description:**
[Detailed explanation of what needs to be built/done]

**Technical Approach:**
- [Implementation method]
- [Libraries/frameworks to use]
- [APIs to call]
- [Files to create/modify]

**Acceptance Criteria:**
- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]
- [ ] Unit tests written and passing
- [ ] Code follows style guide
- [ ] No linter errors
- [ ] Peer reviewed

**Estimated Hours:** [X hours]
**Assigned To:** [Developer name or Unassigned]
**Status:** To Do | In Progress | In Review | Done
**Blocked By:** [Task IDs if applicable]
```

**Task Examples:**

```markdown
Story: User Registration

Task 1: Create User Registration API
- POST /api/auth/register endpoint
- Validate email format and password strength
- Hash password with bcrypt
- Store user in database
- Return JWT token
- Estimated: 4 hours

Task 2: Build Registration Form UI
- Email input with validation
- Password input with strength meter
- Confirm password with match validation
- Submit button with loading state
- Error message display
- Estimated: 3 hours

Task 3: Email Verification Service
- Generate verification token
- Send email via SendGrid
- Create verification endpoint
- Handle token expiration
- Estimated: 3 hours

Task 4: Write Tests
- Unit tests for validation logic
- Integration tests for API
- Component tests for UI
- E2E test for full flow
- Estimated: 4 hours
```

### Step 8: Story Point Estimation

**Fibonacci Scale:** 1, 2, 3, 5, 8, 13, 21

| Points | Time | Complexity | Example |
|--------|------|------------|---------|
| 1 | 1-2h | Trivial | Fix typo, update text |
| 2 | 2-4h | Simple | Add field to form |
| 3 | 4-8h | Straightforward | Basic CRUD operation |
| 5 | 1-2d | Moderate | User registration with email |
| 8 | 3-5d | Complex | Payment integration |
| 13 | 1w+ | Very complex | Full auth system - BREAK DOWN |
| 21+ | Too large | Epic-sized | MUST decompose |

**Estimation Factors:**
- Complexity (technical difficulty)
- Effort (amount of work)
- Uncertainty (unknowns, risks)
- Dependencies (external blockers)

**Planning Poker Process:**
1. Product Owner presents story
2. Team asks questions
3. Each member estimates privately
4. Reveal simultaneously
5. Discuss outliers (highest/lowest explain)
6. Re-estimate until consensus

### Step 9: Prioritization

**MoSCoW:**
- **P0 (Must Have)**: Critical, blocking for launch
- **P1 (Should Have)**: Important, not blocking
- **P2 (Could Have)**: Nice to have, time permitting
- **P3 (Won't Have)**: Out of scope this release

**RICE Score:**
```
RICE = (Reach × Impact × Confidence) / Effort

Where:
- Reach: Users affected per quarter
- Impact: 3=massive, 2=high, 1=medium, 0.5=low
- Confidence: 100%=high, 80%=medium, 50%=low
- Effort: Story points or person-months
```

**Example:**
```
Story: Social Login
- Reach: 1000 users/quarter
- Impact: 2 (high - reduces friction)
- Confidence: 80% (medium - tested pattern)
- Effort: 5 story points

RICE = (1000 × 2 × 0.8) / 5 = 320
```

Higher RICE = Higher priority

### Step 10: Complete Epic Breakdown Example

```markdown
# Product: AI Study Planner
# Epic: User Onboarding System

## Epic ID: STUDY-E001
## Epic: User Onboarding and Profile Setup

**Description:**
As a new user,
I want a smooth onboarding experience,
So that I can quickly start using the study planner.

**Business Value:**
- Increase activation rate from 30% to 50%
- Reduce time-to-first-value from 10 min to 3 min
- Improve Day-7 retention by 15%

**Success Metrics:**
- Onboarding completion rate: 60%+
- Time to complete: <3 minutes
- Users who create first study session: 70%+

**User Stories:**
- [ ] STUDY-001: Email/Password Registration
- [ ] STUDY-002: Profile Setup (name, university, major)
- [ ] STUDY-003: Course Import
- [ ] STUDY-004: Study Preferences Configuration
- [ ] STUDY-005: Onboarding Tutorial

**Timeline:** 3 weeks
**Priority:** High

---

### Story ID: STUDY-001
**Title:** Email/Password Registration

**User Story:**
As a prospective user,
I want to register with my email and password,
So that I can create a personal account and save my data.

**Acceptance Criteria:**

#### Scenario 1: Successful Registration
Given I am on the registration page
When I enter a valid email (e.g., "user@university.edu")
And I enter a password meeting requirements (min 8 chars, 1 number, 1 special)
And I confirm the password correctly
And I click "Create Account"
Then my account is created in the system
And I receive a verification email
And I am redirected to the profile setup page (STUDY-002)
And I see a welcome toast "Welcome! Let's set up your profile"

#### Scenario 2: Email Already Exists
Given I am on the registration page
When I enter an email that's already registered
And I click "Create Account"
Then I see an error "This email is already registered"
And I see a link "Log in instead"
And the form does not submit

#### Scenario 3: Password Too Weak
Given I am on the registration page
When I enter a password with fewer than 8 characters
And I click "Create Account"
Then I see an error "Password must be at least 8 characters with 1 number and 1 special character"
And the form does not submit

#### Scenario 4: Passwords Don't Match
Given I am on the registration page
When the password and confirm password fields don't match
And I click "Create Account"
Then I see an error "Passwords do not match"
And the form does not submit

#### Scenario 5: Invalid Email Format
Given I am on the registration page
When I enter an invalid email (e.g., "notanemail")
And I click "Create Account"
Then I see an error "Please enter a valid email address"
And the form does not submit

**Non-Functional Requirements:**
- Security: Password hashed with bcrypt (10 salt rounds)
- Performance: Registration completes in <2 seconds
- Accessibility: Form is keyboard navigable, ARIA labels present
- Browser: Works in Chrome, Firefox, Safari (latest 2 versions)

**UI/UX Requirements:**
- Real-time validation on blur
- Password strength meter (weak/medium/strong)
- Show/hide password toggle
- Loading spinner during submission
- Disabled submit button while processing

**Priority:** P0 (Must Have)
**Story Points:** 5
**Sprint:** Sprint 1
**Dependencies:** None
**Design:** [Link to Figma mockup]

**Tasks:**
- [ ] STUDY-001-T1: Create User model and database schema (2h)
- [ ] STUDY-001-T2: Build POST /api/auth/register endpoint (3h)
- [ ] STUDY-001-T3: Implement email/password validation (2h)
- [ ] STUDY-001-T4: Set up email verification service (3h)
- [ ] STUDY-001-T5: Create registration form UI component (4h)
- [ ] STUDY-001-T6: Add client-side validation (2h)
- [ ] STUDY-001-T7: Write unit tests (backend) (2h)
- [ ] STUDY-001-T8: Write component tests (frontend) (2h)
- [ ] STUDY-001-T9: Integration test for full flow (2h)

**Definition of Done:**
- [ ] All tasks completed
- [ ] Code reviewed and approved
- [ ] All acceptance criteria verified
- [ ] Unit tests >80% coverage
- [ ] Integration tests passing
- [ ] No critical/high bugs
- [ ] Accessibility audit passed
- [ ] QA signed off
- [ ] Product Owner approved
- [ ] Deployed to staging

---

### Story ID: STUDY-002
**Title:** Profile Setup

[Repeat structure]

---

[Continue for remaining stories in Epic]
```

## Best Practices

### Writing User Stories
✅ **Do:**
- Focus on user value, not implementation
- Use specific personas (not "user")
- Keep independent when possible
- Make completable in one sprint
- Include "so that" benefit clause

❌ **Don't:**
- Write technical tasks as stories
- Skip the "so that" (why it matters)
- Make stories dependent unnecessarily
- Combine multiple features
- Use vague language

### Acceptance Criteria
✅ **Do:**
- Use Given-When-Then format
- Cover happy path, errors, edge cases
- Be specific and testable
- Include performance/security/accessibility
- Specify exact error messages
- Document loading/empty states

❌ **Don't:**
- Be vague ("works well", "is fast")
- Only test happy path
- Skip error handling
- Forget edge cases
- Leave untestable criteria
- Include implementation details

### Task Breakdown
✅ **Do:**
- Break into 2-8 hour chunks
- Include testing in tasks
- Assign clear ownership
- Specify technical approach
- Estimate hours realistically

❌ **Don't:**
- Create multi-day tasks
- Forget testing tasks
- Skip implementation details
- Leave tasks unassigned too long
- Underestimate complexity

## Output Format

**File Naming:**
```
[product]-user-stories-v[version].md
Example: study-planner-user-stories-v1.0.md
```

**Structure:**
```
# Product Name - User Stories

## Epic 1: [Name]
[Epic details]

### Story 1.1
[Story details]

### Story 1.2
[Story details]

## Epic 2: [Name]
[Repeat]
```

## Integration Points

This Skill works with:
- **userstory-agent**: Primary user of this skill
- **prd-documentation**: Takes PRD as input
- **pm-knowledge-base**: Uses estimation, prioritization frameworks

Always use reference templates to ensure consistency and completeness.
